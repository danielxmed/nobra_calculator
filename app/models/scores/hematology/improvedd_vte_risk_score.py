"""
IMPROVEDD VTE Risk Score Models

Request and response models for IMPROVEDD VTE Risk Score calculation.

References (Vancouver style):
1. Gibson CM, Spyropoulos AC, Cohen AT, et al. The IMPROVEDD VTE Risk Score: Incorporation 
   of D-Dimer into the IMPROVE Score to Improve Venous Thromboembolism Risk Stratification. 
   TH Open. 2017 Oct 9;1(1):e56-e65. doi: 10.1055/s-0037-1603929.
2. Spyropoulos AC, Lipardi C, Xu J, et al. Modified IMPROVE VTE Risk Score and Elevated 
   D-Dimer Identify a High Venous Thromboembolism Risk in Acutely Ill Medical Population 
   for Extended Thromboprophylaxis. TH Open. 2020 Mar 6;4(1):e59-e65. doi: 10.1055/s-0040-1705137.
3. Spyropoulos AC, Anderson FA Jr, FitzGerald G, et al. Predictive and associative 
   models to identify hospitalized medical patients at risk for VTE. Chest. 2011 
   Sep;140(3):706-714. doi: 10.1378/chest.10-1944.

The IMPROVEDD VTE Risk Score predicts 77-day risk of acute venous thromboembolism (VTE) 
in hospitalized medical patients by incorporating D-dimer levels into the IMPROVE Risk Score. 
Developed from the APEX trial involving 7,441 hospitalized medically ill patients, this 
enhanced tool adds D-dimer ≥2× upper limit of normal as an additional risk factor worth 
2 points. The addition of D-dimer significantly improves VTE risk discrimination (ΔAUC: 0.06, 
p=0.0006) and reclassification compared to the original IMPROVE score. An IMPROVEDD score 
≥2 identifies patients with heightened VTE risk through 77 days, helping clinicians make 
more informed decisions about extended thromboprophylaxis duration.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ImprovedVteRiskScoreRequest(BaseModel):
    """
    Request model for IMPROVEDD VTE Risk Score calculation
    
    Predicts 77-day risk of acute venous thromboembolism (VTE) in hospitalized 
    medical patients using the original 7 IMPROVE clinical variables plus D-dimer.
    
    Risk Factors Assessed:
    - Previous VTE history (highest risk factor - 3 points)
    - Known thrombophilia (2 points)
    - Current lower-limb paralysis (2 points)
    - Current cancer (2 points)
    - Recent immobilization ≥7 days (1 point)
    - ICU/CCU stay (1 point)
    - Age >60 years (1 point)
    - D-dimer ≥2× ULN (2 points) - NEW addition enhancing risk discrimination
    
    Scoring Interpretation:
    - Score <2: Low VTE risk, pharmacologic thromboprophylaxis not warranted
    - Score ≥2: Increased VTE risk, start pharmacologic or mechanical prophylaxis
    - Score-specific 77-day VTE risks: 0 (0.5%), 1 (0.7%), 2 (1.0%), 3 (1.4%), 4 (1.9%), ≥5 (≥2.7%)
    
    The IMPROVEDD score enhances the original IMPROVE VTE risk assessment by incorporating 
    D-dimer levels, which independently predict VTE (adjusted HR: 2.22). This biomarker 
    addition significantly improves risk stratification and helps identify patients who 
    may benefit from extended thromboprophylaxis duration in the post-acute care period.

    References (Vancouver style):
    1. Gibson CM, Spyropoulos AC, Cohen AT, et al. The IMPROVEDD VTE Risk Score: Incorporation 
       of D-Dimer into the IMPROVE Score to Improve Venous Thromboembolism Risk Stratification. 
       TH Open. 2017 Oct 9;1(1):e56-e65. doi: 10.1055/s-0037-1603929.
    2. Spyropoulos AC, Lipardi C, Xu J, et al. Modified IMPROVE VTE Risk Score and Elevated 
       D-Dimer Identify a High Venous Thromboembolism Risk in Acutely Ill Medical Population 
       for Extended Thromboprophylaxis. TH Open. 2020 Mar 6;4(1):e59-e65. doi: 10.1055/s-0040-1705137.
    """
    
    previous_vte: Literal["yes", "no"] = Field(
        ...,
        description="History of previous venous thromboembolism (deep vein thrombosis or pulmonary embolism). Previous VTE is the strongest risk factor, carrying the highest point value (3 points) due to significantly increased likelihood of recurrence",
        example="no"
    )
    
    known_thrombophilia: Literal["yes", "no"] = Field(
        ...,
        description="Known thrombophilia or hereditary thrombotic disorder (Factor V Leiden, prothrombin gene mutation, antithrombin deficiency, protein C or S deficiency, antiphospholipid syndrome). Thrombophilic disorders increase VTE risk through various mechanisms affecting coagulation pathways. Scores 2 points if yes",
        example="no"
    )
    
    current_lower_limb_paralysis: Literal["yes", "no"] = Field(
        ...,
        description="Current lower-limb paralysis or paresis affecting mobility. Paralysis increases VTE risk through venous stasis and reduced muscle pump function in affected limbs, particularly concerning for DVT development. Scores 2 points if yes",
        example="no"
    )
    
    current_cancer: Literal["yes", "no"] = Field(
        ...,
        description="Current active cancer diagnosis regardless of type or stage. Cancer increases VTE risk through multiple mechanisms including tumor-related procoagulant factors, chemotherapy effects, reduced mobility, and systemic hypercoagulable state. Scores 2 points if yes",
        example="no"
    )
    
    immobilized_7_days: Literal["yes", "no"] = Field(
        ...,
        description="Immobilized ≥7 days immediately prior to and during hospital admission. Prolonged immobilization increases VTE risk through venous stasis and activation of coagulation pathways. Includes bed rest, wheelchair confinement, or significant mobility limitation. Scores 1 point if yes",
        example="no"
    )
    
    icu_ccu_stay: Literal["yes", "no"] = Field(
        ...,
        description="Current stay in intensive care unit (ICU) or coronary care unit (CCU). Critical care setting indicates severe illness with increased VTE risk from immobility, invasive procedures, systemic inflammation, and hemodynamic instability. Scores 1 point if yes",
        example="no"
    )
    
    age_over_60: Literal["yes", "no"] = Field(
        ...,
        description="Age greater than 60 years. Advanced age increases VTE risk through age-related changes in coagulation factors, decreased mobility, increased comorbidities, and reduced physiological reserve. Scores 1 point if yes",
        example="no"
    )
    
    d_dimer_elevated: Literal["yes", "no"] = Field(
        ...,
        description="D-dimer ≥2× upper limit of normal (ULN). Elevated D-dimer reflects ongoing fibrin formation and breakdown, indicating activation of the coagulation and fibrinolytic systems. This biomarker significantly enhances VTE risk prediction when added to clinical risk factors (adjusted HR: 2.22). Scores 2 points if yes",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "previous_vte": "no",
                "known_thrombophilia": "no",
                "current_lower_limb_paralysis": "no",
                "current_cancer": "no",
                "immobilized_7_days": "no",
                "icu_ccu_stay": "no",
                "age_over_60": "yes",
                "d_dimer_elevated": "yes"
            }
        }


class ImprovedVteRiskScoreResponse(BaseModel):
    """
    Response model for IMPROVEDD VTE Risk Score calculation
    
    Returns the IMPROVEDD VTE Risk Score with risk stratification and clinical
    recommendations for VTE prophylaxis in hospitalized medical patients.
    
    Risk Categories and 77-day VTE Rates:
    - Score 0: 0.5% 77-day VTE risk (Very Low Risk)
    - Score 1: 0.7% 77-day VTE risk (Low Risk)
    - Score 2: 1.0% 77-day VTE risk (Moderate Risk)
    - Score 3: 1.4% 77-day VTE risk (Moderate-High Risk)
    - Score 4: 1.9% 77-day VTE risk (High Risk)
    - Score ≥5: ≥2.7% 77-day VTE risk (Very High Risk)
    
    The IMPROVEDD score provides enhanced evidence-based guidance for thromboprophylaxis 
    decisions compared to the original IMPROVE score. Patients with scores <2 may not 
    warrant pharmacologic prophylaxis, while those with scores ≥2 should receive prophylaxis. 
    The addition of D-dimer significantly improves risk discrimination and may help identify 
    patients who benefit from extended prophylaxis duration. Consider bleeding risk assessment 
    using tools like the IMPROVE Bleeding Risk Score for comprehensive evaluation.
    
    Reference: Gibson CM, et al. TH Open. 2017;1(1):e56-e65.
    """
    
    result: int = Field(
        ...,
        description="IMPROVEDD VTE Risk Score calculated from clinical risk factors and D-dimer (range 0-14 points)",
        example=3,
        ge=0,
        le=14
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and VTE prophylaxis recommendations based on the score",
        example="1.4% 77-day VTE risk. Start pharmacologic or mechanical prophylaxis. Consider patient-specific bleeding risk before initiating anticoagulation."
    )
    
    stage: str = Field(
        ...,
        description="VTE risk category (Very Low Risk, Low Risk, Moderate Risk, Moderate-High Risk, High Risk, Very High Risk)",
        example="Moderate-High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category with score",
        example="Score 3 points"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "1.4% 77-day VTE risk. Start pharmacologic or mechanical prophylaxis. Consider patient-specific bleeding risk before initiating anticoagulation.",
                "stage": "Moderate-High Risk",
                "stage_description": "Score 3 points"
            }
        }