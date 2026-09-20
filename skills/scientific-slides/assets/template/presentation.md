# Gallery draft

This file is the authoring source, not an executable build input. Visible prose
below is translated into `index.html` by the author or an agent. Blocks labelled
**Instructions** are directions, never visible slide text. Update the title,
presenter, research material, and directions for your own talk. Preserve agreed
wording when translating; ask about substantive ambiguity before implementing it.

Purpose: demonstrate reusable scientific slide layouts. Audience: researchers
preparing an HTML talk. Duration: a short layout tour, not a research presentation.

---

## 1. A clear scientific story

An offline layout gallery

Presenter name  
Research group · Event · Date

**Instructions**
- Title layout, no fragments. Large title above subtitle and byline.
- White background; use editable text rather than institutional branding.

---

## 2. The shape of the argument

**01 · Question**  
What relationship do we want to learn?

**02 · Model**  
State the assumptions and the uncertainty.

**03 · Evidence**  
Compare predictions with observed data.

**04 · Takeaway**  
Say what the results support.

**Instructions**
- Four outline cards in a 2×2 grid within one absolute slide block.
- Reveal cards in reading order at fragment indices 0–3; keep earlier cards visible.

---

## 3. Start with an explicit model

We describe a response with a **linear mean**.

$$y_i = \beta_0 + \beta_1 x_i + \varepsilon_i$$

$$\varepsilon_i\sim N(0,\sigma^2),\qquad \boldsymbol\beta\sim N(\mathbf0,I_2)$$

The posterior describes uncertainty about the intercept and slope.

**Instructions**
- Use vocabulary color for “linear mean”.
- Four fragments: first sentence → observation equation → distributions → last sentence.
- Use centered equations with ample font size; no extra explanatory prose.

---

## 4. Make the uncertainty explicit

**Pointwise credible intervals**

At each input, the band contains a stated amount of posterior probability for the mean response.

These figures use Matplotlib.  
(Hunter, 2007)

**Instructions**
- Reveal the first two paragraphs together in a bordered box at index 0.
- Reveal the Matplotlib sentence, in-text citation, and matching full footer reference at index 1.
- Source `hunter2007` in `references.bib`; format APA 7.
- The box describes marginal intervals, not simultaneous coverage or observation predictions.

---

## 5. The model has a short implementation

Gaussian prior + Gaussian noise

$$\boldsymbol\beta\mid\mathbf y\sim N(m,V)$$

The covariance keeps uncertainty in both coefficients.

**Instructions**
- Reveal the mathematics/text column on the left, then the code column on the right.
- Insert the exact marked `posterior` function from `code/generate_figures.py`.
- The script supplies NumPy imports, the design matrix with columns `(1, x)`, observations,
  and the known observation standard deviation. Code panels omit those calls for space.
- Use a white code theme, preserve indentation, and keep all lines visible.

---

## 6. Connect the model to the evidence

Observed data  
Prior  
Posterior  
Predictions

**Instructions**
- Inline SVG diagram: two left boxes feed a middle posterior box, then a right prediction box.
- Reveal inputs → posterior plus connecting arrows → predictions plus connecting arrow.
- Diagram labels are the only body text. Use neutral input boxes, teal posterior, and coral predictions.

---

## 7. What do the data say?

Predictions · residuals · uncertainty

**Instructions**
- Coral section divider, white text, no fragments.

---

## 8. Show the fit and the observation noise

A small synthetic example with known observation noise.

Left: posterior intervals for the mean. Right: the known observation-noise distribution.

**Instructions**
- Reveal the introductory sentence at index 0, then both plots and the caption at index 1.
- Left: `figs/regression.png`; right: `figs/residuals.png`, with errors measured against the true mean.
- Caption is the final body sentence above; put it below both figures.
- Both figures show nested 50/80/95% intervals, with different interpretations stated on the plots.
- Fixed seed 2026; true intercept 0.5, slope 1.4; known noise standard deviation 0.35.
- Generate all assets with `python code/generate_figures.py --compute --plot`.

---

## 9. From an equation to a result

$$\boldsymbol\beta\mid\mathbf y\sim N(m,V)$$

**Instructions**
- Introduce the equation and executable posterior function at large size, no fragments.
- Equation above code. Use the same source excerpt as slide 5.
- Pair with slide 10 using native Reveal auto-animation and shared `data-id` values.

---

## 10. From an equation to a result

$$\boldsymbol\beta\mid\mathbf y\sim N(m,V)$$

**Instructions**
- Retain exact title, equation, and source excerpt from slide 9.
- On advancing, move the equation to the upper left and code to the upper right, reducing both
  to their compact sizes. Both result plots then occupy the lower portion, with no extra prose.
- Explicitly match shared title/equation/code elements. Disable unmatched fades.
- Backward navigation reverses the transformation. Reduced motion skips the transition.

---

## 11. Watch the evidence accumulate

Update the posterior as each observation arrives.

Bands describe uncertainty in the mean response.

**Instructions**
- Reveal the first sentence, then `figs/animation.mp4` and its caption.
- Poster: `figs/animation-initial.png`. Video performs analytic sequential posterior updates using
  only the observations revealed so far; the last frame holds before the loop restarts.
- Use the fragment video lifecycle in `slides.js`: start on reveal, pause/reset when hidden or
  on slide exit, restart when re-entering, and handle deep links. No `data-autoplay`.
- Provide the small play/pause button. Respect reduced motion by leaving the animation paused
  until the user presses play. The button labels are functional UI, not talk prose.

---

## 12. Questions?

Presenter name · Contact details

**Instructions**
- Coral closing slide, white text, no fragments.
- Replace contact text with your details before presenting.

---

## Reproduction and publication

**Instructions**
- No scientific software installation is needed to view these already rendered examples.
- See `code/generate_figures.py` for the exact analytic posterior and uncertainty definitions.
- `--compute` creates data/cache; `--plot` only reads cached arrays and renders figures/video.
- Inspect plots and every fragment at 960×700. Check code, equations, animation, and references.
- Keep this draft tracked in Git and excluded from Jekyll and publication staging. Merge
  `_config.yml` exclusions into a parent site using paths relative to that site's root.
- No speaker notes are requested for this gallery.
