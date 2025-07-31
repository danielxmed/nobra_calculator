"""
ABC Score for Massive Transfusion Models

Request and response models for ABC Score calculation.

References (Vancouver style):
1. Nunez TC, Voskresensky IV, Dossett LA, Shinall R, Hairston B, Ware DN, et al. 
   Early prediction of massive transfusion in trauma: simple as ABC (assessment of 
   blood consumption)? J Trauma. 2009 Feb;66(2):346-52. doi: 10.1097/TA.0b013e3181961c35.
2. Cotton BA, Dossett LA, Haut ER, Shafi S, Nunez TC, Au BK, et al. Multicenter 
   validation of a simplified score to predict massive transfusion in trauma. 
   J Trauma. 2010 Jul;69 Suppl 1:S33-9. doi: 10.1097/TA.0b013e3181e42411.
3. Jennings LK, Watson S. Massive Transfusion. In: StatPearls [Internet]. Treasure 
   Island (FL): StatPearls Publishing; 2023. PMID: 29763104.

The ABC Score (Assessment of Blood Consumption) is a clinical decision tool designed 
to predict the necessity for massive transfusion in trauma patients. It uses four 
easily obtainable clinical variables available at the time of initial assessment, 
requiring no laboratory values. The score was developed from a retrospective study 
of 596 trauma patients and validated in multiple trauma center registries involving 
over 1,600 patients. A score ≥2 indicates high risk for massive transfusion and 
should trigger activation of massive transfusion protocols.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AbcScoreRequest(BaseModel):
    """
    Request model for ABC Score for Massive Transfusion
    
    The ABC Score assesses four clinical variables to predict massive transfusion risk:
    
    Clinical Variables (each scored as yes=1 point, no=0 points):
    1. Penetrating mechanism - Presence of penetrating trauma (gunshot wound, stab wound, etc.)
    2. Systolic BP ≤90 mmHg - Hypotension in the Emergency Department  
    3. Heart rate ≥120 bpm - Tachycardia in the Emergency Department
    4. Positive FAST - Positive Focused Assessment with Sonography in Trauma examination
    
    Scoring:
    - Each criterion scores 1 point if present, 0 if absent
    - Total score ranges from 0 to 4 points
    - Score 0-1: Low risk for massive transfusion (NPV ~97%)
    - Score ≥2: High risk for massive transfusion (PPV ~55%, Sensitivity 75%, Specificity 86%)
    
    Clinical Application:
    - Designed for early trauma resuscitation decision-making
    - Helps identify patients who need immediate activation of massive transfusion protocol (MTP)
    - Uses only clinical variables available at initial assessment - no lab values required
    - Massive transfusion defined as ≥10 units of packed red blood cells in first 24 hours
    - Validated across multiple trauma centers with consistent performance
    
    References (Vancouver style):
    1. Nunez TC, Voskresensky IV, Dossett LA, Shinall R, Hairston B, Ware DN, et al. 
    Early prediction of massive transfusion in trauma: simple as ABC (assessment of 
    blood consumption)? J Trauma. 2009 Feb;66(2):346-52. doi: 10.1097/TA.0b013e3181961c35.
    2. Cotton BA, Dossett LA, Haut ER, Shafi S, Nunez TC, Au BK, et al. Multicenter 
    validation of a simplified score to predict massive transfusion in trauma. 
    J Trauma. 2010 Jul;69 Suppl 1:S33-9. doi: 10.1097/TA.0b013e3181e42411.
    3. Jennings LK, Watson S. Massive Transfusion. In: StatPearls [Internet]. Treasure 
    Island (FL): StatPearls Publishing; 2023. PMID: 29763104.
    """
    
    penetrating_mechanism: Literal["yes", "no"] = Field(
        ...,
        description="Presence of penetrating mechanism of injury (gunshot wound, stab wound, penetrating object). Scores 1 point if yes, 0 if no",
        example="no"
    )
    
    systolic_bp_90_or_less: Literal["yes", "no"] = Field(
        ...,
        description="Systolic blood pressure ≤90 mmHg measured in the Emergency Department. Scores 1 point if yes, 0 if no",
        example="yes"
    )
    
    heart_rate_120_or_more: Literal["yes", "no"] = Field(
        ...,
        description="Heart rate ≥120 beats per minute measured in the Emergency Department. Scores 1 point if yes, 0 if no",
        example="yes"
    )
    
    positive_fast: Literal["yes", "no"] = Field(
        ...,
        description="Positive FAST (Focused Assessment with Sonography in Trauma) ultrasound examination showing free fluid/blood. Scores 1 point if yes, 0 if no",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "penetrating_mechanism": "no",
                "systolic_bp_90_or_less": "yes",
                "heart_rate_120_or_more": "yes", 
                "positive_fast": "no"
            }
        }


class AbcScoreResponse(BaseModel):
    """
    Response model for ABC Score for Massive Transfusion
    
    The ABC Score ranges from 0 to 4 points and stratifies patients into:
    - Score 0-1: Low risk for massive transfusion (Standard trauma protocols)
    - Score ≥2: High risk for massive transfusion (Activate MTP immediately)
    
    Performance characteristics from validation studies:
    - Sensitivity: 75% for predicting massive transfusion
    - Specificity: 86% for predicting massive transfusion
    - Negative Predictive Value: 97% (very reliable for ruling out massive transfusion)
    - Positive Predictive Value: 55% (45-50% of high-risk patients may not need MTP)
    
    Reference: Nunez TC, et al. J Trauma. 2009;66(2):346-52.
    """
    
    result: int = Field(
        ...,
        description="ABC Score calculated from four clinical variables (range: 0 to 4 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended actions based on the score",
        example="Patient is likely to require massive transfusion, defined as ≥10 units of packed red blood cells in the first 24 hours of resuscitation. Immediate activation of massive transfusion protocol (MTP) is recommended."
    )
    
    stage: str = Field(
        ...,
        description="Risk category for massive transfusion (Low Risk or High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Likely to require massive transfusion"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "Patient is likely to require massive transfusion, defined as ≥10 units of packed red blood cells in the first 24 hours of resuscitation. Immediate activation of massive transfusion protocol (MTP) is recommended.",
                "stage": "High Risk",
                "stage_description": "Likely to require massive transfusion"
            }
        }