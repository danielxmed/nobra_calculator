"""
Khorana Risk Score for Venous Thromboembolism in Cancer Patients Models

Request and response models for Khorana Risk Score calculation.

References (Vancouver style):
1. Khorana AA, Kuderer NM, Culakova E, Lyman GH, Francis CW. Development and 
   validation of a predictive model for chemotherapy-associated venous 
   thromboembolism. Blood. 2008;111(10):4902-7.
2. Ay C, Dunkler D, Marosi C, Chiriac AL, Vormittag R, Simanek R, et al. 
   Prediction of venous thromboembolism in cancer patients. Blood. 
   2010;116(24):5377-82.
3. Verso M, Agnelli G, Barni S, Gasparini G, LaBianca R. A modified Khorana 
   risk assessment score for venous thromboembolism in cancer patients 
   receiving chemotherapy: the Protecht score. Intern Emerg Med. 2012;7(3):291-2.
4. Mulder FI, Candeloro M, Kamphuisen PW, Di Nisio M, Bossuyt PM, Guman N, et al. 
   The Khorana score for prediction of venous thromboembolism in cancer patients: 
   a systematic review and meta-analysis. Haematologica. 2019;104(6):1277-1287.

The Khorana Risk Score is a validated clinical prediction tool designed to identify 
cancer patients at high risk for venous thromboembolism (VTE) during chemotherapy. 
VTE is a significant cause of morbidity and mortality in cancer patients, occurring 
in approximately 4-20% of patients depending on cancer type and treatment.

The score incorporates five easily obtainable clinical and laboratory variables:
1. Cancer type (stratified by VTE risk)
2. Pre-chemotherapy platelet count
3. Hemoglobin level or use of erythropoiesis-stimulating agents
4. Pre-chemotherapy leukocyte count
5. Body mass index

This tool is specifically designed for:
- Cancer patients starting chemotherapy (solid tumors and lymphomas)
- Identifying candidates for thromboprophylaxis
- Risk stratification in clinical trials

Important limitations:
- Do NOT use in patients with brain tumors or multiple myeloma
- Limited sensitivity (only 23.4% of VTE patients classified as high risk)
- Performance varies by cancer type (less predictive in lung cancer)
- Not intended for diagnosing VTE, only for risk prediction

Thromboprophylaxis with LMWH in high-risk patients can reduce VTE risk by 64% 
without significantly increasing major bleeding risk.
"""

from pydantic import BaseModel, Field
from typing import Literal


class KhoranaRiskScoreRequest(BaseModel):
    """
    Request model for Khorana Risk Score for VTE in Cancer Patients
    
    The Khorana score uses five clinical and laboratory variables to predict 
    VTE risk in cancer patients starting chemotherapy:
    
    Cancer Type Stratification:
    - Very High Risk (2 points): Stomach, pancreas cancers
    - High Risk (1 point): Lung, lymphoma, gynecologic, bladder, testicular cancers
    - Standard Risk (0 points): All other cancer types
    
    Laboratory and Clinical Parameters (each scores 1 point if positive):
    - Pre-chemotherapy platelet count ≥350×10⁹/L (≥350,000/μL)
    - Hemoglobin <10 g/dL or use of RBC growth factors (EPO, darbepoetin)
    - Pre-chemotherapy leukocyte count >11×10⁹/L (>11,000/μL)
    - BMI ≥35 kg/m²
    
    Risk Stratification:
    - Low Risk (0 points): ~5.0% 6-month VTE incidence
    - Intermediate Risk (1-2 points): ~6.6% 6-month VTE incidence
    - High Risk (≥3 points): ~11.0% 6-month VTE incidence
    
    Clinical Application:
    - High-risk patients (≥3 points, or ≥2 points per recent evidence) should be 
      considered for thromboprophylaxis with LMWH
    - Risk should be reassessed with changes in clinical status
    - Not for use in brain tumor or multiple myeloma patients
    
    References (Vancouver style):
    1. Khorana AA, Kuderer NM, Culakova E, Lyman GH, Francis CW. Development and 
       validation of a predictive model for chemotherapy-associated venous 
       thromboembolism. Blood. 2008;111(10):4902-7.
    2. Ay C, Dunkler D, Marosi C, Chiriac AL, Vormittag R, Simanek R, et al. 
       Prediction of venous thromboembolism in cancer patients. Blood. 
       2010;116(24):5377-82.
    3. Verso M, Agnelli G, Barni S, Gasparini G, LaBianca R. A modified Khorana 
       risk assessment score for venous thromboembolism in cancer patients 
       receiving chemotherapy: the Protecht score. Intern Emerg Med. 2012;7(3):291-2.
    4. Mulder FI, Candeloro M, Kamphuisen PW, Di Nisio M, Bossuyt PM, Guman N, et al. 
       The Khorana score for prediction of venous thromboembolism in cancer patients: 
       a systematic review and meta-analysis. Haematologica. 2019;104(6):1277-1287.
    """
    
    cancer_type: Literal["very_high_risk", "high_risk", "standard_risk"] = Field(
        ...,
        description="Cancer type risk category. Very high risk (2 points): stomach, pancreas. "
                   "High risk (1 point): lung, lymphoma, gynecologic, bladder, testicular. "
                   "Standard risk (0 points): all other cancer types.",
        example="high_risk"
    )
    
    platelet_count_elevated: Literal["yes", "no"] = Field(
        ...,
        description="Pre-chemotherapy platelet count ≥350×10⁹/L (≥350,000/μL). "
                   "Elevated platelet count is associated with increased VTE risk. "
                   "Scores 1 point if yes.",
        example="no"
    )
    
    hemoglobin_low_or_epo: Literal["yes", "no"] = Field(
        ...,
        description="Hemoglobin level <10 g/dL OR use of red blood cell growth factors "
                   "(erythropoietin, darbepoetin). Either condition indicates increased "
                   "VTE risk. Scores 1 point if yes.",
        example="yes"
    )
    
    leukocyte_count_elevated: Literal["yes", "no"] = Field(
        ...,
        description="Pre-chemotherapy leukocyte count >11×10⁹/L (>11,000/μL). "
                   "Leukocytosis is associated with increased VTE risk in cancer patients. "
                   "Scores 1 point if yes.",
        example="no"
    )
    
    bmi_elevated: Literal["yes", "no"] = Field(
        ...,
        description="Body mass index ≥35 kg/m². Severe obesity is an independent "
                   "risk factor for VTE in cancer patients. Scores 1 point if yes.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "cancer_type": "high_risk",
                "platelet_count_elevated": "no",
                "hemoglobin_low_or_epo": "yes",
                "leukocyte_count_elevated": "no",
                "bmi_elevated": "no"
            }
        }


class KhoranaRiskScoreResponse(BaseModel):
    """
    Response model for Khorana Risk Score for VTE in Cancer Patients
    
    Provides VTE risk assessment with thromboprophylaxis recommendations based on 
    the calculated Khorana score. The score ranges from 0-6 points and stratifies 
    patients into risk categories:
    
    - Low Risk (0 points): Routine prophylaxis not recommended
    - Intermediate-Low Risk (1 point): Consider individual factors
    - Intermediate-High Risk (2 points): Consider thromboprophylaxis
    - High Risk (≥3 points): Thromboprophylaxis recommended
    
    Clinical Implications:
    - LMWH prophylaxis can reduce VTE risk by 64% in high-risk patients
    - Number needed to treat: ~15 for high-risk patients
    - Minimal increase in major bleeding risk with prophylaxis
    - Risk reassessment recommended with clinical changes
    
    Limitations:
    - Only 23.4% sensitivity for identifying patients who develop VTE
    - Variable performance across cancer types
    - Not validated for brain tumors or multiple myeloma
    
    Reference: Khorana AA, et al. Blood. 2008;111(10):4902-7.
    """
    
    result: int = Field(
        ...,
        description="Khorana risk score (0-6 points) for VTE prediction",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including VTE risk percentage, thromboprophylaxis "
                   "recommendations, and monitoring guidance based on the calculated score",
        example="Intermediate-high risk of VTE (Khorana score: 2). The 6-month VTE incidence is approximately 6.6% in intermediate-risk patients. Recent evidence suggests the optimal high-risk cutoff may be ≥2 points rather than ≥3. Consider thromboprophylaxis with LMWH, which can reduce VTE risk by 64% in high-risk patients. Discuss risks and benefits with patient, considering bleeding risk and other factors."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Intermediate-Low Risk, Intermediate-High Risk, High Risk)",
        example="Intermediate-High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the VTE risk level",
        example="Intermediate-high risk of VTE"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "Intermediate-high risk of VTE (Khorana score: 2). The 6-month VTE incidence is approximately 6.6% in intermediate-risk patients. Recent evidence suggests the optimal high-risk cutoff may be ≥2 points rather than ≥3. Consider thromboprophylaxis with LMWH, which can reduce VTE risk by 64% in high-risk patients. Discuss risks and benefits with patient, considering bleeding risk and other factors.",
                "stage": "Intermediate-High Risk",
                "stage_description": "Intermediate-high risk of VTE"
            }
        }