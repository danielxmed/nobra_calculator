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
    
    The CKD-EPI 2021 equation is the current gold standard for estimating glomerular 
    filtration rate (eGFR) in adults. This race-free equation was developed to provide 
    more accurate kidney function assessment across diverse populations.
    
    **Clinical Context:**
    - Used for CKD staging and monitoring
    - Guides nephrology referral decisions  
    - Assists in medication dosing adjustments
    - Essential for pre-operative risk assessment
    
    **Important Notes:**
    - Requires standardized (IDMS-traceable) serum creatinine
    - Valid only for adults ≥18 years
    - Less accurate in extremes of muscle mass
    - Should be interpreted with clinical context
    """
    sex: SexType = Field(
        ..., 
        description="**Patient's biological sex**\n\nUsed to determine sex-specific constants in the eGFR calculation:\n- **Female**: κ=0.7, α=-0.241, multiplier=1.012\n- **Male**: κ=0.9, α=-0.302, multiplier=1.0\n\n*Note: Based on biological sex, not gender identity*"
    )
    age: int = Field(
        ..., 
        ge=18, 
        le=120, 
        description="**Patient's age in years**\n\nAge is incorporated as an exponential factor (0.9938^age) in the equation.\n\n**Valid Range**: 18-120 years\n**Clinical Notes**:\n- Equation validated primarily in adults 18-70 years\n- Use with caution in very elderly patients (>90 years)\n- Consider functional assessment in addition to eGFR in elderly"
    )
    serum_creatinine: float = Field(
        ..., 
        ge=0.1, 
        le=20.0, 
        description="**Standardized serum creatinine concentration in mg/dL**\n\n**Critical Requirements**:\n- Must be IDMS-traceable (standardized)\n- Steady-state creatinine (not acute changes)\n- Fasting not required\n\n**Valid Range**: 0.1-20.0 mg/dL\n**Clinical Context**:\n- Normal ranges: ~0.6-1.2 mg/dL (varies by lab)\n- Values >2.0 mg/dL suggest significant kidney impairment\n- Very high values (>10 mg/dL) may indicate kidney failure\n\n**Important Notes**:\n- Affected by muscle mass, diet, and medications\n- May be falsely elevated by some drugs (trimethoprim, cimetidine)\n- Consider cystatin C-based equations if creatinine unreliable"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "sex": "female",
                "age": 65,
                "serum_creatinine": 1.2
            },
            "examples": {
                "normal_young_male": {
                    "summary": "Normal kidney function - Young male",
                    "description": "25-year-old male with normal creatinine",
                    "value": {
                        "sex": "male",
                        "age": 25,
                        "serum_creatinine": 0.9
                    }
                },
                "ckd_stage3_female": {
                    "summary": "CKD Stage 3a - Elderly female",
                    "description": "65-year-old female with mild-moderate kidney impairment",
                    "value": {
                        "sex": "female",
                        "age": 65,
                        "serum_creatinine": 1.2
                    }
                },
                "severe_ckd_male": {
                    "summary": "CKD Stage 4 - Middle-aged male",
                    "description": "55-year-old male with severe kidney impairment",
                    "value": {
                        "sex": "male",
                        "age": 55,
                        "serum_creatinine": 3.5
                    }
                },
                "kidney_failure": {
                    "summary": "CKD Stage 5 - Kidney failure",
                    "description": "45-year-old female with kidney failure",
                    "value": {
                        "sex": "female",
                        "age": 45,
                        "serum_creatinine": 6.8
                    }
                }
            }
        }


# Response Models
class CKDEpi2021Response(BaseModel):
    """
    Response model for CKD-EPI 2021 eGFR calculation
    
    Provides comprehensive kidney function assessment including eGFR value, 
    CKD staging, and clinical interpretation with actionable recommendations.
    
    **Clinical Significance:**
    - eGFR ≥90: Normal or high (investigate for kidney damage)
    - eGFR 60-89: Mild decrease (investigate for kidney damage)  
    - eGFR 45-59: Stage 3a CKD (nephrology follow-up recommended)
    - eGFR 30-44: Stage 3b CKD (nephrologist referral necessary)
    - eGFR 15-29: Stage 4 CKD (prepare for renal replacement therapy)
    - eGFR <15: Stage 5 CKD (kidney failure - RRT needed)
    """
    result: float = Field(
        ..., 
        description="**Estimated Glomerular Filtration Rate (eGFR)**\n\nCalculated using the CKD-EPI 2021 equation. Represents the volume of plasma filtered by the kidneys per minute, normalized to 1.73 m² body surface area.\n\n**Clinical Interpretation**:\n- **>90**: Normal or high kidney function\n- **60-89**: Mild decrease in kidney function\n- **45-59**: Mild to moderate decrease (Stage 3a CKD)\n- **30-44**: Moderate to severe decrease (Stage 3b CKD)\n- **15-29**: Severe decrease (Stage 4 CKD)\n- **<15**: Kidney failure (Stage 5 CKD)\n\n**Units**: mL/min/1.73 m²"
    )
    unit: str = Field(
        ..., 
        description="**Unit of measurement for eGFR**\n\nStandardized as mL/min/1.73 m² (milliliters per minute per 1.73 square meters of body surface area)\n\nThis normalization allows comparison across patients of different sizes."
    )
    interpretation: str = Field(
        ..., 
        description="**Clinical interpretation and recommendations**\n\nProvides stage-specific clinical guidance including:\n- **Risk assessment**: Current kidney function status\n- **Follow-up recommendations**: When to refer to nephrology\n- **Monitoring guidance**: Frequency of reassessment\n- **Treatment considerations**: When to prepare for renal replacement therapy\n\n*Always correlate with clinical context and other laboratory values*"
    )
    stage: str = Field(
        ..., 
        description="**CKD Stage Classification**\n\nBased on KDIGO 2012 CKD guidelines:\n- **G1**: Normal or high (≥90 mL/min/1.73 m²)\n- **G2**: Mild decrease (60-89 mL/min/1.73 m²)\n- **G3a**: Mild to moderate decrease (45-59 mL/min/1.73 m²)\n- **G3b**: Moderate to severe decrease (30-44 mL/min/1.73 m²)\n- **G4**: Severe decrease (15-29 mL/min/1.73 m²)\n- **G5**: Kidney failure (<15 mL/min/1.73 m²)\n\n*Note: CKD diagnosis requires evidence of kidney damage for stages G1-G2*"
    )
    stage_description: str = Field(
        ..., 
        description="**Detailed description of the CKD stage**\n\nProvides plain-language explanation of the kidney function level and its clinical significance."
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 52.3,
                "unit": "mL/min/1.73 m²",
                "interpretation": "Stage 3a Chronic Kidney Disease. Nephrology follow-up recommended.",
                "stage": "G3a",
                "stage_description": "Mild to moderate decrease in GFR"
            },
            "examples": {
                "normal_function": {
                    "summary": "Normal kidney function (G1)",
                    "description": "Young adult with normal eGFR",
                    "value": {
                        "result": 105.2,
                        "unit": "mL/min/1.73 m²",
                        "interpretation": "Normal or high GFR. Investigate presence of kidney damage to determine if CKD is present.",
                        "stage": "G1",
                        "stage_description": "Normal or high kidney function"
                    }
                },
                "mild_decrease": {
                    "summary": "Mild decrease in kidney function (G2)",
                    "description": "Mild reduction in eGFR, investigate for kidney damage",
                    "value": {
                        "result": 75.8,
                        "unit": "mL/min/1.73 m²",
                        "interpretation": "Mild decrease in GFR. Investigate presence of kidney damage to determine if CKD is present.",
                        "stage": "G2",
                        "stage_description": "Mild decrease in GFR"
                    }
                },
                "stage_3a_ckd": {
                    "summary": "Stage 3a CKD",
                    "description": "Mild to moderate CKD requiring nephrology follow-up",
                    "value": {
                        "result": 52.3,
                        "unit": "mL/min/1.73 m²",
                        "interpretation": "Stage 3a Chronic Kidney Disease. Nephrology follow-up recommended.",
                        "stage": "G3a",
                        "stage_description": "Mild to moderate decrease in GFR"
                    }
                },
                "stage_4_ckd": {
                    "summary": "Stage 4 CKD",
                    "description": "Severe CKD requiring preparation for renal replacement therapy",
                    "value": {
                        "result": 22.1,
                        "unit": "mL/min/1.73 m²",
                        "interpretation": "Stage 4 Chronic Kidney Disease. Specialized nephrology follow-up and preparation for kidney replacement therapy.",
                        "stage": "G4",
                        "stage_description": "Severe decrease in GFR"
                    }
                },
                "kidney_failure": {
                    "summary": "Kidney failure (G5)",
                    "description": "End-stage kidney disease requiring immediate RRT",
                    "value": {
                        "result": 8.5,
                        "unit": "mL/min/1.73 m²",
                        "interpretation": "Stage 5 Chronic Kidney Disease (kidney failure). Kidney replacement therapy (dialysis or transplant) is necessary.",
                        "stage": "G5",
                        "stage_description": "Kidney failure"
                    }
                }
            }
        }


class ScoreInfo(BaseModel):
    """Basic information of a score"""
    id: str = Field(..., description="Unique ID of the score")
    title: str = Field(..., description="Title of the score")
    description: str = Field(..., description="Description of the score")
    category: str = Field(..., description="Medical category of the score")
    version: Optional[str] = Field(None, description="Version of the score")


class ScoreListResponse(BaseModel):
    """Response for listing available scores"""
    scores: List[ScoreInfo] = Field(..., description="List of available scores")
    total: int = Field(..., description="Total number of available scores")
    
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
    """Model for score parameters"""
    name: str = Field(..., description="Parameter name")
    type: str = Field(..., description="Parameter type")
    required: bool = Field(..., description="Whether the parameter is required")
    description: str = Field(..., description="Parameter description")
    options: Optional[List[str]] = Field(None, description="Valid options for the parameter")
    validation: Optional[Dict[str, Any]] = Field(None, description="Validation rules")
    unit: Optional[str] = Field(None, description="Parameter unit")


class ResultInfo(BaseModel):
    """Information about a score's result"""
    name: str = Field(..., description="Result name")
    type: str = Field(..., description="Result type")
    unit: str = Field(..., description="Result unit")
    description: str = Field(..., description="Result description")


class InterpretationRange(BaseModel):
    """Interpretation range of a score"""
    min: float = Field(..., description="Minimum value of the range")
    max: Optional[float] = Field(None, description="Maximum value of the range")
    stage: str = Field(..., description="Stage or classification")
    description: str = Field(..., description="Description of the stage")
    interpretation: str = Field(..., description="Clinical interpretation")


class Interpretation(BaseModel):
    """Model for score interpretations"""
    ranges: List[InterpretationRange] = Field(..., description="Interpretation ranges")


class ScoreMetadataResponse(BaseModel):
    """Detailed response for a score's metadata"""
    id: str = Field(..., description="Unique ID of the score")
    title: str = Field(..., description="Title of the score")
    description: str = Field(..., description="Detailed description of the score")
    category: str = Field(..., description="Medical category of the score")
    version: Optional[str] = Field(None, description="Version of the score")
    parameters: List[Parameter] = Field(..., description="Parameters required for calculation")
    result: ResultInfo = Field(..., description="Information about the result")
    interpretation: Interpretation = Field(..., description="Interpretations of the result")
    references: List[str] = Field(..., description="Bibliographic references")
    formula: str = Field(..., description="Mathematical formula of the calculation")
    notes: List[str] = Field(..., description="Important notes about the score")


class ErrorResponse(BaseModel):
    """
    Standardized error response model for all API endpoints
    
    Provides consistent error information across all endpoints to facilitate
    proper error handling and debugging in client applications.
    
    **Error Types:**
    - **ValidationError**: Invalid input parameters (422)
    - **ScoreNotFound**: Calculator ID not found (404)
    - **CalculatorNotImplemented**: Calculator exists but not implemented (501)
    - **CalculationError**: Calculation execution failure (500)
    - **InternalServerError**: General server errors (500)
    - **ReloadError**: System reload failures (500)
    """
    error: str = Field(
        ..., 
        description="**Error type classification**\n\nStandardized error categories for programmatic handling:\n- `ValidationError`: Invalid parameters\n- `ScoreNotFound`: Calculator not found\n- `CalculatorNotImplemented`: Not yet implemented\n- `CalculationError`: Calculation failure\n- `InternalServerError`: Server error\n- `ReloadError`: System reload failure"
    )
    message: str = Field(
        ..., 
        description="**Human-readable error message**\n\nClear, descriptive message explaining what went wrong and providing context for the error."
    )
    details: Optional[Dict[str, Any]] = Field(
        None, 
        description="**Additional error details and suggestions**\n\nStructured information including:\n- Specific validation failures\n- Parameter requirements\n- Suggested corrective actions\n- Available alternatives\n- Contact information for support"
    )
    
    class Config:
        schema_extra = {
            "examples": {
                "validation_error": {
                    "summary": "Parameter validation failure",
                    "description": "Invalid input parameters provided",
                    "value": {
                        "error": "ValidationError",
                        "message": "Invalid parameters for ckd_epi_2021",
                        "details": {
                            "score_id": "ckd_epi_2021",
                            "validation_error": "Age must be an integer between 18 and 120 years",
                            "suggestion": "Use GET /api/scores/ckd_epi_2021 to see parameter requirements",
                            "provided_parameters": ["sex", "age", "serum_creatinine"]
                        }
                    }
                },
                "calculator_not_found": {
                    "summary": "Calculator not found",
                    "description": "Requested calculator ID does not exist",
                    "value": {
                        "error": "ScoreNotFound",
                        "message": "Calculator 'unknown_score' not found",
                        "details": {
                            "score_id": "unknown_score",
                            "available_calculators": "Use GET /api/scores to see available calculators",
                            "suggestion": "Check spelling or use GET /api/scores to browse available options"
                        }
                    }
                },
                "not_implemented": {
                    "summary": "Calculator not implemented",
                    "description": "Calculator exists but implementation is pending",
                    "value": {
                        "error": "CalculatorNotImplemented",
                        "message": "Calculator for 'future_score' exists but is not yet implemented",
                        "details": {
                            "score_id": "future_score",
                            "status": "Calculator metadata available but calculation logic not implemented",
                            "suggestion": "Check back later or contact support for implementation timeline"
                        }
                    }
                },
                "calculation_error": {
                    "summary": "Calculation execution failure",
                    "description": "Error occurred during calculation process",
                    "value": {
                        "error": "CalculationError",
                        "message": "Error calculating ckd_epi_2021",
                        "details": {
                            "score_id": "ckd_epi_2021",
                            "parameters": {"sex": "female", "age": 65, "serum_creatinine": 1.2},
                            "suggestion": "Verify parameters match calculator requirements or contact support"
                        }
                    }
                },
                "internal_server_error": {
                    "summary": "Internal server error",
                    "description": "Unexpected server-side error occurred",
                    "value": {
                        "error": "InternalServerError",
                        "message": "Internal error in calculation",
                        "details": {
                            "score_id": "ckd_epi_2021",
                            "error": "Database connection failed",
                            "suggestion": "Contact support if this error persists"
                        }
                    }
                }
            }
        }


class HealthResponse(BaseModel):
    """Response for health check endpoint"""
    status: str = Field(..., description="API status")
    message: str = Field(..., description="Status message")
    version: str = Field(..., description="API version")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "message": "nobra_calculator API is running correctly",
                "version": "1.0.0"
            }
        }


class ReloadResponse(BaseModel):
    """Response model for system reload operations"""
    status: str = Field(..., description="Reload operation status (success/error)")
    message: str = Field(..., description="Descriptive message about the reload operation")
    scores_loaded: int = Field(..., description="Number of calculator metadata files loaded")
    timestamp: str = Field(..., description="ISO timestamp of the reload operation")
    details: Dict[str, Any] = Field(..., description="Additional reload operation details")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "message": "Calculators reloaded successfully",
                "scores_loaded": 19,
                "timestamp": "2024-01-01T12:00:00Z",
                "details": {
                    "metadata_reloaded": True,
                    "calculators_reloaded": True,
                    "available_categories": ["cardiology", "nephrology", "neurology"]
                }
            }
        }


class CategoriesResponse(BaseModel):
    """Response model for medical categories listing"""
    categories: List[str] = Field(..., description="List of available medical specialty categories")
    total: int = Field(..., description="Total number of medical categories")
    specialty_count: Dict[str, int] = Field(..., description="Number of calculators per specialty")
    description: str = Field(..., description="Description of the categories system")
    usage: str = Field(..., description="Usage instructions for filtering by category")
    
    class Config:
        schema_extra = {
            "example": {
                "categories": ["cardiology", "nephrology", "neurology", "pulmonology"],
                "total": 11,
                "specialty_count": {
                    "cardiology": 3,
                    "nephrology": 1,
                    "neurology": 4,
                    "pulmonology": 2
                },
                "description": "Medical specialties covered by nobra_calculator API",
                "usage": "Use category names with GET /api/scores?category={category} to filter calculators"
            }
        }


class Cha2ds2VascRequest(BaseModel):
    """Request model for CHA₂DS₂-VASc Score"""
    age: int = Field(..., ge=18, le=120, description="Patient's age in years")
    sex: SexType = Field(..., description="Patient's biological sex")
    congestive_heart_failure: bool = Field(..., description="History of congestive heart failure or LV dysfunction (LVEF ≤40%)")
    hypertension: bool = Field(..., description="History of arterial hypertension")
    stroke_tia_thromboembolism: bool = Field(..., description="Previous history of stroke, TIA, or thromboembolism")
    vascular_disease: bool = Field(..., description="Vascular disease (previous MI, PAD, or aortic plaque)")
    diabetes: bool = Field(..., description="History of diabetes mellitus")
    
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
    """Response model for CHA₂DS₂-VASc Score"""
    result: int = Field(..., description="Total CHA₂DS₂-VASc score (0-9 points)")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Clinical interpretation and anticoagulation recommendation")
    stage: str = Field(..., description="Risk classification")
    stage_description: str = Field(..., description="Description of the risk level")
    annual_stroke_risk: str = Field(..., description="Annual stroke risk in percentage")
    components: Dict[str, int] = Field(..., description="Score of each component")
    
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
    """Request model for CURB-65 Score"""
    confusion: bool = Field(..., description="Recent onset mental confusion (disorientation in time, place, or person)")
    urea: float = Field(..., ge=0, le=200, description="Serum urea in mg/dL")
    respiratory_rate: int = Field(..., ge=0, le=60, description="Respiratory rate (breaths/min)")
    systolic_bp: int = Field(..., ge=0, le=300, description="Systolic blood pressure (mmHg)")
    diastolic_bp: int = Field(..., ge=0, le=200, description="Diastolic blood pressure (mmHg)")
    age: int = Field(..., ge=0, le=120, description="Patient's age in years")
    
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
    """Response model for CURB-65 Score"""
    result: int = Field(..., description="Total CURB-65 score (0-5 points)")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Clinical interpretation and treatment recommendation")
    stage: str = Field(..., description="Risk classification")
    stage_description: str = Field(..., description="Description of the risk level")
    mortality_risk: str = Field(..., description="Mortality risk in percentage")
    components: Dict[str, int] = Field(..., description="Score of each component")
    
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
    """Enum for blood pressure in ABCD²"""
    NORMAL = "normal"
    ELEVATED = "elevated"


class ClinicalFeaturesType(str, Enum):
    """Enum for clinical features in ABCD²"""
    UNILATERAL_WEAKNESS = "unilateral_weakness"
    SPEECH_DISTURBANCE = "speech_disturbance"
    OTHER = "other"


class DurationType(str, Enum):
    """Enum for symptom duration in ABCD²"""
    LESS_10MIN = "less_10min"
    BETWEEN_10_59MIN = "10_59min"
    MORE_60MIN = "60min_or_more"


class DiabetesType(str, Enum):
    """Enum for diabetes"""
    YES = "yes"
    NO = "no"


class Abcd2Request(BaseModel):
    """Request model for ABCD² Score"""
    age: int = Field(..., ge=18, le=120, description="Patient's age in years")
    blood_pressure: BloodPressureType = Field(..., description="Blood pressure at evaluation (≥140/90 = elevated)")
    clinical_features: ClinicalFeaturesType = Field(..., description="Clinical features of the TIA episode")
    duration: DurationType = Field(..., description="Duration of TIA symptoms")
    diabetes: DiabetesType = Field(..., description="History of diabetes mellitus")
    
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
    """Response model for ABCD² Score"""
    result: int = Field(..., description="Total ABCD² score (0-7 points)")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Clinical interpretation and risk stratification")
    stage: str = Field(..., description="Stroke risk classification")
    stage_description: str = Field(..., description="Description of the risk level")
    stroke_risk_2days: str = Field(..., description="Stroke risk in 2 days")
    stroke_risk_7days: str = Field(..., description="Stroke risk in 7 days")
    stroke_risk_90days: str = Field(..., description="Stroke risk in 90 days")
    
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
    """Enum for thrombocytopenia severity"""
    FALL_GREATER_50_NADIR_GREATER_20 = "fall_greater_50_nadir_greater_20"
    FALL_30_50_OR_NADIR_10_19 = "fall_30_50_or_nadir_10_19"
    FALL_LESS_30_OR_NADIR_LESS_10 = "fall_less_30_or_nadir_less_10"


class TimingOnsetType(str, Enum):
    """Enum for timing of thrombocytopenia onset"""
    ONSET_5_10_DAYS_OR_FALL_1_DAY_HEPARIN_30_DAYS = "onset_5_10_days_or_fall_1_day_heparin_30_days"
    POSSIBLE_5_10_DAYS_OR_ONSET_AFTER_10_DAYS_OR_HEPARIN_30_100_DAYS = "possible_5_10_days_or_onset_after_10_days_or_heparin_30_100_days"
    FALL_LESS_4_DAYS_NO_RECENT_EXPOSURE = "fall_less_4_days_no_recent_exposure"


class ThrombosisSequelaeType(str, Enum):
    """Enum for thrombosis/sequelae"""
    NEW_THROMBOSIS_OR_SKIN_NECROSIS_OR_SYSTEMIC_REACTION = "new_thrombosis_or_skin_necrosis_or_systemic_reaction"
    PROGRESSIVE_THROMBOSIS_OR_SKIN_LESIONS_OR_SUSPECTED_THROMBOSIS = "progressive_thrombosis_or_skin_lesions_or_suspected_thrombosis"
    NO_THROMBOSIS_OR_SEQUELAE = "no_thrombosis_or_sequelae"


class OtherCausesType(str, Enum):
    """Enum for other causes of thrombocytopenia"""
    NO_OTHER_APPARENT_CAUSE = "no_other_apparent_cause"
    OTHER_POSSIBLE_CAUSES = "other_possible_causes"
    OTHER_DEFINITIVE_CAUSES = "other_definitive_causes"


class FourTsRequest(BaseModel):
    """Request model for 4Ts Score"""
    thrombocytopenia_severity: ThrombocytopeniaSeverityType = Field(..., description="Severity of thrombocytopenia (magnitude of platelet fall)")
    timing_onset: TimingOnsetType = Field(..., description="Timing of platelet fall onset")
    thrombosis_sequelae: ThrombosisSequelaeType = Field(..., description="Presence of thrombosis or other sequelae")
    other_causes: OtherCausesType = Field(..., description="Other possible causes of thrombocytopenia")
    
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
    """Response model for 4Ts Score"""
    result: int = Field(..., description="Total 4Ts score (0-8 points)")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Clinical interpretation and management recommendation")
    stage: str = Field(..., description="HIT probability classification")
    stage_description: str = Field(..., description="Probability description")
    hit_probability: str = Field(..., description="HIT probability in percentage")
    
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
    """Enum for urea unit"""
    MMOL_L = "mmol_L"
    MG_DL = "mg_dL"


class FourCMortalityRequest(BaseModel):
    """Request model for 4C Mortality Score"""
    age: int = Field(..., ge=0, le=120, description="Patient's age in years")
    sex: SexType = Field(..., description="Patient's sex")
    comorbidities: int = Field(..., ge=0, le=20, description="Number of comorbidities")
    respiratory_rate: int = Field(..., ge=5, le=60, description="Respiratory rate (breaths/min)")
    oxygen_saturation: float = Field(..., ge=50.0, le=100.0, description="Peripheral oxygen saturation (%)")
    glasgow_coma_scale: int = Field(..., ge=3, le=15, description="Glasgow Coma Scale")
    urea_unit: UreaUnitType = Field(..., description="Urea measurement unit")
    urea_value: float = Field(..., ge=0.1, le=300.0, description="Serum urea value")
    crp: float = Field(..., ge=0.0, le=1000.0, description="C-reactive protein (mg/L)")
    
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
    """Response model for 4C Mortality Score"""
    result: int = Field(..., description="Total 4C score (0-21 points)")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Clinical interpretation and prognosis")
    stage: str = Field(..., description="Mortality risk classification")
    stage_description: str = Field(..., description="Description of the risk level")
    mortality_risk: str = Field(..., description="In-hospital mortality risk")
    
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
    """Request model for 6 Minute Walk Distance"""
    age: int = Field(..., ge=18, le=100, description="Patient's age in years")
    sex: SexType = Field(..., description="Patient's sex")
    height: float = Field(..., ge=120.0, le=220.0, description="Patient's height (cm)")
    weight: float = Field(..., ge=30.0, le=200.0, description="Patient's weight (kg)")
    observed_distance: Optional[float] = Field(None, ge=0.0, le=1000.0, description="Observed distance (optional, for comparison)")
    
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
    """Response model for 6 Minute Walk Distance"""
    result: float = Field(..., description="Predicted 6-minute walk distance (meters)")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Interpretation of functional capacity")
    stage: str = Field(..., description="Functional capacity classification")
    stage_description: str = Field(..., description="Description of functional level")
    lower_limit_normal: float = Field(..., description="Lower limit of normality (meters)")
    percentage_predicted: Optional[float] = Field(None, description="Percentage of predicted (if observed distance provided)")
    
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
    """Request model for A-a O2 Gradient"""
    age: int = Field(..., ge=1, le=120, description="Patient's age in years")
    fio2: float = Field(..., ge=0.21, le=1.0, description="Inspired oxygen fraction (0.21 for room air)")
    paco2: float = Field(..., ge=10.0, le=100.0, description="Arterial CO₂ partial pressure (mmHg)")
    pao2: float = Field(..., ge=30.0, le=600.0, description="Arterial O₂ partial pressure (mmHg)")
    patm: Optional[float] = Field(760.0, ge=500.0, le=800.0, description="Atmospheric pressure (mmHg)")
    respiratory_quotient: Optional[float] = Field(0.8, ge=0.7, le=1.0, description="Respiratory quotient")
    
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
    """Response model for A-a O2 Gradient"""
    result: float = Field(..., description="Alveolar-arterial oxygen gradient (mmHg)")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Interpretation of lung function")
    stage: str = Field(..., description="Gradient classification")
    stage_description: str = Field(..., description="Gradient description")
    pao2_alveolar: float = Field(..., description="Calculated alveolar O₂ pressure (mmHg)")
    age_adjusted_normal: float = Field(..., description="Age-adjusted upper normal limit (mmHg)")
    
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
    """Enum for yes/no answers"""
    YES = "yes"
    NO = "no"


class YesNoNAType(str, Enum):
    """Enum for yes/no/not applicable answers"""
    YES = "yes"
    NO = "no"
    NOT_APPLICABLE = "not_applicable"


class AasRequest(BaseModel):
    """Request model for AAS (Abuse Assessment Screen)"""
    emotional_physical_abuse: YesNoType = Field(..., description="Have you ever been emotionally or physically abused by your partner?")
    physical_hurt_recently: YesNoType = Field(..., description="Since your last visit, have you been physically hurt?")
    physical_hurt_pregnancy: YesNoNAType = Field(..., description="Since you became pregnant, have you been physically hurt?")
    sexual_abuse: YesNoType = Field(..., description="In the last year, has anyone forced you to do something sexual you didn't want to do?")
    afraid_of_partner: YesNoType = Field(..., description="Are you afraid of your partner?")
    
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
    """Response model for AAS"""
    result: str = Field(..., description="AAS screening result (Positive/Negative)")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Screening interpretation")
    stage: str = Field(..., description="Screening result")
    stage_description: str = Field(..., description="Description of the result")
    positive_responses_count: int = Field(..., description="Number of positive responses")
    is_positive: bool = Field(..., description="Whether the screening is positive")
    
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
    """Request model for AAP Pediatric Hypertension"""
    age: int = Field(..., ge=1, le=17, description="Patient's age in years")
    sex: SexType = Field(..., description="Patient's sex")
    height: float = Field(..., ge=70.0, le=200.0, description="Patient's height (cm)")
    systolic_bp: int = Field(..., ge=60, le=200, description="Systolic blood pressure (mmHg)")
    diastolic_bp: int = Field(..., ge=30, le=150, description="Diastolic blood pressure (mmHg)")
    
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
    """Response model for AAP Pediatric Hypertension"""
    result: str = Field(..., description="Pediatric blood pressure classification")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Clinical interpretation and recommendations")
    stage: str = Field(..., description="Blood pressure stage")
    stage_description: str = Field(..., description="Description of the stage")
    systolic_percentile: float = Field(..., description="Systolic BP percentile")
    diastolic_percentile: float = Field(..., description="Diastolic BP percentile")
    
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
    """Request model for Abbey Pain Scale"""
    vocalization: int = Field(..., ge=0, le=3, description="Vocalization (0-3)")
    facial_expression: int = Field(..., ge=0, le=3, description="Facial expression (0-3)")
    body_language: int = Field(..., ge=0, le=3, description="Body language (0-3)")
    behavioral_change: int = Field(..., ge=0, le=3, description="Behavioral change (0-3)")
    physiological_change: int = Field(..., ge=0, le=3, description="Physiological change (0-3)")
    physical_change: int = Field(..., ge=0, le=3, description="Physical change (0-3)")
    
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
    """Response model for Abbey Pain Scale"""
    result: int = Field(..., description="Total Abbey Pain Scale score (0-18)")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Interpretation of pain intensity")
    stage: str = Field(..., description="Pain classification")
    stage_description: str = Field(..., description="Description of pain level")
    pain_present: bool = Field(..., description="Whether pain is present")
    
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
    """Request model for ABIC Score"""
    age: int = Field(..., ge=18, le=100, description="Patient's age in years")
    serum_bilirubin: float = Field(..., ge=0.1, le=50.0, description="Total serum bilirubin (mg/dL)")
    serum_creatinine: float = Field(..., ge=0.1, le=20.0, description="Serum creatinine (mg/dL)")
    inr: float = Field(..., ge=0.5, le=10.0, description="International Normalized Ratio (INR)")
    
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
