"""
ACTION ICU Score for Intensive Care in NSTEMI Models

Request and response models for ACTION ICU score calculation.

References (Vancouver style):
1. Fanaroff AC, Chen AY, Roe MT, Wang TY, Alexander KP, Rao SV, et al. A Simple Risk 
   Score to Predict In-Hospital Complications in Patients With Non-ST-Segment Elevation 
   Myocardial Infarction. J Am Heart Assoc. 2018 Jun 13;7(11):e008108. 
   doi: 10.1161/JAHA.117.008108.

The ACTION ICU score is a simple risk prediction tool developed to identify patients 
with non-ST-segment elevation myocardial infarction (NSTEMI) who are at high risk for 
developing complications that would require intensive care unit (ICU) management. The 
score uses 9 readily available clinical variables to stratify patients into low, 
intermediate, and high-risk categories for ICU-level complications.

This tool helps clinicians make informed decisions about ICU admission and resource 
allocation for NSTEMI patients, potentially improving patient outcomes while optimizing 
healthcare resource utilization. However, the score is not externally validated and 
should be used in conjunction with clinical judgment.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ActionIcuNstemiRequest(BaseModel):
    """
    Request model for ACTION ICU Score for Intensive Care in NSTEMI
    
    The ACTION ICU score uses 9 clinical variables to predict ICU complications in NSTEMI:
    
    Age Categories:
    - under_70: Age <70 years (0 points)
    - 70_or_over: Age ≥70 years (+1 point)
    
    Serum Creatinine:
    - under_1_1: Creatinine <1.1 mg/dL (0 points)
    - 1_1_or_over: Creatinine ≥1.1 mg/dL (+1 point)
    
    Heart Rate Categories:
    - under_85: HR <85 bpm (0 points)
    - 85_to_100: HR 85-100 bpm (+1 point)
    - 100_or_over: HR ≥100 bpm (+3 points)
    
    Systolic Blood Pressure:
    - 145_or_over: SBP ≥145 mmHg (0 points)
    - 125_to_145: SBP 125-145 mmHg (+1 point)
    - under_125: SBP <125 mmHg (+3 points)
    
    Troponin Ratio:
    - under_12: Initial troponin/ULN <12 (0 points)
    - 12_or_over: Initial troponin/ULN ≥12 (+2 points)
    
    Clinical Signs:
    - Heart failure signs or symptoms (+5 points if present)
    - ST segment depression on EKG (+1 point if present)
    - No prior revascularization history (+1 point if no prior PCI/CABG)
    - Chronic lung disease (+2 points if present)

    References (Vancouver style):
    1. Fanaroff AC, Chen AY, Roe MT, Wang TY, Alexander KP, Rao SV, et al. A Simple Risk 
    Score to Predict In-Hospital Complications in Patients With Non-ST-Segment Elevation 
    Myocardial Infarction. J Am Heart Assoc. 2018 Jun 13;7(11):e008108. 
    doi: 10.1161/JAHA.117.008108.
    """
    
    age: Literal["under_70", "70_or_over"] = Field(
        ...,
        description="Patient age category. Under 70 years scores 0 points, 70 or over scores +1 point",
        example="under_70"
    )
    
    serum_creatinine: Literal["under_1_1", "1_1_or_over"] = Field(
        ...,
        description="Serum creatinine level category. Under 1.1 mg/dL scores 0 points, 1.1 or over scores +1 point",
        example="under_1_1"
    )
    
    heart_rate: Literal["under_85", "85_to_100", "100_or_over"] = Field(
        ...,
        description="Heart rate category. Under 85 bpm scores 0 points, 85-100 bpm scores +1 point, 100+ bpm scores +3 points",
        example="85_to_100"
    )
    
    systolic_bp: Literal["145_or_over", "125_to_145", "under_125"] = Field(
        ...,
        description="Systolic blood pressure category. 145+ mmHg scores 0 points, 125-145 mmHg scores +1 point, under 125 mmHg scores +3 points",
        example="125_to_145"
    )
    
    troponin_ratio: Literal["under_12", "12_or_over"] = Field(
        ...,
        description="Ratio of initial troponin to upper limit of normal. Under 12 scores 0 points, 12 or over scores +2 points",
        example="12_or_over"
    )
    
    heart_failure_signs: Literal["no", "yes"] = Field(
        ...,
        description="Presence of signs or symptoms of heart failure (dyspnea, rales, elevated JVP, peripheral edema). Scores +5 points if yes",
        example="no"
    )
    
    st_depression: Literal["no", "yes"] = Field(
        ...,
        description="ST segment depression on 12-lead electrocardiogram. Scores +1 point if yes",
        example="yes"
    )
    
    prior_revascularization: Literal["yes", "no"] = Field(
        ...,
        description="History of prior coronary revascularization (PCI or CABG). Scores 0 points if yes, +1 point if no",
        example="no"
    )
    
    chronic_lung_disease: Literal["no", "yes"] = Field(
        ...,
        description="Presence of chronic lung disease (COPD, asthma, chronic bronchitis, etc.). Scores +2 points if yes",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": "under_70",
                "serum_creatinine": "under_1_1",
                "heart_rate": "85_to_100",
                "systolic_bp": "125_to_145",
                "troponin_ratio": "12_or_over",
                "heart_failure_signs": "no",
                "st_depression": "yes",
                "prior_revascularization": "no",
                "chronic_lung_disease": "no"
            }
        }


class ActionIcuNstemiResponse(BaseModel):
    """
    Response model for ACTION ICU Score for Intensive Care in NSTEMI
    
    The ACTION ICU score ranges from 0 to 20 points and stratifies patients into:
    - Low risk (0-3 points): Low risk of ICU complications
    - Intermediate risk (4-7 points): Intermediate risk of ICU complications  
    - High risk (8-20 points): High risk of ICU complications
    
    Higher scores indicate greater likelihood of developing complications requiring 
    ICU-level care, including cardiogenic shock, mechanical ventilation, mechanical 
    circulatory support, or cardiac arrest.
    
    Reference: Fanaroff AC, et al. J Am Heart Assoc. 2018;7(11):e008108.
    """
    
    result: int = Field(
        ...,
        description="ACTION ICU score calculated from clinical variables (range: 0-20 points)",
        example=5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended care level based on the score",
        example="Intermediate risk of complications requiring ICU care. Consider enhanced monitoring and possible step-down unit care."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low risk, Intermediate risk, High risk)",
        example="Intermediate risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Intermediate risk of ICU complications"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5,
                "unit": "points",
                "interpretation": "Intermediate risk of complications requiring ICU care. Consider enhanced monitoring and possible step-down unit care.",
                "stage": "Intermediate risk",
                "stage_description": "Intermediate risk of ICU complications"
            }
        }