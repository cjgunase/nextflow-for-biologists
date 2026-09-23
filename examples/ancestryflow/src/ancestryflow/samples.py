"""Validation utilities for sample identifiers."""

from collections.abc import Iterable


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
