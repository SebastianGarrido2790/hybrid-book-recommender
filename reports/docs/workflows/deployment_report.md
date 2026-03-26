# Phase 4: Deployment Report

## 1. Executive Summary
This document details the successful execution of **Phase 4: Deployment**, transforming the *Hybrid Book Recommender* from a local development project into a production-ready, containerized application with automated testing and Continuous Integration/Continuous Deployment (CI/CD) pipelines.

The deployment strategy focuses on **Reliability**, **Portability**, and **Automation**. We have established a robust testing framework to catch regressions, a Docker container for consistent execution across environments, and a GitHub Actions workflow to automate the build verification process.

## 2. Testing Framework (`tests`)
A comprehensive testing suite has been implemented using **`pytest`** to ensure the reliability of the core recommendation logic before it reaches production.

> [!NOTE]
> Detailed test methodology and scores have been moved to the [**Test Suite Report**](../evaluations/test_suite_report.md).

### **Execution Protocol**
*   **Command:** `uv run pytest tests/`
*   **Environment:** Runs within a deterministic lockfile environment to ensure 100% reproducibility.
*   **Coverage:** Includes both unit and integration tests across the recommendation engine and data enrichment pipelines.

## 3. Containerization Strategy (Docker)
The application has been packaged into a Docker container to guarantee **"Build Once, Run Anywhere"** portability.

### **Dockerfile Architecture**
*   **Base Image:** `python:3.11-slim` (Minimizes attack surface and image size).
*   **Package Management:** **`uv`** (Astral) installed directly from its official image.
*   **Layer Caching:** `uv.lock` and `pyproject.toml` are copied and synced *before* the source code.
*   **Runtime Security:** The application runs as a standard processes, listening on port `7860`.
*   **Command:** The container executes using `uv run python -m src.app.main` for full package support.

### **Docker Ignore**
A rigorous `.dockerignore` file ensures that local development artifacts (virtual environments, logs, caches, large datasets) are **excluded** from the build context, keeping the image lean and secure.

## 4. CI/CD Pipeline (GitHub Actions)
An automated pipeline has been established to guard the `main` branch against broken code.

### **Workflow: `.github/workflows/main.yaml`**
*   **Trigger:** Pushes and Pull Requests to the `main` branch.
*   **Jobs:**
    1.  **Environment Setup:** Installs Python 3.11 and `uv`.
    2.  **Dependency Synchronization:** Runs `uv sync --frozen` to install the **exact** dependency versions defined in `uv.lock`.
    3.  **Automated Testing:** Executes the unit test suite (`pytest`). The build **fails** if logic is broken.
    4.  **Build & Push (CD):**
        *   **Action:** Uses `docker/build-push-action`.
        *   **Metadata:** Automatically generates tags (e.g., `latest`).
        *   **Push:** Pushes the built image to **GitHub Container Registry (GHCR)** *only* if the branch is `main`. This ensures that every merged PR results in a deployable artifact.
        
#### **Security & Authorization**
*   **GHCR Login:** Authenticates using `secrets.GITHUB_TOKEN` (automatic repository secret) to push images securely to the package registry.
*   **Permissions:** Verified `packages: write` permission for the job.

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
uv run pytest tests -v

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

### **Modular Execution**
Running the app without Docker:
```bash
# Launch server via python modular command
uv run python -m src.app.main

# Or via Makefile (Recommended)
make serve
```

### **Cleanup**
```bash
# Remove the image
docker rmi hybrid-recommender

# Prune unused Docker objects (use with caution)
docker system prune
```
