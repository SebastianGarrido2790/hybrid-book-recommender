# **Project Executive Summary**

## **1. Project Goals**
The primary objective of this project is to develop a **Hybrid Book Recommender System** that bridges the gap between traditional Machine Learning and modern AI Engineering. The project serves a dual purpose: to solve the "Cold Start" problem in recommendation engines by combining user behavior data with semantic content analysis, and to demonstrate mastery of a production-grade **MLOps (Machine Learning Operations)** lifecycle. Key learning outcomes include the implementation of Large Language Models (LLMs) in a functional workflow and the automation of the data science pipeline from ingestion to deployment.

## **2. Architectural Design**
The system adopts a **Hybrid Inference Architecture** that integrates two distinct recommendation strategies into a unified pipeline:

* **Collaborative Filtering (Traditional ML):** Utilizes unsupervised learning (Nearest Neighbors) on user-item interaction matrices to recommend books based on community usage patterns and implicit trust.
* **Semantic Content-Based Filtering (GenAI):** Leverages Large Language Models (LLMs) to perform "Zero-Shot" classification and sentiment analysis on book descriptions. These descriptions are converted into vector embeddings and stored in a Vector Database (ChromaDB/FAISS) to enable semantic similarity search.

### **The High-Level Architecture**

This system operates on two parallel tracks that converge at the inference layer (Streamlit/API).

  * **Track A (Traditional):** `Ratings Matrix` $\rightarrow$ `CSR Matrix` $\rightarrow$ `KNN Model`.
  * **Track B (GenAI):** `Book Metadata` $\rightarrow$ `LLM Processing (Zero-shot/Sentiment)` $\rightarrow$ `Embeddings` $\rightarrow$ `Vector DB`.

The infrastructure is built on a modular, pipeline-driven codebase. Package management is handled by **uv** to ensure deterministic environments, while **DVC (Data Version Control)** orchestrates the workflow steps (ingestion, transformation, training), ensuring that data and model lineage are strictly tracked.

## **3. Design Requirements & Standards**
The project is strictly governed by four non-functional requirements to ensure production readiness:

* **Reliability:** The system must be robust against data errors. This is achieved through strict schema validation (Pydantic), comprehensive exception handling, and automated unit testing within the pipeline.
* **Scalability:** The architecture must support growth in data volume and traffic. This is managed by containerizing the application with **Docker** and deploying to **AWS EC2**, allowing the inference engine to run independently of the development environment.
* **Maintainability:** The codebase adheres to "Clean Code" principles, utilizing a modular structure (separating Configuration, Components, and Pipelines). Configuration is decoupled using `params.yaml`, allowing hyperparameters to be tuned without altering the source code.
*   **Adaptability:** The system is designed for rapid iteration. By implementing **CI/CD (GitHub Actions)** and **MLflow**, the project supports the seamless swapping of LLM providers (e.g., Gemini, Hugging Face models) or algorithm logic without disrupting the core pipeline, facilitating continuous experiment tracking and model evolution.

## **4. Technology Stack**
* **Language & Management:** Python 3.12, uv
* **Orchestration & Versioning:** DVC, Git, MLflow
* **Machine Learning:** Scikit-Learn, LangChain, Gemini API (LLM), Hugging Face Transformers (Open-Source LLMs)
* **Deployment:** Docker, AWS (EC2), GitHub Actions
* **Interface:** Streamlit

---

## **7k Books Dataset** 
[Link](https://www.kaggle.com/datasets/dylanjcastillo/7k-books-with-metadata)

The dataset provides close to seven thousand books containing identifiers, title, subtitle, authors, categories, thumbnail url, description, published year, average rating, and number of ratings. The dataset is provided as comma-delimited CSV.

### **Suitability for LLM Applications**
The design calls for **Vector Embeddings**, **Sentiment Analysis**, and **Zero-Shot Classification**.

| Feature | **7k-books-with-metadata** ||
| :--- | :--- | :--- |
| **Data Source** | `description` column (Rich text) 
| **Vector Search** | ✅ **Possible.** We can embed the full synopsis to find semantic similarities (e.g., "books about overcoming grief").
| **Sentiment Analysis** | ✅ **High Quality.** An LLM can easily analyze the tone of a paragraph-long description. 
| **Classification** | ✅ **Accurate.** LLMs can read the description and zero-shot classify it into "Fiction/Non-fiction".

### **Suitability for MLOps & Clean Code**
The idea is a "clean, simple, and well-documented" project.

* **Data Hygiene:** `7k-books` is a modern, UTF-8 encoded CSV. Unlike old datasets, which uses `latin-1` encoding, has "bad lines" (semicolon delimiters inside text fields), and mixed data types (Integers mixed with Strings in the Year column).
* **Pipeline Stability:** Using dirty data often causes `Data Validation` pipelines (Pydantic/Great Expectations) to fail constantly, forcing you to spend 80% of the time cleaning data rather than building models.
* **Speed:** 7,000 rows is the "Goldilocks" size for a portfolio project. It is large enough to be interesting but small enough that **Docker builds**, **CI/CD tests**, and **LLM embedding generation** will run in minutes, not days.

### **The Hybrid "Collaborative" Challenge**
There is one trade-off. The `7k-books` dataset usually comes as metadata only. To build the **Collaborative Filtering** (User-User) component, user ratings are needed.

**The Solution for the Project:**
Since we are combining systems, we have two options:
1.  **Find the accompanying ratings:** This dataset is often a subset of larger crawls. we can look for a "ratings" file that matches these ISBNs.
2.  **Synthetic/Implicit Data (Recommended for Portfolios):** Since our goal is to *master the architecture*, we can simulate the interaction matrix for the 7k books, OR simply use the `ratings_count` and `average_rating` columns included in `7k-books` to build a "Popularity-Based" filter as a proxy for the traditional component until we merge a user-ratings file.

---

## **Project Plan**

This is a high-level strategic plan. We are adopting a **"Platform Engineering"** mindset—building not just a model, but a reproducible factory for models.

**UV** is the package manager of our choice; it is significantly faster than Pip/Poetry and creates strict, deterministic environments, which is the first step toward **Reliability**.

Here is the comprehensive overview of how we will execute this Hybrid Recommender System using the **CRISP-DM** lifecycle, adapted for modern **MLOps**.

---

### **I. The AI Engineering Lifecycle (CRISP-DM + MLOps)**

We will not build linearly. We will iterate through cycles, moving from "Lab" (Notebooks) to "Factory" (Pipelines) to "Showroom" (Deployment).

#### **Phase 1: Business & Data Understanding (The Foundation)**

  * **Goal:** Define exactly *how* the hybrid logic works and ensure our data supports it.
  * **Action:** We will audit the `7k-books` dataset. We need to decide the specific **Weighting Strategy** ($\alpha$ and $\beta$) for the hybrid merge:
    $$Score_{final} = \alpha \cdot Score_{Collaborative} + \beta \cdot Score_{Semantic}$$
  * **Deliverable:** A Data Validation Report and a finalized schema (Pydantic models).

#### **Phase 2: Data Engineering (The Pipeline Core)**

  * **Goal:** Create a reproducible data flow.
  * **Tools:** `uv` for environment, `DVC` for versioning.
  * **Strategy:** We will split processing into two parallel tracks:
    1.  **Structured Track:** Cleaning ratings, pivoting to user-item matrix (Sparse Matrices).
    2.  **Unstructured Track:** Text cleaning, LLM Augmentation (Sentiment tagging), and Embedding generation (Vectorization).

#### **Phase 3: Modeling (The Hybrid Engine)**

  * **Goal:** Train modular components that can be swapped easily (Adaptability).
  * **Collaborative:** Implement Nearest Neighbors (KNN). It's simple, interpretable, and effective for dense clusters.
  * **Content-Based:** Build a Vector Index (ChromaDB). This acts as our "Semantic Search Engine."
  * **Tracking:** We will use **MLflow** here to log parameters (e.g., `n_neighbors`, `embedding_model`) and metrics to ensure we aren't degrading performance as we iterate.

#### **The Hybrid Pipeline Stages**

We will automate these stages using `dvc repro`.

#### Stage 00: Ingestion

  * **Goal:** Fetch data from Kaggle/GitHub.
  * **Action:** Write a script that checks if data exists; if not, downloads and unzips it.
  * **MLOps:** DVC tracks the `.csv` hash. If the source data changes, DVC invalidates downstream stages.

#### Stage 01: Validation & Cleaning

  * **Goal:** Ensure data schema integrity.
  * **Reliability:** Use Pydantic models (in `src/entity`) to validate incoming data types.
  * **Logic:** Filter out users with \< 50 ratings (to reduce noise for the KNN) and books with no descriptions (useless for LLM).

#### Stage 02: Hybrid Transformation (The Complex Part)

We branch the logic here:

1.  **For KNN:** Pivot `User-ID`, `ISBN`, `Rating` into a matrix.
2.  **For LLM:**
      * **Text Cleaning:** Remove HTML tags/artifacts.
      * **Feature Augmentation:** Use `LangChain` + `Gemini` to generate a "Sentiment" tag for each book description (e.g., "Melancholic", "Uplifting").
      * **Zero-Shot:** Classify books into standardized genres if the raw data is messy.

#### Stage 03: Model Training & Vector Indexing

1.  **KNN:** Fit the `NearestNeighbors` algorithm on the matrix. Save as `model.pkl`.
2.  **Vector DB:** Use `LangChain` to embed book summaries (using `GoogleGenerativeAIEmbeddings`) and push them into **ChromaDB** (local) or **FAISS**.
3.  **Tracking:** Log the KNN metrics (cluster inertia) and the Vector DB size to **MLflow**.

#### **Phase 4: Deployment (The Production Layer)**

  * **Goal:** Serve the model with high reliability.
  * **Containerization:** We will use **Docker** to package the OS, UV environment, code, and artifacts into a single portable unit.
  * **CI/CD:** We will use **GitHub Actions** to automate the "Build & Push" process whenever you commit code, ensuring that the production branch is always deployable.

#### Docker Integration

We will write a `Dockerfile` that:

1.  Uses a slim Python base image.
2.  Installs `uv`.
3.  Copies `pyproject.toml` and `uv.lock`.
4.  Runs `uv sync` to install dependencies.
5.  Exposes port 8501 (Streamlit).

#### AWS & CI/CD

  * **GitHub Actions:** On a push to `main`:
    1.  Run unit tests (`pytest`).
    2.  Build the Docker image.
    3.  Push to AWS ECR (Elastic Container Registry).
    4.  SSH into EC2 and run `docker pull` && `docker run`.

---

### **II. Project Structure (Optimization)**

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

### **III. Expected Deliverables**

By the end of this project, you will have:

1.  **The Codebase:** A clean, modular Python package managed by UV.
2.  **The Artifacts:** Versioned datasets and trained models (KNN `.pkl` and ChromaDB index) tracked by DVC.
3.  **The Application:** A Streamlit interface running inside a Docker container.
4.  **The API:** An interface that accepts a User ID or a Search Query and returns a list of ISBNs.
5.  **The Documentation:** A `README.md` and inline comments explaining the *architectural decisions* (The "Why").
6.  **The Dashboard:** An MLflow server (local or hosted) showing your experiment history.

---

### **IV. Potential Starting Points**

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

## **Project Analogy**:

Building this hybrid recommender system using **MLOps practices** is like creating a high-tech custom kitchen (the final product) from scratch.

- **The Recommender Systems are the cooking components**: The Collaborative Filter is your classic oven (reliable, based on past usage history), and the LLM/Vector Search is your smart induction cooktop (fast, precise, and handles complex new ingredients/queries).

- **The MLOps Pipeline is the construction plan and automated assembly line**: Instead of building the kitchen manually (Jupyter Notebook), you have specialized crews (Data Ingestion, Transformation, Training components) that work sequentially.

- **Docker**: Is the pre-fabricated, tested module that guarantees the oven and cooktop fit and work perfectly, regardless of where you install the kitchen (AWS EC2).

- **MLflow/DVC**: Are the detailed blueprints and material logs, tracking every model version and every batch of ingredients used, ensuring the kitchen can be rebuilt exactly the same way anytime.

- **Configuration Management**: Is the single master panel where you can adjust the temperature or materials across the entire kitchen instantly, rather than manually adjusting every individual component.