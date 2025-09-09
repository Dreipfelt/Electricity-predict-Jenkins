import pytest
from app.set_operations import add_to_set, remove_negatives, sum_of_set


@pytest.fixture
def sample_set():
    return {1, 2, 3, -4, -5, 6}


def test_add_to_set(sample_set):
    updated_set = add_to_set(sample_set, 7)
    assert 7 in updated_set


def test_remove_negatives(sample_set):
    updated_set = remove_negatives(sample_set)
    assert all(x >= 0 for x in updated_set)


def test_sum_of_set(sample_set):
    total = sum_of_set(remove_negatives(sample_set))
    assert total == sum({1, 2, 3, 6})  # Expected sum of non-negative values
