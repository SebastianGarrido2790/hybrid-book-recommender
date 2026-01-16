"""
OFFLINE SCRIPT: Data Enrichment via Zero-Shot Classification.

This script reads the cleaned book dataset and uses a Large Language Model (BART)
to classify each book into a simplified 'Broad Category' based on its description.

WARNING: This process is CPU/GPU intensive.
On a standard CPU, expect approx 0.5 - 1.0 seconds per book.
"""

import pandas as pd
from tqdm import tqdm
from transformers import pipeline
import torch
from src.entity.config_entity import DataEnrichmentConfig
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataEnrichment:
    """
    Component for enriching book metadata using Zero-Shot Classification.
    Standardizes messy categories into a few broad, usable facets.
    """

    def __init__(self, config: DataEnrichmentConfig):
        self.config = config

    def initiate_data_enrichment(self):
        """
        Executes the enrichment process.
        """
        try:
            logger.info(f"Loading data from {self.config.data_path}")
            df = pd.read_csv(self.config.data_path)

            # Fill NaNs in descriptions with empty string
            descriptions = df["description"].fillna("").tolist()

            logger.info(
                f"Initializing Zero-Shot Classification model: {self.config.model_name}"
            )
            # Use CPU (-1) as per plan, but if GPU is available it could be used.
            device = 0 if torch.cuda.is_available() else -1
            if device == 0:
                logger.info("GPU detected, using GPU for classification.")
            else:
                logger.info("No GPU detected, using CPU. This might be slow.")

            classifier = pipeline(
                "zero-shot-classification", model=self.config.model_name, device=device
            )

            candidate_labels = self.config.candidate_labels
            batch_size = self.config.batch_size

            logger.info(f"Enriching {len(df)} books in batches of {batch_size}...")

            new_categories = []

            for i in tqdm(
                range(0, len(descriptions), batch_size), desc="Classifying Descriptions"
            ):
                batch = descriptions[i : i + batch_size]

                # Zero-shot classification
                results = classifier(batch, candidate_labels, multi_label=False)

                # Extract top labels
                for res in results:
                    new_categories.append(res["labels"][0])

            df["simple_category"] = new_categories

            logger.info(f"Saving enriched data to {self.config.enriched_data_path}")
            df.to_csv(self.config.enriched_data_path, index=False)

            logger.info("✅ Data enrichment completed successfully.")

        except Exception as e:
            logger.error(f"Error during data enrichment: {e}")
            raise e
