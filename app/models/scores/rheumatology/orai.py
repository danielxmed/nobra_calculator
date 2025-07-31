"""
Osteoporosis Risk Assessment Instrument (ORAI) Models

Request and response models for ORAI calculation.

References (Vancouver style):
1. Cadarette SM, Jaglal SB, Kreiger N, McIsaac WJ, Darlington GA, Tu JV. Development 
   and validation of the Osteoporosis Risk Assessment Instrument to facilitate selection 
   of women for bone densitometry. CMAJ. 2000 May 2;162(9):1289-94. PMID: 10813010; 
   PMCID: PMC1232396.
2. El Maghraoui A, Habbassi A, Ghazi M, Achemlal L, Mounach A, Nouijai A, et al. 
   Validation and comparative evaluation of four osteoporosis risk assessment tools in 
   Moroccan menopausal women. Arch Osteoporos. 2006 Dec;1(1-2):35-42. doi: 
   10.1007/s11657-006-0006-1.
3. Rubin KH, Abrahamsen B, Friis-Holmberg T, Hjelmborg JV, Bech M, Hermann AP, et al. 
   Comparison of different screening tools (FRAX®, OST, ORAI, OSIRIS, SCORE and age alone) 
   to identify women with increased risk of fracture. A population-based prospective study. 
   Bone. 2013 Sep;56(1):16-22. doi: 10.1016/j.bone.2013.05.002.

The ORAI is a simple clinical tool that uses only 3 variables (age, weight, and current 
estrogen use) to identify postmenopausal women who should undergo bone densitometry. With 
a sensitivity of 93.3% and specificity of 46.4%, it effectively identifies women at risk 
for osteoporosis while reducing unnecessary testing in low-risk populations.
"""

from pydantic import BaseModel, Field
from typing import Literal


class OraiRequest(BaseModel):
    """
    Request model for Osteoporosis Risk Assessment Instrument (ORAI)
    
    The ORAI uses 3 clinical variables to assess osteoporosis risk:
    
    Age Categories:
    - 45-54 years: 0 points
    - 55-64 years: 5 points
    - 65-74 years: 9 points
    - ≥75 years: 15 points
    
    Weight Categories:
    - >69 kg (>152 lbs): 0 points
    - 60-69 kg (132-152 lbs): 3 points
    - <60 kg (<132 lbs): 9 points
    
    Current Estrogen Use:
    - Yes (currently using HRT): 0 points
    - No (not using HRT): 2 points
    
    Total score ≥9 points indicates need for bone densitometry.

    References (Vancouver style):
    1. Cadarette SM, Jaglal SB, Kreiger N, McIsaac WJ, Darlington GA, Tu JV. Development 
    and validation of the Osteoporosis Risk Assessment Instrument to facilitate selection 
    of women for bone densitometry. CMAJ. 2000 May 2;162(9):1289-94.
    2. El Maghraoui A, Habbassi A, Ghazi M, Achemlal L, Mounach A, Nouijai A, et al. 
    Validation and comparative evaluation of four osteoporosis risk assessment tools in 
    Moroccan menopausal women. Arch Osteoporos. 2006 Dec;1(1-2):35-42.
    3. Rubin KH, Abrahamsen B, Friis-Holmberg T, Hjelmborg JV, Bech M, Hermann AP, et al. 
    Comparison of different screening tools (FRAX®, OST, ORAI, OSIRIS, SCORE and age alone) 
    to identify women with increased risk of fracture. Bone. 2013 Sep;56(1):16-22.
    """
    
    age: Literal["45-54", "55-64", "65-74", "75_or_older"] = Field(
        ...,
        description="Patient age range. 45-54 years scores 0 points, 55-64 years scores 5 points, 65-74 years scores 9 points, 75 or older scores 15 points",
        example="55-64"
    )
    
    weight: Literal["over_69kg", "60-69kg", "under_60kg"] = Field(
        ...,
        description="Patient weight category. Over 69kg (>152 lbs) scores 0 points, 60-69kg (132-152 lbs) scores 3 points, under 60kg (<132 lbs) scores 9 points",
        example="60-69kg"
    )
    
    current_estrogen_use: Literal["yes", "no"] = Field(
        ...,
        description="Current estrogen use (hormone replacement therapy). Yes scores 0 points, No scores 2 points. This refers to current use at the time of assessment",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": "55-64",
                "weight": "60-69kg",
                "current_estrogen_use": "no"
            }
        }


class OraiResponse(BaseModel):
    """
    Response model for Osteoporosis Risk Assessment Instrument (ORAI)
    
    The ORAI score ranges from 0 to 26 points and classifies patients into:
    - Low risk (<9 points): Bone densitometry may not be needed
    - High risk (≥9 points): Consider bone densitometry
    
    Reference: Cadarette SM, et al. CMAJ. 2000;162(9):1289-94.
    """
    
    result: int = Field(
        ...,
        description="ORAI score calculated from clinical variables (range: 0-26 points)",
        example=10
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended next steps based on the score",
        example="This patient scores 10 points on the ORAI scale. Bone densitometry should be considered for this patient. The ORAI has a sensitivity of 93.3% and specificity of 46.4% for identifying women with low bone mineral density."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low risk or High risk)",
        example="High risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Consider bone densitometry"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 10,
                "unit": "points",
                "interpretation": "This patient scores 10 points on the ORAI scale. Bone densitometry should be considered for this patient. The ORAI has a sensitivity of 93.3% and specificity of 46.4% for identifying women with low bone mineral density.",
                "stage": "High risk",
                "stage_description": "Consider bone densitometry"
            }
        }