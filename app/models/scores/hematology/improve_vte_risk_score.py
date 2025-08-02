"""
IMPROVE VTE Risk Score Models

Request and response models for IMPROVE VTE Risk Score calculation.

References (Vancouver style):
1. Spyropoulos AC, Anderson FA Jr, FitzGerald G, et al. Predictive and associative 
   models to identify hospitalized medical patients at risk for VTE. Chest. 2011 
   Sep;140(3):706-714. doi: 10.1378/chest.10-1944.
2. Hostler DC, Marx ES, Moores LK, et al. Validation of the International Medical 
   Prevention Registry on Venous Thromboembolism bleeding risk model. Chest. 2016 
   Apr;149(4):1002-1009. doi: 10.1378/chest.15-2082.
3. Rosenberg D, Eichorn A, Alarcon M, et al. External validation of the risk assessment 
   model of the International Medical Prevention Registry on Venous Thromboembolism 
   (IMPROVE) for medical patients in a tertiary health system. J Am Heart Assoc. 2014 
   Nov 4;3(6):e001152. doi: 10.1161/JAHA.114.001152.

The IMPROVE VTE Risk Score predicts 3-month risk of acute venous thromboembolism (VTE) 
in hospitalized medical patients. Developed from the International Medical Prevention 
Registry on Venous Thromboembolism database, this validated tool uses 7 clinical variables 
to stratify patients into risk categories. Patients with scores <2 (representing <1% 
3-month VTE risk) may not warrant pharmacologic thromboprophylaxis, while those with 
scores ≥2 should receive prophylaxis. The score is particularly valuable for identifying 
low-risk medical patients who can safely avoid anticoagulation.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ImproveVteRiskScoreRequest(BaseModel):
    """
    Request model for IMPROVE VTE Risk Score calculation
    
    Predicts 3-month risk of acute venous thromboembolism (VTE) in hospitalized 
    medical patients using 7 clinical variables.
    
    Risk Factors Assessed:
    - Previous VTE history (highest risk factor - 3 points)
    - Known thrombophilia (2 points)
    - Current lower-limb paralysis (2 points)
    - Current cancer (2 points)
    - Recent immobilization ≥7 days (1 point)
    - ICU/CCU stay (1 point)
    - Age >60 years (1 point)
    
    Scoring Interpretation:
    - Score <2: Pharmacologic thromboprophylaxis not warranted (<1% 3-month VTE risk)
    - Score ≥2: Start pharmacologic or mechanical prophylaxis
    - Score-specific VTE risks: 0 (0.4%), 1 (0.6%), 2 (1.0%), 3 (1.7%), 4 (2.9%), ≥5 (≥7.2%)
    
    The IMPROVE VTE score helps healthcare providers risk stratify hospitalized medical 
    patients and identify those who may not need VTE prophylaxis, thereby reducing 
    unnecessary anticoagulation exposure while maintaining appropriate prophylaxis 
    for higher-risk patients.

    References (Vancouver style):
    1. Spyropoulos AC, Anderson FA Jr, FitzGerald G, et al. Predictive and associative 
       models to identify hospitalized medical patients at risk for VTE. Chest. 2011 
       Sep;140(3):706-714. doi: 10.1378/chest.10-1944.
    2. Hostler DC, Marx ES, Moores LK, et al. Validation of the International Medical 
       Prevention Registry on Venous Thromboembolism bleeding risk model. Chest. 2016 
       Apr;149(4):1002-1009. doi: 10.1378/chest.15-2082.
    3. Rosenberg D, Eichorn A, Alarcon M, et al. External validation of the risk assessment 
       model of the International Medical Prevention Registry on Venous Thromboembolism 
       (IMPROVE) for medical patients in a tertiary health system. J Am Heart Assoc. 2014 
       Nov 4;3(6):e001152. doi: 10.1161/JAHA.114.001152.
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
    
    class Config:
        schema_extra = {
            "example": {
                "previous_vte": "no",
                "known_thrombophilia": "no",
                "current_lower_limb_paralysis": "no",
                "current_cancer": "no",
                "immobilized_7_days": "no",
                "icu_ccu_stay": "no",
                "age_over_60": "yes"
            }
        }


class ImproveVteRiskScoreResponse(BaseModel):
    """
    Response model for IMPROVE VTE Risk Score calculation
    
    Returns the IMPROVE VTE Risk Score with risk stratification and clinical
    recommendations for VTE prophylaxis in hospitalized medical patients.
    
    Risk Categories and VTE Rates:
    - Score 0: 0.4% 3-month VTE risk (Very Low Risk)
    - Score 1: 0.6% 3-month VTE risk (Low Risk)
    - Score 2: 1.0% 3-month VTE risk (Moderate Risk)
    - Score 3: 1.7% 3-month VTE risk (Moderate-High Risk)
    - Score 4: 2.9% 3-month VTE risk (High Risk)
    - Score ≥5: ≥7.2% 3-month VTE risk (Very High Risk)
    
    The score provides evidence-based guidance for thromboprophylaxis decisions. 
    Patients with scores <2 may not warrant pharmacologic prophylaxis, while those 
    with scores ≥2 should receive prophylaxis. Consider bleeding risk assessment 
    using tools like the IMPROVE Bleeding Risk Score for comprehensive evaluation.
    
    Reference: Spyropoulos AC, et al. Chest. 2011;140(3):706-714.
    """
    
    result: int = Field(
        ...,
        description="IMPROVE VTE Risk Score calculated from clinical risk factors (range 0-12 points)",
        example=1,
        ge=0,
        le=12
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and VTE prophylaxis recommendations based on the score",
        example="0.6% 3-month VTE risk. Pharmacologic thromboprophylaxis not warranted. Consider mechanical prophylaxis or early mobilization as appropriate."
    )
    
    stage: str = Field(
        ...,
        description="VTE risk category (Very Low Risk, Low Risk, Moderate Risk, Moderate-High Risk, High Risk, Very High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category with score",
        example="Score 1 point"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "0.6% 3-month VTE risk. Pharmacologic thromboprophylaxis not warranted. Consider mechanical prophylaxis or early mobilization as appropriate.",
                "stage": "Low Risk",
                "stage_description": "Score 1 point"
            }
        }