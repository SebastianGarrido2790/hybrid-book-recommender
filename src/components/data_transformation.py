"""
This module handles the data transformation logic for the Hybrid Book Recommender project.
It performs data cleaning (filtering descriptions, formatting authors/categories, removing duplicates)
and orchestrates the train-test-validation split for model development and evaluation.
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from src.utils.logger import get_logger
from src.entity.config_entity import DataTransformationConfig

logger = get_logger(__name__)


class DataTransformation:
    """
    Component for cleaning raw book data and splitting it into production-ready datasets.

    This class implements the 'Transformation' stage of the CRISP-DM lifecycle,
    ensuring data quality and deterministic data lineage for MLOps tracking.
    """

    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processes the input DataFrame to ensure data quality before model training.

        Performs the following:
        - Drops records with missing descriptions.
        - Filters out descriptions shorter than the configured threshold.
        - Sanitizes 'categories' and 'authors' columns (removes bracket notation).
        - Removes duplicate records based on ISBN13.

        Args:
            df (pd.DataFrame): Raw ingested data.

        Returns:
            pd.DataFrame: Cleaned and filtered book data.
        """
        logger.info(f"Initial Shape: {df.shape}")

        # Use param from yaml for filtering
        df = df.dropna(subset=["description"])

        # New robust check using params.yaml
        if "description" in df.columns:
            df = df[df["description"].str.len() > self.config.min_desc_len]

        if "categories" in df.columns:
            df["categories"] = (
                df["categories"].astype(str).str.replace(r"[\[\]']", "", regex=True)
            )
            df = df[df["categories"].str.len() > 2]

        if "authors" in df.columns:
            df["authors"] = (
                df["authors"].astype(str).str.replace(r"[\[\]']", "", regex=True)
            )

        df = df.drop_duplicates(subset=["isbn13"])

        logger.info(f"Final Cleaned Shape: {df.shape}")
        return df

    def initiate_data_transformation(self):
        """
        Orchestrates the full transformation pipeline.

        Reads the ingested CSV, applies cleaning logic, performs a 3-way split
        (Train/Val/Test), and saves the resulting artifacts to the root directory.

        Raises:
            Exception: If any error occurs during the transformation process.
        """
        try:
            data_path = self.config.data_path
            df = pd.read_csv(data_path)
            logger.info(f"Loaded data from {data_path}")

            df_cleaned = self.clean_data(df)

            # --- MLOps Strategy: 3-Way Split using params.yaml ---
            train_df, temp_df = train_test_split(
                df_cleaned,
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
