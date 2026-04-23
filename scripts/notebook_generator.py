"""
SIMPLE PRODUCTION NOTEBOOK PATTERN

This is NOT complex code generation. This is just the PATTERN you repeat.

Copy this into EACH notebook you create:
"""

# =========================================================================
# PASTE THIS INTO YOUR NOTEBOOK (then customize the 3 lines marked)
# =========================================================================

template = """
# 1. IMPORTS
import pandas as pd
from pathlib import Path

# 2. PATHS (CUSTOMIZE THESE 2 LINES)
DATA_DIR = Path('../data')
INPUT_FILE = DATA_DIR / 'df_eda_features.parquet'          # ← Change input name
OUTPUT_FILE = DATA_DIR / 'df_features_engineered.parquet'  # ← Change output name

# 3. LOAD
df = pd.read_parquet(INPUT_FILE)
print(f"Loaded {df.shape}")

# 4. YOUR LOGIC (WRITE YOUR CODE HERE)
df_processed = df.copy()
# ... your feature engineering / cleaning / processing ...

# 5. SAVE
DATA_DIR.mkdir(parents=True, exist_ok=True)
df_processed.to_parquet(OUTPUT_FILE, index=False)
print(f"✅ Saved {OUTPUT_FILE}")
"""

# =========================================================================
# That's it. Seriously.
# =========================================================================

if __name__ == "__main__":
    print("📌 PRODUCTION NOTEBOOK PATTERN")
    print("=" * 70)
    print(template)
    print("=" * 70)
    print("\n✅ Just copy ↑↑↑ into your notebook")
    print("✅ Change 2 file names")
    print("✅ Add your logic")
    print("✅ Run & save")
    print("✅ Done!")
