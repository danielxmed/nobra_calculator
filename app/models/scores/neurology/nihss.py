"""
NIH Stroke Scale/Score (NIHSS) Models

Request and response models for NIHSS calculation.

References (Vancouver style):
1. Brott T, Adams HP Jr, Olinger CP, Marler JR, Barsan WG, Biller J, et al. 
   Measurements of acute cerebral infarction: a clinical examination scale. 
   Stroke. 1989 Jul;20(7):864-70. doi: 10.1161/01.str.20.7.864.
2. Lyden P, Brott T, Tilley B, Welch KM, Mascha EJ, Levine S, et al. 
   Improved reliability of the NIH Stroke Scale using video training. 
   NINDS TPA Stroke Study Group. Stroke. 1994 Nov;25(11):2220-6. 
   doi: 10.1161/01.str.25.11.2220.
3. Goldstein LB, Samsa GP. Reliability of the National Institutes of Health 
   Stroke Scale. Extension to non-neurologists in the context of a clinical trial. 
   Stroke. 1997 Feb;28(2):307-10. doi: 10.1161/01.str.28.2.307.

The NIH Stroke Scale (NIHSS) is a 15-item neurological examination stroke scale 
used to evaluate the effect of acute cerebral infarction on the levels of consciousness, 
language, neglect, visual-field loss, extraocular movement, motor strength, ataxia, 
dysarthria, and sensory loss. A trained observer rates the patient's ability to answer 
questions and perform activities. The scale ranges from 0 to 42, with higher scores 
indicating greater stroke severity.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class NihssRequest(BaseModel):
    """
    Request model for NIH Stroke Scale/Score (NIHSS)
    
    The NIHSS is a 15-item neurological examination used to quantify stroke severity:
    
    **Level of Consciousness (3 items):**
    - 1a. LOC Responsiveness: General alertness level
    - 1b. LOC Questions: Ability to answer month and age correctly
    - 1c. LOC Commands: Ability to follow simple commands (close eyes, make fist)
    
    **Neurological Function Items (12 items):**
    - Best Gaze: Horizontal eye movements
    - Visual Fields: Visual field testing
    - Facial Palsy: Facial symmetry and movement
    - Motor Function (4 items): Arm and leg strength bilaterally
    - Limb Ataxia: Coordination testing
    - Sensory: Response to pinprick
    - Language: Aphasia assessment
    - Dysarthria: Speech clarity
    - Extinction/Inattention: Neglect assessment
    
    Proper training in NIHSS administration is recommended. Free training available at:
    https://www.nihstrokescale.org/
    
    References (Vancouver style):
    1. Brott T, Adams HP Jr, Olinger CP, Marler JR, Barsan WG, Biller J, et al. 
       Measurements of acute cerebral infarction: a clinical examination scale. 
       Stroke. 1989 Jul;20(7):864-70. doi: 10.1161/01.str.20.7.864.
    2. Lyden P, Brott T, Tilley B, Welch KM, Mascha EJ, Levine S, et al. 
       Improved reliability of the NIH Stroke Scale using video training. 
       NINDS TPA Stroke Study Group. Stroke. 1994 Nov;25(11):2220-6. 
       doi: 10.1161/01.str.25.11.2220.
    """
    
    loc_responsiveness: Literal[0, 1, 2, 3] = Field(
        ...,
        description="1a. Level of consciousness. 0=Alert, keenly responsive; 1=Not alert, arousable by minor stimulation; 2=Not alert, requires repeated stimulation; 3=Unresponsive or responds only with reflexes",
        example=0
    )
    
    loc_questions: Literal[0, 1, 2] = Field(
        ...,
        description="1b. LOC questions (month and age). 0=Answers both correctly; 1=Answers one correctly; 2=Answers neither correctly",
        example=0
    )
    
    loc_commands: Literal[0, 1, 2] = Field(
        ...,
        description="1c. LOC commands (close eyes, make fist). 0=Performs both correctly; 1=Performs one correctly; 2=Performs neither correctly",
        example=0
    )
    
    best_gaze: Literal[0, 1, 2] = Field(
        ...,
        description="2. Best gaze (horizontal eye movements). 0=Normal; 1=Partial gaze palsy; 2=Forced deviation or total gaze paresis",
        example=0
    )
    
    visual_fields: Literal[0, 1, 2, 3] = Field(
        ...,
        description="3. Visual fields. 0=No visual loss; 1=Partial hemianopia; 2=Complete hemianopia; 3=Bilateral hemianopia or blindness",
        example=0
    )
    
    facial_palsy: Literal[0, 1, 2, 3] = Field(
        ...,
        description="4. Facial palsy. 0=Normal symmetrical movements; 1=Minor paralysis; 2=Partial paralysis; 3=Complete paralysis of one or both sides",
        example=0
    )
    
    motor_arm_left: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="5a. Motor arm - left. 0=No drift; 1=Drift; 2=Some effort against gravity; 3=No effort against gravity; 4=No movement",
        example=0
    )
    
    motor_arm_right: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="5b. Motor arm - right. 0=No drift; 1=Drift; 2=Some effort against gravity; 3=No effort against gravity; 4=No movement",
        example=0
    )
    
    motor_leg_left: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="6a. Motor leg - left. 0=No drift; 1=Drift; 2=Some effort against gravity; 3=No effort against gravity; 4=No movement",
        example=0
    )
    
    motor_leg_right: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="6b. Motor leg - right. 0=No drift; 1=Drift; 2=Some effort against gravity; 3=No effort against gravity; 4=No movement",
        example=0
    )
    
    limb_ataxia: Literal[0, 1, 2] = Field(
        ...,
        description="7. Limb ataxia. 0=Absent; 1=Present in one limb; 2=Present in two or more limbs",
        example=0
    )
    
    sensory: Literal[0, 1, 2] = Field(
        ...,
        description="8. Sensory. 0=Normal; 1=Mild-to-moderate sensory loss; 2=Severe to total sensory loss",
        example=0
    )
    
    best_language: Literal[0, 1, 2, 3] = Field(
        ...,
        description="9. Best language (aphasia). 0=No aphasia; 1=Mild-to-moderate aphasia; 2=Severe aphasia; 3=Mute, global aphasia",
        example=0
    )
    
    dysarthria: Literal[0, 1, 2] = Field(
        ...,
        description="10. Dysarthria. 0=Normal; 1=Mild-to-moderate dysarthria; 2=Severe dysarthria or mute/anarthric",
        example=0
    )
    
    extinction_inattention: Literal[0, 1, 2] = Field(
        ...,
        description="11. Extinction and inattention (neglect). 0=No abnormality; 1=Inattention or extinction to one modality; 2=Profound hemi-inattention or extinction to more than one modality",
        example=0
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "loc_responsiveness": 0,
                "loc_questions": 0,
                "loc_commands": 0,
                "best_gaze": 0,
                "visual_fields": 0,
                "facial_palsy": 0,
                "motor_arm_left": 0,
                "motor_arm_right": 0,
                "motor_leg_left": 0,
                "motor_leg_right": 0,
                "limb_ataxia": 0,
                "sensory": 0,
                "best_language": 0,
                "dysarthria": 0,
                "extinction_inattention": 0
            }
        }
    }


class NihssResponse(BaseModel):
    """
    Response model for NIH Stroke Scale/Score (NIHSS)
    
    The NIHSS score ranges from 0-42 points and classifies stroke severity:
    - 0: No stroke symptoms
    - 1-4: Minor stroke
    - 5-15: Moderate stroke
    - 16-20: Moderate to severe stroke
    - 21-42: Severe stroke
    
    The scale is widely used for:
    - Initial stroke assessment
    - Determining thrombolytic therapy eligibility
    - Monitoring neurological status
    - Predicting stroke outcomes
    - Research standardization
    
    Reference: Brott T, et al. Stroke. 1989;20(7):864-70.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=42,
        description="Total NIHSS score (sum of all 15 items), ranging from 0-42 points",
        example=5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the NIHSS score with treatment implications",
        example="Moderate stroke requiring urgent evaluation and treatment. May be eligible for thrombolytic therapy if within time window"
    )
    
    stage: str = Field(
        ...,
        description="Stroke severity classification",
        example="Moderate stroke"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the stroke severity category",
        example="Moderate stroke"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "result": 5,
                "unit": "points",
                "interpretation": "Moderate stroke requiring urgent evaluation and treatment. May be eligible for thrombolytic therapy if within time window",
                "stage": "Moderate stroke",
                "stage_description": "Moderate stroke"
            }
        }
    }