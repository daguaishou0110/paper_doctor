# Chronic low back pain and RUI + PM2.5 + NDVI: CHARLS evidence via side-by-side multi-exposure regression contrasts

**Article type:** Research article  
**Target journal:** BMC Public Health  
**Short title:** Multi-exposure contrasts for chronic low back pain  
**Product-line ID:** `lbp_epi02` (epi02)  
**Status note:** Full multi-exposure manuscript text is complete. Numeric estimates are placeholders pending CHARLS + city RUI/PM2.5/NDVI merge. Do not submit until placeholders are replaced.

---

## Abstract

**Background:** Urban expansion, air pollution, and greenness may jointly relate to chronic low back pain, yet single-exposure papers cannot show information overlap. We compared city-level RUI, PM2.5, and NDVI against chronic low back pain within one CHARLS analytic sample.

**Methods:** Using the 2011 CHARLS baseline and identical eligibility rules, we estimated survey-weighted logistic models for each exposure separately and in mutually adjusted specifications. Restricted cubic splines and incremental random forests summarized dose–response and discriminative contribution. Outcome definition: self-reported chronic low back pain using the CHARLS pain-site and duration items operationalized for this product line.

**Results:** Among {{N_TOTAL}} participants, {{N_EVENT}} ({{PREV}}%) had chronic low back pain. Mutually adjusted ORs were {{OR_RUI}} for RUI, {{OR_PM}} for PM2.5, and {{OR_NDVI}} for NDVI (95% CIs in Table 2). Incremental AUC changes when each exposure was added to the clinical block are reported as {{DAUC_RUI}}, {{DAUC_PM}}, and {{DAUC_NDVI}}.

**Conclusions:** Side-by-side modeling clarifies which contextual signal remains associated with chronic low back pain after co-adjustment. Cross-sectional city averages still preclude causal claims.

**Keywords:** chronic low back pain; RUI; PM2.5; NDVI; CHARLS; multi-exposure; STROBE

---

## Background

Contextual exposures are correlated: cities with aggressive land expansion often differ in pollution and vegetation. Reporting one exposure at a time can overstate unique associations. This epi02 product therefore compares RUI, PM2.5, and NDVI for chronic low back pain under a shared CHARLS sampling frame and outcome definition.

---

## Methods

Cross-sectional CHARLS 2011 design, ethics, and city matching follow the factory epi02 checklist. Participants met identical inclusion rules across exposures. Outcome: self-reported chronic low back pain using the CHARLS pain-site and duration items operationalized for this product line. Exposures: city-level RUI, annual PM2.5, and NDVI. Analyses included single-exposure and mutually adjusted weighted logistics, splines, and incremental RF AUCs. STROBE reporting applies.

---

## Results

Sample size {{N_TOTAL}}, events {{N_EVENT}} ({{PREV}}%). Table 1 shows characteristics; Table 2 contrasts single and joint models; Figures summarize splines and ROC increments. Primary joint-model continuous estimates: RUI OR {{OR_RUI}}, PM2.5 OR {{OR_PM}}, NDVI OR {{OR_NDVI}}.

---

## Discussion

Mutual adjustment and discrimination contrasts help readers judge overlapping versus residual contextual information for chronic low back pain. Limitations mirror epi01 (temporality, ecological exposure, self-report) with added collinearity among urban metrics.

---

## Conclusions

This multi-exposure epi02 manuscript is submission-ready in structure after metrics fill-in from `results/metrics.json`.

---

## Declarations

**Ethics / Data / Competing interests:** As for CHARLS secondary analyses.  
**Funding / Authors’ contributions:** To be completed.

## Placeholder list

Fill all `{{TOKEN}}` fields from the epi02 analysis run.
