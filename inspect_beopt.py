import sqlite3
import zipfile
from pathlib import Path

DATA_DIR = Path(r"C:\Users\tajwa\OneDrive\Desktop\BEopt_Automation\data")
beopt_files = list(DATA_DIR.glob("*.BEopt")) + list(DATA_DIR.glob("*.beopt"))

target_file = beopt_files[0]
print(f"Reading archive: {target_file.name}\n")

with zipfile.ZipFile(target_file, "r") as z:
    # Extract the .Project.sqlite file temporarily to read its tables
    sqlite_filename = [f for f in z.namelist() if f.endswith(".Project.sqlite")][0]
    z.extract(sqlite_filename, path=DATA_DIR)
    
db_path = DATA_DIR / sqlite_filename

print(f"Extracted SQLite DB: {sqlite_filename}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all table names inside the project database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]

print("\n--- TABLES FOUND IN BEOPT PROJECT ---")
for t in tables:
    print(f"  - {t}")

# Check tables that likely store options/parameters
print("\n--- SEARCHING FOR OPTIONS / PARAMETERS ---")
for table in tables:
    if any(k in table.lower() for k in ["option", "parameter", "input", "category", "case", "construction"]):
        print(f"\n[ Table: {table} ]")
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"Columns: {columns}")
        
        # Preview first few rows
        cursor.execute(f"SELECT * FROM {table} LIMIT 5;")
        rows = cursor.fetchall()
        for r in rows:
            print(f"  Row: {r}")

conn.close()
