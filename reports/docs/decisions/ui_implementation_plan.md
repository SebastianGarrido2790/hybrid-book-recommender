# Implementation Plan - Phase 4: Gradio UI Development

# Goal Description
Build a modern, interactive web interface using **Gradio** to serve as the "Storefront" for the Hybrid Book Recommender. The UI will allow users to perform natural language searches, filter by category and emotional tone, and view results with a premium, AI-driven aesthetic.

## User Review
> [!IMPORTANT]
>
> **Framework Switch**: We are switching from Streamlit to **Gradio** (using the `Blocks` API) to better align with the goal of showcasing ML models.
>
> **Dependency**: This requires adding `gradio` to our `pyproject.toml`.

## Implementation

### Dependencies
[pyproject.toml](hybrid-book-recommender/pyproject.toml)
- Add `gradio>=4.0.0`.

### UI Architecture (`src/app/`)
The application is modularized to ensure separation of concerns:
- **`main.py`**: Orchestrates the Gradio `Blocks` lifecycle and event handlers.
- **`styles.py`**: Concentrates all CSS-in-Python and HTML templates for the glassmorphism UI.
- **`data_loaders.py`**: Handles engine initialization and data formatting helpers.

#### Layout (Gradio Blocks)
- **Header**: Project title and description with SVG icon.
- **Control Panel**:
    - `Dropdown`: Category Filter (Logic: Load from `params.yaml`).
    - `Dropdown`: Emotional Tone Filter (Joy, Fear, Sadness, etc.).
- **Main Area**:
    - `Textbox`: Search bar (Natural Language Query).
    - `Gallery`: Result preview with hover captions.
    - `HTML`: Interactive details view triggered by selection.

### Styling
Leverages `gr.themes.Glass()` as a base, with additional CSS injected for:
- Dark-mode compatibility.
- Interactive card effects.
- Responsive container handling.

## Verification

### Automated Tests
- No automated tests for the UI, but we will verify the console logs for engine initialization.

### Manual Verification
1.  **Framework Check**: Run `uv run python app.py` and verify the local server starts.
2.  **Filter Logic**: Select "Non-Fiction" and "Joy" and search for "happy facts". Verify results adhere to both filters.
3.  **Semantic Search**: Query for "A book about space but with a dark vibe". Verify the engine returns relevant books with "Fear" or "Sadness" tones.
4.  **Responsive Check**: Verify the UI layout holds on narrow (mobile-sized) windows.
