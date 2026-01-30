# Phase 4: Deployment Report

## 1. Executive Summary
This document details the successful execution of **Phase 4: Deployment**, transforming the *Hybrid Book Recommender* from a local development project into a production-ready, containerized application with automated testing and Continuous Integration/Continuous Deployment (CI/CD) pipelines.

The deployment strategy focuses on **Reliability**, **Portability**, and **Automation**. We have established a robust testing framework to catch regressions, a Docker container for consistent execution across environments, and a GitHub Actions workflow to automate the build verification process.

## 2. Testing Framework (`src/tests`)
A comprehensive testing suite has been implemented using **`pytest`** to ensure the reliability of the core recommendation logic before it reaches production. We selected `pytest` over `unittest` for its simplicity, scalability, and ability to handle complex test scenarios with minimal boilerplate.

### **Unit Tests**
*   **Location:** `src/tests/test_recommender.py`
*   **Scope:** Verifies the functionality of the `HybridRecommender` class.
*   **Framework Features Used:**
    *   **Fixtures:** Modular setup functions (annotated with `@pytest.fixture`) are used to inject mock configurations and data (`mock_config`, `mock_dependencies`). This replaces the rigid `setUp()` method of `unittest`.
    *   **Assertions:** Uses standard Python `assert` statements (e.g., `assert len(recommendations) == 2`) which are cleaner and more pythonic than `self.assertEqual`.
    *   **Approximate Comparisons:** Uses `pytest.approx()` for floating-point comparisons in scoring logic.
*   **Mocking Strategy:**
    *   **External Dependencies:** Mocks `langchain_chroma.Chroma` and `src.models.llm_utils.EmbeddingFactory` to isolate the recommender logic from external API calls (Gemini/Hugging Face) and file system operations.
    *   **Data Sources:** Mocks `pandas.read_csv` to provide controlled, synthetic book data for predictable test outcomes.
*   **Key Test Cases:**
    *   `test_recommend_flow`: Verifies that the hybrid score matches the expected mathematical formula (Use Case: General Search).
    *   `test_recommend_with_filter`: Verifies that hard filters (Category/Tone) correctly exclude non-matching candidates (Use Case: Filtered Search).

### **Test Configuration**
*   **ConfTest:** `src/tests/conftest.py` ensures that the project root is strictly added to `sys.path`, preventing `ModuleNotFoundError` during test discovery.
*   **Execution:** Tests are executed via `uv run pytest src/tests`, ensuring they run within the deterministic lockfile environment.

## 3. Containerization Strategy (Docker)
The application has been packaged into a Docker container to guarantee **"Build Once, Run Anywhere"** portability.

### **Dockerfile Architecture**
*   **Base Image:** `python:3.12-slim` (Minimizes attack surface and image size).
*   **Package Management:** **`uv`** (Astral) is installed directly from its official image to handle dependency installation.
*   **Layer Caching:** `uv.lock` and `pyproject.toml` are copied and synced *before* the source code. This ensures that Docker rebuilds are instant unless dependencies change.
*   **Runtime Security:** The application runs as a standard process, listening on port `7860`.
*   **Configuration Handling:** The `ConfigurationManager` was updated to gracefully fallback to `params.yaml` direct reading when running inside Docker (where `.git` and DVC internals are absent).

### **Docker Ignore**
A rigorous `.dockerignore` file ensures that local development artifacts (virtual environments, logs, caches, large datasets) are **excluded** from the build context, keeping the image lean and secure.

## 4. CI/CD Pipeline (GitHub Actions)
An automated pipeline has been established to guard the `main` branch against broken code.

### **Workflow: `.github/workflows/main.yaml`**
*   **Trigger:** Pushes and Pull Requests to the `main` branch.
*   **Jobs:**
    1.  **Environment Setup:** Installs Python 3.12 and `uv`.
    2.  **Dependency Synchronization:** Runs `uv sync --frozen` to install the **exact** dependency versions defined in `uv.lock`.
    3.  **Automated Testing:** Executes the unit test suite (`pytest`). The build **fails** if logic is broken.
    4.  **Build Verification:** Attempts to build the Docker image (`docker build .`). This ensures that the application is always packaging-ready.

#### **Docker Logic**
Wrapped the build command in a conditional check (`if docker info ...`). This ensures the step won't crash if the Docker daemon isn't available (common in some local runners), but will still execute on the standard GitHub Actions runner.

This file is an Insurance Policy. It guarantees that:

1. The code works on a clean machine (not just "on my machine").
2. Dependencies are locked and secure.
3. The core logic (Recommend) is mathematically correct.
4. The application can be packaged into a container.

## 5. Verification & Results
*   **Local Test Pass:** All unit tests gathered and passed successfully in `< 1s`.
*   **Container Runtime:** The container `hybrid-recommender` successfully builds and serves the Gradio application on `http://localhost:7860`.
*   **Network Binding:** The application listening interface was updated to `0.0.0.0` to ensure accessibility from outside the container.
*   **GitHub Actions:** The CI/CD pipeline successfully executed all jobs and passed all tests.

## 6. Conclusion
Phase 4 successfully bridges the gap between "Science" and "Engineering". The *Hybrid Book Recommender* is no longer just a script; it is a tested, portable, and automatable software product ready for cloud deployment (e.g., AWS EC2, Hugging Face Spaces).

## 7. Appendix: Operational Commands

### **CI/CD Workflow (Local)**
To simulate the GitHub Actions pipeline locally:

```bash
# 1. Install Dependencies (Exact versions from uv.lock)
uv sync --frozen

# 2. Run Unit Tests
uv run pytest src/tests -v

# 3. Build Docker Image
docker build . -t hybrid-recommender:latest
```

### **Docker Operations**

### **Build & Run**
```bash
# Build the image (tag it as 'hybrid-recommender')
docker build -t hybrid-recommender .

# Run the container (detached mode, mapping port 7860)
docker run -d -p 7860:7860 --name hybrid-app hybrid-recommender
```

### **Management & Debugging**
```bash
# View running containers
docker ps

# View logs (add -f to follow real-time)
docker logs -f hybrid-app

# Stop the container
docker stop hybrid-app

# Remove the container
docker rm hybrid-app

# Access the container shell (for deep debugging)
docker exec -it hybrid-app /bin/bash
```

### **Cleanup**
```bash
# Remove the image
docker rmi hybrid-recommender

# Prune unused Docker objects (use with caution)
docker system prune
```
