"""
Direct-Acting Oral Anticoagulants (DOAC) Score Models

Request and response models for DOAC Score calculation.

References (Vancouver style):
1. Aggarwal A, Wang TY, Rumsfeld JS, Turakhia MP, Sauer AJ, Gersh BJ, et al. 
   Development and Validation of the DOAC Score: A Novel Bleeding Risk Prediction 
   Tool for Patients With Atrial Fibrillation on Direct-Acting Oral Anticoagulants. 
   Circulation. 2023 Nov 7;148(19):1482-1492. doi: 10.1161/CIRCULATIONAHA.123.064556.
2. Costa OS, Beyer-Westendorf J, Ashton V, Milentijevic D, Tzikas A, Bezuidenhout A, 
   et al. Performance of HAS-BLED and DOAC scores to predict major bleeding events in 
   atrial fibrillation patients treated with direct oral anticoagulants: A report from 
   a prospective European observational registry. Thromb Res. 2024 Aug;240:109063. 
   doi: 10.1016/j.thromres.2024.109063.
3. Ding WY, Gupta D, Wong CF, Lip GYH. Pathophysiology of atrial fibrillation and 
   chronic kidney disease. Cardiovasc Res. 2021 Mar 1;117(4):1046-1059. 
   doi: 10.1093/cvr/cvaa258.

The DOAC Score predicts bleeding risk in patients with atrial fibrillation on 
direct-acting oral anticoagulants (DOACs). It was developed specifically for DOAC-treated 
patients and demonstrates superior performance compared to the HAS-BLED score. The score 
incorporates 10 parameters: age (0-5 points), creatinine clearance (0-2 points), and 
8 clinical risk factors (1 point each). Total scores range from 0-10 and classify 
patients into five bleeding risk categories: very low (0-3), low (4-5), moderate (6-7), 
high (8-9), and very high (10). Each additional point is associated with a 48.7% 
increase in major bleeding risk.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class DoacScoreRequest(BaseModel):
    """
    Request model for Direct-Acting Oral Anticoagulants (DOAC) Score
    
    The DOAC Score evaluates bleeding risk in AF patients on DOACs using 10 parameters:
    
    Age Categories (0-5 points):
    - under_65: Age <65 years (0 points)
    - 65_to_69: Age 65-69 years (2 points)
    - 70_to_74: Age 70-74 years (3 points)
    - 75_to_79: Age 75-79 years (4 points)
    - 80_or_over: Age ≥80 years (5 points)
    
    Creatinine Clearance Categories (0-2 points):
    - over_60: >60 mL/min (0 points)
    - 30_to_60: 30-60 mL/min (1 point)
    - under_30: <30 mL/min (2 points)
    
    Risk Factors (1 point each if present):
    - Underweight (BMI <18.5 kg/m²)
    - History of stroke, TIA, or systemic embolism
    - Diabetes mellitus
    - Hypertension
    - Current antiplatelet agent use
    - Current NSAID use
    - History of major bleeding
    - Liver disease

    References (Vancouver style):
    1. Aggarwal A, Wang TY, Rumsfeld JS, Turakhia MP, Sauer AJ, Gersh BJ, et al. 
       Development and Validation of the DOAC Score: A Novel Bleeding Risk Prediction 
       Tool for Patients With Atrial Fibrillation on Direct-Acting Oral Anticoagulants. 
       Circulation. 2023 Nov 7;148(19):1482-1492. doi: 10.1161/CIRCULATIONAHA.123.064556.
    2. Costa OS, Beyer-Westendorf J, Ashton V, Milentijevic D, Tzikas A, Bezuidenhout A, 
       et al. Performance of HAS-BLED and DOAC scores to predict major bleeding events in 
       atrial fibrillation patients treated with direct oral anticoagulants. Thromb Res. 
       2024 Aug;240:109063. doi: 10.1016/j.thromres.2024.109063.
    """
    
    age_category: Literal["under_65", "65_to_69", "70_to_74", "75_to_79", "80_or_over"] = Field(
        ...,
        description="Patient age category. Under 65 (0 pts), 65-69 (2 pts), 70-74 (3 pts), 75-79 (4 pts), ≥80 (5 pts)",
        example="70_to_74"
    )
    
    creatinine_clearance_category: Literal["over_60", "30_to_60", "under_30"] = Field(
        ...,
        description="Creatinine clearance category. >60 mL/min (0 pts), 30-60 mL/min (1 pt), <30 mL/min (2 pts)",
        example="over_60"
    )
    
    underweight: Literal["yes", "no"] = Field(
        ...,
        description="BMI <18.5 kg/m². Scores 1 point if yes",
        example="no"
    )
    
    stroke_tia_embolism_history: Literal["yes", "no"] = Field(
        ...,
        description="History of stroke, transient ischemic attack, or systemic embolism. Scores 1 point if yes",
        example="no"
    )
    
    diabetes: Literal["yes", "no"] = Field(
        ...,
        description="Diabetes mellitus. Scores 1 point if yes",
        example="yes"
    )
    
    hypertension: Literal["yes", "no"] = Field(
        ...,
        description="Hypertension. Scores 1 point if yes",
        example="yes"
    )
    
    antiplatelet_use: Literal["yes", "no"] = Field(
        ...,
        description="Current antiplatelet agent use (aspirin, clopidogrel, etc.). Scores 1 point if yes",
        example="no"
    )
    
    nsaid_use: Literal["yes", "no"] = Field(
        ...,
        description="Current nonsteroidal anti-inflammatory drug (NSAID) use. Scores 1 point if yes",
        example="no"
    )
    
    bleeding_history: Literal["yes", "no"] = Field(
        ...,
        description="History of major bleeding. Scores 1 point if yes",
        example="no"
    )
    
    liver_disease: Literal["yes", "no"] = Field(
        ...,
        description="Liver disease. Scores 1 point if yes",
        example="no"
    )
    
    @field_validator('age_category')
    def validate_age_category(cls, v):
        valid_ages = ["under_65", "65_to_69", "70_to_74", "75_to_79", "80_or_over"]
        if v not in valid_ages:
            raise ValueError(f"age_category must be one of: {valid_ages}")
        return v
    
    @field_validator('creatinine_clearance_category')
    def validate_creatinine_category(cls, v):
        valid_categories = ["over_60", "30_to_60", "under_30"]
        if v not in valid_categories:
            raise ValueError(f"creatinine_clearance_category must be one of: {valid_categories}")
        return v
    
    @field_validator('underweight', 'stroke_tia_embolism_history', 'diabetes', 'hypertension', 
              'antiplatelet_use', 'nsaid_use', 'bleeding_history', 'liver_disease')
    def validate_yes_no_fields(cls, v):
        if v not in ["yes", "no"]:
            raise ValueError("Field must be 'yes' or 'no'")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "age_category": "70_to_74",
                "creatinine_clearance_category": "over_60",
                "underweight": "no",
                "stroke_tia_embolism_history": "no",
                "diabetes": "yes",
                "hypertension": "yes",
                "antiplatelet_use": "no",
                "nsaid_use": "no",
                "bleeding_history": "no",
                "liver_disease": "no"
            }
        }


class DoacScoreResponse(BaseModel):
    """
    Response model for Direct-Acting Oral Anticoagulants (DOAC) Score
    
    The DOAC Score ranges from 0-10 points and classifies patients into five bleeding risk categories:
    - Very Low (0-3 points): Annual bleeding rate ~0.3-0.8%
    - Low (4-5 points): Annual bleeding rate ~1.1-1.9%
    - Moderate (6-7 points): Annual bleeding rate ~2.5-4.1%
    - High (8-9 points): Annual bleeding rate ~5.2-8.1%
    - Very High (10 points): Annual bleeding rate ~10.8%
    
    The score demonstrates superior performance compared to HAS-BLED in DOAC-treated patients,
    with each additional point associated with a 48.7% increase in major bleeding risk.
    
    Reference: Aggarwal A, et al. Circulation. 2023;148(19):1482-1492.
    """
    
    result: int = Field(
        ...,
        description="DOAC score calculated from clinical parameters (range: 0-10 points)",
        example=5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and bleeding risk assessment with recommendations",
        example="Low bleeding risk. Patient may continue DOAC therapy with standard monitoring. Annual bleeding rate approximately 1.1-1.9%."
    )
    
    stage: str = Field(
        ...,
        description="Bleeding risk category (Very Low, Low, Moderate, High, Very High)",
        example="Low"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the bleeding risk category",
        example="Low bleeding risk"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 5,
                "unit": "points",
                "interpretation": "Low bleeding risk. Patient may continue DOAC therapy with standard monitoring. Annual bleeding rate approximately 1.1-1.9%.",
                "stage": "Low",
                "stage_description": "Low bleeding risk"
            }
        }