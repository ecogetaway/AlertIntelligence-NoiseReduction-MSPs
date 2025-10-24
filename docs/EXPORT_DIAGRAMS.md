# Export Mermaid Diagrams to SVG

Destination folder:
- `public/images/`

Install Mermaid CLI (once):
- `brew install node`   (if Node not installed)
- `npm i -g @mermaid-js/mermaid-cli`

Export commands (run from project root):
- `mmdc -i docs/system-architecture.mmd -o public/images/system-architecture.svg`
- `mmdc -i docs/data-flow.mmd -o public/images/data-flow.svg`

Optional PNGs:
- `mmdc -i docs/system-architecture.mmd -o public/images/system-architecture.png -b transparent`
- `mmdc -i docs/data-flow.mmd -o public/images/data-flow.png -b transparent`

Tips:
- If labels wrap poorly, adjust wording or use `--width` (e.g., `--width 1600`).
- Most slide apps import SVG cleanly; use PNG if you need raster output.
