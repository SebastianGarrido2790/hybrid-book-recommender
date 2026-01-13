"""
This script is used to perform predictions using the HybridRecommender model.
It loads the model from the specified configuration and runs a set of test queries.
Results are saved to a text file in the artifacts/prediction directory.
"""

from src.utils.logger import get_logger

# Initialize logger with headline BEFORE importing stages
# This ensures "stage_05_prediction.py" is the recorded headline for this process
logger = get_logger(__name__, headline="PredictionPipeline")

from src.config.configuration import ConfigurationManager
from src.models.hybrid_recommender import HybridRecommender
from src.utils.paths import PROJECT_ROOT


class PredictionPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            # 1. Load Configuration
            config_manager = ConfigurationManager()
            inference_config = config_manager.get_inference_config()

            # 2. Init Component
            recommender = HybridRecommender(config=inference_config)

            # Test cases to verify different aspects (semantic vs hybrid)
            queries = [
                "A cyberpunk novel about artificial intelligence",
                "A historical fiction about Roman Empire",
                "A book about learning machine learning",
            ]

            # 3. Define Output Path
            output_dir = PROJECT_ROOT / "artifacts" / "prediction"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / "results.txt"

            with open(output_file, "w", encoding="utf-8") as f:
                for query in queries:
                    logger.info(f"🔍 Testing Query: {query}")
                    print(f"\n🔍 Query: {query}")
                    print("-" * 60)
                    f.write(f"\n🔍 Query: {query}\n")
                    f.write("-" * 60 + "\n")

                    results = recommender.recommend(query)

                    for i, book in enumerate(results):
                        print(
                            f"{i + 1}. {book['title']} (Rating: {book['rating']}, Score: {book['score']:.3f})"
                        )
                        print(f"   Author: {book['authors']}")
                        # Truncate description for cleaner output
                        result_line = f"{i + 1}. {book['title']} (Rating: {book['rating']}, Score: {book['score']:.3f})\n"
                        f.write(result_line)
                        f.write(f"   Author: {book['authors']}\n")

                        desc_preview = (
                            book["description"][:100].replace("\n", " ") + "..."
                            if book["description"]
                            else "No description"
                        )
                        print(f"   Desc: {desc_preview}")
                        f.write(f"   Desc: {desc_preview}\n")

            logger.info(f"✅ Results saved to {output_file}")

        except Exception as e:
            logger.exception(e)
            raise e


if __name__ == "__main__":
    try:
        logger.info("🚀 Prediction Pipeline Started 🚀")
        obj = PredictionPipeline()
        obj.main()
        logger.info("✅ Prediction Pipeline Completed ✅")
    except Exception as e:
        logger.exception(e)
        raise e
