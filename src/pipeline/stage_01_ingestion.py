"""
This pipeline orchestrates the Data Ingestion stage.
It triggers the download and extraction of the raw dataset.
"""

from src.config.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion
from src.utils.logger import get_logger

STAGE_NAME = "Data Ingestion Stage"


class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        logger = get_logger(__name__, headline=STAGE_NAME)
        try:
            logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")

            # 1. Initialize Configuration
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()

            # 2. Initialize Component
            data_ingestion = DataIngestion(config=data_ingestion_config)

            # 3. Execute Actions
            data_ingestion.download_file()
            data_ingestion.extract_zip_file()

            logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

        except Exception as e:
            logger.exception(e)
            raise e


if __name__ == "__main__":
    try:
        obj = DataIngestionTrainingPipeline()
        obj.main()
    except Exception as e:
        raise e
