# Matplotlib helper

Copy `assets/plot_style.py` into the project and import it locally. Python 3.10+, NumPy, and Matplotlib are required. Static rendering needs no animation package.

```python
import matplotlib.pyplot as plt
from plot_style import STYLE_COLORS, apply_slide_style, add_nested_band
from plot_style import despine_curve_axis, save_figure

apply_slide_style(font_size=18)
fig, ax = plt.subplots(figsize=(4.3, 3.0), layout="constrained")
add_nested_band(ax, x, [(lo95, hi95), (lo80, hi80), (lo50, hi50)],
                color=STYLE_COLORS["dark_teal"])
ax.plot(x, mean, color=STYLE_COLORS["dark_teal"])
despine_curve_axis(ax)
save_figure(fig, "figs/result")  # PNG, SVG, PDF
```

- `apply_paper_style(font_size=9)` and `apply_slide_style(font_size=18)` change global Matplotlib defaults. Call before constructing a figure. They do not enforce a universal physical figure size.
- `add_nested_band(ax, x, bands, color=..., alphas=(.10,.16,.24))` accepts outer-to-inner `(lower, upper)` arrays. It checks matching lengths/shapes, finite values, increasing coordinates, valid endpoints, and nesting. Split genuinely missing segments before calling it. It returns the Matplotlib collections.
- `despine_curve_axis(ax)` opens the top/right frame; `box_image_axis(ax)` restores a thin full frame. `add_subfigure_label(fig, ax, "(a)")` places a centered label below an axes; leave sufficient bottom space.
- `save_figure(fig, stem, formats=("png", "svg", "pdf"), dpi=300, tight=True)` creates parent directories and returns output paths. Use `tight=False` when a fixed canvas size matters.
- `save_mp4(animation, path, fps=30, dpi=150, crf=20, ffmpeg_path=None)` exports H.264/yuv420p with a browser-friendly fast-start header. It uses explicit FFmpeg if provided, otherwise Matplotlib's configured executable if runnable, otherwise lazily imports `imageio_ffmpeg`. Install `imageio-ffmpeg` only if needed. Construct even-pixel frame dimensions (`inches × dpi`); odd dimensions raise a clear error. `savefig.bbox` is disabled during movie writing so the frame dimensions stay fixed.

For Matplotlib animation, hold the final state by repeating it in the frame sequence. The writer does not invent timing, a causal interpretation, or a loop: the animation source and the HTML player define those behaviors.
