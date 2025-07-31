"""
Newsom Score for Non-traumatic Chest Pain Models

Request and response models for Newsom Score calculation.

References (Vancouver style):
1. Rothrock SG, Green SM, Costanzo KA, Fanelli JM, Cruzen ES, Pagane JR. High yield 
   criteria for obtaining non-trauma chest radiography in the adult emergency department 
   population. J Emerg Med. 2002 Aug;23(2):117-24. doi: 10.1016/s0736-4679(02)00496-1.
2. Newsom C, Jeanmonod R, Woolley W, Muir M, Jeanmonod D. Prospective Validation and 
   Refinement of a Decision Rule to Obtain Chest X-ray in Patients With Nontraumatic 
   Chest Pain in the Emergency Department. Acad Emerg Med. 2018 Jun;25(6):650-656. 
   doi: 10.1111/acem.13380.

The Newsom Score is a clinical decision rule that uses 12 criteria to determine which 
patients with non-traumatic chest pain require chest radiography. With a sensitivity of 
92.9% and negative predictive value of 98.4%, it can safely reduce chest x-ray 
utilization by approximately 28.9% in the emergency department setting.
"""

from pydantic import BaseModel, Field
from typing import Literal


class NewsomScoreRequest(BaseModel):
    """
    Request model for Newsom Score for Non-traumatic Chest Pain
    
    The Newsom Score evaluates 12 clinical criteria to identify low-risk patients 
    who do not require chest radiography:
    
    1. Age ≥60 years
    2. History of congestive heart failure (CHF)
    3. Smoking history (current or former)
    4. Hemoptysis
    5. History of tuberculosis
    6. History of thromboembolic disease (PE/DVT)
    7. Prior or current alcohol abuse
    8. Fever ≥100.4°F (38°C)
    9. Oxygen saturation <90%
    10. Respiratory rate >24 breaths/minute
    11. Diminished breath sounds
    12. Rales on auscultation
    
    Each positive criterion scores 1 point. A total score of 0 indicates low risk 
    where chest x-ray is not needed.
    
    References (Vancouver style):
    1. Rothrock SG, Green SM, Costanzo KA, Fanelli JM, Cruzen ES, Pagane JR. High yield 
    criteria for obtaining non-trauma chest radiography in the adult emergency department 
    population. J Emerg Med. 2002 Aug;23(2):117-24. doi: 10.1016/s0736-4679(02)00496-1.
    2. Newsom C, Jeanmonod R, Woolley W, Muir M, Jeanmonod D. Prospective Validation and 
    Refinement of a Decision Rule to Obtain Chest X-ray in Patients With Nontraumatic 
    Chest Pain in the Emergency Department. Acad Emerg Med. 2018 Jun;25(6):650-656. 
    doi: 10.1111/acem.13380.
    """
    
    age_60_or_more: Literal["yes", "no"] = Field(
        ...,
        description="Is the patient 60 years old or older? Scores 1 point if yes",
        example="no"
    )
    
    chf_history: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have a history of congestive heart failure (CHF)? Scores 1 point if yes",
        example="no"
    )
    
    smoking_history: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have a smoking history (current or former)? Scores 1 point if yes",
        example="no"
    )
    
    hemoptysis: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have hemoptysis (coughing up blood)? Scores 1 point if yes",
        example="no"
    )
    
    tuberculosis_history: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have a history of tuberculosis? Scores 1 point if yes",
        example="no"
    )
    
    thromboembolic_history: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have a history of thromboembolic disease (pulmonary embolism or deep vein thrombosis)? Scores 1 point if yes",
        example="no"
    )
    
    alcohol_abuse: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have prior or current alcohol abuse? Scores 1 point if yes",
        example="no"
    )
    
    fever: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have fever ≥100.4°F (38°C)? Scores 1 point if yes",
        example="no"
    )
    
    oxygen_saturation_low: Literal["yes", "no"] = Field(
        ...,
        description="Is the patient's oxygen saturation <90% on room air? Scores 1 point if yes",
        example="no"
    )
    
    respiratory_rate_high: Literal["yes", "no"] = Field(
        ...,
        description="Is the patient's respiratory rate >24 breaths per minute? Scores 1 point if yes",
        example="no"
    )
    
    diminished_breath_sounds: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have diminished breath sounds on physical examination? Scores 1 point if yes",
        example="no"
    )
    
    rales: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have rales (crackles) on lung auscultation? Scores 1 point if yes",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age_60_or_more": "no",
                "chf_history": "no",
                "smoking_history": "no",
                "hemoptysis": "no",
                "tuberculosis_history": "no",
                "thromboembolic_history": "no",
                "alcohol_abuse": "no",
                "fever": "no",
                "oxygen_saturation_low": "no",
                "respiratory_rate_high": "no",
                "diminished_breath_sounds": "no",
                "rales": "no"
            }
        }


class NewsomScoreResponse(BaseModel):
    """
    Response model for Newsom Score for Non-traumatic Chest Pain
    
    The Newsom Score ranges from 0 to 12 points:
    - 0 points: Low risk - Chest x-ray not needed (NPV 98.4%)
    - ≥1 point: Not low risk - Consider chest x-ray (Sensitivity 92.9%)
    
    Application of this rule could reduce chest x-ray utilization by approximately 28.9%.
    
    Reference: Newsom C, et al. Acad Emerg Med. 2018;25(6):650-656.
    """
    
    result: int = Field(
        ...,
        description="Newsom Score calculated from clinical criteria (range: 0-12 points)",
        example=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommendation based on the score",
        example="This patient has no risk factors present and is considered low risk. Chest x-ray is not needed based on the Newsom Score criteria. The negative predictive value is 98.4%, making it highly unlikely that a clinically significant finding would be missed."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low risk or Not low risk)",
        example="Low risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the recommendation",
        example="Chest x-ray not needed"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "This patient has no risk factors present and is considered low risk. Chest x-ray is not needed based on the Newsom Score criteria. The negative predictive value is 98.4%, making it highly unlikely that a clinically significant finding would be missed.",
                "stage": "Low risk",
                "stage_description": "Chest x-ray not needed"
            }
        }