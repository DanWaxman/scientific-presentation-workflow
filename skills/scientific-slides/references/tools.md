# Portable deck tools

These commands use Python 3.10 or newer. Resolve the script paths relative to this
skill's installation; they do not depend on a particular agent or working directory.

## Start a deck

```sh
python /path/to/scientific-slides/scripts/new_deck.py my-talk
```

The destination must not exist. The command copies the complete offline gallery,
including its draft, source, finished media, fonts, runtime, and license notices.
Open `my-talk/index.html` directly in a browser. Viewing requires no Python, Node,
server, or network connection. A local HTTP server is optional:

```sh
python -m http.server --directory my-talk 8000
```

Edit `presentation.md`, then translate the agreed content into `index.html` with
your agent. The draft is tracked source, not an executable slide compiler.

## Capture slides and reveals

Install the optional automated-review dependencies in a virtual environment:

```sh
python -m pip install playwright pillow
python -m playwright install chromium
python /path/to/scientific-slides/scripts/preview.py my-talk --sheet
python /path/to/scientific-slides/scripts/preview.py my-talk --all-fragments --sheet
python /path/to/scientific-slides/scripts/preview.py my-talk --slides 3,5 --all-fragments
```

An installed Chromium browser can replace Playwright's download:

```sh
python /path/to/scientific-slides/scripts/preview.py my-talk --browser /path/to/chromium
```

`SLIDES_BROWSER` is the equivalent environment override. Browser dependencies are
needed only for automated review. Playwright's browser installation may require
additional system packages on Linux; use its documented browser setup for your OS.

Each run creates a new timestamped directory under `my-talk/.preview/`; previous
reviews are never deleted. `--out DIR` changes that parent. Slides are numbered
from **1** in the command and filenames, regardless of Reveal's zero-based URLs.
Without `--all-fragments`, each slide is captured with its final reveal visible.
With it, the initial state and every distinct fragment index are captured.

The tool blocks HTTP(S) requests to test offline rendering, waits for Reveal,
fonts, and visible media, and writes a `manifest.json` with the slide inventory,
screenshots, and detected errors. It exits unsuccessfully on missing media,
KaTeX failures, JavaScript errors, or blocked external asset requests. Read the
images; successful capture does not prove a layout is visually correct.

Useful options:

- `--scale 1.5`: higher-resolution screenshots; default is the 960×700 canvas at 1×.
- `--video-time 4`: pause visible videos at four seconds for snapshots; default is the beginning.
- `--settle-ms 1200`: allow longer custom transitions to finish.
- `--reduced-motion reduce`: check the reduced-motion presentation.
- `--sheet`: create a contact sheet with Pillow.

Snapshots pause media for repeatability. Check actual playback, forward/backward
navigation, and deep links separately in a browser.

## Prepare publication files

```sh
python /path/to/scientific-slides/scripts/package.py my-talk --out public-talk
```

The output must be a new directory outside the source deck. This command copies
`index.html`, `styles.css`, `slides.js`, `LICENSE`, `THIRD_PARTY_NOTICES.md`, approved
media formats in `figs/`, and runtime, font, stylesheet, and license files in
`vendor/` (including its pinned-dependency `provenance.json`). It checks static
local HTML/SVG/CSS references before writing. Symlinks,
remote assets, and references to omitted files are rejected. It does not analyze
arbitrary dynamically constructed JavaScript URLs; preview the staged copy too.

Drafts, bibliography source, scientific source, cached data, and previews are not
publication files. New asset directories or formats require an explicit update to
the allowlist in `package.py`; do not solve an omitted asset by copying the entire
project. Nothing is uploaded, deployed, committed, or pushed by these tools.

For Jekyll, merge the template's `exclude` entries into the site's existing
`_config.yml`; preserve its other exclusions. Excluding drafts from Git would
remove valuable authoring history, and `.nojekyll` alone does not exclude drafts
from publication. Prefer publishing the staged directory when the hosting system
allows it.
