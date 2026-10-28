from pathlib import Path
from typing import Optional, List

import pandas as pd
from pyfedappwrap.learning.app_types import BaseSelfLearnedApp
from pyfedappwrap.learning.run_runfig import AppOutputVisualisations
from typing_extensions import override

from config import MyAppConfig, MyAppInputConfig, MyAppOutputConfig
from run_unpast import run_unpast
from viz import build_echarts_heatmap_from_exprs


class MyAPP(BaseSelfLearnedApp[MyAppConfig, MyAppInputConfig, MyAppOutputConfig]):

    def __init__(self):
        super().__init__()

    def run_algorithm(self, data: MyAppInputConfig) -> MyAppOutputConfig:
        exprs = data.data

        output_dir = Path("./output")
        output_dir.mkdir(exist_ok=True, parents=True)

        self.logger.info("Starting unpast biclustering...")
        result = self.run_unpast(exprs, str(output_dir))
        self.logger.info(f"Finished unpast biclustering.")

        heatmap = build_echarts_heatmap_from_exprs(exprs, result)
        return MyAppOutputConfig(outputFile=result,
                                 visualisations=[AppOutputVisualisations(name="Heatmap",
                                                                         description="Unpast Heatmap (max rows and cols = 50)",
                                                                         visualisation=heatmap)])

    def run_unpast(self, exprs: pd.DataFrame, out_dir: str):
        # Map high-level config → underlying algorithm parameters
        directions: List[str] = ["DOWN", "UP"] if self.config.bidirectional else ["UP"]
        # similarity_cutoffs: -1 enables the algorithm's automatic mode; otherwise pass manual cutoff value
        similarity_cutoffs = -1 if self.config.similarity_cutoff_mode == "automatic" else float(
            self.config.similarity_cutoff_value)

        try:
            return run_unpast(
                exprs=exprs,
                out_dir=out_dir,
                ceiling=self.config.ceiling,
                bin_method=self.config.binarization_method,
                clust_method=self.config.clustering_method,
                pval=self.config.p_value,
                directions=directions,
                similarity_cutoffs=similarity_cutoffs,
                ds=self.config.deep_split,
                dch=self.config.dynamic_tree_cut,
                seed=self.config.seed,
                logger=self.logger,
            )
        except Exception as e:
            self.logger.error(f"Error running unpast: {str(e)}")
            raise

    @override
    def get_test_data(self) -> Optional[dict[str, Path]]:
        return {"data": Path("data/test_unpast.tsv")}
