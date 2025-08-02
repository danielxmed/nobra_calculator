"""
HINTS for Stroke in Acute Vestibular Syndrome Models

Request and response models for HINTS examination calculation.

References (Vancouver style):
1. Kattah JC, Talkad AV, Wang DZ, Hsieh YH, Newman-Toker DE. HINTS to diagnose 
   stroke in the acute vestibular syndrome: three-step bedside oculomotor 
   examination more sensitive than early MRI diffusion-weighted imaging. 
   Stroke. 2009 Nov;40(11):3504-10. doi: 10.1161/STROKEAHA.109.551234.
2. Newman-Toker DE, Kerber KA, Hsieh YH, Pula JH, Omron R, Saber Tehrani AS, 
   et al. HINTS outperforms ABCD2 to screen for stroke in acute continuous 
   vertigo and dizziness. Acad Emerg Med. 2013 Oct;20(10):986-96. 
   doi: 10.1111/acem.12223.
3. Kerber KA, Burke JF, Brown DL, Meurer WJ, Smith MA, Lisabeth LD, et al. 
   Stroke risk stratification in acute dizziness presentations: A prospective 
   imaging-based study. Neurology. 2015 Nov 24;85(21):1869-78. 
   doi: 10.1212/WNL.0000000000002141.

The HINTS examination is a three-step bedside oculomotor assessment that helps 
differentiate between peripheral and central causes of acute vestibular syndrome (AVS), 
with particular emphasis on identifying posterior circulation strokes. It has been 
shown to be more sensitive than early MRI diffusion-weighted imaging for detecting 
posterior circulation strokes.
"""

from pydantic import BaseModel, Field
from typing import Literal


class HintsRequest(BaseModel):
    """
    Request model for HINTS (Head Impulse, Nystagmus, Test of Skew) examination
    
    The HINTS exam consists of three components performed at the bedside:
    
    1. Head Impulse Test (h-HIT):
       - Tests the vestibulo-ocular reflex (VOR)
       - Normal h-HIT (no corrective saccade) suggests central pathology
       - Abnormal h-HIT (corrective saccade present) suggests peripheral pathology
    
    2. Nystagmus:
       - Direction-fixed horizontal nystagmus suggests peripheral pathology
       - Direction-changing horizontal nystagmus suggests central pathology
       - Vertical or torsional nystagmus always suggests central pathology
    
    3. Test of Skew:
       - Tests for vertical ocular misalignment
       - Absent skew deviation suggests peripheral pathology
       - Present skew deviation suggests central pathology
    
    Important Notes:
    - Only applicable for continuous vertigo lasting >24 hours
    - Not for episodic vertigo or dizziness
    - Requires patient cooperation for all three tests
    - Any "not testable" finding should raise concern for central cause
    
    References (Vancouver style):
    1. Kattah JC, Talkad AV, Wang DZ, Hsieh YH, Newman-Toker DE. HINTS to diagnose 
       stroke in the acute vestibular syndrome: three-step bedside oculomotor 
       examination more sensitive than early MRI diffusion-weighted imaging. 
       Stroke. 2009 Nov;40(11):3504-10.
    2. Newman-Toker DE, Kerber KA, Hsieh YH, Pula JH, Omron R, Saber Tehrani AS, 
       et al. HINTS outperforms ABCD2 to screen for stroke in acute continuous 
       vertigo and dizziness. Acad Emerg Med. 2013 Oct;20(10):986-96.
    """
    
    head_impulse_test: Literal["normal", "abnormal", "not_testable"] = Field(
        ...,
        description="Head Impulse Test (h-HIT) result. 'normal' means no corrective saccade "
                    "(concerning for central cause), 'abnormal' means corrective saccade present "
                    "(suggests peripheral cause), 'not_testable' if patient cannot cooperate or "
                    "test cannot be performed (concerning for central cause).",
        example="abnormal"
    )
    
    nystagmus: Literal["direction_fixed", "direction_changing", "not_testable"] = Field(
        ...,
        description="Nystagmus observation pattern. 'direction_fixed' means horizontal nystagmus "
                    "that beats in the same direction regardless of gaze direction (suggests "
                    "peripheral cause), 'direction_changing' means nystagmus that changes direction "
                    "with gaze or includes vertical/torsional components (suggests central cause), "
                    "'not_testable' if cannot be assessed (concerning for central cause).",
        example="direction_fixed"
    )
    
    test_of_skew: Literal["absent", "present", "not_testable"] = Field(
        ...,
        description="Test of Skew result - presence of vertical ocular misalignment. 'absent' "
                    "means no vertical misalignment when covering/uncovering eyes (suggests "
                    "peripheral cause), 'present' means vertical misalignment detected (suggests "
                    "central cause), 'not_testable' if cannot be assessed (concerning for "
                    "central cause).",
        example="absent"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "head_impulse_test": "abnormal",
                "nystagmus": "direction_fixed",
                "test_of_skew": "absent"
            }
        }


class HintsResponse(BaseModel):
    """
    Response model for HINTS examination
    
    The HINTS exam interpretation is binary:
    - Benign HINTS: All three findings suggest peripheral cause
    - Dangerous HINTS: One or more findings suggest central cause
    
    Clinical Significance:
    - Benign HINTS has high negative predictive value for stroke
    - Dangerous HINTS requires urgent neuroimaging and stroke evaluation
    - HINTS is more sensitive than early MRI for posterior circulation stroke
    - Early MRI diffusion-weighted imaging may be falsely negative in up to 20% 
      of posterior circulation strokes in the first 48 hours
    
    Reference: Kattah JC, et al. Stroke. 2009;40(11):3504-10.
    """
    
    result: str = Field(
        ...,
        description="HINTS examination pattern (Benign HINTS or Dangerous HINTS)",
        example="Benign HINTS"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="pattern"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the HINTS pattern with recommendations",
        example="Pattern consistent with peripheral vestibular disorder. All three findings point to peripheral etiology: abnormal head impulse test, direction-fixed horizontal nystagmus, and absent skew deviation. Consider vestibular neuritis or labyrinthitis."
    )
    
    stage: str = Field(
        ...,
        description="HINTS classification (Benign HINTS or Dangerous HINTS)",
        example="Benign HINTS"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the likely etiology",
        example="Suggests peripheral cause"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Benign HINTS",
                "unit": "pattern",
                "interpretation": "Pattern consistent with peripheral vestibular disorder. All three findings point to peripheral etiology: abnormal head impulse test, direction-fixed horizontal nystagmus, and absent skew deviation. Consider vestibular neuritis or labyrinthitis.",
                "stage": "Benign HINTS",
                "stage_description": "Suggests peripheral cause"
            }
        }