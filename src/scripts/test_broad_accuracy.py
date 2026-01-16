import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import os
from src.utils.logger import get_logger

logger = get_logger(__name__, headline="BroadAccuracyTest")


def test_broad_accuracy():
    """
    Evaluates accuracy using broad masks (Fiction vs Non-Fiction).
    """
    try:
        df = pd.read_csv("artifacts/data_enrichment/enriched_books.csv")

        # 1. Map Ground Truth to Broad classes
        # Categories starting with 'Juvenile Fiction' or just 'Fiction'
        def get_broad_gt(cat):
            cat = str(cat)
            if "Fiction" in cat or "Novel" in cat or "Literary Criticism" in cat:
                return "Broad_Fiction"
            return "Broad_NonFiction"

        # 2. Map Predictions to Broad classes
        def get_broad_pred(label):
            fiction_labels = ["Fiction", "Fantasy", "Thriller"]
            if label in fiction_labels:
                return "Broad_Fiction"
            return "Broad_NonFiction"

        # Filter for rows that have SOME category label
        df = df.dropna(subset=["categories"])

        y_true = df["categories"].apply(get_broad_gt)
        y_pred = df["simple_category"].apply(get_broad_pred)

        report = classification_report(y_true, y_pred)

        print("\n" + "=" * 60)
        print("BROAD (FICTION VS NON-FICTION) ACCURACY REPORT")
        print("=" * 60)
        print(report)
        print("=" * 60)

        # 3. Output Confusion Matrix
        labels = ["Broad_Fiction", "Broad_NonFiction"]
        cm = confusion_matrix(y_true, y_pred, labels=labels)

        plt.figure(figsize=(8, 6))
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            xticklabels=labels,
            yticklabels=labels,
            cmap="Greens",
        )
        plt.xlabel("Predicted (Zero-Shot Grouped)")
        plt.ylabel("True (Original Grouped)")
        plt.title("Enrichment Accuracy: Broad Confusion Matrix")

        figures_dir = "reports/figures"
        os.makedirs(figures_dir, exist_ok=True)
        plot_path = os.path.join(figures_dir, "enrichment_broad_cm.png")
        plt.savefig(plot_path)
        logger.info(f"Broad confusion matrix saved to {plot_path}")

    except Exception as e:
        logger.error(f"Broad test failed: {e}")


if __name__ == "__main__":
    test_broad_accuracy()
