"""Integration tests for the command-line interface."""

import subprocess
import sys
import pysam

def run_cli(*arguments):
    """Run the CLI using the active Python environment."""
    return subprocess.run(
        [sys.executable, "-m", "ancestryflow.cli", *arguments],
        capture_output=True,
        text=True,
        timeout=10,
    )


def test_cli_help():
    result = run_cli("--help")

    assert result.returncode == 0
    assert "validate-samples" in result.stdout


def test_cli_valid_samples(tmp_path):
    sample_file = tmp_path / "samples.txt"
    sample_file.write_text("donor_01\ndonor_02\n", encoding="utf-8")

    result = run_cli("validate-samples", "--samples", str(sample_file))

    assert result.returncode == 0
    assert result.stdout.strip() == "Validated 2 sample IDs."
    assert result.stderr == ""


def test_cli_duplicate_samples(tmp_path):
    sample_file = tmp_path / "samples.txt"
    sample_file.write_text("donor_01\ndonor_01\n", encoding="utf-8")

    result = run_cli("validate-samples", "--samples", str(sample_file))

    assert result.returncode == 2
    assert "Duplicate sample ID" in result.stderr
    assert result.stdout == ""


def test_cli_missing_file(tmp_path):
    missing_file = tmp_path / "missing.txt"

    result = run_cli("validate-samples", "--samples", str(missing_file))

    assert result.returncode == 2
    assert "missing.txt" in result.stderr
    assert "Traceback" not in result.stderr


def test_cli_requires_samples_argument():
    result = run_cli("validate-samples")

    assert result.returncode == 2
    assert "--samples" in result.stderr

def test_cli_matches_vcf_samples(tmp_path, vcf_path):
    sample_file = tmp_path / "samples.txt"
    sample_file.write_text("donor_01\ndonor_02\n", encoding="utf-8")

    result = run_cli(
        "validate-samples",
        "--samples", str(sample_file),
        "--vcf", str(vcf_path),
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "Matched 2 sample IDs in the VCF header."
    assert result.stderr == ""

def test_cli_rejects_sample_absent_from_vcf(tmp_path, vcf_path):
    sample_file = tmp_path / "samples.txt"
    sample_file.write_text("absent_donor\n", encoding="utf-8")

    result = run_cli(
        "validate-samples",
        "--samples", str(sample_file),
        "--vcf", str(vcf_path),
    )

    assert result.returncode == 2
    assert "Requested samples not found: absent_donor" in result.stderr
    assert result.stdout == ""

def test_cli_reports_missing_vcf(tmp_path):
    sample_file = tmp_path / "samples.txt"
    sample_file.write_text("donor_01\n", encoding="utf-8")

    result = run_cli(
        "validate-samples",
        "--samples", str(sample_file),
        "--vcf", str(tmp_path / "missing.vcf"),
    )

    assert result.returncode == 2
    assert "missing.vcf" in result.stderr
    assert "Traceback" not in result.stderr

def test_cli_extracts_samples(tmp_path, vcf_path):
    sample_file = tmp_path / "samples.txt"
    sample_file.write_text("donor_01\n", encoding="utf-8")
    output = tmp_path / "selected.vcf"

    result = run_cli(
        "extract-samples",
        "--samples", str(sample_file),
        "--vcf", str(vcf_path),
        "--output", str(output),
    )

    assert result.returncode == 0
    assert "Wrote 1 variant records for 1 samples" in result.stdout
    assert result.stderr == ""

    with pysam.VariantFile(str(output)) as selected:
        assert list(selected.header.samples) == ["donor_01"]
        record = next(selected)
        assert record.samples["donor_01"]["GT"] == (0, 0)


def test_cli_extraction_reports_missing_donor(tmp_path, vcf_path):
    sample_file = tmp_path / "samples.txt"
    sample_file.write_text("missing_donor\n", encoding="utf-8")
    output = tmp_path / "selected.vcf"

    result = run_cli(
        "extract-samples",
        "--samples", str(sample_file),
        "--vcf", str(vcf_path),
        "--output", str(output),
    )

    assert result.returncode == 2
    assert "Requested samples not found: missing_donor" in result.stderr
    assert "Traceback" not in result.stderr
    assert result.stdout == ""
    assert not output.exists()
