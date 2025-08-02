"""
Injury Severity Score (ISS) Models

Request and response models for Injury Severity Score calculation.

References (Vancouver style):
1. Baker SP, O'Neill B, Haddon W Jr, Long WB. The injury severity score: a method 
   for describing patients with multiple injuries and evaluating emergency care. 
   J Trauma. 1974 Mar;14(3):187-96.
2. Beverland DE, Rutherford WH. An assessment of the validity of the injury severity 
   score when applied to gunshot wounds. Injury. 1983 Mar;14(5):471-5.
3. Copes WS, Champion HR, Sacco WJ, Lawnick MM, Keast SL, Bain LW. The Injury 
   Severity Score revisited. J Trauma. 1988 Jan;28(1):69-77.

The Injury Severity Score (ISS) standardizes traumatic injury severity based on 
the worst injury from 6 body systems using the Abbreviated Injury Scale (AIS). 
Developed by Baker and colleagues in 1974, the ISS correlates linearly with 
mortality, morbidity, and hospitalization time after trauma. The score divides 
the body into six regions, uses the three most severely injured systems, and 
calculates the final score by squaring and summing these three highest AIS scores.
"""

from pydantic import BaseModel, Field
from typing import Literal


class InjurySeverityScoreRequest(BaseModel):
    """
    Request model for Injury Severity Score (ISS) calculation
    
    Assesses trauma severity using the Abbreviated Injury Scale (AIS) across 6 body regions.
    Each region is scored 0-6 based on injury severity:
    
    AIS Scale:
    - 0: No injury
    - 1: Minor injury (minimal threat to life)
    - 2: Moderate injury (moderate threat to life)
    - 3: Serious injury (serious but not immediately life-threatening)
    - 4: Severe injury (life-threatening but survival probable)
    - 5: Critical injury (survival uncertain)
    - 6: Unsurvivable injury (fatal)
    
    Body Regions:
    - Head and neck: Includes cervical spine injuries
    - Face: Includes facial skeleton, nose, mouth, eyes, and ears
    - Chest: Includes rib cage, thoracic spine, and diaphragm
    - Abdomen: Includes abdominal organs and lumbar spine
    - Extremity: Includes pelvic skeleton, sprains, fractures, dislocations
    - External: Includes skin and soft tissue injuries
    
    ISS Calculation:
    - If any AIS = 6 (unsurvivable), ISS automatically = 75
    - Otherwise: ISS = A² + B² + C² (where A, B, C are the 3 highest AIS scores)
    - Score range: 0-75 points
    - Score ≥16 traditionally defines major trauma
    
    References (Vancouver style):
    1. Baker SP, O'Neill B, Haddon W Jr, Long WB. The injury severity score: a method 
       for describing patients with multiple injuries and evaluating emergency care. 
       J Trauma. 1974 Mar;14(3):187-96.
    2. Copes WS, Champion HR, Sacco WJ, Lawnick MM, Keast SL, Bain LW. The Injury 
       Severity Score revisited. J Trauma. 1988 Jan;28(1):69-77.
    """
    
    head_neck_ais: int = Field(
        ...,
        description="Head and neck injury severity using AIS scale (0-6). Includes brain, skull, cervical spine, and neck injuries. Score 0=No injury, 1=Minor, 2=Moderate, 3=Serious, 4=Severe, 5=Critical, 6=Unsurvivable",
        example=3,
        ge=0,
        le=6
    )
    
    face_ais: int = Field(
        ...,
        description="Facial injury severity using AIS scale (0-6). Includes facial skeleton, nose, mouth, eyes, ears, and facial soft tissue. Score 0=No injury, 1=Minor, 2=Moderate, 3=Serious, 4=Severe, 5=Critical, 6=Unsurvivable",
        example=1,
        ge=0,
        le=6
    )
    
    chest_ais: int = Field(
        ...,
        description="Chest injury severity using AIS scale (0-6). Includes rib cage, sternum, thoracic spine, diaphragm, and intrathoracic organs. Score 0=No injury, 1=Minor, 2=Moderate, 3=Serious, 4=Severe, 5=Critical, 6=Unsurvivable",
        example=4,
        ge=0,
        le=6
    )
    
    abdomen_ais: int = Field(
        ...,
        description="Abdominal injury severity using AIS scale (0-6). Includes abdominal organs, lumbar spine, and pelvic contents. Score 0=No injury, 1=Minor, 2=Moderate, 3=Serious, 4=Severe, 5=Critical, 6=Unsurvivable",
        example=2,
        ge=0,
        le=6
    )
    
    extremity_ais: int = Field(
        ...,
        description="Extremity injury severity using AIS scale (0-6). Includes pelvic skeleton, arms, legs, sprains, fractures, and dislocations. Score 0=No injury, 1=Minor, 2=Moderate, 3=Serious, 4=Severe, 5=Critical, 6=Unsurvivable",
        example=2,
        ge=0,
        le=6
    )
    
    external_ais: int = Field(
        ...,
        description="External injury severity using AIS scale (0-6). Includes skin, soft tissue, burns, and external wounds. Score 0=No injury, 1=Minor, 2=Moderate, 3=Serious, 4=Severe, 5=Critical, 6=Unsurvivable",
        example=1,
        ge=0,
        le=6
    )
    
    class Config:
        schema_extra = {
            "example": {
                "head_neck_ais": 3,
                "face_ais": 1,
                "chest_ais": 4,
                "abdomen_ais": 2,
                "extremity_ais": 2,
                "external_ais": 1
            }
        }


class InjurySeverityScoreResponse(BaseModel):
    """
    Response model for Injury Severity Score (ISS) calculation
    
    Returns the calculated ISS with trauma severity classification:
    - Minor Trauma (0-8): Low mortality risk, standard protocols
    - Moderate Trauma (9-15): Increased morbidity, consider trauma team
    - Major Trauma (16-24): Significant mortality risk, trauma team activation
    - Severe Trauma (25-40): High mortality risk, aggressive resuscitation
    - Critical Trauma (41-75): Very high mortality, maximum response
    
    The ISS provides standardized trauma severity assessment for research purposes 
    and correlates with mortality, morbidity, and hospitalization time. Scores ≥16 
    traditionally define major trauma requiring trauma center care. The maximum 
    possible score is 75, automatically assigned when any body region has an 
    unsurvivable injury (AIS = 6).
    
    Reference: Baker SP, et al. J Trauma. 1974;14(3):187-96.
    """
    
    result: int = Field(
        ...,
        description="Injury Severity Score calculated from the three highest AIS scores (range 0-75 points)",
        example=29,
        ge=0,
        le=75
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the ISS score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and trauma management recommendations based on ISS severity category",
        example="Severe trauma. High mortality risk. Requires immediate trauma team response, aggressive resuscitation, and specialized trauma care."
    )
    
    stage: str = Field(
        ...,
        description="Trauma severity category (Minor, Moderate, Major, Severe, Critical)",
        example="Severe Trauma"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the trauma severity category with score range",
        example="ISS 29 points (25-40 points)"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 29,
                "unit": "points",
                "interpretation": "Severe trauma. High mortality risk. Requires immediate trauma team response, aggressive resuscitation, and specialized trauma care.",
                "stage": "Severe Trauma",
                "stage_description": "ISS 29 points (25-40 points)"
            }
        }