"""
FOUR (Full Outline of UnResponsiveness) Score Models

Request and response models for FOUR Score calculation.

References (Vancouver style):
1. Wijdicks EF, Bamlet WR, Maramattom BV, Manno EM, McClelland RL. Validation of a new 
   coma scale: The FOUR score. Ann Neurol. 2005;58(4):585-93. doi: 10.1002/ana.20611.
2. Wolf CA, Wijdicks EF, Bamlet WR, McClelland RL. Further validation of the FOUR score 
   coma scale by intensive care unit nurses. Mayo Clin Proc. 2007;82(4):435-8. 
   doi: 10.4065/82.4.435.
3. Stead LG, Wijdicks EF, Bhagra A, et al. Validation of a new coma scale, the FOUR score, 
   in the emergency department. Neurocrit Care. 2009;10(1):50-4. 
   doi: 10.1007/s12028-008-9145-0.
4. Kramer AA, Wijdicks EF, Snavely VL, et al. A multicenter prospective study of 
   interobserver agreement using the Full Outline of UnResponsiveness score coma scale 
   in the intensive care unit. Crit Care Med. 2012;40(9):2671-6. 
   doi: 10.1097/CCM.0b013e318258fd85.

The FOUR (Full Outline of UnResponsiveness) Score is a neurological assessment tool 
developed by Dr. Eelco F.M. Wijdicks to evaluate consciousness level in comatose patients. 
It addresses limitations of the Glasgow Coma Scale and provides more detailed assessment 
of neurological function through four distinct components.

The FOUR Score consists of four components, each scored from 0-4 points:

1. **Eye Response (E)**: Assesses eyelid opening and tracking ability
   - 4: Eyelids open, tracking, or blinking to command
   - 3: Eyelids open but not tracking
   - 2: Eyelids closed but open to loud voice
   - 1: Eyelids closed but open to pain
   - 0: Eyelids remain closed with pain

2. **Motor Response (M)**: Evaluates upper extremity motor function
   - 4: Thumbs-up, fist, or peace sign
   - 3: Localizing to pain
   - 2: Flexion response to pain
   - 1: Extension response to pain
   - 0: No response to pain or generalized myoclonus

3. **Brainstem Reflexes (B)**: Assesses brainstem function
   - 4: Pupil and corneal reflexes present
   - 3: One pupil wide and fixed
   - 2: Pupil OR corneal reflex absent
   - 1: Pupil AND corneal reflexes absent
   - 0: Absent pupil, corneal, and cough reflexes

4. **Respiration Pattern (R)**: Evaluates breathing patterns
   - 4: Not intubated, regular breathing
   - 3: Not intubated, Cheyne-Stokes breathing
   - 2: Not intubated, irregular breathing
   - 1: Breathes above ventilatory rate
   - 0: Breathes at ventilator rate or apnea

Clinical Application:
- More accurate than Glasgow Coma Scale, particularly for lowest GCS scores
- Identifies impending neurological decline
- Provides objective neurological assessment
- High inter-rater reliability among healthcare providers
- Validated in emergency department, ICU, and neurological care settings

Advantages over GCS:
- Addresses limitations of GCS in intubated patients
- Includes brainstem reflex assessment
- Better prognostic accuracy
- More detailed evaluation of neurological function
"""

from pydantic import BaseModel, Field
from typing import Literal


class FourScoreRequest(BaseModel):
    """
    Request model for FOUR (Full Outline of UnResponsiveness) Score
    
    The FOUR Score evaluates consciousness level through four components, each scored 
    from 0-4 points, with higher scores indicating better neurological function.
    
    **Component Descriptions:**
    
    **Eye Response (E4-E0):**
    - **E4**: Eyelids open, tracking, or blinking to command (best response)
    - **E3**: Eyelids open but not tracking
    - **E2**: Eyelids closed but open to loud voice
    - **E1**: Eyelids closed but open to pain
    - **E0**: Eyelids remain closed with pain (worst response)
    
    **Motor Response (M4-M0):**
    - **M4**: Thumbs-up, fist, or peace sign (best response)
    - **M3**: Localizing to pain
    - **M2**: Flexion response to pain
    - **M1**: Extension response to pain
    - **M0**: No response to pain or generalized myoclonus (worst response)
    
    **Brainstem Reflexes (B4-B0):**
    - **B4**: Pupil and corneal reflexes present (best response)
    - **B3**: One pupil wide and fixed
    - **B2**: Pupil OR corneal reflex absent
    - **B1**: Pupil AND corneal reflexes absent
    - **B0**: Absent pupil, corneal, and cough reflexes (worst response)
    
    **Respiration Pattern (R4-R0):**
    - **R4**: Not intubated, regular breathing (best response)
    - **R3**: Not intubated, Cheyne-Stokes breathing
    - **R2**: Not intubated, irregular breathing
    - **R1**: Breathes above ventilatory rate
    - **R0**: Breathes at ventilator rate or apnea (worst response)
    
    **Total Score Interpretation:**
    - **0-4 points**: Very severe coma (poor prognosis)
    - **5-8 points**: Severe coma (guarded prognosis)
    - **9-12 points**: Moderate coma (variable prognosis)
    - **13-16 points**: Mild impairment (better prognosis)

    References (Vancouver style):
    1. Wijdicks EF, Bamlet WR, Maramattom BV, Manno EM, McClelland RL. Validation of a new 
       coma scale: The FOUR score. Ann Neurol. 2005;58(4):585-93.
    2. Wolf CA, Wijdicks EF, Bamlet WR, McClelland RL. Further validation of the FOUR score 
       coma scale by intensive care unit nurses. Mayo Clin Proc. 2007;82(4):435-8.
    3. Stead LG, Wijdicks EF, Bhagra A, et al. Validation of a new coma scale, the FOUR score, 
       in the emergency department. Neurocrit Care. 2009;10(1):50-4.
    """
    
    eye_response: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description=(
            "Eye response component (0-4 points). "
            "4: Eyelids open, tracking, or blinking to command. "
            "3: Eyelids open but not tracking. "
            "2: Eyelids closed but open to loud voice. "
            "1: Eyelids closed but open to pain. "
            "0: Eyelids remain closed with pain."
        ),
        example=3
    )
    
    motor_response: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description=(
            "Motor response of upper extremities (0-4 points). "
            "4: Thumbs-up, fist, or peace sign. "
            "3: Localizing to pain. "
            "2: Flexion response to pain. "
            "1: Extension response to pain. "
            "0: No response to pain or generalized myoclonus."
        ),
        example=2
    )
    
    brainstem_reflexes: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description=(
            "Brainstem reflexes assessment (0-4 points). "
            "4: Pupil and corneal reflexes present. "
            "3: One pupil wide and fixed. "
            "2: Pupil OR corneal reflex absent. "
            "1: Pupil AND corneal reflexes absent. "
            "0: Absent pupil, corneal, and cough reflexes."
        ),
        example=2
    )
    
    respiration_pattern: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description=(
            "Respiration pattern assessment (0-4 points). "
            "4: Not intubated, regular breathing. "
            "3: Not intubated, Cheyne-Stokes breathing. "
            "2: Not intubated, irregular breathing. "
            "1: Breathes above ventilatory rate. "
            "0: Breathes at ventilator rate or apnea."
        ),
        example=1
    )
    
    class Config:
        schema_extra = {
            "example": {
                "eye_response": 3,
                "motor_response": 2,
                "brainstem_reflexes": 2,
                "respiration_pattern": 1
            }
        }


class FourScoreResponse(BaseModel):
    """
    Response model for FOUR (Full Outline of UnResponsiveness) Score
    
    The FOUR Score provides a comprehensive assessment of consciousness level with 
    better prognostic accuracy than the Glasgow Coma Scale, particularly for patients 
    with severe neurological impairment.
    
    **Score Interpretation:**
    - **Total Score Range**: 0-16 points (sum of four components)
    - **Higher Scores**: Better neurological function and prognosis
    - **Lower Scores**: More severe impairment and worse prognosis
    
    **Prognostic Categories:**
    - **Very Severe Coma (0-4)**: Profound impairment, poor prognosis, high mortality
    - **Severe Coma (5-8)**: Significant impairment, guarded prognosis, intensive care needed
    - **Moderate Coma (9-12)**: Variable function, prognosis depends on etiology and treatment
    - **Mild Impairment (13-16)**: Preserved function, better prognosis, potential for recovery
    
    **Clinical Applications:**
    - Neurological assessment and monitoring
    - Prognostic evaluation and family counseling
    - Treatment planning and resource allocation
    - Research and quality improvement initiatives
    - Communication among healthcare providers
    
    **Key Advantages over GCS:**
    - More detailed assessment of brainstem function
    - Better evaluation of intubated patients
    - Higher inter-rater reliability
    - Superior prognostic accuracy
    - Identification of impending neurological decline
    
    Reference: Wijdicks EF, et al. Ann Neurol. 2005;58(4):585-93.
    """
    
    result: int = Field(
        ...,
        description="Total FOUR Score calculated from all four components (range: 0-16 points)",
        ge=0,
        le=16,
        example=8
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including severity assessment, prognosis, and management recommendations",
        example="FOUR Score: 8/16. Severe coma with significant neurological impairment. Substantial brainstem dysfunction present. Guarded prognosis requiring intensive care and frequent neurological assessment."
    )
    
    stage: str = Field(
        ...,
        description="Severity category based on the total score (Very Severe Coma, Severe Coma, Moderate Coma, Mild Impairment)",
        example="Severe Coma"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the severity category",
        example="Severe impairment of consciousness"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 8,
                "unit": "points",
                "interpretation": "FOUR Score: 8/16. Severe coma with significant neurological impairment. Substantial brainstem dysfunction present. Guarded prognosis requiring intensive care and frequent neurological assessment.",
                "stage": "Severe Coma",
                "stage_description": "Severe impairment of consciousness"
            }
        }