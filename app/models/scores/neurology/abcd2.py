"""
Abcd2 calculation models
"""

from pydantic import BaseModel, Field
from enum import Enum


class BloodPressureType(str, Enum):
    """Enum for blood pressure classification in ABCD² score"""
    ELEVATED = "elevated"  # ≥140/90 mmHg
    NORMAL = "normal"      # <140/90 mmHg


class ClinicalFeaturesType(str, Enum):
    """Enum for clinical features in ABCD² score"""
    UNILATERAL_WEAKNESS = "unilateral_weakness"  # 2 points
    SPEECH_DISTURBANCE = "speech_disturbance"    # 1 point
    OTHER = "other"                              # 0 points


class DurationType(str, Enum):
    """Enum for symptom duration in ABCD² score"""
    SIXTY_MIN_OR_MORE = "60min_or_more"    # ≥60 min (2 points)
    TEN_TO_FIFTY_NINE_MIN = "10_59min"     # 10-59 min (1 point)
    LESS_THAN_TEN_MIN = "less_10min"       # <10 min (0 points)


class DiabetesType(str, Enum):
    """Enum for diabetes history in ABCD² score"""
    YES = "yes"
    NO = "no"


class Abcd2Request(BaseModel):
    """
    Request model for ABCD² Score calculation
    
    The ABCD² score predicts stroke risk following transient ischemic attack (TIA),
    helping clinicians make urgent decisions about hospitalization and immediate interventions.
    
    **Clinical Use**:
    - Early stroke risk stratification after TIA
    - Urgent hospitalization decision-making
    - Immediate intervention planning
    - Patient triage and resource allocation
    - Risk communication with patients and families
    
    **Score Components**:
    - A: Age ≥60 years (1 point)
    - B: Blood pressure ≥140/90 mmHg (1 point)
    - C: Clinical features - unilateral weakness (2 points), speech disturbance (1 point), other (0 points)
    - D: Duration - ≥60 min (2 points), 10-59 min (1 point), <10 min (0 points)
    - D: Diabetes (1 point)
    
    **Reference**: Johnston SC, et al. Validation and refinement of scores to predict very early stroke risk after transient ischaemic attack. Lancet. 2007;369(9558):283-92.
    """
    age: int = Field(
        ..., 
        ge=18, 
        le=120, 
        description="Patient's age in years. Age ≥60 years adds 1 point, reflecting increased stroke risk in elderly patients after TIA.",
        example=72
    )
    blood_pressure: BloodPressureType = Field(
        ..., 
        description="Blood pressure at time of evaluation. Elevated BP (≥140/90 mmHg) adds 1 point and indicates higher stroke risk.",
        example="elevated"
    )
    clinical_features: ClinicalFeaturesType = Field(
        ..., 
        description="Clinical features of the TIA episode. Unilateral weakness (2 points) carries highest risk, speech disturbance (1 point) moderate risk, other symptoms (0 points).",
        example="unilateral_weakness"
    )
    duration: DurationType = Field(
        ..., 
        description="Duration of TIA symptoms. Longer duration indicates higher stroke risk: ≥60 min (2 points), 10-59 min (1 point), <10 min (0 points).",
        example="60min_or_more"
    )
    diabetes: DiabetesType = Field(
        ..., 
        description="History of diabetes mellitus. Presence of diabetes adds 1 point due to increased vascular risk.",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 72,
                "blood_pressure": "elevated",
                "clinical_features": "unilateral_weakness",
                "duration": "60min_or_more",
                "diabetes": "yes"
            }
        }


class Abcd2Response(BaseModel):
    """
    Response model for ABCD² Score calculation
    
    Provides urgent stroke risk assessment with time-specific risk predictions and 
    evidence-based recommendations for immediate clinical management.
    
    **Risk Stratification & Management**:
    - Score 0-3: Low risk - outpatient management may be appropriate with close follow-up
    - Score 4-5: Moderate risk - consider hospitalization, urgent evaluation recommended
    - Score 6-7: High risk - hospitalization strongly recommended, immediate investigation
    
    **Urgent Interventions**:
    - Dual antiplatelet therapy (aspirin + clopidogrel) for 21 days if appropriate
    - Carotid imaging within 24-48 hours
    - Cardiac evaluation including ECG, echocardiogram
    - MRI brain with DWI to detect silent infarction
    """
    result: int = Field(
        ..., 
        description="Total ABCD² score ranging from 0-7 points. Higher scores indicate progressively increased stroke risk in the days following TIA.",
        example=6
    )
    unit: str = Field(
        ..., 
        description="Unit of the score result",
        example="points"
    )
    interpretation: str = Field(
        ..., 
        description="Comprehensive clinical interpretation with time-specific stroke risks and urgent management recommendations based on current stroke guidelines.",
        example="Stroke risk in 2 days: 8.1%; in 7 days: 11.7%; in 90 days: 17.8%. Urgent hospitalization recommended for investigation and immediate initiation of preventive measures."
    )
    stage: str = Field(
        ..., 
        description="Risk classification (Low Risk, Moderate Risk, High Risk) for stroke occurrence",
        example="High Risk"
    )
    stage_description: str = Field(
        ..., 
        description="Description of the overall risk level",
        example="High stroke risk"
    )
    stroke_risk_2days: str = Field(
        ..., 
        description="Predicted stroke risk within 2 days of TIA, critical for immediate management decisions",
        example="8.1%"
    )
    stroke_risk_7days: str = Field(
        ..., 
        description="Predicted stroke risk within 7 days of TIA, important for early follow-up planning",
        example="11.7%"
    )
    stroke_risk_90days: str = Field(
        ..., 
        description="Predicted stroke risk within 90 days of TIA, relevant for long-term prevention strategies",
        example="17.8%"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": "Stroke risk in 2 days: 8.1%; in 7 days: 11.7%; in 90 days: 17.8%. Urgent hospitalization recommended for investigation and immediate initiation of preventive measures.",
                "stage": "High Risk",
                "stage_description": "High stroke risk",
                "stroke_risk_2days": "8.1%",
                "stroke_risk_7days": "11.7%",
                "stroke_risk_90days": "17.8%"
            }
        }
