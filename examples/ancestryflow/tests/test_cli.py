"""Integration tests for the command-line interface."""

import subprocess
import sys


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
