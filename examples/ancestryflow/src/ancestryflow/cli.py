"""Command-line interface for AncestryFlow."""

import argparse
from pathlib import Path

from ancestryflow.samples import read_sample_ids, validate_sample_selection
from ancestryflow.vcf import read_vcf_samples


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ancestryflow",
        description="Tools for reference-based genetic ancestry analysis.",
    )

    commands = parser.add_subparsers(dest="command", required=True)

    validate = commands.add_parser(
        "validate-samples",
        help="Check sample IDs, optionally against a VCF header.",
    )
    validate.add_argument(
        "--samples",
        type=Path,
        required=True,
        help="Sample-list file without a header.",
    )
    validate.add_argument(
        "--vcf",
        type=Path,
        help="VCF whose header must contain every requested sample.",
    )

    args = parser.parse_args(argv)

    try:
        sample_ids = read_sample_ids(args.samples)

        if args.vcf is not None:
            available_ids = read_vcf_samples(args.vcf)
            sample_ids = validate_sample_selection(
                sample_ids, available_ids
            )
    except (OSError, ValueError) as error:
        parser.error(str(error))

    if args.vcf is None:
        print(f"Validated {len(sample_ids)} sample IDs.")
    else:
        print(f"Matched {len(sample_ids)} sample IDs in the VCF header.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
