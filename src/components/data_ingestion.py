"""
This module serves as the 'Worker' for the Data Ingestion Stage of the pipeline.
It handles the data ingestion process from a remote source.
"""

import os
import urllib.request as request
import zipfile
from src.utils.logger import get_logger
from src.entity.config_entity import DataIngestionConfig

logger = get_logger(__name__)


class DataIngestion:
    """
    This class is responsible for downloading the dataset from a specified URL
    and extracting it to a local directory for further processing.
    """

    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        """
        Downloads the file from the source URL.

        Checks if the file already exists locally. If not, it downloads the file
        and logs the process.
        """
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url=self.config.source_URL, filename=self.config.local_data_file
            )
            logger.info(f"{filename} downloaded! Info: \n{headers}")
        else:
            logger.info(
                f"File already exists of size: {os.path.getsize(self.config.local_data_file)}"
            )

    def extract_zip_file(self):
        """
        Extracts the zip file into the configured data directory.

        Creates the extraction directory if it doesn't exist and unzips
        the downloaded file into it.
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, "r") as zip_ref:
            zip_ref.extractall(unzip_path)
            logger.info(f"Extracted zip file to {unzip_path}")
