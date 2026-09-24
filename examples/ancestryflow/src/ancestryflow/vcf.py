"""Utilities for reading variant-file metadata."""

from pathlib import Path

import pysam

from ancestryflow.samples import validate_sample_ids


def read_vcf_samples(path: str | Path) -> list[str]:
    """Read and validate sample IDs in VCF header order.

    This checks sample identifiers, not variant records or genotype quality.
    File-opening and parsing errors propagate to the caller.
    """
    with pysam.VariantFile(str(path)) as variant_file:
        return validate_sample_ids(variant_file.header.samples)
