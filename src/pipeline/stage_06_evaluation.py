"""
This module serves as the 'Conductor' for the Model Evaluation Stage.
It orchestrates the execution of MLflow tracking and metric logging.
"""

from src.config.configuration import ConfigurationManager
from src.components.model_evaluation import ModelEvaluation
from src.utils.logger import get_logger

STAGE_NAME = "Model Evaluation Stage"
logger = get_logger(headline=STAGE_NAME)


class ModelEvaluationPipeline:
    """
    Orchestration class for the Model Evaluation pipeline stage.
    """

    def __init__(self):
        pass

    def main(self):
        """
        Main execution flow for the Model Evaluation stage.
        """
        try:
            logger.info("🚀 Starting Model Evaluation Pipeline 🚀")

            # 1. Load Config
            config = ConfigurationManager()
            model_evaluation_config = config.get_model_evaluation_config()

            # 2. Init Component
            model_evaluation = ModelEvaluation(config=model_evaluation_config)

            # 3. Run Logic
            model_evaluation.log_into_mlflow()

            logger.info("✅ Model Evaluation Pipeline Completed ✅")

        except Exception as e:
            logger.exception(e)
            raise e


if __name__ == "__main__":
    try:
        obj = ModelEvaluationPipeline()
        obj.main()
    except Exception as e:
        logger.exception(e)
        raise e
