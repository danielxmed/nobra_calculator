"""
Los Angeles Motor Scale (LAMS) Models

Request and response models for LAMS stroke severity assessment.

References (Vancouver style):
1. Llanes JN, Kidwell CS, Starkman S, Leary MC, Eckstein M, Saver JL. The Los Angeles 
   Motor Scale (LAMS): a new measure to characterize stroke severity in the field. 
   Prehosp Emerg Care. 2004 Jan-Mar;8(1):46-50. doi: 10.1080/312703002806.
2. Nazliel B, Starkman S, Liebeskind DS, Ovbiagele B, Kim D, Sanossian N, et al. A brief 
   prehospital stroke severity scale identifies ischemic stroke patients harboring 
   persisting large arterial occlusions. Stroke. 2008 Aug;39(8):2264-7. 
   doi: 10.1161/STROKEAHA.107.508127.
3. Pérez de la Ossa N, Carrera D, Gorchs M, Querol M, Millán M, Gomis M, et al. Design 
   and validation of a prehospital stroke scale to predict large arterial occlusion: 
   the rapid arterial occlusion evaluation scale. Stroke. 2014 Jan;45(1):87-91. 
   doi: 10.1161/STROKEAHA.113.003071.

The Los Angeles Motor Scale (LAMS) is a validated 3-component motor assessment tool 
designed for rapid prehospital stroke severity evaluation. It demonstrates strong 
correlation with NIHSS (r=0.75) and excellent accuracy for identifying large vessel 
occlusion strokes (sensitivity 81%, specificity 89%). LAMS ≥4 indicates severe stroke 
requiring direct transport to comprehensive stroke centers with endovascular capabilities, 
while LAMS <4 suggests minor to moderate stroke appropriate for standard stroke facilities.
"""

from pydantic import BaseModel, Field
from typing import Literal


class LosAngelesMotorScaleRequest(BaseModel):
    """
    Request model for Los Angeles Motor Scale (LAMS) stroke severity assessment
    
    The LAMS is a rapid 3-component motor examination designed for prehospital use 
    to identify stroke severity and guide transport decisions:
    
    Facial Droop Assessment:
    - absent: No facial asymmetry or weakness observed
    - present: Facial droop or asymmetry present when patient smiles or shows teeth
    
    Arm Drift Assessment:
    - absent: Both arms remain stable when held extended for 10 seconds
    - drifts_down: One arm drifts downward but does not fall to bed/surface
    - falls_rapidly: One arm falls rapidly to bed/surface within 10 seconds
    
    Grip Strength Assessment:
    - normal: Patient can grip examiner's fingers with normal strength bilaterally
    - weak_grip: Patient has detectably weak grip strength on one or both sides
    - no_grip: Patient cannot grip or has no detectable grip strength on affected side
    
    Clinical Application:
    - Total score 0-5 points (facial droop 0-1, arm drift 0-2, grip strength 0-2)
    - LAMS ≥4: High probability of large vessel occlusion, transport to comprehensive stroke center
    - LAMS <4: Lower probability of LVO, transport to nearest stroke-capable facility
    - Should be completed rapidly (<2 minutes) to avoid transport delays
    - Strong correlation with NIHSS but not a substitute for comprehensive assessment
    
    Validation Data:
    - Sensitivity: 81% for large vessel occlusion detection
    - Specificity: 89% for large vessel occlusion detection
    - Correlation with NIHSS: r=0.75
    - Developed and validated for use by paramedics and EMTs
    
    References (Vancouver style):
    1. Llanes JN, Kidwell CS, Starkman S, Leary MC, Eckstein M, Saver JL. The Los Angeles 
    Motor Scale (LAMS): a new measure to characterize stroke severity in the field. 
    Prehosp Emerg Care. 2004 Jan-Mar;8(1):46-50. doi: 10.1080/312703002806.
    2. Nazliel B, Starkman S, Liebeskind DS, Ovbiagele B, Kim D, Sanossian N, et al. A brief 
    prehospital stroke severity scale identifies ischemic stroke patients harboring 
    persisting large arterial occlusions. Stroke. 2008 Aug;39(8):2264-7. 
    doi: 10.1161/STROKEAHA.107.508127.
    3. Pérez de la Ossa N, Carrera D, Gorchs M, Querol M, Millán M, Gomis M, et al. Design 
    and validation of a prehospital stroke scale to predict large arterial occlusion: 
    the rapid arterial occlusion evaluation scale. Stroke. 2014 Jan;45(1):87-91. 
    doi: 10.1161/STROKEAHA.113.003071.
    """
    
    facial_droop: Literal["absent", "present"] = Field(
        ...,
        description="Presence of facial droop or asymmetry. Assess by asking patient to smile or show teeth. "
                   "Score 0 points if absent, 1 point if present",
        example="absent"
    )
    
    arm_drift: Literal["absent", "drifts_down", "falls_rapidly"] = Field(
        ...,
        description="Arm drift assessment with arms extended for 10 seconds. "
                   "absent (0 points): Both arms remain stable. "
                   "drifts_down (1 point): One arm drifts down but doesn't fall. "
                   "falls_rapidly (2 points): One arm falls rapidly to surface",
        example="drifts_down"
    )
    
    grip_strength: Literal["normal", "weak_grip", "no_grip"] = Field(
        ...,
        description="Hand grip strength assessment. "
                   "normal (0 points): Equal bilateral grip strength. "
                   "weak_grip (1 point): Detectably weak grip on one or both sides. "
                   "no_grip (2 points): Cannot grip or no detectable grip on affected side",
        example="weak_grip"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "facial_droop": "absent",
                "arm_drift": "drifts_down", 
                "grip_strength": "weak_grip"
            }
        }


class LosAngelesMotorScaleResponse(BaseModel):
    """
    Response model for Los Angeles Motor Scale (LAMS) stroke severity assessment
    
    The LAMS provides rapid stroke severity stratification for prehospital transport decisions:
    
    Score Interpretation:
    - 0-3 points: Minor to moderate stroke, LVO less likely
      Transport to nearest stroke-capable facility for IV thrombolysis evaluation
    
    - 4-5 points: Severe stroke, LVO likely (81% sensitivity, 89% specificity)
      Direct transport to comprehensive stroke center with endovascular capabilities
      7-fold increased likelihood of persisting large vessel occlusion
    
    Clinical Significance:
    - Strong correlation with NIHSS scores (r=0.75)
    - Predictive of functional outcomes at 3 months
    - Validated for use by prehospital providers to guide transport decisions
    - Time-sensitive assessment critical for optimal stroke outcomes
    
    Reference: Llanes JN, et al. Prehosp Emerg Care. 2004;8(1):46-50.
    """
    
    result: int = Field(
        ...,
        description="LAMS score calculated from motor assessment components (range 0-5 points)",
        ge=0,
        le=5,
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the LAMS score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with transport recommendations and prehospital care guidance",
        example="Los Angeles Motor Scale (LAMS) Score Assessment:\n\nComponent Scores:\n• Facial droop: 0 points\n• Arm drift: 1 point\n• Grip strength: 1 point\n• Total LAMS score: 2/5 points\n\nClinical Interpretation:\n• Stroke severity: Minor to Moderate Stroke\n• Large vessel occlusion (LVO): LVO less likely"
    )
    
    stage: str = Field(
        ...,
        description="Stroke severity category based on LAMS score",
        example="Minor to Moderate Stroke"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of large vessel occlusion likelihood",
        example="LVO less likely"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "Los Angeles Motor Scale (LAMS) Score Assessment:\n\nComponent Scores:\n• Facial droop: 0 points\n• Arm drift: 1 point\n• Grip strength: 1 point\n• Total LAMS score: 2/5 points\n\nClinical Interpretation:\n• Stroke severity: Minor to Moderate Stroke\n• Large vessel occlusion (LVO): LVO less likely\n\nTransport Recommendations:\n• Destination: Transport to nearest stroke-capable facility\n• Urgency: Moderate - stroke treatment beneficial but less time-sensitive\n• Expected interventions: IV thrombolysis (tPA) if within time window\n\nMinor to Moderate Stroke Management (LAMS <4):\n• Lower probability of large vessel occlusion\n• May still benefit from IV thrombolysis if within time window\n• Transport to nearest stroke-capable facility appropriate\n• Standard stroke protocol and supportive care\n• Monitor for neurological deterioration during transport",
                "stage": "Minor to Moderate Stroke",
                "stage_description": "LVO less likely"
            }
        }