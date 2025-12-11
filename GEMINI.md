# 🤖 GEMINI CLI Customization for Hybrid Recommender System

This file provides context to the Gemini model for its role as an AI assistant in the development of a **Hybrid Book Recommender System** that bridges Traditional Machine Learning and modern AI Engineering.

## 🚀 1. Project Goal

The primary objective is to solve the "Cold Start" problem in recommendation engines by combining **Collaborative Filtering** (User behavior) and **Semantic Search** (LLM-based content analysis). Concurrently, the project aims to demonstrate mastery of a production-grade **MLOps lifecycle** (Data Ingestion to Deployment) using "Platform Engineering" principles.

* **Architecture:**
    * **Track A (Traditional):** `Ratings Matrix` $\to$ `KNN` (Collaborative Filtering).
    * **Track B (GenAI):** `Book Descriptions` $\to$ `Gemini` (Augmentation) $\to$ `Embeddings` $\to$ `ChromaDB` (Semantic Search).

## 🛠️ 2. Core Technology Stack

Please assume all code examples, advice, and configuration relate to this specific stack:

| Layer | Tool | Notes |
| :--- | :--- | :--- |
| **Project Methodology** | CRISP-DM + MLOps | For lifecycle and structure (Lab $\to$ Factory $\to$ Showroom). |
| **Python** | Python 3.12 | Preferred environment. |
| **Dependencies** | **`uv`** + `pyproject.toml` | **Strict requirement.** Fast, reproducible dependency management. |
| **Data Versioning** | **DVC** | To track data lineage and orchestrate pipeline stages (`dvc.yaml`). |
| **Experiment Tracking** | **MLflow** | To log KNN metrics, Embedding parameters, and manage artifacts. |
| **GenAI & LLM** | **Gemini API** + **LangChain** | For Zero-Shot Classification and generating Vector Embeddings. |
| **Vector Database** | **ChromaDB** | For storing and retrieving semantic embeddings. |
| **Deployment** | **Docker** + **AWS EC2** | Containerized Streamlit application exposed via port mapping. |
| **CI/CD** | **GitHub Actions** | For automated testing, Docker builds, and deployment triggers. |
| **ML Models** | **Nearest Neighbors (KNN)** (Traditional) & **LLM Embeddings** (Content-Based) | Hybrid inference logic. |

## ✨ 3. Design Pillars (Non-Negotiable Requirements)

All proposed solutions, code, and architectural advice **must prioritize** these four requirements:

1.  **Reliability:** Robust error handling (`src/utils/exception.py`), strict data validation (Pydantic schemas), and deterministic environments (`uv.lock`).
2.  **Scalability:** Decoupled architecture where the Inference Engine (Streamlit/API) runs independently of the Training Pipeline (DVC).
3.  **Maintainability:** Adherence to "Clean Code" with a strict modular hierarchy:
    * `src/entity/`: Data classes.
    * `src/config/`: Configuration managers.
    * `src/components/`: Functional logic.
    * `src/pipeline/`: Orchestration scripts.
4.  **Adaptability & Reproducibility:**
    *   **DVC-Centric Configuration:** Parameters must be loaded from `params.yaml` via the DVC API (`dvc.api.params_show()`) to guarantee experiment reproducibility.
    *   **Flexible Overrides:** Ensure developers can override these defaults via command-line arguments (CLI) for rapid local testing without altering the tracked `params.yaml`.
    *   **Modular Design:** Facilitate swapping LLM providers (Gemini $\leftrightarrow$ OpenAI) or Algorithms (KNN $\leftrightarrow$ SVD) purely through configuration.

## 📝 4. Preferred Response Style

When responding to development queries, please:

* **Be brief and direct.**
* Provide **fully complete, self-contained code snippets** (e.g., full Python files or YAML configs).
* Focus on **MLOps best practices**: **Automation, Reproducibility, and Separation of Concerns**.
* Reference the specific project structure (e.g., "Add this to `src/components/data_ingestion.py`...").
* **Code Style:** "Clean Code" principles—modular, type-hinted, and documented (explaining the *why*, not just the *what*).

## ❓ 5. Example Interaction Topics

You can expect prompts related to the following specific development tasks:

* Writing **DVC stage definitions** for data ingestion and hybrid transformation.
* Configuring **MLflow logging** for unsupervised learning metrics (e.g., Silhouette score).
* Implementing **LangChain wrappers** for Gemini API interactions.
* Creating a **`Dockerfile`** that handles `uv` installation and Streamlit execution.
* Refactoring "Notebook code" into modular `src/components/` classes.
* Setting up **GitHub Actions** to trigger DVC reproduction on commit.

## 🤔 6. Additional Interaction Examples

| User Query | Expected Response Focus |
| :--- | :--- |
| "How do I set up the ingestion stage?" | Provide the `DataIngestionConfig` (Entity), the `DataIngestion` class (Component), and the `stage_01_ingestion.py` (Pipeline). |
| "Write the Dockerfile." | Provide a multi-stage `Dockerfile` that installs `uv`, copies `pyproject.toml`, and runs `uv sync` before starting Streamlit. |
| "How do I combine the two recommendation scores?" | Suggest a weighted average logic configurable via `params.yaml` ($\alpha \cdot Collaborative + \beta \cdot Content$). |
| "Configure the LLM parameters." | Show how to structure `params.yaml` for LLM settings (temperature, model name) and read them via `src/config/configuration.py`. |