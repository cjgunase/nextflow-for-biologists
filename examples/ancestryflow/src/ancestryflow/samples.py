"""Validation utilities for sample identifiers."""

from collections.abc import Iterable
from pathlib import Path

def read_sample_ids(path: str | Path) -> list[str]:
    """Read and validate a file containing one sample ID per line.

    Blank lines, duplicate IDs and whitespace within IDs are rejected.
    File access errors propagate to the caller.
    """
    text = Path(path).read_text(encoding="utf-8-sig")
    return validate_sample_ids(text.splitlines())

def validate_sample_ids(sample_ids: Iterable[str]) -> list[str]:
    """Return sample IDs in their original order after validation.

    Raises:
        TypeError: If the input is a single string or contains nonstrings.
        ValueError: If IDs are empty, contain whitespace, repeat, or are absent.
    """
    if isinstance(sample_ids, (str, bytes)):
        raise TypeError("Provide a collection of sample IDs, not a single string.")

    validated: list[str] = []
    seen: set[str] = set()

    for position, sample_id in enumerate(sample_ids, start=1):
        if not isinstance(sample_id, str):
            raise TypeError(f"Sample ID at position {position} must be a string.")

        if not sample_id:
            raise ValueError(f"Sample ID at position {position} is empty.")

        if any(character.isspace() for character in sample_id):
            raise ValueError(f"Sample ID contains whitespace: {sample_id!r}")

        if sample_id in seen:
            raise ValueError(f"Duplicate sample ID: {sample_id!r}")

        seen.add(sample_id)
        validated.append(sample_id)

    if not validated:
        raise ValueError("At least one sample ID is required.")

    return validated
