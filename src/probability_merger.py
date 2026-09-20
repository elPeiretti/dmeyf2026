import pandas as pd
import glob
import os

# --- Configuration ---
INPUT_DIR = "/home/elpeiretti/maestria/subidas/todas"
OUTPUT_FILE = "merged_probs.csv"
OUTPUT_AVG_FILE = "final_prob.txt"
# ---------------------

txt_files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.txt")))

if not txt_files:
    raise FileNotFoundError(f"No .txt files found in '{INPUT_DIR}'")

dfs = []
for path in txt_files:
    file_name = os.path.splitext(os.path.basename(path))[0]
    df = pd.read_csv(path, sep="\t", dtype={"numero_de_cliente": str})
    df = df.rename(columns={"prob": file_name})   # no prefix → column = file name
    dfs.append(df)

merged = dfs[0]
for df in dfs[1:]:
    merged = merged.merge(df, on="numero_de_cliente", how="outer")

# All columns except the ID are prob columns
prob_cols = [c for c in merged.columns if c != "numero_de_cliente"]
merged["prob"] = merged[prob_cols].mean(axis=1)

merged.to_csv(OUTPUT_FILE, index=False)
merged[["numero_de_cliente", "prob"]].to_csv(OUTPUT_AVG_FILE, index=False, sep="\t")
print(f"Done! {len(merged):,} rows → {OUTPUT_FILE}")
print(f"Slim avg file  → {OUTPUT_AVG_FILE}")