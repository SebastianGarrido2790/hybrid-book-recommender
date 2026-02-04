"""
This module serves as the 'Worker' for the Data Validation Stage of the pipeline.
It handles the data cleaning and validation process to ensure data quality.
"""

import sys
import pandas as pd
from src.entity.config_entity import DataValidationConfig
from src.utils.logger import get_logger
from src.utils.exception import CustomException

logger = get_logger(__name__)


class DataValidation:
    """
    This class performs data cleaning steps such as dropping missing values,
    filtering by description length, cleaning artifacts from text columns,
    deduplicating entries, and enforcing schema checks.
    """

    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_and_clean_data(self) -> bool:
        """
        Reads raw data, cleans it, checks validity, and saves the clean version.

        Performs a series of cleaning operations:
        1. Drops rows with missing critical fields.
        2. Filters rows based on description length.
        3. Cleans text artifacts in 'categories' and 'authors' columns.
        4. Deduplicates based on ISBN.
        5. Checks if the resulting dataset is empty.

        Returns:
            bool: True if validation and cleaning were successful (dataset not empty), False otherwise.
        """
        try:
            logger.info(f"Loading raw data from {self.config.unzip_data_dir}")
            df = pd.read_csv(self.config.unzip_data_dir)
            initial_shape = df.shape

            # 1. Drop missing critical fields
            df = df.dropna(subset=["description", "title"])

            # 2. Filter by description length
            if "description" in df.columns:
                df = df[df["description"].str.len() > self.config.min_desc_len]

            # 3. Clean Text Artifacts (Categories/Authors)
            # Removes brackets ['Fiction'] -> Fiction
            if "categories" in df.columns:
                df["categories"] = (
                    df["categories"].astype(str).str.replace(r"[\[\]']", "", regex=True)
                )
                df = df[df["categories"].str.len() > self.config.categories_min_len]

            if "authors" in df.columns:
                df["authors"] = (
                    df["authors"].astype(str).str.replace(r"[\[\]']", "", regex=True)
                )

            # 4. Deduplicate
            df = df.drop_duplicates(subset=["isbn13"])

            final_shape = df.shape
            dropped_rows = initial_shape[0] - final_shape[0]
            logger.info(
                f"Cleaning complete. Dropped {dropped_rows} rows. Final shape: {final_shape}"
            )

            # 5. Validation Check
            validation_status = True
            if df.empty:
                validation_status = False
                logger.error("Validation Failed: Dataset is empty after cleaning!")

            # 6. Save Artifacts
            # Save status
            with open(self.config.STATUS_FILE, "w") as f:
                f.write(f"Validation status: {validation_status}\n")
                f.write(f"Rows retained: {final_shape[0]}")

            # Save clean data
            if validation_status:
                df.to_csv(self.config.cleaned_data_file, index=False)
                logger.info(f"Cleaned data saved to {self.config.cleaned_data_file}")

            return validation_status

        except Exception as e:
            raise CustomException(e, sys)
