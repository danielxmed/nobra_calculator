"""
Aas calculation models
"""

from pydantic import BaseModel, Field
from enum import Enum


class YesNoType(str, Enum):
    """Enum for yes/no responses"""
    YES = "yes"
    NO = "no"


class YesNoNAType(str, Enum):
    """Enum for yes/no/not applicable responses"""
    YES = "yes"
    NO = "no"
    NOT_APPLICABLE = "not_applicable"


class AasRequest(BaseModel):
    """
    Request model for Abuse Assessment Screen (AAS)
    
    The AAS is a validated screening tool for identifying domestic violence and intimate
    partner violence in healthcare settings, particularly effective in emergency and
    prenatal care environments.
    
    **Clinical Use**:
    - Domestic violence screening in healthcare settings
    - Intimate partner violence identification
    - Emergency department risk assessment
    - Prenatal care safety evaluation
    - Primary care routine screening
    - Mental health assessment context
    
    **Implementation Guidelines**:
    - Conduct screening in private, confidential setting
    - Ensure patient safety and privacy
    - Have resources and referrals readily available
    - Document carefully with attention to legal implications
    - Follow mandatory reporting requirements per jurisdiction
    
    **Reference**: Soeken KL, et al. The abuse assessment screen: a clinical instrument to measure frequency, severity, and perpetrator of abuse against women. In: Campbell JC, editor. Empowering survivors of abuse. Thousand Oaks, CA: Sage; 1998.
    """
    emotional_physical_abuse: YesNoType = Field(
        ..., 
        description="Have you ever been emotionally or physically abused by your partner or someone important to you? This broad question screens for any history of intimate partner violence.",
        example="no"
    )
    physical_hurt_recently: YesNoType = Field(
        ..., 
        description="Within the last year (or since your last visit), have you been hit, slapped, kicked, or otherwise physically hurt by someone? This assesses recent physical violence.",
        example="no"
    )
    physical_hurt_pregnancy: YesNoNAType = Field(
        ..., 
        description="Since you've been pregnant (or if not applicable, select 'not_applicable'), have you been hit, slapped, kicked, or otherwise physically hurt by someone? Violence during pregnancy poses risks to both mother and fetus.",
        example="not_applicable"
    )
    sexual_abuse: YesNoType = Field(
        ..., 
        description="Within the last year, has anyone forced you to have sexual activities that you did not want? This screens for sexual violence and coercion.",
        example="no"
    )
    afraid_of_partner: YesNoType = Field(
        ..., 
        description="Are you afraid of your partner or anyone you listed above? Fear indicates ongoing threat and immediate safety concerns.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "emotional_physical_abuse": "no",
                "physical_hurt_recently": "no",
                "physical_hurt_pregnancy": "not_applicable",
                "sexual_abuse": "no",
                "afraid_of_partner": "no"
            }
        }


class AasResponse(BaseModel):
    """
    Response model for Abuse Assessment Screen (AAS)
    
    Provides domestic violence screening results with appropriate clinical guidance
    and resource information for both positive and negative screens.
    
    **Positive Screen Actions**:
    - Ensure immediate safety and privacy
    - Provide validation and support
    - Offer resources (hotlines, shelters, counseling)
    - Safety planning if appropriate
    - Documentation per institutional policy
    - Follow mandatory reporting laws
    
    **Negative Screen Actions**:
    - Provide information about available resources
    - Normalize the screening process
    - Encourage future disclosure if situations change
    - Document negative screen appropriately
    
    **Resources**:
    - National Domestic Violence Hotline: 1-800-799-7233
    - Local law enforcement and emergency services
    - Community domestic violence programs
    - Legal advocacy services
    """
    result: str = Field(
        ..., 
        description="Overall AAS screening result indicating presence or absence of domestic violence indicators (Positive/Negative).",
        example="Negative"
    )
    unit: str = Field(
        ..., 
        description="Unit of the screening result",
        example="result"
    )
    interpretation: str = Field(
        ..., 
        description="Clinical interpretation with appropriate guidance for follow-up actions, resource provision, and safety considerations based on screening results.",
        example="Negative result for domestic violence. Continue to offer support and information about available resources."
    )
    stage: str = Field(
        ..., 
        description="Screening result classification (Positive Screening, Negative Screening)",
        example="Negative Screening"
    )
    stage_description: str = Field(
        ..., 
        description="Description of the screening outcome",
        example="No indication of domestic abuse"
    )
    positive_responses_count: int = Field(
        ..., 
        description="Number of questions answered positively, providing quantitative assessment of abuse indicators.",
        example=0
    )
    is_positive: bool = Field(
        ..., 
        description="Boolean indicator of whether the screening is considered positive (any 'yes' response typically indicates positive screen).",
        example=False
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Negative",
                "unit": "result",
                "interpretation": "Negative result for domestic violence. Continue to offer support and information about available resources.",
                "stage": "Negative Screening",
                "stage_description": "No indication of domestic abuse",
                "positive_responses_count": 0,
                "is_positive": False
            }
        }
