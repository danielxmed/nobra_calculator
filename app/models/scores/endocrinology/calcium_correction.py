"""
Calcium Correction for Hypoalbuminemia and Hyperalbuminemia Models

Request and response models for Calcium Correction calculation.

References (Vancouver style):
1. Payne RB, Little AJ, Williams RB, Milner JR. Interpretation of serum calcium 
   in patients with abnormal serum proteins. Br Med J. 1973 Dec 15;4(5893):643-6. 
   doi: 10.1136/bmj.4.5893.643.
2. Clase CM, Norman GL, Beecroft ML, Churchill DN. Albumin-corrected calcium and 
   ionized calcium in stable haemodialysis patients. Nephrol Dial Transplant. 
   2000 Nov;15(11):1841-6. doi: 10.1093/ndt/15.11.1841.
3. Gauci C, Moranne O, Fouqueray B, de la Faille R, Maruani G, Haymann JP, et al. 
   Pitfalls of measuring total blood calcium in patients with CKD. J Am Soc 
   Nephrol. 2008 Aug;19(8):1592-8. doi: 10.1681/ASN.2007040449.
4. Calvi LM, Bushinsky DA. When is it appropriate to order an ionized calcium? 
   J Am Soc Nephrol. 2008 Jul;19(7):1257-60. doi: 10.1681/ASN.2007121327.

The calcium correction formula adjusts total serum calcium for abnormal albumin 
levels, as approximately 40% of calcium is bound to albumin. However, recent 
evidence suggests this formula has significant limitations and ionized calcium 
measurement is preferred when available.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, Dict, Any, Optional


class CalciumCorrectionRequest(BaseModel):
    """
    Request model for Calcium Correction for Hypoalbuminemia and Hyperalbuminemia
    
    The calcium correction formula compensates for the fact that ~40% of serum 
    calcium is bound to albumin. When albumin levels are abnormal, total calcium 
    may not accurately reflect the physiologically active ionized calcium.
    
    Calcium: Total serum calcium measurement
    - Normal range (US): 8.5-10.5 mg/dL
    - Normal range (SI): 2.125-2.625 mmol/L
    - Includes both bound (40% to albumin, 10% to anions) and free (50%) calcium
    
    Albumin: Serum albumin level
    - Normal range (US): 3.5-5.5 g/dL
    - Normal range (SI): 35-55 g/L
    - Major binding protein for calcium in blood
    
    Unit System:
    - US/Standard: Uses mg/dL for calcium, g/dL for albumin
    - SI: Uses mmol/L for calcium, g/L for albumin
    
    Clinical Context:
    - Hypoalbuminemia (low albumin) can cause falsely low total calcium
    - Hyperalbuminemia (high albumin) can cause falsely high total calcium
    - Most commonly used in hospitalized patients, liver disease, malnutrition
    - Critical care patients often have significant albumin abnormalities
    
    Important Limitations:
    - Formula accuracy decreases with severe hypoalbuminemia
    - Poor performance in CKD/ESRD patients
    - May overestimate calcium, leading to false hypercalcemia diagnosis
    - Ionized calcium measurement is preferred when available
    - Recent guidelines suggest abandoning correction formulas entirely
    
    References (Vancouver style):
    1. Payne RB, et al. Br Med J. 1973;4(5893):643-6.
    2. Clase CM, et al. Nephrol Dial Transplant. 2000;15(11):1841-6.
    """
    
    calcium: float = Field(
        ...,
        description="Total serum calcium level. Normal: 8.5-10.5 mg/dL (US) or 2.125-2.625 mmol/L (SI).",
        example=7.8
    )
    
    albumin: float = Field(
        ...,
        description="Serum albumin level. Normal: 3.5-5.5 g/dL (US) or 35-55 g/L (SI).",
        example=2.5
    )
    
    unit_system: Optional[Literal["us", "si"]] = Field(
        "us",
        description="Unit system for calculations. 'us' uses mg/dL and g/dL, 'si' uses mmol/L and g/L.",
        example="us"
    )
    
    @field_validator('calcium')
    def validate_calcium(cls, v, values):
        # Since unit_system comes after calcium, we can't validate here
        # We'll handle unit-specific validation in the calculator
        return v
    
    @field_validator('albumin')
    def validate_albumin(cls, v, values):
        # Since unit_system comes after albumin, we can't validate here
        # We'll handle unit-specific validation in the calculator
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "calcium": 7.8,
                "albumin": 2.5,
                "unit_system": "us"
            }
        }


class CalciumCorrectionResponse(BaseModel):
    """
    Response model for Calcium Correction for Hypoalbuminemia and Hyperalbuminemia
    
    The corrected calcium represents an estimate of what the total calcium would 
    be if the albumin were normal (4 g/dL or 40 g/L).
    
    Formulas:
    - US: Corrected Ca = [0.8 × (4 - Patient's Albumin)] + Serum Ca
    - SI: Corrected Ca = Total Ca + 0.02 × (40 - Albumin)
    
    Interpretation:
    - Hypocalcemia: Requires evaluation for causes (hypoparathyroidism, vitamin D 
      deficiency, CKD, medications)
    - Normal: No calcium-related intervention needed
    - Hypercalcemia: Requires evaluation for causes (hyperparathyroidism, 
      malignancy, vitamin D intoxication)
    
    Clinical Pearls:
    - Symptoms of hypocalcemia: paresthesias, muscle cramps, tetany, seizures
    - Symptoms of hypercalcemia: "stones, bones, groans, psychiatric overtones"
    - Critical values usually <7 or >13 mg/dL require immediate attention
    - Consider ECG in severe cases (prolonged QT in hypocalcemia, short QT in 
      hypercalcemia)
    
    Formula Limitations:
    - Agreement with ionized calcium only 55-65% in general population
    - Even worse in CKD/ESRD patients
    - May lead to unnecessary treatment if relied upon exclusively
    - Should not replace clinical judgment or ionized calcium when indicated
    
    Reference: Payne RB, et al. Br Med J. 1973;4(5893):643-6.
    """
    
    result: float = Field(
        ...,
        description="Corrected calcium level adjusted for albumin",
        example=9.2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (mg/dL for US, mmol/L for SI)",
        example="mg/dL"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommendations based on corrected calcium",
        example="Calcium level is within normal range when adjusted for albumin. No immediate intervention needed based on calcium level alone."
    )
    
    stage: str = Field(
        ...,
        description="Calcium status category (Hypocalcemia, Normal, Hypercalcemia)",
        example="Normal"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the calcium status",
        example="Normal corrected calcium"
    )
    
    details: Dict[str, Any] = Field(
        ...,
        description="Detailed breakdown of the calculation components",
        example={
            "original_calcium": 7.8,
            "albumin": 2.5,
            "albumin_deficit": 1.5,
            "correction_applied": 1.2,
            "unit_system": "us"
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 9.0,
                "unit": "mg/dL",
                "interpretation": "Calcium level is within normal range when adjusted for albumin. No immediate intervention needed based on calcium level alone.",
                "stage": "Normal",
                "stage_description": "Normal corrected calcium",
                "details": {
                    "original_calcium": 7.8,
                    "albumin": 2.5,
                    "albumin_deficit": 1.5,
                    "correction_applied": 1.2,
                    "unit_system": "us"
                }
            }
        }