"""
Forward Fill Logic - Complete Guide
====================================

Forward Fill (ffill) is used to fill missing values with the previous row's value.
This notebook shows how to choose columns, parameters, and best practices.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================================
# COMPLETE FORWARD FILL PARAMETERS
# ============================================================================

"""
df.ffill() / df.fillna(method='ffill')

Main Parameters:
    
1. method='ffill'  
   - Forward fill (propagate last valid observation)
   
2. axis=0 (DEFAULT)
   - axis=0: Fill down rows (most common)
   - axis=1: Fill across columns (rare)
   
3. limit=None (DEFAULT)
   - Maximum number of consecutive NaN values to forward fill
   - limit=1: Only fill 1 NaN, stop if more consecutive
   - limit=5: Fill up to 5 consecutive NaNs
   
4. inplace=False (DEFAULT)
   - inplace=False: Returns new dataframe (safe)
   - inplace=True: Modifies original (be careful!)
   
5. downcast=None (DEFAULT)
   - Downcast data type after filling
   - downcast='integer': Convert float to int if possible
   - downcast='infer': Auto-detect best type

6. fill_value (for .fillna())
   - fill_value=0: Fill with constant value instead of previous row
"""

# ============================================================================
# PRODUCTION LOGIC: SELECT COLUMNS TO FORWARD FILL
# ============================================================================

def forward_fill_selective(df, columns_to_fill=None, limit=None, inplace=False):
    """
    Forward fill only selected columns (PRODUCTION BEST PRACTICE)
    
    Args:
        df: DataFrame
        columns_to_fill: List of column names to fill (None=all)
        limit: Max consecutive NaNs to fill (None=unlimited)
        inplace: Modify original or return new (DEFAULT: False for safety)
    
    Returns:
        DataFrame with forward filled values
    """
    
    if columns_to_fill is None:
        # Fill all columns
        return df.ffill(limit=limit)
    else:
        # Fill only specified columns
        df_copy = df.copy() if not inplace else df
        df_copy[columns_to_fill] = df_copy[columns_to_fill].ffill(limit=limit)
        return df_copy


# ============================================================================
# PRODUCTION LOGIC: IDENTIFY WHICH COLUMNS NEED FILLING
# ============================================================================

def analyze_missing_values(df):
    """
    Analyze which columns have missing values and suggest fill strategy
    """
    
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    
    print("MISSING VALUES ANALYSIS:")
    print("=" * 60)
    
    for col in df.columns:
        if missing[col] > 0:
            print(f"\n{col}")
            print(f"  Missing: {missing[col]} rows ({missing_pct[col]}%)")
            print(f"  Type: {df[col].dtype}")
            print(f"  First non-null: {df[col].first_valid_index()}")
            print(f"  Last non-null: {df[col].last_valid_index()}")
            
            # Suggest strategy
            if missing_pct[col] < 5:
                print(f"  → Recommendation: Fill with ffill (small gap)")
            elif missing_pct[col] < 20:
                print(f"  → Recommendation: ffill with limit=5")
            else:
                print(f"  → Recommendation: Consider interpolate() or drop")


# ============================================================================
# EXAMPLES: DIFFERENT FORWARD FILL STRATEGIES
# ============================================================================

# Example 1: Fill ALL columns
def example_1_fill_all():
    """Forward fill all columns with NaN values"""
    df = pd.DataFrame({
        'price': [100, np.nan, np.nan, 110, 112],
        'volume': [1000, 1100, np.nan, np.nan, 1200],
        'symbol': ['AAPL', np.nan, np.nan, 'AAPL', 'AAPL']
    })
    
    print("\n" + "="*60)
    print("EXAMPLE 1: Fill ALL columns")
    print("="*60)
    print("Before:")
    print(df)
    
    df_filled = df.ffill()
    
    print("\nAfter df.ffill():")
    print(df_filled)


# Example 2: Fill only specific columns
def example_2_fill_specific():
    """Forward fill only price and volume, NOT symbol"""
    df = pd.DataFrame({
        'price': [100, np.nan, np.nan, 110, 112],
        'volume': [1000, 1100, np.nan, np.nan, 1200],
        'symbol': ['AAPL', np.nan, np.nan, 'IBM', 'IBM']
    })
    
    print("\n" + "="*60)
    print("EXAMPLE 2: Fill only SPECIFIC columns")
    print("="*60)
    print("Before:")
    print(df)
    
    # Fill only numeric columns
    df_filled = df.copy()
    df_filled[['price', 'volume']] = df_filled[['price', 'volume']].ffill()
    
    print("\nAfter filling only ['price', 'volume']:")
    print(df_filled)
    print("\n✓ Notice: 'symbol' still has NaN (not filled)")


# Example 3: Forward fill with LIMIT
def example_3_fill_with_limit():
    """Forward fill but stop after N consecutive NaNs"""
    df = pd.DataFrame({
        'price': [100, np.nan, np.nan, np.nan, np.nan, 120],
        'volume': [1000, 1100, 1200, 1300, 1400, 1500]
    })
    
    print("\n" + "="*60)
    print("EXAMPLE 3: Fill with LIMIT (stop after N NaNs)")
    print("="*60)
    print("Before:")
    print(df)
    
    print("\nAfter df.ffill(limit=1): (only fill 1 NaN)")
    print(df.ffill(limit=1))
    
    print("\nAfter df.ffill(limit=2): (only fill 2 consecutive NaNs)")
    print(df.ffill(limit=2))


# Example 4: Forward fill by GROUPS
def example_4_fill_by_group():
    """Forward fill within groups (don't leak between groups)"""
    df = pd.DataFrame({
        'symbol': ['AAPL', 'AAPL', 'AAPL', 'IBM', 'IBM', 'IBM'],
        'price': [100, np.nan, np.nan, 50, np.nan, np.nan],
        'date': pd.date_range('2026-01-01', periods=6)
    })
    
    print("\n" + "="*60)
    print("EXAMPLE 4: Fill by GROUP (critical for multi-stock data!)")
    print("="*60)
    print("Before:")
    print(df)
    
    # ✓ CORRECT: Fill within each stock group
    df_filled = df.copy()
    df_filled['price'] = df_filled.groupby('symbol')['price'].ffill()
    
    print("\nAfter groupby('symbol').ffill():")
    print(df_filled)
    print("\n✓ Notice: AAPL values don't leak into IBM and vice versa")


# Example 5: Forward fill then BACKWARD fill remaining
def example_5_forward_then_backward():
    """Forward fill, then use backward fill for remaining NaNs"""
    df = pd.DataFrame({
        'price': [np.nan, 100, np.nan, np.nan, 110, np.nan],
        'volume': [np.nan, 1000, np.nan, 1200, 1300, np.nan]
    })
    
    print("\n" + "="*60)
    print("EXAMPLE 5: Forward fill THEN backward fill")
    print("="*60)
    print("Before:")
    print(df)
    
    # Forward fill first, then backward fill remaining
    df_filled = df.ffill().bfill()
    
    print("\nAfter df.ffill().bfill():")
    print(df_filled)
    print("\n✓ Forward fills down, backward fills any remaining gaps")


# Example 6: Conditional forward fill
def example_6_conditional_fill():
    """Only forward fill if data type is numeric"""
    df = pd.DataFrame({
        'price': [100, np.nan, np.nan, 110],
        'symbol': ['AAPL', np.nan, np.nan, 'IBM'],
        'date': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-03', '2026-01-04'])
    })
    
    print("\n" + "="*60)
    print("EXAMPLE 6: Conditional fill (numeric only)")
    print("="*60)
    print("Before:")
    print(df)
    
    df_filled = df.copy()
    # Only fill numeric columns
    numeric_cols = df_filled.select_dtypes(include=[np.number]).columns
    df_filled[numeric_cols] = df_filled[numeric_cols].ffill()
    
    print("\nAfter filling only numeric columns:")
    print(df_filled)
    print("\n✓ Symbol stays NaN (not numeric)")


# ============================================================================
# PRODUCTION RECOMMENDATION FOR YOUR DATA
# ============================================================================

def production_recommendation():
    """
    Best practice for financial/market data
    """
    
    print("\n" + "="*60)
    print("PRODUCTION RECOMMENDATION FOR YOUR DATA")
    print("="*60)
    
    code = '''
# For your market snapshots data:

# Step 1: Analyze missing values
missing = df.isnull().sum()
print(f"Columns with missing: {missing[missing > 0]}")

# Step 2: Fill by strategy
df_filled = df.copy()

# Option A: Fill specific numeric columns only
numeric_cols = df.select_dtypes(include=[np.number]).columns
df_filled[numeric_cols] = df_filled[numeric_cols].ffill(limit=3)

# Option B: Fill per stock symbol group (RECOMMENDED for multi-stock)
df_filled = df.groupby('symbol').apply(lambda x: x.ffill(limit=3)).reset_index(drop=True)

# Option C: Forward fill with time limit
# Only fill NaNs if timestamp gap is small
df_filled = df.copy()
df_filled['price'] = df_filled['price'].ffill(limit=1)  # Skip at most 1 data point gap

# Step 3: Verify
print(f"Missing after fill: {df_filled.isnull().sum().sum()}")

# Step 4: Save
df_filled.to_parquet('data/df_filled.parquet', index=False)
'''
    
    print(code)


# ============================================================================
# RUN ALL EXAMPLES
# ============================================================================

if __name__ == "__main__":
    example_1_fill_all()
    example_2_fill_specific()
    example_3_fill_with_limit()
    example_4_fill_by_group()
    example_5_forward_then_backward()
    example_6_conditional_fill()
    production_recommendation()
    
    print("\n" + "="*60)
    print("PARAMETER SUMMARY")
    print("="*60)
    print("""
df.ffill() / df.fillna(method='ffill')

Parameters you can use:
├── axis=0              (fill down rows)
├── limit=N             (max N consecutive fills)
├── inplace=False       (modify in-place or return new)
├── downcast=None       (convert type after filling)
└── fill_value=X        (fill with constant instead)

DataFrame methods:
├── .ffill()            (forward fill)
├── .bfill()            (backward fill)
├── .interpolate()      (linear interpolation)
├── .fillna(value=X)    (fill with constant)
└── .dropna()           (remove NaN)

For your use case:
✓ Use .ffill(limit=3) for market data
✓ Use .groupby('symbol').ffill() for multi-stock
✓ Combine with .bfill() for gaps at start
✓ Always analyze first with .isnull().sum()
    """)
