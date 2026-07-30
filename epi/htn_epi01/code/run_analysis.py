#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mirror of 公卫队列/htn_epi01 — website package entry."""
from __future__ import annotations

import runpy
from pathlib import Path

# Prefer shared factory pipeline
FACTORY = Path(__file__).resolve().parents[3] / "公卫队列" / "htn_epi01" / "code" / "run_analysis.py"
if FACTORY.exists():
    runpy.run_path(str(FACTORY), run_name="__main__")
else:
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    LIB = Path(__file__).resolve().parents[3] / "公卫队列" / "_lib"
    sys.path.insert(0, str(LIB))
    from epi_pipeline import EpiConfig, run_pipeline

    print(run_pipeline(EpiConfig(project_root=ROOT, method="epi01", outcome="htn", exposure="rui")))
