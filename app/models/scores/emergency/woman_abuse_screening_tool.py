"""
Woman Abuse Screening Tool (WAST) Models

Request and response models for WAST calculation.

References (Vancouver style):
1. Brown JB, Lent B, Brett PJ, Sas G, Pederson LL. Development of the Woman Abuse 
   Screening Tool for use in family practice. Fam Med. 1996;28(6):422-428.
2. Brown JB, Lent B, Schmidt G, Sas G. Application of the Woman Abuse Screening Tool 
   (WAST) and WAST-short in the family practice setting. J Fam Pract. 2000;49(10):896-903.
3. MacMillan HL, Wathen CN, Jamieson E, et al. Screening for intimate partner violence 
   in health care settings: a randomized trial. JAMA. 2009;302(5):493-501. 
   doi: 10.1001/jama.2009.1089
4. Rabin RF, Jennings JM, Campbell JC, Bair-Merritt MH. Intimate partner violence 
   screening tools: a systematic review. Am J Prev Med. 2009;36(5):439-445.e4. 
   doi: 10.1016/j.amepre.2009.01.024

The WAST is a validated 8-question screening instrument designed to detect intimate 
partner violence (domestic abuse) in healthcare settings. It assesses relationship 
dynamics, emotional impact, and history of physical, emotional, and sexual abuse. 
Lower scores indicate higher risk of domestic violence. The tool requires 
administration in a private, confidential setting and should be integrated with 
safety planning and resource provision for positive screens.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any, List


class WomanAbuseScreeningToolRequest(BaseModel):
    """
    Request model for Woman Abuse Screening Tool (WAST)
    
    The WAST uses 8 questions to screen for intimate partner violence in healthcare 
    settings. This validated instrument assesses relationship dynamics, emotional 
    impact of arguments, and history of abuse across multiple domains.
    
    **IMPORTANT CLINICAL CONSIDERATIONS:**
    - Administer in private, confidential setting without partner present
    - Follow trauma-informed care principles
    - Have domestic violence resources readily available
    - Follow institutional protocols for positive screens
    - Lower scores indicate HIGHER risk of domestic violence
    
    Scoring System:
    - Questions 1-5: Scored 1-3 points (1 = highest risk response)
    - Questions 6-8: Scored 1-2 points (1 = yes = highest risk response)
    - Total score range: 8-24 points
    - Lower scores indicate higher risk of intimate partner violence
    
    Risk Interpretation:
    - Score 8-12: High risk of intimate partner violence
    - Score 13-17: Moderate risk of intimate partner violence  
    - Score 18-24: Low risk of intimate partner violence
    
    Clinical Questions:
    
    1. Relationship Tension: "In general, how would you describe your relationship?"
       - lots_of_tension (1 point): Highest risk
       - some_tension (2 points): Moderate risk
       - no_tension (3 points): Lowest risk
    
    2. Argument Resolution: "Do you and your partner work out arguments with:"
       - great_difficulty (1 point): Highest risk
       - some_difficulty (2 points): Moderate risk
       - no_difficulty (3 points): Lowest risk
    
    3. Arguments Impact: "Do arguments ever result in you feeling down or bad about yourself?"
       - often (1 point): Highest risk
       - sometimes (2 points): Moderate risk
       - never (3 points): Lowest risk
    
    4. Physical Violence: "Do arguments ever result in hitting, kicking or pushing?"
       - often (1 point): Highest risk
       - sometimes (2 points): Moderate risk
       - never (3 points): Lowest risk
    
    5. Fear Response: "Do you ever feel frightened by what your partner says or does?"
       - often (1 point): Highest risk
       - sometimes (2 points): Moderate risk
       - never (3 points): Lowest risk
    
    6. Physical Abuse History: "Has your partner ever abused you physically?"
       - yes (1 point): Indicates abuse (higher risk)
       - no (2 points): No physical abuse reported
    
    7. Emotional Abuse History: "Has your partner ever abused you emotionally?"
       - yes (1 point): Indicates abuse (higher risk)
       - no (2 points): No emotional abuse reported
    
    8. Sexual Abuse History: "Has your partner ever abused you sexually?"
       - yes (1 point): Indicates abuse (higher risk)
       - no (2 points): No sexual abuse reported
    
    References (Vancouver style):
    1. Brown JB, Lent B, Brett PJ, Sas G, Pederson LL. Development of the Woman Abuse 
    Screening Tool for use in family practice. Fam Med. 1996;28(6):422-428.
    2. Brown JB, Lent B, Schmidt G, Sas G. Application of the Woman Abuse Screening Tool 
    (WAST) and WAST-short in the family practice setting. J Fam Pract. 2000;49(10):896-903.
    3. MacMillan HL, Wathen CN, Jamieson E, et al. Screening for intimate partner violence 
    in health care settings: a randomized trial. JAMA. 2009;302(5):493-501. 
    doi: 10.1001/jama.2009.1089
    4. Rabin RF, Jennings JM, Campbell JC, Bair-Merritt MH. Intimate partner violence 
    screening tools: a systematic review. Am J Prev Med. 2009;36(5):439-445.e4. 
    doi: 10.1016/j.amepre.2009.01.024
    """
    
    tension_arguments_relationship: Literal["lots_of_tension", "some_tension", "no_tension"] = Field(
        ...,
        description="Relationship tension level. 'lots_of_tension' indicates highest risk (1 point), 'some_tension' moderate risk (2 points), 'no_tension' lowest risk (3 points)",
        example="some_tension"
    )
    
    partner_jealousy_possessiveness: Literal["great_difficulty", "some_difficulty", "no_difficulty"] = Field(
        ...,
        description="Difficulty resolving arguments with partner. 'great_difficulty' indicates highest risk (1 point), 'some_difficulty' moderate risk (2 points), 'no_difficulty' lowest risk (3 points)",
        example="no_difficulty"
    )
    
    arguments_resolution: Literal["often", "sometimes", "never"] = Field(
        ...,
        description="Frequency of arguments resulting in feeling bad about yourself. 'often' indicates highest risk (1 point), 'sometimes' moderate risk (2 points), 'never' lowest risk (3 points)",
        example="never"
    )
    
    arguments_feeling_bad: Literal["often", "sometimes", "never"] = Field(
        ...,
        description="Frequency of arguments escalating to physical violence (hitting, kicking, pushing). 'often' indicates highest risk (1 point), 'sometimes' moderate risk (2 points), 'never' lowest risk (3 points)",
        example="never"
    )
    
    physical_violence_frequency: Literal["often", "sometimes", "never"] = Field(
        ...,
        description="Frequency of feeling frightened by partner's words or actions. 'often' indicates highest risk (1 point), 'sometimes' moderate risk (2 points), 'never' lowest risk (3 points)",
        example="never"
    )
    
    feel_frightened: Literal["yes", "no"] = Field(
        ...,
        description="History of physical abuse by partner. 'yes' indicates abuse history (higher risk, 1 point), 'no' indicates no physical abuse reported (2 points)",
        example="no"
    )
    
    physical_abuse_history: Literal["yes", "no"] = Field(
        ...,
        description="History of emotional abuse by partner. 'yes' indicates abuse history (higher risk, 1 point), 'no' indicates no emotional abuse reported (2 points)",
        example="no"
    )
    
    emotional_abuse_history: Literal["yes", "no"] = Field(
        ...,
        description="History of sexual abuse by partner. 'yes' indicates abuse history (higher risk, 1 point), 'no' indicates no sexual abuse reported (2 points)",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "tension_arguments_relationship": "some_tension",
                "partner_jealousy_possessiveness": "no_difficulty",
                "arguments_resolution": "never",
                "arguments_feeling_bad": "never",
                "physical_violence_frequency": "never",
                "feel_frightened": "no",
                "physical_abuse_history": "no",
                "emotional_abuse_history": "no"
            }
        }


class WomanAbuseScreeningToolResponse(BaseModel):
    """
    Response model for Woman Abuse Screening Tool (WAST)
    
    The WAST score ranges from 8-24 points and indicates domestic violence risk:
    
    Risk Stratification:
    - 8-12 points: High risk of intimate partner violence
      * Immediate safety assessment and intervention planning required
      * Provide resources, safety planning, and appropriate referrals
      * Follow institutional protocols for high-risk situations
      
    - 13-17 points: Moderate risk of intimate partner violence
      * Further assessment recommended
      * Provide domestic violence resources and support services
      * Consider follow-up screening and social services referral
      
    - 18-24 points: Low risk of intimate partner violence
      * Continue routine care and periodic re-screening
      * Provide general relationship health information if appropriate
      * Remain alert for other indicators of domestic violence
    
    **CRITICAL CLINICAL REMINDERS:**
    - Lower scores indicate HIGHER risk of domestic violence
    - Always ensure patient privacy and safety during screening
    - Have domestic violence resources readily available
    - Follow mandatory reporting requirements per institutional policy
    - Use trauma-informed care principles throughout assessment
    
    Reference: Brown JB, et al. Fam Med. 1996;28(6):422-428.
    """
    
    result: int = Field(
        ...,
        description="WAST total score calculated from 8 screening questions (range: 8-24 points). LOWER scores indicate HIGHER risk of intimate partner violence",
        ge=8,
        le=24,
        example=18
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended actions based on the WAST score and risk level",
        example="WAST score of 18 indicates low likelihood of domestic violence based on current responses. Continue routine care and provide general information about healthy relationships if appropriate. Consider periodic re-screening as relationship dynamics may change over time. Remain alert to other signs or symptoms that may indicate domestic violence."
    )
    
    stage: str = Field(
        ...,
        description="Risk level category (High Risk, Moderate Risk, Low Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level category",
        example="Low probability of intimate partner violence"
    )
    
    risk_level: str = Field(
        ...,
        description="Risk level classification (high, moderate, low)",
        example="low"
    )
    
    safety_recommendations: List[str] = Field(
        ...,
        description="Safety recommendations and immediate actions based on risk level",
        example=[
            "Continue routine screening at future visits",
            "Provide general relationship health information if appropriate",
            "Remain alert for other indicators of domestic violence",
            "Document negative screening results"
        ]
    )
    
    detailed_assessment: Dict[str, Any] = Field(
        ...,
        description="Comprehensive assessment including score breakdown, risk factors, interventions, and resources",
        example={
            "score_breakdown": {
                "individual_scores": {
                    "tension_arguments_relationship": {
                        "response": "some_tension",
                        "score": 2,
                        "description": "Relationship tension level"
                    }
                },
                "high_risk_indicators": [],
                "total_possible_score": 24,
                "risk_percentage": 12.5
            },
            "risk_factors": [],
            "intervention_guidelines": [
                "Continue supportive care",
                "Maintain awareness of domestic violence indicators"
            ],
            "resource_recommendations": [
                "General relationship health resources",
                "Mental health and wellness resources"
            ]
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 18,
                "unit": "points",
                "interpretation": "WAST score of 18 indicates low likelihood of domestic violence based on current responses. Continue routine care and provide general information about healthy relationships if appropriate. Consider periodic re-screening as relationship dynamics may change over time. Remain alert to other signs or symptoms that may indicate domestic violence.",
                "stage": "Low Risk",
                "stage_description": "Low probability of intimate partner violence",
                "risk_level": "low",
                "safety_recommendations": [
                    "Continue routine screening at future visits",
                    "Provide general relationship health information if appropriate",
                    "Remain alert for other indicators of domestic violence",
                    "Document negative screening results"
                ],
                "detailed_assessment": {
                    "score_breakdown": {
                        "individual_scores": {
                            "tension_arguments_relationship": {
                                "response": "some_tension",
                                "score": 2,
                                "description": "Relationship tension level"
                            }
                        },
                        "high_risk_indicators": [],
                        "total_possible_score": 24,
                        "risk_percentage": 12.5
                    },
                    "risk_factors": [],
                    "intervention_guidelines": [
                        "Continue supportive care",
                        "Maintain awareness of domestic violence indicators"
                    ],
                    "resource_recommendations": [
                        "General relationship health resources",
                        "Mental health and wellness resources"
                    ]
                }
            }
        }