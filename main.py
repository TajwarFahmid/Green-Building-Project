# main.py
from build_doe_files import generate_doe_runs
from logger import logger

def main():
    logger.info("=== Starting BEopt DOE Generation Pipeline ===")
    generate_doe_runs()
    logger.info("=== Pipeline Run Complete! ===")

if __name__ == "__main__":
    main()