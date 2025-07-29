"""
ATRIA Stroke Risk Score Models

Request and response models for ATRIA Stroke Risk Score calculation.

References (Vancouver style):
1. Singer DE, Chang Y, Borowsky LH, Fang MC, Pomernacki NK, Udaltsova N, et al. A new 
   risk scheme to predict ischemic stroke and other thromboembolism in atrial fibrillation: 
   the ATRIA study stroke risk score. J Am Heart Assoc. 2013 Jun 21;2(3):e000250. 
   doi: 10.1161/JAHA.113.000250.
2. Go AS, Fang MC, Udaltsova N, Chang Y, Pomernacki NK, Borowsky L, et al. Impact of 
   proteinuria and glomerular filtration rate on risk of thromboembolism in atrial 
   fibrillation: the anticoagulation and risk factors in atrial fibrillation (ATRIA) 
   study. Circulation. 2009 Mar 17;119(10):1363-9. doi: 10.1161/CIRCULATIONAHA.108.816082.
3. Aspberg S, Chang Y, Atterman A, Go AS, Singer DE. Comparison of the ATRIA, CHADS2, 
   and CHA2DS2-VASc stroke risk scores in predicting ischaemic stroke in a large Swedish 
   cohort of patients with atrial fibrillation. Eur Heart J. 2016 Nov 7;37(42):3203-3210. 
   doi: 10.1093/eurheartj/ehw077.

The ATRIA stroke risk score predicts ischemic stroke and systemic thromboembolism in 
patients with atrial fibrillation. It incorporates age, sex, and several comorbidities 
including renal dysfunction parameters that distinguish it from other stroke risk scores.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class AtriaStrokeRequest(BaseModel):
    """
    Request model for ATRIA Stroke Risk Score
    
    The ATRIA score uses 8 clinical variables to assess stroke risk in patients 
    with atrial fibrillation:
    
    Age scoring varies based on stroke history:
    - Without prior stroke: <65 years (0 points), 65-74 (3 points), 75-84 (5 points), ≥85 (6 points)
    - With prior stroke: <65 years (8 points), 65-74 (7 points), 75-84 (7 points), ≥85 (9 points)
    
    Other risk factors:
    - Female sex (1 point)
    - Diabetes mellitus (1 point)
    - Congestive heart failure (1 point)
    - Hypertension (1 point)
    - Proteinuria (1 point)
    - eGFR <45 or ESRD (1 point)
    
    Total score ranges from 0-15 points.
    
    References (Vancouver style):
    1. Singer DE, Chang Y, Borowsky LH, Fang MC, Pomernacki NK, Udaltsova N, et al. A new 
    risk scheme to predict ischemic stroke and other thromboembolism in atrial fibrillation: 
    the ATRIA study stroke risk score. J Am Heart Assoc. 2013 Jun 21;2(3):e000250. 
    doi: 10.1161/JAHA.113.000250.
    """
    
    age: int = Field(
        ...,
        ge=0,
        le=120,
        description="Patient age in years. Age is the most important risk factor in the ATRIA score, with higher scores for older patients and those with prior stroke.",
        example=72
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Biological sex of the patient. Female sex contributes 1 point to the total score.",
        example="female"
    )
    
    history_of_stroke: Literal["yes", "no"] = Field(
        ...,
        description="History of prior ischemic stroke or transient ischemic attack (TIA). Patients with prior stroke have modified age scoring resulting in significantly higher total scores.",
        example="no"
    )
    
    diabetes: Literal["yes", "no"] = Field(
        ...,
        description="Diabetes mellitus (Type 1 or Type 2). Contributes 1 point to the total score.",
        example="yes"
    )
    
    congestive_heart_failure: Literal["yes", "no"] = Field(
        ...,
        description="Congestive heart failure of any etiology. Contributes 1 point to the total score.",
        example="no"
    )
    
    hypertension: Literal["yes", "no"] = Field(
        ...,
        description="Hypertension (diagnosed high blood pressure requiring treatment). Contributes 1 point to the total score.",
        example="yes"
    )
    
    proteinuria: Literal["yes", "no"] = Field(
        ...,
        description="Proteinuria defined as >1+ on dipstick or >300 mg/day on quantitative testing. This renal parameter contributes 1 point to the total score.",
        example="no"
    )
    
    egfr_less_than_45_or_esrd: Literal["yes", "no"] = Field(
        ...,
        description="Estimated glomerular filtration rate (eGFR) <45 mL/min/1.73m² or end-stage renal disease (ESRD) requiring dialysis. This renal parameter contributes 1 point to the total score.",
        example="no"
    )
    
    @validator('age')
    def validate_age(cls, v):
        if v < 0 or v > 120:
            raise ValueError('Age must be between 0 and 120 years')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "age": 72,
                "sex": "female",
                "history_of_stroke": "no",
                "diabetes": "yes",
                "congestive_heart_failure": "no",
                "hypertension": "yes",
                "proteinuria": "no",
                "egfr_less_than_45_or_esrd": "no"
            }
        }


class AtriaStrokeResponse(BaseModel):
    """
    Response model for ATRIA Stroke Risk Score
    
    The ATRIA score stratifies patients into three risk categories:
    - Low risk (0-5 points): <1% annual stroke risk
    - Intermediate risk (6 points): 1-<2% annual stroke risk
    - High risk (≥7 points): ≥2% annual stroke risk
    
    The score predicts ischemic stroke and systemic thromboembolism, not just stroke alone.
    
    Reference: Singer DE, et al. J Am Heart Assoc. 2013;2(3):e000250.
    """
    
    result: int = Field(
        ...,
        description="ATRIA stroke risk score calculated from clinical variables (range: 0-15 points)",
        example=6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the stroke risk and recommendations for anticoagulation therapy",
        example="Intermediate risk of stroke (1-<2% per year). These patients have moderate stroke risk. Anticoagulation should be considered based on patient preferences, bleeding risk, and overall clinical context."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low, Intermediate, or High)",
        example="Intermediate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Intermediate stroke risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": "Intermediate risk of stroke (1-<2% per year). These patients have moderate stroke risk. Anticoagulation should be considered based on patient preferences, bleeding risk, and overall clinical context.",
                "stage": "Intermediate",
                "stage_description": "Intermediate stroke risk"
            }
        }