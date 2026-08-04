import subprocess
import sqlite3
import zipfile
import pandas as pd
from pathlib import Path

BASE_DIR = Path(r"C:\Users\tajwa\OneDrive\Desktop\BEopt_Automation")
DOE_DIR = BASE_DIR / "doe_runs"
EXCEL_PATH = BASE_DIR / "Yash_DOE_RET-Spring2026.xlsx"
BEOPT_EXE = r"C:\Program Files (x86)\NREL\BEopt_3.0.1\BEopt.exe"

def run_simulations_and_update_excel():
    df = pd.read_excel(EXCEL_PATH, sheet_name="Sheet3")
    
    # 0.15 rate = $0.10 kWh + $0.05 delivery/fees
    RATE = 0.15 
    kwh_col = df.columns[11]
    cost_col = df.columns[12]

    print("Starting automated execution of all DOE simulation runs...\n")

    for idx, row in df.iterrows():
        run_num = row['# Run']
        if pd.isna(run_num) or run_num > 48:
            continue
            
        run_file = DOE_DIR / f"Run_{int(run_num):02d}.BEopt"
        if not run_file.exists():
            continue

        print(f"Executing Simulation: Run_{int(run_num):02d}.BEopt...")
        
        # 1. Trigger BEopt headless runner CLI
        subprocess.run([BEOPT_EXE, "/run", str(run_file)], check=False)

        # 2. Extract results from internal SQLite database
        with zipfile.ZipFile(run_file, 'r') as z:
            sqlite_file = [f for f in z.namelist() if f.endswith('.Project.sqlite')][0]
            z.extract(sqlite_file, path=DOE_DIR)
            
        db_path = DOE_DIR / sqlite_file
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Query site electricity result
        cursor.execute("SELECT TotalValue FROM OutputResult WHERE EnergyType = 'Electricity' AND ResultType = 'Site Energy'")
        result = cursor.fetchone()
        conn.close()
        
        if db_path.exists():
            db_path.unlink()

        # 3. Write values to DataFrame
        if result:
            kwh_val = float(result[0])
            df.at[idx, kwh_col] = kwh_val
            df.at[idx, cost_col] = round(kwh_val * RATE, 4)
            print(f"  -> Run {int(run_num):02d} Complete: {kwh_val:.2f} kWh | ${kwh_val * RATE:.2f}")

    # Save final completed Excel sheet
    output_excel = BASE_DIR / "Yash_DOE_RET-Spring2026_Completed.xlsx"
    with pd.ExcelWriter(output_excel) as writer:
        df.to_excel(writer, sheet_name="Sheet3", index=False)
        
    print(f"\nAll calculations complete! Final spreadsheet saved to: {output_excel}")

if __name__ == "__main__":
    run_simulations_and_update_excel()