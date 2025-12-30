"""
This script creates the needed folder structure for a machine learning project.
"""

import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s")

source_code = "src"

list_of_files = [
    ".github/workflows/main.yaml",
    "config/config.yaml",
    "config/params.yaml",
    "data/external/.gitkeep",
    "data/interim/.gitkeep",
    "data/processed/.gitkeep",
    "data/raw/.gitkeep",
    "models/.gitkeep",
    "notebooks/.gitkeep",
    "references/.gitkeep",
    "reports/docs/.gitkeep",
    "reports/figures/.gitkeep",
    f"{source_code}/__init__.py",
    f"{source_code}/features/__init__.py",
    f"{source_code}/features/build_features.py",
    f"{source_code}/components/__init__.py",
    f"{source_code}/components/data_ingestion.py",
    f"{source_code}/components/data_validation.py",
    f"{source_code}/components/data_transformation.py",
    f"{source_code}/components/model_trainer.py",
    f"{source_code}/config/__init__.py",
    f"{source_code}/config/configuration.py",
    f"{source_code}/entity/__init__.py",
    f"{source_code}/entity/config_entity.py",
    f"{source_code}/pipeline/__init__.py",
    f"{source_code}/pipeline/stage_01_ingestion.py",
    f"{source_code}/pipeline/stage_02_validation.py",
    f"{source_code}/pipeline/stage_03_training.py",
    f"{source_code}/models/__init__.py",
    f"{source_code}/models/hybrid_recommender.py",
    f"{source_code}/models/llm_utils.py",
    f"{source_code}/utils/__init__.py",
    f"{source_code}/utils/common.py",
    f"{source_code}/utils/paths.py",
    f"{source_code}/utils/mlflow_config.py",
    f"{source_code}/utils/exception.py",
    f"{source_code}/utils/logger.py",
    f"{source_code}/visualization/__init__.py",
    f"{source_code}/visualization/plot_settings.py",
    f"{source_code}/visualization/visualize.py",
    "dvc.yaml",
    "pyproject.toml",
    "Dockerfile",
    "README.md",
    "LICENSE.txt",
    ".env",
    ".gitignore",
    "main.py",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")
