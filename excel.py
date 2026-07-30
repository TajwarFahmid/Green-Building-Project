import pandas as pd
from pathlib import Path
from logger import logger

def load_doe_matrix(excel_path: Path, sheet_name: str = "Sheet3") -> pd.DataFrame:
    """
    Reads the full 13-column DOE spreadsheet and cleans valid run rows.
    """
    logger.info(f"Reading 13-column DOE matrix file: {excel_path} (Sheet: {sheet_name})")
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    
    # Identify Run column
    run_col = df.columns[0]
    clean_df = df[pd.to_numeric(df[run_col], errors='coerce').notnull()].copy()
    clean_df[run_col] = clean_df[run_col].astype(int)
    
    # Filter to only the 13 valid columns
    clean_df = clean_df.iloc[:, :13]
    
    logger.info(f"Successfully loaded {len(clean_df)} experimental runs with all 10 input factors.")
    return clean_df