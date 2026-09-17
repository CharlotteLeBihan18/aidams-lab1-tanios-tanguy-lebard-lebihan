# Global Iron and Steel Plants — Geospatial Analysis

A data analysis lab that explores the location, capacity, and ownership of steel plants worldwide using the Global Energy Monitor dataset. We clean and map the data, link each plant to a local economic exposure score (LitPop), aggregate results by company, and present everything in an interactive Streamlit dashboard.

**Live dashboard →** https://aidams-lab1-tanios-tanguy-lebard-lebihan.streamlit.app

---

## Team

| Name | Student ID |
|---|---|
| Charlotte Le Bihan | B00818310 |
| Ines Lebard | B00820964 |
| Camille Tanguy | B00821659 |
| Oceane Tanios | B00822694 |

---

## What's in this repo

| File | What it does |
|---|---|
| `lab_1.ipynb` | Main analysis notebook (Parts 1–6 + Bonus) |
| `app.py` | Streamlit dashboard |
| `requirements.txt` | Python dependencies |
| `litpop/` | LitPop exposure data for China, India, Japan |
| `*.csv` | Pre-computed outputs used by the dashboard |

---

## Prerequisites

- Python 3.12 or later
- The steel plants Excel file from [Global Iron and Steel Tracker](https://globalenergymonitor.org/projects/global-iron-steel-tracker) placed in the project folder
- The `litpop/` folder with the three `.hdf5` files (provided on Moodle)

---

## Run locally

```bash
# 1. Clone the repo
git clone https://github.com/CharlotteLeBihan18/aidams-lab1-tanios-tanguy-lebard-lebihan.git
cd aidams-lab1-tanios-tanguy-lebard-lebihan

# 2. Create a virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install openpyxl h5py tables  # needed to read the raw data files

# 3. Open the notebook
jupyter notebook lab_1.ipynb

# 4. Run the dashboard
streamlit run app.py
```

---

## Data sources

- **Steel plants:** Global Energy Monitor — [Global Iron and Steel Tracker](https://globalenergymonitor.org/projects/global-iron-steel-tracker), June 2026
- **LitPop:** ETH Zurich Research Collection — socio-economic exposure data at 300 arc-second resolution
