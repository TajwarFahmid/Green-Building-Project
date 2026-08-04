import sqlite3
import zipfile
import pandas as pd
from pathlib import Path

# Base Setup
BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

excel_path = BASE_DIR / "Yash_DOE_RET-Spring2026.xlsx"
if not excel_path.exists():
    excel_path = DATA_DIR / "Yash_DOE_RET-Spring2026.xlsx"

base_files = list(DATA_DIR.glob("*.BEopt")) + list(DATA_DIR.glob("*.beopt"))
if not base_files:
    base_files = list(BASE_DIR.glob("*.BEopt")) + list(BASE_DIR.glob("*.beopt"))

BASE_BEOPT = base_files[0]

EXCEL_TO_BEOPT_CATEGORY = {
    "Ceilings: Batt Insulation\nCeiling > unfinished attic": "Unfinished Attic",
    "Vertical Walls: Batt Insulation\nWalls > wood stud": "Wood Stud",
    "Roof: Ext Finish/Color\nCeiling roof > roof material": "Roof Material",
    "Available Option in Beopt\nAbove Grade Walls: Ext Finish/Color": "Exterior Finish",
    "Window: Frame Type\nWindows & doors > \nWindow": "Windows",
    "Roof: Radiant Barrier\nCeiling roof > radiant barrier": "Radiant Barrier",
    "Water Heater Type\nWater heating > water heater": "Water Heater",
    "Space Conditioning > Duct\nDUCT": "Ducts",
    "HVAC System\nSpace conditioning > \nAir source Heat Pump": "Air Source Heat Pump",
    "Ceiling Fan": "Ceiling Fan"
}

def clean_search_string(search_str):
    s = str(search_str).strip().lower().replace("fiiberglass", "fiberglass")
    if "r-19" in s and "2x4" in s:
        s = s.replace("2x4", "2x6")
    return s

def get_option_guid(cursor, category_name, option_search_str):
    cursor.execute("""
    SELECT o.OptionGUID, o.OptionName 
    FROM Option o JOIN Category c ON c.CategoryID = o.CategoryID
    WHERE LOWER(c.CategoryName) = LOWER(?)
    """, (category_name,))
    rows = cursor.fetchall()
    
    search_str = clean_search_string(option_search_str)
    search_str_no_dots = search_str.replace(".", "")
    
    for guid, name in rows:
        name_clean = name.strip().lower()
        if search_str == name_clean or search_str in name_clean or search_str_no_dots in name_clean.replace(".", ""):
            return guid
            
    tokens = [t.strip() for t in search_str.replace("low e", "low-e").replace(",", " ").split() if t.strip()]
    best_guid, max_matches = None, 0
    for guid, name in rows:
        match_count = sum(1 for tok in tokens if tok in name.strip().lower())
        if match_count > max_matches:
            max_matches = match_count
            best_guid = guid
            
    return best_guid if max_matches >= 2 else None

def build_master():
    df = pd.read_excel(excel_path)
    df['# Run'] = pd.to_numeric(df['# Run'], errors='coerce')
    df = df[df['# Run'].notna() & (df['# Run'] <= 48)].copy()
    
    print(f"Loaded {len(df)} active DOE runs.")

    with zipfile.ZipFile(BASE_BEOPT, 'r') as z:
        sqlite_filename = [f for f in z.namelist() if f.endswith('.Project.sqlite')][0]
        z.extract(sqlite_filename, path=OUTPUT_DIR)

    temp_db_path = OUTPUT_DIR / sqlite_filename
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()

    # Update selections directly in BEoptDesignOption table
    for idx, row in df.iterrows():
        run_num = int(row['# Run'])
        for excel_col, beopt_cat in EXCEL_TO_BEOPT_CATEGORY.items():
            opt_val = row.get(excel_col)
            if pd.isna(opt_val): continue
            target_guid = get_option_guid(cursor, beopt_cat, opt_val)
            if target_guid:
                cursor.execute("SELECT CategoryID FROM Category WHERE LOWER(CategoryName) = LOWER(?)", (beopt_cat,))
                cat_res = cursor.fetchone()
                if cat_res:
                    cursor.execute("UPDATE BEoptDesignOption SET IsSelected = 0 WHERE OptionGUID IN (SELECT OptionGUID FROM Option WHERE CategoryID = ?)", (cat_res[0],))
                    cursor.execute("UPDATE BEoptDesignOption SET IsSelected = 1 WHERE OptionGUID = ?", (target_guid,))

    conn.commit()
    conn.close()

    master_beopt = OUTPUT_DIR / "Master_DOE_48_Runs.BEopt"
    with zipfile.ZipFile(BASE_BEOPT, 'r') as zin:
        file_data = {item.filename: zin.read(item.filename) for item in zin.infolist()}

    with open(temp_db_path, 'rb') as f:
        file_data[sqlite_filename] = f.read()

    with zipfile.ZipFile(master_beopt, 'w', zipfile.ZIP_DEFLATED) as zout:
        for fname, content in file_data.items():
            zout.writestr(fname, content)

    if temp_db_path.exists():
        temp_db_path.unlink()

    print(f"Master file successfully created: {master_beopt}")

if __name__ == "__main__":
    build_master()