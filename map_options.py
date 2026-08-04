import sqlite3
import zipfile
from pathlib import Path

DATA_DIR = Path(r"C:\Users\tajwa\OneDrive\Desktop\BEopt_Automation\data")
beopt_files = list(DATA_DIR.glob("*.BEopt")) + list(DATA_DIR.glob("*.beopt"))

target_file = beopt_files[0]

with zipfile.ZipFile(target_file, "r") as z:
    sqlite_filename = [f for f in z.namelist() if f.endswith(".Project.sqlite")][0]
    z.extract(sqlite_filename, path=DATA_DIR)

db_path = DATA_DIR / sqlite_filename
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query options linked to categories
query = """
SELECT c.CategoryID, c.CategoryName, o.OptionGUID, o.OptionName
FROM Category c
JOIN Option o ON c.CategoryID = o.CategoryID
ORDER BY c.CategoryName, o.OptionName;
"""

cursor.execute(query)
rows = cursor.fetchall()

print(f"{'CATEGORY':<30} | {'OPTION NAME':<40} | {'OPTION GUID'}")
print("-" * 110)

# Filter preview for relevant factor keywords
keywords = ["wall", "ceiling", "attic", "roof", "water", "duct", "hvac", "barrier", "finish", "insulation"]
for cat_id, cat_name, opt_guid, opt_name in rows:
    if any(k in cat_name.lower() or k in opt_name.lower() for k in keywords):
        print(f"{cat_name:<30} | {opt_name:<40} | {opt_guid}")

conn.close()