"""
AWOL Score for Delirium Models

Request and response models for AWOL Score calculation.

References (Vancouver style):
1. Douglas VC, Hessler CS, Dhaliwal G, Betjemann JP, Fukuda KA, Alameddine LR, et al. 
   The AWOL tool: derivation and validation of a delirium prediction rule. J Hosp Med. 
   2013 Sep;8(9):493-9. doi: 10.1002/jhm.2062.
2. Douglas VC, Fan VS, Barnes ML, Diaz R, Lawson K, Lim CJ, et al. Predicting inpatient 
   delirium: The AWOL delirium risk-stratification score in clinical practice. Geriatr Nurs. 
   2018 Mar-Apr;39(2):204-209. doi: 10.1016/j.gerinurse.2017.08.006.

The AWOL score is a validated delirium prediction tool that assesses four factors:
Age ≥80 years, inability to spell World backward, disOrientation to place, and 
iLlness severity. It predicts the likelihood of developing delirium during hospitalization,
with scores ≥2 indicating high risk and need for delirium prevention measures.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AwolScoreRequest(BaseModel):
    """
    Request model for AWOL Score for Delirium
    
    The AWOL score uses 4 clinical variables to predict delirium risk:
    
    AWOL Components:
    - A: Age ≥80 years (1 point if yes)
    - W: World - inability to spell backward (1 point if unable)
    - O: Orientation - disoriented to place (1 point if disoriented)
    - L: iLlness severity - moderate or higher (1 point if moderate/severe/moribund)
    
    Score interpretation:
    - 0 points: 2% risk of delirium
    - 1 point: 4% risk of delirium
    - 2 points: 14% risk of delirium
    - 3 points: 20% risk of delirium
    - 4 points: 64% risk of delirium
    
    A score ≥2 indicates high risk for delirium and directs resources for prevention.

    References (Vancouver style):
    1. Douglas VC, Hessler CS, Dhaliwal G, Betjemann JP, Fukuda KA, Alameddine LR, et al. 
       The AWOL tool: derivation and validation of a delirium prediction rule. J Hosp Med. 
       2013 Sep;8(9):493-9. doi: 10.1002/jhm.2062.
    """
    
    age: Literal["under_80", "80_or_over"] = Field(
        ...,
        description="Patient age category. Age <80 years scores 0 points, age ≥80 years scores 1 point",
        example="under_80"
    )
    
    spelling_world_backward: Literal["yes", "no"] = Field(
        ...,
        description="Ability to spell 'WORLD' backward correctly (D-L-R-O-W). If patient can spell it correctly, scores 0 points; if unable, scores 1 point",
        example="yes"
    )
    
    orientation: Literal["yes", "no"] = Field(
        ...,
        description="Oriented to place (city, state, county, hospital name, and floor). If oriented to all, scores 0 points; if disoriented to any, scores 1 point",
        example="yes"
    )
    
    illness_severity: Literal["not_ill", "mildly_ill", "moderately_ill", "severely_ill", "moribund"] = Field(
        ...,
        description="Nursing illness severity assessment. 'Not ill' or 'mildly ill' score 0 points; 'moderately ill', 'severely ill', or 'moribund' score 1 point. Not ill: vital signs stable, physically self-sufficient. Mildly ill: mild symptoms but stable. Moderately ill: acute symptoms, may need assistance. Severely ill: acute/unstable, significant assistance needed. Moribund: death expected within 24-48 hours",
        example="mildly_ill"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": "under_80",
                "spelling_world_backward": "yes",
                "orientation": "yes",
                "illness_severity": "mildly_ill"
            }
        }


class AwolScoreResponse(BaseModel):
    """
    Response model for AWOL Score for Delirium
    
    The AWOL score ranges from 0 to 4 points and stratifies patients into risk categories:
    - Very Low Risk (0 points): 2% delirium risk
    - Low Risk (1 point): 4% delirium risk
    - Moderate Risk (2 points): 14% delirium risk
    - High Risk (3 points): 20% delirium risk
    - Very High Risk (4 points): 64% delirium risk
    
    Scores ≥2 indicate need for delirium prevention protocols including early mobilization,
    reorientation strategies, sleep hygiene, and avoiding deliriogenic medications.
    
    Reference: Douglas VC, et al. J Hosp Med. 2013;8(9):493-9.
    """
    
    result: int = Field(
        ...,
        description="AWOL score calculated from 4 clinical variables (range: 0-4 points)",
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with delirium risk percentage and recommended actions",
        example="4% risk of delirium during hospitalization. Low risk patient - routine monitoring appropriate."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Very Low Risk, Low Risk, Moderate Risk, High Risk, Very High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the score value",
        example="1 point"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "4% risk of delirium during hospitalization. Low risk patient - routine monitoring appropriate.",
                "stage": "Low Risk",
                "stage_description": "1 point"
            }
        }