"""Portable scientific plotting helpers. MIT © 2026 Daniel Waxman.

Copy this file into the figure project; it has no dependency on its installation
directory. NumPy/Matplotlib are required. Animation dependencies are lazy.
"""
from __future__ import annotations

from pathlib import Path
from typing import Sequence
import shutil
import subprocess

import matplotlib as mpl
import numpy as np

STYLE_COLORS = {
    "warm_red": "#E64B35", "orange": "#E69F00", "teal_green": "#009E73",
    "dark_teal": "#00897B", "cyan_blue": "#56B4E9", "muted_blue": "#80B1D3",
    "purple": "#8C79B8", "lavender": "#BEBADA", "salmon": "#F08070",
    "olive": "#8DA35B", "light_green": "#7CC943", "coral": "#F04E3E",
    "neutral_gray": "#5F5F5F", "light_gray": "#BDBDBD", "black": "#222222",
}
TIME_GRADIENT_ANCHORS = ("#3B4CC0", "#25A186", "#FDE725", "#E64B35")


def _apply_style(font_size: float, *, slide: bool) -> None:
    if not np.isfinite(font_size) or font_size <= 0:
        raise ValueError("font_size must be positive and finite")
    mpl.rcParams.update({
        "figure.dpi": 160, "savefig.dpi": 300, "savefig.bbox": "tight",
        "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.facecolor": "white", "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans", "pdf.fonttype": 42, "ps.fonttype": 42,
        "font.size": font_size, "axes.titlesize": font_size + 1,
        "axes.labelsize": font_size, "xtick.labelsize": font_size - (2 if slide else 1),
        "ytick.labelsize": font_size - (2 if slide else 1),
        "legend.fontsize": font_size - (2 if slide else 1),
        "axes.linewidth": .9, "lines.linewidth": 2.2 if slide else 2.,
        "patch.linewidth": .8, "xtick.direction": "out", "ytick.direction": "out",
        "xtick.major.size": 3., "ytick.major.size": 3.,
        "xtick.major.width": .8, "ytick.major.width": .8,
        "legend.frameon": False, "axes.grid": False,
        "text.color": STYLE_COLORS["black"], "axes.labelcolor": STYLE_COLORS["black"],
        "xtick.color": STYLE_COLORS["black"], "ytick.color": STYLE_COLORS["black"],
    })


def apply_paper_style(font_size: float = 9) -> None:
    """Apply manuscript defaults; inspect at the actual column width."""
    _apply_style(font_size, slide=False)


def apply_slide_style(font_size: float = 18) -> None:
    """Apply larger defaults; inspect at the final slide block dimensions."""
    _apply_style(font_size, slide=True)


def despine_curve_axis(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="out")


def box_image_axis(ax) -> None:
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(.9)
    ax.tick_params(direction="out")


def add_nested_band(ax, x, bands, *, color: str,
                    alphas: Sequence[float] = (.10, .16, .24)) -> list:
    """Draw validated outer-to-inner bands; split missing segments beforehand."""
    x = np.asarray(x, dtype=float)
    bands, alphas = list(bands), list(alphas)
    if x.ndim != 1 or x.size < 2 or not np.all(np.isfinite(x)):
        raise ValueError("x must contain at least two finite one-dimensional values")
    if np.any(np.diff(x) <= 0):
        raise ValueError("x must be strictly increasing")
    if not bands or len(bands) != len(alphas):
        raise ValueError("Supply one alpha per band, with at least one band")
    if any(not np.isfinite(a) or not 0 <= a <= 1 for a in alphas):
        raise ValueError("Band alphas must be finite and in [0, 1]")
    checked = []
    for pair in bands:
        if len(pair) != 2:
            raise ValueError("Each band must be a (lower, upper) pair")
        lower, upper = (np.asarray(v, dtype=float) for v in pair)
        if lower.shape != x.shape or upper.shape != x.shape:
            raise ValueError("Every band endpoint must have the same shape as x")
        if not np.all(np.isfinite(lower)) or not np.all(np.isfinite(upper)):
            raise ValueError("Band endpoints must be finite; split missing segments")
        if np.any(lower > upper):
            raise ValueError("Band lower endpoints cannot exceed upper endpoints")
        if checked and (np.any(lower < checked[-1][0]) or np.any(upper > checked[-1][1])):
            raise ValueError("Bands must be nested from widest to narrowest")
        checked.append((lower, upper))
    return [ax.fill_between(x, lo, hi, color=color, alpha=a, linewidth=0)
            for (lo, hi), a in zip(checked, alphas)]


def add_subfigure_label(fig, ax, label: str, y_offset: float = .055) -> None:
    bbox = ax.get_position()
    fig.text((bbox.x0 + bbox.x1) / 2, bbox.y0 - y_offset, label,
             ha="center", va="top", fontsize=mpl.rcParams["font.size"])


def save_figure(fig, stem, *, formats=("png", "svg", "pdf"), dpi=300,
                tight: bool = True) -> list[Path]:
    """Export vector/raster files; set tight=False to preserve fixed dimensions."""
    stem = Path(stem)
    formats = tuple(formats)
    if not formats or any(f not in {"png", "svg", "pdf"} for f in formats):
        raise ValueError("formats must contain png, svg, and/or pdf")
    stem.parent.mkdir(parents=True, exist_ok=True)
    paths = []
    with mpl.rc_context({"savefig.bbox": "tight" if tight else None}):
        for extension in formats:
            path = stem.parent / f"{stem.name}.{extension}"
            fig.savefig(path, dpi=dpi)
            paths.append(path)
    return paths


def save_mp4(animation, path, *, fps=30, dpi=150, crf=20, ffmpeg_path=None) -> Path:
    """Write H.264/yuv420p, loading optional imageio-ffmpeg only when needed."""
    from matplotlib.animation import FFMpegWriter
    if fps <= 0 or dpi <= 0 or not np.isfinite(fps) or not np.isfinite(dpi):
        raise ValueError("fps and dpi must be positive and finite")
    if not isinstance(crf, int) or not 0 <= crf <= 51:
        raise ValueError("crf must be an integer in [0, 51]")
    width, height = (int(v * dpi) for v in animation._fig.get_size_inches())
    if width % 2 or height % 2:
        raise ValueError("H.264/yuv420p needs even pixel dimensions; adjust figsize or dpi")
    executable = str(ffmpeg_path or mpl.rcParams["animation.ffmpeg_path"])
    def runnable(candidate):
        if not shutil.which(candidate):
            return False
        try:
            return subprocess.run([candidate, "-version"], capture_output=True,
                                  timeout=5, check=False).returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            return False
    if not runnable(executable):
        if ffmpeg_path:
            raise RuntimeError(f"FFmpeg executable is unavailable or cannot run: {executable}")
        try:
            import imageio_ffmpeg
        except ImportError as exc:
            raise RuntimeError("Install FFmpeg or the optional imageio-ffmpeg package") from exc
        executable = imageio_ffmpeg.get_ffmpeg_exe()
        if not runnable(executable):
            raise RuntimeError("Bundled imageio-ffmpeg executable cannot run")
    path = Path(path)
    if path.suffix.lower() != ".mp4":
        raise ValueError("Animation destination must end in .mp4")
    path.parent.mkdir(parents=True, exist_ok=True)
    with mpl.rc_context({"animation.ffmpeg_path": executable, "savefig.bbox": None}):
        writer = FFMpegWriter(fps=fps, codec="libx264", extra_args=[
            "-pix_fmt", "yuv420p", "-crf", str(crf), "-movflags", "+faststart"])
        animation.save(path, writer=writer, dpi=dpi)
    return path
