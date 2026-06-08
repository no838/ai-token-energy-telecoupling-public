#!/usr/bin/env python3
"""
Reconstruct manuscript-facing analytic outputs from public derived source tables.

This script rebuilds reviewer-facing reference outputs from the included
derived CSV tables. The outputs support audit of the manuscript-facing
burden-geography evidence chain, including demand-execution displacement,
compute-host plausibility alignment and China infrastructure-context layers.

The script uses public derived tables and source identifiers. It does not
redistribute restricted third-party raw data or higher-resolution private
evidence classes such as provider routing logs, facility electricity loads,
procurement contracts, hourly marginal emissions, physical fuel-procurement
records or facility-resolved water-use measurements.
"""
from __future__ import annotations

from pathlib import Path

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


def build_fig2_reconstructed() -> None:
    df = read_csv("Fig2_source_data.csv")
    num_cols = [c for c in df.columns if df[c].dtype.kind in "if"]
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    if {"demand_share", "burden_share"}.issubset(df.columns):
        x, y = "demand_share", "burden_share"
    else:
        if len(num_cols) < 2:
            raise ValueError("Fig2 source data needs either demand_share/burden_share or two numeric columns")
        x, y = num_cols[:2]
    ax.scatter(df[x], df[y], s=28, color=BLUE, alpha=0.75, edgecolor="white", linewidth=0.4)
    lim = max(float(df[x].max()), float(df[y].max())) * 1.08
    ax.plot([0, lim], [0, lim], color=SLATE, lw=0.9, ls="--")
    ax.set_xlabel(x.replace("_", " "))
    ax.set_ylabel(y.replace("_", " "))
    ax.set_title("Demand-execution displacement reconstruction", loc="left", weight="bold")
    ax.grid(True, color=GRID, lw=0.4, alpha=0.55)
    save(fig, "Fig2_reconstructed_displacement")


def build_fig3_reconstructed() -> None:
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
    ax.set_title("Compute-host plausibility reconstruction", loc="left", weight="bold")
    ax.grid(True, color=GRID, lw=0.4, alpha=0.55)
    save(fig, "Fig3_reconstructed_compute_plausibility")


def build_fig5_reconstructed() -> None:
    entry = read_csv("Fig5_source_china_entry_envelope.csv")
    roles = read_csv("Fig5_source_contextual_role_matrix.csv")
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.8), gridspec_kw={"width_ratios": [1.0, 1.25]})
    ax = axes[0]
    ax.axis("off")
    lines = ["China infrastructure context", "contextual, non-additive"]
    for col in entry.columns:
        vals = "/".join(str(v) for v in entry[col].dropna().tolist()[:3])
        if vals:
            lines.append(f"{col}: {vals}")
    ax.text(
        0.02,
        0.96,
        "\n".join(lines),
        va="top",
        ha="left",
        fontsize=8.6,
        bbox=dict(boxstyle="round,pad=0.45", facecolor=LIGHT, edgecolor=TEAL, linewidth=1.0),
    )
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
    save(fig, "Fig5_reconstructed_china_context")


def main() -> None:
    build_fig2_reconstructed()
    build_fig3_reconstructed()
    build_fig5_reconstructed()
    summary = pd.DataFrame([
        {
            "output": "Fig2_reconstructed_displacement",
            "claim_evidence_alignment": "modeled displacement, not observed routing",
        },
        {
            "output": "Fig3_reconstructed_compute_plausibility",
            "claim_evidence_alignment": "host plausibility alignment, not routing validation",
        },
        {
            "output": "Fig5_reconstructed_china_context",
            "claim_evidence_alignment": "contextual national infrastructure module, not causal domestic burden transfer",
        },
    ])
    summary.to_csv(OUT_TAB / "reconstruction_claim_evidence_summary.csv", index=False)
    print(f"Wrote reconstructed outputs to {OUT_FIG} and {OUT_TAB}")


if __name__ == "__main__":
    main()
