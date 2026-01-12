"""
This module serves as the 'Brain' of the system, responsible for coordinating
configurations and parameters across the pipeline.
"""

import dvc.api
from box import ConfigBox
from src.constants import *
from src.utils.common import read_yaml, create_directories
from src.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
)
from src.utils.paths import CONFIG_FILE_PATH, PARAMS_FILE_PATH


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
        self.config = read_yaml(config_filepath)
        self.params = ConfigBox(dvc.api.params_show())
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
