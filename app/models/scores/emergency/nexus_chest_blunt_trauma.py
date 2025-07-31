"""
NEXUS Chest Decision Instrument for Blunt Chest Trauma Models

Request and response models for NEXUS Chest calculation.

References (Vancouver style):
1. Rodriguez RM, Hendey GW, Mower W, Kea B, Fortman J, Merchant G, et al. 
   Derivation of a decision instrument for selective chest radiography in blunt 
   trauma. J Trauma. 2011 Sep;71(3):549-53. doi: 10.1097/TA.0b013e3181f2ac9d.
2. Rodriguez RM, Anglin D, Langdorf MI, Baumann BM, Hendey GW, Bradley RN, et al. 
   NEXUS chest: validation of a decision instrument for selective chest imaging in 
   blunt trauma. JAMA Surg. 2013 Oct;148(10):940-6. doi: 10.1001/jamasurg.2013.2757.
3. Rodriguez RM, Hendey GW, Marek G, Dery RA, Bjoring A. A pilot study to derive 
   clinical variables for selective chest radiography in blunt trauma patients. 
   Ann Emerg Med. 2006 May;47(5):415-8. doi: 10.1016/j.annemergmed.2005.10.001.

The NEXUS Chest Decision Instrument uses 7 criteria to determine which blunt trauma 
patients require chest imaging. With 99% sensitivity for clinically significant 
thoracic injury, it can safely reduce unnecessary imaging and radiation exposure.
"""

from pydantic import BaseModel, Field
from typing import Literal


class NexusChestBluntTraumaRequest(BaseModel):
    """
    Request model for NEXUS Chest Decision Instrument for Blunt Chest Trauma
    
    The NEXUS Chest evaluates 7 criteria to identify patients at very low risk for 
    thoracic injury who can potentially avoid chest imaging:
    
    1. Age > 60 years
    2. Rapid deceleration mechanism (fall > 20 ft or MVC > 40 mph)
    3. Chest pain
    4. Intoxication
    5. Altered mental status
    6. Distracting painful injury
    7. Tenderness to chest wall palpation
    
    If ALL criteria are absent (score = 0), chest imaging can potentially be avoided.
    
    References (Vancouver style):
    1. Rodriguez RM, Hendey GW, Mower W, Kea B, Fortman J, Merchant G, et al. 
    Derivation of a decision instrument for selective chest radiography in blunt 
    trauma. J Trauma. 2011 Sep;71(3):549-53. doi: 10.1097/TA.0b013e3181f2ac9d.
    2. Rodriguez RM, Anglin D, Langdorf MI, Baumann BM, Hendey GW, Bradley RN, et al. 
    NEXUS chest: validation of a decision instrument for selective chest imaging in 
    blunt trauma. JAMA Surg. 2013 Oct;148(10):940-6. doi: 10.1001/jamasurg.2013.2757.
    """
    
    age_over_60: Literal["yes", "no"] = Field(
        ...,
        description="Is the patient older than 60 years? Scores 1 point if yes",
        example="no"
    )
    
    rapid_deceleration: Literal["yes", "no"] = Field(
        ...,
        description="Was there a rapid deceleration mechanism? Fall from >20 feet (>6 meters) OR motor vehicle crash >40 mph (>64 km/h). Scores 1 point if yes",
        example="no"
    )
    
    chest_pain: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have chest pain? Scores 1 point if yes",
        example="no"
    )
    
    intoxication: Literal["yes", "no"] = Field(
        ...,
        description="Is the patient intoxicated (alcohol or drugs)? Scores 1 point if yes",
        example="no"
    )
    
    altered_mental_status: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have altered mental status (altered alertness/cognition)? Scores 1 point if yes",
        example="no"
    )
    
    distracting_injury: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have a distracting painful injury? Any injury that may distract from chest symptoms. Scores 1 point if yes",
        example="no"
    )
    
    chest_wall_tenderness: Literal["yes", "no"] = Field(
        ...,
        description="Does the patient have tenderness to chest wall palpation? Scores 1 point if yes",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age_over_60": "no",
                "rapid_deceleration": "no",
                "chest_pain": "no",
                "intoxication": "no",
                "altered_mental_status": "no",
                "distracting_injury": "no",
                "chest_wall_tenderness": "no"
            }
        }


class NexusChestBluntTraumaResponse(BaseModel):
    """
    Response model for NEXUS Chest Decision Instrument for Blunt Chest Trauma
    
    The score ranges from 0 to 7 points:
    - 0 points: Very low risk - Consider no imaging (NPV 98.5% for thoracic injury, 99.9% for major injury)
    - ≥1 point: Not low risk - Consider chest imaging (99% sensitive for clinically significant injury)
    
    In well-appearing patients with positive criteria, consider chest x-ray only.
    In ill-appearing patients or those with multi-organ injury, consider chest CT.
    
    Reference: Rodriguez RM, et al. JAMA Surg. 2013;148(10):940-6.
    """
    
    result: int = Field(
        ...,
        description="NEXUS Chest score calculated from clinical criteria (range: 0-7 points)",
        example=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommendation based on the score",
        example="No NEXUS Chest criteria are present. This patient is at very low risk for thoracic injury. Chest imaging can potentially be avoided. The negative predictive value is 98.5% for thoracic injury and 99.9% for clinically major injury."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Very low risk or Not low risk)",
        example="Very low risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the recommendation",
        example="Consider no imaging"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "No NEXUS Chest criteria are present. This patient is at very low risk for thoracic injury. Chest imaging can potentially be avoided. The negative predictive value is 98.5% for thoracic injury and 99.9% for clinically major injury.",
                "stage": "Very low risk",
                "stage_description": "Consider no imaging"
            }
        }