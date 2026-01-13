"""
This module defines the configuration entities for the pipeline stages.
It includes the root directory, data path, and tokenizer name.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    """
    Configuration for the Data Ingestion stage.

    Attributes:
        root_dir (Path): Root directory for data ingestion artifacts.
        source_URL (str): URL to download the source data from.
        local_data_file (Path): Path where the downloaded zip file will be saved.
        unzip_dir (Path): Directory where the zip file will be extracted.
    """

    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path


@dataclass(frozen=True)
class DataValidationConfig:
    """
    Configuration for the Data Validation stage.

    Attributes:
        root_dir (Path): Root directory for data validation artifacts.
        unzip_data_dir (Path): Path to the extracted data file from ingestion.
        STATUS_FILE (Path): Path to the validation status file.
        cleaned_data_file (Path): Path where the cleaned dataset will be saved.
        min_desc_len (int): Minimum length of book description to retain.
        categories_min_len (int): Minimum length of categories string to retain.
    """

    root_dir: Path
    unzip_data_dir: Path
    STATUS_FILE: Path
    cleaned_data_file: Path
    min_desc_len: int
    categories_min_len: int


@dataclass(frozen=True)
class DataTransformationConfig:
    """
    Configuration for the Data Transformation stage.

    Attributes:
        root_dir (Path): Root directory for data transformation artifacts.
        data_path (Path): Path to the cleaned data file.
        test_size (float): Proportion of the dataset to include in the test split.
        val_size (float): Proportion of the remaining dataset to include in the validation split.
        random_state (int): Random seed for reproducibility.
        tokenizer_name (str, optional): Name of the tokenizer to use (if applicable).
    """

    root_dir: Path
    data_path: Path
    test_size: float
    val_size: float
    random_state: int
    tokenizer_name: str = None  # Optional: for adding tokenization later


@dataclass(frozen=True)
class ModelTrainerConfig:
    """
    Configuration for the Model Training (Vector DB) stage.

    Attributes:
        root_dir (Path): Root directory for model artifacts.
        data_path (Path): Path to the training data.
        db_path (Path): Path where the ChromaDB will be persisted.
        model_name (str): Name of the sentence-transformer model.
        collection_name (str): Name of the ChromaDB collection.
        embedding_provider (str): Provider of the embedding model (huggingface or gemini).
        batch_size (int): Number of documents to process in each batch.
    """

    root_dir: Path
    data_path: Path
    db_path: Path
    model_name: str
    collection_name: str
    embedding_provider: str
    batch_size: int


@dataclass(frozen=True)
class InferenceConfig:
    """
    Configuration for the Inference Stage (Hybrid Recommender).

    Attributes:
        model_name (str): Name of the sentence-transformer model.
        embedding_provider (str): Provider of the embedding model (huggingface or gemini).
        chroma_db_dir (Path): Path to the ChromaDB directory.
        data_path (Path): Path to the data file.
        collection_name (str): Name of the ChromaDB collection.
        top_k (int): Number of top recommendations to return.
        popularity_weight (float): Weight for the rating boost in hybrid score.
    """

    model_name: str
    embedding_provider: str
    chroma_db_dir: Path
    data_path: Path
    collection_name: str
    top_k: int
    popularity_weight: float
