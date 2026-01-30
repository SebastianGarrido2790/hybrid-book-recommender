"""
Unit tests for the HybridRecommender class using pytest.

This module validates the core recommendation logic, ensuring that:
1. Hybrid scoring math is correct (combining semantic distance and popularity).
2. Filtering mechanisms (Categories) work efficiently.
3. External dependencies (ChromaDB, Google/HuggingFace APIs) are mocked to ensure
   tests are fast, deterministic, and runnable in CI/CD environments without API keys.
"""

import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from src.entity.config_entity import InferenceConfig
from src.models.hybrid_recommender import HybridRecommender
from src.utils.paths import PROJECT_ROOT


# --- Fixtures ---


@pytest.fixture
def mock_config():
    """Provides a mock configuration object."""
    return InferenceConfig(
        model_name="test-model",
        embedding_provider="huggingface",
        chroma_db_dir=PROJECT_ROOT / "test_db_dir",
        data_path=PROJECT_ROOT / "test_data.csv",
        collection_name="test_collection",
        top_k=2,
        popularity_weight=0.5,
    )


@pytest.fixture
def mock_books_data():
    """Provides a sample pandas DataFrame mimicking the books metadata."""
    return pd.DataFrame(
        {
            "isbn13": [1234567890123, 9876543210987, 1111111111111],
            "title": ["Book One", "Book Two", "Book Three"],
            "authors": ["Author A", "Author B", "Author C"],
            "average_rating": [4.5, 3.0, 5.0],
            "ratings_count": [100, 50, 10],
            "categories": ["Fiction", "Non-Fiction", "Sci-Fi"],
            "simple_category": ["Fiction", "Non-Fiction", "Fiction"],
            "dominant_tone": ["joy", "sadness", "suspense"],
            "joy": [0.8, 0.1, 0.1],
            "thumbnail": ["http://img1.jpg", "http://img2.jpg", "http://img3.jpg"],
        }
    )


@pytest.fixture
def mock_dependencies(mock_books_data):
    """
    Patches external dependencies (Chroma, EmbeddingFactory, pd.read_csv).
    Returns the set of mock objects for assertion.
    """
    with (
        patch("src.models.hybrid_recommender.pd.read_csv") as mock_read_csv,
        patch("src.models.hybrid_recommender.Chroma") as mock_chroma,
        patch(
            "src.models.hybrid_recommender.EmbeddingFactory"
        ) as mock_embedding_factory,
    ):
        # Setup specific return values
        mock_read_csv.return_value = mock_books_data
        mock_embedding_factory.get_embedding_function.return_value = MagicMock()

        # Setup Chroma vector store mock
        mock_vector_store = MagicMock()
        mock_chroma.return_value = mock_vector_store

        yield {
            "read_csv": mock_read_csv,
            "chroma": mock_chroma,
            "embedding_factory": mock_embedding_factory,
            "vector_store": mock_vector_store,
        }


# --- Tests ---


def test_recommend_flow(mock_config, mock_dependencies):
    """Verifies that the recommend method returns correctly calculated hybrid scores."""

    # 1. Setup Mock Vector Search Results
    mock_vector_store = mock_dependencies["vector_store"]

    # Mock Document objects returned by Chroma
    mock_doc1 = MagicMock()
    mock_doc1.metadata = {
        "isbn": "1234567890123",
        "title": "Book One",
        "authors": "Author A",
        "description": "A great fiction book.",
    }

    mock_doc2 = MagicMock()
    mock_doc2.metadata = {
        "isbn": "9876543210987",
        "title": "Book Two",
        "authors": "Author B",
        "description": "A sad non-fiction book.",
    }

    # Simulate finding 2 results with specific similarity distances
    # Distance: 0.1 (Close match), 0.4 (Further match)
    mock_vector_store.similarity_search_with_score.return_value = [
        (mock_doc1, 0.1),
        (mock_doc2, 0.4),
    ]

    # 2. Initialize Recommender
    recommender = HybridRecommender(mock_config)

    # 3. Execution
    recommendations = recommender.recommend("some query")

    # 4. Assertions
    assert len(recommendations) == 2, "Should return exactly 2 recommendations"

    first_rec = recommendations[0]

    # Structure checks
    assert "isbn" in first_rec
    assert "score" in first_rec
    assert first_rec["isbn"] == 1234567890123
    assert first_rec["title"] == "Book One"

    # Score Logic Verification
    # Formula: (1 - distance) + (rating/5.0 * weight)
    # Expected: (1 - 0.1) + (4.5/5.0 * 0.5) = 0.9 + 0.45 = 1.35
    expected_score = (1 - 0.1) + (4.5 / 5.0) * 0.5

    # Use pytest.approx for floating point comparisons
    assert first_rec["score"] == pytest.approx(expected_score, abs=0.01)


def test_recommend_with_filter(mock_config, mock_dependencies):
    """Verifies that category filtering correctly excludes mismatched items."""

    mock_vector_store = mock_dependencies["vector_store"]

    # Mock Docs
    mock_doc1 = MagicMock()
    mock_doc1.metadata = {
        "isbn": "1234567890123",
        "title": "Book One",
    }  # Found in metadata as 'Fiction'

    mock_doc2 = MagicMock()
    mock_doc2.metadata = {
        "isbn": "9876543210987",
        "title": "Book Two",
    }  # Found in metadata as 'Non-Fiction'

    mock_vector_store.similarity_search_with_score.return_value = [
        (mock_doc1, 0.1),
        (mock_doc2, 0.4),
    ]

    recommender = HybridRecommender(mock_config)

    # Apply Filter: 'Non-Fiction'
    # Should exclude Book One (Fiction) but keep Book Two (Non-Fiction)
    recommendations = recommender.recommend("query", category_filter="Non-Fiction")

    assert len(recommendations) == 1
    assert recommendations[0]["isbn"] == 9876543210987
    assert recommendations[0]["category"] == "Non-Fiction"
