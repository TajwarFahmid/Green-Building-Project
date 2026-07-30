import os
from pathlib import Path

# Workspace base directories
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"
IMAGES_DIR = BASE_DIR / "images"

for directory in [DATA_DIR, OUTPUT_DIR, LOGS_DIR, IMAGES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Path for BEopt 3.0.1 Executable
BEOPT_EXE_PATH = r"C:\Program Files (x86)\NREL\BEopt_3.0.1\BEopt.exe"

# Base Building Model
DEFAULT_PROJECT_FILE = DATA_DIR / "3bedtwnhome (1).BEopt"