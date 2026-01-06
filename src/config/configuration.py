"""
This module serves as the 'Brain' of the system, responsible for coordinating
configurations and parameters across the pipeline.
"""

import dvc.api
from box import ConfigBox
from src.constants import *
from src.utils.common import read_yaml, create_directories
from src.entity.config_entity import DataIngestionConfig, DataTransformationConfig
from src.utils.paths import CONFIG_FILE_PATH, PARAMS_FILE_PATH


class ConfigurationManager:
    """
    Manages project configurations and parameters.

    This class centralizes the loading of 'config.yaml' and 'params.yaml' (via DVC API),
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

    def get_data_transformation_config(self) -> DataTransformationConfig:
        """
        Creates the Data Transformation configuration entity.

        Fetches processing parameters (test_size, random_state, etc.) from
        params.yaml via the DVC API to ensure experiment reproducibility.

        Returns:
            DataTransformationConfig: Configuration for the data transformation component.
        """
        config = self.config.data_transformation
        params = self.params.data_transformation  # Reads from params.yaml

        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            test_size=params.test_size,
            val_size=params.val_size,
            random_state=params.random_state,
            min_desc_len=params.min_desc_len,
        )

        return data_transformation_config
