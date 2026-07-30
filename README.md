# BEopt & DView Energy Modeling Workflow

This repository contains documentation, guidelines, and reference steps for setting up building energy simulations in **BEopt** and analyzing detailed time-series output data using **DView**.

---

## 📌 Project Overview

The goal of this workflow is to move from initial building parameters to detailed hourly and sub-hourly energy performance analytics. By combining BEopt's parametric modeling with DView's visual analytics tools, we can evaluate end-use loads, seasonal trends, and peak demand profiles.

---

## 🛠️ Software & Tools

* **BEopt (Building Energy Optimization Tool):** Used to define building characteristics, envelope performance, HVAC systems, and run EnergyPlus simulations.
* **DView:** Used to visualize and analyze time-series output data (hourly/sub-hourly loads, temperatures, and weather profiles).

---

## 🚀 Step-by-Step Workflow

### 1. Building Setup & Simulation (BEopt)
1. Launch **BEopt** and configure your baseline building inputs (geometry, location, insulation, HVAC equipment, and schedules).
2. Run the simulation to generate detailed energy consumption and time-series output files.

### 2. Exporting Data to DView
1. Once the run completes, navigate to the **Output / Results** screen in BEopt.
2. Click the **DView** (or **View Hourly Data**) button on the top toolbar.
3. BEopt will automatically package the simulation outputs (`.csv` files) and launch DView with your project data loaded.

---

## 📊 Key Output Views in DView

Once loaded into DView, data can be analyzed using the following visual tabs:

| View Tab | Primary Use Case |
| :--- | :--- |
| **Hourly / Time Series** | Continuous interactive line graphs of energy loads over time. |
| **Heat Map** | 365-day carpet plots showing peak hours vs. seasonality at a glance. |
| **Profile** | Diurnal (24-hour) average load shapes broken down by month. |
| **Duration Curve** | Values sorted in descending order to analyze peak load requirements. |
| **Statistics & Scatter** | Summary metrics (min, max, mean) and multi-variable correlations. |

---

## 💡 Quick Tips
* **Standalone DView:** You can also launch DView separately to inspect raw `.csv` output files, `.epw` weather files, or TMY3 data.
* **Data Export:** Time-series charts and numerical tables inside DView can be exported or copied into Excel or Python for additional analysis.
