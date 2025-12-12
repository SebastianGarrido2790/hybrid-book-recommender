"""
Centralized logging configuration for the entire project.

Usage:
    from src.utils.logger import get_logger
    logger = get_logger(__name__, headline="data_ingestion.py")
    logger.info("Started data download...")
"""

import logging
import sys
from datetime import datetime
from typing import Optional
from logging.handlers import RotatingFileHandler

from src.utils.paths import LOGS_DIR

LOG_FILE = LOGS_DIR / "running_logs.log"


def get_logger(name: str = __name__, headline: Optional[str] = None) -> logging.Logger:
    """
    Returns a configured logger with consistent formatting.
    Adds an optional headline section to separate logs per script run.

    Ensures that:
        - Only one handler is attached (prevents duplicates)
        - Log messages include timestamps and module names
        - Works safely across multi-module projects

    Args:
        name (str): Logger name, typically __name__.
        headline (Optional[str]): Optional headline for visual separation (e.g., script name).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if logger is already configured
    if not logger.handlers:
        # Define the format
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s: %(module)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # 1. File Handler (Rotates after 5MB, keeps 5 backups)
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=5_000_000,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

        # 2. Console Handler (Stream to stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # Do not propagate up to the root logger to avoid double printing
        logger.propagate = False

        # Add a visual separator in the log file for new runs
        if headline:
            headline_text = f"\n{'=' * 20} START: {headline} ({datetime.now():%Y-%m-%d %H:%M:%S}) {'=' * 20}\n"
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(headline_text)

    return logger
