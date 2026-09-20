# Drafting and translating a scientific talk

## The three artifacts

`presentation.md` records the author's words and presentation instructions. `index.html` contains the slides that a browser presents. Scientific source and caches generate the figures referenced by the HTML. Keep these responsibilities separate: changing a font should not refit a model, and editing the draft does not automatically update the deck.

For a new talk, establish its purpose, audience, duration, and available evidence. Ask about a missing choice when it affects scientific meaning or the argument. Preserve decisions already made. For a requested local change, inspect the relevant draft and neighbouring slides before broadening the scope.

## Draft format

Use headings for exact titles, ordinary text for exact visible prose, and clearly marked instruction blocks. This is a human-readable convention, not a parser contract. Start with a normal Markdown heading rather than YAML frontmatter; reserve `---` for slide separators.

```markdown
# Presentation draft

Purpose: Explain how uncertainty changes a regression prediction.
Audience: Researchers familiar with linear algebra.
Duration: 12 minutes.

## Predicting with uncertainty

We can distinguish uncertainty about the mean from noise in a new observation.

$y_\star = \phi(x_\star)^\top \beta + \epsilon_\star$

<instructions>
Layout: prose at the top, equation in the centre, result plot below.
Reveals: 0 prose; 1 equation; 2 figure.
Figure: figs/prediction.svg. Show posterior mean and 95% predictive interval.
Citation: none for this synthetic example.
</instructions>

---

## A second slide

Exact visible prose goes here.
```

Treat instruction text as authoring guidance, not slide content. Keep the supplied wording, symbols, capitalization, and punctuation. HTML escaping and changing math delimiters are translation; changing a scientific claim is an editorial change. If a supplied phrase appears mistaken, ask or propose an explicit correction. Do not silently make it more confident, add a caveat, or introduce a teaching aside.

Use a notes instruction only when notes were requested or agreed. Record figure provenance, seeds, commands, and limitations in project documentation even when they are not intended as speaker notes. If the author requests a layout revision, update that slide's instructions so the next translation preserves it.

## HTML layout

The template uses locally authored CSS, Reveal.js 6.0.2, and native Reveal auto-animation. Its absolute blocks retain a consistent coordinate system without depending on an export service.

```html
<section>
  <div class="sl-block" style="left: 55px; top: 18px; width: 850px;">
    <div class="sl-block-content"><h3>Predicting with uncertainty</h3></div>
  </div>
  <div class="sl-block" style="left: 80px; top: 110px; width: 800px;">
    <div class="sl-block-content">
      <p class="fragment" data-fragment-index="0">Exact visible prose.</p>
      <p class="fragment" data-fragment-index="1">\[y_\star = \phi(x_\star)^\top\beta + \epsilon_\star\]</p>
    </div>
  </div>
</section>
```

Use the gallery's classes and layouts as working examples. Titles use `h3`; body blocks commonly start 55–80 px from the left. Reserve the bottom area, roughly y=610–680, for references or closing details. These are starting positions, not a requirement to leave a large blank band. Balance each slide as a whole, including intermediate states. Keep top-level blocks absolute; grids of cards or aligned cells can use grid or flex inside a block.

Montserrat, body `#444`, secondary `#555`, labels `#777`, key terms `#ac2a2a`, and coral `#f08383` establish the default visual language. Citation spans are smaller and italic; footer references are gray with a hanging indent. Change branding and author details for each talk. Use spacing or fewer elements before making text smaller. Figure labels must be readable after embedding at their actual slide dimensions.

The gallery demonstrates title and closing slides, progressive prose/math, a boxed statement, two-panel results, code beside mathematics, an SVG diagram, an outline, a divider, fragment video, and an explanation-to-results transition. Copy only the relevant section and its needed classes. Do not propagate unused slide content or personal affiliations.

## Math, code, and citations

Use `\(...\)` for inline math and `\[...\]` for display math. A draft's `$...$` requires conversion. Configure shared macros deliberately or define local macros where used; do not assume a definition in one expression applies to every other expression. Inspect the rendered expression for over-wide equations and KaTeX errors.

Keep code on white panels and preserve actual indentation. When splitting one executable function across multiple blocks, avoid automatic trimming that removes meaningful indentation. Code should be a real excerpt from the included source; shorten it by selecting a useful excerpt, not by inventing an API. Explain omitted setup in requested notes or source documentation. Review highlighting after any code edit.

Add bibliographic entries to the talk's `references.bib` before citing them. Use ordinary APA 7 author names unless the author requests a different convention:

- One author: `(Surname, 2026)`.
- Two authors: `(Surname & Surname, 2026)`.
- Three or more: `(Surname et al., 2026)`.

Put the author–year citation next to its claim and the full reference in that slide's footer. Reveal both at the same fragment index. Use one footer paragraph per reference in order of appearance. Render full author initials, sentence-case article titles, italic journal names and volume numbers, and DOI links where available. Verify bibliographic facts from the source; do not invent citations for generic examples. The BibTeX file supports authoring; the rendered reference text is authored in HTML.

## Reveals and motion

Assign explicit fragment indices starting at zero. Share an index for simultaneous elements; avoid relying on DOM order in a diagram. A typical sequence is claim → equation → figure, adjusted to the agreed narrative. Reveal the border and content of a box together so its first state is not an empty frame.

For large explanations that move aside for results, use consecutive `data-auto-animate` sections with stable `data-id` attributes on matching blocks. The first state can give code and math most of the canvas; the next uses the same content at its compact final position with space for results. Set `data-auto-animate-unmatched="false"` when unrelated elements should appear immediately. Inspect the transition as well as both endpoints. The gallery disables motion under the browser's reduced-motion preference.

For fragment videos, follow the gallery's `slides.js` convention instead of combining slide-level autoplay with fragment timing. Videos should start when their fragment becomes visible, reset when hidden or left, and behave consistently on a deep link or backward entry. Keep `muted`, `playsinline`, looping behavior, poster images, and accessible labels explicit. Browser autoplay restrictions may require a click; retain a way to start playback. If multiple figures swap in one area while bullets accumulate, synchronize that change by fragment index and test every state.

## Scientific assets

Keep all browser media in the deck, with descriptive relative paths. Prefer SVG or sufficiently large PNGs for static plots; use H.264 with yuv420p for browser MP4s. Fix comparison axes and color meaning across panels and animation frames. Distinguish credible intervals, prediction intervals, ensemble spread, and numerical approximations to uncertainty in labels or the agreed explanation.

Separate data generation or inference from rendering. Save seeds, provenance, parameters, uncertainty summaries, and the package versions needed to reproduce scientific results. Use cached results for layout revisions. A schematic must be identified as a schematic; neither the code nor the plot should imply a scientific calculation that was not performed. The gallery's synthetic regression data and calculation are included under `code/` as a small reproducible example.

## Review and publication

Use [tools.md](tools.md) to capture screenshots. Inspect a contact sheet for rhythm, then each changed slide and fragment at presentation size. Look for clipped blocks, excessive gaps, equations overflowing their blocks, tiny plot labels, wrapped code, crowded references, and unexpected layer order. Regenerate an illegible figure with appropriate typography rather than just enlarging its enclosing block. Check neighbouring slides after moving or adding content.

Exercise forward/backward navigation, a fresh deep link, fragment media resets, auto-animation, and reduced motion. Open a copied deck without network access to check local fonts, math, scripts, and media. Scientific or browser failures should be reported concretely rather than hidden by cosmetic changes.

Track the draft and scientific source in Git. Ignore transient caches, local environments, and previews. Excluding the draft from Git would lose the authoring history and is not the intended workflow.

For Jekyll, merge the template's `exclude` entries into the site's existing `_config.yml`; do not replace unrelated configuration. Exclude drafts, scientific source, caches, and preview directories from the build. A `.nojekyll` file only disables processing on hosts that recognize it; it does not remove source files from a published directory.

For a static upload, use `package.py DECK --out DEST` to create a separate directory containing only browser assets and licenses. Review that directory before publication. Packaging does not authorize deployment, commits, or pushes. Keep third-party license files and notices when redistributing the bundled runtime.
