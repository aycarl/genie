# DiaMOND Genie — Web Version

A self-contained, single-file web version of DiaMOND Genie. It replicates the
two tabs from the desktop app (Plate Calculator and Constituent Drugs) using
only HTML, CSS, and JavaScript — no build step or dependencies.

## Run locally

Open [index.html](index.html) directly in a browser, or serve the folder with
any static file server:

```bash
python3 -m http.server --directory web
```

## Embedding on another site

Host `index.html` anywhere (e.g. GitHub Pages, a static file host, or your own
server) and embed it with an `<iframe>`:

```html
<iframe
  src="https://your-domain.example/genie/index.html"
  style="width: 100%; height: 800px; border: none;"
  title="DiaMOND Genie"
></iframe>
```

The page is responsive, so the iframe will adapt to the width of its
container — adjust `height` as needed for your layout.

## Formula

Uses the same plate-estimate formula as the desktop app — see the
[formula reference](../docs/formula-reference.md) for details.
