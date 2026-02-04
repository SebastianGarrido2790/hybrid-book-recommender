"""
Main application script for the book recommender system.
This script initializes the recommender engine, defines UI components,
and implements the recommendation logic using Gradio.

Usage:
    uv run python app.py
"""

import os
import gradio as gr
from src.config.configuration import ConfigurationManager
from src.models.hybrid_recommender import HybridRecommender
from src.utils.logger import get_logger
from src.utils.exception import CustomException
import sys

logger = get_logger(__name__)


# --- ENGINE INITIALIZATION ---
def init_recommender():
    """
    Initializes the HybridRecommender engine.

    This function creates a ConfigurationManager to get the inference configuration,
    initializes the HybridRecommender with this configuration, and handles any
    exceptions during initialization.

    Returns:
        HybridRecommender: The initialized recommender engine, or None if initialization fails.
    """
    try:
        config = ConfigurationManager()
        inference_config = config.get_inference_config()
        recommender = HybridRecommender(config=inference_config)
        return recommender
    except Exception as e:
        logger.error(f"Failed to initialize recommender: {CustomException(e, sys)}")
        return None


recommender = init_recommender()

# --- CONSTANTS ---
CATEGORIES = [
    "All",
    "Biography",
    "Fantasy",
    "Fiction",
    "History",
    "Non-Fiction",
    "Science",
    "Thriller",
]
TONES = ["All", "Happy", "Surprising", "Angry", "Suspenseful", "Sad"]
TONE_MAP = {
    "Happy": "joy",
    "Surprising": "surprise",
    "Angry": "anger",
    "Suspenseful": "fear",
    "Sad": "sadness",
}

PLACEHOLDER_IMG_ABS = os.path.abspath("assets/placeholder.png")
PLACEHOLDER_IMG_URL = PLACEHOLDER_IMG_ABS


# --- HELPER FUNCTIONS ---
def get_high_res_image(url):
    if not isinstance(url, str) or not url or url.lower() == "nan":
        return PLACEHOLDER_IMG_URL

    url = url.strip().strip("'").strip('"')
    if url.startswith("http://"):
        url = url.replace("http://", "https://")
    return f"{url}&fife=w800" if "?" in url else f"{url}?fife=w800"


def format_authors(authors_str):
    if not isinstance(authors_str, str) or not authors_str:
        return "Unknown Author"

    clean_str = (
        authors_str.replace("[", "")
        .replace("]", "")
        .replace("'", "")
        .replace('"', "")
        .replace(";", ",")
    )
    authors = [a.strip() for a in clean_str.split(",")]

    if len(authors) == 0:
        return "Unknown Author"
    if len(authors) == 1:
        return authors[0]
    if len(authors) == 2:
        return f"{authors[0]} and {authors[1]}"
    return f"{authors[0]} et al."


# --- UI LOGIC ---
def recommend_books(query, category, tone):
    if not recommender:
        return [], [], "System Error: Recommender not initialized."

    cat_filter = None if category == "All" else category
    tone_filter = TONE_MAP.get(tone) if tone != "All" else None

    if not query.strip() and not cat_filter and not tone_filter:
        return (
            [],
            [],
            "Please enter a search query or select a filter to find recommendations.",
        )

    try:
        results = recommender.recommend(
            query=query, category_filter=cat_filter, tone_filter=tone_filter
        )
    except Exception as e:
        logger.error(f"Recommendation failed: {CustomException(e, sys)}")
        return [], [], "An error occurred while finding recommendations."

    if not results:
        return (
            [],
            [],
            "### ⚠️ No books found matching your criteria.\n\nTry adjusting the filters or using different keywords in your description.",
        )

    results = results[:48]
    gallery_items = []
    full_data = []

    for book in results:
        image_url = get_high_res_image(book.get("thumbnail"))
        title = book.get("title", "Untitled")
        authors = format_authors(book.get("authors"))
        desc = book.get("description", "No description available.")
        rating = book.get("rating", "N/A")
        tone_prob = book.get("tone_prob", 0)

        try:
            mood_score = f"{float(tone_prob):.2f}"
        except Exception:
            mood_score = "N/A"

        # Caption for Gallery Preview
        truncated_desc = (desc[:120] + "...") if len(desc) > 120 else desc
        caption = (
            f"{title} by {authors}\n⭐ {rating} | 🎭 {mood_score}\n{truncated_desc}"
        )

        gallery_items.append((image_url, caption))

        full_data.append(
            {
                "title": title,
                "authors": authors,
                "description": desc,
                "rating": rating,
                "mood_score": mood_score,
                "thumbnail": image_url,
            }
        )

    return gallery_items, full_data, ""


def on_select(evt: gr.SelectData, data):
    if not data or evt.index >= len(data):
        return ""

    book = data[evt.index]

    return f"""
    <div style="background-color: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.1); display: flex; gap: 20px; margin-top: 20px;">
        <img src="{book["thumbnail"]}" style="width: 120px; height: 180px; object-fit: cover; border-radius: 5px;">
        <div style="flex: 1;">
            <h3 style="margin: 0 0 5px 0; font-size: 1.5em; color: white;">{book["title"]}</h3>
            <p style="margin: 0 0 10px 0; color: #ccc;">by {book["authors"]}</p>
            <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                <span style="background: #eab308; color: black; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 0.9em;">⭐ Rating: {book["rating"]}</span>
                <span style="background: #6366f1; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 0.9em;">🎭 Mood: {book["mood_score"]}</span>
            </div>
            <p style="line-height: 1.6; color: #ddd;">{book["description"]}</p>
        </div>
    </div>
    """


# --- UI DEFINITION ---
with gr.Blocks(theme=gr.themes.Glass(), title="Semantic book recommender") as demo:
    gr.Markdown("# Semantic book recommender")
    gr.Markdown(
        "Discover your next favorite read using AI-powered semantic search.",
        elem_classes=["subtitle"],
    )

    # State to store full book data for details view
    results_state = gr.State([])

    with gr.Row():
        user_query = gr.Textbox(
            label="Please enter a description of a book:",
            placeholder="e.g., A story about forgiveness",
        )
        category_dropdown = gr.Dropdown(
            choices=CATEGORIES, label="Select a category:", value="All"
        )
        tone_dropdown = gr.Dropdown(
            choices=TONES, label="Select an emotional tone:", value="All"
        )
        submit_button = gr.Button("Find recommendations", variant="primary")

    gr.Markdown("## Recommendations")
    status_output = gr.Markdown()

    output_gallery = gr.Gallery(
        label="Recommended books",
        columns=8,
        rows=6,
        height="auto",
        allow_preview=True,
        object_fit="contain",
    )

    details_output = gr.HTML(label="Book Details")

    # Event handlers
    submit_button.click(
        fn=recommend_books,
        inputs=[user_query, category_dropdown, tone_dropdown],
        outputs=[output_gallery, results_state, status_output],
    )
    user_query.submit(
        fn=recommend_books,
        inputs=[user_query, category_dropdown, tone_dropdown],
        outputs=[output_gallery, results_state, status_output],
    )

    # When a book in the gallery is selected, update the details area
    output_gallery.select(fn=on_select, inputs=[results_state], outputs=details_output)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        allowed_paths=[os.path.dirname(PLACEHOLDER_IMG_ABS)],
    )
