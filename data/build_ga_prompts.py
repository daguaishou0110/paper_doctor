# -*- coding: utf-8 -*-
"""Build Nature-style GA prompts — formal journal figures, no art0x codes."""
from __future__ import annotations

import json
from pathlib import Path

DATA = Path(__file__).resolve().parent
papers = json.loads((DATA / "papers.json").read_text(encoding="utf-8"))

STYLE = (
    "Formal Nature journal graphical abstract for a peer-reviewed oncology paper, "
    "wide cinematic 16:9 composition, pristine white background, "
    "flat vector scientific illustration, soft navy teal and muted coral accents, "
    "crisp medical icons, elegant minimal English scientific labels only "
    "(words like Cohort, Model, Validation, Survival, Immune, Subtype are OK), "
    "left-to-right narrative flow, generous whitespace, publication-ready figure, "
    "no photorealism, no 3D gloss, no cartoon characters, no watermark, no UI chrome, "
    "absolutely no project codes, no art01 art02 art03 labels, no internal IDs, no slug text"
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
        "Clinical–Transcriptomic Overall Survival Model",
        "clipboard of clinical covariates and a transcriptomic heatmap flow into a Cox model node, "
        "then Kaplan–Meier curves and a time-dependent ROC badge for external validation",
    ),
    "art02": (
        "Clinical–Genomic Overall Survival Model",
        "mutation lollipop plot, DNA helix, TMB meter and MMR badge merge with clinical stage into a survival model",
    ),
    "art03": (
        "Clinical–Transcriptomic Recurrence-Free Survival Model",
        "recurrence timeline with clinical factors and a transcriptomic signature leading to RFS Kaplan–Meier curves",
    ),
    "art04": (
        "Transcriptomic Risk × Adjuvant Chemotherapy Interaction",
        "2×2 matrix of high/low risk versus chemotherapy yes/no with a central interaction arrow and four small KM sketches",
    ),
    "art05": (
        "Cross-Platform Molecular Subtype Validation",
        "RNA-seq sequencer versus microarray chip arrows into consensus subtype badges, agreement meter, subtype KM curves",
    ),
    "art06": (
        "Clinical–Immune–Genomic Prognostic Model",
        "immune cells and IFN-γ signal with TMB and MMR badges enter an integrated model then overall survival stratification",
    ),
    "art07": (
        "Stage II/III Subgroup Recurrence-Free Survival Model",
        "stage II/III selection funnel, clinical plus transcriptomic inputs, subgroup RFS survival curves",
    ),
}


def prompt_for(paper: dict) -> str:
    cancer_en, organ = CANCER_VISUAL[paper["cancer_id"]]
    short, scene = METHOD_SCENE[paper["method_id"]]
    return (
        f"{STYLE}. Disease: {cancer_en}. Theme: {short}. "
        f"Place a small {organ} at the top-left corner. Main visual narrative: {scene}. "
        f"Optional tiny disease name only: '{cancer_en}'. Do not print any art codes."
    )


out = []
for p in papers:
    out.append(
        {
            "id": p["id"],
            "filename": f"{p['id']}.jpg",
            "prompt": prompt_for(p),
            "cancer_id": p["cancer_id"],
            "method_id": p["method_id"],
        }
    )

(DATA / "ga_prompts.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(len(out))
