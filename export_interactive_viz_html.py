from __future__ import annotations

import json
import math
import os
from pathlib import Path
from time import time

REPO_ROOT = Path(__file__).resolve().parent
NOTEBOOK_PATH = REPO_ROOT / "interactive_viz.ipynb"
OUTPUT_HTML = REPO_ROOT / "index.html"
DATA_DIR = REPO_ROOT / "interactive_viz_data"


def load_notebook_code() -> str:
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    code_cells = [
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell.get("cell_type") == "code"
    ]
    return "\n\n".join(code_cells)


def remove_stale_data_files() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    for path in DATA_DIR.glob("*.json"):
        path.unlink()


def sanitize_json_value(node: object) -> object:
    if isinstance(node, dict):
        return {key: sanitize_json_value(value) for key, value in node.items()}
    if isinstance(node, list):
        return [sanitize_json_value(value) for value in node]
    if isinstance(node, float) and not math.isfinite(node):
        return None
    return node


def externalize_datasets(spec: dict[str, object]) -> tuple[dict[str, object], dict[str, str]]:
    datasets = spec.pop("datasets", {})
    dataset_urls: dict[str, str] = {}

    for dataset_name, dataset_rows in datasets.items():
        dataset_path = DATA_DIR / f"{dataset_name}.json"
        cleaned_rows = sanitize_json_value(dataset_rows)
        dataset_path.write_text(
            json.dumps(cleaned_rows, separators=(",", ":"), allow_nan=False),
            encoding="utf-8",
        )
        dataset_urls[dataset_name] = f"{DATA_DIR.name}/{dataset_path.name}"

    return spec, dataset_urls


def build_html(spec: dict[str, object], dataset_urls: dict[str, str]) -> str:
    spec_json = json.dumps(spec, separators=(",", ":"))
    dataset_urls_json = json.dumps(dataset_urls, separators=(",", ":"))
    cache_bust = str(int(time()))
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Applicant Journey Flow</title>
  <style>
    body {{
      margin: 0;
      padding: 24px;
      font-family: Georgia, serif;
      background: #f7f5ef;
      color: #1f2933;
    }}
    .page {{
      max-width: 1180px;
      margin: 0 auto;
    }}
    .page-header {{
      margin: 0 0 20px;
    }}
    .page-title {{
      margin: 0 0 8px;
      font-size: 2rem;
      line-height: 1.1;
    }}
    .page-subtitle {{
      margin: 0;
      font-size: 1rem;
      line-height: 1.5;
      color: #4b5b68;
    }}
    #vis {{
      margin: 0 auto;
    }}
    #vis.vega-embed {{
      width: 100%;
      display: flex;
    }}
    #vis.vega-embed details,
    #vis.vega-embed details summary {{
      position: relative;
    }}
    .credits {{
      margin-top: 24px;
      padding: 18px 20px;
      border: 1px solid #d8d2c6;
      background: #fffdf8;
      border-radius: 10px;
    }}
    .credits-title {{
      margin: 0 0 12px;
      font-size: 1.05rem;
    }}
    .credits-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 10px 18px;
      margin-bottom: 14px;
    }}
    .credit-name {{
      display: block;
      font-weight: 700;
      margin-bottom: 2px;
    }}
    .credit-email {{
      color: #4b5b68;
      text-decoration: none;
    }}
    .credits-note {{
      margin: 0;
      line-height: 1.5;
      color: #4b5b68;
    }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/vega@6"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-lite@6.1.0"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-embed@7"></script>
</head>
<body>
  <main class="page">
    <header class="page-header">
      <h1 class="page-title">Applicant Journey Flow</h1>
      <p class="page-subtitle">National Heritage Academies application flow visualization.</p>
    </header>
    <div id="vis"></div>
    <section class="credits" aria-labelledby="credits-title">
      <h2 class="credits-title" id="credits-title">Assignment Information</h2>
      <div class="credits-grid">
        <div>
          <span class="credit-name">Christina Ng</span>
          <a class="credit-email" href="mailto:cwjng@umich.edu">cwjng@umich.edu</a>
        </div>
        <div>
          <span class="credit-name">Adia Lee</span>
          <a class="credit-email" href="mailto:adialee@umich.edu">adialee@umich.edu</a>
        </div>
        <div>
          <span class="credit-name">Selina Shan</span>
          <a class="credit-email" href="mailto:sselina@umich.edu">sselina@umich.edu</a>
        </div>
        <div>
          <span class="credit-name">Shirley Ai</span>
          <a class="credit-email" href="mailto:shirleyi@umich.edu">shirleyi@umich.edu</a>
        </div>
      </div>
      <p class="credits-note">Developed in partnership with National Heritage Academies, Inc. (NHA), University of Michigan School of Information, April 2026.</p>
    </section>
  </main>
  <script>
    const spec = {spec_json};
    const datasetUrls = {dataset_urls_json};
    const cacheBust = "{cache_bust}";

    Promise.all(
      Object.entries(datasetUrls).map(([name, url]) =>
        fetch(`${{url}}?v=${{cacheBust}}`, {{ cache: "no-store" }})
          .then((response) => {{
            if (!response.ok) {{
              throw new Error(`Failed to load ${{url}}: ${{response.status}}`);
            }}
            return response.json();
          }})
          .then((data) => [name, data])
      )
    )
      .then((entries) => {{
        spec.datasets = Object.fromEntries(entries);
        return vegaEmbed("#vis", spec, {{ mode: "vega-lite", actions: false }});
      }})
      .catch((error) => {{
        document.getElementById("vis").innerHTML = `<pre>${{error.message}}</pre>`;
        throw error;
      }});
  </script>
</body>
</html>
"""


def main() -> None:
    os.chdir(REPO_ROOT)
    remove_stale_data_files()

    namespace: dict[str, object] = {"__name__": "__main__"}
    notebook_code = load_notebook_code()
    exec(compile(notebook_code, str(NOTEBOOK_PATH), "exec"), namespace)

    dashboard = namespace.get("dashboard")
    if dashboard is None:
        raise RuntimeError("The notebook did not define a `dashboard` chart.")

    spec, dataset_urls = externalize_datasets(dashboard.to_dict())
    OUTPUT_HTML.write_text(build_html(spec, dataset_urls), encoding="utf-8")


if __name__ == "__main__":
    main()
