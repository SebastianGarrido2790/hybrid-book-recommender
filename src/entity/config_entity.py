"""
This module defines the configuration for data transformation.
It includes the root directory, data path, and tokenizer name.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    # Params
    test_size: float
    val_size: float
    random_state: int
    min_desc_len: int
    tokenizer_name: str = None  # Optional: for adding tokenization later
