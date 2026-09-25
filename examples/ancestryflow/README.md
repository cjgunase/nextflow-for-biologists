# AncestryFlow

Reusable Python tools for a reference-based ancestry-analysis workflow.

## Current functionality

- Read and validate sample lists.
- Read sample names from VCF headers.
- Check exact, case-sensitive sample matches.
- Run validation through a command-line interface.
- Extract selected donors into plain or BGZF-compressed VCF files.

Ancestry estimation and Nextflow integration are not implemented yet.

## Installation

Requires Python 3.11 or later. From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```
## Extract selected donors

Try the included synthetic example from the project directory:

```bash
demo_dir=$(mktemp -d)

ancestryflow extract-samples \
  --samples examples/samples.txt \
  --vcf examples/tiny.vcf \
  --output "$demo_dir/selected.vcf.gz"

gzip -dc "$demo_dir/selected.vcf.gz"
```

The command writes two variant records for donor_01 and donor_02,
excluding donor_03.

For your own data, replace the sample-list and input-VCF paths.
Output must be a new `.vcf` or `.vcf.gz` file in an existing directory.

Extraction preserves input sample order and all variant rows.
INFO annotations are copied without recalculation; allele frequencies
in those annotations may still describe the original cohort.
The command does not automatically create an index.

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

The current suite contains 37 tests and uses synthetic data.
