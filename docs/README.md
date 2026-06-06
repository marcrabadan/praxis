# praxis — landing page (GitHub Pages)

Static promo page for the **praxis** plugin. No build, no dependencies:
vanilla HTML + CSS + JS. Served as-is from GitHub Pages.

## Files

| File           | Purpose                                                |
| -------------- | ------------------------------------------------------ |
| `index.html`   | Main page (hero, experts, memory, install) + JSON-LD   |
| `styles.css`   | Styles (dark + light themes, responsive, WCAG AA)      |
| `script.js`    | Theme toggle, scrollspy nav, tabs, menu, copy, reveal  |
| `favicon.svg`  | Icon                                                   |
| `.nojekyll`    | Disables GitHub Pages' Jekyll processing               |

## Enabling GitHub Pages

1. On GitHub: **Settings → Pages**.
2. Under **Build and deployment → Source**, pick **Deploy from a branch**.
3. Select the branch (e.g. `main`) and the **`/docs`** folder.
4. Save. The page will be published at:
   `https://marcrabadan.github.io/praxis/`

> If you prefer to publish from another branch, select it in step 3.
> Everything in `/docs` is served unmodified thanks to `.nojekyll`.

## Local development

Any static server works. For example:

```bash
cd docs && python3 -m http.server 8080
# open http://localhost:8080
```
