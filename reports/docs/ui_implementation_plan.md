# Implementation Plan - Phase 4: Gradio UI Development

# Goal Description
Build a modern, interactive web interface using **Gradio** to serve as the "Storefront" for the Hybrid Book Recommender. The UI will allow users to perform natural language searches, filter by category and emotional tone, and view results with a premium, AI-driven aesthetic.

## User Review
> **IMPORTANT**
>
> **Framework Switch**: We are switching from Streamlit to **Gradio** (using the `Blocks` API) to better align with the goal of showcasing ML models.
>
> **Dependency**: This requires adding `gradio` to our `pyproject.toml`.

## Implementation

### Dependencies
[pyproject.toml](hybrid-book-recommender/pyproject.toml)
- Add `gradio>=4.0.0`.

### UI
[app.py](hybrid-book-recommender/app.py)
- **Engine Initialization**: Load `ConfigurationManager` and `HybridRecommender`.
- **Layout (Gradio Blocks)**:
    - **Header**: Project title and description with SVG icon.
    - **Control Panel (Left Sidebar/Column)**:
        - `Dropdown`: Category Filter (Logic: Fetch unique categories from metadata).
        - `Radio/Dropdown`: Mood/Tone Filter (Joy, Fear, Sadness, etc.).
    - **Main Area**:
        - `Textbox`: Search bar (Natural Language Query).
        - `Button`: Search trigger.
        - `Markdown`: Results container (Iterative card display).
- **Styling**: Inject vanilla CSS into `gr.Blocks(css=...)` to achieve a dark-mode, glassmorphism aesthetic.

## Verification

### Automated Tests
- No automated tests for the UI, but we will verify the console logs for engine initialization.

### Manual Verification
1.  **Framework Check**: Run `uv run python app.py` and verify the local server starts.
2.  **Filter Logic**: Select "Non-Fiction" and "Joy" and search for "happy facts". Verify results adhere to both filters.
3.  **Semantic Search**: Query for "A book about space but with a dark vibe". Verify the engine returns relevant books with "Fear" or "Sadness" tones.
4.  **Responsive Check**: Verify the UI layout holds on narrow (mobile-sized) windows.
