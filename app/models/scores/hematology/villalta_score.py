"""
Villalta Score for Post-thrombotic Syndrome (PTS) Models

Request and response models for Villalta Score calculation.

References (Vancouver style):
1. Villalta S, Bagatella P, Piccioli A, et al. Assessment of validity and reproducibility 
   of a clinical scale for the post-thrombotic syndrome. Haemostasis. 1994;24(4):158a.
2. Kahn SR, Partsch H, Vedantham S, et al. Definition of post-thrombotic syndrome of the 
   leg for use in clinical investigations: a recommendation for standardization. 
   J Thromb Haemost. 2009;7(5):879-883.
3. Soosainathan A, Moore HM, Gohel MS, et al. Scoring systems for the post-thrombotic 
   syndrome. J Vasc Surg. 2013;57(1):254-261.

The Villalta Score is the most widely used and recommended tool for diagnosing and 
grading post-thrombotic syndrome (PTS) severity following deep venous thrombosis (DVT). 
The score combines 5 patient-reported symptoms with 6 physician-assessed clinical signs, 
each rated from 0 (absent) to 3 (severe).

Scoring Components:
Patient-reported symptoms (0-3 each):
- Pain, cramps, heaviness, paresthesia, pruritus

Physician-assessed signs (0-3 each):  
- Pretibial edema, skin induration, hyperpigmentation, redness, venous ectasia, calf compression pain

Special rule: Presence of venous ulcer automatically classifies PTS as severe (≥15 points)

Clinical interpretation:
- 0-4 points: PTS absent
- 5-9 points: Mild PTS
- 10-14 points: Moderate PTS  
- ≥15 points or venous ulcer: Severe PTS

The Villalta score should be assessed at least 6 months after acute DVT when 
post-thrombotic changes have stabilized.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict


class VillaltaScoreRequest(BaseModel):
    """
    Request model for Villalta Score for Post-thrombotic Syndrome calculation
    
    The Villalta Score combines patient-reported symptoms with physician-assessed clinical 
    signs to diagnose and grade post-thrombotic syndrome severity. Each component is rated 
    on a 0-3 scale (0=absent, 1=mild, 2=moderate, 3=severe).
    
    Patient-reported symptoms (5 components):
    1. Pain - Aching, burning, or sharp pain in the affected limb
    2. Cramps - Muscle cramps or spasms in the affected limb
    3. Heaviness - Feeling of heaviness or fatigue in the affected limb
    4. Paresthesia - Numbness, tingling, or abnormal sensations
    5. Pruritus - Itching sensation in the affected limb
    
    Physician-assessed clinical signs (6 components):
    1. Pretibial edema - Swelling in front of the shin bone
    2. Skin induration - Hardening or thickening of the skin
    3. Hyperpigmentation - Darkening of the skin color
    4. Redness - Erythema or reddish discoloration
    5. Venous ectasia - Dilated superficial veins
    6. Calf compression pain - Pain elicited by calf compression
    
    Special consideration:
    - Venous ulcer presence automatically classifies PTS as severe
    - Assessment should be performed ≥6 months post-DVT
    - Requires trained healthcare provider for clinical examination
    
    Clinical applications:
    - Post-DVT patient monitoring
    - Treatment response assessment
    - Research standardization
    - Quality of life evaluation
    
    References (Vancouver style):
    1. Villalta S, Bagatella P, Piccioli A, et al. Assessment of validity and reproducibility 
    of a clinical scale for the post-thrombotic syndrome. Haemostasis. 1994;24(4):158a.
    2. Kahn SR, Partsch H, Vedantham S, et al. Definition of post-thrombotic syndrome of the 
    leg for use in clinical investigations: a recommendation for standardization. 
    J Thromb Haemost. 2009;7(5):879-883.
    """
    
    pain: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Patient-reported pain severity in affected limb. 0=absent, 1=mild, 2=moderate, 3=severe",
        example=1
    )
    
    cramps: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Patient-reported cramping severity in affected limb. 0=absent, 1=mild, 2=moderate, 3=severe",
        example=1
    )
    
    heaviness: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Patient-reported feeling of heaviness in affected limb. 0=absent, 1=mild, 2=moderate, 3=severe",
        example=2
    )
    
    paresthesia: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Patient-reported paresthesia (numbness/tingling) in affected limb. 0=absent, 1=mild, 2=moderate, 3=severe",
        example=0
    )
    
    pruritus: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Patient-reported itching severity in affected limb. 0=absent, 1=mild, 2=moderate, 3=severe",
        example=1
    )
    
    pretibial_edema: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Physician-assessed pretibial edema severity. 0=absent, 1=mild, 2=moderate, 3=severe",
        example=1
    )
    
    skin_induration: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Physician-assessed skin induration (hardening) severity. 0=absent, 1=mild, 2=moderate, 3=severe",
        example=0
    )
    
    hyperpigmentation: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Physician-assessed skin hyperpigmentation severity. 0=absent, 1=mild, 2=moderate, 3=severe",
        example=1
    )
    
    redness: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Physician-assessed skin redness severity. 0=absent, 1=mild, 2=moderate, 3=severe",
        example=0
    )
    
    venous_ectasia: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Physician-assessed venous ectasia (dilated superficial veins) severity. 0=absent, 1=mild, 2=moderate, 3=severe",
        example=1
    )
    
    calf_compression_pain: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Physician-assessed pain on calf compression severity. 0=absent, 1=mild, 2=moderate, 3=severe",
        example=0
    )
    
    venous_ulcer_present: Literal["yes", "no"] = Field(
        ...,
        description="Presence of venous ulcer. If yes, automatically classifies PTS as severe regardless of other scores",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "pain": 1,
                "cramps": 1,
                "heaviness": 2,
                "paresthesia": 0,
                "pruritus": 1,
                "pretibial_edema": 1,
                "skin_induration": 0,
                "hyperpigmentation": 1,
                "redness": 0,
                "venous_ectasia": 1,
                "calf_compression_pain": 0,
                "venous_ulcer_present": "no"
            }
        }


class VillaltaScoreResponse(BaseModel):
    """
    Response model for Villalta Score for Post-thrombotic Syndrome calculation
    
    Returns the Villalta score with PTS severity classification and clinical interpretation.
    
    Score interpretation:
    - 0-4 points: PTS absent
      → Continue routine DVT follow-up, monitor for PTS development
    - 5-9 points: Mild PTS  
      → Conservative management: compression (20-30 mmHg), elevation, exercise
    - 10-14 points: Moderate PTS
      → Intensified management: higher compression (30-40 mmHg), specialist referral
    - ≥15 points or venous ulcer: Severe PTS
      → Intensive management, advanced therapies, multidisciplinary care
    
    Component breakdown provides transparency showing:
    - Individual symptom and sign scores
    - Subtotal scores for symptoms vs. clinical signs
    - Whether venous ulcer adjustment was applied
    
    Clinical significance:
    - Most widely used PTS assessment tool
    - Recommended by international guidelines
    - Good inter-observer reliability when performed by trained clinicians
    - Requires clinical examination, cannot be performed remotely
    
    Reference: Kahn SR, et al. J Thromb Haemost. 2009;7(5):879-883.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=33,
        description="Total Villalta score calculated from symptoms and clinical signs",
        example=8
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the Villalta score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with specific management recommendations based on PTS severity",
        example="Villalta score of 8 indicates mild post-thrombotic syndrome. Initiate conservative management including compression therapy (20-30 mmHg), leg elevation, regular exercise, weight management, and patient education about PTS. Regular follow-up to monitor progression and symptom response to treatment."
    )
    
    stage: str = Field(
        ...,
        description="PTS severity classification (PTS Absent, Mild PTS, Moderate PTS, Severe PTS)",
        example="Mild PTS"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the PTS severity stage",
        example="Mild post-thrombotic syndrome"
    )
    
    component_breakdown: Dict = Field(
        ...,
        description="Detailed breakdown of score components showing symptoms, signs, and any special adjustments",
        example={
            "symptom_score": 5,
            "sign_score": 3,
            "venous_ulcer_present": False,
            "ulcer_adjustment_applied": False,
            "symptoms": {
                "pain": 1,
                "cramps": 1,
                "heaviness": 2,
                "paresthesia": 0,
                "pruritus": 1
            },
            "clinical_signs": {
                "pretibial_edema": 1,
                "skin_induration": 0,
                "hyperpigmentation": 1,
                "redness": 0,
                "venous_ectasia": 1,
                "calf_compression_pain": 0
            }
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 8,
                "unit": "points",
                "interpretation": "Villalta score of 8 indicates mild post-thrombotic syndrome. Initiate conservative management including compression therapy (20-30 mmHg), leg elevation, regular exercise, weight management, and patient education about PTS. Regular follow-up to monitor progression and symptom response to treatment.",
                "stage": "Mild PTS",
                "stage_description": "Mild post-thrombotic syndrome",
                "component_breakdown": {
                    "symptom_score": 5,
                    "sign_score": 3,
                    "venous_ulcer_present": False,
                    "ulcer_adjustment_applied": False,
                    "symptoms": {
                        "pain": 1,
                        "cramps": 1,
                        "heaviness": 2,
                        "paresthesia": 0,
                        "pruritus": 1
                    },
                    "clinical_signs": {
                        "pretibial_edema": 1,
                        "skin_induration": 0,
                        "hyperpigmentation": 1,
                        "redness": 0,
                        "venous_ectasia": 1,
                        "calf_compression_pain": 0
                    }
                }
            }
        }