"""
Functional Outcome in Patients With Primary Intracerebral Hemorrhage (FUNC) Score Models

Request and response models for FUNC Score calculation.

References (Vancouver style):
1. Rost NS, Smith EE, Chang Y, Snider RW, Chanderraj R, Schwab K, et al. Prediction 
   of functional outcome in patients with primary intracerebral hemorrhage: the FUNC 
   score. Stroke. 2008 Aug;39(8):2304-9. doi: 10.1161/STROKEAHA.107.512202.
2. Garrett JS, Zarghouni M, Layton KF, Graybeal D, Daoud YA. Validation of clinical 
   prediction scores in patients with primary intracerebral hemorrhage. Neurocrit Care. 
   2013 Dec;19(3):329-35. doi: 10.1007/s12028-013-9926-y.
3. Hemphill JC 3rd, Farrant M, Neill TA Jr. Prospective validation of the ICH Score 
   for 12-month functional outcome. Neurology. 2009 Oct 6;73(14):1088-94. 
   doi: 10.1212/WNL.0b013e3181b8b332.

The FUNC score predicts the likelihood of achieving functional independence (Glasgow 
Outcome Score ≥4) at 90 days following primary intracerebral hemorrhage. It uses five 
clinical parameters available at admission: ICH volume, age, ICH location, Glasgow Coma 
Scale, and pre-ICH cognitive impairment status.
"""

from pydantic import BaseModel, Field
from typing import Literal


class FuncScoreRequest(BaseModel):
    """
    Request model for Functional Outcome in Patients With Primary ICH (FUNC) Score
    
    The FUNC score uses five parameters to predict functional independence at 90 days:
    
    1. ICH Volume (cm³):
       - less_than_30: <30 cm³ (4 points) - smaller hemorrhages have better prognosis
       - 30_to_60: 30-60 cm³ (2 points) - moderate size with intermediate prognosis
       - greater_than_60: >60 cm³ (0 points) - large hemorrhages have poor prognosis
    
    2. Age:
       - less_than_70: <70 years (2 points) - younger patients have better recovery
       - 70_to_79: 70-79 years (1 point) - intermediate age group
       - 80_or_greater: ≥80 years (0 points) - advanced age associated with poor outcome
    
    3. ICH Location:
       - lobar: Cortical/subcortical location (2 points) - better prognosis
       - deep: Basal ganglia, thalamus, internal capsule (1 point) - intermediate
       - infratentorial: Brainstem or cerebellum (0 points) - worst prognosis
    
    4. Glasgow Coma Scale:
       - 9_or_greater: GCS ≥9 (2 points) - better consciousness level
       - 8_or_less: GCS ≤8 (0 points) - severe impairment of consciousness
    
    5. Pre-ICH Cognitive Impairment:
       - no: No pre-existing cognitive impairment (1 point)
       - yes: Pre-existing cognitive impairment (0 points)
    
    Total score ranges from 0-11 points. Higher scores indicate better prognosis.
    
    References (Vancouver style):
    1. Rost NS, Smith EE, Chang Y, Snider RW, Chanderraj R, Schwab K, et al. Prediction 
       of functional outcome in patients with primary intracerebral hemorrhage: the FUNC 
       score. Stroke. 2008 Aug;39(8):2304-9.
    2. Garrett JS, Zarghouni M, Layton KF, Graybeal D, Daoud YA. Validation of clinical 
       prediction scores in patients with primary intracerebral hemorrhage. Neurocrit Care. 
       2013 Dec;19(3):329-35.
    """
    
    ich_volume: Literal["less_than_30", "30_to_60", "greater_than_60"] = Field(
        ...,
        description="Volume of intracerebral hemorrhage on initial CT scan. <30 cm³ scores 4 points, 30-60 cm³ scores 2 points, >60 cm³ scores 0 points",
        example="less_than_30"
    )
    
    age: Literal["less_than_70", "70_to_79", "80_or_greater"] = Field(
        ...,
        description="Patient age at time of ICH. <70 years scores 2 points, 70-79 years scores 1 point, ≥80 years scores 0 points",
        example="less_than_70"
    )
    
    ich_location: Literal["lobar", "deep", "infratentorial"] = Field(
        ...,
        description="Location of intracerebral hemorrhage. Lobar (cortical/subcortical) scores 2 points, deep (basal ganglia/thalamus/internal capsule) scores 1 point, infratentorial (brainstem/cerebellum) scores 0 points",
        example="lobar"
    )
    
    glasgow_coma_scale: Literal["9_or_greater", "8_or_less"] = Field(
        ...,
        description="Glasgow Coma Scale score on admission. GCS ≥9 scores 2 points, GCS ≤8 scores 0 points",
        example="9_or_greater"
    )
    
    pre_ich_cognitive_impairment: Literal["yes", "no"] = Field(
        ...,
        description="Presence of cognitive impairment before the ICH. No impairment scores 1 point, presence of impairment scores 0 points",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "ich_volume": "less_than_30",
                "age": "less_than_70",
                "ich_location": "lobar",
                "glasgow_coma_scale": "9_or_greater",
                "pre_ich_cognitive_impairment": "no"
            }
        }


class FuncScoreResponse(BaseModel):
    """
    Response model for Functional Outcome in Patients With Primary ICH (FUNC) Score
    
    The FUNC score ranges from 0 to 11 points and predicts functional independence at 90 days:
    - 0-4 points: 0% achieve functional independence
    - 5-7 points: 13% overall (29% of survivors) achieve functional independence
    - 8 points: 42% overall (48% of survivors) achieve functional independence
    - 9-10 points: 66% overall (75% of survivors) achieve functional independence
    - 11 points: 82% overall (95% of survivors) achieve functional independence
    
    Functional independence is defined as Glasgow Outcome Score ≥4, meaning the patient
    can live independently with or without minor assistance.
    
    Clinical Use:
    - Calculate at initial ICH diagnosis for prognostication
    - Helps guide goals of care discussions with families
    - Aids in resource allocation and rehabilitation planning
    - Not intended for continuous monitoring or tracking changes
    
    Reference: Rost NS, et al. Stroke. 2008;39(8):2304-9.
    """
    
    result: int = Field(
        ...,
        description="FUNC score (0-11 points) predicting functional outcome at 90 days",
        example=11
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including prognosis and care recommendations",
        example="82% of all patients (95% of survivors) achieved functional independence at 90 days. Full supportive care with rehabilitation planning is strongly recommended."
    )
    
    stage: str = Field(
        ...,
        description="Prognosis category (Very Poor, Poor, Moderate, Good, or Excellent)",
        example="Excellent"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the functional independence likelihood",
        example="82% chance of functional independence"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 11,
                "unit": "points",
                "interpretation": "82% of all patients (95% of survivors) achieved functional independence at 90 days. Full supportive care with rehabilitation planning is strongly recommended.",
                "stage": "Excellent",
                "stage_description": "82% chance of functional independence"
            }
        }