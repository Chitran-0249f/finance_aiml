# Production Notebook - Simple Approach

## The Real Pattern (Use This)

For production, just follow this **simple repeating pattern** in ANY notebook:

```python
# ====== PRODUCTION PATTERN ======

# 1. IMPORTS
import pandas as pd
from pathlib import Path

# 2. DEFINE PATHS (always use Path())
PROJECT_ROOT = Path('..')
DATA_DIR = PROJECT_ROOT / 'data'
INPUT_FILE = DATA_DIR / 'df_eda_features.parquet'
OUTPUT_FILE = DATA_DIR / 'df_processed.parquet'

# 3. LOAD DATA
df = pd.read_parquet(INPUT_FILE)
print(f"Loaded: {df.shape}")

# 4. YOUR BUSINESS LOGIC HERE
df_processed = df.copy()
# ... do cleaning, feature engineering, etc ...

# 5. SAVE RESULTS
DATA_DIR.mkdir(parents=True, exist_ok=True)
df_processed.to_parquet(OUTPUT_FILE, index=False)
print(f"✅ Saved to {OUTPUT_FILE}")

# ====== THAT'S LITERALLY IT ======
```

## How to Use This for Production

### Step 1: Create Notebook Manually
- Open VS Code
- Click "Create New Notebook"
- Name it (e.g., `feature_engineering.ipynb`)

### Step 2: Copy the Pattern Above
- Paste the template 5 cells into your notebook
- Customize INPUT/OUTPUT file names
- Add your logic in cell #4

### Step 3: Commit to Git
```bash
git add notebooks/feature_engineering.ipynb
git commit -m "Add feature engineering notebook"
git push
```

### Step 4: Reuse for New Projects
- Copy `feature_engineering.ipynb` to new project
- Update paths if needed
- Done!

## Why This Works in Production

✅ **Simple**: Just 5 steps, no complexity  
✅ **Reusable**: Copy → paste → modify paths  
✅ **Traceable**: Git tracks all changes  
✅ **Debuggable**: Run cells individually  
✅ **Collaborative**: Team uses same notebook  

## Actual Workflow

```
eda.ipynb
  → Save: df_eda_features.parquet

feature_engineering.ipynb  (COPY this pattern)
  → Load: df_eda_features.parquet
  → Save: df_features_engineered.parquet

ml_training.ipynb  (COPY this pattern)
  → Load: df_features_engineered.parquet
  → Save: model.pkl
```

## That's Production. Done.

No fancy notebook generators. No code generation. Just:
1. Create notebook
2. Copy pattern
3. Customize 2 file names
4. Add your logic
5. Run & save
6. Commit to git

The end.
