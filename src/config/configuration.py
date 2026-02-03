"""
This module serves as the 'Brain' of the system, responsible for coordinating configurations and parameters across the pipeline.
It centralizes the loading of 'config.yaml' and 'params.yaml', providing strictly-typed Configuration Entity objects for other components.
"""

import dvc.api
from box import ConfigBox

from src.utils.common import read_yaml, create_directories
from src.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    DataEnrichmentConfig,
    ToneAnalysisConfig,
    ModelTrainerConfig,
    InferenceConfig,
    ModelEvaluationConfig,
)
from src.utils.paths import CONFIG_FILE_PATH, PARAMS_FILE_PATH, PROJECT_ROOT
from pathlib import Path
from src.utils.mlflow_config import get_mlflow_uri


class ConfigurationManager:
    """
    Manages project configurations and parameters.

    This class centralizes the loading of 'config.yaml' and 'params.yaml',
    providing strictly-typed Configuration Entity objects for other components.
    """

    def __init__(
        self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH
    ):
        """
        Initializes the ConfigurationManager.

        Args:
            config_filepath (Path): Path to the static configuration file.
            params_filepath (Path): Path to the parameters file (tracked by DVC).
        """
        import os

        self.config = read_yaml(config_filepath)

        # DVC API expects paths relative to the project root
        rel_params_path = os.path.relpath(params_filepath, PROJECT_ROOT)

        try:
            params_dict = dvc.api.params_show(rel_params_path)
            self.params = ConfigBox(params_dict)
        except Exception:
            # Fallback for production/Docker environments without .git/.dvc
            self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Creates the Data Ingestion configuration entity.

        Returns:
            DataIngestionConfig: Configuration for the data ingestion component.
        """
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir,
        )

        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        """
        Creates the Data Validation configuration entity.

        Returns:
            DataValidationConfig: Configuration object containing paths and parameters
            for the data validation stage.
        """
        config = self.config.data_validation
        params = self.params.data_validation

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            unzip_data_dir=config.unzip_data_dir,
            STATUS_FILE=config.STATUS_FILE,
            cleaned_data_file=config.cleaned_data_file,
            min_desc_len=params.min_desc_len,
            categories_min_len=params.categories_min_len,
        )

        return data_validation_config

    def get_data_transformation_config(self) -> DataTransformationConfig:
        """
        Creates the Data Transformation configuration entity.

        Returns:
            DataTransformationConfig: Configuration object containing paths, split ratios,
            and parameters for the data transformation stage.
        """
        config = self.config.data_transformation
        params = self.params.data_transformation

        create_directories([config.root_dir])

        # NOTE: We removed min_desc_len from here as it's now handled upstream
        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            test_size=params.test_size,
            val_size=params.val_size,
            random_state=params.random_state,
        )

        return data_transformation_config

    def get_data_enrichment_config(self) -> DataEnrichmentConfig:
        """
        Creates the Data Enrichment (Zero-Shot) configuration entity.
        """
        config = self.config.data_enrichment
        params = self.params.data_enrichment

        create_directories([config.root_dir])

        data_enrichment_config = DataEnrichmentConfig(
            root_dir=Path(config.root_dir),
            data_path=Path(config.data_path),
            enriched_data_path=Path(config.enriched_data_path),
            model_name=params.model_name,
            candidate_labels=params.candidate_labels,
            batch_size=params.batch_size,
        )

        return data_enrichment_config

    def get_tone_analysis_config(self) -> ToneAnalysisConfig:
        """
        Creates the Tone Analysis (Sentiment) configuration entity.
        """
        config = self.config.tone_analysis
        params = self.params.tone_analysis

        create_directories([config.root_dir])

        # Ensure we chain from Enrichment if available, enabling fallback logic is handled
        # by the component loading, but here we explicitly prefer enriched data as input source.
        source_data = Path(config.data_path)
        if not source_data.exists():
            # If Enriched data doesn't exist, fallback to clean data directly?
            # Ideally tone analysis should come after enrichment.
            # But for robustness, we can fallback to clean data.
            source_data = Path(self.config.data_validation.cleaned_data_file)

        tone_analysis_config = ToneAnalysisConfig(
            root_dir=Path(config.root_dir),
            data_path=source_data,
            output_path=Path(config.output_path),
            model_name=params.model_name,
            target_emotions=params.target_emotions,
            batch_size=params.batch_size,
        )

        return tone_analysis_config

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        """
        Creates the Model Trainer (Vector DB) configuration entity.

        Returns:
            ModelTrainerConfig: Configuration object for vector database creation.
        """
        config = self.config.model_trainer
        params = self.params.model_trainer

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            db_path=config.db_path,
            model_name=params.model_name,
            collection_name=params.collection_name,
            embedding_provider=params.embedding_provider,
            batch_size=params.batch_size,
        )

        return model_trainer_config

    def get_inference_config(self) -> InferenceConfig:
        """
        Creates the Inference configuration entity.
        """
        model_trainer_config = self.config.model_trainer
        params_inference = self.params.inference

        # 1. Check for Toned Data (Highest Level)
        data_path = PROJECT_ROOT / self.config.tone_analysis.output_path

        # 2. Fallback to Enriched Data
        if not data_path.exists():
            data_path = PROJECT_ROOT / self.config.data_enrichment.enriched_data_path

        # 3. Fallback to Clean Data (Base Level)
        if not data_path.exists():
            data_path = PROJECT_ROOT / self.config.data_validation.cleaned_data_file

        inference_config = InferenceConfig(
            model_name=params_inference.model_name,
            embedding_provider=params_inference.embedding_provider,
            chroma_db_dir=PROJECT_ROOT / model_trainer_config.db_path,
            data_path=data_path,
            collection_name=params_inference.collection_name,
            top_k=params_inference.top_k,
            popularity_weight=params_inference.popularity_weight,
        )

        return inference_config

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        """
        Creates the Model Evaluation configuration entity.

        Returns:
            ModelEvaluationConfig: Configuration object for model evaluation and MLflow tracking.
        """
        config = self.config.model_evaluation
        params = self.params

        create_directories([config.root_dir])

        model_evaluation_config = ModelEvaluationConfig(
            root_dir=Path(config.root_dir),
            data_path=Path(config.data_path),
            model_path=Path(config.model_path),
            all_params=params,
            mlflow_uri=get_mlflow_uri(),  # Uses robust logic (Env > Staging > Yaml)
            experiment_name=params.mlflow.experiment_name,
        )

        return model_evaluation_config
