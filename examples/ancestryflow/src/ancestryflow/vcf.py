"""Utilities for reading variant-file metadata."""
from collections.abc import Iterable
from pathlib import Path

import pysam

from ancestryflow.samples import (
    validate_sample_ids,
    validate_sample_selection,
)


def read_vcf_samples(path: str | Path) -> list[str]:
    """Read and validate sample IDs in VCF header order.

    This checks sample identifiers, not variant records or genotype quality.
    File-opening and parsing errors propagate to the caller.
    """
    with pysam.VariantFile(str(path)) as variant_file:
        return validate_sample_ids(variant_file.header.samples)

def extract_vcf_samples(
    input_path: str | Path,
    output_path: str | Path,
    sample_ids: Iterable[str],
) -> int:
    """Extract sample columns and return the number of variant records written.

    Keeps all variant records and preserves input sample order.
    INFO annotations are copied without recalculation.
    Output must be a new, uncompressed .vcf file.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    if output_path.suffix != ".vcf":
        raise ValueError("Output must have a .vcf extension.")

    if output_path.exists():
        raise FileExistsError(f"Output already exists: {output_path}")

    with pysam.VariantFile(str(input_path)) as source:
        requested = validate_sample_selection(
            sample_ids,
            source.header.samples,
        )
        source.subset_samples(requested)

        count = 0
        with pysam.VariantFile(
            str(output_path),
            "w",
            header=source.header,
        ) as destination:
            for record in source:
                destination.write(record)
                count += 1

    return count
