# Third-party assets

The original template, scripts, and synthetic figures use the MIT license in
[LICENSE](LICENSE), copyright 2026 Daniel Waxman. This does not relicense the
dependencies below. All assets needed for viewing are local; no CDN is used.

| Component | Pinned version | License and source |
| --- | --- | --- |
| Reveal.js core and highlighting plugin | 6.0.2 | [MIT](vendor/reveal/LICENSE), [upstream](https://github.com/hakimel/reveal.js/tree/6.0.2) |
| highlight.js engine bundled in the Reveal plugin, plus GitHub theme | 11.11.1 | [BSD 3-Clause](vendor/highlight/LICENSE), [upstream](https://github.com/highlightjs/highlight.js/tree/11.11.1) |
| KaTeX, auto-render, and math fonts | 0.18.7 | [MIT](vendor/katex/LICENSE), [upstream](https://github.com/KaTeX/KaTeX/tree/v0.18.7) |
| Montserrat regular and italic variable fonts | Google Fonts commit `8b0a1d0f5983c89bc2b93f1b5fb55f9e252744b5` | [SIL Open Font License 1.1](vendor/montserrat/OFL.txt), [upstream](https://github.com/google/fonts/tree/8b0a1d0f5983c89bc2b93f1b5fb55f9e252744b5/ofl/montserrat) |

[vendor/provenance.json](vendor/provenance.json) records exact download URLs and
SHA-256 checksums. Reveal/KaTeX/highlight assets were extracted without modification
from their official npm tarballs. Only distribution assets required by this
template, math fonts, and licenses are retained. Montserrat font files and OFL
notice were copied unchanged from the pinned Google Fonts revision.

Matplotlib generates the original synthetic figure outputs; it is not bundled as
a runtime dependency. The cited paper is recorded in `references.bib`.
