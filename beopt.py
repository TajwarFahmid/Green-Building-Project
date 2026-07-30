import time
import psutil
from pathlib import Path
from pywinauto import Application
import pyautogui
from config import BEOPT_EXE_PATH, DEFAULT_PROJECT_FILE
from logger import logger

def switch_to_options_screen(app):
    """
    Forces BEopt to switch directly to the Options screen.
    """
    logger.info("Switching to Options screen...")
    try:
        main_win = app.top_window()
        main_win.set_focus()
        time.sleep(0.5)
        
        # Method 1: Precise toolbar coordinate click for the Grid icon
        rect = main_win.rectangle()
        # Shifted left from 185 to 165 to hit the Table/Grid icon instead of the Globe icon
        icon_x = rect.left + 165
        icon_y = rect.top + 82
        
        pyautogui.click(icon_x, icon_y)
        time.sleep(1.5)
    except Exception as e:
        logger.warning(f"Toolbar click warning: {e}")

    # Method 2: Menu navigation backup (Screen -> Options)
    logger.info("Sending Screen -> Options menu sequence (Alt+S -> O)...")
    pyautogui.hotkey('alt', 's')
    time.sleep(0.5)
    pyautogui.press('o')
    time.sleep(2)

def launch_and_run_project(project_file_path=DEFAULT_PROJECT_FILE, current_run=1, total_runs=48, run_data=None):
    """
    Launches BEopt, opens base model, creates isolated 'Run X of Y' case,
    switches to Options screen, and triggers simulation execution.
    """
    exe_path = Path(BEOPT_EXE_PATH)
    if not exe_path.exists():
        logger.error(f"BEopt executable NOT found at: {BEOPT_EXE_PATH}")
        raise FileNotFoundError(f"Executable missing: {BEOPT_EXE_PATH}")

    target_project = project_file_path if project_file_path else DEFAULT_PROJECT_FILE
    abs_project_path = str(Path(target_project).resolve())
    
    logger.info("Launching BEopt GUI application...")
    app = Application(backend="win32").start(f'"{exe_path}"')
    time.sleep(6)

    # 1. Open Base Project File (Ctrl + O)
    logger.info(f"Opening base project file: {abs_project_path}...")
    pyautogui.hotkey('ctrl', 'o')
    time.sleep(2)
    pyautogui.write(abs_project_path, interval=0.03)
    time.sleep(1)
    pyautogui.press('enter')
    
    logger.info("Waiting for base model to load...")
    time.sleep(8)

    # 2. Create Isolated Case 'Run X of Y' (Step 6/SOP)
    case_name = f"Run {current_run} of {total_runs}"
    logger.info(f"Creating new case: '{case_name}'...")
    
    pyautogui.hotkey('alt', 'c')
    time.sleep(1)
    pyautogui.press('n')
    time.sleep(2)
    
    pyautogui.write(case_name, interval=0.03)
    time.sleep(1)
    pyautogui.press('enter')
    
    time.sleep(4)  # Wait for case tab to render

    # 3. Switch to Options Screen
    switch_to_options_screen(app)

    # 4. Trigger Simulation Queue (Ctrl + R)
    logger.info("Triggering simulation queue (Ctrl + R)...")
    pyautogui.hotkey('ctrl', 'r')
    time.sleep(3)
    
    # Confirm 'Run' on simulation dialog (Step 10/SOP)
    pyautogui.press('enter')

    return app

def monitor_run_completion(check_interval=5, max_timeout=1800):
    """
    Monitors simulation engine processes until all calculations complete.
    """
    logger.info("Monitoring background EnergyPlus/OpenStudio simulation processes...")
    elapsed = 0
    time.sleep(10)
    
    while elapsed < max_timeout:
        time.sleep(check_interval)
        elapsed += check_interval
        
        active_sims = [
            p.name() for p in psutil.process_iter() 
            if 'energyplus' in p.name().lower() or 'openstudio' in p.name().lower()
        ]
        
        if active_sims:
            logger.info(f"Simulation in progress... Active processes: {active_sims}")
        elif elapsed > 25:
            logger.info("No active EnergyPlus or OpenStudio processes detected. All runs complete!")
            break

    logger.info(f"Finished monitoring queue (Elapsed time: {elapsed} seconds).")