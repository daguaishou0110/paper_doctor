# -*- coding: utf-8 -*-
"""Build Nature-style GA prompts (English-only labels for image models)."""
from __future__ import annotations

import json
from pathlib import Path

DATA = Path(__file__).resolve().parent
papers = json.loads((DATA / "papers.json").read_text(encoding="utf-8"))
methods = {m["id"]: m for m in json.loads((DATA / "methods.json").read_text(encoding="utf-8"))}
cancers = {c["id"]: c for c in json.loads((DATA / "cancers.json").read_text(encoding="utf-8"))}

STYLE = (
    "Nature journal graphical abstract style, wide cinematic 16:9 composition, "
    "pristine white background, flat vector scientific illustration, "
    "soft navy teal and muted coral accents, crisp medical icons, "
    "elegant minimal English labels only, left-to-right narrative flow, "
    "generous whitespace, premium oncology bioinformatics figure, "
    "no photorealism, no 3D gloss, no cartoon characters, no watermark, no phone UI"
)

CANCER_VISUAL = {
    "crc": ("Colorectal Cancer", "subtle colon silhouette"),
    "brca": ("Breast Cancer", "subtle breast tissue icon"),
    "stad": ("Gastric Adenocarcinoma", "subtle stomach silhouette"),
    "luad": ("Lung Adenocarcinoma", "subtle lung silhouette"),
    "lusc": ("Lung Squamous Cell Carcinoma", "subtle lung silhouette"),
    "lihc": ("Hepatocellular Carcinoma", "subtle liver silhouette"),
    "paad": ("Pancreatic Adenocarcinoma", "subtle pancreas silhouette"),
    "hnsc": ("Head and Neck Squamous Cell Carcinoma", "subtle head-neck anatomy icon"),
    "kirc": ("Clear Cell Renal Cell Carcinoma", "subtle kidney silhouette"),
}

METHOD_SCENE = {
    "art01": (
        "Clinical-Transcriptomic OS",
        "clipboard of clinical covariates and a transcriptomic heatmap flow into a Cox model hexagon, "
        "then Kaplan-Meier curves and a time-dependent ROC badge",
    ),
    "art02": (
        "Clinical-Genomic OS",
        "mutation lollipop plot, DNA helix, TMB meter and MMR badge merge with clinical stage into a survival model",
    ),
    "art03": (
        "Clinical-Transcriptomic RFS",
        "recurrence clock icon with clinical factors and transcriptomic signature leading to RFS Kaplan-Meier curves",
    ),
    "art04": (
        "Chemo Benefit Interaction",
        "2x2 matrix of high/low risk versus chemo yes/no with a central interaction arrow and four tiny KM sketches",
    ),
    "art05": (
        "Cross-Platform Subtyping",
        "RNA-seq sequencer versus microarray chip arrows into consensus subtype chips, kappa dial, subtype KM curves",
    ),
    "art06": (
        "Immune-TMB Prognosis",
        "immune cells and IFN-gamma spark with TMB and MMR badges enter an integrated model then OS stratification",
    ),
    "art07": (
        "Stage II/III Subgroup RFS",
        "stage II/III funnel filter, clinical plus transcriptomic inputs, subgroup RFS survival curves",
    ),
}


def prompt_for(paper: dict) -> str:
    cancer_en, organ = CANCER_VISUAL[paper["cancer_id"]]
    short, scene = METHOD_SCENE[paper["method_id"]]
    return (
        f"{STYLE}. Cancer focus: {cancer_en}. Study type: {short}. "
        f"Place a small {organ} at top-left. Main visual: {scene}. "
        f"Tiny caption labels: '{cancer_en.split()[0]}' and '{paper['method_id']}'."
    )


out = []
for p in papers:
    out.append(
        {
            "id": p["id"],
            "filename": f"{p['id']}.png",
            "prompt": prompt_for(p),
            "cancer_id": p["cancer_id"],
            "method_id": p["method_id"],
        }
    )

(DATA / "ga_prompts.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(len(out))
