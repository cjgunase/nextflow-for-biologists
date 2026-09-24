# AncestryFlow: library foundation

Companion source for the book's AncestryFlow case study. This checkpoint implements sample-ID validation, text-file input VCF-header reading and a command-line interface. It does not perform ancestry inference.

From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest -q
ancestryflow validate-samples --samples examples/samples.txt
```

Expected: 31 passing tests. Sample names are synthetic. No genotype data is included.

To check names against your own VCF header, add `--vcf /path/to/cohort.vcf.gz`. This checks sample presence only.
