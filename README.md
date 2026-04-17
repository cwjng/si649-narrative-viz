# si649-narrative-viz

Interactive applicant journey visualization for National Heritage Academies, Inc. (NHA), developed by Christina Ng, Adia Lee, Selina Shan, and Shirley Ai through the University of Michigan School of Information, April 2026.

## Files

- `interactive_viz.ipynb`: source notebook used to prepare data and define the Altair dashboard
- `export_interactive_viz_html.py`: exports the dashboard into a hostable HTML page
- `index.html`: GitHub Pages entry point
- `interactive_viz_data/`: JSON datasets loaded by `index.html`

## Regenerate The Hosted Visualization

Run:

```bash
python3 export_interactive_viz_html.py
```

This refreshes `index.html` and the JSON files in `interactive_viz_data/`.

## GitHub Pages

Configure GitHub Pages to deploy from:

- Branch: `main`
- Folder: `/ (root)`

The site will be available at:

`https://cwjng.github.io/si649-narrative-viz/`
