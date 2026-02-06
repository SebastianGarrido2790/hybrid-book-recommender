hybrid-book-recommender
├── .dockerignore
├── .dvc/                      <- DVC configuration directory.
├── .dvcignore
├── .env                       <- Secret environment variables (Gemini API Key, AWS creds).
├── .github/
│   └── workflows/             <- CI/CD configuration (main.yaml).
├── .gitignore
├── .pytest_cache/
├── .python-version
├── .venv/                     <- Virtual environment.
├── .vscode/
├── Dockerfile                 <- Production container definition.
├── GEMINI.md                  <- Gemini Model Documentation.
├── Hybrid-Book-Recommender.code-workspace
├── LICENSE.txt                <- Project's license.
├── README.md                  <- Top-level documentation.
├── app.py                     <- Gradio Web Application.
├── artifacts/                 <- Pipeline outputs (gitignored, tracked by DVC).
│   ├── data_enrichment/
│   ├── data_ingestion/
│   ├── data_transformation/
│   ├── data_validation/
│   ├── model_evaluation/
│   ├── model_trainer/
│   ├── prediction/
│   └── tone_analysis/
├── assets/                    <- Static assets (images, logos).
├── config/
│   ├── config.yaml            <- System paths configuration.
│   └── params.yaml            <- Hyperparameters configuration.
├── data/                      <- Raw data storage (gitignored).
├── dvc.lock                   <- DVC reproduction lock file (Exact state snapshot).
├── dvc.yaml                   <- DVC Pipeline definition (DAG).
├── logs/                      <- Runtime logs.
├── main.py                    <- Pipeline Orchestrator (Script mode).
├── mlflow.db                  <- Local MLflow database.
├── mlruns/                    <- MLflow experiment tracking storage.
├── models/                    <- Serialized models / artifacts.
├── notebooks/                 <- Jupyter notebooks for experimentation.
├── pyproject.toml             <- UV dependency definitions.
├── references/                <- Project documentation and standards.
│   ├── project_overview.md
│   └── ...
├── reports/                   <- Generated analysis and documentation.
│   ├── docs/                  <- Pipeline stage reports.
│   │   ├── dvc_pipeline_report.md
│   │   ├── stage_01_ingestion.md
│   │   └── ...
│   └── figures/
├── scripts/                   <- Shell scripts.
├── src/                       <- Application Source Code.
│   ├── __init__.py
│   │
│   ├── components/            <- Business Logic / Workers (The "How").
│   │   ├── __init__.py
│   │   ├── batch_prediction.py     <- Batch inference logic.
│   │   ├── data_enrichment.py      <- Zero-shot classification logic.
│   │   ├── data_ingestion.py       <- Download & unzip logic.
│   │   ├── data_transformation.py  <- Split & Clean logic.
│   │   ├── data_validation.py      <- Schema validation logic.
│   │   ├── model_evaluation.py     <- Metric calculation logic.
│   │   ├── model_trainer.py        <- Embedding Generation & Indexing.
│   │   └── tone_analysis.py        <- Sentiment analysis logic.
│   │
│   ├── config/                <- Configuration Management.
│   │   ├── __init__.py
│   │   └── configuration.py        <- Validates inputs and creates config entities.
│   │
│   ├── entity/                <- Dataclasses (Type Definitions).
│   │   ├── __init__.py
│   │   ├── config_entity.py        <- Config DTOs.
│   │   └── recommendation_entity.py<- Recommendation Result DTOs.
│   │
│   ├── features/              <- Feature Engineering.
│   │   ├── __init__.py
│   │   └── build_features.py
│   │
│   ├── models/                <- Core Model Architectures.
│   │   ├── __init__.py
│   │   ├── hybrid_recommender.py   <- Hybrid Engine (Vector Search + Filtering).
│   │   └── llm_utils.py            <- LLM & Embedding Wrappers.
│   │
│   ├── pipeline/              <- Execution Stages (The "When").
│   │   ├── __init__.py
│   │   ├── stage_01_ingestion.py
│   │   ├── stage_02_validation.py
│   │   ├── stage_03_transformation.py
│   │   ├── stage_04_training.py
│   │   ├── stage_05_prediction.py
│   │   └── stage_06_evaluation.py
│   │
│   ├── scripts/               <- Offline specific scripts.
│   │   ├── run_enrichment.py       <- Runner for offline enrichment.
│   │   └── run_tone_analysis.py    <- Runner for offline tone analysis.
│   │
│   ├── tests/                 <- Unit and Integration Tests.
│   │   ├── __init__.py
│   │   ├── conftest.py             <- Pytest fixtures.
│   │   ├── test_broad_accuracy.py
│   │   ├── test_enrichment_accuracy.py
│   │   ├── test_recommender.py
│   │   └── test_tone_accuracy.py
│   │
│   ├── utils/                 <- Shared Utilities.
│   │   ├── __init__.py
│   │   ├── common.py               <- YAML readers, directory creators.
│   │   ├── exception.py            <- Custom Exception handling.
│   │   ├── logger.py               <- Centralized Logging.
│   │   ├── mlflow_config.py        <- MLflow URL logic.
│   │   └── paths.py                <- Path constants.
│   │
│   └── visualization/         <- Plotting Tools.
│       ├── __init__.py
│       ├── plot_settings.py
│       └── visualize.py
│
├── template.py                <- Project scaffolding script.
└── uv.lock                    <- Dependency lock file (Exact versions).