# Hybrid Book Recommender System - Context & Instructions

## 1. Project Overview
This project aims to build a **Hybrid Book Recommender System** bridging traditional Collaborative Filtering (KNN) with modern Semantic Search (LLMs + Vector DBs).

*   **Goal:** Solve the "Cold Start" problem and demonstrate a production-grade MLOps lifecycle.
*   **Architecture:**
    *   **Collaborative Filtering:** Unsupervised learning (Nearest Neighbors) on user interaction matrices.
    *   **Content-Based:** Gemini/LLM-based zero-shot classification and embedding generation stored in ChromaDB/FAISS.
*   **Target Stack:** Python 3.12, `uv` (Package Manager), `DVC` (Data Pipelines), `MLflow` (Tracking), Docker, AWS EC2.

## 2. Current Project Status
**Status: Initial Scaffolding / Planning Phase**

The directory structure is currently a standard data science scaffold. The detailed architecture described in `references/project_overview.md` (Modular Pipelines, Components, DVC integration) **has not yet been implemented**.

*   **Existing:** Folder structure, detailed documentation/planning files.
*   **Missing:** `pyproject.toml` (UV config), `dvc.yaml`, implementation code in `src/`.
*   **Action Item:** The immediate focus is setting up the environment and implementing the first pipeline stage (Data Ingestion).

## 3. Architecture & Development Roadmap
The project plan calls for a specific "Platform Engineering" structure that differs from the current standard layout.

### Intended Structure (Target)
Future development should refactor `src/` to match this modular pattern:
```text
src/
├── components/                 # Logic (DataIngestion, ModelTrainer)
├── config/                     # Configuration Managers
├── entity/                     # Data Classes (ConfigEntity)
├── pipeline/                   # Orchestration scripts (Stage 01, Stage 02)
└── models/                     # Architecture definitions
```

### Immediate Next Steps
1.  **Environment Setup:** Initialize `uv` and create `pyproject.toml`.
2.  **Dependency Management:** Install core libraries (`dvc`, `pandas`, `scikit-learn`, `langchain`, `google-generativeai`).
3.  **Configuration:** Create `params.yaml` and `config/config.yaml`.
4.  **Data Ingestion:** Implement `src/components/data_ingestion.py` to handle the `7k-books` dataset.

## 4. Operational Commands (Planned)
*These commands are targets to be implemented.*

*   **Dependency Install:** `uv sync`
*   **Run Pipeline:** `dvc repro`
*   **Experiment Tracking:** `mlflow ui`

## 5. Development Conventions
*   **Package Management:** strictly use **`uv`**. Do not use `pip` directly if possible.
*   **Versioning:** All data and models must be tracked via **DVC**.
*   **Typing:** Use `pydantic` or Python dataclasses for configuration objects (`entity/`).
*   **Style:** Follow "Clean Code" principles—separate configuration from logic.
