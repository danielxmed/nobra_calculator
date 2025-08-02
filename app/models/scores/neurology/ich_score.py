"""
Intracerebral Hemorrhage (ICH) Score Models

Request and response models for ICH Score calculation.

References (Vancouver style):
1. Hemphill JC 3rd, Bonovich DC, Besmertis L, Manley GT, Johnston SC. The ICH score: a 
   simple, reliable grading scale for intracerebral hemorrhage. Stroke. 2001 Apr;32(4):891-7. 
   doi: 10.1161/01.str.32.4.891.
2. Rost NS, Smith EE, Chang Y, Snider RW, Chanderraj R, Schwab K, et al. Prediction of 
   functional outcome in patients with primary intracerebral hemorrhage: the FUNC score. 
   Stroke. 2008 Aug;39(8):2304-9. doi: 10.1161/STROKEAHA.107.512202.
3. Godoy DA, Pinero G, Papa F. Predicting mortality in spontaneous intracerebral hemorrhage: 
   can modification to original score improve the prediction? Stroke. 2006 Apr;37(4):1038-44. 
   doi: 10.1161/01.STR.0000206441.79646.49.

The Intracerebral Hemorrhage (ICH) Score is a validated clinical grading scale that 
predicts 30-day mortality in patients with spontaneous intracerebral hemorrhage. It uses 
five independent risk factors: Glasgow Coma Scale score, age ≥80 years, infratentorial 
location, ICH volume ≥30 cm³, and intraventricular hemorrhage presence. The score ranges 
from 0-6 points with excellent discrimination for mortality prediction and is widely used 
for clinical decision-making and prognostic discussions.
"""

from pydantic import BaseModel, Field
from typing import Literal


class IchScoreRequest(BaseModel):
    """
    Request model for Intracerebral Hemorrhage (ICH) Score
    
    The ICH Score uses five independent risk factors to predict 30-day mortality:
    
    Glasgow Coma Scale (GCS):
    - 13_15: GCS 13-15 (0 points) - normal to mild impairment
    - 5_12: GCS 5-12 (1 point) - moderate impairment
    - 3_4: GCS 3-4 (2 points) - severe impairment
    
    Age:
    - under_80: Age <80 years (0 points)
    - 80_or_older: Age ≥80 years (1 point)
    
    ICH Location:
    - supratentorial: Above tentorium cerebelli (0 points)
    - infratentorial: Below tentorium cerebelli, brainstem/cerebellum (1 point)
    
    ICH Volume:
    - less_than_30: <30 cm³ (0 points)
    - 30_or_greater: ≥30 cm³ (1 point)
    
    Intraventricular Hemorrhage (IVH):
    - absent: No IVH (0 points)
    - present: IVH present (1 point)
    
    ICH volume is calculated using the ABC/2 ellipsoid method:
    A = largest diameter, B = perpendicular diameter, C = number of slices × slice thickness

    References (Vancouver style):
    1. Hemphill JC 3rd, Bonovich DC, Besmertis L, Manley GT, Johnston SC. The ICH score: a 
    simple, reliable grading scale for intracerebral hemorrhage. Stroke. 2001 Apr;32(4):891-7. 
    doi: 10.1161/01.str.32.4.891.
    2. Rost NS, Smith EE, Chang Y, Snider RW, Chanderraj R, Schwab K, et al. Prediction of 
    functional outcome in patients with primary intracerebral hemorrhage: the FUNC score. 
    Stroke. 2008 Aug;39(8):2304-9. doi: 10.1161/STROKEAHA.107.512202.
    3. Godoy DA, Pinero G, Papa F. Predicting mortality in spontaneous intracerebral hemorrhage: 
    can modification to original score improve the prediction? Stroke. 2006 Apr;37(4):1038-44. 
    doi: 10.1161/01.STR.0000206441.79646.49.
    """
    
    glasgow_coma_scale: Literal["13_15", "5_12", "3_4"] = Field(
        ...,
        description="Glasgow Coma Scale score at presentation or transfer from emergency department. GCS 13-15 scores 0 points (normal to mild impairment), GCS 5-12 scores 1 point (moderate impairment), GCS 3-4 scores 2 points (severe impairment)",
        example="13_15"
    )
    
    age: Literal["under_80", "80_or_older"] = Field(
        ...,
        description="Patient age at presentation. Age <80 years scores 0 points, age ≥80 years scores 1 point. Age ≥80 is an independent risk factor for poor outcome",
        example="under_80"
    )
    
    ich_location: Literal["supratentorial", "infratentorial"] = Field(
        ...,
        description="Location of intracerebral hemorrhage on CT scan. Supratentorial location (above tentorium cerebelli) scores 0 points, infratentorial location (brainstem/cerebellum) scores 1 point due to critical anatomical structures",
        example="supratentorial"
    )
    
    ich_volume: Literal["less_than_30", "30_or_greater"] = Field(
        ...,
        description="ICH volume calculated using ABC/2 ellipsoid method on initial CT scan. Volume <30 cm³ scores 0 points, volume ≥30 cm³ scores 1 point. ABC/2 method: A=largest diameter, B=perpendicular diameter, C=number of slices × slice thickness",
        example="less_than_30"
    )
    
    intraventricular_hemorrhage: Literal["absent", "present"] = Field(
        ...,
        description="Presence of intraventricular hemorrhage (IVH) on CT scan. Absent IVH scores 0 points, present IVH scores 1 point. IVH indicates extension into ventricular system and worsens prognosis",
        example="absent"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "glasgow_coma_scale": "13_15",
                "age": "under_80",
                "ich_location": "supratentorial",
                "ich_volume": "less_than_30",
                "intraventricular_hemorrhage": "absent"
            }
        }


class IchScoreResponse(BaseModel):
    """
    Response model for Intracerebral Hemorrhage (ICH) Score
    
    The ICH Score ranges from 0-6 points with corresponding 30-day mortality rates:
    
    Mortality Risk by Score:
    - Score 0: 0-5% mortality (Very Low Risk)
    - Score 1: ~16% mortality (Low Risk)
    - Score 2: ~33% mortality (Moderate Risk)
    - Score 3: ~54% mortality (High Risk)
    - Score 4: ~93% mortality (Very High Risk)
    - Score 5-6: 95-100% mortality (Extremely High Risk)
    
    The score provides excellent discrimination for mortality prediction and facilitates
    clinical decision-making, prognostic discussions, and treatment planning.
    
    Reference: Hemphill JC 3rd, et al. Stroke. 2001;32(4):891-7.
    """
    
    result: int = Field(
        ...,
        description="ICH score calculated from five risk factors (range: 0-6 points)",
        example=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with 30-day mortality prediction and management recommendations",
        example="Excellent prognosis. 30-day mortality: 0-5%. All patients with ICH Score 0 survived in the original validation study. Standard ICH management with close monitoring. Consider less aggressive interventions. Favorable outcome expected with appropriate care. Excellent candidate for rehabilitation planning."
    )
    
    stage: str = Field(
        ...,
        description="Mortality risk category (Very Low Risk, Low Risk, Moderate Risk, High Risk, Very High Risk, Extremely High Risk)",
        example="Very Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the score range",
        example="Score 0 points"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "Excellent prognosis. 30-day mortality: 0-5%. All patients with ICH Score 0 survived in the original validation study. Standard ICH management with close monitoring. Consider less aggressive interventions. Favorable outcome expected with appropriate care. Excellent candidate for rehabilitation planning.",
                "stage": "Very Low Risk",
                "stage_description": "Score 0 points"
            }
        }