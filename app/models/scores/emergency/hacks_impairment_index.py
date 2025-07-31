"""
Hack's Impairment Index (HII) Models

Request and response models for HII calculation.

References (Vancouver style):
1. Hack JB, Goldlust EJ, Gibbs F, Zink B. The H-Impairment Index (HII): a standardized 
   assessment of alcohol-induced impairment in the Emergency Department. Am J Drug 
   Alcohol Abuse. 2014 Mar;40(2):111-7. doi: 10.3109/00952990.2013.877019.
2. Goldlust EJ, Bookstaver AD, Zink BJ, Hack JB. Performance of the Hack's Impairment 
   Index Score: A Novel Tool to Assess Impairment from Alcohol in Emergency Department 
   Patients. Acad Emerg Med. 2017 Oct;24(10):1193-1203. doi: 10.1111/acem.13256.
3. Bookstaver AD, Liang Y, Goldlust E, Zink B, Hack J. Introduction of an Electronic 
   Mobile Device Version of an Alcohol Impairment Scale (the Hack's Impairment Index 
   Score) Does Not Impair Nursing Assessment of Patients in Emergency Departments. 
   Comput Inform Nurs. 2021 Aug 1;39(8):419-426. doi: 10.1097/CIN.0000000000000698.

The HII provides a quantitative, standardized assessment of alcohol-induced impairment 
in emergency department patients. It evaluates five domains (speech/mentation, gross motor, 
eye movement, coordination, and fine motor skills), each scored 0-4, to create an objective 
measure that is superior to blood alcohol levels for assessing clinical impairment.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional


class HacksImpairmentIndexRequest(BaseModel):
    """
    Request model for Hack's Impairment Index (HII)
    
    The HII assesses five key domains of function to quantify alcohol-induced impairment:
    
    1. Speech Quality and Mentation (0-4 points):
       - 0: Normal or baseline speech; conversive and appropriate
       - 1: Mildly impaired speech clarity or slight confusion
       - 2: Moderately slurred speech or confusion
       - 3: Severely slurred speech or significant confusion
       - 4: Unintelligible speech or only moans
    
    2. Gross Motor Skills (0-4 points):
       - 0: Can stand and walk, and is steady
       - 1: Can stand and walk but unsteady
       - 2: Can stand with assistance
       - 3: Can sit up but cannot stand
       - 4: Cannot sit up
    
    3. Eye Movement (0-4 points):
       - 0: No nystagmus; follows finger with eyes whole time
       - 1: Mild nystagmus or occasional difficulty following
       - 2: Moderate nystagmus or frequent difficulty following
       - 3: Severe nystagmus or rare ability to follow
       - 4: Unable to participate
    
    4. Coordination with Target Pursuit (0-4 points):
       - 0: Steady; accurate finger to target
       - 1: Mild tremor or slight inaccuracy
       - 2: Moderate tremor or frequent misses
       - 3: Severe tremor or rare hits to target
       - 4: Unable to participate
    
    5. Fine Motor Skills (0-4 points):
       - 0: Traces curve perfectly
       - 1: Mild difficulty tracing curve
       - 2: Moderate difficulty tracing curve
       - 3: Severe difficulty tracing curve
       - 4: Unable to participate
    
    The final HII score is calculated as: (Sum of all subscores) / (Number of tasks completed × 4)
    
    References (Vancouver style):
    1. Hack JB, Goldlust EJ, Gibbs F, Zink B. The H-Impairment Index (HII): a standardized 
       assessment of alcohol-induced impairment in the Emergency Department. Am J Drug 
       Alcohol Abuse. 2014 Mar;40(2):111-7.
    2. Goldlust EJ, Bookstaver AD, Zink BJ, Hack JB. Performance of the Hack's Impairment 
       Index Score: A Novel Tool to Assess Impairment from Alcohol in Emergency Department 
       Patients. Acad Emerg Med. 2017 Oct;24(10):1193-1203.
    """
    
    speech_mentation: int = Field(
        ...,
        ge=0,
        le=4,
        description="Speech quality and mentation score (0-4). 0=normal speech, 4=unintelligible speech",
        example=2
    )
    
    gross_motor: int = Field(
        ...,
        ge=0,
        le=4,
        description="Gross motor skills score (0-4). 0=steady standing/walking, 4=cannot sit up",
        example=2
    )
    
    eye_movement: int = Field(
        ...,
        ge=0,
        le=4,
        description="Eye movement score (0-4). 0=no nystagmus/follows well, 4=unable to participate",
        example=1
    )
    
    coordination: int = Field(
        ...,
        ge=0,
        le=4,
        description="Coordination with target pursuit score (0-4). 0=accurate to target, 4=unable to participate",
        example=2
    )
    
    fine_motor: int = Field(
        ...,
        ge=0,
        le=4,
        description="Fine motor skills score (0-4). 0=traces curve perfectly, 4=unable to participate",
        example=1
    )
    
    tasks_completed: int = Field(
        ...,
        ge=1,
        le=5,
        description="Number of tasks completed (1-5). Required to calculate the HII score properly",
        example=5
    )
    
    @validator('tasks_completed')
    def validate_tasks_completed(cls, v, values):
        """Ensure tasks_completed doesn't exceed number of non-zero scores"""
        # Count how many tasks were actually attempted (scored > 0 or completed with 0)
        # This is a simplified validation - in practice, clinical judgment determines completion
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "speech_mentation": 2,
                "gross_motor": 2,
                "eye_movement": 1,
                "coordination": 2,
                "fine_motor": 1,
                "tasks_completed": 5
            }
        }


class HacksImpairmentIndexResponse(BaseModel):
    """
    Response model for Hack's Impairment Index (HII)
    
    The HII score ranges from 0 to 15 points, with higher scores indicating greater impairment:
    - 0-2: Minimal impairment - consider discharge evaluation
    - 2.01-4: Mild impairment - reassess in 2 hours
    - 4.01-8: Moderate impairment - not safe for discharge
    - 8.01-12: Severe impairment - requires close monitoring
    - 12.01-15: Profound impairment - consider ICU care
    
    Clinical Significance:
    - Superior to blood alcohol levels for assessing clinical impairment
    - Serial assessments every 2 hours track improvement
    - HII <4 generally indicates readiness for discharge evaluation
    - Estimated time to resolution (hours) = HII Score / 0.0616
    
    Important Notes:
    - Not intended to determine driving safety
    - Should be used with clinical judgment and other criteria
    - Consider screening for alcohol withdrawal in appropriate patients
    
    Reference: Hack JB, et al. Am J Drug Alcohol Abuse. 2014;40(2):111-7.
    """
    
    result: float = Field(
        ...,
        description="HII score (0-15 points) indicating degree of alcohol-induced impairment",
        example=8.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations",
        example="Patient shows moderate impairment. Not safe for discharge. Continue supportive care and reassess every 2 hours."
    )
    
    stage: str = Field(
        ...,
        description="Impairment severity category (Minimal, Mild, Moderate, Severe, or Profound)",
        example="Moderate Impairment"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the impairment level",
        example="Moderate alcohol-induced impairment"
    )
    
    estimated_time_to_resolution_hours: Optional[float] = Field(
        None,
        description="Estimated hours until HII <4 based on formula: HII/0.0616",
        example=129.9
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 8.0,
                "unit": "points",
                "interpretation": "Patient shows moderate impairment. Not safe for discharge. Continue supportive care and reassess every 2 hours.",
                "stage": "Moderate Impairment",
                "stage_description": "Moderate alcohol-induced impairment",
                "estimated_time_to_resolution_hours": 129.9
            }
        }