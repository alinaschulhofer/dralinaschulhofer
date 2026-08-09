# dralinaschulhofer

Dr. Alina Schulhofer — psychotherapy practice website (dralinaschulhofer.com).

Kept deliberately separate from [Architecture of Excellence™](https://architectureofexcellence.com) (a different repo/site). See `HANDOFF.md` for full project context, design system, and editing rules.

## Structure

- **Deploy files (repo root):** `index.html`, `about.html`, `services.html`, `faq.html`, `styles.css`, `assets/` — the actual site, ready to host as-is (GitHub Pages, Netlify, etc.).
- **`src/`** — master source. Edit here, not the root files directly:
  - `therapy_template.html` — single-file SPA source of truth for all content/design.
  - `assets.b64` — base64 fonts/images injected into the template at build time.
  - `build_site.py` — regenerates the root deploy files from `therapy_template.html`.

## Editing workflow

1. Edit `src/therapy_template.html`.
2. Regenerate the deploy files: `python3 src/build_site.py` (run from the repo root).
3. Commit both the template and the regenerated root files together.

See `HANDOFF.md` §9 for the full set of rules on preserving the design system (color tokens, class names, animation conventions, etc.).
