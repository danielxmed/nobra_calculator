"""
Creatinine Clearance (Cockcroft-Gault Equation) Models

Request and response models for Cockcroft-Gault creatinine clearance calculation.

References (Vancouver style):
1. Cockcroft DW, Gault MH. Prediction of creatinine clearance from serum creatinine. 
   Nephron. 1976;16(1):31-41. doi:10.1159/000180580
2. Stevens LA, Coresh J, Greene T, Levey AS. Assessing kidney function--measured 
   and estimated glomerular filtration rate. N Engl J Med. 2006;354(23):2473-2483.
3. Levey AS, Inker LA, Coresh J. GFR estimation: from physiology to public health. 
   Am J Kidney Dis. 2014;63(5):820-834.

The Cockcroft-Gault equation, developed in 1973, estimates creatinine clearance 
from serum creatinine, age, weight, and sex. While historically important for 
kidney function assessment and drug dosing, it has been largely superseded by 
more accurate equations like CKD-EPI for GFR estimation.

The equation is: CrCl = [(140 - age) × weight × (0.85 if female)] / (72 × serum creatinine)

Despite its limitations, the Cockcroft-Gault equation is still used in specific 
clinical scenarios, particularly for medication dosing decisions where regulatory 
guidance specifically recommends its use (e.g., direct-acting oral anticoagulants).
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class CreatinineClearanceCockcroftGaultRequest(BaseModel):
    """
    Request model for Creatinine Clearance (Cockcroft-Gault Equation)
    
    The Cockcroft-Gault equation estimates creatinine clearance using 4 main parameters:
    
    Required Parameters:
    - age: Patient age in years (18-120)
    - weight: Patient weight in kilograms (30-300 kg)
    - sex: Patient biological sex (male/female)
    - serum_creatinine: Serum creatinine level in mg/dL (0.3-15.0)
    
    Optional Parameter:
    - height: Patient height in centimeters (for BMI calculation and weight recommendations)
    
    Formula: CrCl = [(140 - age) × weight × (0.85 if female)] / (72 × serum creatinine)
    
    Clinical Interpretation:
    - ≥90 mL/min: Normal kidney function
    - 60-89 mL/min: Mildly decreased kidney function
    - 30-59 mL/min: Moderately decreased kidney function  
    - 15-29 mL/min: Severely decreased kidney function
    - <15 mL/min: Kidney failure
    
    Clinical Applications:
    - Medication dosing for renally eliminated drugs
    - Initial assessment of kidney function
    - Drug development and pharmacokinetic studies
    - Regulatory guidance for specific medications (e.g., DOACs)
    
    Important Considerations:
    - Tends to overestimate GFR by 10-20% compared to measured values
    - Less accurate at extremes of weight and in elderly patients
    - Assumes normal muscle mass and may be inaccurate with altered muscle mass
    - Not adjusted for body surface area unlike newer equations
    
    References (Vancouver style):
    1. Cockcroft DW, Gault MH. Prediction of creatinine clearance from serum creatinine. 
    Nephron. 1976;16(1):31-41. doi:10.1159/000180580
    2. Stevens LA, Coresh J, Greene T, Levey AS. Assessing kidney function--measured 
    and estimated glomerular filtration rate. N Engl J Med. 2006;354(23):2473-2483.
    3. Levey AS, Inker LA, Coresh J. GFR estimation: from physiology to public health. 
    Am J Kidney Dis. 2014;63(5):820-834.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in years. Used in the calculation as (140 - age). Normal aging is associated with gradual decline in kidney function",
        example=65
    )
    
    weight: float = Field(
        ...,
        ge=30.0,
        le=300.0,
        description="Patient weight in kilograms. Directly proportional to creatinine clearance in the equation. Consider using ideal or adjusted body weight for obese patients",
        example=70.0
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient biological sex. Females receive a 0.85 correction factor due to typically lower muscle mass. This accounts for differences in creatinine production",
        example="female"
    )
    
    serum_creatinine: float = Field(
        ...,
        ge=0.3,
        le=15.0,
        description="Serum creatinine level in mg/dL. Inversely related to creatinine clearance. Normal range is typically 0.6-1.2 mg/dL for adults",
        example=1.1
    )
    
    height: Optional[float] = Field(
        None,
        ge=100.0,
        le=250.0,
        description="Patient height in centimeters (optional). Used to calculate BMI and provide weight-specific recommendations for equation accuracy",
        example=165.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "weight": 70.0,
                "sex": "female",
                "serum_creatinine": 1.1,
                "height": 165.0
            }
        }


class CreatinineClearanceCockcroftGaultResponse(BaseModel):
    """
    Response model for Creatinine Clearance (Cockcroft-Gault Equation)
    
    The Cockcroft-Gault equation provides an estimate of creatinine clearance 
    that can be used for kidney function assessment and medication dosing decisions.
    
    Interpretation Guidelines:
    - ≥90 mL/min: Normal kidney function - Standard medication dosing
    - 60-89 mL/min: Mildly decreased - Monitor closely, consider dose adjustments
    - 30-59 mL/min: Moderately decreased - Dose adjustments required for many medications
    - 15-29 mL/min: Severely decreased - Significant dose reductions or alternatives needed
    - <15 mL/min: Kidney failure - Avoid nephrotoxic drugs, consider dialysis dosing
    
    Clinical Context:
    While newer equations like CKD-EPI are preferred for general GFR estimation,
    the Cockcroft-Gault equation remains relevant for specific clinical scenarios,
    particularly when regulatory guidance recommends its use for drug dosing.
    
    Reference: Cockcroft DW, Gault MH. Nephron. 1976;16(1):31-41.
    """
    
    result: float = Field(
        ...,
        description="Estimated creatinine clearance in mL/min calculated using the Cockcroft-Gault equation",
        example=52.3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for creatinine clearance",
        example="mL/min"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with kidney function assessment and medication guidance",
        example="Creatinine clearance of 52.3 mL/min indicates moderately decreased kidney function. Dose adjustments are required for many medications. Consider nephrology consultation."
    )
    
    stage: str = Field(
        ...,
        description="Kidney function stage classification (Normal, Mildly Decreased, Moderately Decreased, Severely Decreased, Kidney Failure)",
        example="Moderately Decreased"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the kidney function stage",
        example="Moderately decreased kidney function"
    )
    
    calculation_details: dict = Field(
        ...,
        description="Detailed breakdown including input parameters, clinical assessments, and recommendations",
        example={
            "input_parameters": {
                "age": 65,
                "weight": 70.0,
                "sex": "female",
                "serum_creatinine": 1.1,
                "height": 165.0,
                "bmi": 25.7
            },
            "clinical_assessment": "Moderate kidney function impairment",
            "medication_guidance": "Dose adjustments required for many medications",
            "monitoring_recommendations": "Close monitoring and nephrology consultation recommended",
            "weight_recommendations": {
                "bmi_category": "Overweight/Obese",
                "weight_recommendation": "Consider using adjusted body weight or ideal body weight",
                "accuracy_note": "Equation may overestimate clearance in obese patients",
                "clinical_note": "Consider clinical context when interpreting results at weight extremes"
            },
            "formula_notes": [
                "CrCl = [(140 - age) × weight × (0.85 if female)] / (72 × serum creatinine)",
                "Historical equation, may overestimate GFR by 10-20%",
                "Still used for specific medication dosing decisions"
            ]
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 52.3,
                "unit": "mL/min",
                "interpretation": "Creatinine clearance of 52.3 mL/min indicates moderately decreased kidney function. Dose adjustments are required for many medications. Consider nephrology consultation.",
                "stage": "Moderately Decreased",
                "stage_description": "Moderately decreased kidney function",
                "calculation_details": {
                    "input_parameters": {
                        "age": 65,
                        "weight": 70.0,
                        "sex": "female",
                        "serum_creatinine": 1.1,
                        "height": 165.0,
                        "bmi": 25.7
                    },
                    "clinical_assessment": "Moderate kidney function impairment",
                    "medication_guidance": "Dose adjustments required for many medications",
                    "monitoring_recommendations": "Close monitoring and nephrology consultation recommended",
                    "weight_recommendations": {
                        "bmi_category": "Overweight/Obese",
                        "weight_recommendation": "Consider using adjusted body weight or ideal body weight",
                        "accuracy_note": "Equation may overestimate clearance in obese patients",
                        "clinical_note": "Consider clinical context when interpreting results at weight extremes"
                    },
                    "formula_notes": [
                        "CrCl = [(140 - age) × weight × (0.85 if female)] / (72 × serum creatinine)",
                        "Historical equation, may overestimate GFR by 10-20%",
                        "Still used for specific medication dosing decisions"
                    ]
                }
            }
        }