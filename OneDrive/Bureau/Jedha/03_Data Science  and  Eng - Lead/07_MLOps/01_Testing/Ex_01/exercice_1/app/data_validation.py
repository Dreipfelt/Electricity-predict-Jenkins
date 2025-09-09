import pandas as pd


def validate_column_types(df, expected_types):
    return df.dtypes.equals(pd.Series(expected_types))


def check_for_missing_values(df):
    return df.isnull().sum().sum() == 0
