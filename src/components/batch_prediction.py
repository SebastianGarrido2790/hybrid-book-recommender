"""
This module contains the BatchPrediction component, which runs inference on a set of queries
and saves the results to a file, satisfying the 'heavy lifting' requirement.
"""

from src.entity.config_entity import BatchPredictionConfig, InferenceConfig
from src.models.hybrid_recommender import HybridRecommender
from src.utils.logger import get_logger
from src.utils.exception import CustomException
import sys

logger = get_logger(__name__)


class BatchPrediction:
    """
    Component responsible for running batch predictions using the HybridRecommender.
    """

    def __init__(
        self,
        batch_config: BatchPredictionConfig,
        inference_config: InferenceConfig,
    ):
        """
        Initializes the BatchPrediction component.

        Args:
            batch_config (BatchPredictionConfig): Configuration for batch output.
            inference_config (InferenceConfig): Configuration for the recommender model.
        """
        try:
            self.batch_config = batch_config
            self.recommender = HybridRecommender(config=inference_config)
        except Exception as e:
            raise CustomException(e, sys)

    def run_batch_predictions(self, queries: list):
        """
        Runs predictions for the provided queries and saves results to the configured file.

        Args:
            queries (list): List of natural language queries to test.
        """
        try:
            output_file = self.batch_config.results_file

            # Ensure parent dir exists (though create_directories usually handles this)
            # output_file.parent.mkdir(parents=True, exist_ok=True)

            logger.info(f"Starting batch prediction for {len(queries)} queries.")
            logger.info(f"Saving results to: {output_file}")

            with open(output_file, "w", encoding="utf-8") as f:
                for query in queries:
                    logger.info(f"🔍 Testing Query: {query}")
                    print(f"\n🔍 Query: {query}")
                    print("-" * 60)
                    f.write(f"\n🔍 Query: {query}\n")
                    f.write("-" * 60 + "\n")

                    try:
                        results = self.recommender.recommend(query)
                    except Exception as e:
                        logger.error(
                            f"Failed to get recommendations for query '{query}': {e}"
                        )
                        f.write(f"Error: {e}\n")
                        continue

                    for i, book in enumerate(results):
                        result_str = (
                            f"{i + 1}. {book.get('title', 'Unknown')} | "
                            f"{book.get('category', 'Unknown')} "
                            f"(Rating: {book.get('rating', 'N/A')}, Score: {book.get('score', 0):.3f})"
                        )

                        print(result_str)
                        print(f"   Author: {book.get('authors', 'Unknown')}")

                        f.write(result_str + "\n")
                        f.write(f"   Author: {book.get('authors', 'Unknown')}\n")

                        desc = book.get("description", "")
                        desc_preview = (
                            desc[:100].replace("\n", " ") + "..."
                            if desc
                            else "No description"
                        )
                        print(f"   Desc: {desc_preview}")
                        f.write(f"   Desc: {desc_preview}\n")

            logger.info("Batch prediction completed successfully.")

        except Exception as e:
            raise CustomException(e, sys)
