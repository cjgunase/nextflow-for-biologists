# AncestryFlow: library foundation

Companion source for the book's AncestryFlow case study. This checkpoint implements sample-ID validation and text-file input. It does not perform ancestry inference.

From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest -q
```

Expected: 15 passing tests. Sample names are synthetic. No genotype data is included.
