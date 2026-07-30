#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auto-generated epi runner for this product card."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = Path(__file__).resolve().parents[3] / "公卫队列" / "_lib"
if not LIB.exists():
    LIB = Path(__file__).resolve().parents[4] / "公卫队列" / "_lib"
sys.path.insert(0, str(LIB))

from epi_pipeline import EpiConfig, fill_manuscript_placeholders, run_pipeline  # noqa: E402


def main() -> None:
    cfg = EpiConfig(
        project_root=ROOT,
        method="epi01",
        outcome="sleep",
        exposure="ndvi",
    )
    metrics = run_pipeline(cfg)
    fill_manuscript_placeholders(ROOT / "manuscript.md", metrics)
    print("data_ready", metrics.get("_data_ready"), "n", metrics.get("N_TOTAL"))


if __name__ == "__main__":
    main()
