import pandas as pd
import numpy as np
import os

# Config
RANDOM_SEED = 1234
np.random.seed(RANDOM_SEED)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))      # etl/scripts
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))  # repo root

INPUT_PATH = os.path.join(REPO_ROOT, "data", "raw", "supply_chain_data.csv")
OUTPUT_PATH = os.path.join(REPO_ROOT, "data", "dirty", "supply_chain_data_dirty.csv")

# Load
df = pd.read_csv(INPUT_PATH)

# Helper to select random rows
def pick_rows(frac):
    return df.sample(frac=frac, random_state=np.random.randint(0, 1_000_000)).index

# 1) Inject NULL (3% shipping costs)
idx_null_shipping = pick_rows(0.03)
df.loc[idx_null_shipping, "Shipping costs"] = np.nan

# 2) Inject NULL (2% manufacturing costs)
idx_null_mfg = pick_rows(0.02)
df.loc[idx_null_mfg, "Manufacturing costs"] = np.nan

# 3) Invalid defect rates (1% > 100)
idx_invalid_defects = pick_rows(0.01)
df.loc[idx_invalid_defects, "Defect rates"] = 150

# 4) Negative shipping costs (1%)
idx_negative_ship_cost = pick_rows(0.01)
df.loc[idx_negative_ship_cost, "Shipping costs"] = -abs(df.loc[idx_negative_ship_cost, "Shipping costs"].fillna(10))

# 5) Messy categorical values (2% transportation modes)
if "Transportation modes" in df.columns:
    idx_modes = pick_rows(0.02)
    df.loc[idx_modes, "Transportation modes"] = df.loc[idx_modes, "Transportation modes"].astype(str).str.lower()

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Save
df.to_csv(OUTPUT_PATH, index=False)

print("Dirty dataset created:")
print(f"- Input : {INPUT_PATH}")
print(f"- Output: {OUTPUT_PATH}")
print("\nInjected issues summary:")
print(f"- NULL Shipping costs: {len(idx_null_shipping)} rows")
print(f"- NULL Manufacturing costs: {len(idx_null_mfg)} rows")
print(f"- Invalid Defect rates (>100): {len(idx_invalid_defects)} rows")
print(f"- Negative Shipping costs: {len(idx_negative_ship_cost)} rows")
print(f"- Messy Transportation modes: {len(idx_modes) if 'Transportation modes' in df.columns else 0} rows")
