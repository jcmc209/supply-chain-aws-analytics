import kagglehub
import shutil
import os

# Download latest version
print("Descargando dataset de Kaggle...")
path = kagglehub.dataset_download("harshsingh2209/supply-chain-analysis")
print(f"Dataset descargado en: {path}")

# Setup paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
TARGET_DIR = os.path.join(REPO_ROOT, "data", "raw")

# Create target directory
os.makedirs(TARGET_DIR, exist_ok=True)

# Find and copy the CSV file
csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
if csv_files:
    source_file = os.path.join(path, csv_files[0])
    target_file = os.path.join(TARGET_DIR, "supply_chain_data.csv")
    shutil.copy2(source_file, target_file)
    print(f"\n[OK] Dataset copiado a: {target_file}")
    print(f"Archivo: {csv_files[0]}")
else:
    print("[ERROR] No se encontro archivo CSV en el dataset descargado")
    print(f"Archivos disponibles: {os.listdir(path)}")
