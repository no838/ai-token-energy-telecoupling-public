#!/usr/bin/env python3
"""Recompute Figure 3 evidence-class ablation diagnostics from release data.

The script reads the Figure 3 country panel and recomputes the Spearman point
estimates reported in Figure 3 and Table S6. Bootstrap intervals are read from
the archived Table S6/figure-source ablation table included in this public
derived-data release.

Run from the release root:
    python scripts/recompute_fig3_ablation.py

Outputs are written to:
    reproduced_outputs/
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Iterable, List, Dict, Tuple


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "derived_tables"
OUTDIR = ROOT / "reproduced_outputs"

COUNTRY_PANEL = DERIVED / "Fig3_source_country_panel.csv"
LOCKED_ABLATION = DERIVED / "Fig3_source_evidence_class_ablation.csv"


def read_csv_dicts(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required input: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def to_float(value: str) -> float:
    if value is None or value == "":
        return float("nan")
    return float(value)


def rank_average(values: List[float]) -> List[float]:
    """Return 1-based average ranks, with average ranks for ties."""
    pairs = sorted((v, i) for i, v in enumerate(values))
    ranks = [0.0] * len(values)
    j = 0
    while j < len(pairs):
        k = j + 1
        while k < len(pairs) and pairs[k][0] == pairs[j][0]:
            k += 1
        avg_rank = (j + 1 + k) / 2.0
        for _, idx in pairs[j:k]:
            ranks[idx] = avg_rank
        j = k
    return ranks


def pearson(x: List[float], y: List[float]) -> float:
    n = len(x)
    if n != len(y) or n < 3:
        return float("nan")
    mx = sum(x) / n
    my = sum(y) / n
    sx = sum((v - mx) ** 2 for v in x)
    sy = sum((v - my) ** 2 for v in y)
    if sx <= 0 or sy <= 0:
        return float("nan")
    sxy = sum((xv - mx) * (yv - my) for xv, yv in zip(x, y))
    return sxy / math.sqrt(sx * sy)


def spearman(x: Iterable[float], y: Iterable[float]) -> float:
    clean: List[Tuple[float, float]] = [
        (float(a), float(b))
        for a, b in zip(x, y)
        if not (math.isnan(float(a)) or math.isnan(float(b)))
    ]
    if len(clean) < 3:
        return float("nan")
    xx, yy = zip(*clean)
    return pearson(rank_average(list(xx)), rank_average(list(yy)))


def locked_bootstrap_lookup() -> Dict[Tuple[str, str], Dict[str, str]]:
    lookup: Dict[Tuple[str, str], Dict[str, str]] = {}
    if not LOCKED_ABLATION.exists():
        return lookup
    for row in read_csv_dicts(LOCKED_ABLATION):
        key = (row.get("diagnostic", ""), row.get("excluded_evidence_class", ""))
        lookup[key] = row
    return lookup


def quantile(sorted_values: List[float], q: float) -> float:
    if not sorted_values:
        return float("nan")
    if len(sorted_values) == 1:
        return sorted_values[0]
    pos = q * (len(sorted_values) - 1)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return sorted_values[lo]
    return sorted_values[lo] * (hi - pos) + sorted_values[hi] * (pos - lo)


def main() -> None:
    rows = read_csv_dicts(COUNTRY_PANEL)
    host = [to_float(r["host_burden_pct"]) for r in rows]
    full_scores = [to_float(r["full_public_plausibility_score"]) for r in rows]
    full_rho = spearman(host, full_scores)

    metric_columns = [
        ("full_public_compute_side_plausibility", "none", "full_public_plausibility_score"),
        ("leave_one_public_evidence_class_out", "AI cluster evidence", "loo_without__AI cluster evidence"),
        ("leave_one_public_evidence_class_out", "data-center footprint", "loo_without__data-center footprint"),
        ("leave_one_public_evidence_class_out", "hyperscale MW", "loo_without__hyperscale MW"),
        ("leave_one_public_evidence_class_out", "public load/capacity", "loo_without__public load/capacity"),
        ("exclude_all_classes_shared_with_host_prior", "data-center footprint|public load/capacity", "shared_removed_plausibility_score"),
        ("capacity_prior_only_comparator", "not_applicable", "capacity_prior_comparator_score"),
    ]

    locked = locked_bootstrap_lookup()
    ablation_rows = []
    for metric, excluded, col in metric_columns:
        scores = [to_float(r[col]) for r in rows]
        rho = spearman(host, scores)
        locked_row = locked.get((metric, excluded), {})
        ablation_rows.append({
            "diagnostic": metric,
            "excluded_evidence_class": excluded,
            "spearman_rho_recomputed": f"{rho:.6f}",
            "spearman_rho_locked_table": locked_row.get("spearman_rho", ""),
            "rho_drop_from_full_recomputed": f"{full_rho - rho:.6f}",
            "rho_drop_from_full_locked_table": locked_row.get("rho_drop_from_full", ""),
            "bootstrap_p05_locked_table": locked_row.get("bootstrap_p05", ""),
            "bootstrap_p50_locked_table": locked_row.get("bootstrap_p50", ""),
            "bootstrap_p95_locked_table": locked_row.get("bootstrap_p95", ""),
            "n_countries": str(len(rows)),
        })

    leave_one_rows = []
    for r in rows:
        idx_iso = r["iso3"]
        idx_country = r["country_name"]
        remaining = [q for q in rows if q["iso3"] != idx_iso]
        h2 = [to_float(q["host_burden_pct"]) for q in remaining]
        for metric, col in [
            ("full_public_compute_side_plausibility", "full_public_plausibility_score"),
            ("shared_classes_removed", "shared_removed_plausibility_score"),
            ("capacity_prior_only_comparator", "capacity_prior_comparator_score"),
        ]:
            s2 = [to_float(q[col]) for q in remaining]
            leave_one_rows.append({
                "metric": metric,
                "left_out_iso3": idx_iso,
                "left_out_country": idx_country,
                "spearman_rho": f"{spearman(h2, s2):.6f}",
            })

    summary_rows = []
    for metric in sorted({r["metric"] for r in leave_one_rows}):
        vals = sorted(float(r["spearman_rho"]) for r in leave_one_rows if r["metric"] == metric)
        summary_rows.append({
            "metric": metric,
            "leave_one_country_p05": f"{quantile(vals, 0.05):.6f}",
            "leave_one_country_median": f"{quantile(vals, 0.50):.6f}",
            "leave_one_country_p95": f"{quantile(vals, 0.95):.6f}",
        })

    OUTDIR.mkdir(parents=True, exist_ok=True)
    for name, rows_out in [
        ("recomputed_Fig3_evidence_class_ablation.csv", ablation_rows),
        ("recomputed_Fig3_leave_one_country_out.csv", leave_one_rows),
        ("recomputed_Fig3_leave_one_country_summary.csv", summary_rows),
    ]:
        outpath = OUTDIR / name
        with outpath.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
            writer.writeheader()
            writer.writerows(rows_out)

    print("Recomputed Figure 3 diagnostics")
    print(f"Country panel: {len(rows)} countries")
    print(f"Full public plausibility rho: {full_rho:.6f}")
    print(f"Outputs written to: {OUTDIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
