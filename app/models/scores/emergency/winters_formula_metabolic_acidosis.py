"""
Winters' Formula for Metabolic Acidosis Compensation Models

Request and response models for Winters' Formula calculation.

References (Vancouver style):
1. Winters RW, Engel K, Dell RB. Acid-base physiology in medicine. 
   A self-instruction program. London, UK: The London Company; 1967.
2. Adrogué HJ, Madias NE. Secondary responses to altered acid-base status: 
   the rules of engagement. J Am Soc Nephrol. 2010;21(6):920-923. 
   doi: 10.1681/ASN.2009121211
3. Berend K, de Vries AP, Gans RO. Physiological approach to assessment of 
   acid-base disturbances. N Engl J Med. 2014;371(15):1434-1445. 
   doi: 10.1056/NEJMra1003327
4. Kraut JA, Madias NE. Serum anion gap: its uses and limitations in clinical 
   medicine. Clin J Am Soc Nephrol. 2007;2(1):162-174. doi: 10.2215/CJN.03020906

Winters' Formula calculates the expected arterial pCO₂ compensation in pure metabolic 
acidosis using the equation: Expected pCO₂ = 1.5 × [HCO₃⁻] + 8 (± 2 mmHg). This 
formula helps clinicians assess whether respiratory compensation is appropriate, 
insufficient, or excessive in patients with metabolic acidosis. The measured pCO₂ 
should fall within ± 2 mmHg of the calculated value for appropriate compensation.
"""

from pydantic import BaseModel, Field
from typing import Optional


class WintersFormulaMetabolicAcidosisRequest(BaseModel):
    """
    Request model for Winters' Formula for Metabolic Acidosis Compensation
    
    Winters' Formula calculates the expected arterial pCO₂ in metabolic acidosis to 
    assess respiratory compensation adequacy:
    
    Formula: Expected pCO₂ = 1.5 × [HCO₃⁻] + 8 (± 2 mmHg)
    
    Parameters:
    - Bicarbonate (HCO₃⁻): Serum bicarbonate concentration in mEq/L
    - Measured pCO₂ (optional): Arterial pCO₂ in mmHg for comparison
    
    Normal Values:
    - Serum bicarbonate: 22-28 mEq/L
    - Arterial pCO₂: 35-45 mmHg
    
    Clinical Applications:
    - Assessment of respiratory compensation in metabolic acidosis
    - Detection of mixed acid-base disorders
    - Evaluation of respiratory function adequacy
    - Guidance for mechanical ventilation settings
    
    Interpretation:
    - Within ± 2 mmHg: Appropriate respiratory compensation
    - >2 mmHg higher: Inadequate compensation or concurrent respiratory acidosis
    - >2 mmHg lower: Overcompensation or concurrent respiratory alkalosis
    
    References (Vancouver style):
    1. Winters RW, Engel K, Dell RB. Acid-base physiology in medicine. 
       A self-instruction program. London, UK: The London Company; 1967.
    2. Adrogué HJ, Madias NE. Secondary responses to altered acid-base status: 
       the rules of engagement. J Am Soc Nephrol. 2010;21(6):920-923. 
       doi: 10.1681/ASN.2009121211
    3. Berend K, de Vries AP, Gans RO. Physiological approach to assessment of 
       acid-base disturbances. N Engl J Med. 2014;371(15):1434-1445. 
       doi: 10.1056/NEJMra1003327
    """
    
    bicarbonate: float = Field(
        ...,
        description="Serum bicarbonate (HCO₃⁻) concentration in mEq/L. Normal range: 22-28 mEq/L. Must be <22 mEq/L for metabolic acidosis",
        example=15.0,
        ge=5.0,
        le=35.0
    )
    
    measured_pco2: Optional[float] = Field(
        None,
        description="Measured arterial pCO₂ in mmHg (optional). Normal range: 35-45 mmHg. Used to compare with expected value and assess compensation adequacy",
        example=28.5,
        ge=10.0,
        le=80.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "bicarbonate": 15.0,
                "measured_pco2": 28.5
            }
        }


class WintersFormulaMetabolicAcidosisResponse(BaseModel):
    """
    Response model for Winters' Formula for Metabolic Acidosis Compensation
    
    Winters' Formula provides the expected arterial pCO₂ for metabolic acidosis 
    compensation and assesses respiratory compensation adequacy:
    
    Expected pCO₂ Calculation:
    - Formula: Expected pCO₂ = 1.5 × [HCO₃⁻] + 8 (± 2 mmHg)
    - Result represents the pCO₂ expected if respiratory compensation is appropriate
    
    Compensation Assessment:
    - Appropriate: Measured pCO₂ within ± 2 mmHg of expected
    - Undercompensation: Measured pCO₂ >2 mmHg higher than expected
    - Overcompensation: Measured pCO₂ >2 mmHg lower than expected
    
    Clinical Significance:
    - Appropriate compensation: Focus on treating underlying acidosis cause
    - Undercompensation: Assess respiratory function, consider ventilatory support
    - Overcompensation: Evaluate for concurrent respiratory alkalosis or mixed disorder
    
    Important Considerations:
    - Formula applies only to pure metabolic acidosis
    - Requires steady-state conditions (6-24 hours after onset)
    - Should be used with arterial blood gas analysis
    - Does not apply to mixed acid-base disorders
    
    Reference: Winters RW, et al. Acid-base physiology in medicine. 1967.
    """
    
    result: float = Field(
        ...,
        description="Expected arterial pCO₂ calculated using Winters' Formula (range varies based on bicarbonate level)",
        example=30.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the expected pCO₂",
        example="mmHg"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation based on expected pCO₂ and compensation analysis",
        example="The measured pCO₂ (28.5 mmHg) is within the expected range (28.5-32.5 mmHg) for metabolic acidosis, indicating appropriate respiratory compensation."
    )
    
    stage: str = Field(
        ...,
        description="Compensation status category (Expected Compensation, Appropriate Compensation, Undercompensation, Overcompensation)",
        example="Appropriate Compensation"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the compensation status",
        example="Expected respiratory compensation"
    )
    
    expected_range: dict = Field(
        ...,
        description="Expected pCO₂ range (± 2 mmHg tolerance) for appropriate compensation",
        example={"lower": 28.5, "upper": 32.5}
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 30.5,
                "unit": "mmHg",
                "interpretation": "The measured pCO₂ (28.5 mmHg) is within the expected range (28.5-32.5 mmHg) for metabolic acidosis, indicating appropriate respiratory compensation. Focus on identifying and treating the underlying cause of metabolic acidosis.",
                "stage": "Appropriate Compensation",
                "stage_description": "Expected respiratory compensation",
                "expected_range": {"lower": 28.5, "upper": 32.5}
            }
        }