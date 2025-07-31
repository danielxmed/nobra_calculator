"""
CHA₂DS₂-VASc Score calculation models
"""

from pydantic import BaseModel, Field
from typing import Dict
from app.models.shared import SexType


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
        json_schema_extra = {
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
        json_schema_extra = {
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