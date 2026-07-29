#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""htn_epi01 analysis stub — fill results/metrics.json from CHARLS merge.

Expected inputs (not shipped):
  data/charls_baseline.csv
  data/city_rui_env_2011.csv

Outputs:
  results/metrics.json  — tokens for manuscript placeholders
  results/flow_exclusions.csv
  results/table1.csv
  results/or_models.csv
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
RES.mkdir(exist_ok=True)

TEMPLATE = {
    "N_TOTAL": None,
    "N_HTN": None,
    "PREV_HTN": None,
    "MEAN_AGE": None,
    "PCT_FEMALE": None,
    "RUI_HTN": None,
    "RUI_NON": None,
    "P_RUI": None,
    "OR_CONT": None,
    "OR_CONT_LO": None,
    "OR_CONT_HI": None,
    "OR_Q4": None,
    "OR_Q4_LO": None,
    "OR_Q4_HI": None,
    "P_TREND": None,
    "P_OVERALL": None,
    "P_NONLINEAR": None,
    "NONLINEAR_PHRASE": "without evidence of nonlinearity",
    "AUC1": None,
    "AUC2": None,
    "AUC3": None,
    "AUC4": None,
    "AUC5": None,
    "DAUC_RUI": None,
    "P_DELONG_RUI": None,
    "DAUC_FULL": None,
    "P_DELONG_FULL": None,
    "_note": "Replace nulls after running weighted logistic + RF pipeline on local CHARLS files.",
}


def main() -> None:
    baseline = ROOT / "data" / "charls_baseline.csv"
    city = ROOT / "data" / "city_rui_env_2011.csv"
    out = RES / "metrics.json"
    if not baseline.exists() or not city.exists():
        out.write_text(json.dumps(TEMPLATE, indent=2) + "\n", encoding="utf-8")
        print("STUB: missing data files; wrote empty metrics template →", out)
        print("Place CHARLS+city tables under data/ then implement modeling here (or R).")
        return
    raise NotImplementedError(
        "Data files found — implement survey-weighted logistic + RCS + RF here, "
        "then write filled metrics.json."
    )


if __name__ == "__main__":
    main()
