"""
2018 Leibovich Model for Renal Cell Carcinoma (RCC) calculation models
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Literal


class Leibovich2018RccRequest(BaseModel):
    """
    Request model for 2018 Leibovich Model for Renal Cell Carcinoma calculation
    
    The 2018 Leibovich prognostic model predicts progression-free survival and cancer-specific 
    survival in patients with renal cell carcinoma using clinical, surgical, and pathologic factors.
    
    **Clinical Use**:
    - Risk stratification for RCC patients after nephrectomy
    - Prediction of progression-free survival (PFS) and cancer-specific survival (CSS)
    - Guidance for surveillance intensity and adjuvant therapy decisions
    - Patient counseling regarding prognosis
    
    **Model Components**:
    - Clinical factors: Age, ECOG status, constitutional symptoms
    - Surgical factors: Adrenalectomy, surgical margins
    - Pathologic factors: Tumor grade, necrosis, sarcomatoid features, size, invasion, thrombus
    
    **Reference**: Thompson RH, et al. Negative impact of sarcomatoid differentiation 
    on the outcome of clear cell renal cell carcinoma. Am J Surg Pathol. 2018;42(4):474-481.
    """
    age: int = Field(
        ..., 
        ge=18, 
        le=100, 
        description="Patient's age at surgery in years. Age ≥60 years adds 1 point to cancer-specific survival score.",
        example=65
    )
    ecog_status: Literal["0", "≥1"] = Field(
        ..., 
        description="ECOG Performance Status. 0 = fully active, ≥1 = restricted activity. ECOG ≥1 adds 2 points to CSS score.",
        example="0"
    )
    constitutional_symptoms: bool = Field(
        ..., 
        description="Presence of constitutional symptoms (fever, night sweats, weight loss). Adds 1 point to both PFS and CSS scores.",
        example=False
    )
    adrenalectomy: bool = Field(
        ..., 
        description="Whether adrenalectomy was performed during surgery. Adds 1 point to CSS score if performed.",
        example=False
    )
    surgical_margins: Literal["negative", "positive"] = Field(
        ..., 
        description="Surgical margin status. Positive margins add 1 point to CSS score.",
        example="negative"
    )
    tumor_grade: Literal["1", "2", "3", "4"] = Field(
        ..., 
        description="Tumor grade (Fuhrman/WHO-ISUP grading). Grade 1=0pts, 2=2pts, 3=3pts, 4=4pts for both PFS and CSS.",
        example="2"
    )
    coagulative_necrosis: bool = Field(
        ..., 
        description="Presence of coagulative tumor necrosis on histology. Adds 2 points to both PFS and CSS scores.",
        example=False
    )
    sarcomatoid_differentiation: bool = Field(
        ..., 
        description="Presence of sarcomatoid differentiation on histology. Adds 1 point to CSS score.",
        example=False
    )
    tumor_size: float = Field(
        ..., 
        ge=0.5, 
        le=25.0, 
        description="Maximum tumor diameter in centimeters. Size categories: ≤4cm=0pts, >4-7cm=3pts, >7-10cm=4pts, >10cm=5pts (PFS).",
        example=6.5
    )
    perinephric_invasion: bool = Field(
        ..., 
        description="Invasion of perinephric fat or renal sinus fat. Adds 1 point to PFS, 2 points to CSS.",
        example=False
    )
    tumor_thrombus: Literal["none", "level_0", "level_1_4"] = Field(
        ..., 
        description="Presence and level of tumor thrombus. Level 0 adds 1 point, Level 1-4 adds 2 points to both scores.",
        example="none"
    )
    extension_beyond_kidney: bool = Field(
        ..., 
        description="Extension beyond kidney capsule. Adds 2 points to PFS score.",
        example=False
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 65,
                "ecog_status": "0",
                "constitutional_symptoms": False,
                "adrenalectomy": False,
                "surgical_margins": "negative",
                "tumor_grade": "2",
                "coagulative_necrosis": False,
                "sarcomatoid_differentiation": False,
                "tumor_size": 6.5,
                "perinephric_invasion": False,
                "tumor_thrombus": "none",
                "extension_beyond_kidney": False
            }
        }


class Leibovich2018RccResponse(BaseModel):
    """
    Response model for 2018 Leibovich Model for Renal Cell Carcinoma calculation
    
    Provides comprehensive prognostic assessment with separate scores for progression-free
    survival and cancer-specific survival, along with risk stratification and management
    recommendations based on current oncological guidelines.
    
    **Risk Stratification**:
    - Low Risk (0-4 points): Excellent prognosis, standard surveillance
    - Intermediate Risk (5-9 points): Good prognosis, enhanced surveillance
    - High Risk (10-14 points): Poor prognosis, intensive surveillance + adjuvant therapy
    - Very High Risk (≥15 points): Very poor prognosis, aggressive management
    
    **Clinical Applications**:
    - Surveillance intensity planning
    - Adjuvant therapy decision-making
    - Clinical trial enrollment consideration
    - Patient and family counseling
    """
    result: Dict[str, Any] = Field(
        ..., 
        description="Comprehensive result containing PFS score, CSS score, and overall risk category",
        example={
            "pfs_score": 5,
            "css_score": 6,
            "overall_risk_category": "Intermediate Risk"
        }
    )
    unit: str = Field(
        ..., 
        description="Unit of the score results",
        example="points"
    )
    interpretation: str = Field(
        ..., 
        description="Combined clinical interpretation for both progression-free and cancer-specific survival",
        example="PFS: Intermediate risk of progression. Enhanced surveillance may be considered. CSS: Intermediate risk of cancer-specific death. Enhanced surveillance may be considered."
    )
    stage: str = Field(
        ..., 
        description="Overall risk classification category based on higher of PFS or CSS scores",
        example="Intermediate Risk"
    )
    stage_description: str = Field(
        ..., 
        description="Description showing both PFS and CSS scores",
        example="PFS Score: 5, CSS Score: 6"
    )
    details: Dict[str, Any] = Field(
        ..., 
        description="Detailed breakdown of progression-free survival and cancer-specific survival assessments",
        example={
            "progression_free_survival": {
                "score": 5,
                "stage": "Intermediate Risk",
                "interpretation": "Intermediate risk of progression. Enhanced surveillance may be considered."
            },
            "cancer_specific_survival": {
                "score": 6,
                "stage": "Intermediate Risk", 
                "interpretation": "Intermediate risk of cancer-specific death. Enhanced surveillance may be considered."
            }
        }
    )
    components: Dict[str, Any] = Field(
        ..., 
        description="Breakdown of points contributed by each component for transparency and clinical understanding",
        example={
            "age_≥60": 1,
            "ecog_≥1": 0,
            "constitutional_symptoms": 0,
            "adrenalectomy": 0,
            "positive_margins": 0,
            "tumor_grade": "2",
            "coagulative_necrosis": 0,
            "sarcomatoid_differentiation": 0,
            "tumor_size_cm": 6.5,
            "perinephric_invasion": 0,
            "tumor_thrombus": "none",
            "extension_beyond_kidney": 0
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": {
                    "pfs_score": 5,
                    "css_score": 6,
                    "overall_risk_category": "Intermediate Risk"
                },
                "unit": "points",
                "interpretation": "PFS: Intermediate risk of progression. Enhanced surveillance may be considered. CSS: Intermediate risk of cancer-specific death. Enhanced surveillance may be considered.",
                "stage": "Intermediate Risk",
                "stage_description": "PFS Score: 5, CSS Score: 6",
                "details": {
                    "progression_free_survival": {
                        "score": 5,
                        "stage": "Intermediate Risk",
                        "interpretation": "Intermediate risk of progression. Enhanced surveillance may be considered."
                    },
                    "cancer_specific_survival": {
                        "score": 6,
                        "stage": "Intermediate Risk",
                        "interpretation": "Intermediate risk of cancer-specific death. Enhanced surveillance may be considered."
                    }
                },
                "components": {
                    "age_≥60": 1,
                    "ecog_≥1": 0,
                    "constitutional_symptoms": 0,
                    "adrenalectomy": 0,
                    "positive_margins": 0,
                    "tumor_grade": "2",
                    "coagulative_necrosis": 0,
                    "sarcomatoid_differentiation": 0,
                    "tumor_size_cm": 6.5,
                    "perinephric_invasion": 0,
                    "tumor_thrombus": "none",
                    "extension_beyond_kidney": 0
                }
            }
        }