"""
COPD Assessment Test (CAT) Models

Request and response models for CAT calculation.

References (Vancouver style):
1. Jones PW, Harding G, Berry P, Wiklund I, Chen WH, Kline Leidy N. Development 
   and first validation of the COPD Assessment Test. Eur Respir J. 2009 Sep;34(3):648-54. 
   doi: 10.1183/09031936.00102509.
2. Global Initiative for Chronic Obstructive Lung Disease (GOLD). Global Strategy 
   for the Diagnosis, Management, and Prevention of Chronic Obstructive Pulmonary 
   Disease: 2023 Report.
3. Gupta N, Pinto LM, Morogan A, Bourbeau J. The COPD assessment test: a systematic 
   review. Eur Respir J. 2014 Oct;44(4):873-84. doi: 10.1183/09031936.00025214.

The CAT is an 8-item questionnaire that measures the impact of COPD on patients' 
health status and daily life, validated as equivalent to the SGRQ.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Dict, List


class CopdCatRequest(BaseModel):
    """
    Request model for COPD Assessment Test (CAT)
    
    The CAT consists of 8 items, each scored 0-5:
    1. Cough frequency
    2. Phlegm production
    3. Chest tightness
    4. Breathlessness on exertion
    5. Activity limitations at home
    6. Confidence leaving home
    7. Sleep quality
    8. Energy level
    
    Total score ranges from 0-40, with higher scores indicating greater impact
    of COPD on quality of life. A change of ≥2 points is considered clinically
    significant.
    
    Note: The CAT is not a diagnostic tool but measures disease impact in 
    patients with established COPD diagnosis.
    
    References (Vancouver style):
    1. Jones PW, Harding G, Berry P, Wiklund I, Chen WH, Kline Leidy N. Development 
       and first validation of the COPD Assessment Test. Eur Respir J. 2009 Sep;34(3):648-54.
    """
    
    cough: int = Field(
        ...,
        ge=0,
        le=5,
        description="Cough frequency. 0='I never cough' to 5='I cough all the time'",
        example=2
    )
    
    phlegm: int = Field(
        ...,
        ge=0,
        le=5,
        description="Phlegm (mucus) production. 0='I have no phlegm in my chest at all' to 5='My chest is completely full of phlegm'",
        example=2
    )
    
    chest_tightness: int = Field(
        ...,
        ge=0,
        le=5,
        description="Chest tightness. 0='My chest does not feel tight at all' to 5='My chest feels very tight'",
        example=1
    )
    
    breathlessness: int = Field(
        ...,
        ge=0,
        le=5,
        description="Breathlessness when walking up a hill or one flight of stairs. 0='I am not breathless' to 5='I am very breathless'",
        example=3
    )
    
    activities: int = Field(
        ...,
        ge=0,
        le=5,
        description="Activity limitation at home. 0='I am not limited doing any activities at home' to 5='I am very limited doing any activities at home'",
        example=2
    )
    
    confidence: int = Field(
        ...,
        ge=0,
        le=5,
        description="Confidence leaving home. 0='I am confident leaving my home despite my lung condition' to 5='I am not at all confident leaving my home because of my lung condition'",
        example=1
    )
    
    sleep: int = Field(
        ...,
        ge=0,
        le=5,
        description="Sleep quality. 0='I sleep soundly' to 5='I don't sleep soundly because of my lung condition'",
        example=2
    )
    
    energy: int = Field(
        ...,
        ge=0,
        le=5,
        description="Energy level. 0='I have lots of energy' to 5='I have no energy at all'",
        example=3
    )
    
    @field_validator('cough', 'phlegm', 'chest_tightness', 'breathlessness', 
                     'activities', 'confidence', 'sleep', 'energy')
    def validate_score_range(cls, v, info):
        """Ensure all scores are within 0-5 range"""
        if not 0 <= v <= 5:
            raise ValueError(f"{info.field_name} must be between 0 and 5")
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "cough": 2,
                "phlegm": 2,
                "chest_tightness": 1,
                "breathlessness": 3,
                "activities": 2,
                "confidence": 1,
                "sleep": 2,
                "energy": 3
            }
        }
    }


class CopdCatResponse(BaseModel):
    """
    Response model for COPD Assessment Test (CAT)
    
    CAT score interpretation:
    - 0-10: Low impact on health
    - 11-20: Medium impact on health
    - 21-30: High impact on health
    - 31-40: Very high impact on health
    
    Management recommendations are based on GOLD 2023 guidelines and include
    bronchodilator optimization, pulmonary rehabilitation, and oxygen therapy
    considerations based on impact level.
    
    Reference: GOLD 2023 Report
    """
    
    result: int = Field(
        ...,
        description="Total CAT score (0-40 points)",
        example=16
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with management recommendations",
        example="COPD has medium impact on patient's life. Optimize bronchodilator therapy with LAMA, LABA, or combination. Ensure smoking cessation, preventive care, and reduced exposure to exacerbation risk factors."
    )
    
    stage: str = Field(
        ...,
        description="Impact level category",
        example="Medium impact"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of COPD impact level",
        example="Medium COPD impact on health"
    )
    
    item_scores: Dict[str, int] = Field(
        ...,
        description="Individual scores for each of the 8 CAT items",
        example={
            "cough": 2,
            "phlegm": 2,
            "chest_tightness": 1,
            "breathlessness": 3,
            "activities": 2,
            "confidence": 1,
            "sleep": 2,
            "energy": 3
        }
    )
    
    highly_symptomatic_items: List[str] = Field(
        ...,
        description="Items with scores ≥3, indicating highly symptomatic areas",
        example=["breathlessness", "energy"]
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "result": 16,
                "unit": "points",
                "interpretation": "COPD has medium impact on patient's life. Optimize bronchodilator therapy with LAMA, LABA, or combination. Ensure smoking cessation, preventive care, and reduced exposure to exacerbation risk factors.",
                "stage": "Medium impact",
                "stage_description": "Medium COPD impact on health",
                "item_scores": {
                    "cough": 2,
                    "phlegm": 2,
                    "chest_tightness": 1,
                    "breathlessness": 3,
                    "activities": 2,
                    "confidence": 1,
                    "sleep": 2,
                    "energy": 3
                },
                "highly_symptomatic_items": ["breathlessness", "energy"]
            }
        }
    }