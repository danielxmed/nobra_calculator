"""
Behavioral Observational Pain Scale (BOPS) Models

Request and response models for BOPS calculation.

References (Vancouver style):
1. Hesselgard K, Larsson S, Romner B, Strömblad LG, Reinstrup P. Validity and 
   reliability of the Behavioural Observational Pain Scale for postoperative pain 
   measurement in children 1-7 years of age. Pediatr Crit Care Med. 2007 Mar;8(2):102-8.
2. von Baeyer CL, Spagrud LJ. Systematic review of observational (behavioral) 
   measures of pain for children and adolescents aged 3 to 18 years. Pain. 2007 Jan;127(1-2):140-50.
3. Duhn LJ, Medves JM. A systematic integrative review of infant pain assessment 
   tools. Adv Neonatal Care. 2004 Jun;4(3):126-40.

The Behavioral Observational Pain Scale (BOPS) was developed in 1996 for nurses and 
physicians to identify, evaluate, and document post-operative pain in children aged 1-7 years. 
It assesses three behavioral components: facial expression, verbalization, and body position.
"""

from pydantic import BaseModel, Field
from typing import Literal


class BehavioralObservationalPainScaleRequest(BaseModel):
    """
    Request model for Behavioral Observational Pain Scale (BOPS)
    
    The BOPS is a validated pediatric pain assessment tool designed specifically for 
    children aged 1-7 years in post-operative settings. It evaluates three key 
    behavioral indicators of pain through direct observation.
    
    Assessment Components:
    
    1. **Facial Expression (0-2 points):**
       - 0: Neutral/positive facial expression, composed, calm
       - 1: Negative facial expression, concerned
       - 2: Negative facial expression, grimace, distorted face
    
    2. **Verbalization (0-2 points):**
       - 0: Normal conversation, laugh, crow
       - 1: Completely quiet, sobbing and/or complaining but not because of pain
       - 2: Crying, screaming and/or complaining about pain
    
    3. **Body Position (0-2 points):**
       - 0: Inactive, laying, relaxed with all extremities or sitting, walking
       - 1: Restless movements, shifting fashion and/or touching wound or wound area
       - 2: Lying rigid and/or drawn up with arms and legs to the body
    
    **Clinical Guidelines:**
    - Target age: 1-7 years old children
    - Use in post-operative settings
    - Assess every 3 hours routinely
    - Reassess 15-20 minutes after IV analgesics
    - Reassess 30-45 minutes after oral/rectal analgesics
    - Scores ≥3 indicate need for analgesia consideration
    
    **Validation Evidence:**
    - Excellent interrater reliability (κw 0.86 to 0.95 for each item)
    - Strong concurrent validity with CHEOPS scale (rs = 0.871, p < 0.001)
    - Validated in post-operative pediatric settings
    
    References (Vancouver style):
    1. Hesselgard K, Larsson S, Romner B, Strömblad LG, Reinstrup P. Validity and 
    reliability of the Behavioural Observational Pain Scale for postoperative pain 
    measurement in children 1-7 years of age. Pediatr Crit Care Med. 2007 Mar;8(2):102-8.
    2. von Baeyer CL, Spagrud LJ. Systematic review of observational (behavioral) 
    measures of pain for children and adolescents aged 3 to 18 years. Pain. 2007 Jan;127(1-2):140-50.
    3. Duhn LJ, Medves JM. A systematic integrative review of infant pain assessment 
    tools. Adv Neonatal Care. 2004 Jun;4(3):126-40.
    """
    
    facial_expression: Literal[0, 1, 2] = Field(
        ...,
        description="Assessment of child's facial expression. 0=Neutral/positive/composed/calm, 1=Negative/concerned, 2=Grimace/distorted face indicating significant distress",
        example=0
    )
    
    verbalization: Literal[0, 1, 2] = Field(
        ...,
        description="Assessment of child's verbal expressions and vocalizations. 0=Normal conversation/laugh/crow, 1=Quiet/sobbing/complaining but not about pain, 2=Crying/screaming/complaining about pain",
        example=1
    )
    
    body_position: Literal[0, 1, 2] = Field(
        ...,
        description="Assessment of child's body positioning and movement patterns. 0=Inactive/relaxed/sitting/walking normally, 1=Restless movements/touching wound area, 2=Rigid/drawn up with arms and legs to body",
        example=0
    )
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "title": "Minimal pain (BOPS = 1)",
                    "value": {
                        "facial_expression": 0,
                        "verbalization": 1,
                        "body_position": 0
                    }
                },
                {
                    "title": "Moderate pain requiring analgesia (BOPS = 3)",
                    "value": {
                        "facial_expression": 1,
                        "verbalization": 1,
                        "body_position": 1
                    }
                },
                {
                    "title": "Severe pain requiring immediate analgesia (BOPS = 6)",
                    "value": {
                        "facial_expression": 2,
                        "verbalization": 2,
                        "body_position": 2
                    }
                }
            ]
        }


class BehavioralObservationalPainScaleResponse(BaseModel):
    """
    Response model for Behavioral Observational Pain Scale (BOPS)
    
    Returns the calculated BOPS score with detailed interpretation including:
    - Pain level classification (Minimal Pain: 0-2 points, Significant Pain: 3-6 points)
    - Component breakdown showing which behaviors contribute to the score
    - Clinical management recommendations based on the pain level
    - Timing guidelines for reassessment after analgesic administration
    
    The BOPS provides a reliable and valid method for assessing post-operative pain 
    in young children through behavioral observation, helping healthcare providers 
    make appropriate pain management decisions in pediatric settings.
    
    **Clinical Thresholds:**
    - Scores 0-2: Minimal pain behaviors, continue comfort measures
    - Scores 3-6: Significant pain behaviors, consider analgesia
    
    **Reassessment Guidelines:**
    - Every 3 hours routinely
    - 15-20 minutes after IV analgesics
    - 30-45 minutes after oral/rectal analgesics
    
    Reference: The BOPS was developed to be simple, clear, and easy to use for 
    caregivers, with excellent psychometric properties for clinical decision-making.
    """
    
    result: int = Field(
        ...,
        description="BOPS score calculated from behavioral observations (0-6 points total)",
        ge=0,
        le=6,
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the BOPS score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation including pain level, component breakdown, and specific management recommendations for post-operative pediatric care",
        example="BOPS score: 1/6 points. Minimal pain behaviors observed in this child aged 1-7 years. Verbalization: Completely quiet, sobbing and/or complaining but not because of pain (1 points). Clinical management: Continue routine monitoring and comfort measures. Consider non-pharmacological comfort interventions such as optimal positioning, parental presence and comfort, distraction techniques, or environmental modifications. Reassess pain regularly every 3 hours or as clinically indicated. No immediate analgesic intervention required at this level, but maintain vigilance for changes."
    )
    
    stage: str = Field(
        ...,
        description="Pain level classification (Minimal Pain or Significant Pain)",
        example="Minimal Pain"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the pain level with clinical significance",
        example="Little to no pain behaviors observed"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "BOPS score: 1/6 points. Minimal pain behaviors observed in this child aged 1-7 years. Verbalization: Completely quiet, sobbing and/or complaining but not because of pain (1 points). Clinical management: Continue routine monitoring and comfort measures. Consider non-pharmacological comfort interventions such as optimal positioning, parental presence and comfort, distraction techniques, or environmental modifications. Reassess pain regularly every 3 hours or as clinically indicated. No immediate analgesic intervention required at this level, but maintain vigilance for changes.",
                "stage": "Minimal Pain",
                "stage_description": "Little to no pain behaviors observed"
            }
        }