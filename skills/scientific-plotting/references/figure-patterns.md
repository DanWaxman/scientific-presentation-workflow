# Figure patterns

Use these patterns when they fit the experimental question, rather than forcing every figure into one layout.

## Regression and time series

Show observations, a solid colored estimate, a black dashed reference when known, and nested uncertainty. When several sources or agents matter, distinguish them with muted marker shapes or separate panels. Do not connect across missing data unless the line represents a model prediction. Put legends above/below the axes when an inset legend would hide evidence.

For forecasts, a prediction row with an aligned error row often helps. Mark the observation cutoff and distinguish fitting, filtering, smoothing, and forecasting. Keep causal displays free of unavailable observations. Use a shared time axis and show gaps explicitly.

## Spatial and spatiotemporal fields

Use rows for methods and columns for increasing time. Share a colormap and limits for comparable quantities, with one labeled colorbar. Signed fields usually need a diverging colormap centered at zero; nonnegative fields need a perceptually ordered sequential colormap. Do not let autoscaling make an inaccurate model appear to match truth.

For geographic maps, retain real coordinates and appropriate units. Use a suitable projection or local physical aspect ratio; equal longitude/latitude degrees do not generally represent equal distances. Faint coastlines, roads, or boundaries provide context. Candidate sensors can be light gray, selected sensors more prominent. Use a simple outline to emphasize a study region.

## Model and metric comparisons

Separate metrics with different units. Group bars by the experimental factor, start bar axes at zero, and add numerical labels only when exact values matter. Box/violin plots should identify the underlying replicates and sample count. Across-run variation is not a posterior interval. Pair methods with the same color throughout the figure; sparse marker or dash differences improve monochrome readability.

For coefficient recovery, show every relevant term, a zero reference, truth markers when known, and marginal intervals. Use separate scales when components have very different physical magnitudes, with explicit axis labels. Continuous shrinkage does not produce posterior inclusion probabilities.

## Posterior trajectories and temporal change

Use a few representative snapshots or a summary figure alongside animation. Gray low-opacity sample paths should support a clearly drawn mean, not obscure it. Encode time with color only when temporal order is itself the message; the helper includes blue→green→yellow→red anchors. Give such a scale a compact “Earlier → Later” label.

For evolving mixture weights or diagnostic traces, use one small panel per method and shared limits where appropriate. Dotted event markers can align plots without heavy grids.

## Composition and final size

Use aligned plot regions, short panel labels, and consistent whitespace. External legends and colorbars must fit within the exported bounds. Compare panels at the actual paper column width or slide block size. For slides, regenerate larger text if needed rather than merely stretching a small figure. Inspect animation frames at the same scale as their intended player, with fixed axes unless changing scale is the subject.
