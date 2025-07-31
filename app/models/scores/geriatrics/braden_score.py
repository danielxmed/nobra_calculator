"""
Braden Score for Pressure Ulcers Models

Request and response models for Braden Score calculation.

References (Vancouver style):
1. Braden BJ, Bergstrom N. Clinical utility of the Braden scale for Predicting 
   Pressure Sore Risk. Decubitus. 1989 Aug;2(3):44-6, 50-1.
2. Bergstrom N, Braden BJ, Laguzza A, Holman V. The Braden Scale for Predicting 
   Pressure Sore Risk. Nurs Res. 1987 Jul-Aug;36(4):205-10.
3. Braden BJ, Maklebust J. Preventing pressure ulcers with the Braden scale: an 
   update on this easy-to-use tool that assesses a patient's risk. Am J Nurs. 
   2005 Jun;105(6):70-2.

The Braden Scale is a clinically validated assessment tool developed in 1987 to 
predict pressure ulcer risk. It evaluates six subscales: sensory perception, 
moisture, activity, mobility, nutrition, and friction/shear. Lower scores indicate 
higher risk, with a total score range of 6-23 points. The tool is widely used 
across various healthcare settings to guide preventive interventions.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class BradenScoreRequest(BaseModel):
    """
    Request model for Braden Score for Pressure Ulcers
    
    The Braden Scale assesses six factors to determine pressure ulcer risk:
    
    1. Sensory Perception (1-4 points):
       - 1: Completely limited - unresponsive to painful stimuli
       - 2: Very limited - responds only to painful stimuli
       - 3: Slightly limited - responds to verbal commands with limitations
       - 4: No impairment - responds normally to pressure discomfort
    
    2. Moisture (1-4 points):
       - 1: Constantly moist - skin always damp
       - 2: Very moist - often damp, linen changed once per shift
       - 3: Occasionally moist - extra linen change once daily
       - 4: Rarely moist - skin usually dry
    
    3. Activity (1-4 points):
       - 1: Bedfast - confined to bed
       - 2: Chairfast - cannot walk, must be assisted to chair
       - 3: Walks occasionally - short distances with/without assistance
       - 4: Walks frequently - outside room 2x/day minimum
    
    4. Mobility (1-4 points):
       - 1: Completely immobile - no position changes without help
       - 2: Very limited - occasional slight changes only
       - 3: Slightly limited - frequent slight changes independently
       - 4: No limitation - major frequent position changes
    
    5. Nutrition (1-4 points):
       - 1: Very poor - never eats complete meal, <2 protein servings/day
       - 2: Probably inadequate - eats ~50% of meals, 3 protein servings/day
       - 3: Adequate - eats >50% of meals, 4 protein servings/day
       - 4: Excellent - eats most meals, 4+ protein servings/day
    
    6. Friction and Shear (1-3 points):
       - 1: Problem - requires maximum assistance, frequent sliding
       - 2: Potential problem - minimal assistance, some sliding
       - 3: No apparent problem - moves independently
    
    References:
    1. Braden BJ, Bergstrom N. Decubitus. 1989;2(3):44-6, 50-1.
    2. Bergstrom N, et al. Nurs Res. 1987;36(4):205-10.
    """
    
    sensory_perception: Literal[1, 2, 3, 4] = Field(
        ...,
        description="Ability to respond meaningfully to pressure-related discomfort. 1=Completely limited (unresponsive), 2=Very limited (responds only to pain), 3=Slightly limited (verbal response with limitations), 4=No impairment",
        example=3
    )
    
    moisture: Literal[1, 2, 3, 4] = Field(
        ...,
        description="Degree to which skin is exposed to moisture. 1=Constantly moist, 2=Very moist (linen change once/shift), 3=Occasionally moist (extra change once/day), 4=Rarely moist",
        example=3
    )
    
    activity: Literal[1, 2, 3, 4] = Field(
        ...,
        description="Degree of physical activity. 1=Bedfast, 2=Chairfast (cannot walk), 3=Walks occasionally (short distances), 4=Walks frequently (2x/day outside room)",
        example=2
    )
    
    mobility: Literal[1, 2, 3, 4] = Field(
        ...,
        description="Ability to change and control body position. 1=Completely immobile, 2=Very limited (occasional slight changes), 3=Slightly limited (frequent slight changes), 4=No limitation",
        example=2
    )
    
    nutrition: Literal[1, 2, 3, 4] = Field(
        ...,
        description="Usual food intake pattern. 1=Very poor (<1/3 meals, 2 protein/day), 2=Probably inadequate (~1/2 meals, 3 protein/day), 3=Adequate (>1/2 meals, 4 protein/day), 4=Excellent (most meals, 4+ protein/day)",
        example=3
    )
    
    friction_shear: Literal[1, 2, 3] = Field(
        ...,
        description="Friction and shear forces when moving. 1=Problem (max assistance needed, frequent sliding), 2=Potential problem (min assistance, some sliding), 3=No apparent problem (moves independently)",
        example=2
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "sensory_perception": 3,
                "moisture": 3,
                "activity": 2,
                "mobility": 2,
                "nutrition": 3,
                "friction_shear": 2
            }
        }


class BradenScoreResponse(BaseModel):
    """
    Response model for Braden Score for Pressure Ulcers
    
    The Braden Score stratifies patients into five risk categories:
    - No Risk (19-23 points): Continue routine care
    - Mild Risk (15-18 points): Basic preventive measures
    - Moderate Risk (13-14 points): Enhanced prevention protocol
    - High Risk (10-12 points): Aggressive prevention measures
    - Very High Risk (≤9 points): Maximum prevention interventions
    
    Lower scores indicate higher risk for pressure ulcer development.
    
    Reference: Braden BJ, Bergstrom N. Decubitus. 1989;2(3):44-6, 50-1.
    """
    
    result: int = Field(
        ...,
        ge=6,
        le=23,
        description="Total Braden score calculated from six subscales (range: 6-23 points)",
        example=15
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk level and recommended preventive interventions",
        example="Patient is at mild risk for developing pressure ulcers. Implement basic preventive measures including turning schedule every 2-3 hours, skin moisturization, and nutritional support."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (No Risk, Mild Risk, Moderate Risk, High Risk, or Very High Risk)",
        example="Mild Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="Mild risk for pressure ulcers"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 15,
                "unit": "points",
                "interpretation": "Patient is at mild risk for developing pressure ulcers. Implement basic preventive measures including turning schedule every 2-3 hours, skin moisturization, and nutritional support.",
                "stage": "Mild Risk",
                "stage_description": "Mild risk for pressure ulcers"
            }
        }