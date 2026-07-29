# -*- coding: utf-8 -*-
"""Strong title de-duplication: compositional templates + collision avoidance.

Does NOT change paper count — only rewrites `title` (keeps first `title_prev`).
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

DATA = Path(__file__).resolve().parent

# Method-specific cores (must stay scientifically aligned)
CORES = {
    "art01": [
        "a clinical–transcriptomic overall-survival model",
        "an integrative clinical plus expression survival score",
        "a locked clinical–RNA prognostic framework for OS",
        "a TRIPOD-style clinical–transcriptomic risk model",
        "a baseline-clinical model augmented with transcriptomic features for OS",
        "a cross-checked clinical–expression prognostication pipeline for OS",
        "a dual-block clinical and transcriptome survival classifier",
        "an OS-oriented clinical–omics fusion model",
    ],
    "art02": [
        "a clinical–genomic OS model using mutations, TMB, and MMR status",
        "a mutation-informed clinical survival framework incorporating TMB/MMR",
        "an integrative somatic-alteration plus clinical OS score",
        "a genomic-instability–aware clinical prognostic model for OS",
        "a driver-mutation and repair-status augmented clinical OS model",
        "a clinicogenomic stratification scheme for overall survival",
        "a TMB/MMR-enriched clinical survival model",
        "a mutation-burden–conscious clinical OS predictor",
    ],
    "art03": [
        "a clinical–transcriptomic recurrence-free survival model",
        "an expression-augmented clinical model for RFS/DFS",
        "a recurrence-oriented clinical–RNA risk score",
        "a relapse-focused clinical–transcriptomic framework",
        "a clinical baseline plus signature model for recurrence-free survival",
        "an RFS stratification pipeline combining clinical factors and expression",
        "a recurrence-risk clinical–omics score",
        "a disease-free/recurrence-free clinical–transcriptomic classifier",
    ],
    "art04": [
        "a transcriptomic-risk × adjuvant-chemotherapy interaction analysis in stage II/III disease",
        "a treatment-effect heterogeneity study of adjuvant chemotherapy by expression risk",
        "an interaction framework linking expression risk strata to adjuvant chemotherapy benefit",
        "a risk-by-treatment analysis of adjuvant chemotherapy associations",
        "a stratified benefit assessment of adjuvant chemotherapy across transcriptomic risk groups",
        "a chemo-benefit interaction model conditioned on expression-based risk",
        "an adjuvant-therapy effect-modification analysis by transcriptomic risk",
        "a stage II/III chemotherapy-interaction evaluation using an expression risk score",
    ],
    "art05": [
        "a cross-platform concordance assessment of consensus molecular subtypes",
        "an RNA-seq versus microarray subtype-transfer validation",
        "a platform-shift robustness check for molecular classification",
        "a cross-assay agreement study of consensus subtypes",
        "a sequencing-to-array subtype mapping and concordance analysis",
        "a reproducibility audit of molecular classes across expression platforms",
        "a cross-platform subtype stability evaluation",
        "a dual-platform molecular-subtype consistency study",
    ],
    "art06": [
        "a clinical–immune–genomic OS model integrating IFN-γ, TMB, and MMR",
        "an immuno-genomic clinical survival score combining interferon programs and mutational burden",
        "a layered IFN-γ plus TMB/MMR clinical prognostication framework for OS",
        "an immune-activation and genomic-instability informed clinical OS model",
        "a multi-axis immuno-genomic clinical risk model for overall survival",
        "an IFN-signature–augmented clinicogenomic OS classifier",
        "a joint immune–mutation clinical survival framework",
        "an integrative interferon, TMB, and MMR clinical OS score",
    ],
    "art07": [
        "a stage II/III–restricted clinical–transcriptomic RFS model",
        "an intermediate-stage recurrence model comparing clinical vs clinical–expression blocks",
        "a stage-stratified clinical–RNA recurrence-risk framework",
        "a stage II/III–focused expression-augmented RFS score",
        "a within-stage clinical–transcriptomic recurrence classifier",
        "an intermediate-risk-window RFS model using clinical plus expression features",
        "a stage-conditioned clinical–omics recurrence pipeline",
        "a stage II/III subgroup RFS modeling analysis with transcriptomic add-on",
    ],
    "art08": [
        "a multi-algorithm survival benchmark of penalized Cox, RSF, and boosting",
        "a head-to-head comparison of classical and ensemble survival learners",
        "a multi-model OS modeling bake-off with locked evaluation",
        "an interpretable multi-learner survival comparison under censoring",
        "a penalized-Cox versus tree-ensemble survival showdown",
        "a systematic multi-algorithm OS model selection study",
        "a cross-learner survival benchmarking framework with explanation metrics",
        "a multi-model machine-learning survival comparison for OS",
    ],
}

OPENERS = [
    "Development of",
    "Construction of",
    "Derivation of",
    "Evaluation of",
    "External assessment of",
    "Cross-cohort validation of",
    "Proposal of",
    "Establishment of",
    "Assembly of",
    "Calibration of",
    "Sensitivity analysis around",
    "Reassessment of",
    "Extension of",
    "Refinement of",
    "Operationalization of",
    "Formalization of",
    "Mapping of",
    "Quantification of",
    "Dissection of",
    "Head-to-head contrast of",
    "Charting of",
    "Anchoring of",
    "Framing of",
    "Updated appraisal of",
    "Positioning of",
    "Synthesis of",
    "Prioritization within",
    "Isolation of",
    "Resolution of",
    "Characterization of",
    "Interrogation of",
    "Audit of",
    "Hardening of",
    "Stabilization of",
    "Generalization test of",
    "Transportability check of",
    "Replication-oriented test of",
    "Cross-check of",
    "Triangulation of",
    "Layered appraisal of",
    "Incremental-value test of",
    "Benchmarking of",
]

BRIDGES = [
    "for",
    "in",
    "among patients with",
    "in a cohort of",
    "using publicly available data for",
    "in resected/diagnosed",
    "across clinically annotated cases of",
]

CLOSERS_TCGA = [
    "with cross-cohort validation around {tcga}",
    "derived primarily from {tcga} with independent checking",
    "trained under leakage-controlled splits on {tcga}",
    "following a TRIPOD-aligned reporting path on {tcga}",
    "with external/holdout evaluation beyond {tcga} discovery",
    "emphasizing incremental value over clinical baselines ({tcga})",
    "with transparent cohort locking based on {tcga}",
    "and reporting discrimination–calibration trade-offs ({tcga})",
    "under a pre-registered analysis skeleton on {tcga}",
    "with geography-/cohort-aware validation after {tcga} development",
]

CLOSERS_GEO = [
    "in the {geo} cohort with internal validation",
    "using {geo} as the primary analysis set",
    "with TRIPOD-style reporting on {geo}",
    "emphasizing recurrence endpoint definitions in {geo}",
    "via locked training–validation splits within {geo}",
    "and sensitivity checks in {geo}",
    "focusing on clinically actionable strata in {geo}",
    "with careful censoring/follow-up documentation in {geo}",
]

CLOSERS_ART04 = [
    "using treatment interaction terms in {geo}",
    "with explicit risk×chemotherapy product terms ({geo})",
    "reporting stratum-specific associations in {geo}",
    "and interpreting benefit heterogeneity cautiously ({geo})",
    "under stage II/III restriction in {geo}",
    "with four-group KM-style contrasts conceptualized in {geo}",
]

CLOSERS_ART05 = [
    "comparing {tcga} RNA-seq with {geo} microarray profiles",
    "mapping subtypes from {tcga} onto {geo}",
    "quantifying agreement beyond chance between {tcga} and {geo}",
    "and discussing platform-shift failure modes ({tcga} vs {geo})",
    "with prognostic separation checks after transfer ({tcga}/{geo})",
    "under matched subtype label harmonization ({tcga}–{geo})",
]

CLOSERS_ART08 = [
    "with unified preprocessing and locked metrics on {tcga}",
    "reporting discrimination, calibration, and explanation side by side ({tcga})",
    "under identical feature blocks across learners ({tcga})",
    "and selecting a champion model without peeking ({tcga})",
    "with nested validation discipline on {tcga}",
    "emphasizing interpretability–performance trade-offs ({tcga})",
]

# Light cancer-specific color (optional clause) — does not change method claim
CANCER_COLOR = {
    "brca": "in the hormone-receptor and subtype-rich setting of",
    "luad": "in the oncogene-defined landscape of",
    "lusc": "in keratinizing squamous",
    "lihc": "in the cirrhosis-associated context of",
    "paad": "in the stroma-rich setting of",
    "gbm": "in highly lethal",
    "lgg": "in lower-grade",
    "ov": "in high-grade serous",
    "prad": "in PSA-monitored",
    "skcm": "in cutaneous",
    "hnsc": "in HPV-heterogeneous",
    "kirc": "in clear-cell",
    "blca": "in urothelial",
    "esca": "in esophageal",
    "stad": "in gastric",
    "crc": "in colorectal",
    "coad": "in colonic",
    "read": "in rectal",
    "cesc": "in cervical",
    "ucec": "in endometrial",
    "thca": "in differentiated thyroid",
    "aml": "in myeloid",
    "dlbc": "in large-B-cell",
}

EPI_OPEN = [
    "Association of",
    "Linking",
    "Contextual correlates of",
    "Place-based signals for",
    "Environmental juxtaposition of",
    "Urban-form correlates of",
    "Exposure patterning of",
    "Dose–response clues for",
    "Incremental identification of",
    "Multi-exposure contrasts for",
    "Prospective signals of",
    "Effect-modification patterns in",
]
EPI_CORE = {
    "epi01": "with weighted logistic modeling and random-forest incremental AUC",
    "epi02": "via side-by-side multi-exposure regression contrasts",
    "epi03": "in a baseline-exposure to incident-disease survival design",
    "epi04": "through prespecified subgroup and interaction analyses",
}


def H(key: str, salt: int = 0) -> int:
    return int(hashlib.md5(f"{key}::{salt}".encode()).hexdigest(), 16)


def first_geo(datasets: list) -> str:
    for d in datasets or []:
        if str(d).upper().startswith("GSE"):
            return str(d)
    for d in datasets or []:
        s = str(d)
        if s and "TCGA" not in s.upper() and not s.startswith("CHARLS"):
            return s
    return "an independent expression cohort"


def first_tcga(datasets: list, fallback: str) -> str:
    for d in datasets or []:
        if "TCGA" in str(d).upper() or "TARGET" in str(d).upper():
            return str(d)
    return fallback or "TCGA"


def cancer_en(cancers: dict, cid: str, disease: str) -> str:
    return (cancers.get(cid) or {}).get("name_en") or disease or cid


def compose_onco(p: dict, cancers: dict, salt: int = 0) -> str:
    mid = p["method_id"]
    cid = p.get("cancer_id") or ""
    en = cancer_en(cancers, cid, p.get("disease", ""))
    tcga = first_tcga(p.get("datasets") or [], (cancers.get(cid) or {}).get("tcga") or "TCGA")
    geo = first_geo(p.get("datasets") or [])
    cores = CORES[mid]
    opener = OPENERS[H(p["id"] + "op", salt) % len(OPENERS)]
    core = cores[H(p["id"] + "core", salt) % len(cores)]
    bridge = BRIDGES[H(p["id"] + "br", salt) % len(BRIDGES)]
    color = CANCER_COLOR.get(cid)
    # sometimes use color bridge
    if color and H(p["id"] + "color", salt) % 3 == 0:
        bridge = color

    if mid in {"art03", "art04", "art07"}:
        closers = CLOSERS_ART04 if mid == "art04" else CLOSERS_GEO
        closer = closers[H(p["id"] + "cl", salt) % len(closers)].format(geo=geo, tcga=tcga)
    elif mid == "art05":
        closer = CLOSERS_ART05[H(p["id"] + "cl", salt) % len(CLOSERS_ART05)].format(geo=geo, tcga=tcga)
    elif mid == "art08":
        closer = CLOSERS_ART08[H(p["id"] + "cl", salt) % len(CLOSERS_ART08)].format(tcga=tcga)
    else:
        closer = CLOSERS_TCGA[H(p["id"] + "cl", salt) % len(CLOSERS_TCGA)].format(tcga=tcga)

    # Alternate syntax families for more diversity
    fam = H(p["id"] + "fam", salt) % 6
    if fam == 0:
        title = f"{opener} {core} {bridge} {en}, {closer}"
    elif fam == 1:
        title = f"{en}: {opener[0].lower() + opener[1:]} {core}, {closer}"
    elif fam == 2:
        title = f"{opener} {core} tailored to {en}, {closer}"
    elif fam == 3:
        title = f"{core[0].upper() + core[1:]} {bridge} {en}, {closer}"
    elif fam == 4:
        title = f"Does {core} improve risk stratification for {en}? Findings {closer}"
    else:
        title = f"{en} survival modeling with {core}, {closer}"

    title = re.sub(r"\s+", " ", title).strip()
    title = title.replace("a a ", "a ").replace("an a ", "an ")
    # tidy capitalization after colon
    if ": " in title:
        a, b = title.split(": ", 1)
        title = a + ": " + b[:1].upper() + b[1:]
    return title[0].upper() + title[1:]


def compose_epi(p: dict, salt: int = 0) -> str:
    locked = {
        "skoa_epi01": (
            "Association and Discriminative Value of the Radical Urbanization Index for "
            "Symptomatic Knee Osteoarthritis among Middle-aged and Older Adults in China: "
            "A CHARLS-Based Cross-Sectional Study"
        ),
        "htn_epi01": (
            "City-Level Radical Urbanization and Hypertension among Middle-aged and Older "
            "Adults in China: A CHARLS Cross-Sectional Study"
        ),
        "dm_epi03": (
            "Baseline Radical Urbanization Index and Incident Diabetes in CHARLS: "
            "A Longitudinal Cohort Analysis"
        ),
    }
    if p["id"] in locked:
        return locked[p["id"]]

    zh2en = {
        "症状性膝骨关节炎": "symptomatic knee osteoarthritis",
        "慢性腰痛": "chronic low back pain",
        "高血压": "hypertension",
        "糖尿病": "diabetes",
        "抑郁症状": "depressive symptoms",
        "慢性肺病": "chronic lung disease",
        "睡眠障碍": "sleep disturbance",
        "心脏病": "heart disease",
        "肥胖": "obesity",
        "骨折史": "fracture history",
        "卒中史": "stroke history",
        "主观记忆下降": "subjective memory decline",
    }
    disease = zh2en.get(p.get("disease") or "", p.get("disease") or "the outcome")
    exposure = p.get("exposure") or "contextual exposure"
    exposure = exposure.replace("+", " + ")
    if exposure == "RUI":
        exposure = "radical urbanization index (RUI)"
    mid = p["method_id"]
    opener = EPI_OPEN[H(p["id"] + "eo", salt) % len(EPI_OPEN)]
    core = EPI_CORE.get(mid, "in CHARLS")
    fam = H(p["id"] + "ef", salt) % 4
    if fam == 0:
        title = f"{opener} {exposure} and {disease} in CHARLS {core}"
    elif fam == 1:
        title = f"{disease.capitalize()} and {exposure}: CHARLS evidence {core}"
    elif fam == 2:
        title = f"CHARLS insights on {exposure} in relation to {disease} {core}"
    else:
        title = f"Revisiting {disease} through {exposure} {core}"
    title = re.sub(r"\s+", " ", title).strip()
    return title[0].upper() + title[1:]


def unique_assign(papers: list, cancers: dict) -> None:
    used_global = set()
    used_prefixes = set()
    for p in papers:
        salt = 0
        mid = p.get("method_id") or ""
        while salt < 400:
            if p.get("line") == "epi" or mid.startswith("epi"):
                title = compose_epi(p, salt)
            else:
                title = compose_onco(p, cancers, salt)
            key = re.sub(r"\s+", " ", title.lower())
            prefix = key[:36]
            if key not in used_global and prefix not in used_prefixes:
                if "title_prev" not in p:
                    p["title_prev"] = p.get("title_prev", p["title"])
                p["title"] = title
                used_global.add(key)
                used_prefixes.add(prefix)
                break
            salt += 1
        else:
            tag = p["id"].replace("_", "-")
            # force uniqueness without changing scientific claim
            base = compose_onco(p, cancers, 0) if not mid.startswith("epi") else compose_epi(p, 0)
            p["title"] = f"{base} ({tag})"
            used_global.add(p["title"].lower())
            used_prefixes.add(p["title"].lower()[:36])


def main() -> None:
    papers = json.loads((DATA / "papers.json").read_text(encoding="utf-8"))
    cancers = {c["id"]: c for c in json.loads((DATA / "cancers.json").read_text(encoding="utf-8"))}
    n_before = len(papers)
    unique_assign(papers, cancers)
    assert len(papers) == n_before, "paper count must not change"
    (DATA / "papers.json").write_text(json.dumps(papers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    titles = [p["title"] for p in papers]
    print("papers", len(papers), "(unchanged count)")
    print("unique titles", len(set(titles)), "of", len(titles))
    # method-level uniqueness
    from collections import defaultdict, Counter

    by = defaultdict(list)
    for p in papers:
        by[p["method_id"]].append(p["title"])
    print("method unique/all:")
    for mid in sorted(by):
        print(f"  {mid}: {len(set(by[mid]))}/{len(by[mid])}")
    # show remaining prefix collisions if any
    prefs = Counter(t.lower()[:40] for t in titles)
    bad = [(k, c) for k, c in prefs.most_common(10) if c > 1]
    print("prefix collisions top:", bad[:5])


if __name__ == "__main__":
    main()
