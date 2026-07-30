# Association and Discriminative Value of the Radical Urbanization Index for Symptomatic Knee Osteoarthritis among Middle-aged and Older Adults in China: A CHARLS-Based Cross-Sectional Study

**Article type:** Research article  
**Target journal:** BMC Musculoskeletal Disorders  
**Short title:** RUI and symptomatic knee osteoarthritis  
**Product-line ID:** `skoa_epi01` (epi01)  
**Status note:** Numeric estimates below are taken from the completed case manuscript `case/BMC_Musculoskeletal_Disorders_main_manuscript(1).docx` (CHARLS 2011 analysis already reported). Local re-run requires placing CHARLS + city RUI tables under `data/`.

---

## Abstract

**Background:** We examined the association between the city-level radical urbanization index (RUI) and symptomatic knee osteoarthritis (sKOA) among middle-aged and older adults in China and assessed whether RUI and environmental indicators added discriminative information beyond individual clinical characteristics.

**Methods:** This cross-sectional analysis used the 2011 baseline survey of CHARLS. sKOA was defined as concurrent self-reported physician-diagnosed arthritis and knee pain. RUI was calculated as ln(city built-up area/total nighttime light intensity) and matched by baseline city of residence. Survey-weighted logistic regression, restricted cubic splines, subgroup analyses, and incremental random-forest models were used.

**Results:** Of 8,022 participants, 762 had sKOA (9.50%). Mean RUI was higher in participants with sKOA (−4.56) than without (−4.94; P < 0.001). After adjustment for demographic, health-related, laboratory, and city-level environmental factors, each one-unit increase in RUI was associated with 33% higher odds of sKOA (OR = 1.33, 95% CI: 1.16–1.53, P < 0.001). Spline analysis showed a significant overall association (P < 0.001) without evidence of nonlinearity (P = 0.904). Validation-set AUCs for the demographic, clinical, clinical–RUI, clinical–environment, and full models were 0.620, 0.714, 0.737, 0.741, and 0.754, respectively. Adding RUI to the clinical model improved AUC by 0.023 (DeLong P = 0.045); the full model improved AUC by 0.040 (P = 0.0046).

**Conclusions:** Higher RUI was associated with increased odds of sKOA and provided incremental information beyond individual clinical characteristics. Findings are associative given the cross-sectional design and city-average exposures.

**Keywords:** knee osteoarthritis; symptomatic knee osteoarthritis; radical urbanization index; CHARLS; environmental exposure; random forest; cross-sectional study

---

## Background

Knee osteoarthritis is a leading cause of pain and disability in aging populations. Rapid urbanization in China has reshaped built environments, air quality, and activity patterns that may influence joint health. The radical urbanization index (RUI), constructed as the ratio of city built-up area to total nighttime light intensity, rises when land expansion outpaces agglomeration of people and economic activity. Using CHARLS 2011, this study evaluated the RUI–sKOA association and the incremental discriminative value of RUI and environmental indicators.

---

## Methods

### Study design and data source

Cross-sectional analysis of the 2011 CHARLS national baseline. City-level RUI and environmental indicators were matched by baseline city of residence. CHARLS ethics approval and informed consent apply; this secondary analysis uses de-identified data.

### Participants

From 17,708 baseline individuals, sequential exclusions for age <45, missing sKOA, unmatchable RUI, and incomplete covariates yielded the analytic sample of 8,022.

### Outcome and exposure

sKOA: physician-diagnosed arthritis plus current knee pain. RUI (2011): ln(built-up area / total nighttime light intensity), continuous and quartile-coded. Environmental covariates included PM2.5, PM10, NO2, O3, meteorology, and NDVI.

### Statistical analysis

Survey-weighted logistic models (crude through fully adjusted), trend tests, restricted cubic splines, subgroups, and five incremental random-forest models with DeLong AUC comparisons. STROBE reporting.

---

## Results

Among 8,022 participants, 762 (9.50%) had sKOA. Mean RUI was −4.56 in sKOA versus −4.94 in non-sKOA (P < 0.001). Fully adjusted continuous OR = 1.33 (95% CI 1.16–1.53). Quartile contrasts and spatial maps are detailed in the case manuscript tables/figures. Spline: overall P < 0.001; nonlinearity P = 0.904. Validation AUCs: 0.620 / 0.714 / 0.737 / 0.741 / 0.754 for demographic → full models; ΔAUC clinical→clinical-RUI = +0.023 (P = 0.045); clinical→full = +0.040 (P = 0.0046).

---

## Discussion

Higher city-level RUI was positively associated with prevalent sKOA and added modest discrimination beyond clinical features. Limitations include cross-sectional temporality, self-report outcome error, and ecological exposure misclassification. Full narrative, subgroup forests, and calibration plots are in the BMC case file.

---

## Conclusions

Higher RUI was associated with increased odds of sKOA among middle-aged and older adults in China; RUI and environmental indicators provided incremental information beyond clinical variables.

---

## Declarations

**Ethics:** Peking University CHARLS ethics approval; informed consent obtained in the parent study.  
**Data availability:** CHARLS https://charls.pku.edu.cn/ (registration required). City exposure sources as cited in the case manuscript.  
**Competing interests:** None declared.

## Source of numbers

`results/metrics.json` mirrored from `case/BMC_Musculoskeletal_Disorders_main_manuscript(1).docx`.
