"""
CKD-EPI 2021 eGFR calculation models
"""

from pydantic import BaseModel, Field
from app.models.scores.shared.base_models import SexType


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