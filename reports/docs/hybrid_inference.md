# **Hybrid Inference Engine Architecture**

## **1. Executive Summary**
The `HybridRecommender` (located in `src/models/hybrid_recommender.py`) acts as the "Brain" of the system. It solves the **Generic Recommendation Problem** (recommending popular but irrelevant items) and the **Long-Tail Problem** (recommending relevant but low-quality items) by combining two scoring signals: deep semantic intent and historical popularity data.

---

## **2. The Hybrid Algorithm**

The final score for a book is calculated using a **Linear Weighted Combination** of Semantic Similarity and Popularity.

$$ Score_{final} = (1 - Distance_{cosine}) + \alpha \cdot (\frac{Rating_{avg}}{5.0}) $$

Where:
* **$(1 - Distance_{cosine})$**: The Semantic Similarity Score (0 to 1). Higher is better (closer match).
* **$\alpha$ (alpha)**: The `popularity_weight` hyperparameter (defined in the `inference` section of `params.yaml`).
* **$Rating_{avg}$**: The book's average rating (1-5 stars) from the "Collaborative" dataset (CSV).

### **Why this works?**
* **Quality Filtering**: If a book is a **Perfect Semantic Match** (Similarity 1.0) but has a **1-star rating**, its final score is penalized.
* **Masterpiece Boosting**: If a book is a **Good Match** (Similarity 0.8) and is a **5-star Masterpiece**, it gets a boost, potentially outranking the perfect but poor-quality match.

---

## **3. Code Architecture & Principles**

### **A. Component Isolation & DI**
Following the **Antigravity Stack** standards, the `HybridRecommender` follows a **Dependency Injection (DI)** pattern. It does not instantiate its own configuration; instead, it receives a pre-validated `InferenceConfig` entity from the `ConfigurationManager`.

### **B. Initialization (`__init__`)**
*   **Decoupled Embeddings**: Uses `EmbeddingFactory` to instantiate the search model. Note: The `inference` model configuration can now be scaled independently of the `trainer` configuration in `params.yaml`.
*   **VectorDB Connection**: Establishes a read-only connection to the persisted `chroma_db` (ChromaDB Vector Store).
*   **Metadata Store**: Loads `clean_books.csv` into a Pandas DataFrame indexed by `isbn13`. This serves as an **O(1) lookup table** for ratings, ensuring sub-millisecond scoring latency.

### **C. Recommendation Flow (`recommend`)**
1.  **Semantic Retrieval**:
    *   The user query is converted into a vector.
    *   ChromaDB returns the top $K \times 3$ candidates to ensure a healthy pool for the quality-filtering phase.
2.  **Entity Linking**:
    *   Extracts the ISBN from the vector metadata. Handles robust type-casting (String to Int64) to ensure consistency with the metadata store.
3.  **Hybrid Scoring**:
    *   Calculates the final ranking score using the formula above.
4.  **Ranked Response**:
    *   Sorts the candidate pool by the final score and truncates to the user-defined `top_k`.

---

## **4. Configuration & Orchestration**

### **Hyperparameters (`params.yaml`)**
The behavior of the engine is fully tunable via DVC:
```yaml
inference:
  embedding_provider: huggingface
  model_name: sentence-transformers/all-MiniLM-L6-v2
  collection_name: books
  top_k: 10
  popularity_weight: 0.2
```

### **DVC Integration (`dvc.yaml`)**
The inference engine is integrated into the project's **Directed Acyclic Graph (DAG)** as `stage_05_prediction`. 
*   **Reproducibility**: Any change to the `popularity_weight` or the `model_name` will trigger a re-run of the prediction stage to verify the new settings.
*   **Verifiability**: It produces a `results.txt` artifact in `artifacts/prediction/` which serves as a "Smoke Test" for model quality after every training run.
