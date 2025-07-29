"""
Bicarbonate Deficit Calculator Models

Request and response models for Bicarbonate Deficit calculation.

References (Vancouver style):
1. Kurtz I. Acid-Base Case Studies. 2nd Ed. Trafford Publishing (2004); 68:150.
2. Forsythe SM, Schmidt GA. Sodium bicarbonate for the treatment of lactic acidosis. 
   Chest. 2000;117(1):260.
3. Kollef MH, et al. The Washington Manual of Critical Care. Lippincott Williams & Wilkins, 
   2007; p185:583.
4. Sabatini S, Kurtzman NA. Bicarbonate Therapy in Severe Metabolic Acidosis. 
   JASN. 2009;20(4):692-695.

The Bicarbonate Deficit calculator estimates total body bicarbonate deficit for assessment 
of metabolic acidosis severity and helps guide bicarbonate replacement therapy planning.
"""

from pydantic import BaseModel, Field
from typing import Optional


class BicarbonateDeficitRequest(BaseModel):
    """
    Request model for Bicarbonate Deficit calculation
    
    This calculator uses the standard formula:
    Bicarbonate Deficit = 0.4 × Weight (kg) × (Target HCO3 - Current HCO3)
    
    Where:
    - 0.4 = Distribution volume coefficient for bicarbonate
    - Weight = Patient weight in kilograms
    - Target HCO3 = Desired bicarbonate level (default: 24 mEq/L)
    - Current HCO3 = Measured serum bicarbonate level
    
    Normal bicarbonate range: 23-28 mEq/L
    
    Clinical Context:
    - Used primarily for severe metabolic acidosis (HCO3 < 15 mEq/L)
    - Provides estimate for bicarbonate replacement therapy
    - Consider underlying etiology before supplementation
    - Avoid overly rapid correction to prevent complications
    """
    
    weight: float = Field(
        ...,
        description="Patient weight in kilograms. Used to estimate total body bicarbonate distribution volume",
        ge=0.5,
        le=500,
        example=70.0
    )
    
    bicarbonate_level: float = Field(
        ...,
        description="Current serum bicarbonate level in mEq/L. Normal range is 23-28 mEq/L. Values <15 mEq/L indicate severe metabolic acidosis",
        ge=4,
        le=60,
        example=12.0
    )
    
    target_bicarbonate: Optional[float] = Field(
        None,
        description="Target bicarbonate level in mEq/L. Default is 24 mEq/L if not specified. Should be within physiologic range (15-30 mEq/L)",
        ge=15,
        le=30,
        example=24.0
    )
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "title": "Severe metabolic acidosis",
                    "value": {
                        "weight": 70.0,
                        "bicarbonate_level": 12.0,
                        "target_bicarbonate": 24.0
                    }
                },
                {
                    "title": "Moderate acidosis with default target",
                    "value": {
                        "weight": 80.0,
                        "bicarbonate_level": 16.0
                    }
                },
                {
                    "title": "Pediatric patient",
                    "value": {
                        "weight": 25.0,
                        "bicarbonate_level": 10.0,
                        "target_bicarbonate": 22.0
                    }
                }
            ]
        }


class BicarbonateDeficitResponse(BaseModel):
    """
    Response model for Bicarbonate Deficit calculation
    
    Returns the calculated bicarbonate deficit with detailed interpretation including:
    - Severity assessment based on current bicarbonate level
    - Clinical recommendations for bicarbonate replacement
    - Dosing guidance for initial treatment
    - Important clinical pearls and monitoring recommendations
    
    Note: This is an estimate of total body bicarbonate deficit. Clinical judgment 
    should always be used in conjunction with arterial blood gas monitoring.
    """
    
    result: float = Field(
        ...,
        description="Calculated bicarbonate deficit in milliequivalents (mEq). Represents total body bicarbonate needed to reach target level",
        example=336.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the bicarbonate deficit",
        example="mEq"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation including severity assessment, replacement recommendations, dosing guidance, and monitoring advice",
        example="Severe metabolic acidosis (HCO3 = 12.0 mEq/L). Bicarbonate replacement may be indicated. Estimated bicarbonate deficit: 336.0 mEq. This represents the total body bicarbonate needed to reach 24.0 mEq/L. Consider initial replacement of 168 mEq (50% of calculated deficit), then reassess with repeat arterial blood gas. Remember: treat underlying cause of acidosis, avoid overly rapid correction, and monitor for complications of bicarbonate therapy."
    )
    
    stage: str = Field(
        ...,
        description="Severity classification based on bicarbonate level (Normal, Mild Acidosis, Moderate Acidosis, Severe Acidosis)",
        example="Severe Acidosis"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the acidosis severity stage",
        example="Severe metabolic acidosis"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 336.0,
                "unit": "mEq",
                "interpretation": "Severe metabolic acidosis (HCO3 = 12.0 mEq/L). Bicarbonate replacement may be indicated. Estimated bicarbonate deficit: 336.0 mEq. This represents the total body bicarbonate needed to reach 24.0 mEq/L. Consider initial replacement of 168 mEq (50% of calculated deficit), then reassess with repeat arterial blood gas. Remember: treat underlying cause of acidosis, avoid overly rapid correction, and monitor for complications of bicarbonate therapy.",
                "stage": "Severe Acidosis",
                "stage_description": "Severe metabolic acidosis"
            }
        }