"""
This module serves as the 'Conductor' for the Model Training Stage of the pipeline.
It orchestrates the execution of vector database building by managing configurations
and triggering the ModelTrainer component.
"""

from src.config.configuration import ConfigurationManager
from src.components.model_trainer import ModelTrainer
from src.utils.logger import get_logger

STAGE_NAME = "Model Training Stage"
logger = get_logger(headline=STAGE_NAME)


class ModelTrainingPipeline:
    """
    Orchestration class for the Model Training pipeline stage.

    Handles the sequence of operations: loading configuration, initializing the
    model trainer component, and executing the vector database creation logic.
    """

    def __init__(self):
        pass

    def main(self):
        """
        Main execution flow for the Model Training stage.
        """
        try:
            logger.info("🚀 Starting Model Training Pipeline 🚀")

            # 1. Load Config
            config = ConfigurationManager()
            model_trainer_config = config.get_model_trainer_config()

            # 2. Init Component
            model_trainer = ModelTrainer(config=model_trainer_config)

            # 3. Run Logic
            model_trainer.initiate_model_training()

            logger.info("✅ Model Training Pipeline Completed ✅")

        except Exception as e:
            logger.exception(e)
            raise e


if __name__ == "__main__":
    try:
        obj = ModelTrainingPipeline()
        obj.main()
    except Exception as e:
        logger.exception(e)
        raise e
