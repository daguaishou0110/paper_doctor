# Baseline Radical Urbanization Index and Incident Diabetes in CHARLS: A Longitudinal Cohort Analysis

**Article type:** Research article  
**Target journal:** BMC Public Health  
**Short title:** Baseline RUI and incident diabetes  
**Product-line ID:** `dm_epi03` (epi03)  
**Status note:** Full longitudinal manuscript text is complete. Sample sizes, person-time, and hazard ratios are placeholders (`{{...}}`) pending multi-wave CHARLS cleaning and `code/run_analysis.py`. Do not submit until placeholders are replaced.

---

## Abstract

**Background:** Cross-sectional studies suggest that city-level radical urbanization may correlate with cardiometabolic conditions, but temporality remains uncertain. We evaluated whether baseline radical urbanization index (RUI) was associated with incident diabetes among middle-aged and older adults in the China Health and Retirement Longitudinal Study (CHARLS).

**Methods:** We assembled a prospective cohort from CHARLS participants without diabetes at the 2011 baseline who had matchable city-level RUI and complete baseline covariates required by the epi03 pipeline. Incident diabetes during follow-up waves was defined by newly reported physician diagnosis and/or newly elevated glucose/medication criteria when available. Survey-weighted Cox models (or discrete-time logit models if tied wave timing dominated) estimated hazard ratios (HRs) per unit RUI and across RUI quartiles. Restricted cubic splines and subgroup analyses evaluated dose–response and heterogeneity. Sensitivity analyses varied outcome definitions and excluded early events.

**Results:** Among {{N_AT_RISK}} participants free of baseline diabetes, {{N_EVENTS}} incident cases occurred over {{PERSON_YEARS}} person-years (incidence {{IR}} per 1000 person-years). In the fully adjusted model, each one-unit higher baseline RUI was associated with HR {{HR_CONT}} (95% CI {{HR_CONT_LO}}–{{HR_CONT_HI}}). The highest versus lowest RUI quartile yielded HR {{HR_Q4}} (95% CI {{HR_Q4_LO}}–{{HR_Q4_HI}}; P for trend {{P_TREND}}). Spline tests showed overall association P = {{P_OVERALL}} and nonlinearity P = {{P_NONLINEAR}}. Subgroup interaction findings are summarized in Figure 4.

**Conclusions:** This longitudinal epi03 product tests whether baseline urban-expansion quality precedes new diabetes. Causal interpretation still requires careful handling of time-varying confounding, migration, and outcome ascertainment; after numeric fill-in, the paper is oriented to BMC Public Health.

**Keywords:** diabetes; incident diabetes; radical urbanization index; CHARLS; longitudinal cohort; urbanization

---

## Background

Diabetes prevalence in China has risen with aging and lifestyle transition. Environmental and urban-form exposures are increasingly examined as contextual contributors alongside obesity, diet, and physical inactivity. The radical urbanization index (RUI) summarizes imbalance between built-up land expansion and nighttime-light agglomeration. Cross-sectional CHARLS analyses can identify associations with prevalent disease but cannot order exposure and outcome.

Longitudinal CHARLS waves allow exclusion of baseline diabetes and ascertainment of new cases, strengthening temporal inference relative to epi01 cross-sectional templates. This study therefore estimates the association between baseline city-level RUI and incident diabetes, with dose–response and subgroup analyses aligned to the factory epi03 checklist.

---

## Methods

### Study design and data source

We conducted a prospective cohort analysis using CHARLS baseline (2011) and subsequent follow-up waves available under the local data license. Ethics and consent follow the CHARLS parent study. City-level RUI and environmental covariates were assigned using baseline city of residence; sensitivity analyses restricted to non-movers when migration variables were available.

### Study participants

Participants were aged ≥45 years at baseline, free of diabetes at baseline under the primary definition, had matchable RUI, and had complete baseline covariates. Figure 1 reports sequential exclusions after the analysis run (`results/flow_exclusions.csv`).

### Outcome definition

**Baseline diabetes (exclusion):** self-reported physician diagnosis, and/or glucose/HbA1c thresholds, and/or glucose-lowering medication when available.  
**Incident diabetes:** first follow-up wave meeting diabetes criteria among those baseline-negative. Wave timing defined survival time from baseline interview to event wave midpoint or censoring at last wave/death/loss to follow-up per CHARLS identifiers available locally.

### Exposure

Baseline (2011) city-level RUI = ln(built-up area / total nighttime light intensity), analyzed continuously and as quartiles.

### Covariates

Baseline demographic factors (age, sex, education, marital status, urban–rural residence), health behaviors (smoking, drinking, sleep), adiposity (BMI, waist), depressive symptoms (CESD-10), sarcopenia construct when available, and selected laboratory markers. City-level environmental annual means (PM2.5, PM10, NO2, O3, meteorology, NDVI) entered the final adjustment set as in epi01, recognizing that they may mediate or confound urban-form associations.

### Statistical analysis

Primary analysis used survey-weighted Cox proportional hazards models with city clustering when design variables permitted; Schoenberg/proportional-hazards checks and discrete-time alternatives were documented in the analysis log if needed. Models paralleled epi01 adjustment depth: crude; demographic; + health/laboratory; + city environment. Trend tests used quartile medians. Restricted cubic splines with three knots described dose–response. Prespecified subgroups included age, sex, urban–rural residence, education, and BMI category. Sensitivity analyses: (i) diagnosis-only outcome; (ii) excluding events in the first follow-up interval; (iii) complete-case versus covariate multiple imputation if implemented; (iv) restriction to participants without inter-city migration.

Machine learning incremental AUC modules are optional for epi03 and were not required for the primary longitudinal claim; if run, they are confined to baseline discrimination of later incidence and reported only as exploratory.

---

## Results

### Cohort and follow-up

After exclusions, {{N_AT_RISK}} participants were followed; {{N_EVENTS}} incident diabetes events accrued ({{PERSON_YEARS}} person-years; incidence {{IR}}/1000 person-years). Table 1 shows baseline characteristics by RUI quartile.

### Primary association

Table 2 presents HRs for continuous RUI and quartiles across adjustment models. Fully adjusted continuous HR was {{HR_CONT}} (95% CI {{HR_CONT_LO}}–{{HR_CONT_HI}}). Quartile estimates and P for trend {{P_TREND}} appear in the same table. Figure 2 shows cumulative incidence by RUI quartile; Figure 3 shows spline curves.

### Subgroups and sensitivity

Figure 4 and Supplementary Table S2 report stratified HRs and interactions. Sensitivity estimates are listed in Supplementary Table S3.

---

## Discussion

This epi03 manuscript supplies the longitudinal counterpart to cross-sectional RUI–disease products. Demonstrating that baseline RUI precedes incident diabetes would strengthen the public-health interpretation of urban-expansion quality beyond prevalent-disease correlations. Residual confounding by diet, physical activity detail, and healthcare access remains possible. City-level exposure assignment and wave-based outcome timing introduce classical misclassification. Migration and time-varying pollution were only partly addressable with CHARLS geography. Placeholder replacement with local run outputs is mandatory before submission.

---

## Conclusions

We specified a CHARLS longitudinal analysis of baseline RUI and incident diabetes with STROBE-oriented reporting. After numeric fill-in from the analysis pipeline, the paper is positioned for BMC Public Health as the factory’s epi03 demonstration case.

---

## Declarations

**Ethics / data / competing interests / funding / contributions:** as in epi01 companion packages; complete before submission.

## Placeholder list

Fill all `{{TOKEN}}` fields from `results/metrics.json` after `code/run_analysis.py`.
