# BEopt Automation

## Overview

This project automates the process of running multiple Building Energy Optimization (BEopt) simulations by reading predefined input values from an Excel spreadsheet and automatically entering them into the BEopt graphical interface.

The automation significantly reduces the time required to manually configure simulation parameters, minimizes human error, and enables large-scale Design of Experiments (DOE) studies.

---

## Features

- Reads simulation parameters from an Excel spreadsheet
- Automatically inputs values into the BEopt interface
- Supports batch execution of multiple simulation runs
- Easily expandable to include additional variables
- Reduces repetitive manual work
- Improves consistency across simulation runs

---

## Technologies Used

- Python 3
- Pandas
- PyAutoGUI
- OpenPyXL
- Pillow
- OpenCV (optional for image recognition)
- BEopt

---

## Project Structure

```
BEopt-Automation/
│
├── data/
│   ├── DOE_Input.xlsx
│   └── screenshots/
│
├── automation.py
├── config.py
├── requirements.txt
├── README.md
└── images/
```

---

## How It Works

1. The program reads an Excel file containing simulation variables.
2. Each row represents one BEopt simulation.
3. The automation script:
   - Opens the appropriate fields in BEopt
   - Enters the corresponding values
   - Saves the project
   - Starts the simulation (optional)
4. The process repeats until every row has been completed.

---

## Example Excel Format

| Run | Wall R | Roof R | Window U | HVAC | Infiltration | ... |
|-----|--------|---------|-----------|------|--------------|-----|
| 1 | 13 | 30 | 0.35 | Heat Pump | 3 ACH50 | |
| 2 | 19 | 38 | 0.30 | Furnace | 5 ACH50 | |
| ... | ... | ... | ... | ... | ... | |

Each row represents one complete simulation.

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/BEopt-Automation.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

1. Open BEopt.
2. Load the desired building model.
3. Place the Excel input file inside the `data/` directory.
4. Update any screen coordinates or image templates if necessary.
5. Run:

```bash
python automation.py
```

The script will automatically process each simulation in sequence.

---

## Customization

The project can easily be extended to:

- Add additional BEopt input variables
- Automate larger Design of Experiments (DOE)
- Support different building templates
- Incorporate image recognition for improved robustness
- Schedule simulations for overnight execution

---

## Requirements

- Windows operating system
- BEopt installed
- Python 3.10+
- Screen resolution matching recorded automation coordinates (if coordinate-based automation is used)

---

## Future Improvements

- Dynamic image recognition instead of fixed coordinates
- Automatic extraction of simulation results
- Logging and error recovery
- Progress tracking
- Parallel execution support
- GUI for selecting input files
- Automatic generation of summary reports

---

## Motivation

Manually configuring hundreds of BEopt simulations is repetitive and time-consuming. This project streamlines the workflow by automating data entry, allowing researchers to focus on analyzing simulation results rather than repetitive setup tasks.

---

## Author

**Tajwar Fahmid**

M.S. Applied Statistics and Data Science  
The University of Texas at Arlington

---

## License

This project is intended for academic and research purposes. Feel free to modify and extend it for your own projects.
