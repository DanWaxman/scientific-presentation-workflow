---
name: scientific-slides
description: Create or revise scientific HTML presentations using an author-led presentation.md draft, absolute-positioned Reveal.js layouts, local math and media, and visual review. Use for this HTML workflow, not PowerPoint or Google Slides editing.
---

# Scientific slides

Turn an agreed scientific argument into a readable presentation. The draft is the author's source of intent; `index.html` is the presentation artifact. Translation means agent-assisted HTML authoring, not an automatic Markdown compiler.

## Author-led workflow

1. Establish the purpose, audience, duration, and available material before writing new content or restructuring a talk. Use answers already supplied; a small requested edit does not need a new interview.
2. Create or revise `presentation.md`. Separate the exact slide prose and mathematics from layout, figure, citation, and reveal instructions. Read [authoring.md](references/authoring.md) when drafting or translating.
3. Clarify substantive ambiguities before the affected implementation: scientific meaning, missing data, contradictory instructions, or an unspecified choice that changes the argument. Continue independent work. Resolve routine spacing and styling from the surrounding deck.
4. Preserve supplied titles, prose, notation, citations, and reveal order. Do not add explanatory bullets or editorial asides. Add speaker notes only when requested or included in the agreed plan. If the wording cannot fit legibly, propose a concrete revision instead of silently rewriting it or shrinking the font.
5. Translate the agreed draft into HTML, render every changed state, inspect the images, and revise. Keep the draft synchronized with agreed changes. Report any unresolved scientific or rendering limitation.

## Presentation conventions

- Start a new talk from [the offline gallery](assets/template/index.html). It uses a **960×700** canvas and absolute `.sl-block` / `.sl-block-content` elements. Keep this coordinate system unless a different canvas and a corresponding relayout are explicitly requested. Use grid or flex only inside a block.
- Use local Montserrat, white backgrounds, dark text, restrained key-term colors, compact layouts, white code panels, and APA author–year citations. Branding and author information are editable; the gallery's content is illustrative.
- Use explicit zero-based fragment indices. Elements revealed together share an index, including a citation and its footer. Check the initial state as well as each reveal; hidden fragments can leave distracting empty space.
- Use KaTeX `\(...\)` / `\[...\]` in HTML. Convert draft delimiters deliberately, preserving the mathematics. Keep code out of math rendering. Source executable excerpts from the accompanying code, with omissions clearly documented when needed.
- Keep fonts, scripts, images, and videos local. The gallery bundles pinned Reveal.js, KaTeX, highlighting, and Montserrat. Preserve their notices. Use native Reveal auto-animation and the gallery's fragment-video lifecycle; no slides.com runtime is required.
- Make explanations large when first introduced. When results appear, a paired auto-animate slide can move and shrink shared elements into their final positions. Preserve stable `data-id` values, test both directions and deep links, and respect reduced motion.

## Figures and review

Generate scientific results reproducibly; cache expensive calculations separately from rendering. State what uncertainty depicts and preserve inconvenient results. If the `scientific-plotting` skill is available, use it for plot styling; otherwise preserve shared scales, clean axes, readable final-size labels, and accurately labeled uncertainty.

Read [tools.md](references/tools.md) for copying, previewing, and packaging commands. Inspect final slides and all fragment states at the intended display size, plus adjacent slides for balance. Check bounds, equation errors, code wrapping, image resolution, references, and media playback. Exercise forward/backward navigation, deep links, and video resets. A successful script exit is not a visual review.

Keep `presentation.md` tracked in Git but excluded from site builds and publication output. Merge the template's Jekyll exclusions into an existing configuration. Use `package.py` to stage browser assets without drafts, code, caches, or previews. Staging does not commit, push, or deploy.
