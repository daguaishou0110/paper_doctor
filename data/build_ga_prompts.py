# -*- coding: utf-8 -*-
"""GA prompts: schematic only — no fake experimental data in the figure."""
from __future__ import annotations

import json
from pathlib import Path

DATA = Path(__file__).resolve().parent

STYLE = (
    "Formal Nature journal graphical abstract, wide 16:9, pristine white background, "
    "flat vector scientific SCHEMATIC illustration only, soft navy teal and muted coral accents, "
    "minimal English labels for process steps only (Cohort, Features, Model, Validation), "
    "left-to-right conceptual workflow, generous whitespace, publication-ready schematic, "
    "no photorealism, no cartoon characters, no watermark, no UI chrome, no art codes, "
    "CRITICAL: do NOT draw any fake experimental results — "
    "no Kaplan-Meier curves with plotted lines, no ROC curves with AUC numbers, "
    "no forest plots with hazard ratios, no heatmaps with expression values, "
    "no number-at-risk tables, no p-values, no C-index, no percentages, no sample-size numerals, "
    "no scatter plots with points, no calibration plots with dots, no bar charts with data, "
    "use empty icon placeholders instead (blank axes box icon, blank grid icon, checkmark badge) "
    "to represent analysis outputs conceptually without inventing data"
)

CANCER_VISUAL = {
    "crc": ("Colorectal Cancer", "subtle abstract colon icon"),
    "coad": ("Colon Adenocarcinoma", "subtle abstract colon icon"),
    "read": ("Rectum Adenocarcinoma", "subtle abstract rectum icon"),
    "brca": ("Breast Cancer", "subtle abstract breast tissue icon"),
    "stad": ("Gastric Adenocarcinoma", "subtle abstract stomach icon"),
    "luad": ("Lung Adenocarcinoma", "subtle abstract lung icon"),
    "lusc": ("Lung Squamous Cell Carcinoma", "subtle abstract lung icon"),
    "lihc": ("Hepatocellular Carcinoma", "subtle abstract liver icon"),
    "paad": ("Pancreatic Adenocarcinoma", "subtle abstract pancreas icon"),
    "hnsc": ("Head and Neck Squamous Cell Carcinoma", "subtle abstract head-neck icon"),
    "kirc": ("Clear Cell Renal Cell Carcinoma", "subtle abstract kidney icon"),
    "blca": ("Bladder Urothelial Carcinoma", "subtle abstract bladder icon"),
    "esca": ("Esophageal Carcinoma", "subtle abstract esophagus icon"),
    "ov": ("Ovarian Serous Cystadenocarcinoma", "subtle abstract ovary icon"),
    "cesc": ("Cervical Squamous Cell Carcinoma", "subtle abstract cervix icon"),
    "ucec": ("Uterine Corpus Endometrial Carcinoma", "subtle abstract uterus icon"),
    "ucs": ("Uterine Carcinosarcoma", "subtle abstract uterus icon"),
    "prad": ("Prostate Adenocarcinoma", "subtle abstract prostate icon"),
    "skcm": ("Skin Cutaneous Melanoma", "subtle abstract skin lesion icon"),
    "gbm": ("Glioblastoma Multiforme", "subtle abstract brain icon"),
    "thca": ("Thyroid Carcinoma", "subtle abstract thyroid icon"),
    "kirp": ("Kidney Renal Papillary Cell Carcinoma", "subtle abstract kidney icon"),
    "kich": ("Kidney Chromophobe", "subtle abstract kidney icon"),
    "chol": ("Cholangiocarcinoma", "subtle abstract bile duct icon"),
    "meso": ("Mesothelioma", "subtle abstract pleural lining icon"),
    "lgg": ("Brain Lower Grade Glioma", "subtle abstract brain icon"),
    "tgct": ("Testicular Germ Cell Tumors", "subtle abstract testis icon"),
    "uvm": ("Uveal Melanoma", "subtle abstract eye icon"),
    "os": ("Osteosarcoma", "subtle abstract bone icon"),
    "sarc": ("Soft Tissue Sarcoma", "subtle abstract soft-tissue icon"),
    "nbl": ("Neuroblastoma", "subtle abstract neural crest icon"),
    "pcpg": ("Pheochromocytoma / Paraganglioma", "subtle abstract adrenal icon"),
    "acc": ("Adrenocortical Carcinoma", "subtle abstract adrenal cortex icon"),
    "thym": ("Thymoma", "subtle abstract thymus icon"),
    "rms": ("Rhabdomyosarcoma", "subtle abstract muscle icon"),
    "rt": ("Rhabdoid Tumor", "subtle abstract pediatric tumor icon"),
    "wt": ("Wilms Tumor", "subtle abstract kidney icon"),
    "ccsk": ("Clear Cell Sarcoma of the Kidney", "subtle abstract kidney icon"),
    "mbrca": ("Metastatic Breast Cancer", "subtle abstract breast tissue icon"),
    "mprad": ("Metastatic Prostate Cancer", "subtle abstract prostate icon"),
    "dlbc": ("Diffuse Large B-Cell Lymphoma", "subtle abstract lymph node icon"),
    "aml": ("Acute Myeloid Leukemia", "subtle abstract blood cell icon"),
}

METHOD_SCENE = {
    "art01": (
        "Clinical–Transcriptomic OS Schematic",
        "three icon panels only: (1) clinical clipboard icon + abstract transcriptomic grid icon without numbers, "
        "(2) Cox model node icon, (3) blank survival-analysis badge and blank validation badge — no plotted curves",
    ),
    "art02": (
        "Clinical–Genomic OS Schematic",
        "three icon panels: DNA helix icon, TMB/MMR badge icons, clinical stage icon merging into a model node, "
        "then a blank outcome badge — no mutation lollipop with fake gene names or fake counts",
    ),
    "art03": (
        "Clinical–Transcriptomic RFS Schematic",
        "icons for clinical factors, transcriptomic signature card, and a blank recurrence-free survival badge — no KM lines",
    ),
    "art04": (
        "Risk × Chemotherapy Interaction Schematic",
        "empty 2×2 conceptual matrix labeled High/Low risk and Chemo yes/no with a center interaction arrow — "
        "no survival curves inside the quadrants",
    ),
    "art05": (
        "Cross-Platform Subtyping Schematic",
        "RNA-seq platform icon versus microarray platform icon arrows into subtype badge icons A/B/C and an agreement badge — "
        "no real heatmaps or survival curves",
    ),
    "art06": (
        "Immune–Genomic Prognosis Schematic",
        "immune cell icons, IFN-γ badge, TMB/MMR badges flowing into an integrated model node and blank OS badge — no data plots",
    ),
    "art08": (
        "Multi-Model ML Prognostic Schematic",
        "icons for clinical+transcriptomic inputs feeding three competing model cards (Penalized Cox, RSF, Gradient Boosting) then a locked-best badge and blank SHAP bars — no fake AUC",
    ),
    "art07": (
        "Stage II/III Subgroup RFS Schematic",
        "stage II/III funnel icon, clinical+transcriptomic icons, blank subgroup RFS badge — no plotted survival curves",
    ),
}


def prompt_for(paper: dict) -> str:
    cancer_en, organ = CANCER_VISUAL[paper["cancer_id"]]
    short, scene = METHOD_SCENE[paper["method_id"]]
    return (
        f"{STYLE}. Disease: {cancer_en}. Theme: {short}. "
        f"Small {organ} at top-left. Visual: {scene}. "
        f"Optional tiny disease title '{cancer_en}'. "
        f"Remember: schematic icons only; zero fabricated statistics or result plots."
    )


def main() -> None:
    papers = json.loads((DATA / "papers.json").read_text(encoding="utf-8"))
    out = [
        {
            "id": p["id"],
            "filename": f"{p['id']}.jpg",
            "prompt": prompt_for(p),
            "cancer_id": p["cancer_id"],
            "method_id": p["method_id"],
        }
        for p in papers
        if p.get("cancer_id") in CANCER_VISUAL
    ]
    (DATA / "ga_prompts.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(len(out))


if __name__ == "__main__":
    main()
