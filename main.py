"""
This module acts as the entry point for the hybrid book recommender system.
It orchestrates the project's pipeline.
It sits at the top level so you can easily run uv run python main.py from your terminal without navigating into subfolders.
"""

from src.utils.logger import get_logger
from src.pipeline.stage_01_ingestion import DataIngestionTrainingPipeline

STAGE_NAME = "Data Ingestion Stage"
logger = get_logger(__name__)

try:
    logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n")
except Exception as e:
    logger.exception(e)
    raise e
