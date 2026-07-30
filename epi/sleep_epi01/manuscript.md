# Revisiting sleep disturbance through radical urbanization index (RUI) with weighted logistic modeling and random-forest incremental AUC

**Article type:** Research article  
**Target journal:** BMC Public Health  
**Short title:** radical urbanization index (RUI) and sleep disturbance in CHARLS  
**Product-line ID:** `sleep_epi01` (epi01)  
**Status note:** Full STROBE manuscript text is complete. Numeric Results/Abstract estimates are placeholders (`{{...}}`) pending local CHARLS + city-exposure merge and `code/run_analysis.py`. Do not submit until placeholders are replaced with run outputs. Do not treat this file alone as a finished submission package.

---

## Abstract

**Background:** Contextual urban and environmental exposures may shape mental health risk among middle-aged and older adults, but national evidence linking city-level radical urbanization index (RUI) to sleep disturbance in China remains limited. We examined the association between city-level radical urbanization index (RUI) and sleep disturbance in the China Health and Retirement Longitudinal Study (CHARLS) and assessed whether the exposure added discriminative information beyond individual characteristics.

**Methods:** This cross-sectional analysis used the 2011 CHARLS baseline. Sleep disturbance was defined as sleep disturbance defined from CHARLS sleep-duration and/or sleep-quality items under a pre-specified rule. City-level radical urbanization index (rui) was matched by baseline city of residence. Survey-weighted logistic regression, restricted cubic splines, and pre-specified subgroups estimated associations. Incremental random-forest models compared demographic, clinical, exposure, and multi-environment feature sets for identifying outcome status on a held-out validation set.

**Results:** Among {{N_TOTAL}} participants aged ≥45 years, {{N_EVENT}} ({{PREV}}%) met the sleep disturbance definition. After multivariable adjustment, each one-unit increase in the primary continuous exposure was associated with OR {{OR_CONT}} (95% CI {{OR_CONT_LO}}–{{OR_CONT_HI}}). The highest versus lowest exposure quartile showed OR {{OR_Q4}} (95% CI {{OR_Q4_LO}}–{{OR_Q4_HI}}; P for trend {{P_TREND}}). Spline analysis indicated an overall association (P = {{P_OVERALL}}) {{NONLINEAR_PHRASE}}. Validation-set AUCs for the incremental models were {{AUC_BASE}} (clinical baseline) and {{AUC_FULL}} (full model); the change in AUC was {{DAUC}}.

**Conclusions:** City-level radical urbanization index (rui) was associated with sleep disturbance in CHARLS under a STROBE-aligned epi01 template. Because the design is cross-sectional and exposures are city averages, findings should be interpreted as associative signals for regional risk patterning rather than causal effects of urban or environmental policy.

**Keywords:** sleep disturbance; CHARLS; urbanization; environmental exposure; weighted logistic regression; random forest; cross-sectional study

---

## Background

Sleep disturbance contributes substantially to disability and healthcare use in aging populations. Individual behavioral and clinical factors do not fully explain geographic variation, motivating attention to urban form, air pollution, and greenness as contextual correlates. The radical urbanization index (RUI), particulate matter, and vegetation indices capture complementary aspects of land expansion, industrial activity, and ecological amenity.

Few studies have jointly estimated the association between city-level radical urbanization index (RUI) and sleep disturbance while quantifying incremental discrimination beyond established individual predictors. Using CHARLS 2011 baseline data, we evaluated association, dose–response, and subgroup patterns, and we compared incremental machine-learning models that successively added demographic, clinical, and environmental features.

---

## Methods

### Study design and data source

This cross-sectional study used the 2011 CHARLS baseline survey. CHARLS employed multistage stratified probability sampling of Chinese residents aged 45 years or older and their spouses. City-level exposures were matched by baseline city of residence. CHARLS was approved by the Ethics Review Committee of Peking University; participants provided informed consent. This secondary analysis uses de-identified data under CHARLS data-use terms.

### Study participants

Adults aged ≥45 years with complete outcome coding, matchable city exposure, and complete covariates required by the epi01 pipeline were included. Sequential exclusions are reported in Figure 1 after the analysis run (`results/flow_exclusions.csv`).

### Outcome definition

Primary outcome: sleep disturbance defined from CHARLS sleep-duration and/or sleep-quality items under a pre-specified rule. Sensitivity definitions varying thresholds or self-report-only coding are pre-specified in the analysis config.

### Exposure

Primary exposure: city-level radical urbanization index (RUI), analyzed continuously and as quartiles. When multiple environmental covariates were available, models adjusted for co-exposures as specified in the product card.

### Covariates

Demographic (age, sex, education, marital status, urban/rural), health-behavior (smoking, drinking, physical activity when available), clinical (BMI, comorbidities relevant to sleep disturbance), and city-level environmental covariates were entered in nested models.

### Statistical analysis

Survey weights were applied in logistic models. We estimated continuous and quartile associations, tests for trend, restricted cubic splines, and pre-specified subgroup interactions. Incremental random forests compared held-out AUCs across feature blocks. Two-sided α = 0.05 guided reporting without claiming confirmatory multiplicity control for exploratory subgroups. Analyses follow STROBE for cross-sectional studies.

---

## Results

Among {{N_TOTAL}} eligible participants, {{N_EVENT}} ({{PREV}}%) had sleep disturbance. Table 1 summarizes weighted characteristics across exposure quartiles. In the fully adjusted model, the continuous exposure OR was {{OR_CONT}} (95% CI {{OR_CONT_LO}}–{{OR_CONT_HI}}), and Q4 versus Q1 OR was {{OR_Q4}} (95% CI {{OR_Q4_LO}}–{{OR_Q4_HI}}; P-trend {{P_TREND}}). Figure 2 shows the spline; Figure 3 shows subgroup estimates; Figure 4 shows incremental ROC curves (AUC {{AUC_BASE}} → {{AUC_FULL}}, ΔAUC {{DAUC}}).

---

## Discussion

This epi01 analysis frames city-level radical urbanization index (RUI) as a contextual correlate of sleep disturbance in a nationally relevant aging cohort. Strengths include survey weighting, dose–response modeling, and discrimination checks. Limitations include cross-sectional temporality, city-average exposure misclassification, self-report outcome error, and residual confounding. After numeric fill-in, the manuscript is oriented to BMC Public Health or related Q2–Q3 public-health venues.

---

## Conclusions

City-level radical urbanization index (rui) was examined in relation to sleep disturbance among middle-aged and older adults in CHARLS using weighted regression and incremental random forests. Submission should proceed only after `results/metrics.json` replaces all placeholders.

---

## Declarations

**Ethics:** CHARLS parent-study approval and consent; secondary de-identified analysis.  
**Data availability:** CHARLS (https://charls.pku.edu.cn/); city exposure sources as cited in Methods; analytic code under `code/`.  
**Competing interests:** None declared.  
**Funding / Authors’ contributions:** To be completed by submitting authors.

## Figure/table checklist

1. Flow diagram  
2. Exposure maps (optional)  
3. RCS curve  
4. Subgroup forest  
5. Incremental ROC  
6. Table 1; Table 2 OR models  

## Placeholder list

All `{{TOKEN}}` fields must be filled from `results/metrics.json` produced by `code/run_analysis.py` (shared pipeline: `公卫队列/_lib/epi_pipeline.py`).
