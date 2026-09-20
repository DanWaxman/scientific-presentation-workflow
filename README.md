# Scientific presentation workflow

A standalone repository with two portable agent skills for making scientific figures and author-led HTML presentations:

- **[scientific-plotting](skills/scientific-plotting/SKILL.md)**: clean Matplotlib figures, consistent color, honest uncertainty, and reproducible rendering.
- **[scientific-slides](skills/scientific-slides/SKILL.md)**: an agreed `presentation.md` draft translated into a local Reveal.js deck, then visually reviewed.

The **[layout gallery](skills/scientific-slides/assets/template/index.html)** is a complete presentation. Open its `index.html` in a modern browser; it needs no network connection, installation, or build step. Use arrow keys to advance and Escape for an overview. All examples are generic and editable.

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

This copies the complete offline gallery into a new directory and refuses to overwrite an existing project. Open `../my-talk/index.html`, then replace the illustrative material with your talk. The gallery includes prose/math reveals, citations, code, scientific plots, diagrams, an outline, video, and large explanations that move and shrink when results appear.

Edit `../my-talk/presentation.md` first. Ordinary text and equations are the exact visible content; clearly marked instructions describe layout, figures, references, and reveals. The matching gallery draft demonstrates this convention. Tell the agent which wording is settled and which content needs development.

> Translate slides 2–4 of presentation.md into index.html. Preserve my titles, prose, notation, and reveal order. Use the draft's layout instructions, ask about substantive ambiguities, then screenshot each fragment state and the neighbouring slides.

> The result slide is crowded. Keep the prose exact, enlarge the explanation initially, then move it into its compact position when the plots arrive. Update that slide's layout instructions after implementing the agreed change.

This is **agent-assisted HTML authoring**, not a Markdown compiler. Editing the draft does not automatically change the slides. `index.html` is the artifact presented in the browser. Keep the draft synchronized with agreed changes and track it in Git, alongside scientific source and bibliography.

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

Keep changes focused and describe the behavior, motivation, and validation in a readable pull request. Preserve the author's supplied prose and notation in translation examples; propose language changes explicitly. Keep scientific computation separate from cached rendering, and retain provenance and the distinction between real results and illustrative data.

For changes to the template or helpers, create a fresh deck outside the checkout, regenerate the synthetic figures, render again from the cache, inspect every fragment, and preview the staged publication files offline. Update the draft and documentation when behavior changes. Preserve dependency versions, upstream provenance, and license notices when modifying the bundled runtime. Generated talks, previews, and local environments do not belong in contributions.

If this workflow is included as a Git submodule, clone the enclosing repository with `git clone --recurse-submodules <repository-url>`, or initialize an existing checkout with `git submodule update --init --recursive`. Commit and push changes inside the skill repository first; then commit its updated submodule pointer in the enclosing repository.

## License

The original skill instructions, helper code, and template content in this collection are **MIT licensed**, copyright 2026 Daniel Waxman; see [LICENSE](LICENSE). Bundled dependencies retain their own licenses and notices. Your added research material remains subject to its own authorship and licensing terms.
