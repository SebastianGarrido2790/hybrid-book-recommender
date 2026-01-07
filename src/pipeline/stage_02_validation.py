"""
This module serves as the 'Conductor' for the Data Validation Stage of the pipeline.
It manages the transition from raw data configuration to local availability
by orchestrating the DataValidation component.
"""

from src.config.configuration import ConfigurationManager
from src.components.data_validation import DataValidation
from src.utils.logger import get_logger

STAGE_NAME = "Data Validation Stage"
logger = get_logger(headline=STAGE_NAME)


class DataValidationTrainingPipeline:
    """
    It coordinates the initialization of the configuration manager,
    fetching of data validation config, and execution of the DataValidation component.
    """

    def __init__(self):
        pass

    def main(self):
        """
        Executes the main steps of the Data Validation pipeline.

        1. Initialize ConfigurationManager.
        2. Retrieve DataValidationConfig.
        3. Instantiate DataValidation component.
        4. Execute validate_and_clean_data method.
        """
        try:
            logger.info("🚀 Starting Validation Pipeline 🚀")

            config = ConfigurationManager()
            data_validation_config = config.get_data_validation_config()

            data_validation = DataValidation(config=data_validation_config)
            data_validation.validate_and_clean_data()

            logger.info("✅ Validation Pipeline Completed ✅")
        except Exception as e:
            logger.exception(e)
            raise e


if __name__ == "__main__":
    try:
        obj = DataValidationTrainingPipeline()
        obj.main()
    except Exception as e:
        logger.exception(e)
        raise e
