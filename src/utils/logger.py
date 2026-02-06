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


_HEADLINE_WRITTEN = False


def get_logger(
    name: Optional[str] = None, headline: Optional[str] = None
) -> logging.Logger:
    """
    Returns a configured logger with consistent formatting.
    Adds an optional headline section to separate logs per script run.

    Ensures that:
        - Handlers are attached to the root logger (child loggers inherit)
        - Only one set of handlers is attached (prevents duplicates)
        - Log messages include timestamps and module names
        - Auto-detects DVC context if no headline is provided
        - Headlines are written only ONCE per process execution

    Args:
        name (Optional[str]): Logger name, typically __name__.
        headline (Optional[str]): Optional headline for visual separation.

    Returns:
        logging.Logger: Configured logger instance.
    """
    global _HEADLINE_WRITTEN

    # 1. Always check/configure the ROOT logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Check existing handlers to avoid duplicates
    has_file_handler = False
    has_console_handler = False

    # Normalize target log path for comparison
    target_log_path = os.path.normpath(str(LOG_FILE.resolve()))

    for handler in root_logger.handlers:
        if isinstance(handler, RotatingFileHandler):
            # Check if it writes to our specific LOG_FILE
            if (
                hasattr(handler, "baseFilename")
                and os.path.normpath(handler.baseFilename) == target_log_path
            ):
                has_file_handler = True
        elif isinstance(handler, logging.StreamHandler):
            # rudimentary check for console handler
            has_console_handler = True

    # Define the format
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(module)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if not has_file_handler:
        # File Handler (Rotates after 5MB)
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=5_000_000,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    if not has_console_handler:
        # Console Handler (Stream to stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    # 2. Get the specific logger requested
    logger = logging.getLogger(name)

    # 3. Headline logic (Single execution per process)
    if not _HEADLINE_WRITTEN:
        # Auto-detection if no headline provided
        if headline is None:
            dvc_stage = os.getenv("DVC_STAGE_NAME")
            if dvc_stage:
                headline = f"DVC Stage: {dvc_stage}"
            elif os.getenv("DVC_ROOT"):
                headline = "DVC repro"

        # Write the headline if we have one (explicit or detected)
        if headline:
            _HEADLINE_WRITTEN = True
            headline_text = f"\n{'=' * 20} START: {headline} ({datetime.now():%Y-%m-%d %H:%M:%S}) {'=' * 20}\n"
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(headline_text)

    return logger


def log_spacer() -> None:
    """
    Appends a raw newline to the log file to provide visual spacing
    without the log formatter prefix (timestamp/levelname).
    """
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n")
