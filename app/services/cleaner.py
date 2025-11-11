import pandas as pd
import numpy as np

def clean_dataframe(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    df = df.copy()

    # log helper
    def log(msg):
        if verbose:
            print(f"[INFO] {msg}")

    # 1. standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    log("Standardized column names.")

    # 2. remove duplicates
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        df.drop_duplicates(inplace=True)
        log(f"Removed {dup_count} duplicate rows.")

    # 3. trim and lowercase string columns
    for col in df.select_dtypes(include='object'):
        df[col] = df[col].astype(str).str.strip().str.lower()
    log("Standardized string columns.")

    # 4. replace placeholder missing values
    placeholders = ['n/a', 'na', '--', '-', 'none', 'null', '', 'nan']
    df.replace(placeholders, np.nan, inplace=True)

    # 5. report missing
    null_report = df.isnull().sum()
    null_report = null_report[null_report > 0]
    if not null_report.empty:
        log(f"Missing values:\n{null_report}")

    # 6. constant cols
    constant_cols = [col for col in df.columns if df[col].nunique() == 1]
    if constant_cols:
        log(f"Constant columns: {constant_cols}")

    # 7. high-cardinality categorical
    high_card_cols = [col for col in df.select_dtypes(include='object') if df[col].nunique() > 100]
    if high_card_cols:
        log(f"High-cardinality columns: {high_card_cols}")

    # 8. outliers
    num_cols = df.select_dtypes(include=np.number).columns
    out_report = {}
    for col in num_cols:
        q1, q3 = df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = df[(df[col] < lower) | (df[col] > upper)].shape[0]
        if outliers > 0:
            out_report[col] = outliers
    if out_report:
        log(f"Outliers detected: {out_report}")

    # 9. convert low-unique object columns to category
    for col in df.select_dtypes(include='object'):
        if df[col].nunique() < len(df) * 0.05:
            df[col] = df[col].astype('category')
    log("Converted suitable columns to category.")

    log("Cleaning complete.")
    return df
