"""
Centralized logging configuration for the entire project.

Usage:
    from src.utils.logger import get_logger
    logger = get_logger(__name__, headline="main.py")
    logger.info("Started data download...")
"""

import os
import sys
import logging
from datetime import datetime
from typing import Optional
from logging.handlers import RotatingFileHandler

from src.utils.paths import LOGS_DIR

LOG_FILE = LOGS_DIR / "running_logs.log"


def get_logger(
    name: Optional[str] = None, headline: Optional[str] = None
) -> logging.Logger:
    """
    Returns a configured logger with consistent formatting.
    Adds an optional headline section to separate logs per script run.

    Ensures that:
        - Only one handler is attached (prevents duplicates)
        - Log messages include timestamps and module names
        - Works safely across multi-module projects
        - Auto-detects DVC context if no headline is provided

    Args:
        name (Optional[str]): Logger name, typically __name__.
        headline (Optional[str]): Optional headline for visual separation.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if logger is already configured
    if not logger.handlers:
        # 1. Define the format
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s: %(module)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # 2. File Handler (Rotates after 5MB)
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=5_000_000,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

        # 3. Console Handler (Stream to stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.propagate = False

        # --- Context Auto-Detection ---
        # If no headline is passed, check if we are running inside DVC
        if headline is None:
            dvc_stage = os.getenv("DVC_STAGE_NAME")
            if dvc_stage:
                headline = f"DVC Stage: {dvc_stage}"
            elif os.getenv("DVC_ROOT"):
                headline = "DVC repro"

        # Add visual separator for new runs
        if headline:
            headline_text = f"\n{'=' * 20} START: {headline} ({datetime.now():%Y-%m-%d %H:%M:%S}) {'=' * 20}\n"
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(headline_text)

    return logger


def log_spacer():
    """
    Appends a raw newline to the log file to provide visual spacing
    without the log formatter prefix (timestamp/levelname).
    """
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n")
