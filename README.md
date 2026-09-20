# Scientific presentation workflow

I've been writing lots of talks recently ([ex1](https://danwaxman.github.io/talks/mit_cse_f26/), [ex2](https://danwaxman.github.io/talks/siam_ne_26/), [ex3](https://danwaxman.github.io/talks/isba_wm_26/), [ex4](https://danwaxman.github.io/talks/q4c_feb_26/index.html)) -- I want these to be high-quality, but also not my full-time job. Figuring out how to use LLMs (I've been told the kids say "agents") for this task is a bit tricky: the point of a presentation is that you're hearing from _me_, and deriving the content, words, and what visuals should be shown are a big part of that experience that shouldn't be automated away! Living in our current age, this has been discussed by many many people, but I especially resonated with Gautam Kamath's [concise blog post](https://kamathematics.wordpress.com/2026/05/27/making-a-talk-without-and-with-ai/).

These are "skills" that I've accumulated to make `reveal.js` presentations, along with the corresponding workflow. The idea is:
1. Write your presentation in a flavored markdown file, `presentation.md`. The agent will use your words _verbatim_ from this file, and follow your instructions `<written in brackets>` regarding layout and accompanying figures.
2. Use a coding agent in "planning mode" to review your proposed new/modified slides, and make them so, handling the requisite HTML/CSS/Javascript schenanigans. The idea is not to add anything new, but execute your vision as-written.
3. The agent has some Python files that let it open in a headless Chrome instance, take screenshots, and iterate on the formatting as to (a) adhere to your instructions whilst (b) avoiding trivial things like line overflows and colliding materials.

(These skills are largely LLM-written, based on existing plots and presentations I had, with some careful human editing done in each case. This write-up is mostly human-written, with some LLM help for installation instructions.)

## Packaged Skills

We package two skills; one for making `reveal.js` plots, and also an opintionated "scientific plotting" skill. Both of these, obviously, come from my taste and style. You can and should edit these to match yours.

- **[scientific-slides](skills/scientific-slides/SKILL.md)**: an agreed `presentation.md` draft translated into a local Reveal.js deck, then visually reviewed.
- **[scientific-plotting](skills/scientific-plotting/SKILL.md)**: clean Matplotlib figures, consistent color, honest uncertainty, and reproducible rendering.

These skills use a set of templates, as seen in the packaged [layout gallery](skills/scientific-slides/assets/template/index.html). This should give a general idea of what the presentation will look like when executed.

## Install or use directly

Clone this repository:

```bash
git clone https://github.com/DanWaxman/scientific-presentation-workflow.git
cd scientific-presentation-workflow
```

Copy `skills/scientific-plotting`, `skills/scientific-slides`, or both into the skill directory supported by your agent. Keep each complete folder, including its `SKILL.md`, references, scripts, assets, and license. The enclosing `skills/` directory is a collection, not itself a skill. Consult your agent's documentation for its installation path and any reload step.

For Codex, a natural-language installation request is:

> Use $skill-installer to install the skills from https://github.com/DanWaxman/scientific-presentation-workflow.git at paths skills/scientific-plotting and skills/scientific-slides.

You can also point an agent at a local `SKILL.md` without installing it. In agents that support named skill invocation, use `$scientific-slides` or `$scientific-plotting`.

> Use the scientific-slides skill. Help me make a 15-minute talk for researchers who know probability but not this application. Start with a presentation.md draft using the notes below, and clarify the scientific choices before translating it.

> Use scientific-plotting to revise this uncertainty figure. Preserve the calculations and labels, use the cached results, and inspect the export at its final presentation size.

## Start a talk

The commands below run from the repository root. Create your talk beside the checkout so its generated files stay separate:

```bash
python3 skills/scientific-slides/scripts/new_deck.py ../my-talk
```

This copies the complete offline gallery into a new directory.

To start writing a talk, open `../my-talk/presentation.md`. Here, you can include slide information, including content and layout. Something like

```markdown
<Layout: 70/30 text/figure. The equation should be centered within the left panel.>

# Linear Regression

- The simplest model we can write is linear regression:

$$ y = X \theta + \varepsilon. $$

- For a simple Bayesian model:
  - Let's assume the law of $\varepsilon$ is known
  - Let's take a prior $\theta \sim \mathcal{N}(0, 1)$.

<Plot: generate 50 points from the generative model x ~ N(0, 1), y | x ~ N(2x + 1, 0.2^2).

Use a simple NumPyro model to implement this model, run MCMC to obtain results, then plot
the resulting regression, with uncertainty bars, using our scientific plotting skill.>
```

Then, instruct an agent to "translate" your markdown example into corresponding HTML.

> Translate slides 2–4 of presentation.md into index.html. Preserve my titles, prose, notation, and reveal order. Use the draft's layout instructions, ask about substantive ambiguities, then screenshot each fragment state and the neighbouring slides.

You can then provide iterative feedback, so that the implementation matches what's in your head :).

> The result slide is crowded. Keep the prose exact, enlarge the explanation initially, then move it into its compact position when the plots arrive. Update that slide's layout instructions after implementing the agreed change.

## Dependencies

| Task | Requirements |
|---|---|
| View or present the gallery | A modern browser; everything else is bundled locally |
| Copy a deck or stage publication files | Python 3.10+ |
| Regenerate the synthetic figures | Python, NumPy, Matplotlib; imageio-ffmpeg for MP4 |
| Capture automated previews | Python, Playwright, and a browser; Pillow for contact sheets |

Use your own Python environment. A typical setup for generation and review is:

```bash
python3 -m venv ../slide-tools-env
. ../slide-tools-env/bin/activate
python -m pip install numpy matplotlib imageio-ffmpeg playwright pillow
python -m playwright install chromium
```

On Windows, activate with `..\slide-tools-env\Scripts\activate` instead. The final deck needs none of these Python packages. No dynestyx installation is required; it can be used for a talk whose scientific calculations call for it.

The browser bundle pins **Reveal.js 6.0.2**, **KaTeX 0.18.7**, highlighting assets, and Montserrat. Its dependency notices identify the upstream sources and licenses. Keep these files together when copying or publishing.

## Regenerate and revise figures

The gallery ships finished PNG/SVG figures, a short MP4, and its synthetic calculation source. Run the computation once, then revise visuals from the cache:

```bash
python ../my-talk/code/generate_figures.py --compute --plot
python ../my-talk/code/generate_figures.py --plot
```

Read the source for the example's data-generating assumptions and uncertainty interpretation. Replace the synthetic example with your real scientific calculation when authoring a talk. Keep costly inference separate from plotting so a visual change does not retrain a model. The plotting skill supplies portable style helpers that can be copied into a project's source; they do not require an import from the installed skill directory.

## Review the presentation

```bash
python skills/scientific-slides/scripts/preview.py ../my-talk --sheet
python skills/scientific-slides/scripts/preview.py ../my-talk --all-fragments --sheet
```

An existing browser can be selected with `--browser /path/to/browser`. See [tool details](skills/scientific-slides/references/tools.md) for setup, output paths, and additional options. Read the screenshots as images: first the contact sheet, then individual slides and every reveal that changes layout. Check legibility at presentation size, math, code wrapping, reference clearance, and vertical balance.

Also click through forward and backward, open deep links, and verify animation start/reset behavior and reduced motion. Open a copied deck offline before presenting. If you prefer serving files locally, run `python -m http.server --directory ../my-talk 8000` from the repository root; direct browser viewing of `index.html` works as well.

## Prepare publication files

Keep `presentation.md` in version control **and out of site builds**. For Jekyll, merge the template's `_config.yml` exclusions into your site's existing list instead of replacing it. The same applies to scientific source, caches, and previews. Ignoring a file in Git and excluding it from a website build are different operations.

To create a separate, source-free publication directory:

```bash
python skills/scientific-slides/scripts/package.py ../my-talk --out ../my-talk-public
```

The command copies the allowed browser assets and licenses, excluding drafts, scientific source, caches, and previews. It does not deploy. Inspect the output and upload that directory using your chosen hosting workflow. Do not upload the entire authoring directory and assume `.gitignore` will filter its contents.

For more detailed layout, citation, motion, and draft conventions, read [authoring.md](skills/scientific-slides/references/authoring.md).

## Contributing

I'm not planning on accepting substantive outside contributions.

## License

The original skill instructions, helper code, and template content in this collection are **MIT licensed**, copyright 2026 Daniel Waxman; see [LICENSE](LICENSE). Bundled dependencies retain their own licenses and notices. Your added research material remains subject to its own authorship and licensing terms.
