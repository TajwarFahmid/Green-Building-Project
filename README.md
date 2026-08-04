# BEopt DOE Simulation & Automation Pipeline

An automated Python-based framework designed to map Design of Experiments (DOE) parameters from Excel matrix files, inject selections directly into **BEopt 3.0+** SQLite project structures, and streamline batch simulation workflows.

---

## 🛠️ Tech Stack & Prerequisites

* **OS:** Windows 10/11
* **Python:** 3.10+
* **Core Libraries:** `pandas`, `openpyxl`, `sqlite3` (built-in), `pywinauto`, `psutil`
* **Building Energy Modeling Tool:** [NREL BEopt 3.0.1+](https://beopt.nrel.gov/)
* **Simulation Engine:** EnergyPlus / OpenStudio

---

## 📁 Project Structure

```text
BEopt_Automation/
├── data/
│   ├── 3bedtwnhome (1).BEopt          # Base template BEopt model file
│   └── Yash_DOE_RET-Spring2026.xlsx   # Master DOE parameter matrix
├── doe_runs/                          # Generated individual .BEopt files (Run_01 to Run_48)
├── output/                            # Destination for batch summary exports & logs
├── beopt_mappings.py                  # Dictionary mapping Excel options to BEopt DB categories
├── build_doe_files.py                 # Core script: Injects Excel matrix into 48 .BEopt files
├── build_master.py                    # Script for multi-case single-file generation
├── config.py                          # Environment paths and execution constants
├── README.md                          # Project documentation
└── requirements.txt                   # Dependency manifest
