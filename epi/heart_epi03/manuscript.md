# Heart disease and radical urbanization index (RUI): CHARLS evidence in a baseline-exposure to incident-disease survival design

**Article type:** Research article  
**Target journal:** BMC Public Health  
**Short title:** Baseline radical urbanization index (RUI) and incident heart disease  
**Product-line ID:** `heart_epi03` (epi03)  
**Status note:** Full longitudinal manuscript text is complete. Sample sizes, person-time, and HRs are placeholders pending multi-wave CHARLS cleaning. Yellow-feasibility cards must lock outcome/follow-up definitions before numeric fill-in.

---

## Abstract

**Background:** Cross-sectional signals linking contextual exposures to heart disease cannot establish temporality. We evaluated whether baseline city-level radical urbanization index (RUI) was associated with incident heart disease in CHARLS.

**Methods:** We formed a prospective cohort of participants free of heart disease at the 2011 baseline, with matchable exposure and covariates. Incident events during follow-up waves used the same clinical logic as the cross-sectional definition where applicable (self-reported heart disease), applied to new-onset coding. Survey-weighted Cox or discrete-time models estimated HRs per unit exposure and across quartiles, with splines and subgroups.

**Results:** Among {{N_AT_RISK}} participants at risk, {{N_EVENTS}} incident cases occurred over {{PERSON_YEARS}} person-years (incidence {{IR}} per 1000 person-years). Fully adjusted HR per unit exposure was {{HR_CONT}} (95% CI {{HR_CONT_LO}}–{{HR_CONT_HI}}). Q4 versus Q1 HR was {{HR_Q4}} (95% CI {{HR_Q4_LO}}–{{HR_Q4_HI}}; P-trend {{P_TREND}}).

**Conclusions:** This epi03 product tests whether baseline contextual exposure precedes new heart disease. Causal reading still requires care with time-varying confounding, migration, and ascertainment.

**Keywords:** heart disease; incidence; CHARLS; longitudinal cohort; urbanization; environmental exposure

---

## Background

Longitudinal CHARLS waves allow exclusion of baseline disease and ascertainment of new cases, strengthening temporal inference relative to epi01 templates for heart disease.

---

## Methods

### Design

Prospective cohort from CHARLS baseline (2011) and subsequent waves available under the local license. Ethics follow the parent study.

### Participants

Age ≥45 years, free of heart disease at baseline, matchable city-level radical urbanization index (RUI), complete baseline covariates. Flow exclusions in Figure 1.

### Outcome and exposure

Incident heart disease as first follow-up meeting criteria derived from: self-reported heart disease. Baseline exposure: city-level radical urbanization index (RUI).

### Analysis

Weighted Cox/discrete-time models, quartiles, trend tests, splines, subgroups, and sensitivity analyses excluding early events or movers. STROBE cohort checklist.

---

## Results

At-risk n={{N_AT_RISK}}, events={{N_EVENTS}}, person-years={{PERSON_YEARS}}, IR={{IR}}. Adjusted HR={{HR_CONT}} ({{HR_CONT_LO}}–{{HR_CONT_HI}}). Quartile and spline results as in Tables/Figures after fill-in.

---

## Discussion

Temporality is improved versus cross-sectional epi01, but wave-based ascertainment and city-average exposures remain limitations. Yellow cards should finalize operational definitions before claiming submission readiness.

---

## Conclusions

Structure-complete epi03 manuscript; replace placeholders via `code/run_analysis.py` before any journal submission.

---

## Declarations

**Ethics / Data / Competing interests:** CHARLS secondary analysis standards.  
**Funding / Authors’ contributions:** To be completed.

## Placeholder list

`{{N_AT_RISK}}`, `{{N_EVENTS}}`, `{{PERSON_YEARS}}`, `{{IR}}`, `{{HR_*}}`, `{{P_*}}` from longitudinal metrics JSON.
