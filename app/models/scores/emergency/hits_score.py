"""
HITS (Hurt, Insult, Threaten, Scream) Score Models

Request and response models for HITS intimate partner violence screening.

References (Vancouver style):
1. Sherin KM, Sinacore JM, Li XQ, Zitter RE, Shakil A. HITS: a short domestic violence 
   screening tool for use in a family practice setting. Fam Med. 1998 Jul-Aug;30(7):508-12. 
   PMID: 9669164.
2. Shakil A, Donald S, Sinacore JM, Krepcho M. Validation of the HITS domestic violence 
   screening tool with males. Fam Med. 2005 Mar;37(3):193-8. PMID: 15739135.
3. US Preventive Services Task Force. Screening for Intimate Partner Violence, Elder Abuse, 
   and Abuse of Vulnerable Adults: US Preventive Services Task Force Recommendation Statement. 
   JAMA. 2018 Oct 23;320(16):1678-1687. doi: 10.1001/jama.2018.14741.

The HITS screening tool consists of four questions (Hurt, Insult, Threaten, Scream) 
that assess the frequency of different types of intimate partner violence. Each question 
is rated on a 5-point frequency scale from "never" (1 point) to "frequently" (5 points), 
with total scores ranging from 4-20. A score ≥11 indicates a positive screen requiring 
immediate safety assessment and intervention.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Optional


class HitsScoreRequest(BaseModel):
    """
    Request model for HITS (Hurt, Insult, Threaten, Scream) Score
    
    The HITS tool uses 4 questions to assess frequency of intimate partner violence:
    
    H - Hurt: Physical violence including hitting, slapping, pushing, kicking, 
        choking, or any form of physical harm
    
    I - Insult: Verbal/emotional abuse including insults, put-downs, name-calling, 
        humiliation, or demeaning language
    
    T - Threaten: Threats of harm including threats of violence, intimidation, 
        weapons, or creating fear of bodily harm
    
    S - Scream: Verbal aggression including screaming, yelling, cursing, 
        or other forms of verbal hostility
    
    Frequency Scale:
    - Never (1 point): Behavior does not occur
    - Rarely (2 points): Behavior occurs infrequently
    - Sometimes (3 points): Behavior occurs occasionally
    - Fairly Often (4 points): Behavior occurs regularly
    - Frequently (5 points): Behavior occurs very often
    
    Important Clinical Notes:
    - Validated for both women and men in healthcare settings
    - Available in English and Spanish with different cut-off scores
    - Should be administered privately without partner/family present
    - Cut-off ≥11 for English version (sensitivity 86%, specificity 99%)
    - Cut-off ≥6 for Spanish version (sensitivity 100%, specificity 86%)
    
    References (Vancouver style):
    1. Sherin KM, Sinacore JM, Li XQ, Zitter RE, Shakil A. HITS: a short domestic violence 
       screening tool for use in a family practice setting. Fam Med. 1998 Jul-Aug;30(7):508-12. 
       PMID: 9669164.
    2. Shakil A, Donald S, Sinacore JM, Krepcho M. Validation of the HITS domestic violence 
       screening tool with males. Fam Med. 2005 Mar;37(3):193-8. PMID: 15739135.
    """
    
    physically_hurt: Literal["never", "rarely", "sometimes", "fairly_often", "frequently"] = Field(
        ...,
        description="How often does your partner physically hurt you? This includes hitting, "
                   "slapping, pushing, kicking, choking, or any form of physical violence. "
                   "Scale: never (1), rarely (2), sometimes (3), fairly_often (4), frequently (5).",
        example="never"
    )
    
    insult_talk_down: Literal["never", "rarely", "sometimes", "fairly_often", "frequently"] = Field(
        ...,
        description="How often does your partner insult you or talk down to you? This includes "
                   "name-calling, put-downs, humiliation, demeaning language, or emotional abuse. "
                   "Scale: never (1), rarely (2), sometimes (3), fairly_often (4), frequently (5).",
        example="never"
    )
    
    threaten_with_harm: Literal["never", "rarely", "sometimes", "fairly_often", "frequently"] = Field(
        ...,
        description="How often does your partner threaten you with harm? This includes threats "
                   "of violence, intimidation, weapon threats, or creating fear of bodily harm. "
                   "Scale: never (1), rarely (2), sometimes (3), fairly_often (4), frequently (5).",
        example="never"
    )
    
    scream_curse: Literal["never", "rarely", "sometimes", "fairly_often", "frequently"] = Field(
        ...,
        description="How often does your partner scream or curse at you? This includes yelling, "
                   "screaming, cursing, or other forms of verbal aggression and hostility. "
                   "Scale: never (1), rarely (2), sometimes (3), fairly_often (4), frequently (5).",
        example="never"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "physically_hurt": "never",
                "insult_talk_down": "never",
                "threaten_with_harm": "never",
                "scream_curse": "never"
            }
        }


class HitsScoreResponse(BaseModel):
    """
    Response model for HITS (Hurt, Insult, Threaten, Scream) Score
    
    The HITS score ranges from 4-20 points with frequency-based scoring:
    
    - Score 4-10: Low risk for intimate partner violence
    - Score ≥11: Positive screen requiring immediate safety assessment
    
    The HITS tool has demonstrated good psychometric properties:
    - Internal consistency: Cronbach's alpha = 0.80
    - Correlation with Conflict Tactics Scale: r = 0.85
    - English version: Cut-off ≥11 (sensitivity 86%, specificity 99%)
    - Spanish version: Cut-off ≥6 (sensitivity 100%, specificity 86%)
    
    A positive screen indicates need for safety planning, resource provision, 
    and follow-up care according to institutional protocols and local reporting requirements.
    
    Reference: Sherin KM, et al. Fam Med. 1998;30(7):508-12.
    """
    
    result: int = Field(
        ...,
        ge=4,
        le=20,
        description="HITS score calculated as sum of frequency ratings for 4 questions (range: 4-20 points)",
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with screening result and recommended actions "
                   "based on score (low risk vs positive screen)",
        example="Low risk for intimate partner violence based on current screening. "
                "Continue to provide supportive care and maintain awareness for signs "
                "of abuse. Consider follow-up screening at future visits."
    )
    
    stage: str = Field(
        ...,
        description="Screening result category (Low Risk or Positive Screen)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Score range description for the screening result",
        example="Score 4-10"
    )
    
    positive_screen: bool = Field(
        ...,
        description="Boolean indicating whether screening result is positive (score ≥11)",
        example=False
    )
    
    requires_safety_assessment: bool = Field(
        ...,
        description="Boolean indicating whether immediate safety assessment is required "
                   "(true for positive screen, false for low risk)",
        example=False
    )
    
    abuse_behaviors_identified: Dict[str, str] = Field(
        ...,
        description="Dictionary of identified abuse behaviors with their reported frequencies. "
                   "May include: Physical Violence, Emotional/Verbal Abuse, Threats of Harm, "
                   "Screaming/Cursing. Only includes behaviors reported as occurring (not 'never').",
        example={}
    )
    
    sensitivity_english: Optional[int] = Field(
        None,
        description="Sensitivity percentage for English version when positive screen (86%)",
        example=None
    )
    
    specificity_english: Optional[int] = Field(
        None,
        description="Specificity percentage for English version when negative screen (99%)",
        example=99
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "Low risk for intimate partner violence based on current "
                                "screening. Continue to provide supportive care and maintain "
                                "awareness for signs of abuse. Consider follow-up screening "
                                "at future visits.",
                "stage": "Low Risk",
                "stage_description": "Score 4-10",
                "positive_screen": False,
                "requires_safety_assessment": False,
                "abuse_behaviors_identified": {},
                "sensitivity_english": None,
                "specificity_english": 99
            }
        }