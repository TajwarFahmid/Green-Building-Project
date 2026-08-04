import sqlite3
import zipfile
import pandas as pd
from pathlib import Path
from config import BASE_DIR, DATA_DIR, OUTPUT_DIR, DEFAULT_PROJECT_FILE
from excel import load_doe_matrix
from logger import logger

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
    s = str(search_str).strip().lower()
    s = s.replace("fiiberglass", "fiberglass")
    if "r-19" in s and "2x4" in s:
        s = s.replace("2x4", "2x6")
    return s

def get_option_guid(cursor, category_name, option_search_str):
    query = """
    SELECT o.OptionGUID, o.OptionName 
    FROM Option o
    JOIN Category c ON c.CategoryID = o.CategoryID
    WHERE LOWER(c.CategoryName) = LOWER(?)
    """
    cursor.execute(query, (category_name,))
    rows = cursor.fetchall()
    
    search_str = clean_search_string(option_search_str)
    search_str_no_dots = search_str.replace(".", "")
    
    for guid, name in rows:
        name_clean = name.strip().lower()
        name_no_dots = name_clean.replace(".", "")
        if search_str == name_clean or search_str in name_clean or search_str_no_dots in name_no_dots or name_clean in search_str:
            return guid
            
    tokens = [t.strip() for t in search_str.replace("low e", "low-e").replace(",", " ").split() if t.strip()]
    best_guid = None
    max_matches = 0
    
    for guid, name in rows:
        name_clean = name.strip().lower()
        match_count = sum(1 for tok in tokens if tok in name_clean)
        if match_count > max_matches:
            max_matches = match_count
            best_guid = guid
            
    if max_matches >= 2:
        return best_guid

    return None

def update_db_selections(db_path, run_row, run_num):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    updates_made = 0

    for excel_col, beopt_cat in EXCEL_TO_BEOPT_CATEGORY.items():
        opt_val = run_row.get(excel_col)
        if pd.isna(opt_val):
            continue

        target_guid = get_option_guid(cursor, beopt_cat, opt_val)
        
        if target_guid:
            cursor.execute("SELECT CategoryID FROM Category WHERE LOWER(CategoryName) = LOWER(?)", (beopt_cat,))
            cat_res = cursor.fetchone()
            if cat_res:
                cat_id = cat_res[0]

                # Deselect current option for active DesignID = 2
                cursor.execute("""
                UPDATE BEoptDesignOption 
                SET IsSelected = 0 
                WHERE DesignID = 2 
                  AND OptionGUID IN (SELECT OptionGUID FROM Option WHERE CategoryID = ?)
                """, (cat_id,))

                # Set new selected option for DesignID = 2
                cursor.execute("""
                UPDATE BEoptDesignOption 
                SET IsSelected = 1 
                WHERE DesignID = 2 
                  AND OptionGUID = ?
                """, (target_guid,))

                updates_made += 1
        else:
            logger.warning(f"[Run {run_num:02d}] No match for '{beopt_cat}' -> '{opt_val}'")

    conn.commit()
    conn.close()
    return updates_made

def generate_doe_runs():
    excel_path = BASE_DIR / "Yash_DOE_RET-Spring2026.xlsx"
    if not excel_path.exists():
        excel_path = DATA_DIR / "Yash_DOE_RET-Spring2026.xlsx"

    df = load_doe_matrix(excel_path)
    logger.info(f"Loaded {len(df)} DOE runs from {excel_path.name}")

    base_beopt = Path(DEFAULT_PROJECT_FILE)
    if not base_beopt.exists():
        base_files = list(DATA_DIR.glob("*.BEopt")) + list(DATA_DIR.glob("*.beopt"))
        if not base_files:
            raise FileNotFoundError("Base .BEopt template file not found in data/ folder!")
        base_beopt = base_files[0]

    OUTPUT_DIR.mkdir(exist_ok=True)

    with zipfile.ZipFile(base_beopt, 'r') as z:
        sqlite_filename = [f for f in z.namelist() if f.endswith('.Project.sqlite')][0]

    for _, row in df.iterrows():
        run_col = df.columns[0]
        run_num = int(row[run_col])
        run_file_name = f"Run_{run_num:02d}.BEopt"
        dest_beopt = OUTPUT_DIR / run_file_name

        temp_db_path = OUTPUT_DIR / sqlite_filename
        with zipfile.ZipFile(base_beopt, 'r') as z:
            z.extract(sqlite_filename, path=OUTPUT_DIR)

        num_updated = update_db_selections(temp_db_path, row, run_num)

        with zipfile.ZipFile(base_beopt, 'r') as zin:
            file_data = {item.filename: zin.read(item.filename) for item in zin.infolist()}

        with open(temp_db_path, 'rb') as f:
            file_data[sqlite_filename] = f.read()

        with zipfile.ZipFile(dest_beopt, 'w', zipfile.ZIP_DEFLATED) as zout:
            for fname, content in file_data.items():
                zout.writestr(fname, content)

        if temp_db_path.exists():
            temp_db_path.unlink()

        logger.info(f"Generated: {run_file_name} ({num_updated} factors updated)")

    logger.info(f"=== Successfully created all {len(df)} .BEopt files in {OUTPUT_DIR} ===")