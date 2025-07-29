"""
BAP-65 Score for Acute Exacerbation of COPD Models

Request and response models for BAP-65 score calculation.

References (Vancouver style):
1. Tabak YP, Sun X, Johannes RS, Gupta V, Shorr AF. Mortality and need for mechanical 
   ventilation in acute exacerbations of chronic obstructive pulmonary disease: 
   development and validation of a simple risk score. Arch Intern Med. 2009 Sep 
   28;169(17):1595-602. doi: 10.1001/archinternmed.2009.270. PMID: 19786679.
2. Shorr AF, Sun X, Johannes RS, Yaitanes A, Tabak YP. Validation of a novel risk 
   score for severity of illness in acute exacerbations of COPD. Chest. 2011 
   Nov;140(5):1177-1183. doi: 10.1378/chest.10-3035. Epub 2011 Apr 28. PMID: 21527510.

The BAP-65 score is a simple risk stratification tool that predicts in-hospital 
mortality in patients with acute exacerbations of chronic obstructive pulmonary 
disease (COPD). It uses four easily obtainable clinical variables: BUN (Blood Urea 
Nitrogen), Altered mental status, Pulse rate, and age ≥65 years. This score helps 
clinicians identify high-risk patients who may require intensive monitoring or ICU care.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class Bap65Request(BaseModel):
    """
    Request model for BAP-65 Score for Acute Exacerbation of COPD
    
    The BAP-65 score uses four clinical variables to assess mortality risk:
    
    BAP stands for:
    - B: BUN (Blood Urea Nitrogen)
    - A: Altered Mental Status
    - P: Pulse rate
    - 65: Age ≥65 years
    
    Each positive finding scores 1 point, for a total possible score of 0-3 points.
    
    Clinical Variables:
    - BUN ≥25 mg/dL (8.9 mmol/L) - Indicates renal dysfunction or dehydration
    - Altered Mental Status - Glasgow Coma Scale <14, or disorientation, stupor, or coma
    - Pulse ≥109 beats/min - Tachycardia indicating physiologic stress
    - Age ≥65 years - Advanced age as a risk factor
    
    Note: This score is only validated for patients >40 years old and should use
    the worst variables on the day of admission.
    
    References (Vancouver style):
    1. Tabak YP, Sun X, Johannes RS, Gupta V, Shorr AF. Mortality and need for mechanical 
       ventilation in acute exacerbations of chronic obstructive pulmonary disease: 
       development and validation of a simple risk score. Arch Intern Med. 2009 Sep 
       28;169(17):1595-602. doi: 10.1001/archinternmed.2009.270. PMID: 19786679.
    2. Shorr AF, Sun X, Johannes RS, Yaitanes A, Tabak YP. Validation of a novel risk 
       score for severity of illness in acute exacerbations of COPD. Chest. 2011 
       Nov;140(5):1177-1183. doi: 10.1378/chest.10-3035. Epub 2011 Apr 28. PMID: 21527510.
    """
    
    bun: Literal["yes", "no"] = Field(
        ...,
        description="Blood Urea Nitrogen (BUN) ≥25 mg/dL (8.9 mmol/L). Elevated BUN may indicate renal dysfunction, dehydration, or severe illness. Scores 1 point if yes",
        example="no"
    )
    
    altered_mental_status: Literal["yes", "no"] = Field(
        ...,
        description="Altered Mental Status defined as initial Glasgow Coma Scale <14, or disorientation, stupor, or coma. Indicates severe illness and poor prognosis. Scores 1 point if yes",
        example="no"
    )
    
    pulse: Literal["yes", "no"] = Field(
        ...,
        description="Pulse ≥109 beats per minute. Tachycardia indicates physiologic stress and increased oxygen demand. Scores 1 point if yes",
        example="yes"
    )
    
    age: int = Field(
        ...,
        description="Patient age in years. Must be >40 years old as the score is not validated for younger patients. Age ≥65 years scores 1 point",
        ge=41,
        le=120,
        example=68
    )
    
    @validator('age')
    def validate_age(cls, v):
        """Validates that age is within acceptable range"""
        if v < 41:
            raise ValueError("BAP-65 score is only validated for patients >40 years old")
        if v > 120:
            raise ValueError("Age must be ≤120 years")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "bun": "no",
                "altered_mental_status": "no",
                "pulse": "yes",
                "age": 68
            }
        }


class Bap65Response(BaseModel):
    """
    Response model for BAP-65 Score for Acute Exacerbation of COPD
    
    The BAP-65 score stratifies patients into five risk classes based on score and age:
    - Class I (0 points, <65 years): 0.3% mortality
    - Class II (0 points, ≥65 years): 1.0% mortality
    - Class III (1 point): 2.2% mortality
    - Class IV (2 points): 6.4% mortality
    - Class V (3 points): 14.1% mortality
    
    Higher scores indicate increased risk of in-hospital mortality and need for 
    mechanical ventilation. Patients in Classes IV-V should be considered for 
    intensive monitoring or ICU admission.
    
    Reference: Tabak YP, et al. Arch Intern Med. 2009;169(17):1595-602.
    """
    
    result: int = Field(
        ...,
        description="BAP-65 score calculated from clinical variables (range: 0-3 points)",
        ge=0,
        le=3,
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the score including mortality risk and management recommendations",
        example="6.4% in-hospital mortality risk. High risk patient. Hospital admission required. Consider early aggressive treatment and close monitoring."
    )
    
    stage: str = Field(
        ...,
        description="Risk classification (Class I-V) based on score and age",
        example="Class IV"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk class",
        example="2 points, any age"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "6.4% in-hospital mortality risk. High risk patient. Hospital admission required. Consider early aggressive treatment and close monitoring.",
                "stage": "Class IV",
                "stage_description": "2 points, any age"
            }
        }