"""
Abcd2 calculation models
"""

from pydantic import BaseModel, Field

class ThrombocytopeniaSeverityType(str, Enum):
    """Enum for thrombocytopenia severity in 4Ts score"""
    FALL_GREATER_50_NADIR_GREATER_20 = "fall_greater_50_nadir_greater_20"
    FALL_30_50_OR_NADIR_10_19 = "fall_30_50_or_nadir_10_19"
    FALL_LESS_30_OR_NADIR_LESS_10 = "fall_less_30_or_nadir_less_10"



class TimingOnsetType(str, Enum):
    """Enum for timing of thrombocytopenia onset in 4Ts score"""
    ONSET_5_10_DAYS_OR_FALL_1_DAY_HEPARIN_30_DAYS = "onset_5_10_days_or_fall_1_day_heparin_30_days"
    POSSIBLE_5_10_DAYS_OR_ONSET_AFTER_10_DAYS_OR_HEPARIN_30_100_DAYS = "possible_5_10_days_or_onset_after_10_days_or_heparin_30_100_days"
    FALL_LESS_4_DAYS_NO_RECENT_EXPOSURE = "fall_less_4_days_no_recent_exposure"



class ThrombosisSequelaeType(str, Enum):
    """Enum for thrombosis/sequelae in 4Ts score"""
    NEW_THROMBOSIS_OR_SKIN_NECROSIS_OR_SYSTEMIC_REACTION = "new_thrombosis_or_skin_necrosis_or_systemic_reaction"
    PROGRESSIVE_THROMBOSIS_OR_SKIN_LESIONS_OR_SUSPECTED_THROMBOSIS = "progressive_thrombosis_or_skin_lesions_or_suspected_thrombosis"
    NO_THROMBOSIS_OR_SEQUELAE = "no_thrombosis_or_sequelae"



class OtherCausesType(str, Enum):
    """Enum for other causes of thrombocytopenia in 4Ts score"""
    NO_OTHER_APPARENT_CAUSE = "no_other_apparent_cause"
    OTHER_POSSIBLE_CAUSES = "other_possible_causes"
    OTHER_DEFINITIVE_CAUSES = "other_definitive_causes"



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


# 4Ts Score Models  
class ThrombocytopeniaSeverityType(str, Enum):
    """Enum for thrombocytopenia severity in 4Ts score"""
    FALL_GREATER_50_NADIR_GREATER_20 = "fall_greater_50_nadir_greater_20"
    FALL_30_50_OR_NADIR_10_19 = "fall_30_50_or_nadir_10_19"
    FALL_LESS_30_OR_NADIR_LESS_10 = "fall_less_30_or_nadir_less_10"


class TimingOnsetType(str, Enum):
    """Enum for timing of thrombocytopenia onset in 4Ts score"""
    ONSET_5_10_DAYS_OR_FALL_1_DAY_HEPARIN_30_DAYS = "onset_5_10_days_or_fall_1_day_heparin_30_days"
    POSSIBLE_5_10_DAYS_OR_ONSET_AFTER_10_DAYS_OR_HEPARIN_30_100_DAYS = "possible_5_10_days_or_onset_after_10_days_or_heparin_30_100_days"
    FALL_LESS_4_DAYS_NO_RECENT_EXPOSURE = "fall_less_4_days_no_recent_exposure"


class ThrombosisSequelaeType(str, Enum):
    """Enum for thrombosis/sequelae in 4Ts score"""
    NEW_THROMBOSIS_OR_SKIN_NECROSIS_OR_SYSTEMIC_REACTION = "new_thrombosis_or_skin_necrosis_or_systemic_reaction"
    PROGRESSIVE_THROMBOSIS_OR_SKIN_LESIONS_OR_SUSPECTED_THROMBOSIS = "progressive_thrombosis_or_skin_lesions_or_suspected_thrombosis"
    NO_THROMBOSIS_OR_SEQUELAE = "no_thrombosis_or_sequelae"


class OtherCausesType(str, Enum):
    """Enum for other causes of thrombocytopenia in 4Ts score"""
    NO_OTHER_APPARENT_CAUSE = "no_other_apparent_cause"
    OTHER_POSSIBLE_CAUSES = "other_possible_causes"
    OTHER_DEFINITIVE_CAUSES = "other_definitive_causes"