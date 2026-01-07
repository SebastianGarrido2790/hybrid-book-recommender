hybrid-book-recommender
├── LICENSE.txt                <- Project's license (Open-source if one is chosen).
├── README.md                  <- The top-level README for developers using this project.
├── .env                       <- Secret environment variables (Gemini API Key, AWS creds).
├── .gitignore                 <- Files to ignore by Git.
├── dvc.yaml                   <- The Pipeline Conductor.
├── params.yaml                <- Hyperparameters (K-neighbors, Chunk size).
├── pyproject.toml             <- UV dependency definitions.
├── Dockerfile                 <- Production container definition.
├── template.py                <- Python script to generate the MLOps directory structure (Configuration, Components, Pipelines) automatically.
├── main.py                    <- Acts as the "Switchboard" for the project.
│
├── .github/
│   └── workflows/             <- CI/CD (main.yaml).
│
├── artifacts/
│   └── data_ingestion/
│       ├── data.zip
│       └── books.csv  (The extracted file)
│
├── config/
│   └── config.yaml            <- System paths (artifacts/data).
│
├── 🛡️ Hybrid-book-Recommender.code-workspace <- VS Code workspace configuration.
│
├── models/                    <- Trained and serialized models, model predictions, or model summaries.
│
├── notebooks/                 <- Jupyter notebooks.
│
├── references/                <- Data dictionaries, manuals, and all other explanatory materials.
│   └── folder_structure.md
│
├── reports/                   <- Generated analysis as HTML, PDF, LaTeX, etc.
│   ├── docs/                  <- Generated documents to be used in reporting.
│   └── figures/               <- Generated graphics and figures to be used in reporting.
│
└── src/                            <- Source code for use in this project.
    │
    ├── __init__.py                 <- Makes src a Python module.
    │
    ├── features/
    │   ├── __init__.py
    │   └── build_features.py       <- Code to create features for modeling.
    │
    ├── components/                 <- The "Workhorses".
    │   ├── __init__.py
    │   ├── data_ingestion.py       <- Downloads & unzips.
    │   ├── data_validation.py      <- Clean & validate.
    │   ├── data_transformation.py  <- Apply transformations and split data into train/val/test.
    │   └── model_trainer.py        <- Trains KNN & Builds VectorDB.
    │
    ├── config/                     <- The "Brain".
    │   ├── __init__.py
    │   └── configuration.py        <- Reads yaml, manages the configuration and returns Entity objects.
    │
    ├── constants/                  <- Never-changing values (e.g., file paths).
    │   └── __init__.py
    │
    ├── entity/                     <- Data Classes only.
    │   ├── __init__.py
    │   └── config_entity.py        <- Typedefs for config (e.g., DataIngestionConfig).
    │
    ├── pipeline/                       <- The "Conductors".
    │   ├── __init__.py
    │   ├── stage_01_ingestion.py       <- Calls component.ingest().
    │   ├── stage_02_validation.py      <- Calls component.validate().
    │   ├── stage_03_transformation.py  <- Calls component.transform().
    │   └── stage_04_training.py        <- Calls component.train().
    │
    ├── models/                     <- Architecture Definitions.
    │   ├── __init__.py
    │   ├── hybrid_recommender.py   <- The class that merges KNN + VectorDB scores.
    │   └── llm_utils.py            <- Wrappers for Gemini/LangChain.
    │
    ├── utils/                   <- Common tools.
    │   ├── common.py            <- Config readers.
    │   ├── paths.py             <- Define and manage file paths used throughout the project.
    │   ├── mlflow_config.py     <- MLflow configuration across modules.
    │   ├── logger.py            <- Logging setup for standardized log messages.
    │   └── exception.py         <- Custom Error Handling (Reliability).
    │
    └── visualization/
        ├── __init__.py
        ├── plot_settings.py
        └── visualize.py         <- Code to create visualizations.