import pytest
from app.string_operations import concatenate_with_number


def test_concatenate_with_number():
    result = concatenate_with_number("test")
    assert result == "test_42"

    result_with_custom_number = concatenate_with_number("test", 99)
    assert result_with_custom_number == "test_99"
