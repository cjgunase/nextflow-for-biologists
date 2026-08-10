# From FASTQ to Nextflow

A beginner-friendly Quarto Book about reproducible bioinformatics with Conda,
containers, Nextflow DSL2, Singularity and SLURM.

The tutorial is paired with the verified
[NGS Workflow Portability Lab](https://github.com/cjgunase/ngs-workflow-portability-lab/tree/v0.1.0).
It uses deterministic synthetic reads and is not a clinical or WGBS pipeline.

## Read the book

The published site will be available at:

<https://cjgunase.github.io/nextflow-for-biologists/>

## Preview locally

Install [Quarto](https://quarto.org/docs/get-started/) and run:

```bash
quarto preview
```

## Build

```bash
quarto render
```

Generated output is written to `_book/` and is not committed to the source
branch.

## Scope

The book teaches workflow-engineering concepts through a small paired-end NGS
QC and alignment example. It does not claim clinical validation, production
scale or methylation-aware alignment.

