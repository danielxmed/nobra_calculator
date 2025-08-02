"""
HOSPITAL Score for Readmissions Models

Request and response models for HOSPITAL Score calculation.

References (Vancouver style):
1. Donzé J, Aujesky D, Williams D, Schnipper JL. Potentially avoidable 30-day hospital 
   readmissions in medical patients: derivation and validation of a prediction model. 
   JAMA Intern Med. 2013 Apr 22;173(8):632-8. doi: 10.1001/jamainternmed.2013.3023.
2. Donzé JD, Williams MV, Robinson EJ, Zimlichman E, Aujesky D, Vasilevskis EE, et al. 
   International Validity of the HOSPITAL Score to Predict 30-Day Potentially Avoidable 
   Hospital Readmissions. JAMA Intern Med. 2016 Apr;176(4):496-502. 
   doi: 10.1001/jamainternmed.2015.8462.

The HOSPITAL Score is a validated prediction tool that uses seven readily available 
clinical variables to identify medical patients at high risk of potentially avoidable 
30-day readmissions. It helps healthcare providers direct transitional care resources 
to patients most likely to benefit from intensive interventions.
"""

from pydantic import BaseModel, Field
from typing import Literal


class HospitalScoreRequest(BaseModel):
    """
    Request model for HOSPITAL Score for Readmissions
    
    The HOSPITAL score is an acronym for its seven components:
    
    H - Hemoglobin level at discharge:
    - gte_12: ≥12 g/dL (0 points)
    - lt_12: <12 g/dL (1 point)
    
    O - Oncology service discharge:
    - no: Not from oncology service (0 points)
    - yes: From oncology service (2 points)
    
    S - Sodium level at discharge:
    - gte_135: ≥135 mEq/L (0 points)
    - lt_135: <135 mEq/L (1 point)
    
    P - Procedure during hospital stay:
    - no: No ICD-9 coded procedure (0 points)
    - yes: ICD-9 coded procedure performed (1 point)
    
    I - Index admission type:
    - elective: Elective admission (0 points)
    - urgent_emergent: Urgent or emergent admission (1 point)
    
    T - Time (admissions in previous year):
    - 0_to_1: 0-1 admissions (0 points)
    - 2_to_5: 2-5 admissions (2 points)
    - over_5: >5 admissions (5 points)
    
    AL - Length of stay:
    - lt_5_days: <5 days (0 points)
    - gte_5_days: ≥5 days (2 points)

    References (Vancouver style):
    1. Donzé J, Aujesky D, Williams D, Schnipper JL. Potentially avoidable 30-day hospital 
    readmissions in medical patients: derivation and validation of a prediction model. 
    JAMA Intern Med. 2013 Apr 22;173(8):632-8.
    """
    
    hemoglobin: Literal["gte_12", "lt_12"] = Field(
        ...,
        description="Hemoglobin level at discharge. ≥12 g/dL scores 0 points, <12 g/dL scores 1 point",
        example="gte_12"
    )
    
    oncology_discharge: Literal["no", "yes"] = Field(
        ...,
        description="Discharge from an oncology service. No scores 0 points, yes scores 2 points",
        example="no"
    )
    
    sodium: Literal["gte_135", "lt_135"] = Field(
        ...,
        description="Sodium level at discharge. ≥135 mEq/L scores 0 points, <135 mEq/L scores 1 point",
        example="gte_135"
    )
    
    procedure: Literal["no", "yes"] = Field(
        ...,
        description="ICD-9 coded procedure during hospital stay. No scores 0 points, yes scores 1 point",
        example="no"
    )
    
    admission_type: Literal["elective", "urgent_emergent"] = Field(
        ...,
        description="Type of index admission. Elective scores 0 points, urgent/emergent scores 1 point",
        example="urgent_emergent"
    )
    
    previous_admissions: Literal["0_to_1", "2_to_5", "over_5"] = Field(
        ...,
        description="Number of hospital admissions in the previous year. 0-1 scores 0 points, "
                    "2-5 scores 2 points, >5 scores 5 points",
        example="2_to_5"
    )
    
    length_of_stay: Literal["lt_5_days", "gte_5_days"] = Field(
        ...,
        description="Length of stay for current admission. <5 days scores 0 points, ≥5 days scores 2 points",
        example="gte_5_days"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "hemoglobin": "lt_12",
                "oncology_discharge": "no",
                "sodium": "gte_135",
                "procedure": "yes",
                "admission_type": "urgent_emergent",
                "previous_admissions": "2_to_5",
                "length_of_stay": "gte_5_days"
            }
        }


class HospitalScoreResponse(BaseModel):
    """
    Response model for HOSPITAL Score for Readmissions
    
    The HOSPITAL score ranges from 0-13 points and stratifies risk:
    - 0-4 points: Low risk (5.8% readmission rate)
    - 5-6 points: Intermediate risk (12.0% readmission rate)
    - ≥7 points: High risk (22.8% readmission rate)
    
    The score predicts potentially avoidable 30-day readmissions, allowing 
    targeted interventions for high-risk patients.
    
    Reference: Donzé J, et al. JAMA Intern Med. 2013;173(8):632-8.
    """
    
    result: int = Field(
        ...,
        description="HOSPITAL score calculated from the seven clinical variables (range: 0-13 points)",
        example=7
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with readmission risk and recommended interventions",
        example="High risk of potentially avoidable 30-day readmission (22.8%). Intensive "
                "transitional care interventions recommended, including early follow-up, "
                "medication reconciliation, and care coordination."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Intermediate Risk, High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Score range for the risk category",
        example="Score ≥7"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 7,
                "unit": "points",
                "interpretation": "High risk of potentially avoidable 30-day readmission (22.8%). "
                                "Intensive transitional care interventions recommended, including "
                                "early follow-up, medication reconciliation, and care coordination.",
                "stage": "High Risk",
                "stage_description": "Score ≥7"
            }
        }