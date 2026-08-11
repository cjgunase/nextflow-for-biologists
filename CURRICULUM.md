# From FASTQ to Nextflow — complete curriculum plan

This document is the writing and verification contract for the book. It defines
the complete beginner-to-industry learning path before the remaining chapters
are written.

## Audience and outcome

The reader is a biologist who understands sequencing at a conceptual level but
may never have used a terminal, Git, Conda, Docker, an HPC scheduler or a
workflow language.

By the end, the reader should be able to:

- work safely and deliberately in a Unix-like terminal;
- explain the difference between the operating-system, module, Conda,
  container, workflow and scheduler layers;
- use Git and GitHub for traceable, collaborative development;
- create versioned environments and deterministic public test fixtures;
- validate an analysis manually before automating it;
- write defensive Bash scripts with logs and meaningful exit codes;
- build, inspect, publish and run an OCI container image;
- implement and configure a Nextflow DSL2 pipeline;
- execute processes locally, in Singularity and through SLURM;
- test success, expected failure, caching and cross-runtime equivalence;
- build useful CI/CD without confusing deployment with scientific validation;
- publish a semantic release with checksums, provenance and reviewable
  evidence; and
- discuss security, privacy, regulated boundaries and limitations honestly.

The reader is **not** expected to become a systems administrator, DevOps
engineer or clinical-validation specialist. The goal is enough engineering
fluency to contribute safely and communicate effectively in an industry
bioinformatics team.

## Teaching contract for every practical chapter

Every practical chapter will contain these sections in this order:

1. **Why a biologist should care** — the scientific or team consequence.
2. **Engineering objective** — the technical capability being developed.
3. **Mental model** — the concept in plain language before syntax.
4. **Before you type** — starting directory, required files and assumptions.
5. **Build it** — small, numbered command or code blocks.
6. **Read the command** — explanation of each new flag and expression.
7. **Expected output** — a short example, not pages of terminal noise.
8. **Verification checkpoint** — an objective command and pass condition.
9. **What changed on disk** — new and modified files made explicit.
10. **Common failure** — at least one authentic failure and diagnosis.
11. **Commit checkpoint** — a suggested Git commit when appropriate.
12. **Try it yourself** — one safe exercise plus a solution or hint.
13. **What to remember** — three to five durable takeaways.
14. **Interview grill** — ten questions that test explanation and judgment,
    not memorized product slogans.

From Chapter 4 onward, examples assume that AI may draft much of the syntax.
The learner must still be able to explain the execution model, inspect every
assumption, predict failure modes, verify outputs and reject unsafe or
scientifically invalid suggestions. Interview questions therefore emphasize
scenarios, tradeoffs and debugging evidence over command recall.

Commands will never silently assume a working directory. Destructive commands
will be avoided or fenced with explicit target checks. Site-specific DLDCC
settings will be labeled and separated from portable concepts.

## The project readers will build

The teaching project is a small paired-end NGS QC and alignment workflow:

```text
paired FASTQ
├── raw FastQC
└── paired Trim Galore
    ├── post-trim FastQC
    └── Bowtie2 alignment → SAMtools sort
        └── index, quickcheck, flagstat and idxstats
```

It uses deterministic synthetic reads derived from public GRCh38 chromosome
22. It contains no patient data and is not a clinical, WGBS or production-scale
pipeline.

The verified companion implementation is pinned to:

<https://github.com/cjgunase/ngs-workflow-portability-lab/tree/v0.1.0>

## Part I — Orientation and safe command-line work

### Chapter 1 — The whole shebang

**Question:** What problem does each technology solve?

Introduces tools, pipelines, package environments, container images, workflow
engines, executors, schedulers, version control and automation as separate
layers. Ends with a diagram readers can explain in their own words.

**Artifact:** annotated architecture diagram.  
**Pass condition:** correctly assign four scenarios to Conda/container,
Nextflow or SLURM.

### Chapter 2 — The terminal, files and paths

Teach the prompt, command/argument/option structure, quoting, tab completion,
working directories, absolute and relative paths, hidden files, wildcards,
standard output/error, pipes, redirection and exit codes.

Core commands: `pwd`, `ls`, `cd`, `mkdir`, `touch`, `cp`, `mv`, `head`, `tail`,
`less`, `wc`, `find`, `rg`, `which`/`command -v`, `echo` and `printf`.

**Artifact:** a small practice directory tree.
**Pass condition:** locate a file, count its lines and explain `$?` without
changing unrelated files.

### Chapter 3 — Set up the learning workstation

Install or verify Git, Conda or Miniforge, Java, Nextflow, Docker where
available, Quarto for the tutorial and a text editor. Explain why Docker is
normally unavailable on managed HPC systems and why Singularity is introduced
later.

Cover `command -v`, `--version`, architecture and operating-system checks.
Provide macOS, Linux and HPC decision paths without mixing their commands.

**Artifact:** `setup-check.txt`.
**Pass condition:** every required command is either verified or explicitly
marked “provided later by the cluster/container.”

### Chapter 4 — HPC mental model: login nodes, compute nodes and storage

Explain shared clusters, SSH, login versus compute nodes, modules, partitions,
accounts, CPU/memory/time requests, home/project/scratch storage and quotas.
Teach `module purge`, `module load`, `module list`, `sinfo`, `squeue`, `sacct`,
`df`, `du` and `quota` as concepts with DLDCC examples.

Explicitly separate modules from Conda: modules alter cluster-provided software
and environment variables; Conda activates a user-controlled package
environment. They can coexist and conflict through `PATH`.

**Artifact:** `hpc-inventory.txt`.
**Pass condition:** identify the Java, Conda, Singularity, scheduler and storage
layers active in a session.

### Chapter 5 — Cloud execution mental model: AWS and transferable concepts

Explain how cloud execution differs from both a workstation and a fixed HPC
cluster. Introduce accounts, regions, availability zones, IAM identities and
roles, virtual networks, object storage, container registries, compute services,
managed batch schedulers, autoscaling, logs, encryption, data transfer and the
shared-responsibility model.

Use AWS as the concrete vocabulary: S3, ECR, EC2, AWS Batch, CloudWatch, IAM,
KMS and VPC. Map the concepts briefly to Azure and Google Cloud so readers learn
the architecture rather than memorizing one vendor's product catalog. Explain
Nextflow execution through AWS Batch and the role of a platform such as Seqera
without requiring readers to create a billable cloud account.

Emphasize cost as an engineering constraint: instance/runtime cost, storage
classes, requests, logs, NAT gateways, idle resources and data egress. Cover
least privilege, temporary credentials, protected biomedical data, regional
placement, auditability, budgets and teardown. Require readers to challenge
AI-generated infrastructure and IAM policies rather than deploying them
blindly.

**Artifact:** `cloud-architecture-review.md` containing a service map, trust
boundaries, cost model, data lifecycle and deployment decision record.
**Pass condition:** explain how one sample moves from object storage through a
containerized batch task to validated outputs, including identity, networking,
logging, cost and failure evidence.

## Part II — Git, GitHub and collaborative engineering

### Chapter 6 — Git mental model and first repository

Explain working tree, staging area, commit, branch, repository, remote and
`.gitignore`. Teach `git init`, `git status`, `git diff`, `git add`,
`git commit`, `git log`, `git show` and `git ls-files`.

Emphasize that Git records selected changes; it is not cloud storage, automatic
backup or a place for raw patient data and large generated results.

**Artifact:** first local repository with two meaningful commits.  
**Pass condition:** clean working tree and ability to explain what each commit
contains.

### Chapter 7 — A safe daily Git workflow

Teach small commits, useful messages, branches, switching, comparing revisions,
restoring a single accidental edit safely and understanding merge conflicts.
Introduce `git switch`, `git branch`, `git diff --staged`, `git log --oneline
--graph`, `git restore` and merge concepts.

Include a warning against copying destructive reset commands from the internet.

**Artifact:** a short feature branch merged locally.  
**Pass condition:** main contains the feature and the history remains readable.

### Chapter 8 — GitHub, issues, pull requests and code review

Explain local Git versus GitHub; SSH keys versus HTTPS credentials; clone,
fetch, pull and push; forks; issues; pull requests; review comments; branch
protection; and why peer review matters in scientific software.

Commands include `git clone`, `git remote -v`, `git fetch`, `git pull --ff-only`
and `git push -u origin <branch>`.

**Artifact:** a public practice repository and one reviewed pull request.  
**Pass condition:** remote branch and local branch point to the intended commit.

### Chapter 9 — Versions, tags, changelogs and releases

Teach semantic versioning as a communication contract, annotated versus
lightweight tags, immutable commit IDs, release notes, changelogs and when a
bioinformatics result should record a commit or image digest instead of only a
friendly version.

Commands include `git tag -a`, `git tag -n`, `git show`, `git push origin
<tag>` and `git ls-remote --tags`.

**Artifact:** a `v0.1.0` practice release.  
**Pass condition:** local and remote tag resolve to the intended commit.

## Part III — Environments, data and a trusted analytical baseline

### Chapter 10 — Dependencies, Conda and channels

Explain package, dependency, environment, solver, channel, Bioconda,
conda-forge, channel priority, pinning, lock/explicit files and why `base`
should not become a dumping ground.

Contrast Conda with `pip`, modules and containers without claiming one is
universally superior.

**Artifact:** readable `environment.yml`.  
**Pass condition:** reader can explain why channel order and version pins
affect reproducibility.

### Chapter 11 — Build and audit the tool environment

Create an environment from the tracked specification, activate it and verify
FastQC, Trim Galore, Cutadapt, Bowtie2, SAMtools, Seqtk and supporting tools.
Teach `conda env create`, `conda activate`, `conda list`, `conda env export`,
`conda deactivate` and executable-path inspection.

Use the real libmamba/CUDA solve failure to teach diagnosis and the value of
small changes rather than repeatedly mutating a trusted environment.

**Artifact:** tool-version and package-resolution records.  
**Pass condition:** versions and executable paths come from the intended
environment.

### Chapter 12 — Deterministic test data, provenance and checksums

Explain fixtures, public reference data, deterministic random seeds,
confidentiality boundaries, checksums and provenance records. Generate 100,000
paired reads from GRCh38 chromosome 22 and build the Bowtie2 index.

Commands include `curl`, `gzip`, `sha256sum`/`shasum`, `wgsim`, `wc` and
`bowtie2-build`/`bowtie2-inspect`.

**Artifact:** reproducible fixture script and checksum manifests.  
**Pass condition:** 400,000 FASTQ lines per mate, 100,000 read pairs, matching
SHA-256 values and a readable `chr22` index.

### Chapter 13 — Validate the workflow manually

Run raw FastQC, paired Trim Galore, post-trim FastQC, Bowtie2, SAMtools sort,
index, quickcheck, flagstat and idxstats one step at a time. Explain FASTQ, BAM,
BAI, coordinate sorting, pairing and key QC summaries at the level needed to
validate engineering behavior.

Use the real all-zero trimmed-output and insert-size failures to show that a
successful command is not automatically a scientifically sensible result.

**Artifact:** trusted baseline outputs and interpretation notes.  
**Pass condition:** nonempty paired trimmed reads, valid indexed BAM and
expected mapping summaries.

## Part IV — Scripting, configuration, logging and tests

### Chapter 14 — Turn the baseline into strict Bash

Teach shebangs, variables, quoting, command continuation, functions and
`set -euo pipefail` one behavior at a time. Explain why pipelines can hide an
upstream failure without `pipefail`.

**Artifact:** `run_manual.sh`.  
**Pass condition:** script syntax check, successful run and outputs equivalent
to the manual baseline.

### Chapter 15 — Defensive scripts, parameters and logs

Add input checks, directory creation, read-only defaults, usage messages,
parameter validation, temporary-file handling, cleanup traps, timestamps and
separate logs. Explain configuration versus hard-coded site paths and secrets
that must never enter Git.

**Artifact:** a parameterized, rerunnable script.  
**Pass condition:** clear help output, safe missing-input failure and no partial
final output presented as success.

### Chapter 16 — Testing bioinformatics software

Distinguish syntax tests, unit tests, integration tests, smoke tests, regression
tests, negative tests, scientific acceptance criteria and full validation.
Teach exit-code assertions, file existence/nonemptiness, `samtools quickcheck`,
summary comparisons and checksum limitations.

**Artifact:** a small smoke-test script and negative-input test.  
**Pass condition:** correct input passes; deliberate missing or corrupt input
fails for the intended reason.

## Part V — Containerization and portable software

### Chapter 17 — Container mental model

Explain host, image, container, layer, registry, repository, tag, digest,
bind mount, working directory, environment and process. Contrast virtual
machines and containers. Explain portability benefits and kernel/architecture
limits.

**Artifact:** annotated container architecture diagram.  
**Pass condition:** explain image versus container and tag versus digest.

### Chapter 18 — Write a Dockerfile deliberately

Teach `FROM`, `LABEL`, `COPY`, `RUN`, `ARG`, `ENV`, `USER`, `WORKDIR`, build
context, `.dockerignore`, layer caching, least privilege and why file ordering
affects rebuild time. Build from the pinned Conda specification.

Commands include `docker build`, `docker image ls`, `docker run`, `docker
inspect` and `docker image history` where Docker is available.

**Artifact:** Dockerfile and `.dockerignore`.  
**Pass condition:** required tools run inside the image without relying on the
host Conda environment.

### Chapter 19 — Registries, image CI and immutable evidence

Use GitHub Actions to build and publish the OCI image to GHCR. Explain workflow
YAML, triggers, jobs, steps, action pinning, permissions, secrets, cache,
artifacts and provenance. Record both a friendly tag and immutable digest.

Clarify that “the image built” is not equivalent to “the analytical pipeline
is validated.”

**Artifact:** passing container-build workflow and image digest.  
**Pass condition:** clean pull and tool smoke checks from the published image.

### Chapter 20 — Singularity/Apptainer on HPC

Explain why HPC sites commonly disallow Docker daemons, how OCI images become
SIF files, clean environments, bind mounts, caches and project storage. Teach
`singularity pull`, `singularity inspect` and `singularity exec --cleanenv`.

Use the real PATH, missing `ps` and home-quota failures as case studies.

**Artifact:** checksummed SIF and container smoke-test record.  
**Pass condition:** all required tools and `ps` execute inside the SIF from a
clean environment.

## Part VI — Nextflow DSL2 from first process to complete pipeline

### Chapter 21 — Nextflow mental model

Teach process, task, channel, value, queue channel, tuple, path staging,
workflow block, operator, executor, work directory, cache and publish directory.
Relate each concept to the already trusted manual workflow.

**Artifact:** annotated dataflow diagram.  
**Pass condition:** reader predicts which processes may run concurrently.

### Chapter 22 — First DSL2 workflow and task anatomy

Run a minimal hello workflow, then implement raw FastQC. Explain
`nextflow.enable.dsl=2`, `process`, `input`, `output`, `script`, interpolation,
`tag`, `cpus` and `publishDir`.

Inspect `.command.sh`, `.command.run`, `.command.log`, `.command.out`,
`.command.err` and `.exitcode`.

**Artifact:** first real `FASTQC_RAW` process.  
**Pass condition:** two FastQC reports and an exit code of zero.

### Chapter 23 — Channels, tuples and paired files

Build paired-read channels with `channel.fromFilePairs`, metadata tuples,
`path`, `val`, `map`, `collect`, `view`, emits and channel reuse. Explain data
shape explicitly before introducing compact syntax.

**Artifact:** channel-shape notebook/diagram and paired-input workflow.  
**Pass condition:** sample identifier and R1/R2 association remain correct.

### Chapter 24 — Port the complete pipeline

Add `TRIM_GALORE`, `FASTQC_TRIMMED`, `ALIGN_SORT` and `BAM_QC`. Explain process
contracts, branching, synchronization, pipes inside a process and why
`set -o pipefail` still matters there.

**Artifact:** five-process `main.nf`.  
**Pass condition:** all five processes succeed and publish the complete expected
result set.

### Chapter 25 — Parameters, configuration and runtime profiles

Move portable parameters and site policy into appropriate configuration. Teach
`params`, `nextflow.config`, profile selection, `process` selectors, labels,
CPUs, memory, time, container settings, Conda cache and configuration precedence.

Create `conda_local`, `singularity_local` and `slurm_singularity` profiles.

**Artifact:** portable configuration with one clearly labeled DLDCC profile.  
**Pass condition:** `nextflow config -profile ...` resolves each runtime as
intended without embedding secrets.

### Chapter 26 — Reports, failures, caching and debugging

Teach `-resume`, task hashes, invalidated cache, trace, report, timeline, DAG,
work-directory inspection, `.nextflow.log`, error strategies and resource
retry concepts. Deliberately test a missing input and then prove five-task cache
reuse.

**Artifact:** negative-test log, cached trace and execution reports.  
**Pass condition:** missing input exits nonzero before analysis; unchanged rerun
shows all five tasks as cached.

## Part VII — Schedulers, CI/CD and reproducible delivery

### Chapter 27 — Execute Nextflow through SLURM

Explain Nextflow as scheduler client, executor settings, queue/account,
resources, scheduler latency and generated wrappers. Compare local execution
with five scheduled jobs and inspect `#SBATCH` directives plus
`singularity exec` proof.

**Artifact:** SLURM trace and wrapper evidence.  
**Pass condition:** five completed SLURM tasks used the expected partition,
account, resources and SIF.

### Chapter 28 — CI/CD for a bioinformatics repository

Define continuous integration, continuous delivery and deployment precisely.
Design a layered GitHub Actions system:

- lint/format and syntax checks on every pull request;
- small fixture smoke test where licensing/resources allow;
- container build and tool checks;
- documentation render and link checks;
- tagged image/release publication; and
- protected deployment environments for anything consequential.

Teach matrices, caches, artifacts, statuses, required checks, least-privilege
permissions and why secrets must be scoped. Discuss when HPC execution needs a
self-hosted runner and why that introduces security/maintenance obligations.

**Artifact:** CI workflow plus Quarto Pages delivery workflow.  
**Pass condition:** deliberate documentation or syntax defect fails the
appropriate check; corrected commit passes.

### Chapter 29 — Reproducibility and cross-runtime equivalence

Compare Conda and container results using checksums, headers, alignment records,
flagstat and idxstats. Explain byte identity, functional equivalence, numerical
tolerance and provenance metadata.

Use the real BAM-header difference to demonstrate how an apparently failed hash
comparison can reveal legitimate provenance rather than changed alignments.

**Artifact:** cross-runtime comparison report.  
**Pass condition:** claims match the evidence: identical headerless records and
summaries, not falsely “byte-identical BAMs.”

### Chapter 30 — Release, provenance and application-ready evidence

Perform clean-room setup, repository audit, README walkthrough, checksums,
release notes, semantic tag, source archive and evidence matrix. Explain SBOM,
software citation, licenses, DOIs/archival services and image digests as next
steps.

**Artifact:** tagged `v0.1.0` project release.  
**Pass condition:** a reviewer can move from each claim to a committed artifact
and reproduce the small test path.

## Part VIII — Working safely and effectively in industry

### Chapter 31 — Security, privacy and regulated boundaries

Introduce least privilege, secrets, dependency/image scanning, trusted base
images, updates, licenses, PHI/PII, encryption, access control, audit trails,
retention and incident escalation. Explain the distinction between an
engineering demonstration and clinical analytical/software validation.

No security theater: readers learn when to stop and involve security, platform,
quality or regulatory specialists.

**Artifact:** project threat/limitations checklist.  
**Pass condition:** repository contains no secrets or sensitive data and its
scope statement is accurate.

### Chapter 32 — Team practices: documentation, review and operations

Teach issue templates, definition of done, code review etiquette, decision
records, runbooks, ownership, change control, deprecation, observability,
incident reports and blameless postmortems. Explain how biologists contribute
domain acceptance criteria and how engineers expose assumptions for review.

**Artifact:** issue, pull-request and incident/postmortem templates.  
**Pass condition:** another reader can understand a change, reproduce its test
and identify its owner and rollback path.

### Chapter 33 — Where to go next

Introduce modular Nextflow organization, nf-core, schema validation, workflow
testing frameworks, MultiQC, reference management, cloud executors,
infrastructure as code, batch/metadata systems and monitoring as next-stage
topics—not as skills earned automatically by this book.

**Artifact:** individualized 30/60/90-day learning plan.  
**Pass condition:** learner can distinguish current demonstrated capability
from the next capability they intend to build.

## Appendices

### Appendix A — Glossary

Plain-language definitions with cross-links to the first chapter where each
term is used.

### Appendix B — Troubleshooting by evidence

Each case uses: symptom → observation → hypothesis → test → root cause → fix →
prevention. Cases come from the actual project rather than invented errors.

### Appendix C — Command reference

Commands grouped by purpose, with warnings and links back to the explanatory
chapter. It will not present context-free destructive recipes.

### Appendix D — Git and GitHub recipes

Safe daily operations, branch synchronization, conflict orientation, tag
verification and recovery boundaries.

### Appendix E — YAML, configuration and regular-expression primer

The minimal syntax needed to read Conda environments, GitHub Actions and
Nextflow configuration without turning the book into a language manual.

### Appendix F — File formats and QC interpretation

FASTQ, FASTA, SAM/BAM/BAI, logs, checksums and the specific FastQC/SAMtools
metrics used in the teaching fixture.

### Appendix G — Installation and platform matrix

macOS, Linux, Windows/WSL and institutional HPC paths, including what cannot be
made identical across those systems.

### Appendix H — Further learning and primary documentation

Curated official documentation and next-step training resources.

## Chapter review gates

A chapter is complete only when all applicable gates pass:

- commands have been recreated by the author from the stated starting point;
- expected output is short, accurate and captured from a real run;
- every new term is defined before use or linked to the glossary;
- code blocks are copyable and do not contain prompt characters;
- paths and site-specific values are clearly labeled;
- failure examples state the actual root cause rather than guessing;
- verification commands have objective pass/fail conditions;
- scientific and engineering claims remain within the evidence;
- Quarto renders with no warnings introduced by the chapter;
- page is visually reviewed at desktop and narrow widths; and
- source change is committed with a meaningful message.

## Proposed chapter-by-chapter writing order

The reader order and writing order will be the same. We will complete and verify
one chapter before beginning the next:

1. revise Chapter 1 against this curriculum;
2. write Chapters 2–5 and verify the local, HPC and cloud foundations;
3. write Chapters 6–9 using this tutorial repository as the live Git example;
4. write Chapters 10–16 from the verified manual workflow evidence;
5. write Chapters 17–20 from the image and Singularity evidence;
6. write Chapters 21–26 by reconstructing the DSL2 port incrementally;
7. write Chapters 27–30 from SLURM, CI, comparison and release evidence;
8. write Chapters 31–33 and finish the appendices; and
9. perform a clean beginner walkthrough of the entire published book.
