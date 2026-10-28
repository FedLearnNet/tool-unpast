from collections import defaultdict
from typing import Optional, Dict, Any

import numpy as np
import pandas as pd


def build_echarts_heatmap_from_exprs(
        exprs: pd.DataFrame,
        biclusters: Optional[pd.DataFrame] = None,
        max_rows: int = 50,  # max gene bins
        max_cols: int = 50,  # max sample bins
) -> Dict[str, Any]:
    sample_keys = defaultdict(list)
    gene_keys = defaultdict(list)

    if biclusters is not None:
        bic_samples = list(biclusters["samples"].values)
        bic_genes = list(biclusters["genes"].values)

        for sample in exprs.columns:
            sample_keys[sample] = [sample in bic for bic in bic_samples]

        for gene in exprs.index:
            gene_keys[gene] = [gene in bic for bic in bic_genes]

    samples_sorted = sorted(exprs.columns, key=lambda item: sample_keys[item], reverse=True)
    genes_sorted = sorted(exprs.index, key=lambda item: gene_keys[item], reverse=True)

    sub_exprs = exprs.loc[genes_sorted, samples_sorted]

    vmin, vmax = -3.0, 3.0  # keep your clamping range

    values = sub_exprs.to_numpy(dtype=float)
    n_genes, n_samples = values.shape

    # number of bins (rows/cols) we want
    n_row_bins = min(n_genes, max_rows)
    n_col_bins = min(n_samples, max_cols)

    # Edge indices for bins along genes and samples
    def make_edges(n_items: int, n_bins: int) -> np.ndarray:
        # edges from 0..n_items in n_bins roughly equal segments
        return np.linspace(0, n_items, n_bins + 1, dtype=int)

    row_edges = make_edges(n_genes, n_row_bins)
    col_edges = make_edges(n_samples, n_col_bins)

    # Aggregated matrix
    agg_matrix = np.empty((n_row_bins, n_col_bins), dtype=float)
    agg_matrix[:] = np.nan

    for i in range(n_row_bins):
        r_start, r_end = row_edges[i], row_edges[i + 1]
        for j in range(n_col_bins):
            c_start, c_end = col_edges[j], col_edges[j + 1]
            tile = values[r_start:r_end, c_start:c_end]
            # mean ignoring NaNs
            if tile.size == 0 or np.all(np.isnan(tile)):
                agg_val = np.nan
            else:
                agg_val = np.nanmean(tile)
            # clamp to [vmin, vmax]
            if not np.isnan(agg_val):
                agg_val = max(vmin, min(vmax, agg_val))
            agg_matrix[i, j] = agg_val

    gene_labels = []
    for i in range(n_row_bins):
        r_start, r_end = row_edges[i], row_edges[i + 1]
        genes_slice = genes_sorted[r_start:r_end]
        if len(genes_slice) == 1:
            label = genes_slice[0]
        elif len(genes_slice) > 1:
            label = f"{genes_slice[0]}..{genes_slice[-1]}"
        else:
            label = ""
        gene_labels.append(label)

    sample_labels = []
    for j in range(n_col_bins):
        c_start, c_end = col_edges[j], col_edges[j + 1]
        samples_slice = samples_sorted[c_start:c_end]
        if len(samples_slice) == 1:
            label = samples_slice[0]
        elif len(samples_slice) > 1:
            label = f"{samples_slice[0]}..{samples_slice[-1]}"
        else:
            label = ""
        sample_labels.append(label)

    data = []
    for i in range(n_row_bins):
        for j in range(n_col_bins):
            val = agg_matrix[i, j]
            value = None if np.isnan(val) else float(val)
            data.append([j, i, value])  # x = sample-bin, y = gene-bin

    option: Dict[str, Any] = {
        "tooltip": {
            "trigger": "item",
            "position": "top",
        },
        "xAxis": {
            "type": "category",
            "data": [str(x) for x in sample_labels],
            "axisLabel": {
                "rotate": 90,
                "fontSize": 9,
            },
        },
        "yAxis": {
            "type": "category",
            "data": [str(y) for y in gene_labels],
            "axisLabel": {
                "fontSize": 8,
            },
        },
        "visualMap": {
            "min": vmin,
            "max": vmax,
            "orient": "vertical",
            "right": "2%",
            "top": "middle",
            "inRange": {
                "color": [
                    "#313695",
                    "#4575b4",
                    "#74add1",
                    "#abd9e9",
                    "#e0f3f8",
                    "#ffffbf",
                    "#fee090",
                    "#fdae61",
                    "#f46d43",
                    "#d73027",
                    "#a50026",
                ]
            },
        },
        "series": [
            {
                "name": "Unpast Expression (binned mean)",
                "type": "heatmap",
                "data": data,
                "progressive": 0,
                "animation": False,
            }
        ],
    }

    return option
