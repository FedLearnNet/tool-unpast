from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pyfedappwrap.learning.run_runfig import (AppConfig, AppInputConfig, AppOutputConfig)


@dataclass
class MyAppConfig(AppConfig):
    binarization_method: str = "kmeans"
    p_value: float = 0.05
    clustering_method: str = "Louvain"
    deep_split: int = 2
    dynamic_tree_cut: float = 0.5
    ceiling: int = 3
    bidirectional: bool = True
    seed: int = 42
    similarity_cutoff_mode: str = "automatic"
    similarity_cutoff_value: float = 0.5


# input data files
@dataclass
class MyAppInputConfig(AppInputConfig):
    data: Any = None


# outputs
@dataclass
class MyAppOutputConfig(AppOutputConfig):
    outputFile: Any = None
