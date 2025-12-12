"""
Utility module for defining and managing file paths used throughout the project.
Includes automatic environment detection from `.env`.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# --- Load environment variables (once, globally) ---
load_dotenv()
ENV = os.getenv("ENV", "local").lower()  # e.g., "local", "staging", "production"

# --- Project Root ---
# Automatically finds the top-level directory (the one containing 'src/')
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# --- Config & Params ---
CONFIG_DIR = PROJECT_ROOT / "config"
CONFIG_FILE_PATH = CONFIG_DIR / "config.yaml"
PARAMS_FILE_PATH = PROJECT_ROOT / "params.yaml"

# --- Data Directories ---
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

# --- Model, Reports, and Artifacts ---
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
DOCS_DIR = REPORTS_DIR / "docs"

# --- Logs and MLflow ---
# Use system-specific log directory if running in production
if ENV == "production":
    LOGS_DIR = Path("/var/log/hybrid_recommender")
else:
    LOGS_DIR = PROJECT_ROOT / "logs"

MLRUNS_DIR = PROJECT_ROOT / "mlruns"

# --- Ensure directories exist (for reproducibility) ---
# This ensures that even if you clone the repo fresh, the folder structure exists
directories_to_create = [
    RAW_DATA_DIR,
    INTERIM_DATA_DIR,
    PROCESSED_DATA_DIR,
    EXTERNAL_DATA_DIR,
    MODELS_DIR,
    REPORTS_DIR,
    FIGURES_DIR,
    DOCS_DIR,
    LOGS_DIR,
]

for path in directories_to_create:
    path.mkdir(parents=True, exist_ok=True)
