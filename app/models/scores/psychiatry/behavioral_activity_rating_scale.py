"""
Behavioral Activity Rating Scale (BARS) Models

Request and response models for BARS calculation.

References (Vancouver style):
1. Swift RH, Harrigan EP, Cappelleri JC, Kramer D, Chandler LP. Validation of the 
   behavioural activity rating scale (BARS): a novel measure of activity in agitated 
   patients. J Psychiatr Res. 2002 Mar-Apr;36(2):87-95.
2. Lindenmayer JP, Bossie CA, Kujawa M, Zhu Y, Canuso CM. Dimensions of agitation 
   in schizophrenia: results from the CATIE study. Schizophr Res. 2009 Feb;107(2-3):225-30.
3. Price LM, Forbat L, Chew-Graham C, Palen L, Robinson D, McGoldrick M, et al. 
   Learning and performance outcomes of mental health first aid training: a systematic 
   review of randomized controlled trials. Acad Med. 2018 Sep;93(9):1404-13.

The Behavioral Activity Rating Scale (BARS) is a 7-point observational scale used to 
assess behavioral activity and agitation in patients in emergency care and psychiatric 
settings. It does not require patient participation and can be used reliably by healthcare 
staff with minimal training.
"""

from pydantic import BaseModel, Field
from typing import Literal


class BehavioralActivityRatingScaleRequest(BaseModel):
    """
    Request model for Behavioral Activity Rating Scale (BARS)
    
    The BARS is a 7-point observational scale used to assess behavioral activity and 
    agitation in patients. It is particularly useful in emergency department and 
    psychiatric settings where rapid assessment of agitation is needed.
    
    Scale Points:
    1. Difficult or unable to arouse - May indicate oversedation or medical emergency
    2. Asleep but responds normally to verbal or physical contact - Sedated but responsive
    3. Drowsy, appears sedated - Sedated with impaired alertness
    4. Quiet and awake (normal level of activity) - Therapeutic target, normal behavior
    5. Signs of over activity; calms down with instructions - Mild agitation, responsive to redirection
    6. Extremely or continuously active; does not require restraint - Moderate agitation
    7. Violent behavior requiring restraint - Severe agitation requiring immediate intervention
    
    Clinical Threshold:
    - Scores >4 typically warrant clinical evaluation and possible intervention
    - Score 7 requires immediate emergency intervention and safety measures
    
    Key Features:
    - Observational tool requiring no patient participation
    - Excellent inter-rater and intra-rater reliability
    - Can be used by nurses, physicians, and other healthcare staff
    - Originally developed for pharmaceutical studies but widely used clinically
    
    References (Vancouver style):
    1. Swift RH, Harrigan EP, Cappelleri JC, Kramer D, Chandler LP. Validation of the 
    behavioural activity rating scale (BARS): a novel measure of activity in agitated 
    patients. J Psychiatr Res. 2002 Mar-Apr;36(2):87-95.
    2. Lindenmayer JP, Bossie CA, Kujawa M, Zhu Y, Canuso CM. Dimensions of agitation 
    in schizophrenia: results from the CATIE study. Schizophr Res. 2009 Feb;107(2-3):225-30.
    3. Price LM, Forbat L, Chew-Graham C, Palen L, Robinson D, McGoldrick M, et al. 
    Learning and performance outcomes of mental health first aid training: a systematic 
    review of randomized controlled trials. Acad Med. 2018 Sep;93(9):1404-13.
    """
    
    activity_level: Literal[1, 2, 3, 4, 5, 6, 7] = Field(
        ...,
        description="Patient's current level of behavioral activity observed by clinician on a 7-point scale. 1=Difficult to arouse, 2=Asleep but responds normally, 3=Drowsy/sedated, 4=Quiet and awake (normal), 5=Overactive but responds to instructions, 6=Extremely active without restraint needs, 7=Violent behavior requiring restraint",
        example=4
    )
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "title": "Normal activity level (BARS = 4)",
                    "value": {
                        "activity_level": 4
                    }
                },
                {
                    "title": "Mild agitation requiring assessment (BARS = 5)",
                    "value": {
                        "activity_level": 5
                    }
                },
                {
                    "title": "Severe agitation requiring immediate intervention (BARS = 7)",
                    "value": {
                        "activity_level": 7
                    }
                }
            ]
        }


class BehavioralActivityRatingScaleResponse(BaseModel):
    """
    Response model for Behavioral Activity Rating Scale (BARS)
    
    Returns the BARS score with detailed interpretation including:
    - Classification of agitation level (Hypoactive, Sedated, Normal, Mild/Moderate/Severe Agitation)
    - Clinical significance and risk assessment
    - Specific management recommendations based on the score
    - Safety considerations and intervention requirements
    
    The BARS provides a standardized approach to assess and monitor agitated patients,
    helping healthcare providers make rapid decisions about appropriate interventions
    and safety measures in emergency and psychiatric settings.
    
    Clinical Interpretation:
    - Scores 1-3: Range from hypoactive to sedated states
    - Score 4: Normal, therapeutic target level
    - Scores 5-7: Increasing levels of agitation requiring intervention
    
    Reference: The BARS has demonstrated excellent psychometric properties with virtually 
    perfect inter- and intra-rater reliability in validation studies.
    """
    
    result: int = Field(
        ...,
        description="BARS score on 7-point scale (1=difficult to arouse, 7=violent behavior requiring restraint)",
        ge=1,
        le=7,
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the BARS score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation including agitation level, clinical significance, and specific management recommendations",
        example="BARS score: 4/7 - Quiet and awake (normal level of activity). Patient demonstrates normal, calm behavior with appropriate activity level. This is the therapeutic target for most patients in emergency psychiatric settings. Clinical management: Continue current management approach and monitor for changes. Maintain therapeutic environment. This score indicates successful de-escalation or appropriate medication response. No immediate intervention required, but continue routine monitoring."
    )
    
    stage: str = Field(
        ...,
        description="Agitation category (Hypoactive, Sedated, Normal, Mild Agitation, Moderate Agitation, Severe Agitation)",
        example="Normal"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the behavioral activity level",
        example="Quiet and awake with normal activity level"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "BARS score: 4/7 - Quiet and awake (normal level of activity). Patient demonstrates normal, calm behavior with appropriate activity level. This is the therapeutic target for most patients in emergency psychiatric settings. Clinical management: Continue current management approach and monitor for changes. Maintain therapeutic environment. This score indicates successful de-escalation or appropriate medication response. No immediate intervention required, but continue routine monitoring.",
                "stage": "Normal",
                "stage_description": "Quiet and awake with normal activity level"
            }
        }