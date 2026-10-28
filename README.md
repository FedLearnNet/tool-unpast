# unpast

Discovers expression biclusters with UnPaSt and exports sample groups, feature sets, and visualizations.

## Runtime inputs

The Dockerfile provisions the R/Bioconductor runtime used by UnPaSt.

## Inputs and outputs

### Inputs

| Name | Type | Description |
| --- | --- | --- |
| `data` | TSV | Expression matrix by tsv file.   Rows = Features (e.g. genes) Columns = Samples  |

### Outputs

| Name | Type | Description |
| --- | --- | --- |
| `outputFile` | CSV | A .tsv file containing the identified biclusters. |

## Configuration

| Name | Default | Description |
| --- | --- | --- |
| `binarization_method` | `kmeans` | The method used for binarization. |
| `deep_split` | `2` | The depth of splitting in the clustering process (used for 'WGCNA'). |
| `dynamic_tree_cut` | `0.5` | Threshold value for dynamic tree cut (used for 'WGCNA'). Must be in [0, 1]. |
| `ceiling` | `3` | Ceiling for z-scores to reduce outliers. Must be 0 or a positive integer. |
| `bidirectional` | `true` | Whether to find biclusters that are both up- and down-regulated. |
| `seed` | `42` | Random seed for reproducibility. |
| `similarity_cutoff_mode` | `automatic` | Mode for similarity cutoff in 'Louvain' clustering. |
| `similarity_cutoff_value` | `0.5` | Similarity cutoff value (used only if similarity_cutoff_mode is 'manual'). |
| `p_value` | `0.05` | The p-value threshold for binarization. Must be in (0, 1]. |
| `clustering_method` | `WGCNA` | The clustering method to use. |

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
# Set APP_ID and platform URLs before connecting.
python main.py
```

The Docker base image provides the FL-Net API. `requirements.txt` lists additional
runtime dependencies; `requirements-dev.txt` includes the API for local development.
Runtime datasets and trained models must be supplied separately; see `data/README.md`.

Build with `docker build -t tool-unpast .`.
