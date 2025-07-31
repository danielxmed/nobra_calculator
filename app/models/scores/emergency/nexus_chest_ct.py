"""
NEXUS Chest CT Decision Instrument Models

Request and response models for NEXUS Chest CT calculation.

References (Vancouver style):
1. Rodriguez RM, Langdorf MI, Nishijima D, Baumann BM, Hendey GW, Medak AJ, et al. 
   Derivation and validation of two decision instruments for selective chest CT in 
   blunt trauma: a multicenter prospective observational study (NEXUS Chest CT). 
   PLoS Med. 2015 Oct 6;12(10):e1001883. doi: 10.1371/journal.pmed.1001883.
2. Rodriguez RM, Hendey GW, Mower W, Kea B, Fortman J, Merchant G, et al. 
   Derivation of a decision instrument for selective chest radiography in blunt 
   trauma. J Trauma. 2011 Sep;71(3):549-53. doi: 10.1097/TA.0b013e3181f2ac9d.

The NEXUS Chest CT-All decision instrument uses 7 criteria to identify blunt trauma 
patients who can safely avoid CT chest imaging. With 99.0% sensitivity for all 
thoracic injuries and 100% sensitivity for aortic and great vessel injuries, it 
provides a reliable tool for selective imaging in hemodynamically stable patients.
"""

from pydantic import BaseModel, Field
from typing import Literal


class NexusChestCtRequest(BaseModel):
    """
    Request model for NEXUS Chest CT Decision Instrument
    
    The NEXUS Chest CT-All version evaluates 7 criteria to determine need for CT imaging:
    
    1. Abnormal chest X-ray (showing any thoracic injury or widened mediastinum)
    2. Distracting injury
    3. Chest wall tenderness
    4. Sternal tenderness
    5. Thoracic spine tenderness
    6. Scapular tenderness
    7. Rapid deceleration mechanism (fall >20 feet or MVA >40 mph)
    
    If ANY criteria are positive, major or minor thoracic injury cannot be excluded 
    and CT chest should be considered.
    
    References (Vancouver style):
    1. Rodriguez RM, Langdorf MI, Nishijima D, Baumann BM, Hendey GW, Medak AJ, et al. 
    Derivation and validation of two decision instruments for selective chest CT in 
    blunt trauma: a multicenter prospective observational study (NEXUS Chest CT). 
    PLoS Med. 2015 Oct 6;12(10):e1001883. doi: 10.1371/journal.pmed.1001883.
    """
    
    abnormal_chest_xray: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have an abnormal chest X-ray showing any thoracic injury or widened mediastinum? Scores 1 if yes",
        example="no"
    )
    
    distracting_injury: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have a distracting painful injury? Any injury that may distract from chest pain or tenderness. Scores 1 if yes",
        example="no"
    )
    
    chest_wall_tenderness: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have tenderness to palpation of the chest wall? Scores 1 if yes",
        example="no"
    )
    
    sternal_tenderness: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have tenderness to palpation of the sternum? Scores 1 if yes",
        example="no"
    )
    
    thoracic_spine_tenderness: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have tenderness to palpation of the thoracic spine? Scores 1 if yes",
        example="no"
    )
    
    scapular_tenderness: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have tenderness to palpation of the scapula? Scores 1 if yes",
        example="no"
    )
    
    rapid_deceleration: Literal["yes", "no"] = Field(
        ...,
        description="Was there a rapid deceleration mechanism? Fall from >20 feet (>6 meters) OR motor vehicle accident >40 mph (>64 km/hour) with sudden deceleration. Scores 1 if yes",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "abnormal_chest_xray": "no",
                "distracting_injury": "no",
                "chest_wall_tenderness": "no",
                "sternal_tenderness": "no",
                "thoracic_spine_tenderness": "no",
                "scapular_tenderness": "no",
                "rapid_deceleration": "no"
            }
        }


class NexusChestCtResponse(BaseModel):
    """
    Response model for NEXUS Chest CT Decision Instrument
    
    The score represents the number of positive criteria (0-7):
    - 0 criteria: Low risk - CT chest not indicated (NPV 98.7%)
    - ≥1 criteria: CT indicated - Consider CT chest (Sensitivity 99.0%)
    
    This rule is 100% sensitive for aortic and great vessel injuries.
    
    Reference: Rodriguez RM, et al. PLoS Med. 2015;12(10):e1001883.
    """
    
    result: int = Field(
        ...,
        description="Number of positive NEXUS Chest CT criteria (range: 0-7)",
        example=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="criteria present"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommendation based on the score",
        example="No NEXUS Chest CT criteria are present. Major or minor thoracic injury can be excluded without CT chest imaging. The negative predictive value is 98.7% for all thoracic injuries."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low risk or CT indicated)",
        example="Low risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the recommendation",
        example="CT chest not indicated"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 0,
                "unit": "criteria present",
                "interpretation": "No NEXUS Chest CT criteria are present. Major or minor thoracic injury can be excluded without CT chest imaging. The negative predictive value is 98.7% for all thoracic injuries.",
                "stage": "Low risk",
                "stage_description": "CT chest not indicated"
            }
        }