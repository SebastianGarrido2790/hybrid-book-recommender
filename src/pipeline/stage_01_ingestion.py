"""
This module serves as the 'Conductor' for the Data Ingestion Stage of the pipeline.
It manages the transition from raw data configuration to local availability
by orchestrating the Data Ingestion component.
"""

from src.config.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion
from src.utils.logger import get_logger

STAGE_NAME = "Data Ingestion Stage"
logger = get_logger(headline=STAGE_NAME)


class DataIngestionTrainingPipeline:
    """
    Orchestration class for the Data Ingestion pipeline stage.

    Handles configuration loading, component initialization, and the execution
    of data acquisition steps (downloading and extracting).
    """

    def __init__(self):
        pass

    def main(self):
        """
        Main execution flow for the Data Ingestion stage.
        """
        try:
            logger.info("🚀 Starting Ingestion Pipeline 🚀")

            # 1. Initialize Configuration
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()

            # 2. Initialize Component
            data_ingestion = DataIngestion(config=data_ingestion_config)

            # 3. Execute Actions
            data_ingestion.download_file()
            data_ingestion.extract_zip_file()

            logger.info("✅ Completed Ingestion Pipeline ✅")

        except Exception as e:
            logger.exception(e)
            raise e


if __name__ == "__main__":
    try:
        obj = DataIngestionTrainingPipeline()
        obj.main()
    except Exception as e:
        raise e
