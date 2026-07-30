import pandas as pd
from pathlib import Path
from config import DATA_DIR, OUTPUT_DIR, DEFAULT_PROJECT_FILE
from excel import load_doe_matrix
from beopt import launch_and_run_project, monitor_run_completion
from logger import logger

def main():
    excel_filename = "Yash_DOE_RET-Spring2026.xlsx"
    excel_path = DATA_DIR / excel_filename

    if not excel_path.exists():
        logger.error(f"Excel file not found at {excel_path}. Place it in data/ folder.")
        return

    # 1. Read DOE Matrix
    logger.info("Step 1: Reading DOE Matrix...")
    doe_df = load_doe_matrix(excel_path)
    total_runs = len(doe_df)

    # 2. Automate BEopt Case Creation and Run Triggering
    current_run = 1  # For starting the batch
    logger.info(f"Step 2: Automating BEopt Case Generation: 'Run {current_run} of {total_runs}'...")
    launch_and_run_project(DEFAULT_PROJECT_FILE, current_run=current_run, total_runs=total_runs)

    # 3. Monitor Calculations
    logger.info("Step 3: Monitoring EnergyPlus Simulation Engine...")
    monitor_run_completion(check_interval=5, max_timeout=1800)

    # 4. Save Final Compiled Matrix
    output_summary = OUTPUT_DIR / "automated_simulation_results.csv"
    doe_df.to_csv(output_summary, index=False)
    logger.info(f"Step 4: Processed dataset saved to {output_summary}")

    logger.info("=== BEopt Automation Completed Successfully ===")

if __name__ == "__main__":
    main()