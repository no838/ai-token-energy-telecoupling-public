# Compute-constrained geography of AI data-centre electricity and carbon burdens

This repository provides the public derived tables, figure-source data, schema
records, claim-evidence ledgers and reconstruction scripts associated with the
manuscript:

**Compute-constrained geography of AI data-centre electricity and carbon burdens**

Repository URL:

```text
https://github.com/no838/ai-token-energy-telecoupling-public
```

The repository is designed to support reviewer inspection of the
manuscript-facing burden-geography analysis. It contains derived source tables,
figure-facing inputs, reconstruction scripts, claim-evidence matrices and
documentation that define the public-data evidence class used in the
manuscript.

The release is not a raw-data redistribution archive. Raw third-party datasets
remain governed by their original licences, access conditions and
source-provider terms. Where redistribution of raw records is restricted or
unnecessary for audit, the repository provides public identifiers, derived
tables, source-data schemas and reconstruction inputs.

## What this repository supports

This repository supports the following review and reproducibility tasks:

1. Inspecting manuscript-facing figure source tables for the demand-origin,
   compute-host, electricity, carbon, fossil-exposure and China-context
   modules.
2. Reconstructing figure-facing analytic outputs from included derived source
   tables.
3. Auditing the claim-evidence alignment used to separate demand-origin
   signals, constrained compute-host allocation, electricity-burden envelopes,
   location-based direct-carbon envelopes, fossil-exposure motifs and national
   infrastructure-context layers.
4. Checking source identifiers, derived variable definitions, claim boundaries
   and figure-panel data dependencies.
5. Rebuilding reviewer-facing reference outputs from the included Python script
   and CSV tables.

The repository is aligned with the manuscript's public-data estimand: a
planning-screen layer for identifying where AI data-centre growth requires
finer provider, facility, procurement and grid-resolved evidence.

## Repository layout

```text
data/examples/
    Manuscript-facing derived source tables and claim-evidence tables.

figures/
    Reference figure outputs used to check visual reconstruction.

scripts/
    Python scripts for reconstructing manuscript-facing analytic outputs.

docs/
    Source-data maps, release-scope notes, claim-evidence documentation and
    data/code availability text.

requirements.txt
    Python package requirements for the reconstruction scripts.

LICENSE
    Code licence.

DATA_LICENSE.md
    Licence and reuse terms for derived tables and documentation.

THIRD_PARTY_DATA_NOTICE.md
    Source-provider and third-party raw-data boundary notes.
```

## Included manuscript-facing tables

The repository includes the following figure-source and audit tables:

```text
data/examples/Fig2_source_data.csv
data/examples/Fig3_source_bootstrap_spearman.csv
data/examples/Fig3_source_country_panel.csv
data/examples/Fig3_source_evidence_overlap_audit.csv
data/examples/Fig3_source_leave_one_country_out.csv
data/examples/Fig4_source_data.csv
data/examples/Fig5_source_china_context_all_provinces.csv
data/examples/Fig5_source_china_entry_envelope.csv
data/examples/Fig5_source_contextual_role_matrix.csv
data/examples/claim_evidence_matrix.csv
data/examples/key_resources_table.csv
```

These tables are derived, manuscript-facing source tables. They are provided to
audit the published values, figure inputs and claim-evidence alignment, not to
redistribute restricted third-party raw data.

## Quick start

Create a clean Python environment and run the reconstruction script:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/reconstruct_manuscript_outputs.py
```

Expected outputs are written to:

```text
outputs/figures/
outputs/tables/
```

The script rebuilds reviewer-facing reference outputs from the included derived
CSV tables. The reconstructed outputs are intended for audit of the
manuscript-facing evidence chain; journal production artwork may differ in
layout, typography or export format.

## Evidence classes

The manuscript separates evidence into two classes.

### Public-data evidence class

This repository contains the public-data evidence class used for the
manuscript-facing burden-geography screen:

```text
demand-origin signals
constrained compute-host allocation
host-burden shares
electricity-burden envelopes
location-based direct-carbon envelopes
public compute-side plausibility diagnostics
fossil-exposure motif tables
China infrastructure-context layers
claim-evidence matrices
figure source tables
```

### Higher-resolution evidence required for future attribution

Several higher-resolution evidence classes would be required for direct
attribution beyond the planning-screen estimand:

```text
provider routing logs
facility-level electricity loads
facility-level GPU utilization
provider procurement contracts
hourly marginal emissions
physical fuel-procurement records
facility-resolved water-use measurements
AI-specific domestic dispatch evidence
```

Those higher-resolution data streams define future attribution layers. They are
not redistributed in this public repository.

## Claim-evidence alignment

The repository supports the manuscript's bounded claims:

```text
modeled demand-execution displacement
compute-host burden concentration
host plausibility alignment with public compute-side evidence
electricity-burden envelope
location-based direct-carbon envelope
fossil-exposure motif stability
China national infrastructure-context embedding
```

The claim-evidence matrix records which source tables support each claim and
which higher-resolution evidence would be required for stronger attribution.

## Reproducibility scope

The repository is intended to support:

```text
source-table inspection
figure-source audit
schema checking
claim-evidence checking
reviewer-facing output reconstruction
requirements-based reruns
```

The repository does not replace third-party raw-data access, provider
disclosure, facility metering, procurement records or hourly grid modelling.
Those evidence classes remain outside the public release and are identified as
future data priorities in the manuscript.

## Requirements

The reconstruction script uses:

```text
Python >= 3.10
matplotlib
numpy
pandas
```

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Versioning

For review, cite the repository URL together with the commit hash used for
submission. Upon acceptance, the repository should be archived as a versioned
release and, where possible, assigned a persistent DOI through a public
research-data archive.

Suggested submission version label:

```text
v1.0.1-applied-energy-public-release
```

## Data and code availability text

The following text matches the manuscript-facing release scope:

```text
Manuscript-facing derived tables, figure source data, schema records, claim-evidence matrices and reconstruction scripts are available in this public repository. Raw third-party datasets remain governed by their original licences and access conditions; the public release therefore provides derived source tables, public source identifiers, reconstruction inputs and audit records rather than redistributing restricted raw data.
```

## Citation

For review, cite this repository using the repository URL and commit hash.
After acceptance, cite the archived release DOI if one is minted.
