import pandas as pd
from tqdm import tqdm
from transformers import pipeline
import torch
import re
from src.entity.config_entity import ToneAnalysisConfig
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ToneAnalysis:
    """
    Enhanced Component for Metadata Enrichment using Sentence-Level Tone Analysis.
    Captures nuance by splitting descriptions into sentences and aggregating emotional scores.
    """

    def __init__(self, config: ToneAnalysisConfig):
        self.config = config

    def _split_into_sentences(self, text: str):
        """
        Splits text into sentences using a robust regex.
        """
        if not isinstance(text, str) or not text.strip():
            return []
        # Regex to split on . ! ? followed by space and capital letter or end of string
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s.strip() for s in sentences if len(s.strip()) > 5]

    def initiate_tone_analysis(self):
        """
        Executes the sentence-level tone analysis process.
        """
        try:
            logger.info(f"Loading data from {self.config.data_path}")
            df = pd.read_csv(self.config.data_path)

            logger.info(f"Initializing Emotion Classifier: {self.config.model_name}")

            # Device selection
            device = 0 if torch.cuda.is_available() else -1
            if device == 0:
                logger.info("GPU detected, using GPU for classification.")
            else:
                logger.info("No GPU detected, using CPU. This might be slow.")

            # Pipeline with top_k=None to get all 7 emotion scores
            classifier = pipeline(
                "text-classification",
                model=self.config.model_name,
                device=device,
                top_k=None,
            )

            book_dominant_tones = []

            logger.info("Processing books using Sentence-Level Analysis...")

            # We process book-by-book to handle sentence-to-book mapping easily
            # Optimizing for accuracy and nuance as requested by the user.
            for idx, row in tqdm(
                df.iterrows(), total=len(df), desc="Analyzing Books (Sentence-Level)"
            ):
                description = str(row.get("description", ""))
                sentences = self._split_into_sentences(description)

                if not sentences:
                    book_dominant_tones.append("neutral")
                    continue

                # Classify all sentences in the description at once
                try:
                    # Limit to first 20 sentences to avoid explosion on extremely long texts
                    sentences = sentences[:20]
                    results = classifier(sentences)
                except Exception as e:
                    logger.warning(
                        f"Error classifying sentences for book '{row.get('title')}': {e}. Falling back to neutral."
                    )
                    book_dominant_tones.append("neutral")
                    continue

                # Aggregate probabilities for each emotion across all sentences
                emotion_sums = {emotion: 0.0 for emotion in self.config.target_emotions}
                num_sentences = len(results)

                for sentence_result in results:
                    for emotion_score in sentence_result:
                        label = emotion_score["label"]
                        score = emotion_score["score"]
                        if label in emotion_sums:
                            emotion_sums[label] += score

                # Calculate average probability
                emotion_averages = {
                    label: score / num_sentences
                    for label, score in emotion_sums.items()
                }

                # Selection Strategy: Determine the "representative vibe"
                # Find the top non-neutral emotion
                non_neutral_averages = {
                    label: score
                    for label, score in emotion_averages.items()
                    if label != "neutral"
                }
                top_non_neutral = max(
                    non_neutral_averages, key=non_neutral_averages.get
                )
                top_non_neutral_score = non_neutral_averages[top_non_neutral]

                # If the top non-neutral emotion is significant (> 0.15 average), we pick it
                # Even if neutral as a whole is higher, because neutral sentences are common noise.
                if top_non_neutral_score > 0.15:
                    book_dominant_tones.append(top_non_neutral)
                else:
                    # If everything else is very weak, it's truly a neutral book
                    book_dominant_tones.append("neutral")

            df["dominant_tone"] = book_dominant_tones

            logger.info(f"Saving refined toned data to {self.config.output_path}")
            df.to_csv(self.config.output_path, index=False)

            logger.info("✅ Sentence-level tone analysis completed successfully.")

        except Exception as e:
            logger.error(f"Error during tone analysis: {e}")
            raise e
