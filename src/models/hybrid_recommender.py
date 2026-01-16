"""
This module implements a hybrid recommendation system that combines semantic search with collaborative filtering.
It uses a vector database (ChromaDB) for semantic search and a collaborative filtering proxy (ratings) to boost books with higher average ratings.
"""

import pandas as pd
from typing import List, Dict, Any
from langchain_chroma import Chroma
from src.models.llm_utils import EmbeddingFactory
from src.entity.config_entity import InferenceConfig
from src.utils.logger import get_logger
from src.utils.paths import PROJECT_ROOT

logger = get_logger(__name__)


class HybridRecommender:
    """
    The 'Brain' of the recommendation system.

    It combines:
    1. Semantic Search (ChromaDB): Finds books with similar content/topics.
    2. Collaborative Filtering Proxy (Ratings): Boosts books with higher average ratings.
    """

    def __init__(self, config: InferenceConfig):
        """
        Initializes the HybridRecommender components.

        Args:
            config (InferenceConfig): The inference configuration entity.
        """
        self.config = config

        self.embedding_fn = EmbeddingFactory.get_embedding_function(
            provider=self.config.embedding_provider, model_name=self.config.model_name
        )

        self.vector_store = Chroma(
            persist_directory=str(self.config.chroma_db_dir),
            embedding_function=self.embedding_fn,
            collection_name=self.config.collection_name,
        )

        # We read 'clean_books.csv' specifically to get ALL ratings, not just the training set.
        # This fixes the issue where a book might be in the vector DB but missing from a 'train.csv' split.
        self.books_metadata = pd.read_csv(self.config.data_path)
        self.books_metadata.set_index("isbn13", inplace=True)

        logger.info(
            f"Hybrid Recommender initialized. DB: {self.config.chroma_db_dir.relative_to(PROJECT_ROOT)}"
        )

    def recommend(
        self, query: str, category_filter: str = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves and ranks book recommendations based on a hybrid score.

        Args:
            query (str): The natural language search query (e.g., "Space opera with aliens").
            category_filter (str, optional): A category to filter results by (e.g., "Non-Fiction").

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing book metadata
                                  and the calculated 'score'.
        """
        top_k = self.config.top_k
        popularity_weight = self.config.popularity_weight

        logger.info(f"Processing query: '{query}' (Filter: {category_filter})")

        # 1. Semantic Search (Fetch more to allow for filtering)
        # If we have a filter, we fetch even more to ensure we have enough results after filtering.
        fetch_k = top_k * 5 if category_filter else top_k * 3
        results = self.vector_store.similarity_search_with_score(query, k=fetch_k)

        recommendations = []

        for doc, score in results:
            try:
                # --- ISBN CASTING ---
                isbn_str = doc.metadata.get("isbn", "0")
                isbn_clean = "".join(filter(str.isdigit, str(isbn_str)))
                isbn = int(isbn_clean) if isbn_clean else 0

                # Check if we have rating data for this book
                if isbn in self.books_metadata.index:
                    book_row = self.books_metadata.loc[isbn]
                    if isinstance(book_row, pd.DataFrame):
                        book_row = book_row.iloc[0]

                    # --- CATEGORICAL FILTERING ---
                    # Use 'simple_category' if available, else fallback to 'categories'
                    category = book_row.get("simple_category")
                    if category is None:
                        category = book_row.get("categories", "Uncategorized")

                    if (
                        category_filter
                        and category_filter.lower() != str(category).lower()
                    ):
                        continue

                    rating = float(book_row.get("average_rating", 0))
                    ratings_count = int(book_row.get("ratings_count", 0))

                    # 2. Hybrid Scoring
                    similarity_score = 1 - score
                    hybrid_score = similarity_score + (
                        (rating / 5.0) * popularity_weight
                    )

                    recommendations.append(
                        {
                            "isbn": isbn,
                            "title": doc.metadata.get("title"),
                            "authors": doc.metadata.get("authors"),
                            "description": doc.metadata.get("description"),
                            "category": category,
                            "rating": rating,
                            "ratings_count": ratings_count,
                            "score": hybrid_score,
                            "match_reason": "Hybrid Match",
                        }
                    )
            except Exception as e:
                logger.warning(f"Skipping book due to error: {e}")
                continue

        # 3. Sort by Hybrid Score
        recommendations = sorted(
            recommendations, key=lambda x: x["score"], reverse=True
        )
        return recommendations[:top_k]
