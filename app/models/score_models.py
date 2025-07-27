"""
Pydantic models for API requests and responses
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any, Union
from enum import Enum


class SexType(str, Enum):
    """Enum for accepted sex types"""
    MALE = "male"
    FEMALE = "female"


# Request Models
class CKDEpi2021Request(BaseModel):
    """
    Request model for CKD-EPI 2021 eGFR calculation
    
    The CKD-EPI 2021 equation estimates glomerular filtration rate (eGFR) without race 
    coefficient, providing a more equitable assessment of kidney function across all populations.
    
    **Clinical Use**: 
    - Chronic kidney disease staging and monitoring
    - Medication dosing adjustments
    - Nephrology referral decisions
    - Cardiovascular risk assessment
    
    **Formula**: eGFR = 142 × min(SCr/κ,1)^α × max(SCr/κ,1)^(-1.200) × 0.9938^Age × 1.012 [if female]
    
    **Reference**: Inker LA, et al. New creatinine- and cystatin C-based equations to estimate GFR without race. N Engl J Med. 2021;385(19):1737-1749.
    """
    sex: SexType = Field(
        ..., 
        description="Patient's biological sex. Required for applying sex-specific coefficients in the equation.",
        example="female"
    )
    age: int = Field(
        ..., 
        ge=18, 
        le=120, 
        description="Patient's age in years. Must be ≥18 years as the equation is validated for adults only.",
        example=65
    )
    serum_creatinine: float = Field(
        ..., 
        ge=0.1, 
        le=20.0, 
        description="Serum creatinine concentration in mg/dL. Must be standardized to IDMS (Isotope Dilution Mass Spectrometry) traceable methods for accuracy.",
        example=1.2
    )
    
    class Config:
        schema_extra = {
            "example": {
                "sex": "female",
                "age": 65,
                "serum_creatinine": 1.2
            }
        }


# Response Models
class CKDEpi2021Response(BaseModel):
    """
    Response model for CKD-EPI 2021 eGFR calculation
    
    Provides estimated glomerular filtration rate with comprehensive clinical interpretation 
    based on KDIGO CKD staging guidelines.
    
    **Interpretation Ranges**:
    - G1 (≥90): Normal/high - investigate for kidney damage
    - G2 (60-89): Mild decrease - investigate for kidney damage  
    - G3a (45-59): Mild-moderate decrease - nephrology follow-up recommended
    - G3b (30-44): Moderate-severe decrease - nephrologist referral necessary
    - G4 (15-29): Severe decrease - prepare for kidney replacement therapy
    - G5 (<15): Kidney failure - dialysis or transplant needed
    """
    result: float = Field(
        ..., 
        description="Estimated glomerular filtration rate (eGFR) in mL/min/1.73 m². Values typically range from 5-150 mL/min/1.73 m².",
        example=52.3
    )
    unit: str = Field(
        ..., 
        description="Unit of measurement for eGFR, normalized to body surface area",
        example="mL/min/1.73 m²"
    )
    interpretation: str = Field(
        ..., 
        description="Clinical interpretation with specific recommendations based on KDIGO guidelines. Includes staging information and suggested clinical actions.",
        example="Stage 3a Chronic Kidney Disease. Nephrology follow-up recommended."
    )
    stage: str = Field(
        ..., 
        description="KDIGO CKD stage classification (G1, G2, G3a, G3b, G4, G5) based on eGFR value",
        example="G3a"
    )
    stage_description: str = Field(
        ..., 
        description="Descriptive explanation of the CKD stage severity and functional status",
        example="Mild to moderate decrease in GFR"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 52.3,
                "unit": "mL/min/1.73 m²",
                "interpretation": "Stage 3a Chronic Kidney Disease. Nephrology follow-up recommended.",
                "stage": "G3a",
                "stage_description": "Mild to moderate decrease in GFR"
            }
        }


class ScoreInfo(BaseModel):
    """Basic information of a medical score"""
    id: str = Field(..., description="Unique identifier of the medical score")
    title: str = Field(..., description="Full title of the medical score or calculator")
    description: str = Field(..., description="Brief description of what the score calculates and its clinical purpose")
    category: str = Field(..., description="Medical specialty or category (e.g., cardiology, nephrology, neurology)")
    version: Optional[str] = Field(None, description="Version year or revision of the score/equation")


class ScoreListResponse(BaseModel):
    """Response for listing available medical scores"""
    scores: List[ScoreInfo] = Field(..., description="Array of available medical scores with basic information")
    total: int = Field(..., description="Total number of available scores in the system")
    
    class Config:
        schema_extra = {
            "example": {
                "scores": [
                    {
                        "id": "ckd_epi_2021",
                        "title": "CKD-EPI 2021 - Estimated Glomerular Filtration Rate",
                        "description": "CKD-EPI 2021 equation to estimate glomerular filtration rate",
                        "category": "nephrology",
                        "version": "2021"
                    }
                ],
                "total": 1
            }
        }


class Parameter(BaseModel):
    """Model for score parameters with validation rules"""
    name: str = Field(..., description="Parameter name as used in the calculation")
    type: str = Field(..., description="Data type (string, integer, float, boolean)")
    required: bool = Field(..., description="Whether this parameter is mandatory for calculation")
    description: str = Field(..., description="Detailed description of the parameter and its clinical significance")
    options: Optional[List[str]] = Field(None, description="Valid options for string parameters (enum values)")
    validation: Optional[Dict[str, Any]] = Field(None, description="Validation rules including min/max values or enum constraints")
    unit: Optional[str] = Field(None, description="Unit of measurement for numeric parameters")


class ResultInfo(BaseModel):
    """Information about a score's calculated result"""
    name: str = Field(..., description="Name of the result variable")
    type: str = Field(..., description="Data type of the result (integer, float, string)")
    unit: str = Field(..., description="Unit of measurement or classification type")
    description: str = Field(..., description="Description of what the result represents clinically")


class InterpretationRange(BaseModel):
    """Interpretation range for score results with clinical significance"""
    min: float = Field(..., description="Minimum value of this interpretation range (inclusive)")
    max: Optional[float] = Field(None, description="Maximum value of this interpretation range (inclusive). Null means no upper limit.")
    stage: str = Field(..., description="Classification stage or risk level name")
    description: str = Field(..., description="Brief description of this stage or risk level")
    interpretation: str = Field(..., description="Detailed clinical interpretation and recommended actions for this range")


class Interpretation(BaseModel):
    """Model for score interpretations with clinical ranges"""
    ranges: List[InterpretationRange] = Field(..., description="Array of interpretation ranges with clinical significance")


class ScoreMetadataResponse(BaseModel):
    """
    Comprehensive metadata response for a medical score
    
    Provides complete information about a medical score including parameters, 
    interpretation ranges, references, and clinical notes.
    """
    id: str = Field(..., description="Unique identifier of the medical score")
    title: str = Field(..., description="Full title of the medical score")
    description: str = Field(..., description="Comprehensive description of the score's purpose and clinical application")
    category: str = Field(..., description="Medical specialty category")
    version: Optional[str] = Field(None, description="Version or year of the score")
    parameters: List[Parameter] = Field(..., description="Required parameters for calculation with validation rules")
    result: ResultInfo = Field(..., description="Information about the calculated result")
    interpretation: Interpretation = Field(..., description="Clinical interpretation ranges and recommendations")
    references: List[str] = Field(..., description="Scientific references and citations for the score")
    formula: str = Field(..., description="Mathematical formula or algorithm description")
    notes: List[str] = Field(..., description="Important clinical notes and considerations")


class ErrorResponse(BaseModel):
    """Standardized error response model"""
    error: str = Field(..., description="Error type classification")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error context and debugging information")
    
    class Config:
        schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid parameters provided",
                "details": {
                    "field": "age",
                    "value": 15,
                    "constraint": "must be >= 18"
                }
            }
        }


class HealthResponse(BaseModel):
    """Response for API health check endpoint"""
    status: str = Field(..., description="Current API operational status")
    message: str = Field(..., description="Status description message")
    version: str = Field(..., description="Current API version")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "message": "nobra_calculator API is running correctly",
                "version": "1.0.0"
            }
        }


class Cha2ds2VascRequest(BaseModel):
    """
    Request model for CHA₂DS₂-VASc Score calculation
    
    The CHA₂DS₂-VASc score predicts stroke risk in patients with non-valvular atrial fibrillation,
    helping clinicians make evidence-based decisions about anticoagulation therapy.
    
    **Clinical Use**:
    - Stroke risk stratification in atrial fibrillation
    - Anticoagulation therapy decision-making
    - Risk-benefit analysis for bleeding vs. thrombotic risk
    - Patient counseling and shared decision-making
    
    **Score Components**:
    - C: Congestive heart failure (1 point)
    - H: Hypertension (1 point)
    - A₂: Age ≥75 years (2 points)
    - D: Diabetes (1 point)
    - S₂: Previous Stroke/TIA/TE (2 points)
    - V: Vascular disease (1 point)
    - A: Age 65-74 years (1 point)
    - Sc: Sex category female (1 point)
    
    **Reference**: Lip GY, et al. Refining clinical risk stratification for predicting stroke and thromboembolism in atrial fibrillation. Chest. 2010;137(2):263-72.
    """
    age: int = Field(
        ..., 
        ge=18, 
        le=120, 
        description="Patient's age in years. Age contributes 0, 1, or 2 points: 0 points for <65 years, 1 point for 65-74 years, 2 points for ≥75 years.",
        example=75
    )
    sex: SexType = Field(
        ..., 
        description="Patient's biological sex. Female sex adds 1 point to the score, reflecting higher stroke risk in women with atrial fibrillation.",
        example="female"
    )
    congestive_heart_failure: bool = Field(
        ..., 
        description="History of congestive heart failure or left ventricular dysfunction (LVEF ≤40%). Adds 1 point if present.",
        example=True
    )
    hypertension: bool = Field(
        ..., 
        description="History of arterial hypertension (≥140/90 mmHg or on antihypertensive treatment). Adds 1 point if present.",
        example=True
    )
    stroke_tia_thromboembolism: bool = Field(
        ..., 
        description="Previous history of stroke, TIA (transient ischemic attack), or systemic thromboembolism. Adds 2 points if present - highest risk factor.",
        example=False
    )
    vascular_disease: bool = Field(
        ..., 
        description="Vascular disease including previous myocardial infarction, peripheral artery disease, or aortic plaque. Adds 1 point if present.",
        example=False
    )
    diabetes: bool = Field(
        ..., 
        description="History of diabetes mellitus (fasting glucose >125 mg/dL or on antidiabetic treatment). Adds 1 point if present.",
        example=True
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 75,
                "sex": "female",
                "congestive_heart_failure": True,
                "hypertension": True,
                "stroke_tia_thromboembolism": False,
                "vascular_disease": False,
                "diabetes": True
            }
        }


class Cha2ds2VascResponse(BaseModel):
    """
    Response model for CHA₂DS₂-VASc Score calculation
    
    Provides comprehensive stroke risk assessment with specific anticoagulation recommendations
    based on current guidelines from ESC, AHA/ACC, and other major cardiology societies.
    
    **Risk Stratification**:
    - Score 0 (men): Very low risk (0.3% annual stroke risk) - no anticoagulation
    - Score 1 (men): Low risk (0.9% annual stroke risk) - consider anticoagulation
    - Score ≥2: Moderate to high risk - anticoagulation recommended
    - Women with score 1 (sex only): No anticoagulation recommended
    
    **Anticoagulation Options**:
    - DOACs (Direct Oral Anticoagulants): dabigatran, rivaroxaban, apixaban, edoxaban
    - Warfarin with INR 2-3
    - Consider HAS-BLED score for bleeding risk assessment
    """
    result: int = Field(
        ..., 
        description="Total CHA₂DS₂-VASc score ranging from 0-9 points. Higher scores indicate increased stroke risk and stronger indication for anticoagulation.",
        example=5
    )
    unit: str = Field(
        ..., 
        description="Unit of the score result",
        example="points"
    )
    interpretation: str = Field(
        ..., 
        description="Evidence-based clinical interpretation with specific anticoagulation recommendations based on current guidelines.",
        example="Oral anticoagulation mandatory. Consider strategies to improve adherence and minimize bleeding risk."
    )
    stage: str = Field(
        ..., 
        description="Risk classification category (Very Low, Low, Moderate, High, Very High, Extreme Risk)",
        example="High Risk"
    )
    stage_description: str = Field(
        ..., 
        description="Description of the risk level with annual stroke risk percentage",
        example="Annual stroke risk: 10.0%"
    )
    annual_stroke_risk: str = Field(
        ..., 
        description="Estimated annual stroke risk percentage based on clinical studies and registry data",
        example="10.0%"
    )
    components: Dict[str, int] = Field(
        ..., 
        description="Breakdown of points contributed by each component of the score for transparency and clinical understanding",
        example={
            "congestive_heart_failure": 1,
            "hypertension": 1,
            "age_points": 2,
            "diabetes": 1,
            "stroke_tia": 0,
            "vascular_disease": 0,
            "sex_category": 1
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5,
                "unit": "points",
                "interpretation": "Oral anticoagulation mandatory. Consider strategies to improve adherence and minimize bleeding risk.",
                "stage": "High Risk",
                "stage_description": "Annual stroke risk: 10.0%",
                "annual_stroke_risk": "10.0%",
                "components": {
                    "congestive_heart_failure": 1,
                    "hypertension": 1,
                    "age_points": 2,
                    "diabetes": 1,
                    "stroke_tia": 0,
                    "vascular_disease": 0,
                    "sex_category": 1
                }
            }
        }


class Curb65Request(BaseModel):
    """
    Request model for CURB-65 Score calculation
    
    The CURB-65 score is a clinical prediction rule for assessing pneumonia severity and 
    guiding treatment decisions regarding hospitalization and antibiotic therapy.
    
    **Clinical Use**:
    - Pneumonia severity assessment
    - Hospitalization decision-making
    - ICU admission criteria
    - Antibiotic therapy guidance
    - Mortality risk prediction
    
    **Score Components**:
    - C: Confusion (new onset mental confusion)
    - U: Urea >19 mg/dL (>7 mmol/L)
    - R: Respiratory rate ≥30/min
    - B: Blood pressure (systolic <90 or diastolic ≤60 mmHg)
    - 65: Age ≥65 years
    
    **Reference**: Lim WS, et al. Defining community acquired pneumonia severity on presentation to hospital: an international derivation and validation study. Thorax. 2003;58(5):377-82.
    """
    confusion: bool = Field(
        ..., 
        description="Recent onset mental confusion defined as disorientation in time, place, or person. New confusion not attributable to other causes.",
        example=False
    )
    urea: float = Field(
        ..., 
        ge=0, 
        le=200, 
        description="Serum urea (BUN) concentration in mg/dL. Values ≥19 mg/dL (≥7 mmol/L) indicate renal impairment and add 1 point.",
        example=25.0
    )
    respiratory_rate: int = Field(
        ..., 
        ge=0, 
        le=60, 
        description="Respiratory rate in breaths per minute. Values ≥30/min indicate respiratory compromise and add 1 point.",
        example=32
    )
    systolic_bp: int = Field(
        ..., 
        ge=0, 
        le=300, 
        description="Systolic blood pressure in mmHg. Values <90 mmHg indicate hemodynamic instability.",
        example=85
    )
    diastolic_bp: int = Field(
        ..., 
        ge=0, 
        le=200, 
        description="Diastolic blood pressure in mmHg. Values ≤60 mmHg indicate hemodynamic instability.",
        example=55
    )
    age: int = Field(
        ..., 
        ge=0, 
        le=120, 
        description="Patient's age in years. Age ≥65 years adds 1 point, reflecting increased mortality risk in elderly patients.",
        example=78
    )
    
    @field_validator('diastolic_bp')
    def validate_blood_pressure(cls, v, info):
        if 'systolic_bp' in info.data and v > info.data['systolic_bp']:
            raise ValueError('Diastolic pressure cannot be greater than systolic pressure')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "confusion": False,
                "urea": 25.0,
                "respiratory_rate": 32,
                "systolic_bp": 85,
                "diastolic_bp": 55,
                "age": 78
            }
        }


class Curb65Response(BaseModel):
    """
    Response model for CURB-65 Score calculation
    
    Provides pneumonia severity assessment with evidence-based treatment recommendations
    and mortality risk stratification.
    
    **Management Guidelines**:
    - Score 0-1: Low risk (1.5% mortality) - outpatient treatment usually appropriate
    - Score 2: Moderate risk (9.2% mortality) - consider hospitalization
    - Score 3-5: High risk (22% mortality) - hospitalization recommended, consider ICU if ≥4
    
    **Antibiotic Recommendations**:
    - Outpatient: Oral antibiotics (amoxicillin, macrolides, fluoroquinolones)
    - Inpatient: IV antibiotics (beta-lactam + macrolide, fluoroquinolone)
    - ICU: Broad-spectrum IV antibiotics with anti-pseudomonal coverage if indicated
    """
    result: int = Field(
        ..., 
        description="Total CURB-65 score ranging from 0-5 points. Higher scores indicate increased severity and mortality risk.",
        example=3
    )
    unit: str = Field(
        ..., 
        description="Unit of the score result",
        example="points"
    )
    interpretation: str = Field(
        ..., 
        description="Evidence-based clinical interpretation with specific treatment recommendations including hospitalization and antibiotic therapy guidance.",
        example="Mandatory hospital admission. Consider ICU admission, especially if CURB-65 ≥ 4. Start intravenous antibiotic therapy immediately."
    )
    stage: str = Field(
        ..., 
        description="Risk classification (Low Risk, Moderate Risk, High Risk) based on mortality prediction",
        example="High Risk"
    )
    stage_description: str = Field(
        ..., 
        description="Description of the risk level with associated mortality percentage",
        example="Mortality: 22%"
    )
    mortality_risk: str = Field(
        ..., 
        description="Estimated mortality risk percentage based on validation studies",
        example="22%"
    )
    components: Dict[str, int] = Field(
        ..., 
        description="Breakdown of points contributed by each CURB-65 component for clinical transparency",
        example={
            "confusion": 0,
            "urea": 1,
            "respiratory_rate": 1,
            "blood_pressure": 1,
            "age": 1
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "Mandatory hospital admission. Consider ICU admission, especially if CURB-65 ≥ 4. Start intravenous antibiotic therapy immediately.",
                "stage": "High Risk",
                "stage_description": "Mortality: 22%",
                "mortality_risk": "22%",
                "components": {
                    "confusion": 0,
                    "urea": 1,
                    "respiratory_rate": 1,
                    "blood_pressure": 1,
                    "age": 1
                }
            }
        }


# ABCD² Score Models
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


class DiabetesType(str, Enum):
    """Enum for diabetes status"""
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


class FourTsRequest(BaseModel):
    """
    Request model for 4Ts Score calculation
    
    The 4Ts score assesses the probability of heparin-induced thrombocytopenia (HIT),
    a serious immune-mediated adverse reaction to heparin therapy.
    
    **Clinical Use**:
    - HIT probability assessment in heparin-exposed patients
    - Decision-making for heparin discontinuation
    - Alternative anticoagulation selection
    - Laboratory testing prioritization
    - Risk stratification for thrombotic complications
    
    **Score Components**:
    - Thrombocytopenia: Magnitude of platelet count fall and nadir
    - Timing: Onset timing relative to heparin exposure
    - Thrombosis: New thrombotic events or other sequelae
    - Other causes: Alternative explanations for thrombocytopenia
    
    **Reference**: Lo GK, et al. Evaluation of pretest clinical score (4 T's) for the diagnosis of heparin-induced thrombocytopenia in two clinical settings. J Thromb Haemost. 2006;4(4):759-65.
    """
    thrombocytopenia_severity: ThrombocytopeniaSeverityType = Field(
        ..., 
        description="Severity of thrombocytopenia based on platelet count fall and nadir. Greater falls and lower nadirs suggest higher HIT probability (2 points: >50% fall and nadir >20k; 1 point: 30-50% fall or nadir 10-19k; 0 points: <30% fall or nadir <10k).",
        example="fall_greater_50_nadir_greater_20"
    )
    timing_onset: TimingOnsetType = Field(
        ..., 
        description="Timing of platelet fall onset relative to heparin exposure. Classic HIT timing is 5-10 days after first exposure (2 points: typical timing; 1 point: possible timing; 0 points: unlikely timing).",
        example="onset_5_10_days_or_fall_1_day_heparin_30_days"
    )
    thrombosis_sequelae: ThrombosisSequelaeType = Field(
        ..., 
        description="Presence of thrombotic complications or other HIT sequelae. New thrombosis strongly suggests HIT (2 points: new thrombosis/skin necrosis/systemic reaction; 1 point: progressive/suspected thrombosis; 0 points: no thrombosis).",
        example="new_thrombosis_or_skin_necrosis_or_systemic_reaction"
    )
    other_causes: OtherCausesType = Field(
        ..., 
        description="Alternative explanations for thrombocytopenia. Absence of other causes increases HIT probability (2 points: no other cause; 1 point: possible other cause; 0 points: definitive other cause).",
        example="no_other_apparent_cause"
    )
    
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
    """
    Response model for 4Ts Score calculation
    
    Provides HIT probability assessment with specific management recommendations
    based on current hematology and thrombosis guidelines.
    
    **Probability & Management**:
    - Score 0-3: Low probability (<5%) - continue heparin, HIT testing not routinely needed
    - Score 4-5: Intermediate probability (~14%) - stop heparin, start alternative anticoagulant, HIT testing recommended
    - Score 6-8: High probability (~64%) - stop heparin immediately, start non-heparin anticoagulant, urgent HIT testing
    
    **Alternative Anticoagulants**:
    - Direct thrombin inhibitors: argatroban, bivalirudin
    - Factor Xa inhibitors: fondaparinux
    - Direct oral anticoagulants (DOACs) in select cases
    
    **Important**: Never use warfarin alone in acute HIT due to risk of venous limb gangrene
    """
    result: int = Field(
        ..., 
        description="Total 4Ts score ranging from 0-8 points. Higher scores indicate increased probability of heparin-induced thrombocytopenia.",
        example=7
    )
    unit: str = Field(
        ..., 
        description="Unit of the score result",
        example="points"
    )
    interpretation: str = Field(
        ..., 
        description="Evidence-based clinical interpretation with specific HIT management recommendations including heparin discontinuation and alternative anticoagulation guidance.",
        example="HIT probability ~64%. Immediately discontinue all heparin. Start non-heparin anticoagulant. Perform confirmatory tests for HIT."
    )
    stage: str = Field(
        ..., 
        description="HIT probability classification (Low Probability, Intermediate Probability, High Probability)",
        example="High Probability"
    )
    stage_description: str = Field(
        ..., 
        description="Description of the HIT probability level",
        example="High probability of HIT"
    )
    hit_probability: str = Field(
        ..., 
        description="Estimated HIT probability percentage based on validation studies",
        example="64%"
    )
    
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


# 4C Mortality Score Models
class UreaUnitType(str, Enum):
    """Enum for urea measurement units"""
    MMOL_L = "mmol_L"
    MG_DL = "mg_dL"


class FourCMortalityRequest(BaseModel):
    """
    Request model for 4C Mortality Score calculation
    
    The 4C Mortality Score predicts in-hospital mortality in patients with COVID-19,
    helping clinicians with risk stratification and treatment intensity decisions.
    
    **Clinical Use**:
    - COVID-19 mortality risk prediction
    - Hospital admission decision-making
    - ICU triage and resource allocation
    - Treatment intensity guidance
    - Patient and family counseling
    - Clinical trial stratification
    
    **Score Components**:
    - Age, sex, comorbidities
    - Respiratory rate, oxygen saturation
    - Glasgow Coma Scale
    - Urea, C-reactive protein
    
    **Reference**: Knight SR, et al. Risk stratification of patients admitted to hospital with covid-19 using the ISARIC WHO Clinical Characterisation Protocol: development and validation of the 4C Mortality Score. BMJ. 2020;370:m3339.
    """
    age: int = Field(
        ..., 
        ge=0, 
        le=120, 
        description="Patient's age in years. Age is the strongest predictor in the 4C score, with points increasing progressively: <50 years (0 points), 50-59 (2 points), 60-69 (4 points), 70-79 (6 points), ≥80 (7 points).",
        example=70
    )
    sex: SexType = Field(
        ..., 
        description="Patient's biological sex. Male sex adds 1 point, reflecting the observed higher mortality risk in men with COVID-19.",
        example="male"
    )
    comorbidities: int = Field(
        ..., 
        ge=0, 
        le=20, 
        description="Number of comorbidities from predefined list (chronic cardiac disease, chronic pulmonary disease, asthma, chronic kidney disease, mild/moderate/severe liver disease, dementia, chronic neurological conditions, connective tissue disease, diabetes, HIV/AIDS, malignancy). Each comorbidity adds 1 point.",
        example=2
    )
    respiratory_rate: int = Field(
        ..., 
        ge=5, 
        le=60, 
        description="Respiratory rate in breaths per minute. Higher rates indicate respiratory compromise: <20 (0 points), 20-29 (1 point), ≥30 (2 points).",
        example=24
    )
    oxygen_saturation: float = Field(
        ..., 
        ge=50.0, 
        le=100.0, 
        description="Peripheral oxygen saturation on room air or current oxygen therapy (%). Lower saturations indicate worse prognosis: >95% (0 points), 92-95% (2 points), <92% (3 points).",
        example=92.0
    )
    glasgow_coma_scale: int = Field(
        ..., 
        ge=3, 
        le=15, 
        description="Glasgow Coma Scale score. Lower scores indicate altered consciousness and worse prognosis: 15 (0 points), 12-14 (1 point), <12 (2 points).",
        example=15
    )
    urea_unit: UreaUnitType = Field(
        ..., 
        description="Unit for urea measurement. Can be mmol/L (standard international unit) or mg/dL (US unit). Conversion: mg/dL = mmol/L × 2.8.",
        example="mg_dL"
    )
    urea_value: float = Field(
        ..., 
        ge=0.1, 
        le=300.0, 
        description="Serum urea value. Elevated urea indicates renal impairment and worse prognosis. Points based on units: mmol/L (<7=0, 7-14=1, >14=3) or mg/dL (<19.6=0, 19.6-39.2=1, >39.2=3).",
        example=45.0
    )
    crp: float = Field(
        ..., 
        ge=0.0, 
        le=1000.0, 
        description="C-reactive protein in mg/L. Elevated CRP indicates systemic inflammation: <50 mg/L (0 points), 50-99 (1 point), ≥100 (2 points).",
        example=80.0
    )
    
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
    """
    Response model for 4C Mortality Score calculation
    
    Provides comprehensive COVID-19 mortality risk assessment with evidence-based
    management recommendations and resource allocation guidance.
    
    **Risk Stratification & Management**:
    - Score 0-3: Low risk (1.2% mortality) - standard ward care, monitor for deterioration
    - Score 4-8: Intermediate risk (9.9% mortality) - enhanced monitoring, consider high-dependency unit
    - Score 9-14: High risk (31.4% mortality) - intensive monitoring, consider ICU evaluation
    - Score ≥15: Very high risk (61.5% mortality) - ICU-level care, advanced life support planning
    
    **Clinical Actions**:
    - Corticosteroids (dexamethasone) for patients requiring oxygen
    - Remdesivir consideration in appropriate patients
    - Thromboprophylaxis for all hospitalized patients
    - Early identification of complications (ARDS, secondary infections)
    """
    result: int = Field(
        ..., 
        description="Total 4C score ranging from 0-21 points. Higher scores indicate progressively increased in-hospital mortality risk from COVID-19.",
        example=10
    )
    unit: str = Field(
        ..., 
        description="Unit of the score result",
        example="points"
    )
    interpretation: str = Field(
        ..., 
        description="Evidence-based clinical interpretation with specific mortality risk and management recommendations based on current COVID-19 treatment guidelines.",
        example="In-hospital mortality of 31.4-34.9%. Patients require intensive care or high-dependency unit monitoring."
    )
    stage: str = Field(
        ..., 
        description="Mortality risk classification (Low Risk, Intermediate Risk, High Risk, Very High Risk)",
        example="High Risk"
    )
    stage_description: str = Field(
        ..., 
        description="Description of the mortality risk level",
        example="High mortality risk"
    )
    mortality_risk: str = Field(
        ..., 
        description="Estimated in-hospital mortality risk percentage based on large validation cohorts",
        example="31.4-34.9%"
    )
    
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


# 6 Minute Walk Distance Models
class SixMinuteWalkRequest(BaseModel):
    """
    Request model for 6-Minute Walk Distance calculation
    
    The 6-minute walk test (6MWT) is a standardized exercise test that assesses functional
    capacity and cardiopulmonary fitness, providing reference values for comparison.
    
    **Clinical Use**:
    - Functional capacity assessment
    - Cardiopulmonary disease monitoring
    - Pre-operative risk stratification
    - Pulmonary rehabilitation outcomes
    - Heart failure assessment
    - Disability evaluation
    - Treatment response monitoring
    
    **Test Protocol**:
    - 30-meter flat corridor
    - Patient walks at own pace for 6 minutes
    - Encouragement every 2 minutes
    - Oxygen saturation and symptoms monitored
    - Distance measured in meters
    
    **Reference**: ATS Committee on Proficiency Standards for Clinical Pulmonary Function Laboratories. ATS statement: guidelines for the six-minute walk test. Am J Respir Crit Care Med. 2002;166(1):111-7.
    """
    age: int = Field(
        ..., 
        ge=18, 
        le=100, 
        description="Patient's age in years. Age significantly affects predicted walking distance, with progressive decline expected with aging.",
        example=65
    )
    sex: SexType = Field(
        ..., 
        description="Patient's biological sex. Men typically have higher predicted walking distances than women due to differences in muscle mass and cardiovascular capacity.",
        example="male"
    )
    height: float = Field(
        ..., 
        ge=120.0, 
        le=220.0, 
        description="Patient's height in centimeters. Taller individuals typically have longer stride length and higher predicted distances.",
        example=175.0
    )
    weight: float = Field(
        ..., 
        ge=30.0, 
        le=200.0, 
        description="Patient's weight in kilograms. Higher weight may limit walking distance due to increased metabolic demand.",
        example=80.0
    )
    observed_distance: Optional[float] = Field(
        None, 
        ge=0.0, 
        le=1000.0, 
        description="Optional: Actual distance walked in meters during the 6MWT. If provided, percentage of predicted will be calculated for comparison with reference values.",
        example=450.0
    )
    
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
    """
    Response model for 6-Minute Walk Distance calculation
    
    Provides predicted walking distance with comprehensive functional capacity interpretation
    and comparison with age-, sex-, and anthropometry-matched reference values.
    
    **Interpretation Guidelines**:
    - >80% of predicted: Normal functional capacity
    - 60-80% of predicted: Mild functional limitation
    - 40-60% of predicted: Moderate functional limitation
    - <40% of predicted: Severe functional limitation
    
    **Clinical Significance**:
    - Distances <350m associated with increased mortality in heart failure
    - >50m improvement clinically significant in pulmonary rehabilitation
    - Lower limit of normal helps identify pathological reduction
    """
    result: float = Field(
        ..., 
        description="Predicted 6-minute walk distance in meters based on age, sex, height, and weight using validated reference equations.",
        example=485.3
    )
    unit: str = Field(
        ..., 
        description="Unit of measurement for walking distance",
        example="meters"
    )
    interpretation: str = Field(
        ..., 
        description="Comprehensive interpretation of functional capacity based on predicted values and observed performance if provided.",
        example="Distance within expected values for age, sex, height, and weight. Indicates preserved functional capacity."
    )
    stage: str = Field(
        ..., 
        description="Functional capacity classification (Normal, Mild Limitation, Moderate Limitation, Severe Limitation)",
        example="Normal"
    )
    stage_description: str = Field(
        ..., 
        description="Description of the functional capacity level",
        example="Normal functional capacity"
    )
    lower_limit_normal: float = Field(
        ..., 
        description="Lower limit of normal walking distance in meters (typically predicted distance minus 1.96 × standard error). Values below this suggest pathological limitation.",
        example=332.3
    )
    percentage_predicted: Optional[float] = Field(
        None, 
        description="Percentage of predicted distance achieved (only calculated if observed distance is provided). Values >80% are typically considered normal.",
        example=92.7
    )
    
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


# A-a O2 Gradient Models
class AAO2GradientRequest(BaseModel):
    """
    Request model for Alveolar-Arterial Oxygen Gradient calculation
    
    The A-a O₂ gradient assesses pulmonary gas exchange efficiency by comparing
    alveolar and arterial oxygen partial pressures, helping diagnose lung disease.
    
    **Clinical Use**:
    - Pulmonary gas exchange assessment
    - Differential diagnosis of hypoxemia
    - Monitoring lung disease progression
    - Ventilator management guidance
    - Pulmonary embolism evaluation
    - Interstitial lung disease assessment
    
    **Physiology**:
    - Normal gradient increases with age: ~2.5 + (0.21 × age)
    - Elevated gradient suggests V/Q mismatch, shunt, or diffusion limitation
    - Normal gradient with hypoxemia suggests hypoventilation or low FiO₂
    
    **Reference**: Mellemgaard K. The alveolar-arterial oxygen difference: its size and components in normal man. Acta Physiol Scand. 1966;67(1):10-20.
    """
    age: int = Field(
        ..., 
        ge=1, 
        le=120, 
        description="Patient's age in years. Age is crucial for interpreting A-a gradient as normal values increase with aging due to physiological changes in lung mechanics.",
        example=45
    )
    fio2: float = Field(
        ..., 
        ge=0.21, 
        le=1.0, 
        description="Fraction of inspired oxygen (0.21 for room air, up to 1.0 for 100% oxygen). Higher FiO₂ increases alveolar oxygen and affects gradient calculation.",
        example=0.21
    )
    paco2: float = Field(
        ..., 
        ge=10.0, 
        le=100.0, 
        description="Arterial carbon dioxide partial pressure in mmHg from arterial blood gas. Used to calculate alveolar oxygen pressure via the alveolar gas equation.",
        example=40.0
    )
    pao2: float = Field(
        ..., 
        ge=30.0, 
        le=600.0, 
        description="Arterial oxygen partial pressure in mmHg from arterial blood gas. This is subtracted from calculated alveolar oxygen to determine the gradient.",
        example=90.0
    )
    patm: Optional[float] = Field(
        760.0, 
        ge=500.0, 
        le=800.0, 
        description="Atmospheric pressure in mmHg. Standard is 760 mmHg at sea level, but adjustments needed for altitude (decreases ~19 mmHg per 1000 feet elevation).",
        example=760.0
    )
    respiratory_quotient: Optional[float] = Field(
        0.8, 
        ge=0.7, 
        le=1.0, 
        description="Respiratory quotient (CO₂ production/O₂ consumption ratio). Typically 0.8 on mixed diet, 0.7 on fat diet, 1.0 on carbohydrate diet.",
        example=0.8
    )
    
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
    """
    Response model for Alveolar-Arterial Oxygen Gradient calculation
    
    Provides comprehensive pulmonary gas exchange assessment with age-adjusted
    interpretation and clinical guidance for hypoxemia evaluation.
    
    **Normal Values**:
    - Young adults (20-30 years): 5-10 mmHg
    - Middle age (40-50 years): 10-15 mmHg  
    - Elderly (>70 years): 15-25 mmHg
    - Formula: Expected A-a gradient = 2.5 + (0.21 × age)
    
    **Clinical Interpretation**:
    - Normal gradient + hypoxemia = hypoventilation or low FiO₂
    - Elevated gradient + hypoxemia = lung disease (V/Q mismatch, shunt, diffusion defect)
    - Massive elevation (>50 mmHg on room air) suggests severe lung pathology
    """
    result: float = Field(
        ..., 
        description="Calculated alveolar-arterial oxygen gradient in mmHg. Normal values increase with age, typically 5-10 mmHg in young adults, up to 25 mmHg in elderly.",
        example=15.2
    )
    unit: str = Field(
        ..., 
        description="Unit of measurement for the oxygen gradient",
        example="mmHg"
    )
    interpretation: str = Field(
        ..., 
        description="Clinical interpretation of the A-a gradient with age-adjusted normal values and assessment of pulmonary gas exchange efficiency.",
        example="Preserved alveolar function. Normal values for young adults are 5-10 mmHg, which may increase with age."
    )
    stage: str = Field(
        ..., 
        description="Gradient classification (Normal, Mildly Elevated, Moderately Elevated, Severely Elevated)",
        example="Normal"
    )
    stage_description: str = Field(
        ..., 
        description="Description of the A-a gradient status",
        example="Normal A-a gradient"
    )
    pao2_alveolar: float = Field(
        ..., 
        description="Calculated alveolar oxygen partial pressure in mmHg using the alveolar gas equation: PAO₂ = (FiO₂ × (Patm - 47)) - (PaCO₂ / RQ).",
        example=105.2
    )
    age_adjusted_normal: float = Field(
        ..., 
        description="Age-adjusted upper limit of normal A-a gradient in mmHg using the formula: 2.5 + (0.21 × age).",
        example=15.25
    )
    
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


# AAS Models
class YesNoType(str, Enum):
    """Enum for yes/no responses"""
    YES = "yes"
    NO = "no"


class YesNoNAType(str, Enum):
    """Enum for yes/no/not applicable responses"""
    YES = "yes"
    NO = "no"
    NOT_APPLICABLE = "not_applicable"


class AasRequest(BaseModel):
    """
    Request model for Abuse Assessment Screen (AAS)
    
    The AAS is a validated screening tool for identifying domestic violence and intimate
    partner violence in healthcare settings, particularly effective in emergency and
    prenatal care environments.
    
    **Clinical Use**:
    - Domestic violence screening in healthcare settings
    - Intimate partner violence identification
    - Emergency department risk assessment
    - Prenatal care safety evaluation
    - Primary care routine screening
    - Mental health assessment context
    
    **Implementation Guidelines**:
    - Conduct screening in private, confidential setting
    - Ensure patient safety and privacy
    - Have resources and referrals readily available
    - Document carefully with attention to legal implications
    - Follow mandatory reporting requirements per jurisdiction
    
    **Reference**: Soeken KL, et al. The abuse assessment screen: a clinical instrument to measure frequency, severity, and perpetrator of abuse against women. In: Campbell JC, editor. Empowering survivors of abuse. Thousand Oaks, CA: Sage; 1998.
    """
    emotional_physical_abuse: YesNoType = Field(
        ..., 
        description="Have you ever been emotionally or physically abused by your partner or someone important to you? This broad question screens for any history of intimate partner violence.",
        example="no"
    )
    physical_hurt_recently: YesNoType = Field(
        ..., 
        description="Within the last year (or since your last visit), have you been hit, slapped, kicked, or otherwise physically hurt by someone? This assesses recent physical violence.",
        example="no"
    )
    physical_hurt_pregnancy: YesNoNAType = Field(
        ..., 
        description="Since you've been pregnant (or if not applicable, select 'not_applicable'), have you been hit, slapped, kicked, or otherwise physically hurt by someone? Violence during pregnancy poses risks to both mother and fetus.",
        example="not_applicable"
    )
    sexual_abuse: YesNoType = Field(
        ..., 
        description="Within the last year, has anyone forced you to have sexual activities that you did not want? This screens for sexual violence and coercion.",
        example="no"
    )
    afraid_of_partner: YesNoType = Field(
        ..., 
        description="Are you afraid of your partner or anyone you listed above? Fear indicates ongoing threat and immediate safety concerns.",
        example="no"
    )
    
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
    """
    Response model for Abuse Assessment Screen (AAS)
    
    Provides domestic violence screening results with appropriate clinical guidance
    and resource information for both positive and negative screens.
    
    **Positive Screen Actions**:
    - Ensure immediate safety and privacy
    - Provide validation and support
    - Offer resources (hotlines, shelters, counseling)
    - Safety planning if appropriate
    - Documentation per institutional policy
    - Follow mandatory reporting laws
    
    **Negative Screen Actions**:
    - Provide information about available resources
    - Normalize the screening process
    - Encourage future disclosure if situations change
    - Document negative screen appropriately
    
    **Resources**:
    - National Domestic Violence Hotline: 1-800-799-7233
    - Local law enforcement and emergency services
    - Community domestic violence programs
    - Legal advocacy services
    """
    result: str = Field(
        ..., 
        description="Overall AAS screening result indicating presence or absence of domestic violence indicators (Positive/Negative).",
        example="Negative"
    )
    unit: str = Field(
        ..., 
        description="Unit of the screening result",
        example="result"
    )
    interpretation: str = Field(
        ..., 
        description="Clinical interpretation with appropriate guidance for follow-up actions, resource provision, and safety considerations based on screening results.",
        example="Negative result for domestic violence. Continue to offer support and information about available resources."
    )
    stage: str = Field(
        ..., 
        description="Screening result classification (Positive Screening, Negative Screening)",
        example="Negative Screening"
    )
    stage_description: str = Field(
        ..., 
        description="Description of the screening outcome",
        example="No indication of domestic abuse"
    )
    positive_responses_count: int = Field(
        ..., 
        description="Number of questions answered positively, providing quantitative assessment of abuse indicators.",
        example=0
    )
    is_positive: bool = Field(
        ..., 
        description="Boolean indicator of whether the screening is considered positive (any 'yes' response typically indicates positive screen).",
        example=False
    )
    
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


# AAP Pediatric Hypertension Models
class AapPediatricHypertensionRequest(BaseModel):
    """
    Request model for AAP Pediatric Hypertension Classification
    
    The AAP 2017 guidelines provide updated blood pressure classification for children and
    adolescents, incorporating height percentiles and age-specific thresholds.
    
    **Clinical Use**:
    - Pediatric blood pressure classification
    - Hypertension screening in children
    - Risk stratification for cardiovascular complications
    - Treatment decision-making
    - Long-term cardiovascular risk assessment
    - School and sports physical evaluations
    
    **Classification System**:
    - Normal: <90th percentile for age, sex, and height
    - Elevated: 90th to <95th percentile or 120/80 to <95th percentile
    - Stage 1 HTN: 95th percentile to <95th percentile + 12 mmHg or 130/80-139/89 mmHg
    - Stage 2 HTN: ≥95th percentile + 12 mmHg or ≥140/90 mmHg
    
    **Reference**: Flynn JT, et al. Clinical Practice Guideline for Screening and Management of High Blood Pressure in Children and Adolescents. Pediatrics. 2017;140(3):e20171904.
    """
    age: int = Field(
        ..., 
        ge=1, 
        le=17, 
        description="Patient's age in years (1-17 years). Age is crucial for determining appropriate percentile-based thresholds.",
        example=10
    )
    sex: SexType = Field(
        ..., 
        description="Patient's biological sex. Sex-specific percentile tables are used for accurate BP classification in pediatric patients.",
        example="male"
    )
    height: float = Field(
        ..., 
        ge=70.0, 
        le=200.0, 
        description="Patient's height in centimeters. Height percentile is essential for determining BP percentiles as taller children have higher normal BP values.",
        example=140.0
    )
    systolic_bp: int = Field(
        ..., 
        ge=60, 
        le=200, 
        description="Systolic blood pressure in mmHg. Should be measured with appropriate cuff size and after 5 minutes of rest.",
        example=110
    )
    diastolic_bp: int = Field(
        ..., 
        ge=30, 
        le=150, 
        description="Diastolic blood pressure in mmHg. For children <13 years, use Korotkoff phase IV; for ≥13 years, use phase V.",
        example=70
    )
    
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
    """
    Response model for AAP Pediatric Hypertension Classification
    
    Provides comprehensive pediatric blood pressure assessment with age-, sex-, and 
    height-adjusted percentiles and evidence-based management recommendations.
    
    **Management Guidelines**:
    - Normal: Routine screening, lifestyle counseling
    - Elevated: Lifestyle modifications, repeat measurements, annual follow-up
    - Stage 1 HTN: Lifestyle modifications, consider medication if target organ damage
    - Stage 2 HTN: Lifestyle modifications + antihypertensive medication
    
    **Follow-up Recommendations**:
    - Normal/Elevated: Annual screening
    - Stage 1: 1-2 week follow-up, then 3-month intervals
    - Stage 2: 1 week follow-up, then monthly until controlled
    
    **Lifestyle Modifications**:
    - Weight management if overweight/obese
    - DASH diet principles
    - Regular physical activity (60 min/day)
    - Limit sodium intake
    - Adequate sleep duration
    """
    result: str = Field(
        ..., 
        description="Pediatric blood pressure classification based on AAP 2017 guidelines (Normal, Elevated, Stage 1 Hypertension, Stage 2 Hypertension).",
        example="Normal"
    )
    unit: str = Field(
        ..., 
        description="Unit of the classification result",
        example="classification"
    )
    interpretation: str = Field(
        ..., 
        description="Evidence-based clinical interpretation with specific management recommendations including lifestyle modifications and follow-up guidance.",
        example="BP below the 90th percentile for age, sex, and height. No specific intervention required."
    )
    stage: str = Field(
        ..., 
        description="Blood pressure stage classification according to AAP guidelines",
        example="Normal"
    )
    stage_description: str = Field(
        ..., 
        description="Detailed description of the blood pressure stage with clinical implications",
        example="Normal blood pressure"
    )
    systolic_percentile: float = Field(
        ..., 
        description="Systolic blood pressure percentile for age, sex, and height. Values help determine exact classification and tracking over time.",
        example=75.2
    )
    diastolic_percentile: float = Field(
        ..., 
        description="Diastolic blood pressure percentile for age, sex, and height. Used in conjunction with systolic percentile for classification.",
        example=68.5
    )
    
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


# Abbey Pain Scale Models
class AbbeyPainRequest(BaseModel):
    """
    Request model for Abbey Pain Scale calculation
    
    The Abbey Pain Scale is a validated tool for assessing pain in people with dementia
    who cannot verbally communicate their pain experience.
    
    **Clinical Use**:
    - Pain assessment in dementia patients
    - Non-verbal pain evaluation
    - Monitoring pain management effectiveness
    - Care planning in aged care facilities
    - Quality of life assessment
    - Medication adjustment guidance
    
    **Assessment Domains**:
    1. Vocalization (whimpering, groaning, crying)
    2. Facial expression (grimacing, frowning, distorted expressions)
    3. Body language (guarding, rigidity, fidgeting, withdrawal)
    4. Behavioral change (increased confusion, refusing food, alteration in usual patterns)
    5. Physiological change (temperature, pulse, blood pressure changes, perspiring, flushing/pallor)
    6. Physical change (skin tears, pressure areas, arthritis, contractures, previous injuries)
    
    **Scoring**: Each domain scored 0-3 (0=absent, 1=mild, 2=moderate, 3=severe)
    
    **Reference**: Abbey J, et al. The Abbey pain scale: a 1-minute numerical indicator for people with end-stage dementia. Int J Palliat Nurs. 2004;10(1):6-13.
    """
    vocalization: int = Field(
        ..., 
        ge=0, 
        le=3, 
        description="Vocalization assessment (0=absent, 1=occasional moaning/groaning, 2=repeated calling out/noisy breathing, 3=loud moaning/crying/distressed sounds). Includes whimpering, groaning, crying.",
        example=1
    )
    facial_expression: int = Field(
        ..., 
        ge=0, 
        le=3, 
        description="Facial expression assessment (0=serene/peaceful, 1=sad/frightened/frown, 2=facial grimacing, 3=facial grimacing with jaw clenching). Look for grimacing, frowning, distorted expressions.",
        example=2
    )
    body_language: int = Field(
        ..., 
        ge=0, 
        le=3, 
        description="Body language assessment (0=relaxed, 1=tense/distressed pacing/fidgeting, 2=rigid/fists clenched/knees pulled up/pulling away, 3=rigid/fists clenched/knees pulled up/striking out). Includes guarding, rigidity, withdrawal.",
        example=1
    )
    behavioral_change: int = Field(
        ..., 
        ge=0, 
        le=3, 
        description="Behavioral change assessment (0=no change, 1=increase in confusion/refusing medication, 2=alteration in behavior patterns/aggressive/withdrawn, 3=crying/increased confusion/agitation). Changes from usual patterns.",
        example=0
    )
    physiological_change: int = Field(
        ..., 
        ge=0, 
        le=3, 
        description="Physiological change assessment (0=no change, 1=pale/flushed/diaphoretic, 2=breathing changes/hyperventilation, 3=fever/blood pressure changes). Temperature, pulse, BP changes, perspiring, flushing/pallor.",
        example=1
    )
    physical_change: int = Field(
        ..., 
        ge=0, 
        le=3, 
        description="Physical change assessment (0=no physical changes, 1=skin tears/pressure sores/lesions/cuts/bruises, 2=limping/arthritis/contractures, 3=previous injuries/surgery). Skin tears, pressure areas, arthritis, contractures.",
        example=0
    )
    
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
    """
    Response model for Abbey Pain Scale calculation
    
    Provides comprehensive pain assessment for dementia patients with evidence-based
    interpretation and management recommendations.
    
    **Pain Classification**:
    - Score 0-2: No pain - continue routine monitoring
    - Score 3-7: Mild pain - consider non-pharmacological interventions
    - Score 8-13: Moderate pain - analgesics and non-pharmacological approaches
    - Score 14-18: Severe pain - immediate pain management, consider specialist referral
    
    **Management Strategies**:
    - Non-pharmacological: repositioning, comfort measures, environmental modifications
    - Mild pain: paracetamol, topical analgesics, heat/cold therapy
    - Moderate pain: regular analgesics, consider opioids for breakthrough pain
    - Severe pain: regular opioids, specialist pain management consultation
    
    **Monitoring Recommendations**:
    - Reassess after interventions (15-30 minutes for medications)
    - Document response to treatments
    - Regular reassessment (every 4-8 hours or as needed)
    """
    result: int = Field(
        ..., 
        description="Total Abbey Pain Scale score ranging from 0-18 points. Higher scores indicate more severe pain requiring more intensive management.",
        example=5
    )
    unit: str = Field(
        ..., 
        description="Unit of the score result",
        example="points"
    )
    interpretation: str = Field(
        ..., 
        description="Evidence-based interpretation of pain intensity with specific management recommendations appropriate for dementia care settings.",
        example="Mild pain present. Monitor and consider non-pharmacological interventions."
    )
    stage: str = Field(
        ..., 
        description="Pain intensity classification (No Pain, Mild Pain, Moderate Pain, Severe Pain)",
        example="Mild Pain"
    )
    stage_description: str = Field(
        ..., 
        description="Description of the pain intensity level with clinical implications",
        example="Mild pain"
    )
    pain_present: bool = Field(
        ..., 
        description="Boolean indicator of whether clinically significant pain is present (typically score ≥3 indicates pain presence).",
        example=True
    )
    
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


# ABIC Score Models
class AbicScoreRequest(BaseModel):
    """
    Request model for ABIC Score calculation
    
    The ABIC (Age, serum Bilirubin, INR, serum Creatinine) score predicts 90-day and 
    1-year survival in patients with alcoholic hepatitis, helping guide treatment decisions.
    
    **Clinical Use**:
    - Prognosis assessment in alcoholic hepatitis
    - Treatment intensity decision-making
    - Patient counseling regarding outcomes
    - Clinical trial stratification
    - Resource allocation decisions
    - Liver transplant evaluation timing
    
    **Score Components**:
    - Age (years)
    - Serum bilirubin (mg/dL)
    - INR (International Normalized Ratio)
    - Serum creatinine (mg/dL)
    
    **Reference**: Dominguez M, et al. A new scoring system for prognostic stratification of patients with alcoholic hepatitis. Am J Gastroenterol. 2008;103(11):2747-56.
    """
    age: int = Field(
        ..., 
        ge=18, 
        le=100, 
        description="Patient's age in years. Older age is associated with worse prognosis in alcoholic hepatitis.",
        example=50
    )
    serum_bilirubin: float = Field(
        ..., 
        ge=0.1, 
        le=50.0, 
        description="Total serum bilirubin concentration in mg/dL. Elevated bilirubin reflects severity of hepatic dysfunction and cholestasis.",
        example=8.5
    )
    serum_creatinine: float = Field(
        ..., 
        ge=0.1, 
        le=20.0, 
        description="Serum creatinine concentration in mg/dL. Elevated creatinine indicates renal dysfunction, often hepatorenal syndrome in severe cases.",
        example=1.2
    )
    inr: float = Field(
        ..., 
        ge=0.5, 
        le=10.0, 
        description="International Normalized Ratio reflecting coagulation status. Elevated INR indicates impaired hepatic synthetic function.",
        example=2.1
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 50,
                "serum_bilirubin": 8.5,
                "serum_creatinine": 1.2,
                "inr": 2.1
            }
        }


class AbicScoreResponse(BaseModel):
    """Response model for ABIC Score"""
    result: float = Field(..., description="Total ABIC score")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Prognostic interpretation")
    stage: str = Field(..., description="Risk classification")
    stage_description: str = Field(..., description="Prognosis description")
    survival_90_days: str = Field(..., description="90-day survival")
    survival_1_year: str = Field(..., description="1-year survival")
    
    class Config:
        schema_extra = {
            "example": {
                "result": 7.5,
                "unit": "points",
                "interpretation": "90-day survival: 70%. 1-year survival: 64.3%.",
                "stage": "Intermediate Risk",
                "stage_description": "Moderate survival",
                "survival_90_days": "70%",
                "survival_1_year": "64.3%"
            }
        }


# ALC Models
class AlcRequest(BaseModel):
    """Request model for ALC (Absolute Lymphocyte Count)"""
    white_blood_cells: float = Field(..., ge=0.1, le=500.0, description="White blood cell count (x10³/μL)")
    lymphocyte_percentage: float = Field(..., ge=0.0, le=100.0, description="Lymphocyte percentage (%)")
    
    class Config:
        schema_extra = {
            "example": {
                "white_blood_cells": 6.5,
                "lymphocyte_percentage": 25.0
            }
        }


class AlcResponse(BaseModel):
    """Response model for ALC"""
    result: float = Field(..., description="Absolute lymphocyte count (x10³/μL)")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Clinical interpretation")
    stage: str = Field(..., description="Count classification")
    stage_description: str = Field(..., description="Status description")
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1.625,
                "unit": "x10³/μL",
                "interpretation": "Normal lymphocyte count. Immune system functioning adequately.",
                "stage": "Normal",
                "stage_description": "Normal lymphocyte count"
            }
        }


# ANC Models  
class AncRequest(BaseModel):
    """Request model for ANC (Absolute Neutrophil Count)"""
    white_blood_cells: float = Field(..., ge=0.1, le=500.0, description="White blood cell count (x10³/μL)")
    neutrophil_percentage: float = Field(..., ge=0.0, le=100.0, description="Neutrophil percentage (%)")
    band_percentage: Optional[float] = Field(0.0, ge=0.0, le=100.0, description="Band percentage (%) - optional")
    
    class Config:
        schema_extra = {
            "example": {
                "white_blood_cells": 6.5,
                "neutrophil_percentage": 60.0,
                "band_percentage": 5.0
            }
        }


class AncResponse(BaseModel):
    """Response model for ANC"""
    result: float = Field(..., description="Absolute neutrophil count (x10³/μL)")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Clinical interpretation")
    stage: str = Field(..., description="Neutropenia classification")
    stage_description: str = Field(..., description="Description of neutropenia degree")
    infection_risk: str = Field(..., description="Infection risk")
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4.225,
                "unit": "x10³/μL",
                "interpretation": "Normal neutrophil count. Low infection risk.",
                "stage": "Normal",
                "stage_description": "Normal count",
                "infection_risk": "Low"
            }
        }


# ACC/AHA HF Staging Models
class HospitalizationFrequencyType(str, Enum):
    """Enum for hospitalization frequency"""
    FREQUENT = "frequent"
    RARE = "rare"
    NONE = "none"


class AccAhaHfStagingRequest(BaseModel):
    """Request model for ACC/AHA HF Staging"""
    risk_factors: YesNoType = Field(..., description="Presence of risk factors for heart failure")
    structural_disease: YesNoType = Field(..., description="Evidence of structural heart disease or elevated biomarkers")
    current_symptoms: YesNoType = Field(..., description="Current or previous symptoms of heart failure")
    advanced_symptoms: YesNoType = Field(..., description="Severe symptoms refractory to optimized treatment")
    hospitalization_frequency: HospitalizationFrequencyType = Field(..., description="Recurrent hospitalizations for heart failure")
    ejection_fraction: Optional[float] = Field(None, ge=0.0, le=100.0, description="Left ventricular ejection fraction (%)")
    
    class Config:
        schema_extra = {
            "example": {
                "risk_factors": "yes",
                "structural_disease": "yes",
                "current_symptoms": "no",
                "advanced_symptoms": "no",
                "hospitalization_frequency": "none",
                "ejection_fraction": 45.0
            }
        }


class AccAhaHfStagingResponse(BaseModel):
    """Response model for ACC/AHA HF Staging"""
    result: str = Field(..., description="Heart failure stage")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Interpretation and therapeutic recommendations")
    stage: str = Field(..., description="HF stage")
    stage_description: str = Field(..., description="Description of the stage")
    therapy_recommendations: Dict[str, Any] = Field(..., description="Detailed therapeutic recommendations")
    prognosis: Dict[str, str] = Field(..., description="Prognostic assessment")
    ejection_fraction: Optional[float] = Field(None, description="Provided ejection fraction")
    can_regress: bool = Field(..., description="Whether the patient can regress to previous stages")
    
    class Config:
        schema_extra = {
            "example": {
                "result": "B",
                "unit": "stage",
                "interpretation": "Structural disease without symptoms. Recommendations: ACEI/ARB, beta-blockers, statins, ICD if indicated (LVEF ≤30% post-MI). Goal: prevent progression to symptomatic HF.",
                "stage": "Stage B",
                "stage_description": "Pre-heart failure",
                "therapy_recommendations": {
                    "primary": ["ACEI or ARB (LVEF ≤40%)", "Evidence-based beta-blockers"],
                    "devices": ["ICD if LVEF ≤30% post-MI (>40 days)"]
                },
                "prognosis": {
                    "outlook": "Good with optimized treatment",
                    "mortality": "Low to moderate"
                },
                "ejection_fraction": 45.0,
                "can_regress": False
            }
        }


# EULAR/ACR PMR Models  
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
    """Request model for EULAR/ACR PMR Criteria"""
    morning_stiffness: MorningStiffnessType = Field(..., description="Duration of morning stiffness")
    hip_pain_limited_rom: HipPainRomType = Field(..., description="Hip pain or limited range of motion")
    rf_or_acpa: RfAcpaType = Field(..., description="Rheumatoid factor (RF) or anti-citrullinated peptide antibody (ACPA)")
    other_joint_pain: OtherJointPainType = Field(..., description="Pain in other joints")
    ultrasound_shoulder_hip: Optional[UltrasoundType] = Field(UltrasoundType.NOT_PERFORMED, description="At least one shoulder with specific findings and one hip with synovitis (ultrasound)")
    ultrasound_both_shoulders: Optional[UltrasoundType] = Field(UltrasoundType.NOT_PERFORMED, description="Both shoulders with specific findings (ultrasound)")
    
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
    """Response model for EULAR/ACR PMR"""
    result: int = Field(..., description="Total EULAR/ACR PMR score")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Diagnostic interpretation")
    stage: str = Field(..., description="Diagnostic result")
    stage_description: str = Field(..., description="Description of the result")
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": "Score ≥4 suggests a diagnosis of polymyalgia rheumatica.",
                "stage": "Probable PMR",
                "stage_description": "PMR diagnosis is probable",
                "diagnosis_likely": True
            }
        }


# Four AT Models
# 4AT Enums
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
    """Request model for 4AT (4 A's Test)"""
    alertness: AlertnessType = Field(..., description="Patient's alertness level")
    amt4_errors: int = Field(..., ge=0, le=4, description="Number of errors in AMT4 (age, date of birth, place, current year)")
    attention_months: AttentionMonthsType = Field(..., description="Performance on attention test (months in reverse order)")
    acute_change: AcuteChangeType = Field(..., description="Presence of acute change or fluctuating course")
    
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
    """Response model for 4AT"""
    result: int = Field(..., description="Total 4AT score (0-12)")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Delirium interpretation")
    stage: str = Field(..., description="Result classification")
    stage_description: str = Field(..., description="Description of the result")
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "Score ≥4 suggests possible delirium or cognitive impairment.",
                "stage": "Possible Delirium",
                "stage_description": "Possible delirium",
                "delirium_likely": True
            }
        }


# HElPS2B Models
class EegFindingType(str, Enum):
    """Enum for EEG findings"""
    PRESENT = "present"
    ABSENT = "absent"


class Helps2bRequest(BaseModel):
    """Request model for 2HELPS2B Score"""
    seizure_history: YesNoType = Field(..., description="History of seizures (remote or recent acute suspected)")
    epileptiform_discharges: EegFindingType = Field(..., description="Epileptiform discharges (spikes or sporadic sharp waves)")
    lateralized_periodic_discharges: EegFindingType = Field(..., description="Lateralized periodic discharges (LPDs)")
    bilateral_independent_periodic_discharges: EegFindingType = Field(..., description="Bilateral independent periodic discharges (BIPDs)")
    brief_potentially_ictal_rhythmic_discharges: EegFindingType = Field(..., description="Brief potentially ictal rhythmic discharges (BIRDs)")
    burst_suppression: EegFindingType = Field(..., description="Burst-suppression pattern on EEG")
    
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
    """Response model for 2HELPS2B Score"""
    result: int = Field(..., description="Total 2HELPS2B Score (0-6 points)")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Interpretation of seizure risk")
    stage: str = Field(..., description="Risk classification")
    stage_description: str = Field(..., description="Risk description")
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0, # Example value, actual calculation would be done in the calculator
                "unit": "points",
                "interpretation": "Low risk of seizures. Continue monitoring as clinically indicated.",
                "stage": "Low Risk",
                "stage_description": "Low risk of seizures"
            }
        }


# AIMS Models
class AimsRequest(BaseModel):
    """Request model for AIMS"""
    facial_muscles: int = Field(..., ge=0, le=4, description="Facial muscles and facial expression (0-4)")
    lips_perioral: int = Field(..., ge=0, le=4, description="Lips and perioral area (0-4)")
    jaw: int = Field(..., ge=0, le=4, description="Jaw (0-4)")
    tongue: int = Field(..., ge=0, le=4, description="Tongue (0-4)")
    upper_extremities: int = Field(..., ge=0, le=4, description="Upper extremities (0-4)")
    lower_extremities: int = Field(..., ge=0, le=4, description="Lower extremities (0-4)")
    trunk_movements: int = Field(..., ge=0, le=4, description="Trunk movements (0-4)")
    global_severity: int = Field(..., ge=0, le=4, description="Global severity of abnormal movements (0-4)")
    incapacitation: int = Field(..., ge=0, le=4, description="Incapacitation due to abnormal movements (0-4)")
    patient_awareness: int = Field(..., ge=0, le=4, description="Patient's awareness of movements (0-4)")
    current_problems_teeth: DiabetesType = Field(..., description="Current problems with teeth/dentures")
    dental_problems_interfere: DiabetesType = Field(..., description="Dental problems interfere with movements?")
    
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
    """Response model for AIMS"""
    result: int = Field(..., description="Total AIMS score (sum of items 1-7)")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Clinical interpretation of tardive dyskinesia")
    stage: str = Field(..., description="Dyskinesia classification")
    stage_description: str = Field(..., description="Description of dyskinesia degree")
    
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
