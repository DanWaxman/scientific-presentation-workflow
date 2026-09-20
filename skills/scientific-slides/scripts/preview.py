#!/usr/bin/env python3
"""Capture an offline Reveal deck's final slides or every fragment state."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlencode


INVENTORY = """() => Reveal.getSlides().map((slide, i) => {
  const position = Reveal.getIndices(slide);
  const fragments = [...new Set([...slide.querySelectorAll('.fragment')]
    .map(el => Number(el.dataset.fragmentIndex)).filter(Number.isFinite))]
    .sort((a, b) => a - b);
  return { number: i + 1, h: position.h, v: position.v || 0,
    title: (slide.querySelector('h1,h2,h3')?.textContent || slide.id || `Slide ${i + 1}`).trim(),
    fragments };
})"""

PREPARE_MEDIA = """async (videoTime) => {
  const slide = Reveal.getCurrentSlide();
  const visible = el => {
    const style = getComputedStyle(el);
    return style.visibility !== 'hidden' && style.display !== 'none' &&
      !el.closest('.fragment:not(.visible)') && el.getBoundingClientRect().width > 0;
  };
  const issues = [];
  for (const img of slide.querySelectorAll('img')) {
    if (!visible(img)) continue;
    if (!img.complete) await Promise.race([
      new Promise(resolve => { img.addEventListener('load', resolve, {once:true});
        img.addEventListener('error', resolve, {once:true}); }),
      new Promise(resolve => setTimeout(resolve, 5000))
    ]);
    if (!img.complete || !img.naturalWidth) issues.push(`Image did not load: ${img.getAttribute('src')}`);
  }
  for (const video of slide.querySelectorAll('video')) {
    if (!visible(video)) continue;
    video.pause();
    if (video.readyState < 2) {
      await Promise.race([
        new Promise(resolve => { video.addEventListener('loadeddata', resolve, {once:true});
          video.addEventListener('error', resolve, {once:true}); video.load(); }),
        new Promise(resolve => setTimeout(resolve, 5000))
      ]);
    }
    if (video.readyState < 2 || video.error) {
      issues.push(`Video did not load: ${video.currentSrc || video.getAttribute('src')}`);
      continue;
    }
    const time = Math.min(videoTime, Math.max(0, video.duration - 0.05));
    if (Math.abs(video.currentTime - time) > 0.001) {
      await Promise.race([
        new Promise(resolve => { video.addEventListener('seeked', resolve, {once:true}); video.currentTime = time; }),
        new Promise(resolve => setTimeout(resolve, 3000))
      ]);
    }
    video.pause();
  }
  for (const el of slide.querySelectorAll('.katex-error')) issues.push(`KaTeX error: ${el.textContent}`);
  return issues;
}"""


def slide_selection(value: str | None, count: int) -> list[int]:
    if value is None:
        return list(range(1, count + 1))
    try:
        selected = sorted(set(int(item.strip()) for item in value.split(",")))
    except ValueError as exc:
        raise ValueError("--slides expects comma-separated numbers, such as 1,3,5") from exc
    if not selected or any(number < 1 or number > count for number in selected):
        raise ValueError(f"slide numbers must be between 1 and {count}")
    return selected


def contact_sheet(output: Path, states: list[dict]) -> None:
    from PIL import Image, ImageDraw

    columns, width, height, label_height = 3, 384, 280, 32
    rows = (len(states) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * width, rows * (height + label_height)), "#e7e7e7")
    draw = ImageDraw.Draw(sheet)
    for i, state in enumerate(states):
        x, y = (i % columns) * width, (i // columns) * (height + label_height)
        with Image.open(output / state["filename"]) as screenshot:
            screenshot = screenshot.convert("RGB")
            screenshot.thumbnail((width - 8, height - 8))
            sheet.paste(screenshot, (x + (width - screenshot.width) // 2, y + 4))
        text = f"{state['number']}: {state['title']} / {state['state']}"
        draw.text((x + 6, y + height + 4), text[:59], fill="#222222")
    sheet.save(output / "contact-sheet.png")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", type=Path, help="directory containing index.html")
    parser.add_argument("--all-fragments", action="store_true", help="include initial state and each reveal")
    parser.add_argument("--slides", help="comma-separated, one-based slide numbers; default: all")
    parser.add_argument("--sheet", action="store_true", help="also make a contact sheet (requires Pillow)")
    parser.add_argument("--browser", default=os.environ.get("SLIDES_BROWSER"), help="Chromium executable; defaults to Playwright's Chromium")
    parser.add_argument("--out", type=Path, help="output parent; default: DECK/.preview")
    parser.add_argument("--scale", type=float, default=1.0, help="screenshot scale of 960×700; default: 1 (presentation size)")
    parser.add_argument("--settle-ms", type=int, default=850, help="wait after each navigation for transitions; default: 850")
    parser.add_argument("--video-time", type=float, default=0.0, help="seek visible videos to this many seconds for snapshots")
    parser.add_argument("--reduced-motion", choices=("reduce", "no-preference"), default="no-preference")
    args = parser.parse_args()
    if args.scale <= 0 or args.settle_ms < 0 or args.video_time < 0:
        parser.error("scale must be positive; settle time and video time must be nonnegative")
    deck = args.deck.expanduser().resolve()
    entry = deck / "index.html"
    if not entry.is_file():
        parser.error(f"deck not found: {entry}")
    try:
        from playwright.sync_api import sync_playwright
        if args.sheet:
            import PIL  # noqa: F401
    except ImportError:
        parser.error("install review dependencies: python -m pip install playwright pillow; then python -m playwright install chromium")
    output_parent = (args.out.expanduser() if args.out else deck / ".preview").absolute()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    output = output_parent / f"review-{stamp}"
    output.mkdir(parents=True, exist_ok=False)
    errors: list[str] = []
    states: list[dict] = []
    manifest = {
        "deck": str(deck), "created_utc": stamp, "offline": True,
        "scale": args.scale, "reduced_motion": args.reduced_motion,
        "video_time": args.video_time, "slides": [], "states": states, "errors": errors,
    }
    try:
        with sync_playwright() as playwright:
            options = {"headless": True}
            if args.browser:
                options["executable_path"] = str(Path(args.browser).expanduser())
            browser = playwright.chromium.launch(**options)
            context = browser.new_context(
                viewport={"width": round(960 * args.scale), "height": round(700 * args.scale)},
                device_scale_factor=1, reduced_motion=args.reduced_motion,
            )

            def block_network(route) -> None:
                if route.request.url.startswith(("http://", "https://")):
                    errors.append(f"Blocked external request: {route.request.url}")
                    route.abort()
                else:
                    route.continue_()

            context.route("**/*", block_network)
            page = context.new_page()
            page.on("pageerror", lambda error: errors.append(f"JavaScript: {error}"))
            page.on("requestfailed", lambda request: errors.append(f"Request failed: {request.url} ({request.failure})"))
            page.on("console", lambda message: errors.append(f"Browser: {message.text}") if message.type == "error" else None)
            query = urlencode({"controls": "false", "progress": "false", "slideNumber": "false"})
            page.goto(f"{entry.as_uri()}?{query}", wait_until="load", timeout=30000)
            page.wait_for_function("window.Reveal && Reveal.isReady()", timeout=15000)
            page.evaluate("() => { Reveal.configure({ margin: 0, controls: false, progress: false, slideNumber: false }); Reveal.layout(); }")
            page.evaluate("() => document.fonts.ready")
            inventory = page.evaluate(INVENTORY)
            manifest["slides"] = inventory
            selected = slide_selection(args.slides, len(inventory))
            for slide in inventory:
                if slide["number"] not in selected:
                    continue
                fragments = [-1, *slide["fragments"]] if args.all_fragments else [slide["fragments"][-1] if slide["fragments"] else -1]
                for fragment in fragments:
                    page.evaluate("p => Reveal.slide(p.h, p.v, p.f)", {"h": slide["h"], "v": slide["v"], "f": fragment})
                    page.wait_for_timeout(args.settle_ms)
                    page.evaluate("() => document.fonts.ready")
                    state_errors = page.evaluate(PREPARE_MEDIA, args.video_time)
                    name = "initial" if fragment == -1 else f"fragment-{fragment:02d}"
                    filename = f"slide-{slide['number']:02d}-{name}.png"
                    # Only the slide canvas is captured, independent of surrounding letterboxing.
                    page.locator(".reveal .slides").screenshot(path=str(output / filename), animations="disabled")
                    state = {**slide, "fragment": fragment, "state": name, "filename": filename, "errors": state_errors}
                    states.append(state)
                    errors.extend(f"Slide {slide['number']} {name}: {error}" for error in state_errors)
                    print(f"Captured {slide['number']}: {slide['title']} / {name}")
            context.close()
            browser.close()
        if args.sheet:
            contact_sheet(output, states)
    except Exception as exc:
        errors.append(f"Preview failed: {exc}")
    finally:
        manifest["errors"] = list(dict.fromkeys(errors))
        (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Review output: {output}")
    if errors:
        for error in dict.fromkeys(errors):
            print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
