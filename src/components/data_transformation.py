"""
This module serves as the 'Worker' for the Data Transformation Stage of the pipeline.
It handles the train-test-validation split for model development and evaluation.
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from src.utils.logger import get_logger
from src.entity.config_entity import DataTransformationConfig

logger = get_logger(__name__)


class DataTransformation:
    """
    This class implements the 'Transformation' stage of the CRISP-DM lifecycle,
    ensuring data quality and deterministic data lineage for MLOps tracking.
    """

    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def initiate_data_transformation(self):
        """
        Orchestrates the full transformation pipeline.

        Reads the ingested CSV and cleaned data, performs a 3-way split
        (Train/Val/Test), and saves the resulting artifacts (train.csv, val.csv, test.csv)
        to the root directory.

        Raises:
            Exception: If any error occurs during the transformation process.
        """
        try:
            # NOTE: We read the CLEAN data, not the raw data
            data_path = self.config.data_path
            df = pd.read_csv(data_path)
            logger.info(f"Loaded CLEAN data from {data_path} with shape {df.shape}")

            # Perform 3-Way Split
            train_df, temp_df = train_test_split(
                df,
                test_size=self.config.test_size,
                random_state=self.config.random_state,
            )

            val_df, test_df = train_test_split(
                temp_df,
                test_size=self.config.val_size,
                random_state=self.config.random_state,
            )

            logger.info(
                f"Split Ratios - Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}"
            )

            train_df.to_csv(
                os.path.join(self.config.root_dir, "train.csv"), index=False
            )
            val_df.to_csv(os.path.join(self.config.root_dir, "val.csv"), index=False)
            test_df.to_csv(os.path.join(self.config.root_dir, "test.csv"), index=False)

            logger.info(
                f"Transformation Completed. Artifacts saved to {self.config.root_dir}"
            )

        except Exception as e:
            logger.exception(e)
            raise e
