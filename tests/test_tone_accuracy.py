"""
Module for testing and validating the accuracy of the Tone Classifier.
Provides functionality for manual verification (Vibe Check) and statistical visualization
of the global tone distribution across the dataset.

Usage Instructions:
    1. Run all tests:
       uv run pytest src/tests

    2. Run tests with verbose output (recommended):
       uv run pytest src/tests -vv

    3. Run a specific test module:
       uv run pytest src/tests/test_tone_accuracy.py

    4. Run specific tests by keyword matching:
       uv run pytest -k "tone"
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from src.utils.logger import get_logger
from src.utils.exception import CustomException

STAGE_NAME = "Tone Accuracy Test"
logger = get_logger(headline=STAGE_NAME)


def test_tone_accuracy() -> None:
    """
    Evaluates the accuracy of the Tone Classifier by performing a 'Vibe Check'
    on a random sample of enriched books and generating a distribution plot.

    Flow:
    1. Loads toned data.
    2. Prints a random sample of book titles, tones, and descriptions for manual verification.
    3. Generates and saves a bar chart of the global tone distribution.

    Raises:
        CustomException: If test fails.
    """
    try:
        data_path = "artifacts/tone_analysis/toned_books.csv"

        # Verify file exists
        if not os.path.exists(data_path):
            logger.error(
                f"Toned data not found at {data_path}. Run tone analysis first."
            )
            return

        df = pd.read_csv(data_path)
        logger.info(f"Loaded {len(df)} books with tone analysis.")

        # Sample random books for manual "Vibe Check"
        sample_size = min(len(df), 20)
        sample = df.sample(n=sample_size)

        print("\n" + "=" * 80)
        print("TONE ANALYSIS VIBE CHECK (Random Sample)")
        print("=" * 80)
        print(f"{'TITLE':<40} | {'TONE':<10} | {'DESCRIPTION SNIPPET'}")
        print("-" * 80)

        for _, row in sample.iterrows():
            title = (
                row["title"][:37] + "..." if len(row["title"]) > 37 else row["title"]
            )
            tone = str(row["dominant_tone"]).upper()
            desc = str(row["description"])[:60].replace("\n", " ") + "..."

            print(f"{title:<40} | {tone:<10} | {desc}")

        print("=" * 80)
        logger.info("Tone 'Vibe Check' completed.")

        # 2. Global Tone Distribution Stats
        print("\nGlobal Tone Distribution:")
        counts = df["dominant_tone"].value_counts()
        print(counts)

        # 3. Visualization
        logger.info("Generating tone distribution plot...")
        plt.figure(figsize=(10, 6))
        sns.set_style("whitegrid")

        # Define a consistent color palette for emotions
        emotion_colors = {
            "joy": "#FFD700",  # Gold
            "sadness": "#4682B4",  # SteelBlue
            "fear": "#4B0082",  # Indigo
            "anger": "#B22222",  # FireBrick
            "surprise": "#FF8C00",  # DarkOrange
            "neutral": "#A9A9A9",  # DarkGray
            "disgust": "#556B2F",  # DarkOliveGreen
        }

        sns.barplot(x=counts.index, y=counts.values, palette=emotion_colors)
        plt.title("Distribution of Emotional Tones in Book Collection", fontsize=15)
        plt.xlabel("Emotional Tone", fontsize=12)
        plt.ylabel("Number of Books", fontsize=12)

        # Save plot
        figures_dir = "reports/figures"
        os.makedirs(figures_dir, exist_ok=True)
        plot_path = os.path.join(figures_dir, "tone_distribution.png")
        plt.savefig(plot_path)
        logger.info(f"Tone distribution plot saved to {plot_path}")

    except Exception as e:
        raise CustomException(e, sys)


if __name__ == "__main__":
    try:
        test_tone_accuracy()
    except Exception as e:
        raise CustomException(e, sys)
