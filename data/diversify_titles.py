# -*- coding: utf-8 -*-
"""Diversify homogeneous shelf titles: multiple templates per method_id, stable per paper id."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

DATA = Path(__file__).resolve().parent

# Placeholders: {cancer} {tcga} {geo} {endpoint}
# Keep scientific accuracy; vary syntax / emphasis / subtitle style.

TITLE_BANK = {
    "art01": [
        "Development and Cross-Cohort Validation of a Clinical–Transcriptomic Prognostic Model for {cancer}: A TRIPOD-Aligned Analysis of {tcga}",
        "Integrating Clinical Covariates with Transcriptomic Profiles to Predict Overall Survival in {cancer}: External Validation Using {tcga} and Independent Cohorts",
        "A TRIPOD-Aligned Survival Model Combining Clinical Features and Gene Expression for {cancer} Overall Survival ({tcga})",
        "Beyond Clinicopathologic Staging: Clinical Plus Transcriptome Risk Modeling for {cancer} with Cross-Cohort Validation",
        "Building an Integrative Clinical–Transcriptomic Risk Score for {cancer} Overall Survival: Derivation in {tcga} and Independent Testing",
        "Can Transcriptomic Features Improve Clinical Prognostication in {cancer}? A Cross-Cohort TRIPOD-Style Evaluation Based on {tcga}",
        "Overall Survival Stratification in {cancer} Using Joint Clinical–Transcriptomic Modeling: Lessons from {tcga}",
        "An Externally Checked Clinical–Expression Prognostic Framework for {cancer} Developed in {tcga}",
        "Refining {cancer} Prognosis with Transcriptomic Features on Top of Clinical Baselines: Cross-Cohort Evidence",
        "Clinical Variables Meet Gene Expression for {cancer} Survival Prediction: A Locked Training–Validation Pipeline around {tcga}",
    ],
    "art02": [
        "Development and Cross-Cohort Validation of a Clinical–Genomic Prognostic Model for {cancer}: Integrating Somatic Mutations, Tumor Mutational Burden, and MMR Status",
        "Somatic Mutation Burden, MMR Status, and Clinical Variables Jointly Stratify Overall Survival in {cancer}: A {tcga}-Based Genomic Prognostic Framework",
        "From Mutations to Risk: Combining TMB, MMR, and Clinicopathologic Factors for {cancer} Overall Survival Prediction",
        "Incremental Prognostic Value of Genomic Alterations Beyond Staging in {cancer}: A Clinical–Genomic Model Derived from {tcga}",
        "A Mutation-Informed Clinical Model for {cancer} Overall Survival Incorporating TMB and MMR/MSI Indicators",
        "Clinical Plus Genomic Features for {cancer} Prognosis: Cross-Cohort Assessment of Driver Mutations, TMB, and DNA Repair Status",
    ],
    "art03": [
        "A Clinical–Transcriptomic Model for Recurrence-Free Survival in {cancer}: A TRIPOD-Aligned {geo} Cohort Study",
        "Predicting Recurrence-Free Survival in {cancer} with Clinical Variables and Expression Signatures: Insights from {geo}",
        "Transcriptome-Augmented Clinical Modeling of {cancer} Recurrence Risk in the {geo} Cohort",
        "Who Relapses Earlier? A Clinical–Expression Framework for {cancer} Recurrence-Free Survival Using {geo}",
        "Deriving a Recurrence-Oriented Clinical–Transcriptomic Score for {cancer}: Internal Validation in {geo}",
        "Expression-Informed Clinical Stratification of Recurrence-Free Survival among Patients with {cancer} ({geo})",
    ],
    "art04": [
        "Transcriptomic Risk Score and Adjuvant Chemotherapy Benefit in Stage II/III {cancer}: A Treatment-Interaction Analysis in {geo}",
        "Does High Transcriptomic Risk Predict Greater Adjuvant Chemotherapy Benefit in Stage II/III {cancer}? An Interaction Analysis Using {geo}",
        "Risk × Treatment Interaction between an Expression-Based Score and Adjuvant Chemotherapy in Stage II/III {cancer}",
        "Heterogeneous Adjuvant Chemotherapy Benefit by Transcriptomic Risk Strata in Stage II/III {cancer}: Evidence from {geo}",
        "Mapping Who Benefits: Transcriptomic Risk Modifying Adjuvant Chemotherapy Associations in Stage II/III {cancer}",
        "Treatment-Effect Heterogeneity for Adjuvant Chemotherapy in Stage II/III {cancer} According to an Expression Risk Score ({geo})",
    ],
    "art05": [
        "Cross-Platform Validation of Consensus Molecular Subtypes in {cancer}: {tcga} RNA-Seq versus {geo} Microarray",
        "How Stable Are Molecular Subtypes of {cancer} across RNA-Seq and Microarray? A Cross-Platform Concordance Study ({tcga} vs {geo})",
        "Transferring Consensus Subtypes of {cancer} from RNA-Seq to Microarray: Agreement, Failure Modes, and Prognostic Separation",
        "Platform Shift Robustness of {cancer} Molecular Classification: Comparing {tcga} Transcriptomes with {geo} Arrays",
        "Concordance and Prognostic Consistency of {cancer} Subtypes Mapped between Sequencing and Array Platforms",
        "Reproducibility of Consensus Molecular Classes in {cancer} under Cross-Platform Gene Expression Measurement",
    ],
    "art06": [
        "A Clinical–Immune–Genomic Prognostic Model for {cancer} Overall Survival: Integrating IFN-γ Signature, Tumor Mutational Burden, and MMR Status in {tcga}",
        "Immune Activation, Mutational Burden, and MMR Status Jointly Inform {cancer} Overall Survival: An Integrative {tcga} Model",
        "Layering IFN-γ Programs with TMB/MMR on Clinical Baselines for {cancer} Prognosis",
        "An Immuno-Genomic Clinical Score for {cancer} Overall Survival Combining Interferon Signaling and Genomic Instability Indicators",
        "Do Immune and Genomic Markers Add Prognostic Information beyond Clinical Factors in {cancer}? A {tcga} Integrative Analysis",
        "Integrating IFN-γ Signature with TMB and MMR for Survival Stratification in {cancer}: Clinical Baseline Comparisons in {tcga}",
    ],
    "art07": [
        "Clinical–Transcriptomic Modeling of Recurrence-Free Survival in Stage II/III {cancer}: A TRIPOD-Aligned {geo} Cohort Study",
        "Stage II/III–Restricted Recurrence Modeling in {cancer}: Clinical versus Clinical–Transcriptomic Approaches in {geo}",
        "Focusing on Intermediate-Stage Disease: Expression-Augmented Recurrence Prediction for Stage II/III {cancer}",
        "Recurrence-Free Survival among Stage II/III {cancer} Patients: Incremental Value of Transcriptomic Features over Clinical Factors ({geo})",
        "A Stage-Stratified Clinical–Expression Model for Recurrence Risk in Intermediate {cancer}",
        "Within Stage II/III {cancer}, Can Transcriptomics Refine Recurrence Risk beyond Standard Clinical Variables?",
    ],
    "art08": [
        "A Multi-Model Machine Learning Framework for {cancer} Overall Survival: Comparing Penalized Cox, Random Survival Forest, and Gradient Boosting",
        "Which Survival Learner Wins for {cancer}? Benchmarking Penalized Cox, RSF, and Boosting with Interpretable Feature Attribution",
        "Model Selection under Censoring: A Head-to-Head Comparison of Classical and Machine-Learning Survival Models in {cancer}",
        "From Cox to Ensembles: Systematic Comparison of Multi-Algorithm Survival Modeling for {cancer} Prognosis",
        "An Interpretable Multi-Algorithm Survival Benchmark for {cancer} Using Clinical–Omics Inputs and Locked Evaluation",
        "Penalized Cox versus Tree Ensembles for {cancer} Overall Survival: Discrimination, Calibration, and Explanation Trade-offs",
    ],
}

EPI_BANK = {
    "epi01": [
        "{exposure} and {disease} among Middle-aged and Older Adults in China: Association and Incremental Discrimination in CHARLS",
        "Linking {exposure} to {disease} in Aging Chinese Adults: Weighted Regression and Random-Forest Evidence from CHARLS",
        "Does {exposure} Help Identify {disease} beyond Individual Clinical Factors? A CHARLS Cross-Sectional Evaluation",
        "City-Level {exposure} in Relation to {disease}: Dose–Response, Subgroups, and Added Discriminative Value (CHARLS)",
        "Contextual Urban/Environmental Exposure and {disease}: A CHARLS Analysis Centered on {exposure}",
        "From Place to Phenotype: {exposure}, {disease}, and Incremental Machine-Learning Discrimination in CHARLS",
    ],
    "epi02": [
        "Comparing {exposure} in Relation to {disease}: A Multi-Exposure CHARLS Analysis",
        "Which Contextual Exposure Matters More for {disease}? Joint Assessment of {exposure} in CHARLS",
        "Urban Form, Pollution, and Greenness Side by Side: Multi-Exposure Contrasts for {disease} in CHARLS",
        "Disentangling Overlapping City-Level Exposures ({exposure}) for {disease} Odds in Midlife and Older Chinese Adults",
        "A Head-to-Head Multi-Exposure Comparison for {disease} Using CHARLS and City-Linked Environmental Layers",
        "Shared and Unique Signals of {exposure} for {disease}: Evidence from a CHARLS Multi-Exposure Design",
    ],
    "epi03": [
        "Baseline {exposure} and Incident {disease} in CHARLS: A Longitudinal Cohort Analysis",
        "Does Baseline {exposure} Precede New-Onset {disease}? Prospective Evidence from CHARLS Follow-up Waves",
        "Temporal Ordering of City-Level {exposure} and Incident {disease} among Middle-aged and Older Adults in CHARLS",
        "From Baseline Context to Later Disease: {exposure} and Incident {disease} in a CHARLS Cohort",
        "Longitudinal Risk of {disease} Associated with Baseline {exposure}: CHARLS Survival Analysis",
        "Prospective Association between Baseline {exposure} and Subsequent {disease} in CHARLS",
    ],
    "epi04": [
        "Age and Urban–Rural Heterogeneity in the Association between {exposure} and {disease}: A CHARLS Subgroup Analysis",
        "Where Is the Association Stronger? Effect Modification of {exposure}–{disease} Links by Age and Residence in CHARLS",
        "Exploring Prespecified Effect Modifiers of {exposure} and {disease} in Middle-aged and Older Chinese Adults",
        "Subgroup Patterns and Interaction Signals for {exposure} in Relation to {disease} (CHARLS)",
        "Heterogeneous Associations of {exposure} with {disease} across Demographic Strata in CHARLS",
        "Effect Modification Focus: How Age and Urbanicity Shape the {exposure}–{disease} Relationship in CHARLS",
    ],
}


def pick(templates: list[str], key: str) -> str:
    h = int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)
    return templates[h % len(templates)]


def first_geo(datasets: list) -> str:
    for d in datasets or []:
        if str(d).upper().startswith("GSE"):
            return str(d)
    for d in datasets or []:
        s = str(d)
        if s.upper().startswith("TCGA"):
            continue
        if s:
            return s
    return "an independent cohort"


def first_tcga(datasets: list, fallback: str) -> str:
    for d in datasets or []:
        if "TCGA" in str(d).upper():
            return str(d)
    return fallback or "TCGA"


def cancer_en(cancers: dict, pid_cancer: str, disease: str) -> str:
    c = cancers.get(pid_cancer) or {}
    return c.get("name_en") or disease or pid_cancer


def diversify_onco(p: dict, cancers: dict) -> str:
    mid = p["method_id"]
    bank = TITLE_BANK.get(mid)
    if not bank:
        return p["title"]
    en = cancer_en(cancers, p.get("cancer_id", ""), p.get("disease", ""))
    # Prefer shorter display names already used in titles when disease looks English-like
    if p.get("disease") and re.search(r"[A-Za-z]", p["disease"]) and len(p["disease"]) < 60:
        # many papers use disease=中文; keep en from cancers
        pass
    tcga = first_tcga(p.get("datasets") or [], (cancers.get(p.get("cancer_id") or "") or {}).get("tcga") or "TCGA")
    geo = first_geo(p.get("datasets") or [])
    tmpl = pick(bank, p["id"])
    title = tmpl.format(cancer=en, tcga=tcga, geo=geo, endpoint="OS", MSI="MSI")
    # fix accidental double hyphen artifacts from old titles style
    title = title.replace("--", "–").replace("IFN-$gamma$", "IFN-γ").replace("{MSI}", "MSI")
    return title


def diversify_epi(p: dict) -> str:
    mid = p["method_id"]
    # Keep locked manuscript titles for finished packages
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
    bank = EPI_BANK.get(mid)
    if not bank:
        return p["title"]
    exposure = p.get("exposure") or "contextual exposure"
    exposure = exposure.replace("+", ", ")
    if exposure == "RUI":
        exposure = "the radical urbanization index (RUI)"
    elif "RUI" in exposure:
        exposure = exposure.replace("RUI", "radical urbanization (RUI)")
    if exposure.startswith("PM"):
        exposure = f"city-level {exposure}"
    if "NDVI" in exposure and "green" not in exposure.lower():
        exposure = exposure.replace("NDVI", "greenness (NDVI)")
    disease = p.get("disease") or p.get("cancer_zh") or "the outcome"
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
    disease_en = zh2en.get(disease, disease)
    tmpl = pick(bank, p["id"])
    title = tmpl.format(exposure=exposure, disease=disease_en)
    # sentence case cleanup for embedded uncapitalized exposure mid-sentence is ok;
    # ensure leading capital
    if title:
        title = title[0].upper() + title[1:]
    # fix "Does the ... Help" style mid-caps
    title = title.replace(" Help Identify", " help identify")
    title = title.replace(" and Incremental", " and incremental")
    title = title.replace(" Weighted Regression", " weighted regression")
    title = title.replace(" Random-Forest", " random-forest")
    title = title.replace(" Association and", " association and")
    title = title.replace(" A CHARLS", " a CHARLS")
    title = title.replace(" A Multi-", " a multi-")
    title = title.replace(" A Longitudinal", " a longitudinal")
    title = title.replace(" A Head-", " a head-")
    title = title.replace(" Evidence from", " evidence from")
    title = title.replace(" Joint Assessment", " joint assessment")
    title = title.replace(" Prospective Evidence", " prospective evidence")
    title = title.replace(" Temporal Ordering", " temporal ordering")
    # re-capitalize first letter after cleanup
    if title:
        title = title[0].upper() + title[1:]
    return title


def main() -> None:
    papers_path = DATA / "papers.json"
    cancers_path = DATA / "cancers.json"
    papers = json.loads(papers_path.read_text(encoding="utf-8"))
    cancers = {c["id"]: c for c in json.loads(cancers_path.read_text(encoding="utf-8"))}

    changed = 0
    for p in papers:
        old = p["title"]
        if p.get("line") == "epi" or str(p.get("method_id", "")).startswith("epi"):
            new = diversify_epi(p)
        else:
            new = diversify_onco(p, cancers)
        if new != old:
            if "title_prev" not in p:
                p["title_prev"] = old
            p["title"] = new
            changed += 1

    papers_path.write_text(json.dumps(papers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    from collections import Counter

    onco = [p for p in papers if p.get("line") != "epi"]

    def skel(t: str) -> str:
        t = re.sub(r"TCGA-[A-Z0-9/]+", "TCGA-X", t)
        t = re.sub(r"GSE\d+", "GSEx", t)
        t = re.sub(r" for [^:]+", " for CANCER", t)
        t = re.sub(r" in [^:]+", " in CANCER", t)
        return t

    print("changed", changed, "/", len(papers))
    print("onco unique skeletons", len(set(skel(p["title"]) for p in onco)), "of", len(onco))
    print("top remaining collisions:")
    for s, c in Counter(skel(p["title"]) for p in onco).most_common(8):
        print(f"  {c:3d}  {s[:110]}")


if __name__ == "__main__":
    main()
