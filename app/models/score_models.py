"""
Pydantic models for API requests and responses

This module imports all models from the refactored structure for backward compatibility.
The models have been organized into specialty-specific modules for better maintainability.
"""

# Import all models from the new organized structure
from app.models.scores import *

# Import additional models that haven't been refactored yet
# These will be moved to appropriate specialty modules in future iterations
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any, Union
from enum import Enum


# ABCD² Score Models - These should be moved to neurology module
class BloodPressureType(str, Enum):
    """Enum for blood pressure categories in ABCD² score"""
    NORMAL = "normal"
    ELEVATED = "elevated"


class ClinicalFeaturesType(str, Enum):
    """Enum for clinical features in ABCD² score"""
    UNILATERAL_WEAKNESS = "unilateral_weakness"
    SPEECH_DISTURBANCE = "speech_disturbance"
    OTHER = "other"


class DurationType(str, Enum):
    """Enum for symptom duration in ABCD² score"""
    LESS_10MIN = "less_10min"
    BETWEEN_10_59MIN = "10_59min"
    MORE_60MIN = "60min_or_more"


class Abcd2Request(BaseModel):
    """Request model for ABCD² Score calculation"""
    age: int = Field(..., ge=18, le=120)
    blood_pressure: BloodPressureType
    clinical_features: ClinicalFeaturesType
    duration: DurationType
    diabetes: DiabetesType
    
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
    """Response model for ABCD² Score calculation"""
    result: int = Field(...)
    unit: str = Field(...)
    interpretation: str = Field(...)
    stage: str = Field(...)
    stage_description: str = Field(...)
    stroke_risk_2days: str = Field(...)
    stroke_risk_7days: str = Field(...)
    stroke_risk_90days: str = Field(...)
    
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


# 4Ts Score Models - These should be moved to hematology module
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


class FourTsRequest(BaseModel):
    """Request model for 4Ts Score calculation"""
    thrombocytopenia_severity: ThrombocytopeniaSeverityType
    timing_onset: TimingOnsetType
    thrombosis_sequelae: ThrombosisSequelaeType
    other_causes: OtherCausesType
    
    class Config:
        schema_extra = {
            "example": {
                "thrombocytopenia_severity": "fall_greater_50_nadir_greater_20",
                "timing_onset": "onset_5_10_days_or_fall_1_day_heparin_30_days",
                "thrombosis_sequelae": "new_thrombosis_or_skin_necrosis_or_systemic_reaction",
                "other_causes": "no_other_apparent_cause"
            }
        }


class FourTsResponse(BaseModel):
    """Response model for 4Ts Score calculation"""
    result: int = Field(...)
    unit: str = Field(...)
    interpretation: str = Field(...)
    stage: str = Field(...)
    stage_description: str = Field(...)
    hit_probability: str = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "result": 7,
                "unit": "points",
                "interpretation": "HIT probability ~64%. Immediately discontinue all heparin. Start non-heparin anticoagulant. Perform confirmatory tests for HIT.",
                "stage": "High Probability",
                "stage_description": "High probability of HIT",
                "hit_probability": "64%"
            }
        }


# AIMS Models - These should be moved to psychiatry module
class AimsRequest(BaseModel):
    """Request model for AIMS calculation"""
    facial_muscles: int = Field(..., ge=0, le=4)
    lips_perioral: int = Field(..., ge=0, le=4)
    jaw: int = Field(..., ge=0, le=4)
    tongue: int = Field(..., ge=0, le=4)
    upper_extremities: int = Field(..., ge=0, le=4)
    lower_extremities: int = Field(..., ge=0, le=4)
    trunk_movements: int = Field(..., ge=0, le=4)
    global_severity: int = Field(..., ge=0, le=4)
    incapacitation: int = Field(..., ge=0, le=4)
    patient_awareness: int = Field(..., ge=0, le=4)
    current_problems_teeth: DiabetesType
    dental_problems_interfere: DiabetesType
    
    class Config:
        schema_extra = {
            "example": {
                "facial_muscles": 2,
                "lips_perioral": 1,
                "jaw": 2,
                "tongue": 3,
                "upper_extremities": 1,
                "lower_extremities": 2,
                "trunk_movements": 1,
                "global_severity": 2,
                "incapacitation": 2,
                "patient_awareness": 3,
                "current_problems_teeth": "no",
                "dental_problems_interfere": "no"
            }
        }


class AimsResponse(BaseModel):
    """Response model for AIMS calculation"""
    result: int = Field(...)
    unit: str = Field(...)
    interpretation: str = Field(...)
    stage: str = Field(...)
    stage_description: str = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "result": 12,
                "unit": "points",
                "interpretation": "Evidence of tardive dyskinesia. Re-evaluate need for neuroleptic medication, consider dose reduction or medication change.",
                "stage": "Mild to Moderate Dyskinesia",
                "stage_description": "Presence of tardive dyskinesia"
            }
        }


# 4C Mortality Score Models - These should be moved to emergency module
class UreaUnitType(str, Enum):
    """Enum for urea measurement units"""
    MMOL_L = "mmol_L"
    MG_DL = "mg_dL"


class FourCMortalityRequest(BaseModel):
    """Request model for 4C Mortality Score calculation"""
    age: int = Field(..., ge=0, le=120)
    sex: SexType
    comorbidities: int = Field(..., ge=0, le=20)
    respiratory_rate: int = Field(..., ge=5, le=60)
    oxygen_saturation: float = Field(..., ge=50.0, le=100.0)
    glasgow_coma_scale: int = Field(..., ge=3, le=15)
    urea_unit: UreaUnitType
    urea_value: float = Field(..., ge=0.1, le=300.0)
    crp: float = Field(..., ge=0.0, le=1000.0)
    
    class Config:
        schema_extra = {
            "example": {
                "age": 70,
                "sex": "male",
                "comorbidities": 2,
                "respiratory_rate": 24,
                "oxygen_saturation": 92.0,
                "glasgow_coma_scale": 15,
                "urea_unit": "mg_dL",
                "urea_value": 45.0,
                "crp": 80.0
            }
        }


class FourCMortalityResponse(BaseModel):
    """Response model for 4C Mortality Score calculation"""
    result: int = Field(...)
    unit: str = Field(...)
    interpretation: str = Field(...)
    stage: str = Field(...)
    stage_description: str = Field(...)
    mortality_risk: str = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "result": 10,
                "unit": "points",
                "interpretation": "In-hospital mortality of 31.4-34.9%. Patients require intensive care or high-dependency unit monitoring.",
                "stage": "High Risk",
                "stage_description": "High mortality risk",
                "mortality_risk": "31.4-34.9%"
            }
        }


# 6 Minute Walk Distance Models - These should be moved to pulmonology module
class SixMinuteWalkRequest(BaseModel):
    """Request model for 6-Minute Walk Distance calculation"""
    age: int = Field(..., ge=18, le=100)
    sex: SexType
    height: float = Field(..., ge=120.0, le=220.0)
    weight: float = Field(..., ge=30.0, le=200.0)
    observed_distance: Optional[float] = Field(None, ge=0.0, le=1000.0)
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "sex": "male",
                "height": 175.0,
                "weight": 80.0,
                "observed_distance": 450.0
            }
        }


class SixMinuteWalkResponse(BaseModel):
    """Response model for 6-Minute Walk Distance calculation"""
    result: float = Field(...)
    unit: str = Field(...)
    interpretation: str = Field(...)
    stage: str = Field(...)
    stage_description: str = Field(...)
    lower_limit_normal: float = Field(...)
    percentage_predicted: Optional[float] = Field(None)
    
    class Config:
        schema_extra = {
            "example": {
                "result": 485.3,
                "unit": "meters",
                "interpretation": "Distance within expected values for age, sex, height, and weight. Indicates preserved functional capacity.",
                "stage": "Normal",
                "stage_description": "Normal functional capacity",
                "lower_limit_normal": 332.3,
                "percentage_predicted": 92.7
            }
        }


# A-a O2 Gradient Models - These should be moved to pulmonology module
class AAO2GradientRequest(BaseModel):
    """Request model for Alveolar-Arterial Oxygen Gradient calculation"""
    age: int = Field(..., ge=1, le=120)
    fio2: float = Field(..., ge=0.21, le=1.0)
    paco2: float = Field(..., ge=10.0, le=100.0)
    pao2: float = Field(..., ge=30.0, le=600.0)
    patm: Optional[float] = Field(760.0, ge=500.0, le=800.0)
    respiratory_quotient: Optional[float] = Field(0.8, ge=0.7, le=1.0)
    
    class Config:
        schema_extra = {
            "example": {
                "age": 45,
                "fio2": 0.21,
                "paco2": 40.0,
                "pao2": 90.0,
                "patm": 760.0,
                "respiratory_quotient": 0.8
            }
        }


class AAO2GradientResponse(BaseModel):
    """Response model for Alveolar-Arterial Oxygen Gradient calculation"""
    result: float = Field(...)
    unit: str = Field(...)
    interpretation: str = Field(...)
    stage: str = Field(...)
    stage_description: str = Field(...)
    pao2_alveolar: float = Field(...)
    age_adjusted_normal: float = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "result": 15.2,
                "unit": "mmHg",
                "interpretation": "Preserved alveolar function. Normal values for young adults are 5-10 mmHg, which may increase with age.",
                "stage": "Normal",
                "stage_description": "Normal A-a gradient",
                "pao2_alveolar": 105.2,
                "age_adjusted_normal": 15.25
            }
        }


# AAS Models - These should be moved to general module
class AasRequest(BaseModel):
    """Request model for Abuse Assessment Screen (AAS)"""
    emotional_physical_abuse: YesNoType
    physical_hurt_recently: YesNoType
    physical_hurt_pregnancy: YesNoNAType
    sexual_abuse: YesNoType
    afraid_of_partner: YesNoType
    
    class Config:
        schema_extra = {
            "example": {
                "emotional_physical_abuse": "no",
                "physical_hurt_recently": "no",
                "physical_hurt_pregnancy": "not_applicable",
                "sexual_abuse": "no",
                "afraid_of_partner": "no"
            }
        }


class AasResponse(BaseModel):
    """Response model for Abuse Assessment Screen (AAS)"""
    result: str = Field(...)
    unit: str = Field(...)
    interpretation: str = Field(...)
    stage: str = Field(...)
    stage_description: str = Field(...)
    positive_responses_count: int = Field(...)
    is_positive: bool = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Negative",
                "unit": "result",
                "interpretation": "Negative result for domestic violence. Continue to offer support and information about available resources.",
                "stage": "Negative Screening",
                "stage_description": "No indication of domestic abuse",
                "positive_responses_count": 0,
                "is_positive": False
            }
        }


# AAP Pediatric Hypertension Models - These should be moved to pediatrics module
class AapPediatricHypertensionRequest(BaseModel):
    """Request model for AAP Pediatric Hypertension Classification"""
    age: int = Field(..., ge=1, le=17)
    sex: SexType
    height: float = Field(..., ge=70.0, le=200.0)
    systolic_bp: int = Field(..., ge=60, le=200)
    diastolic_bp: int = Field(..., ge=30, le=150)
    
    class Config:
        schema_extra = {
            "example": {
                "age": 10,
                "sex": "male",
                "height": 140.0,
                "systolic_bp": 110,
                "diastolic_bp": 70
            }
        }


class AapPediatricHypertensionResponse(BaseModel):
    """Response model for AAP Pediatric Hypertension Classification"""
    result: str = Field(...)
    unit: str = Field(...)
    interpretation: str = Field(...)
    stage: str = Field(...)
    stage_description: str = Field(...)
    systolic_percentile: float = Field(...)
    diastolic_percentile: float = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Normal",
                "unit": "classification",
                "interpretation": "BP below the 90th percentile for age, sex, and height. No specific intervention required.",
                "stage": "Normal",
                "stage_description": "Normal blood pressure",
                "systolic_percentile": 75.2,
                "diastolic_percentile": 68.5
            }
        }


# Abbey Pain Scale Models - These should be moved to geriatrics module
class AbbeyPainRequest(BaseModel):
    """Request model for Abbey Pain Scale calculation"""
    vocalization: int = Field(..., ge=0, le=3)
    facial_expression: int = Field(..., ge=0, le=3)
    body_language: int = Field(..., ge=0, le=3)
    behavioral_change: int = Field(..., ge=0, le=3)
    physiological_change: int = Field(..., ge=0, le=3)
    physical_change: int = Field(..., ge=0, le=3)
    
    class Config:
        schema_extra = {
            "example": {
                "vocalization": 1,
                "facial_expression": 2,
                "body_language": 1,
                "behavioral_change": 0,
                "physiological_change": 1,
                "physical_change": 0
            }
        }


class AbbeyPainResponse(BaseModel):
    """Response model for Abbey Pain Scale calculation"""
    result: int = Field(...)
    unit: str = Field(...)
    interpretation: str = Field(...)
    stage: str = Field(...)
    stage_description: str = Field(...)
    pain_present: bool = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5,
                "unit": "points",
                "interpretation": "Mild pain present. Monitor and consider non-pharmacological interventions.",
                "stage": "Mild Pain",
                "stage_description": "Mild pain",
                "pain_present": True
            }
        }


# ALC Models - These should be moved to hematology module
class AlcRequest(BaseModel):
    """Request model for Absolute Lymphocyte Count (ALC) calculation"""
    white_blood_cells: float = Field(..., ge=0.1, le=500.0)
    lymphocyte_percentage: float = Field(..., ge=0.0, le=100.0)
    
    class Config:
        schema_extra = {
            "example": {
                "white_blood_cells": 6.5,
                "lymphocyte_percentage": 25.0
            }
        }


class AlcResponse(BaseModel):
    """Response model for Absolute Lymphocyte Count (ALC) calculation"""
    result: float = Field(...)
    unit: str = Field(...)
    interpretation: str = Field(...)
    stage: str = Field(...)
    stage_description: str = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1625,
                "unit": "cells/mm³",
                "interpretation": "Indeterminate range for CD4 prediction. Specific CD4 count is necessary for accurate immunological status assessment.",
                "stage": "Indeterminate Zone", 
                "stage_description": "CD4 indeterminate"
            }
        }


# ANC Models - These should be moved to hematology module
class AncRequest(BaseModel):
    """Request model for Absolute Neutrophil Count (ANC) calculation"""
    white_blood_cells: float = Field(..., ge=0.1, le=500.0)
    neutrophil_percentage: float = Field(..., ge=0.0, le=100.0)
    band_percentage: Optional[float] = Field(0.0, ge=0.0, le=100.0)
    
    class Config:
        schema_extra = {
            "example": {
                "white_blood_cells": 6.5,
                "neutrophil_percentage": 60.0,
                "band_percentage": 5.0
            }
        }


class AncResponse(BaseModel):
    """Response model for Absolute Neutrophil Count (ANC) calculation"""
    result: float = Field(...)
    unit: str = Field(...)
    interpretation: str = Field(...)
    stage: str = Field(...)
    stage_description: str = Field(...)
    infection_risk: str = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4225,
                "unit": "cells/mm³",
                "interpretation": "Neutrophil count within normal range (1500-8000 cells/mm³). Infection risk not increased by neutropenia.",
                "stage": "Normal",
                "stage_description": "Normal count",
                "infection_risk": "normal"
            }
        }


# EULAR/ACR PMR Models - These should be moved to rheumatology module
class MorningStiffnessType(str, Enum):
    """Enum for morning stiffness duration"""
    SHORT = "<=45min"
    LONG = ">45min"


class RfAcpaType(str, Enum):
    """Enum for presence of RF or ACPA"""
    PRESENT = "present"
    ABSENT = "absent"


class OtherJointPainType(str, Enum):
    """Enum for pain in other joints"""
    PRESENT = "present"
    ABSENT = "absent"


class UltrasoundType(str, Enum):
    """Enum for ultrasound findings"""
    NO = "no"
    YES = "yes" 
    NOT_PERFORMED = "not_performed"


class HipPainRomType(str, Enum):
    """Enum for hip pain or limited ROM"""
    NO = "no"
    YES = "yes"


class EularAcrPmrRequest(BaseModel):
    """Request model for EULAR/ACR 2012 Classification Criteria for Polymyalgia Rheumatica"""
    morning_stiffness: MorningStiffnessType
    hip_pain_limited_rom: HipPainRomType
    rf_or_acpa: RfAcpaType
    other_joint_pain: OtherJointPainType
    ultrasound_shoulder_hip: Optional[UltrasoundType] = UltrasoundType.NOT_PERFORMED
    ultrasound_both_shoulders: Optional[UltrasoundType] = UltrasoundType.NOT_PERFORMED
    
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
    """Response model for EULAR/ACR 2012 Polymyalgia Rheumatica Classification Criteria"""
    result: int = Field(...)
    unit: str = Field(...)
    interpretation: str = Field(...)
    stage: str = Field(...)
    stage_description: str = Field(...)
    
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


# 4AT Models - These should be moved to neurology module
class AlertnessType(str, Enum):
    """Enum for alertness level"""
    NORMAL = "normal"
    ALTERED = "altered"


class AttentionMonthsType(str, Enum):
    """Enum for attention test with months"""
    SEVEN_OR_MORE = "7_or_more"
    STARTS_LESS_THAN_7 = "starts_less_than_7"
    REFUSES_UNTESTABLE = "refuses_untestable"


class AcuteChangeType(str, Enum):
    """Enum for acute change or fluctuating course"""
    ABSENT = "absent"
    PRESENT = "present"


class FourAtRequest(BaseModel):
    """Request model for 4AT (4 A's Test) Delirium Screening Tool"""
    alertness: AlertnessType
    amt4_errors: int = Field(..., ge=0, le=4)
    attention_months: AttentionMonthsType
    acute_change: AcuteChangeType
    
    class Config:
        schema_extra = {
            "example": {
                "alertness": "normal",
                "amt4_errors": 1,
                "attention_months": "7_or_more",
                "acute_change": "absent"
            }
        }


class FourAtResponse(BaseModel):
    """Response model for 4AT (4 A's Test) Delirium Screening"""
    result: int = Field(...)
    unit: str = Field(...)
    interpretation: str = Field(...)
    stage: str = Field(...)
    stage_description: str = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "Score ≥4 suggests possible delirium. This result is not diagnostic - the final diagnosis must be based on clinical judgment. Comprehensive mental assessment and investigation of reversible causes are recommended.",
                "stage": "Possible Delirium",
                "stage_description": "Result suggests delirium"
            }
        }


# HElPS2B Models - These should be moved to neurology module
class EegFindingType(str, Enum):
    """Enum for EEG findings"""
    PRESENT = "present"
    ABSENT = "absent"


class Helps2bRequest(BaseModel):
    """Request model for 2HELPS2B Score - Seizure Risk Prediction in Hospitalized Patients"""
    seizure_history: YesNoType
    epileptiform_discharges: EegFindingType
    lateralized_periodic_discharges: EegFindingType
    bilateral_independent_periodic_discharges: EegFindingType
    brief_potentially_ictal_rhythmic_discharges: EegFindingType
    burst_suppression: EegFindingType
    
    class Config:
        schema_extra = {
            "example": {
                "seizure_history": "no",
                "epileptiform_discharges": "absent",
                "lateralized_periodic_discharges": "absent",
                "bilateral_independent_periodic_discharges": "absent",
                "brief_potentially_ictal_rhythmic_discharges": "absent",
                "burst_suppression": "absent"
            }
        }


class Helps2bResponse(BaseModel):
    """Response model for 2HELPS2B Score - Seizure Risk Prediction"""
    result: int = Field(...)
    unit: str = Field(...)
    interpretation: str = Field(...)
    stage: str = Field(...)
    stage_description: str = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "Seizure risk in 72h: 5%. Only 1-hour screening EEG recommended. Additional monitoring generally not necessary.",
                "stage": "Low Risk",
                "stage_description": "Very low seizure risk"
            }
        }
