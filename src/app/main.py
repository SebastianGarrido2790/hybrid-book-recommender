"""
Core Gradio UI definition and interaction logic for the book recommender application.
"""

import os
import sys
from typing import Any

import gradio as gr

from src.app.data_loaders import (
    PLACEHOLDER_IMG_ABS,
    format_authors,
    get_app_config,
    get_high_res_image,
    init_recommender,
)
from src.app.styles import get_book_details_html
from src.utils.exception import CustomException
from src.utils.logger import get_logger

logger = get_logger(__name__)

# --- State Initialization ---
recommender = init_recommender()
CATEGORIES, TONES, TONE_MAP, MAX_RESULTS = get_app_config()


def recommend_books(
    query: str, category: str, tone: str
) -> tuple[list[tuple[str, str]], list[dict[str, Any]], str]:
    """
    Handles recommendation requests from the UI.
    """
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
            "### ⚠️ No books found matching your criteria.\n\n"
            "Try adjusting the filters or using different keywords in your description.",
        )

    results = results[:MAX_RESULTS]
    gallery_items = []
    full_data = []

    for book in results:
        image_url = get_high_res_image(book.thumbnail)
        title = book.title
        authors = format_authors(book.authors)
        desc = book.description if book.description else "No description available."
        rating = book.rating
        tone_prob = book.tone_prob

        try:
            mood_score = f"{float(tone_prob):.2f}"
        except Exception:
            mood_score = "N/A"

        # Caption for Gallery Preview
        truncated_desc = (desc[:120] + "...") if len(desc) > 120 else desc
        caption = f"{title} by {authors}\n⭐ {rating} | 🎭 {mood_score}\n{truncated_desc}"

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


def on_select(evt: gr.SelectData, data: list[dict[str, Any]]) -> str:
    """
    Callback for when a book is selected in the gallery.
    """
    if not data or evt.index >= len(data):
        return ""

    book = data[evt.index]
    return get_book_details_html(book)


def create_ui():
    """
    Constructs the Gradio interface.
    """
    with gr.Blocks(title="Semantic book recommender") as demo:
        gr.Markdown("# Semantic book recommender")
        gr.Markdown(
            "Discover your next favorite read using AI-powered semantic search.",
            elem_classes=["subtitle"],
        )

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

        output_gallery.select(fn=on_select, inputs=[results_state], outputs=details_output)

    return demo


def main():
    """
    Entry point for the Gradio application.
    """
    demo = create_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        theme=gr.themes.Glass(),  # type: ignore[reportPrivateImportUsage]
        inbrowser=True,
        allowed_paths=[os.path.dirname(PLACEHOLDER_IMG_ABS)],
    )


if __name__ == "__main__":
    main()
