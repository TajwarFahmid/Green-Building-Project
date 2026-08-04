import sqlite3
import zipfile
from pathlib import Path

BASE_DIR = Path(r"C:\Users\tajwa\OneDrive\Desktop\BEopt_Automation")
OUTPUT_DIR = BASE_DIR / "doe_runs"

# Inspect active selections across key test runs
for run_num in [1, 4, 7]:
    beopt_path = OUTPUT_DIR / f"Run_{run_num:02d}.BEopt"
    if not beopt_path.exists():
        print(f"File not found: {beopt_path}")
        continue
        
    with zipfile.ZipFile(beopt_path, 'r') as z:
        sqlite_filename = [f for f in z.namelist() if f.endswith('.Project.sqlite')][0]
        z.extract(sqlite_filename, path=BASE_DIR)
    
    db_path = BASE_DIR / sqlite_filename
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"\n--- ACTIVE SELECTIONS IN RUN {run_num:02d} ---")
    cursor.execute("""
        SELECT c.CategoryName, o.OptionName 
        FROM BEoptDesignOption d
        JOIN Option o ON o.OptionGUID = d.OptionGUID
        JOIN Category c ON c.CategoryID = o.CategoryID
        WHERE d.IsSelected = 1 AND d.DesignID = 2
    """)
    rows = cursor.fetchall()
    for cat, opt in rows:
        print(f"  {cat} : {opt}")
        
    conn.close()
    if db_path.exists():
        db_path.unlink()