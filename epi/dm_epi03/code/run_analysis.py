#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dm_epi03 longitudinal analysis stub — incident diabetes vs baseline RUI."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
RES.mkdir(exist_ok=True)

TEMPLATE = {
    "N_AT_RISK": None,
    "N_EVENTS": None,
    "PERSON_YEARS": None,
    "IR": None,
    "HR_CONT": None,
    "HR_CONT_LO": None,
    "HR_CONT_HI": None,
    "HR_Q4": None,
    "HR_Q4_LO": None,
    "HR_Q4_HI": None,
    "P_TREND": None,
    "P_OVERALL": None,
    "P_NONLINEAR": None,
    "_note": "Need baseline + follow-up waves; exclude baseline diabetes; Cox/discrete-time HR.",
}


def main() -> None:
    baseline = ROOT / "data" / "charls_baseline.csv"
    follow = ROOT / "data" / "charls_followup.csv"
    city = ROOT / "data" / "city_rui_env_2011.csv"
    out = RES / "metrics.json"
    if not (baseline.exists() and follow.exists() and city.exists()):
        out.write_text(json.dumps(TEMPLATE, indent=2) + "\n", encoding="utf-8")
        print("STUB: missing wave/city files; wrote empty metrics template →", out)
        return
    raise NotImplementedError("Implement longitudinal diabetes incidence models locally.")


if __name__ == "__main__":
    main()
