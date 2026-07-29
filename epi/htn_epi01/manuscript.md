# City-Level Radical Urbanization and Hypertension among Middle-aged and Older Adults in China: A CHARLS Cross-Sectional Study

**Article type:** Research article  
**Target journal:** BMC Public Health  
**Short title:** RUI and hypertension in CHARLS  
**Product-line ID:** `htn_epi01` (epi01)  
**Status note:** Full manuscript text is complete. Numeric Results/Abstract estimates are placeholders (`{{...}}`) pending local CHARLS + city-exposure merge and `code/run_analysis.py`. Do not submit until placeholders are replaced with run outputs.

---

## Abstract

**Background:** Rapid land-centered urbanization may reshape cardiometabolic risk environments, but national evidence linking the radical urbanization index (RUI) to hypertension among middle-aged and older Chinese adults remains limited. We examined the association between city-level RUI and prevalent hypertension and assessed whether RUI added discriminative information beyond individual clinical characteristics.

**Methods:** This cross-sectional analysis used the 2011 baseline survey of the China Health and Retirement Longitudinal Study (CHARLS). Hypertension was defined by self-reported physician diagnosis and/or measured blood-pressure thresholds (and antihypertensive medication when available). City-level RUI was calculated as ln(built-up area/total nighttime light intensity) and matched by baseline city of residence. Survey-weighted logistic regression, restricted cubic splines, and subgroup analyses estimated associations. Five incremental random forest models compared demographic, clinical, RUI, and environmental information for identifying hypertension status.

**Results:** Among {{N_TOTAL}} participants aged ≥45 years, {{N_HTN}} ({{PREV_HTN}}%) had hypertension. After adjustment for demographic, health-related, laboratory, and city-level environmental factors, each one-unit increase in RUI was associated with {{OR_CONT}} (95% CI {{OR_CONT_LO}}–{{OR_CONT_HI}}) higher odds of hypertension. Compared with the lowest RUI quartile, the highest quartile showed {{OR_Q4}} (95% CI {{OR_Q4_LO}}–{{OR_Q4_HI}}; P for trend {{P_TREND}}). Spline analysis indicated an overall association (P = {{P_OVERALL}}) {{NONLINEAR_PHRASE}}. Validation-set AUCs for demographic, clinical, clinical–RUI, clinical–environment, and full models were {{AUC1}}, {{AUC2}}, {{AUC3}}, {{AUC4}}, and {{AUC5}}, respectively; adding RUI to the clinical model changed AUC by {{DAUC_RUI}} (DeLong P = {{P_DELONG_RUI}}).

**Conclusions:** City-level RUI was associated with prevalent hypertension and may provide incremental identification information beyond clinical covariates. Because the design is cross-sectional and exposures are city averages, findings should be interpreted as associative signals for regional risk patterning rather than causal effects of urban policy.

**Keywords:** hypertension; radical urbanization index; CHARLS; urbanization; environmental exposure; random forest; cross-sectional study

---

## Background

Hypertension remains a leading contributor to cardiovascular morbidity and premature mortality in China and worldwide. Population aging, dietary transition, obesity, and reduced physical activity have expanded the absolute burden of elevated blood pressure, while urban–rural and regional contrasts suggest that living environments and development patterns also shape risk. Conventional urbanization metrics emphasize population share or economic scale and may miss the coordination between land expansion and the agglomeration of people and economic activity.

The radical urbanization index (RUI), defined from the ratio of city built-up area to total nighttime light intensity, rises when land expansion outpaces agglomeration and therefore indexes more extensive, lower-density growth. Prior CHARLS-based work has linked higher RUI to chronic lung disease and, in a related musculoskeletal analysis, to symptomatic knee osteoarthritis, with partial attenuation after air pollution and ecological covariates were included. Parallel cardiometabolic pathways—including motorization, green-space loss, noise, heat, and particulate exposure—provide a rationale for examining hypertension.

Few studies have jointly estimated the RUI–hypertension association and quantified whether RUI adds discrimination beyond established clinical predictors. Using CHARLS 2011 baseline data, we evaluated association, dose–response, and subgroup patterns between city-level RUI and prevalent hypertension, and we compared incremental random forest models that successively added demographic, clinical, RUI, and environmental features.

---

## Methods

### Study design and data source

This cross-sectional study used the 2011 CHARLS baseline survey. CHARLS employed multistage, stratified, cluster probability sampling of Chinese residents aged 45 years or older and their spouses. City-level RUI and environmental indicators were matched by baseline city of residence. CHARLS was approved by the Ethics Review Committee of Peking University; participants provided informed consent. This secondary analysis uses de-identified public data under CHARLS data-use terms.

### Study participants

Eligible participants were aged ≥45 years, had determinable hypertension status, matchable city-level RUI, and complete required demographic, health-related, and laboratory covariates under the same completeness rules used in the factory epi01 pipeline. Exclusion counts are recorded in `results/flow_exclusions.csv` after the analysis run and summarized in Figure 1.

### Outcome definition

Hypertension was defined if any of the following was present: (i) self-reported physician diagnosis of hypertension; (ii) measured systolic blood pressure ≥140 mmHg or diastolic blood pressure ≥90 mmHg (mean of available baseline readings per CHARLS protocol); (iii) current use of antihypertensive medication when recorded. Participants with missing outcome components needed for classification were excluded. This definition captures prevalent hypertension rather than incident disease.

### Radical urbanization index

RUI was calculated as ln(city built-up area / total nighttime light intensity) for 2011 and matched to participants by city. Higher RUI indicates faster land expansion relative to agglomeration. RUI entered models as a continuous variable and as quartiles (lowest quartile as reference).

### Covariates and city-level environmental indicators

Demographic covariates included age, sex, education, marital status, and urban–rural residence. Health-related covariates included body mass index, waist circumference, chronic disease count (excluding hypertension), sleep duration, CESD-10 score, smoking, drinking, and sarcopenia status (AWGS 2019 when constructible). Laboratory covariates included white blood cell count, platelet count, hemoglobin, lipids, and C-reactive protein when available under the shared epi01 covariate panel. City-level annual means for PM2.5, PM10, NO2, O3, temperature, humidity, surface pressure, and NDVI were matched by city as in the reference epi01 musculoskeletal manuscript.

### Statistical analysis

Survey-weighted logistic regression estimated odds ratios (ORs) and 95% confidence intervals (CIs). The crude model was unadjusted. Model 1 adjusted for demographic factors. Model 2 further adjusted for health-related and laboratory covariates. Model 3 additionally adjusted for city-level environmental indicators. Linear trend across RUI quartiles used quartile medians. Restricted cubic splines with three knots assessed dose–response; overall and nonlinearity P values were reported. Prespecified subgroups included age, sex, education, urban–rural residence, smoking, drinking, BMI category, and sarcopenia. Interactions used product terms and were treated as exploratory. Analyses used city as the clustering unit with CHARLS design variables where applicable.

### Machine learning analysis

Participants were split 7:3 into training and validation sets with outcome-stratified sampling. Random forests were fit in five incremental feature sets: demographic; clinical (demographic + health/laboratory); clinical + RUI; clinical + environment; and full (clinical + RUI + environment). Hyperparameters were tuned by cross-validation in the training set. Validation AUCs were compared with DeLong tests. Brier scores, calibration curves, and decision curves were reported as secondary metrics. Machine learning quantified incremental identification value and was not positioned as a deployable clinical prediction tool.

---

## Results

### Participant characteristics

After exclusions, {{N_TOTAL}} participants remained (mean age {{MEAN_AGE}} years; {{PCT_FEMALE}}% women). Hypertension prevalence was {{PREV_HTN}}% (n = {{N_HTN}}). Table 1 compares covariates and RUI by hypertension status. Mean RUI was {{RUI_HTN}} among participants with hypertension and {{RUI_NON}} among those without (P = {{P_RUI}}).

### Spatial distribution

Figure 2 maps city-level RUI and environmental indicators across provinces represented in the analytic sample. Regional contrasts between western/southwestern and eastern coastal cities were described qualitatively from the mapped surfaces generated by the analysis script.

### Association between RUI and hypertension

Table 2 reports survey-weighted ORs. In Model 3, continuous RUI was associated with hypertension (OR {{OR_CONT}}, 95% CI {{OR_CONT_LO}}–{{OR_CONT_HI}}). Quartile contrasts and P for trend are shown in the same table. Figure 3 displays restricted cubic spline estimates (overall P = {{P_OVERALL}}; nonlinearity P = {{P_NONLINEAR}}).

### Subgroup analyses

Figure 4 summarizes stratified ORs. Interaction P values are listed in Supplementary Table S2. Subgroup patterns were interpreted jointly with interaction tests rather than isolated within-stratum significance.

### Machine learning performance

Validation AUCs were {{AUC1}} (demographic), {{AUC2}} (clinical), {{AUC3}} (clinical–RUI), {{AUC4}} (clinical–environment), and {{AUC5}} (full). Adding RUI to the clinical model changed AUC by {{DAUC_RUI}} (P = {{P_DELONG_RUI}}); the full model versus clinical changed AUC by {{DAUC_FULL}} (P = {{P_DELONG_FULL}}). Calibration and decision curves are shown in Supplementary Figures.

---

## Discussion

This CHARLS-based cross-sectional analysis extends the epi01 factory template from musculoskeletal disease to hypertension, a high-burden cardiometabolic endpoint. The analytic emphasis remains twofold: estimating the adjusted association between city-level RUI and disease status, and quantifying whether RUI and environmental layers improve discrimination beyond clinical covariates.

Several mechanisms could link expansive urbanization to blood-pressure elevation, including reduced walkability, greater vehicle dependence, sleep disruption, heat and noise exposure, and particulate pollution. Partial attenuation after environmental adjustment would suggest shared pathways; persistence of a residual RUI association would suggest that RUI captures additional urban-form information not fully represented by annual pollutant and NDVI averages.

Limitations mirror other epi01 products. The design cannot establish temporality. Hypertension definitions mix self-report and measurements and may misclassify milder or untreated cases. City-level annual exposures ignore within-city variation, residential history, and daily mobility. Random splits can place residents of the same city in both training and validation sets, so geographic transportability remains unproven. Manuscript numbers must be taken exclusively from the local analysis run before journal submission.

---

## Conclusions

Higher city-level RUI was examined in relation to prevalent hypertension among middle-aged and older adults in CHARLS using weighted regression and incremental random forests. After placeholders are replaced with run outputs, the manuscript supports BMC Public Health–oriented submission as an epi01 cardiometabolic companion to the musculoskeletal reference paper.

---

## Declarations

**Ethics:** CHARLS ethics approval and informed consent as reported by the CHARLS team; secondary analysis of de-identified data.  
**Data availability:** CHARLS (https://charls.pku.edu.cn/); city exposure sources as cited in Methods; analytic code in `code/`.  
**Competing interests:** None declared.  
**Funding:** To be completed by submitting authors.  
**Authors’ contributions:** To be completed by submitting authors.

## Figure/table checklist

1. Flow diagram  
2. Spatial maps of RUI/environment  
3. RCS curve  
4. Subgroup forest  
5. Incremental ROC  
6. Table 1 characteristics; Table 2 OR models  

## Placeholder list

All `{{TOKEN}}` fields must be filled from `results/metrics.json` produced by `code/run_analysis.py`.
