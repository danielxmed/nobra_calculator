"""
DIRE Score for Opioid Treatment Models

Request and response models for DIRE Score calculation.

References (Vancouver style):
1. Belgrade MJ, Schamber CD, Lindgren BR. The DIRE score: predicting outcomes of 
   opioid prescribing for chronic pain. J Pain. 2006 Sep;7(9):671-81. 
   doi: 10.1016/j.jpain.2006.03.001.
2. Chou R, Fanciullo GJ, Fine PG, Adler JA, Ballantyne JC, Davies P, et al. Clinical 
   guidelines for the use of chronic opioid therapy in chronic noncancer pain. J Pain. 
   2009 Feb;10(2):113-30. doi: 10.1016/j.jpain.2008.10.008.
3. Jamison RN, Serraillier J, Michna E. Assessment and treatment of abuse risk in 
   opioid prescribing for chronic pain. Pain Res Treat. 2011;2011:941808. 
   doi: 10.1155/2011/941808.

The DIRE score (Diagnosis, Intractability, Risk, and Efficacy) is a clinical tool 
designed to predict patient compliance with long-term opioid therapy for chronic 
non-cancer pain. It evaluates six domains: diagnosis severity, treatment intractability, 
psychological risk, chemical health risk, reliability risk, and social support risk. 
Each domain is scored 1-3 (unfavorable to favorable), with total scores ranging from 
7-21. Scores ≤13 suggest the patient is not a suitable candidate for long-term opioid 
therapy, while scores ≥14 indicate a good candidate.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class DireScoreRequest(BaseModel):
    """
    Request model for DIRE Score for Opioid Treatment
    
    The DIRE score evaluates 6 domains to predict opioid treatment compliance:
    
    1. Diagnosis (D):
       - Score 1: Benign chronic condition, minimal objective findings, or no definite diagnosis
       - Score 2: Slowly progressive condition concordant with moderate pain or fixed condition with moderate objective findings
       - Score 3: Advanced condition concordant with severe pain with objective findings
    
    2. Intractability (I):
       - Score 1: Few therapies tried; patient takes a passive role in pain management process
       - Score 2: Most customary treatments tried but patient not fully engaged or barriers prevent
       - Score 3: Patient fully engaged in appropriate treatments but with inadequate response
    
    3. Psychological Risk (R):
       - Score 1: Serious personality dysfunction or mental illness interfering with care
       - Score 2: Personality or mental health interferes moderately
       - Score 3: Good communication with clinic, no significant personality dysfunction
    
    4. Chemical Health Risk (R):
       - Score 1: Active or very recent use of illicit drugs, excessive alcohol, or prescription drug abuse
       - Score 2: Chemical coper or history of chemical dependence in remission
       - Score 3: No CD history, not drug-focused or chemically reliant
    
    5. Reliability Risk (R):
       - Score 1: History of numerous problems (medication misuse, missed appointments)
       - Score 2: Occasional difficulties with compliance but generally reliable
       - Score 3: Highly reliable patient with meds, appointments, and treatment
    
    6. Social Support Risk (E for Efficacy):
       - Score 1: Life in chaos, little family support, few close relationships
       - Score 2: Reduction in some relationships and life roles
       - Score 3: Supportive family/close relationships, involved in work or school

    References (Vancouver style):
    1. Belgrade MJ, Schamber CD, Lindgren BR. The DIRE score: predicting outcomes of 
       opioid prescribing for chronic pain. J Pain. 2006 Sep;7(9):671-81. 
       doi: 10.1016/j.jpain.2006.03.001.
    2. Chou R, Fanciullo GJ, Fine PG, Adler JA, Ballantyne JC, Davies P, et al. Clinical 
       guidelines for the use of chronic opioid therapy in chronic noncancer pain. J Pain. 
       2009 Feb;10(2):113-30. doi: 10.1016/j.jpain.2008.10.008.
    """
    
    diagnosis: Literal[1, 2, 3] = Field(
        ...,
        description="Diagnosis severity and objective findings. Score 1: Benign/minimal findings, Score 2: Moderate concordant findings, Score 3: Advanced condition with severe pain and objective findings",
        example=2
    )
    
    intractability: Literal[1, 2, 3] = Field(
        ...,
        description="Treatment response and patient engagement. Score 1: Few therapies/passive role, Score 2: Most treatments tried/moderate engagement, Score 3: Fully engaged but inadequate response",
        example=3
    )
    
    psychological_risk: Literal[1, 2, 3] = Field(
        ...,
        description="Psychological factors affecting care. Score 1: Serious dysfunction interfering with care, Score 2: Moderate interference, Score 3: Good communication/no significant dysfunction",
        example=3
    )
    
    chemical_health_risk: Literal[1, 2, 3] = Field(
        ...,
        description="Substance use history and risk. Score 1: Active use/recent abuse, Score 2: Chemical coper/history in remission, Score 3: No history/not drug-focused",
        example=3
    )
    
    reliability_risk: Literal[1, 2, 3] = Field(
        ...,
        description="Compliance with treatment plan. Score 1: Numerous problems/misuse history, Score 2: Occasional difficulties/generally reliable, Score 3: Highly reliable with all aspects",
        example=3
    )
    
    social_support_risk: Literal[1, 2, 3] = Field(
        ...,
        description="Social support and life stability. Score 1: Life chaos/little support, Score 2: Some reduction in relationships/roles, Score 3: Good support/involved in work or school",
        example=2
    )
    
    @field_validator('diagnosis', 'intractability', 'psychological_risk', 'chemical_health_risk', 'reliability_risk', 'social_support_risk')
    def validate_scores(cls, v):
        if v not in [1, 2, 3]:
            raise ValueError("All DIRE score parameters must be 1, 2, or 3")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "diagnosis": 2,
                "intractability": 3,
                "psychological_risk": 3,
                "chemical_health_risk": 3,
                "reliability_risk": 3,
                "social_support_risk": 2
            }
        }


class DireScoreResponse(BaseModel):
    """
    Response model for DIRE Score for Opioid Treatment
    
    The DIRE score ranges from 7-21 points and classifies patients into:
    - Not suitable (7-13 points): Not a suitable candidate for long-term opioid therapy
    - Good candidate (14-21 points): Good candidate for long-term opioid therapy
    
    Note: This tool has not been prospectively validated externally and should be 
    used alongside clinical judgment and other risk assessment tools.
    
    Reference: Belgrade MJ, et al. J Pain. 2006;7(9):671-81.
    """
    
    result: int = Field(
        ...,
        description="DIRE score calculated from 6 domains (range: 7-21 points)",
        example=16
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommendations based on the score",
        example="Good candidate for long-term opioid analgesia. May proceed with opioid therapy with appropriate monitoring, treatment agreement, and regular follow-up."
    )
    
    stage: str = Field(
        ...,
        description="Suitability category (Not suitable or Good candidate)",
        example="Good candidate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the suitability category",
        example="Good candidate"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 16,
                "unit": "points",
                "interpretation": "Good candidate for long-term opioid analgesia. May proceed with opioid therapy with appropriate monitoring, treatment agreement, and regular follow-up.",
                "stage": "Good candidate",
                "stage_description": "Good candidate"
            }
        }
