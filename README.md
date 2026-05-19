# Displaced AI electricity and carbon burden: schematic code package

This repository is a lightweight, public-facing code package for the manuscript
**"Displaced electricity and carbon burdens of artificial intelligence demand under constrained compute infrastructure"**.

The package is intentionally illustrative. It exposes the manuscript-facing figure-source tables,
claim-gate tables, and compact plotting code used to demonstrate the public-evidence-constrained
burden-allocation framework. It is not a release of private provider-routing logs, measured
country-level AI electricity loads, facility-level GPU utilization, provider procurement data, hourly
marginal emissions, physical fuel procurement records, or AI-specific water-demand measurements.
Those data are not publicly observed in the current evidence frontier and were not used.

## What this package supports

- Rebuilding simplified demonstration versions of Figures 2-5 from included source CSVs.
- Inspecting the claim-evidence matrix and source-data tables used for manuscript-facing figures.
- Understanding the release boundary between public derived tables and unavailable/private evidence.

## What this package does not support

- Observed provider routing.
- Measured AI electricity load.
- Exact serving-region reconstruction.
- Provider-specific procurement or market-based Scope 2 responsibility.
- Physical fuel-procurement chains.
- AI-induced water-demand attribution.
- Causal domestic burden transfer.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/build_schematic_demo_figures.py
```

Expected outputs are written to `outputs/figures/` and `outputs/tables/`.

## Repository layout

```text
scripts/                 lightweight demonstration plotting code
data/examples/           small derived source-data CSVs, not raw data
figures/                 manuscript-facing reference PNGs
docs/                    release scope and data/code availability text
```

## Claim boundary

This is a public-evidence-constrained burden-allocation package. It estimates modeled displacement,
host plausibility, burden envelopes, exposure motifs, and nested context. It does not validate routing
or measure AI electricity consumption.
