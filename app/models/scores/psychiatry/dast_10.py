"""
Drug Abuse Screening Test-10 (DAST-10) Models

Request and response models for DAST-10 calculation.

References (Vancouver style):
1. Skinner HA. The drug abuse screening test. Addict Behav. 1982;7(4):363-71. 
   doi: 10.1016/0306-4603(82)90006-8.
2. Yudko E, Lozhkina O, Fouts AA. A comprehensive review of the psychometric properties 
   of the Drug Abuse Screening Test. J Subst Abuse Treat. 2007;32(2):189-98. 
   doi: 10.1016/j.jsat.2006.08.002.
3. Cocco KM, Carey KB. Psychometric properties of the drug abuse screening test in 
   psychiatric outpatients. Psychol Assess. 1998;10(4):408-14. 
   doi: 10.1037/1040-3590.10.4.408.

The DAST-10 is a brief, 10-item assessment tool designed to measure, evaluate, and 
identify drug use problems, excluding alcohol or tobacco. It assesses drug use in the 
past 12 months and provides a quantitative index of the degree of consequences related 
to drug abuse. The tool has demonstrated good internal consistency (α = 0.81–0.84) 
and is widely used in clinical settings for rapid assessment of drug-related problems.
"""

from pydantic import BaseModel, Field
from typing import Literal


class Dast10Request(BaseModel):
    """
    Request model for Drug Abuse Screening Test-10 (DAST-10)
    
    The DAST-10 consists of 10 yes/no questions about drug use patterns and consequences
    in the past 12 months, excluding alcohol and tobacco:
    
    Scoring:
    - Questions 1, 2, 4-10: 1 point for each "yes" answer
    - Question 3: 1 point for "no" answer (reverse scored)
    - Total score range: 0-10 points
    
    Interpretation:
    - 0: No problems reported
    - 1-2: Low level problems (monitoring recommended)
    - 3-5: Moderate level problems (further investigation needed)
    - 6-8: Substantial problems (intensive assessment and treatment required)
    - 9-10: Severe problems (immediate specialized treatment warranted)
    
    Note: A score of ≥3 is generally considered indicative of problematic substance use.
    The optimal cutoff score is 7 for diagnostic purposes.

    References (Vancouver style):
    1. Skinner HA. The drug abuse screening test. Addict Behav. 1982;7(4):363-71. 
       doi: 10.1016/0306-4603(82)90006-8.
    2. Yudko E, Lozhkina O, Fouts AA. A comprehensive review of the psychometric properties 
       of the Drug Abuse Screening Test. J Subst Abuse Treat. 2007;32(2):189-98. 
       doi: 10.1016/j.jsat.2006.08.002.
    3. Cocco KM, Carey KB. Psychometric properties of the drug abuse screening test in 
       psychiatric outpatients. Psychol Assess. 1998;10(4):408-14. 
       doi: 10.1037/1040-3590.10.4.408.
    """
    
    used_drugs_other_than_medical: Literal["yes", "no"] = Field(
        ...,
        description="Have you used drugs other than those required for medical reasons? (1 point for 'yes')",
        example="no"
    )
    
    abuse_prescription_drugs: Literal["yes", "no"] = Field(
        ...,
        description="Do you abuse more than one drug at a time? (1 point for 'yes')",
        example="no"
    )
    
    always_able_to_stop: Literal["yes", "no"] = Field(
        ...,
        description="Are you always able to stop using drugs when you want to? (REVERSE SCORED: 1 point for 'no')",
        example="yes"
    )
    
    blackouts_flashbacks: Literal["yes", "no"] = Field(
        ...,
        description="Have you had 'blackouts' or 'flashbacks' as a result of drug use? (1 point for 'yes')",
        example="no"
    )
    
    feel_bad_guilty: Literal["yes", "no"] = Field(
        ...,
        description="Do you ever feel bad or guilty about your drug use? (1 point for 'yes')",
        example="no"
    )
    
    spouse_parents_complain: Literal["yes", "no"] = Field(
        ...,
        description="Does your spouse (or parents) ever complain about your involvement with drugs? (1 point for 'yes')",
        example="no"
    )
    
    neglected_family_work: Literal["yes", "no"] = Field(
        ...,
        description="Have you neglected your family because of your use of drugs? (1 point for 'yes')",
        example="no"
    )
    
    engaged_illegal_activities: Literal["yes", "no"] = Field(
        ...,
        description="Have you engaged in illegal activities in order to obtain drugs? (1 point for 'yes')",
        example="no"
    )
    
    withdrawal_symptoms: Literal["yes", "no"] = Field(
        ...,
        description="Have you ever experienced withdrawal symptoms (felt sick) when you stopped taking drugs? (1 point for 'yes')",
        example="no"
    )
    
    medical_problems: Literal["yes", "no"] = Field(
        ...,
        description="Have you had medical problems as a result of your drug use (e.g., memory loss, hepatitis, convulsions, bleeding, etc.)? (1 point for 'yes')",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "used_drugs_other_than_medical": "no",
                "abuse_prescription_drugs": "no",
                "always_able_to_stop": "yes",
                "blackouts_flashbacks": "no",
                "feel_bad_guilty": "no",
                "spouse_parents_complain": "no",
                "neglected_family_work": "no",
                "engaged_illegal_activities": "no",
                "withdrawal_symptoms": "no",
                "medical_problems": "no"
            }
        }


class Dast10Response(BaseModel):
    """
    Response model for Drug Abuse Screening Test-10 (DAST-10)
    
    The DAST-10 score ranges from 0 to 10 points and indicates:
    - 0: No problems reported - Continue routine screening
    - 1-2: Low level problems - Monitoring and re-assessment recommended
    - 3-5: Moderate level problems - Further investigation with additional resources needed
    - 6-8: Substantial problems - Intensive assessment and treatment required
    - 9-10: Severe problems - Immediate specialized addiction treatment warranted
    
    A score of ≥3 is generally considered indicative of problematic substance use.
    Clinical judgment should be used to interpret scores considering demographic 
    and contextual factors.
    
    Reference: Skinner HA. Addict Behav. 1982;7(4):363-71.
    """
    
    result: int = Field(
        ...,
        description="DAST-10 total score calculated from responses (range: 0-10 points)",
        example=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended actions based on the DAST-10 score",
        example="No evidence of drug-related problems. Continue routine screening at appropriate intervals."
    )
    
    stage: str = Field(
        ...,
        description="Risk level category (No Problems, Low Level, Moderate Level, Substantial Level, or Severe Level)",
        example="No Problems"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level category",
        example="No drug problems reported"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "No evidence of drug-related problems. Continue routine screening at appropriate intervals.",
                "stage": "No Problems",
                "stage_description": "No drug problems reported"
            }
        }