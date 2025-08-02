"""
Transtubular Potassium Gradient (TTKG) Models

Request and response models for TTKG calculation.

References (Vancouver style):
1. Ethier JH, Kamel KS, Magner PO, Lemann J Jr, Halperin ML. The transtubular 
   potassium concentration in patients with hypokalemia and hyperkalemia. 
   Am J Kidney Dis. 1990 Apr;15(4):309-15. PMID: 2321642.
2. Choi MJ, Ziyadeh FN. The utility of the transtubular potassium gradient in 
   the evaluation of hyperkalemia. J Am Soc Nephrol. 2008 Mar;19(3):424-6. 
   doi: 10.1681/ASN.2007091017.
3. Kamel KS, Halperin ML. Intrarenal urea recycling leads to a higher rate of 
   renal excretion of potassium: an hypothesis with clinical implications. 
   Curr Opin Nephrol Hypertens. 2011 Sep;20(5):547-54. 
   doi: 10.1097/MNH.0b013e328349b8f9.

The transtubular potassium gradient (TTKG) estimates the ratio of potassium 
in the lumen of the cortical collecting duct (CCD) to that in the peritubular 
capillaries. It helps evaluate whether the kidneys are appropriately responding 
to hyperkalemia or hypokalemia.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class TtkgRequest(BaseModel):
    """
    Request model for Transtubular Potassium Gradient (TTKG)
    
    TTKG evaluates renal potassium handling by estimating the gradient across
    the cortical collecting duct. It requires measurements of potassium and
    osmolality in both urine and serum.
    
    The formula is: TTKG = (Urine K × Serum osmolality) / (Serum K × Urine osmolality)
    
    Key validity requirements:
    - Urine osmolality should exceed serum osmolality
    - Urine sodium should ideally be >25 mmol/L
    
    References (Vancouver style):
    1. Ethier JH, Kamel KS, Magner PO, Lemann J Jr, Halperin ML. The transtubular 
       potassium concentration in patients with hypokalemia and hyperkalemia. 
       Am J Kidney Dis. 1990 Apr;15(4):309-15.
    """
    
    urine_potassium: float = Field(
        ...,
        gt=0,
        le=200,
        description="Urine potassium concentration in mEq/L. Normal range varies widely based on dietary intake",
        example=40.0
    )
    
    serum_potassium: float = Field(
        ...,
        ge=1.5,
        le=10,
        description="Serum potassium concentration in mEq/L. Normal range: 3.5-5.0 mEq/L",
        example=5.5
    )
    
    urine_osmolality: float = Field(
        ...,
        ge=50,
        le=1400,
        description="Urine osmolality in mOsm/kg. Normal range: 500-800 mOsm/kg (concentrated urine)",
        example=600.0
    )
    
    serum_osmolality: float = Field(
        ...,
        ge=250,
        le=350,
        description="Serum osmolality in mOsm/kg. Normal range: 275-295 mOsm/kg",
        example=290.0
    )
    
    @field_validator('urine_potassium')
    @classmethod
    def validate_urine_potassium(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Urine potassium must be positive")
        if v > 200:
            raise ValueError("Urine potassium >200 mEq/L is physiologically unlikely")
        return v
    
    @field_validator('serum_potassium')
    @classmethod
    def validate_serum_potassium(cls, v: float) -> float:
        if v < 1.5:
            raise ValueError("Serum potassium <1.5 mEq/L is life-threatening")
        if v > 10:
            raise ValueError("Serum potassium >10 mEq/L is physiologically unlikely")
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "urine_potassium": 40.0,
                "serum_potassium": 5.5,
                "urine_osmolality": 600.0,
                "serum_osmolality": 290.0
            }
        }
    }


class TtkgResponse(BaseModel):
    """
    Response model for Transtubular Potassium Gradient (TTKG)
    
    Interpretation guidelines:
    - Normal TTKG: 8-9 with normal diet
    - Hyperkalemia (K+ >5.0): TTKG ≥7 indicates appropriate renal response
    - Hyperkalemia (K+ >5.0): TTKG <7 suggests hypoaldosteronism
    - Hypokalemia (K+ <3.5): TTKG <3 indicates appropriate renal conservation
    - Hypokalemia (K+ <3.5): TTKG ≥3 suggests renal potassium wasting
    
    Reference: Ethier JH, et al. Am J Kidney Dis. 1990;15(4):309-15.
    """
    
    result: float = Field(
        ...,
        description="Calculated TTKG value (dimensionless)",
        example=4.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for dimensionless ratio)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation based on TTKG value and serum potassium level",
        example="TTKG of 4.0 (<7) in hyperkalemia suggests hypoaldosteronism or aldosterone resistance, indicating impaired renal potassium excretion. Consider mineralocorticoid deficiency, medications affecting the RAAS system (ACE inhibitors, ARBs, aldosterone antagonists), or type 4 RTA."
    )
    
    stage: str = Field(
        ...,
        description="Clinical classification (e.g., Appropriate Response, Hypoaldosteronism, Renal K+ Wasting)",
        example="Hypoaldosteronism"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the clinical finding",
        example="Impaired K+ excretion in hyperkalemia"
    )
    
    potassium_status: Literal["hyperkalemia", "hypokalemia", "normal"] = Field(
        ...,
        description="Current potassium status based on serum level",
        example="hyperkalemia"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "result": 4.0,
                "unit": "",
                "interpretation": "TTKG of 4.0 (<7) in hyperkalemia suggests hypoaldosteronism or aldosterone resistance, indicating impaired renal potassium excretion. Consider mineralocorticoid deficiency, medications affecting the RAAS system (ACE inhibitors, ARBs, aldosterone antagonists), or type 4 RTA.",
                "stage": "Hypoaldosteronism",
                "stage_description": "Impaired K+ excretion in hyperkalemia",
                "potassium_status": "hyperkalemia"
            }
        }
    }