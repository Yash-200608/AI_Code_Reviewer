import sys
from pathlib import Path

# Flat layout: make analyzer.py / scorer.py / app.py importable from tests
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
