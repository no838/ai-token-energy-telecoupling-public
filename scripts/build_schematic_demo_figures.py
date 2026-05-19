#!/usr/bin/env python3
"""Build lightweight schematic demonstration figures from public derived CSVs.

This script is intentionally small and portable. It rebuilds demonstration
versions of manuscript-facing figure panels from the included derived source
CSV files. It does not use private provider-routing logs, measured AI electricity
load, provider procurement data, physical fuel procurement records, or AI-specific
water-demand observations.
"""
from __future__ import annotations

from pathlib import Path
import math
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "examples"
OUT_FIG = ROOT / "outputs" / "figures"
OUT_TAB = ROOT / "outputs" / "tables"
OUT_FIG.mkdir(parents=True, exist_ok=True)
OUT_TAB.mkdir(parents=True, exist_ok=True)

INK = "#1F2937"
BLUE = "#3B6EA8"
TEAL = "#0F766E"
SLATE = "#64748B"
RED = "#B91C1C"
GRID = "#CBD5E1"
LIGHT = "#F8FAFC"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8.5,
    "axes.edgecolor": INK,
    "axes.linewidth": 0.8,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


def read_csv(name: str) -> pd.DataFrame:
    path = DATA / name
    if not path.exists():
        raise FileNotFoundError(f"Missing required source data: {path}")
    return pd.read_csv(path)


def save(fig: plt.Figure, stem: str) -> None:
    fig.savefig(OUT_FIG / f"{stem}.png", dpi=300, bbox_inches="tight")
    fig.savefig(OUT_FIG / f"{stem}.pdf", bbox_inches="tight")
    plt.close(fig)


def build_fig2_demo() -> None:
    df = read_csv("Fig2_source_data.csv")
    num_cols = [c for c in df.columns if df[c].dtype.kind in "if"]
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    if {"demand_share", "burden_share"}.issubset(df.columns):
        x, y = "demand_share", "burden_share"
    else:
        # Fallback for schema variation: use the first two numeric columns.
        if len(num_cols) < 2:
            raise ValueError("Fig2 source data needs either demand_share/burden_share or two numeric columns")
        x, y = num_cols[:2]
    ax.scatter(df[x], df[y], s=28, color=BLUE, alpha=0.75, edgecolor="white", linewidth=0.4)
    lim = max(float(df[x].max()), float(df[y].max())) * 1.08
    ax.plot([0, lim], [0, lim], color=SLATE, lw=0.9, ls="--")
    ax.set_xlabel(x.replace("_", " "))
    ax.set_ylabel(y.replace("_", " "))
    ax.set_title("Demand-execution displacement demo", loc="left", weight="bold")
    ax.grid(True, color=GRID, lw=0.4, alpha=0.55)
    save(fig, "Fig2_demo_displacement")


def build_fig3_demo() -> None:
    df = read_csv("Fig3_source_country_panel.csv")
    x_candidates = ["public_compute_side_plausibility_score", "plausibility_score"]
    y_candidates = ["modeled_host_burden_share_pct", "modeled_host_burden_share", "compute_execution_received_p50"]
    x = next((c for c in x_candidates if c in df.columns), None)
    y = next((c for c in y_candidates if c in df.columns), None)
    if x is None or y is None:
        numeric = [c for c in df.columns if df[c].dtype.kind in "if"]
        if len(numeric) < 2:
            raise ValueError("Fig3 source data needs two numeric columns")
        x, y = numeric[:2]
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    ax.scatter(df[x], df[y], s=32, color=BLUE, alpha=0.72, edgecolor="white", linewidth=0.4)
    if len(df) >= 3:
        rho = df[x].rank().corr(df[y].rank())
        ax.text(0.03, 0.94, f"Spearman rho = {rho:.3f}; n = {len(df)}", transform=ax.transAxes, color=INK)
    ax.set_xlabel(x.replace("_", " "))
    ax.set_ylabel(y.replace("_", " "))
    ax.set_title("Compute-host plausibility alignment demo", loc="left", weight="bold")
    ax.grid(True, color=GRID, lw=0.4, alpha=0.55)
    save(fig, "Fig3_demo_compute_plausibility")


def build_fig5_demo() -> None:
    entry = read_csv("Fig5_source_china_entry_envelope.csv")
    roles = read_csv("Fig5_source_contextual_role_matrix.csv")
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.8), gridspec_kw={"width_ratios": [1.0, 1.25]})
    ax = axes[0]
    ax.axis("off")
    lines = ["China nested context", "contextual, non-additive"]
    for col in entry.columns:
        vals = "/".join(str(v) for v in entry[col].dropna().tolist()[:3])
        if vals:
            lines.append(f"{col}: {vals}")
    ax.text(0.02, 0.96, "\n".join(lines), va="top", ha="left", fontsize=8.6,
            bbox=dict(boxstyle="round,pad=0.45", facecolor=LIGHT, edgecolor=TEAL, linewidth=1.0))
    ax.set_title("Global-to-national entry", loc="left", weight="bold")

    ax = axes[1]
    if {"province", "layer"}.issubset(roles.columns):
        tab = pd.crosstab(roles["province"], roles["layer"])
    else:
        tab = roles.select_dtypes(include=[np.number]).head(12)
        if tab.empty:
            tab = pd.DataFrame([[1]], columns=["context"], index=["China"])
    arr = tab.to_numpy(dtype=float)
    ax.imshow(arr > 0, cmap=matplotlib.colors.ListedColormap(["#F8FAFC", BLUE]), aspect="auto")
    ax.set_yticks(range(len(tab.index)))
    ax.set_yticklabels([str(x)[:18] for x in tab.index], fontsize=6.8)
    ax.set_xticks(range(len(tab.columns)))
    ax.set_xticklabels([str(x)[:18] for x in tab.columns], rotation=35, ha="right", fontsize=6.8)
    ax.set_title("Domestic context-role matrix", loc="left", weight="bold")
    save(fig, "Fig5_demo_china_nested_context")


def main() -> None:
    build_fig2_demo()
    build_fig3_demo()
    build_fig5_demo()
    summary = pd.DataFrame([
        {"output": "Fig2_demo_displacement", "claim_boundary": "modeled displacement, not observed routing"},
        {"output": "Fig3_demo_compute_plausibility", "claim_boundary": "host plausibility alignment, not routing validation"},
        {"output": "Fig5_demo_china_nested_context", "claim_boundary": "contextual nested module, not causal domestic burden transfer"},
    ])
    summary.to_csv(OUT_TAB / "demo_output_claim_boundaries.csv", index=False)
    print(f"Wrote demonstration outputs to {OUT_FIG} and {OUT_TAB}")


if __name__ == "__main__":
    main()
