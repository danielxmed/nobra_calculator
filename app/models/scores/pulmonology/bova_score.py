"""
Bova Score for Pulmonary Embolism Complications Models

Request and response models for Bova Score calculation.

References (Vancouver style):
1. Bova C, Sanchez O, Prandoni P, Lankeit M, Konstantinides S, Vanni S, et al. 
   Identification of intermediate-risk patients with acute symptomatic pulmonary 
   embolism. Eur Respir J. 2014 Sep;44(3):694-703. doi: 10.1183/09031936.00006114.
2. Fernández C, Bova C, Sanchez O, Prandoni P, Lankeit M, Konstantinides S, et al. 
   Validation of a Model for Identification of Patients at Intermediate to High Risk 
   for Complications Associated With Acute Symptomatic Pulmonary Embolism. Chest. 
   2015 Jul;148(1):211-218. doi: 10.1378/chest.14-2551.

The Bova Score is a risk stratification tool that predicts 30-day risk of PE-related 
complications (death, hemodynamic collapse, or recurrent PE) in hemodynamically stable 
patients with confirmed pulmonary embolism. It combines clinical parameters (blood pressure, 
heart rate) with biomarkers (troponin) and imaging findings (RV dysfunction) to classify 
patients into three risk categories.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class BovaScoreRequest(BaseModel):
    """
    Request model for Bova Score for Pulmonary Embolism Complications
    
    The Bova Score uses 4 parameters to assess risk in hemodynamically stable PE patients:
    
    1. Systolic Blood Pressure:
       - >100 mmHg: 0 points
       - 90-100 mmHg: 2 points
       - <90 mmHg: Not eligible (hemodynamically unstable)
    
    2. Elevated Cardiac Troponin:
       - No: 0 points
       - Yes: 2 points (any elevation above normal reference range)
    
    3. Right Ventricular (RV) Dysfunction:
       - No: 0 points
       - Yes: 2 points
       - Defined by TTE: RV/LV ratio >0.9, sPAP >30, RV EDD >30mm, RV dilation, or free wall hypokinesis
       - Defined by CT: RV/LV ratio >1 (short axis diameter)
    
    4. Heart Rate:
       - <110 beats/min: 0 points
       - ≥110 beats/min: 1 point
    
    Total score ranges from 0-7 points, stratifying patients into three risk categories.
    
    References:
    1. Bova C, et al. Eur Respir J. 2014;44(3):694-703.
    2. Fernández C, et al. Chest. 2015;148(1):211-218.
    """
    
    systolic_bp: int = Field(
        ...,
        ge=90,
        le=300,
        description="Systolic blood pressure in mmHg. Must be ≥90 for score eligibility (hemodynamically stable patients only). Scores 2 points if 90-100 mmHg, 0 points if >100 mmHg",
        example=95
    )
    
    elevated_troponin: Literal["yes", "no"] = Field(
        ...,
        description="Elevated cardiac troponin above normal reference range. Any elevation counts. Scores 2 points if yes, 0 points if no",
        example="yes"
    )
    
    rv_dysfunction: Literal["yes", "no"] = Field(
        ...,
        description="Right ventricular dysfunction on imaging. TTE criteria: RV/LV >0.9, sPAP >30 mmHg, RV EDD >30mm, RV dilation, or free wall hypokinesis. CT criteria: RV/LV >1. Scores 2 points if yes, 0 points if no",
        example="yes"
    )
    
    heart_rate: int = Field(
        ...,
        ge=30,
        le=250,
        description="Heart rate in beats per minute. Scores 1 point if ≥110 bpm, 0 points if <110 bpm",
        example=115
    )
    
    @validator('systolic_bp')
    def validate_hemodynamic_stability(cls, v):
        """Ensures patient is hemodynamically stable"""
        if v < 90:
            raise ValueError("Bova score is only applicable for hemodynamically stable patients (systolic BP ≥90 mmHg)")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "systolic_bp": 95,
                "elevated_troponin": "yes",
                "rv_dysfunction": "yes",
                "heart_rate": 115
            }
        }


class BovaScoreResponse(BaseModel):
    """
    Response model for Bova Score for Pulmonary Embolism Complications
    
    The Bova Score stratifies patients into three risk stages:
    - Stage I (0-2 points): Low risk - 4.4% complications, 3.1% mortality
    - Stage II (3-4 points): Intermediate risk - 18% complications, 6.8% mortality  
    - Stage III (>4 points): High risk - 42% complications, 10% mortality
    
    PE-related complications include death, hemodynamic collapse, or recurrent PE within 30 days.
    
    Reference: Bova C, et al. Eur Respir J. 2014;44(3):694-703.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=7,
        description="Bova score calculated from clinical parameters (range: 0-7 points)",
        example=5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk percentages and management recommendations",
        example="42% risk of PE-related complications and 10% PE-related mortality at 30 days. Requires hospital admission and close monitoring. Consider ICU admission and advanced therapies such as thrombolysis or embolectomy."
    )
    
    stage: str = Field(
        ...,
        description="Risk stage classification (Stage I, Stage II, or Stage III)",
        example="Stage III"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="High risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5,
                "unit": "points",
                "interpretation": "42% risk of PE-related complications and 10% PE-related mortality at 30 days. Requires hospital admission and close monitoring. Consider ICU admission and advanced therapies such as thrombolysis or embolectomy.",
                "stage": "Stage III",
                "stage_description": "High risk"
            }
        }