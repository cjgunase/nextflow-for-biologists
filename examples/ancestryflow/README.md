# AncestryFlow

Reusable Python tools for a reference-based ancestry-analysis workflow.

## Current functionality

- Read and validate sample lists.
- Read sample names from VCF headers.
- Check exact, case-sensitive sample matches.
- Run validation through a command-line interface.

Ancestry estimation and Nextflow integration are not implemented yet.

## Installation

Requires Python 3.11 or later. From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

The development extra installs the testing dependencies.

## Validate a sample list

```bash
ancestryflow validate-samples --samples examples/samples.txt
```

Expected output:

```text
Validated 2 sample IDs.
```

Sample lists contain one exact ID per line, without a header.
Blank lines, duplicate IDs and whitespace within IDs are rejected.

## Check samples against a VCF

Replace the paths below with your own files:

```bash
ancestryflow validate-samples \
  --samples /path/to/samples.txt \
  --vcf /path/to/cohort.vcf.gz
```

Plain VCF and BGZF-compressed VCF inputs are tested.
This command checks sample presence, not genotype quality or genome assembly.

Exit status 0 indicates success. Input errors reported by the CLI use status 2.

## Development

Run the automated tests:

```bash
python -m pytest -q
```

List discovered tests without running them:

```bash
python -m pytest --collect-only -q
```

The current suite contains 31 tests and uses synthetic data.
