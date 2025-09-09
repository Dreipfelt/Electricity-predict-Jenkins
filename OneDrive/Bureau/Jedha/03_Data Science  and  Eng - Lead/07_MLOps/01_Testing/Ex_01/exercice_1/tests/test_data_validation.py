import pytest
import pandas as pd
import great_expectations as ge
from app.data_validation import validate_column_types, check_for_missing_values


def test_validate_column_types():
    df = pd.DataFrame({"feature": [1, 2, 3, 4], "target": [2, 4, 6, 8]})
    expected_types = {"feature": "int64", "target": "int64"}
    assert validate_column_types(df, expected_types)


def test_check_for_missing_values():
    df = pd.DataFrame({"feature": [1, 2, 3, 4], "target": [2, 4, 6, None]})
    assert not check_for_missing_values(df)


def validate_data_with_ge(df):
    ge_df = ge.from_pandas(df)
    ge_df.expect_column_values_to_not_be_null("feature")
    ge_df.expect_column_values_to_be_of_type("feature", "int")
    return ge_df.validate()


def test_validate_data_with_ge():
    df = pd.DataFrame({"feature": [1, 2, 3, 4], "target": [2, 4, 6, 8]})
    result = validate_data_with_ge(df)
    assert result["success"] == True
