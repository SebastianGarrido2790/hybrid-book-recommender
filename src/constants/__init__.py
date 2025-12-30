"""
This file serves as a safety guard against "Circular Import" errors.
In robust MLOps projects, src/constants is the "Single Source of Truth"
for values that never change (unlike params.yaml, which changes between experiments).
"""

# This re-exports everything from paths.py so other modules
# can do "from src.constants import CONFIG_FILE_PATH"
from src.utils.paths import *
