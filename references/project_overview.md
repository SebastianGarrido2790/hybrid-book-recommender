# **Project Executive Summary**

**1. Project Goals**
The primary objective of this project is to develop a **Hybrid Book Recommender System** that bridges the gap between traditional Machine Learning and modern AI Engineering. The project serves a dual purpose: to solve the "Cold Start" problem in recommendation engines by combining user behavior data with semantic content analysis, and to demonstrate mastery of a production-grade **MLOps (Machine Learning Operations)** lifecycle. Key learning outcomes include the implementation of Large Language Models (LLMs) in a functional workflow and the automation of the data science pipeline from ingestion to deployment.

**2. Architectural Design**
The system adopts a **Hybrid Inference Architecture** that integrates two distinct recommendation strategies into a unified pipeline:

* **Collaborative Filtering (Traditional ML):** Utilizes unsupervised learning (Nearest Neighbors) on user-item interaction matrices to recommend books based on community usage patterns and implicit trust.
* **Semantic Content-Based Filtering (GenAI):** Leverages Large Language Models (LLMs) to perform "Zero-Shot" classification and sentiment analysis on book descriptions. These descriptions are converted into vector embeddings and stored in a Vector Database (ChromaDB/FAISS) to enable semantic similarity search.

The infrastructure is built on a modular, pipeline-driven codebase. Package management is handled by **uv** to ensure deterministic environments, while **DVC (Data Version Control)** orchestrates the workflow steps (ingestion, transformation, training), ensuring that data and model lineage are strictly tracked.

**3. Design Requirements & Standards**
The project is strictly governed by four non-functional requirements to ensure production readiness:

* **Reliability:** The system must be robust against data errors. This is achieved through strict schema validation (Pydantic), comprehensive exception handling, and automated unit testing within the pipeline.
* **Scalability:** The architecture must support growth in data volume and traffic. This is managed by containerizing the application with **Docker** and deploying to **AWS EC2**, allowing the inference engine to run independently of the development environment.
* **Maintainability:** The codebase adheres to "Clean Code" principles, utilizing a modular structure (separating Configuration, Components, and Pipelines). Configuration is decoupled using `params.yaml`, allowing hyperparameters to be tuned without altering the source code.
* **Adaptability:** The system is designed for rapid iteration. By implementing **CI/CD (GitHub Actions)** and **MLflow**, the project supports the seamless swapping of LLM providers or algorithm logic without disrupting the core pipeline, facilitating continuous experiment tracking and model evolution.

**4. Technology Stack**
* **Language & Management:** Python 3.12, uv
* **Orchestration & Versioning:** DVC, Git, MLflow
* **Machine Learning:** Scikit-Learn, LangChain, Gemini API (LLM)
* **Deployment:** Docker, AWS (EC2), GitHub Actions
* **Interface:** Streamlit

---

### **7k Books** [Link](https://www.kaggle.com/datasets/dylanjcastillo/7k-books-with-metadata)

The dataset provides close to seven thousand books containing identifiers, title, subtitle, authors, categories, thumbnail url, description, published year, average rating, and number of ratings. The dataset is provided as comma-delimited CSV.

---

### **Project Plan**

This is a high-level strategic plan. We are adopting a **"Platform Engineering"** mindset—building not just a model, but a reproducible factory for models.

**UV** is the package manager of our choice; it is significantly faster than Pip/Poetry and creates strict, deterministic environments, which is the first step toward **Reliability**.

Here is the comprehensive overview of how we will execute this Hybrid Recommender System using the **CRISP-DM** lifecycle, adapted for modern **MLOps**.

---

### I. The AI Engineering Lifecycle (CRISP-DM + MLOps)

We will not build linearly. We will iterate through cycles, moving from "Lab" (Notebooks) to "Factory" (Pipelines) to "Showroom" (Deployment).

#### Phase 1: Business & Data Understanding (The Foundation)

  * **Goal:** Define exactly *how* the hybrid logic works and ensure our data supports it.
  * **Action:** We will audit the `7k-books` dataset. We need to decide the specific **Weighting Strategy** ($\alpha$ and $\beta$) for the hybrid merge:
    $$Score_{final} = \alpha \cdot Score_{Collaborative} + \beta \cdot Score_{Semantic}$$
  * **Deliverable:** A Data Validation Report and a finalized schema (Pydantic models).

#### Phase 2: Data Engineering (The Pipeline Core)

  * **Goal:** Create a reproducible data flow.
  * **Tools:** `uv` for environment, `DVC` for versioning.
  * **Strategy:** We will split processing into two parallel tracks:
    1.  **Structured Track:** Cleaning ratings, pivoting to user-item matrix (Sparse Matrices).
    2.  **Unstructured Track:** Text cleaning, LLM Augmentation (Sentiment tagging), and Embedding generation (Vectorization).

#### Phase 3: Modeling (The Hybrid Engine)

  * **Goal:** Train modular components that can be swapped easily (Adaptability).
  * **Collaborative:** Implement Nearest Neighbors (KNN). It's simple, interpretable, and effective for dense clusters.
  * **Content-Based:** Build a Vector Index (ChromaDB). This acts as our "Semantic Search Engine."
  * **Tracking:** We will use **MLflow** here to log parameters (e.g., `n_neighbors`, `embedding_model`) and metrics to ensure we aren't degrading performance as we iterate.

#### Phase 4: Deployment (The Production Layer)

  * **Goal:** Serve the model with high reliability.
  * **Containerization:** We will use **Docker** to package the OS, UV environment, code, and artifacts into a single portable unit.
  * **CI/CD:** We will use **GitHub Actions** to automate the "Build & Push" process whenever you commit code, ensuring that the production branch is always deployable.

---

### II. Project Structure (Optimization)

To maximize **Maintainability** and **Separation of Concerns** for a DVC pipeline unmlike classic Cookiecutter Data Science, we should use a decouple **Pipeline Stages** (the scripts DVC runs) from the **Model Definitions** (the logic).

**Source structure `src/`:**

```text
src/
├── __init__.py
├── components/                 # The "Workhorses"
│   ├── __init__.py
│   ├── data_ingestion.py       # Downloads & unzips
│   ├── data_validation.py      # Checks schemas
│   ├── data_transformation.py  # Pivot tables & Embeddings
│   └── model_trainer.py        # Trains KNN & Builds VectorDB
│
├── config/                     # Configuration Managers
│   ├── __init__.py
│   └── configuration.py        # Reads yaml and returns Entity objects
│
├── entity/                     # Data Classes only
│   ├── __init__.py
│   └── config_entity.py        # Typedefs for config (e.g., DataIngestionConfig)
│
├── pipeline/                   # The "Conductors"
│   ├── __init__.py
│   ├── stage_01_ingestion.py   # Calls component.ingest()
│   ├── stage_02_validation.py
│   └── stage_03_training.py
│
├── models/                     # Architecture Definitions
│   ├── __init__.py
│   ├── hybrid_recommender.py   # The class that merges KNN + VectorDB scores
│   └── llm_utils.py            # Wrappers for Gemini/LangChain
│
└── utils/                      # Shared Utilities
```

  * **`components`** contain the logic (functional).
  * **`pipeline`** triggers the components (orchestration).
  * **`dvc.yaml`** executes the files in `src/pipeline/`.
    This makes debugging significantly easier. If the pipeline fails, you check `pipeline`. If the math is wrong, you check `components` or `models`.

---

### III. Expected Deliverables

By the end of this project, you will have:

1.  **The Codebase:** A clean, modular Python package managed by UV.
2.  **The Artifacts:** Versioned datasets and trained models (KNN `.pkl` and ChromaDB index) tracked by DVC.
3.  **The Application:** A Streamlit interface running inside a Docker container.
4.  **The API:** An interface that accepts a User ID or a Search Query and returns a list of ISBNs.
5.  **The Documentation:** A `README.md` and inline comments explaining the *architectural decisions* (The "Why").
6.  **The Dashboard:** An MLflow server (local or hosted) showing your experiment history.

---

### IV. Potential Starting Points

Here is a recommended roadmap to begin:

1.  **Environment Initialization:**

      * Initialize the Git repo.
      * Set up `pyproject.toml` with UV.
      * Create the folder structure (scripted).

2.  **Data Ingestion (Stage 01):**

      * Write `params.yaml` to define where data comes from.
      * Implement the download logic.
      * Initialize DVC to track the raw CSV.

3.  **Exploratory Data Analysis (EDA):**

      * Before writing the pipeline, we will use a Notebook to inspect the `7k-books` dataset, checking for missing values and distribution, to inform our `clean_data` logic.

---

## **Analogy**:

Building this hybrid recommender system using **MLOps practices** is like creating a high-tech custom kitchen (the final product) from scratch.

- **The Recommender Systems are the cooking components**: The Collaborative Filter is your classic oven (reliable, based on past usage history), and the LLM/Vector Search is your smart induction cooktop (fast, precise, and handles complex new ingredients/queries).

- **The MLOps Pipeline is the construction plan and automated assembly line**: Instead of building the kitchen manually (Jupyter Notebook), you have specialized crews (Data Ingestion, Transformation, Training components) that work sequentially.

- **Docker**: Is the pre-fabricated, tested module that guarantees the oven and cooktop fit and work perfectly, regardless of where you install the kitchen (AWS EC2).

- **MLflow/DVC**: Are the detailed blueprints and material logs, tracking every model version and every batch of ingredients used, ensuring the kitchen can be rebuilt exactly the same way anytime.

- **Configuration Management**: Is the single master panel where you can adjust the temperature or materials across the entire kitchen instantly, rather than manually adjusting every individual component.