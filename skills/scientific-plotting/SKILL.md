---
name: scientific-plotting
description: Create, edit, or review scientific figures with Matplotlib, including uncertainty bands, time series, spatial fields, model comparisons, and presentation animations.
---

# Scientific plotting

Make scientific evidence readable at its final size: white backgrounds, crisp thin axes, deliberate colors, and restrained annotation. Preserve the experiment and the author's intended claim while improving its visual presentation.

## Workflow

1. Establish the quantity, units, comparison, uncertainty interpretation, and final display size. Clarify missing scientific meaning; use reasonable defaults for routine styling.
2. Separate computation from rendering. Save expensive inference/simulation outputs, provenance, seeds, and diagnostics in a cache; visual revisions should reuse those outputs. Do not change data or retrain a model merely to make a figure look better.
3. Define colors, labels, and limits explicitly. Arrange time from left to right, comparable methods in consistent rows or colors, and different metrics on separate axes. Use shared limits for like quantities unless a difference is explicitly explained.
4. Render, view the actual image at its intended paper or slide dimensions, and revise. Check the whole composite and the smallest labels. Improve the layout before reducing the font.
5. Deliver source plus a PNG and an appropriate vector format (SVG/PDF). For animation, also provide representative stills and document what each frame means.

## Visual defaults

- White background; thin black axes and outward ticks. Remove top/right spines for curves; use a thin frame for spatial fields and image panels. Skip decorative gradients, shadows, and heavy grids.
- Use the explicit palette in [assets/plot_style.py](assets/plot_style.py). Pick two to four distinguishable method colors and preserve their meaning within an experiment. Combine color with dashes or markers when needed. The palette is a vocabulary, not a fixed global mapping.
- Truth/reference is black and usually dashed. Available observations are muted, small, and distinguishable from model output. Keep legends frameless, concise, and away from important data.
- Use short labels with units and only necessary tick precision. Compact bold panel labels are useful; large decorative plot titles rarely are.
- Show uncertainty as nested translucent bands, normally 95/80/50% from outside to inside. Use a solid mean/median and no band outline. Posterior sample paths can be thin light gray behind the summary.
- Label uncertainty accurately: distinguish posterior credible intervals, predictive intervals, confidence intervals, and across-run variability; identify pointwise versus simultaneous bands. A Gaussian moment summary of a mixture is not generally a mixture quantile. Do not imply that continuous shrinkage is variable selection.
- Preserve missing observations as missing. Do not score them as observed or show future data in a causal animation. State whether model parameters were fitted offline or learned online.

Read [references/figure-patterns.md](references/figure-patterns.md) for spatial panels, maps, regression, forecasts, comparisons, and temporal displays. Read [references/helper-api.md](references/helper-api.md) when using the Python helper.

## Portable implementation

Copy [assets/plot_style.py](assets/plot_style.py) into the project so source does not depend on the skill's installation path. It provides paper/slide typography, validated nested bands, static exports, and optional H.264 animation export. NumPy and Matplotlib are required; `imageio-ffmpeg` is needed only if a system FFmpeg executable is unavailable. No particular inference library is required; use dynestyx only when the scientific task calls for it.

The supplied sizes are starting points. Judge readability at the final embedded size, not in a full-screen plotting window. Before completion, inspect labels, legends, overlapping marks, uncertainty ordering, shared scales, and any animation's beginning, transitions, and final hold.
