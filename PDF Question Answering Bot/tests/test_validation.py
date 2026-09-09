# tests/test_validation.py

import pytest

from app.utils.validation import (
    validate_chunk_parameters,
    validate_top_k,
)


def test_validate_chunk_parameters_accepts_valid_values():
    assert validate_chunk_parameters(1000, 150) is True


def test_validate_chunk_parameters_rejects_invalid_chunk_size():
    with pytest.raises(ValueError):
        validate_chunk_parameters(0, 100)


def test_validate_chunk_parameters_rejects_negative_overlap():
    with pytest.raises(ValueError):
        validate_chunk_parameters(1000, -1)


def test_validate_chunk_parameters_rejects_overlap_equal_to_size():
    with pytest.raises(ValueError):
        validate_chunk_parameters(1000, 1000)


def test_validate_top_k_accepts_valid_value():
    assert validate_top_k(5) == 5


def test_validate_top_k_rejects_zero():
    with pytest.raises(ValueError):
        validate_top_k(0)


def test_validate_top_k_rejects_negative_value():
    with pytest.raises(ValueError):
        validate_top_k(-5)