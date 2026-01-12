"""
Project Root Path Setup

Purpose:
- Dynamically add the project root to sys.path.
- Ensures that Python modules in the project can be imported correctly
  without installing the package.
- Commonly used in scripts, tests, or demos that run from subdirectories.
"""

import sys
from pathlib import Path

# ---------------------------
# Determine Project Root
# ---------------------------
PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
"""
PROJECT_ROOT:
- Resolves the absolute path of the file (__file__).
- .parents[1] goes up two levels:
    1. __file__ directory
    2. Parent of that directory (assumed project root)
- Why: makes imports relative to project root possible
"""

# ---------------------------
# Insert Project Root into sys.path
# ---------------------------
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
"""
Why this exists:
- sys.path controls Python module search paths.
- Adding PROJECT_ROOT ensures that scripts can import modules from the project
  without needing installation or PYTHONPATH modifications.
- Insert at index 0 so project modules take priority over installed modules.
"""
