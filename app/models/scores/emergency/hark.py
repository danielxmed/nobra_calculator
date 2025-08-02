"""
HARK (Humiliation, Afraid, Rape, Kick) Models

Request and response models for HARK intimate partner violence screening.

References (Vancouver style):
1. Sohal H, Eldridge S, Feder G. The sensitivity and specificity of four questions (HARK) 
   to identify intimate partner violence: a diagnostic accuracy study in general practice. 
   BMC Fam Pract. 2007 Oct 15;8:49. doi: 10.1186/1471-2296-8-49.
2. Cronholm PF, Fogarty CT, Ambuel B, Harrison SL. Intimate partner violence. Am Fam 
   Physician. 2011 Oct 15;84(8):945-52. PMID: 22010770.
3. US Preventive Services Task Force. Screening for Intimate Partner Violence, Elder Abuse, 
   and Abuse of Vulnerable Adults: US Preventive Services Task Force Recommendation Statement. 
   JAMA. 2018 Oct 23;320(16):1678-1687. doi: 10.1001/jama.2018.14741.

The HARK screening tool consists of four questions (Humiliation, Afraid, Rape, Kick) 
designed to detect intimate partner violence in adult women. Each question addresses 
a different type of abuse: emotional/psychological, intimidation, sexual violence, 
and physical violence. A score of ≥1 indicates a positive screen requiring immediate 
safety assessment and appropriate intervention.
"""

from pydantic import BaseModel, Field
from typing import Literal, List


class HarkRequest(BaseModel):
    """
    Request model for HARK (Humiliation, Afraid, Rape, Kick) screening
    
    The HARK tool uses 4 questions to screen for intimate partner violence in the past year:
    
    H - Humiliation: Emotional/psychological abuse including verbal abuse, threats, 
        isolation, controlling behavior, or other forms of psychological harm
    
    A - Afraid: Fear-based intimidation including threats of violence, weapons, 
        stalking, or creating an atmosphere of fear and control
    
    R - Rape: Sexual violence including forced sexual activity, sexual coercion, 
        or any non-consensual sexual contact
    
    K - Kick: Physical violence including hitting, slapping, kicking, pushing, 
        choking, or any form of physical harm
    
    Important Clinical Notes:
    - Validated only in English and for adult women in heterosexual relationships
    - Should be administered privately without partner/family present
    - All questions refer to IPV by current or former partner in the past year
    - Positive screen (≥1) requires immediate safety assessment and intervention
    
    References (Vancouver style):
    1. Sohal H, Eldridge S, Feder G. The sensitivity and specificity of four questions (HARK) 
       to identify intimate partner violence: a diagnostic accuracy study in general practice. 
       BMC Fam Pract. 2007 Oct 15;8:49. doi: 10.1186/1471-2296-8-49.
    2. US Preventive Services Task Force. Screening for Intimate Partner Violence, Elder Abuse, 
       and Abuse of Vulnerable Adults: US Preventive Services Task Force Recommendation Statement. 
       JAMA. 2018 Oct 23;320(16):1678-1687. doi: 10.1001/jama.2018.14741.
    """
    
    humiliation: Literal["yes", "no"] = Field(
        ...,
        description="Within the last year, have you been humiliated or emotionally abused "
                   "in other ways by your partner or ex-partner? This includes verbal abuse, "
                   "threats, isolation, controlling behavior, or psychological harm.",
        example="no"
    )
    
    afraid: Literal["yes", "no"] = Field(
        ...,
        description="Within the last year, have you been afraid of your partner or ex-partner? "
                   "This includes fear due to threats, intimidation, weapons, stalking, or "
                   "creating an atmosphere of fear and control.",
        example="no"
    )
    
    rape: Literal["yes", "no"] = Field(
        ...,
        description="Within the last year, have you been raped or forced to have any kind "
                   "of sexual activity by your partner or ex-partner? This includes any "
                   "non-consensual sexual contact or sexual coercion.",
        example="no"
    )
    
    kick: Literal["yes", "no"] = Field(
        ...,
        description="Within the last year, have you been kicked, hit, slapped or otherwise "
                   "physically hurt by your partner or ex-partner? This includes any form "
                   "of physical violence such as pushing, choking, or physical harm.",
        example="no"  
    )
    
    class Config:
        schema_extra = {
            "example": {
                "humiliation": "no",
                "afraid": "no", 
                "rape": "no",
                "kick": "no"
            }
        }


class HarkResponse(BaseModel):
    """
    Response model for HARK (Humiliation, Afraid, Rape, Kick) screening
    
    The HARK score ranges from 0-4 points with simple interpretation:
    
    - Score 0: Negative screen for intimate partner violence
    - Score ≥1: Positive screen requiring immediate safety assessment
    
    A positive screen indicates disclosure of at least one form of IPV in the past year 
    and triggers the need for safety planning, resource provision, and follow-up care 
    according to institutional protocols and local reporting requirements.
    
    Reference: Sohal H, et al. BMC Fam Pract. 2007;8:49.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=4,
        description="HARK score calculated as sum of 'yes' responses to 4 questions (range: 0-4 points)",
        example=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )  
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with screening result and recommended actions "
                   "based on score (negative vs positive screen)",
        example="Negative screen for intimate partner violence. No indication of IPV based "
                "on current screening. Continue to provide supportive care and maintain "
                "awareness for signs of abuse."
    )
    
    stage: str = Field(
        ...,
        description="Screening result category (Negative Screen or Positive Screen)",
        example="Negative Screen"
    )
    
    stage_description: str = Field(
        ...,
        description="Score range description for the screening result",
        example="Score 0"
    )
    
    abuse_types_identified: List[str] = Field(
        ...,
        description="List of specific types of abuse identified based on positive responses. "
                   "May include: Emotional/Psychological Abuse, Intimidation/Fear, "
                   "Sexual Violence, Physical Violence",
        example=[]
    )
    
    requires_safety_assessment: bool = Field(
        ...,  
        description="Boolean indicating whether immediate safety assessment is required "
                   "(true for any positive response, false for all negative responses)",
        example=False
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "Negative screen for intimate partner violence. No indication "
                                "of IPV based on current screening. Continue to provide supportive "
                                "care and maintain awareness for signs of abuse.",
                "stage": "Negative Screen",
                "stage_description": "Score 0",
                "abuse_types_identified": [],
                "requires_safety_assessment": False
            }
        }