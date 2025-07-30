"""
Columbia Suicide Severity Rating Scale (C-SSRS) Screener Models

Request and response models for C-SSRS calculation.

References (Vancouver style):
1. Posner K, Brown GK, Stanley B, Brent DA, Yershova KV, Oquendo MA, et al. The 
   Columbia-Suicide Severity Rating Scale: initial validity and internal consistency 
   findings from three multisite studies with adolescents and adults. Am J Psychiatry. 
   2011 Dec;168(12):1266-77. doi: 10.1176/appi.ajp.2011.10111704.
2. Bjureberg J, Dahlin M, Carlborg A, Edberg H, Haglund A, Runeson B. Columbia-Suicide 
   Severity Rating Scale Screen Version: initial screening for suicide risk in a 
   psychiatric emergency department. Psychol Med. 2022 Dec;52(16):3904-3912. 
   doi: 10.1017/S0033291721000751.
3. Madan A, Frueh BC, Allen JG, Ellis TE, Rufino KA, Oldham JM, et al. Psychometric 
   Reevaluation of the Columbia-Suicide Severity Rating Scale: Findings From a 
   Prospective, Inpatient Cohort of Severely Mentally Ill Adults. J Clin Psychiatry. 
   2016 Jul;77(7):e867-73. doi: 10.4088/JCP.15m10069.

The C-SSRS Screener is a brief, evidence-based tool for suicide risk assessment that 
evaluates both suicidal ideation severity and behavior to stratify risk levels.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Dict, Any


class CSSRSRequest(BaseModel):
    """
    Request model for Columbia Suicide Severity Rating Scale (C-SSRS) Screener
    
    The C-SSRS evaluates two main domains:
    
    1. Severity of Suicidal Ideation (Past Month):
       - Ranges from 0 (no ideation) to 5 (active ideation with plan and intent)
       - Higher scores indicate more severe ideation
    
    2. Suicidal Behavior (Lifetime):
       - Ranges from 0 (no behavior) to 5 (completed suicide)
       - Includes preparatory acts, interrupted/aborted attempts, and actual attempts
       - Timing of behavior is critical for risk stratification
    
    Risk levels are determined by combining ideation severity and behavior recency:
    - High Risk: Ideation 4-5 OR behavior within past 3 months
    - Moderate Risk: Ideation 3 OR lifetime behavior >3 months ago
    - Low Risk: Ideation 0-2 with no recent behavior
    
    Note: The C-SSRS Screener can be administered by non-mental health professionals
    but should not replace comprehensive clinical evaluation.
    
    References (Vancouver style):
    1. Posner K, Brown GK, Stanley B, Brent DA, Yershova KV, Oquendo MA, et al. The 
       Columbia-Suicide Severity Rating Scale: initial validity and internal consistency 
       findings from three multisite studies with adolescents and adults. Am J Psychiatry. 
       2011 Dec;168(12):1266-77.
    """
    
    ideation_level: int = Field(
        ...,
        ge=0,
        le=5,
        description="Severity of suicidal ideation in the past month. 0=No ideation, 1=Wish to be dead, 2=Nonspecific active thoughts, 3=Methods without intent, 4=Some intent to act, 5=Specific plan and intent",
        example=2
    )
    
    behavior_level: int = Field(
        ...,
        ge=0,
        le=5,
        description="Most severe lifetime suicidal behavior. 0=No behavior, 1=Preparatory acts, 2=Aborted attempt, 3=Interrupted attempt, 4=Actual attempt, 5=Completed suicide",
        example=0
    )
    
    behavior_recent: Literal["Never", "More than 3 months ago", "Within past 3 months"] = Field(
        ...,
        description="Timing of most recent suicidal behavior. Critical for risk stratification as behavior within 3 months indicates high risk",
        example="Never"
    )
    
    @validator('behavior_recent')
    def validate_behavior_consistency(cls, v, values):
        """Ensure behavior timing is consistent with behavior level"""
        if 'behavior_level' in values:
            if values['behavior_level'] == 0 and v != "Never":
                raise ValueError("If no suicidal behavior reported (level 0), timing must be 'Never'")
            if values['behavior_level'] > 0 and v == "Never":
                raise ValueError("If suicidal behavior reported (level >0), timing cannot be 'Never'")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "ideation_level": 3,
                "behavior_level": 1,
                "behavior_recent": "More than 3 months ago"
            }
        }


class CSSRSResponse(BaseModel):
    """
    Response model for Columbia Suicide Severity Rating Scale (C-SSRS) Screener
    
    The C-SSRS stratifies patients into three risk categories:
    
    - Low Risk: Requires standard care with possible outpatient referral
    - Moderate Risk: Requires behavioral health consultation and safety planning
    - High Risk: Requires immediate intervention and possible hospitalization
    
    Management recommendations are evidence-based and aligned with standard
    psychiatric emergency protocols.
    
    Reference: Bjureberg J, et al. Psychol Med. 2022;52(16):3904-3912.
    """
    
    result: Literal["Low Risk", "Moderate Risk", "High Risk"] = Field(
        ...,
        description="Suicide risk stratification level based on ideation severity and behavior recency",
        example="Moderate Risk"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (category for risk stratification)",
        example="category"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with specific management recommendations",
        example="Moderate risk for suicide. Recommend behavioral health consultation and implementation of patient safety precautions. Develop safety plan before discharge."
    )
    
    stage: str = Field(
        ...,
        description="Risk level category",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="Moderate suicide risk"
    )
    
    assessment_details: Dict[str, Any] = Field(
        ...,
        description="Detailed breakdown of ideation and behavior assessments",
        example={
            "ideation": {
                "level": 3,
                "description": "Active suicidal ideation with methods (no intent)"
            },
            "behavior": {
                "level": 1,
                "description": "Preparatory acts or behavior",
                "timing": "More than 3 months ago"
            }
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Moderate Risk",
                "unit": "category",
                "interpretation": "Moderate risk for suicide. Recommend behavioral health consultation and implementation of patient safety precautions. Develop safety plan before discharge.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate suicide risk",
                "assessment_details": {
                    "ideation": {
                        "level": 3,
                        "description": "Active suicidal ideation with methods (no intent)"
                    },
                    "behavior": {
                        "level": 1,
                        "description": "Preparatory acts or behavior",
                        "timing": "More than 3 months ago"
                    }
                }
            }
        }