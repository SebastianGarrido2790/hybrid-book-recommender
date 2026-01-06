"""
This module acts as the entry point for the hybrid book recommender system.
It orchestrates the project's pipeline, useful for debugging and development.
It sits at the top level so you can easily run uv run python main.py from your terminal without navigating into subfolders.
"""

from src.utils.logger import get_logger, log_spacer
from src.pipeline.stage_01_ingestion import DataIngestionTrainingPipeline
from src.pipeline.stage_02_transformation import DataTransformationTrainingPipeline

logger = get_logger(headline="main.py")

# Data Ingestion Stage
try:
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
except Exception as e:
    logger.exception(e)
    raise e

log_spacer()

# Data Transformation Stage
try:
    data_transformation = DataTransformationTrainingPipeline()
    data_transformation.main()
except Exception as e:
    logger.exception(e)
    raise e
