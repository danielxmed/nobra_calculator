"""
APGAR Score Models

Request and response models for APGAR Score calculation.

References (Vancouver style):
1. Apgar V. A proposal for a new method of evaluation of the newborn infant. 
   Curr Res Anesth Analg. 1953;32(4):260-267.
2. Apgar V, Holaday DA, James LS, Weisbrot IM, Berrien C. Evaluation of the 
   newborn infant; second report. J Am Med Assoc. 1958;168(15):1985-1988.
3. American College of Obstetricians and Gynecologists Committee on Obstetric Practice. 
   The Apgar Score. Committee Opinion No. 644. Obstet Gynecol. 2015;126:e52-55.

The APGAR Score is a quick method for assessing the health of newborn infants 
immediately after birth and their need for resuscitation. It was developed by 
Dr. Virginia Apgar in 1952 at Columbia University. The score evaluates five 
criteria: Activity (muscle tone), Pulse (heart rate), Grimace (reflex irritability), 
Appearance (skin color), and Respirations (breathing effort). Each criterion is 
scored 0, 1, or 2, for a total possible score of 10.

The assessment is typically performed at 1 and 5 minutes after birth, with 
additional assessments every 5 minutes until 20 minutes if the 5-minute score 
is less than 7. The score helps healthcare providers quickly identify newborns 
who need immediate medical attention or resuscitation.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ApgarScoreRequest(BaseModel):
    """
    Request model for APGAR Score calculation
    
    The APGAR Score evaluates five clinical criteria to assess neonatal vitality:
    
    Activity/Muscle Tone:
    - active: Active motion, flexed arms and legs (2 points)
    - some_flexion: Some flexion of extremities (1 point)  
    - limp: Limp, no movement (0 points)
    
    Pulse (Heart Rate):
    - >=100_bpm: Heart rate ≥100 beats per minute (2 points)
    - <100_bpm: Heart rate <100 beats per minute (1 point)
    - absent: No heart rate detected (0 points)
    
    Grimace (Reflex Irritability):
    - sneeze_cough: Vigorous response (sneeze, cough, pull away) (2 points)
    - grimace: Facial grimace only (1 point)
    - none: No response to stimulation (0 points)
    
    Appearance (Skin Color):
    - all_pink: Completely pink (2 points)
    - blue_extremities: Pink body, blue extremities (acrocyanosis) (1 point)
    - blue_pale: Blue or pale all over (0 points)
    
    Respirations (Breathing Effort):
    - good_crying: Good, strong cry; normal breathing (2 points)
    - irregular_slow: Weak cry, irregular breathing (1 point)
    - absent: No breathing effort (0 points)

    References (Vancouver style):
    1. Apgar V. A proposal for a new method of evaluation of the newborn infant. 
    Curr Res Anesth Analg. 1953;32(4):260-267.
    2. Apgar V, Holaday DA, James LS, Weisbrot IM, Berrien C. Evaluation of the 
    newborn infant; second report. J Am Med Assoc. 1958;168(15):1985-1988.
    3. American College of Obstetricians and Gynecologists Committee on Obstetric Practice. 
    The Apgar Score. Committee Opinion No. 644. Obstet Gynecol. 2015;126:e52-55.
    """
    
    activity_muscle_tone: Literal["active", "some_flexion", "limp"] = Field(
        ...,
        description="Assessment of muscle tone and activity. Active motion scores 2 points, some flexion scores 1 point, limp scores 0 points",
        example="active"
    )
    
    pulse: Literal[">=100_bpm", "<100_bpm", "absent"] = Field(
        ...,
        description="Heart rate assessment. ≥100 bpm scores 2 points, <100 bpm scores 1 point, absent scores 0 points",
        example=">=100_bpm"
    )
    
    grimace_reflex: Literal["sneeze_cough", "grimace", "none"] = Field(
        ...,
        description="Reflex irritability/grimace response to stimulation. Vigorous response (sneeze/cough) scores 2 points, grimace only scores 1 point, no response scores 0 points",
        example="sneeze_cough"
    )
    
    appearance_color: Literal["all_pink", "blue_extremities", "blue_pale"] = Field(
        ...,
        description="Skin color assessment. All pink scores 2 points, pink body with blue extremities scores 1 point, blue/pale all over scores 0 points",
        example="blue_extremities"
    )
    
    respirations: Literal["good_crying", "irregular_slow", "absent"] = Field(
        ...,
        description="Respiratory effort assessment. Good/strong cry scores 2 points, weak/irregular breathing scores 1 point, no breathing scores 0 points",
        example="good_crying"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "activity_muscle_tone": "active",
                "pulse": ">=100_bpm",
                "grimace_reflex": "sneeze_cough",
                "appearance_color": "blue_extremities",
                "respirations": "good_crying"
            }
        }


class ApgarScoreResponse(BaseModel):
    """
    Response model for APGAR Score calculation
    
    The APGAR score ranges from 0 to 10 points and classifies neonatal condition:
    - 7-10 points: Normal condition, reassuring
    - 4-6 points: Moderate distress, may need assistance
    - 0-3 points: Severe distress, immediate medical attention required
    
    The score should be assessed at 1 and 5 minutes after birth, with additional 
    assessments every 5 minutes up to 20 minutes if the 5-minute score is <7.
    
    Reference: Apgar V. Curr Res Anesth Analg. 1953;32(4):260-267.
    """
    
    result: int = Field(
        ...,
        description="APGAR score calculated from the five clinical criteria (range: 0-10 points)",
        example=9
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended actions based on the score",
        example="Score 7-10 indicates good condition. The neonate is adapting well to extrauterine life. Scores of 8-9 are most common, as most newborns lose 1 point for blue extremities which is normal."
    )
    
    stage: str = Field(
        ...,
        description="Clinical condition category (Normal, Moderate Distress, Severe Distress)",
        example="Normal"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the clinical condition category",
        example="Normal condition - reassuring"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 9,
                "unit": "points",
                "interpretation": "Score 7-10 indicates good condition. The neonate is adapting well to extrauterine life. Scores of 8-9 are most common, as most newborns lose 1 point for blue extremities which is normal.",
                "stage": "Normal",
                "stage_description": "Normal condition - reassuring"
            }
        }
