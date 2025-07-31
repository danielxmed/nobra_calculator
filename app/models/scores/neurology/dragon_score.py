"""
DRAGON Score for Post-TPA Stroke Outcome Models

Request and response models for DRAGON Score calculation.

References (Vancouver style):
1. Strbian D, Meretoja A, Ahlhelm FJ, et al. Predicting outcome of IV thrombolysis-treated 
   ischemic stroke patients: the DRAGON score. Neurology. 2012;78(6):427-432. 
   doi: 10.1212/WNL.0b013e318245d2a9.
2. Turc G, Maïer B, Naggara O, et al. Clinical scales do not reliably identify acute 
   ischemic stroke patients with large-artery occlusion. Stroke. 2016;47(6):1466-1472. 
   doi: 10.1161/STROKEAHA.115.011336.
3. Saposnik G, Guzik AK, Reeves M, et al. Stroke Prognosis Assessment Scale (SPAS) to 
   predict mortality and functional outcome. Stroke. 2014;45(7):2018-2024. 
   doi: 10.1161/STROKEAHA.114.004667.

The DRAGON score predicts 3-month functional outcome (modified Rankin Scale 0-2) in 
ischemic stroke patients treated with intravenous tissue plasminogen activator (tPA). 
The acronym DRAGON stands for: Dense cerebral artery sign or early infarct signs (D), 
prestroke modified Rankin Scale >1 (R), Age (A), Glucose level at baseline (G), 
Onset to treatment time (O), and baseline NIHSS score (N).
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict


class DragonScoreRequest(BaseModel):
    """
    Request model for DRAGON Score for Post-TPA Stroke Outcome
    
    The DRAGON score uses 6 clinical variables to predict 3-month functional outcome
    in ischemic stroke patients treated with IV tPA:
    
    1. Dense cerebral artery/early infarct signs on CT (0-2 points)
    2. Pre-stroke modified Rankin Scale >1 (0-1 points)
    3. Age (<65: 0, 65-79: 1, ≥80: 2 points)
    4. Glucose level >144 mg/dL (0-1 points)
    5. Onset to treatment time >90 minutes (0-1 points)
    6. Baseline NIHSS score (0-4: 0, 5-9: 1, 10-15: 2, ≥16: 3 points)
    
    Score range: 0-10 points
    - Lower scores indicate better prognosis
    - 0-1: 96% chance of good outcome
    - 9-10: 100% chance of miserable outcome

    References (Vancouver style):
    1. Strbian D, Meretoja A, Ahlhelm FJ, et al. Predicting outcome of IV thrombolysis-treated 
       ischemic stroke patients: the DRAGON score. Neurology. 2012;78(6):427-432. 
       doi: 10.1212/WNL.0b013e318245d2a9.
    2. Turc G, Maïer B, Naggara O, et al. Clinical scales do not reliably identify acute 
       ischemic stroke patients with large-artery occlusion. Stroke. 2016;47(6):1466-1472. 
       doi: 10.1161/STROKEAHA.115.011336.
    3. Saposnik G, Guzik AK, Reeves M, et al. Stroke Prognosis Assessment Scale (SPAS) to 
       predict mortality and functional outcome. Stroke. 2014;45(7):2018-2024. 
       doi: 10.1161/STROKEAHA.114.004667.
    """
    
    hyperdense_artery_infarct: Literal["none", "either", "both"] = Field(
        ...,
        description="Hyperdense cerebral artery sign or early infarct signs on admission CT scan. 'none' = neither present (0 points), 'either' = one present (1 point), 'both' = both present (2 points)",
        example="none"
    )
    
    prestroke_mrs: Literal["no", "yes"] = Field(
        ...,
        description="Pre-stroke modified Rankin Scale (mRS) score greater than 1. 'no' = mRS ≤1 (0 points), 'yes' = mRS >1 (1 point)",
        example="no"
    )
    
    age: int = Field(
        ...,
        description="Patient age in years. <65 years = 0 points, 65-79 years = 1 point, ≥80 years = 2 points",
        ge=18,
        le=120,
        example=72
    )
    
    glucose: float = Field(
        ...,
        description="Baseline glucose level in mg/dL. ≤144 mg/dL = 0 points, >144 mg/dL = 1 point",
        ge=50,
        le=800,
        example=120
    )
    
    onset_to_treatment: int = Field(
        ...,
        description="Time from symptom onset to treatment initiation in minutes. ≤90 minutes = 0 points, >90 minutes = 1 point",
        ge=0,
        le=480,
        example=75
    )
    
    nihss: int = Field(
        ...,
        description="Baseline National Institutes of Health Stroke Scale (NIHSS) score. 0-4 = 0 points, 5-9 = 1 point, 10-15 = 2 points, ≥16 = 3 points",
        ge=0,
        le=42,
        example=8
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "hyperdense_artery_infarct": "none",
                "prestroke_mrs": "no",
                "age": 72,
                "glucose": 120,
                "onset_to_treatment": 75,
                "nihss": 8
            }
        }


class DragonScoreResponse(BaseModel):
    """
    Response model for DRAGON Score for Post-TPA Stroke Outcome
    
    The DRAGON score predicts 3-month functional outcome in stroke patients:
    - 0-1 points: Excellent prognosis (96% good outcome)
    - 2 points: Good prognosis (88% good outcome) 
    - 3 points: Moderate prognosis (74% good outcome)
    - 4-7 points: Poor prognosis (decreasing good outcome chance)
    - 8 points: Very poor prognosis (0% good outcome, 70% miserable outcome)
    - 9-10 points: Miserable prognosis (0% good outcome, 100% miserable outcome)
    
    Good outcome = mRS 0-2 (functional independence)
    Miserable outcome = mRS 5-6 (bedridden, incontinent, requiring constant care, or death)
    
    Reference: Strbian D, et al. Neurology. 2012;78(6):427-432.
    """
    
    result: int = Field(
        ...,
        description="DRAGON score calculated from clinical variables (range: 0-10 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and prognosis based on the DRAGON score",
        example="88% chance of good outcome (mRS 0-2 at 3 months). Good functional prognosis with high likelihood of functional independence."
    )
    
    stage: str = Field(
        ...,
        description="Prognostic category (Excellent, Good, Moderate, Poor, Very Poor, or Miserable Prognosis)",
        example="Good Prognosis"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the prognostic category",
        example="Low risk"
    )
    
    component_scores: Dict[str, int] = Field(
        ...,
        description="Individual component scores contributing to the total DRAGON score",
        example={
            "hyperdense_artery": 0,
            "prestroke_mrs": 0,
            "age": 1,
            "glucose": 0,
            "onset_time": 0,
            "nihss": 1
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "88% chance of good outcome (mRS 0-2 at 3 months). Good functional prognosis with high likelihood of functional independence.",
                "stage": "Good Prognosis",
                "stage_description": "Low risk",
                "component_scores": {
                    "hyperdense_artery": 0,
                    "prestroke_mrs": 0,
                    "age": 1,
                    "glucose": 0,
                    "onset_time": 0,
                    "nihss": 1
                }
            }
        }