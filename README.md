# si649-narrative-viz

An explorable explainer for understanding student applicant journeys at National Heritage Academies (NHA), characterizing applicant archetypes through clustering analysis. Developed by Christina Ng, Adia Lee, Selina Shan, and Shirley Ai through the University of Michigan School of Information, April 2026.

**Live site:** [https://cwjng.github.io/si649-narrative-viz/](https://cwjng.github.io/si649-narrative-viz/)

## Data Source & Availability

The dataset consists of historical student application records from a network of over 100 charter schools managed by National Heritage Academies (NHA). This data cannot be made available due to client confidentiality and NDA restrictions.

Code and methodological details are provided to enable replication with comparable data.

## Files

- `interactive_viz.ipynb`: source notebook used to prepare data and define the Altair dashboard
- `nha_clustering.ipynb`: notebook for the clustering analysis

### Site Pages

- [`index.html`](https://cwjng.github.io/si649-narrative-viz/index.html): home page for the explorable explainer
- [`flow.html`](https://cwjng.github.io/si649-narrative-viz/flow.html): interactive flow chart for applicant journeys
- [`cluster_index.html`](https://cwjng.github.io/si649-narrative-viz/cluster_index.html): interactive page to explore and understand applicant journey archetypes identified through clustering analysis
- [`appendix_cluster.html`](https://cwjng.github.io/si649-narrative-viz/appendix_cluster.html): methodology and steps taken for the clustering analysis
- [`appendix_flow.html`](https://cwjng.github.io/si649-narrative-viz/appendix_flow.html): methodology and steps taken for identifying the applicant journeys

## Dependencies
 
All dependencies are listed in `requirements.txt`. To install:
 
```bash
pip install -r requirements.txt
```
 
Or install manually:
 
```bash
pip install altair==6.0.0 ipykernel==7.2.0 jupyterlab==4.5.6 numpy==2.4.4 pandas==3.0.2 vega_datasets==0.9.0 matplotlib==3.9.2 scikit-learn==1.5.2
```
 
| Package | Version | Purpose |
|---|---|---|
| `altair` | 6.0.0 | Interactive chart and dashboard authoring |
| `ipykernel` | 7.2.0 | Jupyter notebook kernel support |
| `jupyterlab` | 4.5.6 | Notebook environment |
| `numpy` | 2.4.4 | Numerical computing |
| `pandas` | 3.0.2 | Data manipulation and analysis |
| `vega_datasets` | 0.9.0 | Sample datasets for Vega/Altair |
| `matplotlib` | 3.9.2 | Static plotting and visualization |
| `scikit-learn` | 1.5.2 | Clustering analysis and machine learning |
