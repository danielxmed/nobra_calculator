"""
ASTRAL Score for Ischemic Stroke Models

Request and response models for ASTRAL score calculation.

References (Vancouver style):
1. Ntaios G, Faouzi M, Ferrari J, Lang W, Vemmos K, Michel P. An integer-based 
   score to predict functional outcome in acute ischemic stroke: the ASTRAL score. 
   Neurology. 2012;78(24):1916-22. doi: 10.1212/WNL.0b013e318259e221.
2. Ntaios G, Gioulekas F, Papavasileiou V, Strbian D, Michel P. ASTRAL, DRAGON 
   and SEDAN scores predict stroke outcome more accurately than physicians. 
   Eur J Neurol. 2016;23(11):1651-1657. doi: 10.1111/ene.13100.
3. Liu G, Ntaios G, Zheng H, Wang Y, Michel P, Wang Y. External validation of 
   the ASTRAL score to predict 3- and 12-month functional outcome in the China 
   National Stroke Registry. Stroke. 2013;44(6):1443-50. doi: 10.1161/STROKEAHA.113.001047.

The ASTRAL score is a validated prognostic tool that predicts 90-day poor outcome 
(modified Rankin Scale >2) in patients with acute ischemic stroke. It combines six 
clinical variables: age, NIHSS score, time from onset to admission, visual field 
defects, glucose abnormalities, and consciousness level. The score has been externally 
validated with excellent discriminative ability (AUC ~0.82) and is more accurate 
than physician estimates for stroke outcome prediction.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AstralScoreRequest(BaseModel):
    """
    Request model for ASTRAL Score for Ischemic Stroke
    
    The ASTRAL score uses six clinical variables to predict 90-day poor outcome 
    (mRS >2) in acute ischemic stroke patients:
    
    Clinical Variables:
    - Age: Patient age in years (directly added to score)
    - NIHSS Score: National Institutes of Health Stroke Scale (0-42 points, directly added)
    - Onset >3h: >3 hours from symptom onset to admission (+2 points if yes)
    - Visual field defect: Any new visual field defect (+2 points if yes)
    - Abnormal glucose: Admission glucose >131 mg/dL or <66 mg/dL (+1 point if yes)
    - Impaired consciousness: Altered consciousness at admission (+3 points if yes)
    
    Score Calculation: Age + NIHSS + onset >3h + visual defect + glucose + consciousness
    
    Interpretation:
    - 0-15 points: Low risk (better prognosis for functional independence)
    - 16-25 points: Moderate risk (requires careful monitoring and rehabilitation)
    - ≥26 points: High risk (significant disability/death risk, consider palliative care)
    
    References (Vancouver style):
    1. Ntaios G, Faouzi M, Ferrari J, Lang W, Vemmos K, Michel P. An integer-based 
    score to predict functional outcome in acute ischemic stroke: the ASTRAL score. 
    Neurology. 2012;78(24):1916-22. doi: 10.1212/WNL.0b013e318259e221.
    2. Ntaios G, Gioulekas F, Papavasileiou V, Strbian D, Michel P. ASTRAL, DRAGON 
    and SEDAN scores predict stroke outcome more accurately than physicians. 
    Eur J Neurol. 2016;23(11):1651-1657. doi: 10.1111/ene.13100.
    3. Liu G, Ntaios G, Zheng H, Wang Y, Michel P, Wang Y. External validation of 
    the ASTRAL score to predict 3- and 12-month functional outcome in the China 
    National Stroke Registry. Stroke. 2013;44(6):1443-50. doi: 10.1161/STROKEAHA.113.001047.
    """
    
    age: int = Field(
        ...,
        description="Patient age in years. This value is directly added to the final score",
        ge=0,
        le=120,
        example=75
    )
    
    nihss_score: int = Field(
        ...,
        description="National Institutes of Health Stroke Scale (NIHSS) score ranging from 0-42 points. Higher scores indicate more severe stroke. This value is directly added to the final score",
        ge=0,
        le=42,
        example=12
    )
    
    onset_to_admission_over_3h: Literal["yes", "no"] = Field(
        ...,
        description="More than 3 hours elapsed from symptom onset (or last time seen without stroke symptoms) to hospital admission. Adds 2 points if 'yes'",
        example="yes"
    )
    
    visual_field_defect: Literal["yes", "no"] = Field(
        ...,
        description="Presence of any new visual field defect (hemianopia, quadrantanopia, etc.). Adds 2 points if 'yes'",
        example="no"
    )
    
    abnormal_glucose: Literal["yes", "no"] = Field(
        ...,
        description="Admission glucose >131 mg/dL (7.3 mmol/L) or <66 mg/dL (3.7 mmol/L). Both hyperglycemia and hypoglycemia are associated with worse outcomes. Adds 1 point if 'yes'",
        example="no"
    )
    
    impaired_consciousness: Literal["yes", "no"] = Field(
        ...,
        description="Impaired consciousness at admission (altered mental status, decreased alertness, stupor, coma). Adds 3 points if 'yes'",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 75,
                "nihss_score": 12,
                "onset_to_admission_over_3h": "yes",
                "visual_field_defect": "no",
                "abnormal_glucose": "no",
                "impaired_consciousness": "no"
            }
        }


class AstralScoreResponse(BaseModel):
    """
    Response model for ASTRAL Score for Ischemic Stroke
    
    The ASTRAL score ranges from the patient's age plus NIHSS score (minimum) to 
    approximately 50+ points (maximum), stratifying patients into risk categories 
    for 90-day poor outcome (mRS >2):
    
    - Low Risk (0-15 points): Better prognosis for functional independence
    - Moderate Risk (16-25 points): Requires monitoring and rehabilitation planning
    - High Risk (≥26 points): High risk for disability/death, consider goals of care
    
    The score has been validated with AUC of ~0.82 and is more accurate than 
    clinical judgment alone.
    
    Reference: Ntaios G, et al. Neurology. 2012;78(24):1916-22.
    """
    
    result: int = Field(
        ...,
        description="ASTRAL score calculated from clinical variables (typically ranges from patient age + NIHSS to 50+ points)",
        example=89
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and prognosis based on the calculated score",
        example="Scores ≥26 points indicate high probability of poor outcome (mRS >2) at 90 days. These patients are at high risk for significant disability or death and may benefit from palliative care discussions."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on score (Low Risk, Moderate Risk, High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="High probability of poor outcome"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 89,
                "unit": "points",
                "interpretation": "Scores ≥26 points indicate high probability of poor outcome (mRS >2) at 90 days. These patients are at high risk for significant disability or death and may benefit from palliative care discussions.",
                "stage": "High Risk",
                "stage_description": "High probability of poor outcome"
            }
        }
