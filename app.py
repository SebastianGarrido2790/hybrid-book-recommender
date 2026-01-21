import gradio as gr
from src.config.configuration import ConfigurationManager
from src.models.hybrid_recommender import HybridRecommender
from src.utils.logger import get_logger

logger = get_logger(__name__)


# --- ENGINE INITIALIZATION ---
try:
    config_manager = ConfigurationManager()
    recommender = HybridRecommender(config=config_manager.get_inference_config())
except Exception as e:
    logger.error(f"Failed to initialize recommender: {e}")
    recommender = None

# Constants
PLACEHOLDER_IMG = "https://via.placeholder.com/140x210.png?text=No+Cover"
TONE_MAP = {
    "Happy": "joy",
    "Sad": "sadness",
    "Angry": "anger",
    "Scary": "fear",
    "Surprising": "surprise",
    "Disgusting": "disgust",
    "Neutral": "neutral",
}


# --- HELPER FUNCTIONS ---
def get_high_res_image(url):
    if not url or not isinstance(url, str):
        return PLACEHOLDER_IMG
    if "http://" in url:
        url = url.replace("http://", "https://")
    if "&zoom=" in url:
        import re

        url = re.sub(r"&zoom=\d+", "&zoom=3", url)
    if "fife=w" not in url:
        url += "&fife=w800"
    return url


def format_authors(authors):
    if not authors:
        return "Unknown Author"
    if isinstance(authors, list):
        return ", ".join(authors)
    return str(authors)


def search_books(query, category, tone):
    if not recommender:
        return [
            [(PLACEHOLDER_IMG, "Error: Recommender not initialized")],
            [],
            "Recommender engine is not ready.",
        ]

    cat_filter = None if category == "All" else category
    tone_filter = TONE_MAP.get(tone) if tone != "All" else None

    if not query.strip() and not cat_filter and not tone_filter:
        return [[], [], ""]

    try:
        results = recommender.recommend(
            query=query, category_filter=cat_filter, tone_filter=tone_filter
        )
    except Exception as e:
        logger.error(f"Recommendation failed: {e}")
        return [[], [], ""]

    gallery_items = []
    full_data = []

    if not results:
        return [[], [], "No books found matches your search."]

    for book in results:
        image_url = get_high_res_image(book.get("thumbnail"))
        title = book.get("title", "Untitled")
        authors = format_authors(book.get("authors"))
        desc = book.get("description", "No description available.")
        rating = book.get("rating", "N/A")
        tone_prob = book.get("tone_prob", 0.0)

        # Simplified caption for gallery view
        caption = f"{title} by {authors}"
        gallery_items.append((image_url, caption))

        full_data.append(
            {
                "title": title,
                "authors": authors,
                "description": desc,
                "rating": rating,
                "tone_prob": tone_prob,
                "thumbnail": image_url,
            }
        )

    return [gallery_items, full_data, f"Found {len(results)} books."]


def on_select(evt: gr.SelectData, full_data):
    if not full_data or evt.index >= len(full_data):
        return ""

    book = full_data[evt.index]

    # Display probability if it's significant
    prob_html = ""
    try:
        tprob = float(book.get("tone_prob", 0))
        if tprob > 0:
            prob_html = f"<span style='background: #eef2ff; color: #4338ca; padding: 4px 10px; border-radius: 999px; font-size: 0.9rem; margin-left: 8px;'>✨ Mood Score: {tprob:.2f}</span>"
    except (ValueError, TypeError):
        pass

    html_template = f"""
    <div style='background: #ffffff; padding: 30px; border-radius: 12px; border: 1px solid #e5e7eb; margin-top: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); display: flex; gap: 20px; align-items: flex-start;'>
        <img src="{book["thumbnail"]}" style="width: 140px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" onerror="this.src='{PLACEHOLDER_IMG}'">
        <div style="flex: 1;">
            <h3 style='margin: 0; color: #111827; font-size: 1.5rem; font-weight: 700;'>{book["title"]}</h3>
            <p style='color: #4b5563; font-size: 1.1rem; margin-bottom: 15px;'>by {book["authors"]}</p>
            <div style='margin-bottom: 15px;'>
                <span style='background: #f3f4f6; color: #374151; padding: 4px 10px; border-radius: 999px; font-size: 0.9rem;'>⭐ Rating: {book["rating"]}</span>
                {prob_html}
            </div>
            <p style='color: #374151; line-height: 1.6; font-size: 1rem;'>{book["description"]}</p>
        </div>
    </div>
    """
    return html_template


# --- STYLING ---
theme = gr.themes.Default(
    primary_hue="blue",
).set(
    body_background_fill="#ffffff",
    block_background_fill="#ffffff",
    block_border_width="1px",
    block_title_text_weight="600",
)

CUSTOM_CSS = """
.container { max-width: 1200px; margin: auto; padding-top: 20px; }
.input-row { 
    background: #f9fafb; 
    padding: 20px; 
    border-radius: 12px; 
    border: 1px solid #e5e7eb;
    margin-bottom: 20px;
}
.gallery-container { border: none !important; background: transparent !important; }
.gr-button-primary { 
    background: #2563eb !important; 
    border: none !important;
    transition: all 0.2s ease;
}
.gr-button-primary:hover { background: #1d4ed8 !important; transform: translateY(-1px); }
"""

with gr.Blocks(theme=theme, css=CUSTOM_CSS, title="Hybrid Book Recommender") as demo:
    # State to store full book data for details view
    full_data_state = gr.State([])

    with gr.Column(elem_classes=["container"]):
        gr.Markdown(
            """
            <div style='text-align: center; margin-bottom: 30px;'>
                <h1 style='font-size: 2.5rem; color: #111827; margin-bottom: 10px;'>📚 Hybrid Book Recommender</h1>
                <p style='font-size: 1.1rem; color: #6b7280;'>Semantic Search meets Collaborative Intelligence</p>
            </div>
            """
        )

        with gr.Row(elem_classes=["input-row"]):
            with gr.Column(scale=4):
                query_input = gr.Textbox(
                    label="Search by description",
                    placeholder="e.g. A gripping mystery set in Victorian London...",
                    show_label=False,
                )
            with gr.Column(scale=2):
                category_dropdown = gr.Dropdown(
                    choices=[
                        "All",
                        "Fiction",
                        "Nonfiction",
                        "Juvenile Fiction",
                        "History",
                        "Science",
                    ],
                    value="All",
                    label="Category",
                    show_label=False,
                )
            with gr.Column(scale=2):
                tone_dropdown = gr.Dropdown(
                    choices=[
                        "All",
                        "Happy",
                        "Sad",
                        "Angry",
                        "Scary",
                        "Surprising",
                        "Disgusting",
                        "Neutral",
                    ],
                    value="All",
                    label="Mood",
                    show_label=False,
                )
            with gr.Column(scale=1):
                search_button = gr.Button("Find recommendations", variant="primary")

        status_output = gr.Markdown("", visible=True)

        book_gallery = gr.Gallery(
            label="Recommendations",
            show_label=False,
            columns=8,
            rows=1,
            height="auto",
            object_fit="contain",
            elem_classes=["gallery-container"],
        )

        detail_output = gr.HTML("")

        # Event Handlers
        search_button.click(
            fn=search_books,
            inputs=[query_input, category_dropdown, tone_dropdown],
            outputs=[book_gallery, full_data_state, status_output],
        )

        query_input.submit(
            fn=search_books,
            inputs=[query_input, category_dropdown, tone_dropdown],
            outputs=[book_gallery, full_data_state, status_output],
        )

        book_gallery.select(
            fn=on_select,
            inputs=[full_data_state],
            outputs=[detail_output],
        )

if __name__ == "__main__":
    demo.launch()
