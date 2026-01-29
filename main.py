"""
This module acts as the entry point for the hybrid book recommender system.
It orchestrates the project's pipeline stages in order for debugging and testing to be easier.
"""

from src.pipeline.stage_01_ingestion import DataIngestionTrainingPipeline
from src.pipeline.stage_02_validation import DataValidationTrainingPipeline
from src.pipeline.stage_03_transformation import DataTransformationTrainingPipeline
from src.pipeline.stage_04_training import ModelTrainingPipeline
from src.pipeline.stage_05_prediction import PredictionPipeline
from src.pipeline.stage_06_evaluation import ModelEvaluationPipeline
from src.utils.logger import get_logger, log_spacer

# Initialize logger with headline
logger = get_logger(headline="main.py")


# 1. Data Ingestion
try:
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
except Exception as e:
    logger.exception(e)
    raise e

log_spacer()

# 2. Data Validation
try:
    data_validation = DataValidationTrainingPipeline()
    data_validation.main()
except Exception as e:
    logger.exception(e)
    raise e

log_spacer()

# 3. Data Transformation
try:
    data_transformation = DataTransformationTrainingPipeline()
    data_transformation.main()
except Exception as e:
    logger.exception(e)
    raise e

log_spacer()

# 4. Model Training
try:
    model_trainer = ModelTrainingPipeline()
    model_trainer.main()
except Exception as e:
    logger.exception(e)
    raise e

log_spacer()

# 5. Prediction
try:
    prediction = PredictionPipeline()
    prediction.main()
except Exception as e:
    logger.exception(e)
    raise e

log_spacer()

# 6. Model Evaluation
try:
    model_evaluation = ModelEvaluationPipeline()
    model_evaluation.main()
except Exception as e:
    logger.exception(e)
    raise e
