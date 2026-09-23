"""Tests for sample identifier validation."""
import pytest
from ancestryflow.samples import read_sample_ids, validate_sample_ids


def test_preserves_sample_order():
    samples = ["donor_02", "donor_01"]
    assert validate_sample_ids(samples) == samples


def test_accepts_a_generator():
    samples = (f"donor_{i}" for i in range(3))
    assert validate_sample_ids(samples) == ["donor_0", "donor_1", "donor_2"]


@pytest.mark.parametrize(
    "samples, message",
    [
        ([], "At least one sample ID"),
        ([""], "is empty"),
        ([" donor_01"], "contains whitespace"),
        (["donor 01"], "contains whitespace"),
        (["donor_01\n"], "contains whitespace"),
        (["donor_01", "donor_01"], "Duplicate sample ID"),
    ],
)
def test_rejects_invalid_ids(samples, message):
    with pytest.raises(ValueError, match=message):
        validate_sample_ids(samples)


@pytest.mark.parametrize(
    "samples",
    ["donor_01", b"donor_01", [123], ["donor_01", None]],
)
def test_rejects_incorrect_types(samples):
    with pytest.raises(TypeError):
        validate_sample_ids(samples)

def test_reads_sample_file(tmp_path):
    sample_file = tmp_path / "samples.txt"
    sample_file.write_text("donor_02\ndonor_01\n", encoding="utf-8")

    assert read_sample_ids(sample_file) == ["donor_02", "donor_01"]


def test_rejects_blank_line_in_sample_file(tmp_path):
    sample_file = tmp_path / "samples.txt"
    sample_file.write_text("donor_01\n\ndonor_02\n", encoding="utf-8")

    with pytest.raises(ValueError, match="is empty"):
        read_sample_ids(sample_file)


def test_reports_missing_sample_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_sample_ids(tmp_path / "missing.txt")
