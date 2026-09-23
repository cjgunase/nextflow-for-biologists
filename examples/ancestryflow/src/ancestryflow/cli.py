"""Command-line interface for AncestryFlow."""

import argparse
from pathlib import Path

from ancestryflow.samples import read_sample_ids


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ancestryflow",
        description="Tools for reference-based genetic ancestry analysis.",
    )

    commands = parser.add_subparsers(dest="command", required=True)

    validate = commands.add_parser(
        "validate-samples",
        help="Check a file containing one sample ID per line.",
    )
    validate.add_argument(
        "--samples",
        type=Path,
        required=True,
        help="Sample-list file without a header.",
    )

    args = parser.parse_args(argv)

    try:
        sample_ids = read_sample_ids(args.samples)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print(f"Validated {len(sample_ids)} sample IDs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
