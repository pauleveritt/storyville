"""Pytest configuration and fixtures."""

import sys
from pathlib import Path

# Add examples directory to sys.path so tests can import from it
examples_path = Path(__file__).parent.parent / "examples"
if str(examples_path) not in sys.path:
    sys.path.insert(0, str(examples_path.parent))
