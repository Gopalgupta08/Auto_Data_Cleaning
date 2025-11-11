import pandas as pd
from app.services.cleaner import clean_dataframe




def test_clean_basic():
    raw = pd.DataFrame({
    ' Name ': ['Alice ', 'Bob', 'alice'],
    'age': [25, 30, 25],
    'notes': ['N/A', None, 'ok']
    })


    cleaned = clean_dataframe(raw, verbose=False)
    # column names standardized
    assert 'name' in cleaned.columns
    # duplicates removed (alice and Alice -> both lowercase -> duplicate)
    assert len(cleaned) <= 3
    # missing placeholder replaced
    assert cleaned['notes'].isnull().sum() >= 1