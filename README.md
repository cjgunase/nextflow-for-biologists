# From FASTQ to Nextflow

A beginner-friendly Quarto Book about reproducible bioinformatics with Conda,
containers, Nextflow DSL2, Singularity and SLURM.

The tutorial is paired with the verified
[NGS Workflow Portability Lab](https://github.com/cjgunase/ngs-workflow-portability-lab/tree/v0.1.0).
It uses deterministic synthetic reads and is not a clinical or WGBS pipeline.

The complete beginner-to-industry writing plan and chapter acceptance gates are
defined in [CURRICULUM.md](CURRICULUM.md).

The Nextflow section includes a five-stage executable ladder in
[`examples/nextflow-basics`](examples/nextflow-basics): one value, one file,
many samples, paired FASTQs and a connected two-process workflow. GitHub Actions
runs the examples with a pinned Nextflow version on every change.

The bonus [real-world production WGBS case study](chapters/34-rwe-wgbs-production-case-study.qmd)
shows how the same concepts were applied to nf-core/methylseq on Slurm: runtime
bootstrap failures, container and framework caches, Bismark reference indexing,
a measured 10M-pair pilot, full-sample qualification and a shared-resource
capacity plan for 30 samples.

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

The default build produces the public HTML book. A PDF edition can be added as
a separate release artifact later, after its TeX dependencies and page layout
have been tested independently.

## Scope

The book teaches workflow-engineering concepts through a small paired-end NGS
QC and alignment example. It does not claim clinical validation, production
scale or methylation-aware alignment.
