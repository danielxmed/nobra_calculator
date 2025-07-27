"""
EularAcrPmr calculation models
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class MorningStiffnessType(str, Enum):
    """Enum for morning stiffness duration"""
    GREATER_45MIN = ">45min"
    LESS_EQUAL_45MIN = "≤45min"


class HipPainRomType(str, Enum):
    """Enum for hip pain or limited range of motion"""
    YES = "yes"
    NO = "no"


class RfAcpaType(str, Enum):
    """Enum for RF or ACPA presence"""
    PRESENT = "present"
    ABSENT = "absent"


class OtherJointPainType(str, Enum):
    """Enum for other joint pain"""
    PRESENT = "present"
    ABSENT = "absent"


class UltrasoundType(str, Enum):
    """Enum for ultrasound findings"""
    PRESENT = "present"
    ABSENT = "absent"
    NOT_PERFORMED = "not_performed"


class EularAcrPmrRequest(BaseModel):
    """
    Request model for EULAR/ACR 2012 Classification Criteria for Polymyalgia Rheumatica
    
    The 2012 EULAR/ACR classification criteria for Polymyalgia Rheumatica (PMR) provide 
    a standardized approach to PMR diagnosis, incorporating clinical features and optional 
    ultrasonographic findings to improve diagnostic accuracy.
    
    **Clinical Applications**:
    - PMR diagnosis and classification
    - Differentiation from rheumatoid arthritis
    - Clinical trial enrollment criteria
    - Standardized diagnostic approach
    - Research and epidemiological studies
    
    **Scoring System**:
    - Morning stiffness >45min: 2 points
    - Hip pain or limited ROM: 1 point
    - Absence of RF and ACPA: 2 points
    - Absence of other joint pain: 1 point
    - Ultrasound findings (if performed): 1-2 additional points
    
    **Diagnostic Thresholds**:
    - Without ultrasound: ≥4 points suggests PMR
    - With ultrasound: ≥5 points suggests PMR
    
    **Clinical Features of PMR**:
    - Bilateral shoulder and/or hip pain/stiffness
    - Age ≥50 years (prerequisite)
    - Elevated inflammatory markers (ESR/CRP)
    - Dramatic response to low-dose corticosteroids
    
    **Differential Diagnosis**:
    - Rheumatoid arthritis (RF/ACPA positive)
    - Giant cell arteritis (associated condition)
    - Fibromyalgia (normal inflammatory markers)
    - Malignancy (weight loss, systemic symptoms)
    
    **References**:
    - Dasgupta B, et al. 2012 Provisional classification criteria for polymyalgia rheumatica: a European League Against Rheumatism/American College of Rheumatology collaborative initiative. Ann Rheum Dis. 2012;71(4):484-92.
    """
    morning_stiffness: MorningStiffnessType = Field(
        ..., 
        description="Duration of morning stiffness. >45 minutes is characteristic of inflammatory conditions like PMR and adds 2 points to the score."
    )
    hip_pain_limited_rom: HipPainRomType = Field(
        ..., 
        description="Presence of hip pain or limited range of motion. Hip involvement is common in PMR and adds 1 point when present."
    )
    rf_or_acpa: RfAcpaType = Field(
        ..., 
        description="Presence of rheumatoid factor (RF) or anti-citrullinated peptide antibody (ACPA). Absence supports PMR diagnosis (2 points) vs. rheumatoid arthritis."
    )
    other_joint_pain: OtherJointPainType = Field(
        ..., 
        description="Pain in joints other than shoulders and hips. Absence is more consistent with PMR (1 point) as PMR typically affects proximal joints."
    )
    ultrasound_shoulder_hip: Optional[UltrasoundType] = Field(
        UltrasoundType.NOT_PERFORMED, 
        description="Ultrasound finding of at least one shoulder with subdeltoid bursitis/bicipital tenosynovitis/glenohumeral synovitis AND one hip with synovitis/trochanteric bursitis. Adds 1 point if present."
    )
    ultrasound_both_shoulders: Optional[UltrasoundType] = Field(
        UltrasoundType.NOT_PERFORMED, 
        description="Ultrasound finding of bilateral shoulder involvement with subdeltoid bursitis, bicipital tenosynovitis, or glenohumeral synovitis. Adds 1 point if present."
    )
    
    class Config:
        schema_extra = {
            "example": {
                "morning_stiffness": ">45min",
                "hip_pain_limited_rom": "yes",
                "rf_or_acpa": "absent",
                "other_joint_pain": "absent",
                "ultrasound_shoulder_hip": "not_performed",
                "ultrasound_both_shoulders": "not_performed"
            }
        }


class EularAcrPmrResponse(BaseModel):
    """
    Response model for EULAR/ACR 2012 Polymyalgia Rheumatica Classification Criteria
    
    Provides comprehensive PMR classification assessment with diagnostic probability
    and clinical management recommendations based on validated criteria.
    
    **Interpretation Framework**:
    - Without ultrasound: ≥4 points classifies as PMR (sensitivity 72%, specificity 65%)
    - With ultrasound: ≥5 points classifies as PMR (sensitivity 71%, specificity 70%)
    - Score <threshold: Consider alternative diagnoses
    
    **Clinical Validation**:
    - Validated in multiple international cohorts
    - Improved specificity over previous criteria
    - Incorporates modern imaging techniques
    - Standardized approach for clinical practice
    
    **Management Implications**:
    - PMR classification: Consider corticosteroid trial (prednisolone 15-20mg daily)
    - Monitor for giant cell arteritis association
    - Assess for contraindications to steroids
    - Plan gradual steroid taper over 12-24 months
    """
    result: int = Field(
        ..., 
        description="Total EULAR/ACR 2012 PMR classification score. Higher scores indicate greater likelihood of PMR diagnosis."
    )
    unit: str = Field(
        ..., 
        description="Unit of measurement for the classification score"
    )
    interpretation: str = Field(
        ..., 
        description="Evidence-based diagnostic interpretation with classification probability, sensitivity/specificity data, and clinical management recommendations."
    )
    stage: str = Field(
        ..., 
        description="Classification result (PMR, Non-PMR, PMR with ultrasound, Non-PMR with ultrasound) based on threshold criteria"
    )
    stage_description: str = Field(
        ..., 
        description="Detailed description of the classification result with clinical implications and next steps"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": "Score of 6 points (≥4) classifies as polymyalgia rheumatica by EULAR/ACR 2012 criteria. Sensitivity 72%, specificity 65%.",
                "stage": "PMR",
                "stage_description": "Classifies as PMR (without ultrasound)"
            }
        }
