"""
BUN Creatinine Ratio Models

Request and response models for BUN Creatinine Ratio calculation.

References (Vancouver style):
1. Levey AS, Bosch JP, Lewis JB, Greene T, Rogers N, Roth D. A more accurate 
   method to estimate glomerular filtration rate from serum creatinine: a new 
   prediction equation. Modification of Diet in Renal Disease Study Group. 
   Ann Intern Med. 1999;130(6):461-470.
2. National Kidney Foundation. K/DOQI clinical practice guidelines for chronic 
   kidney disease: evaluation, classification, and stratification. Am J Kidney 
   Dis. 2002;39(2 Suppl 1):S1-266.
3. Schrier RW. Diseases of the Kidney and Urinary Tract. 8th ed. Philadelphia, 
   PA: Lippincott Williams & Wilkins; 2007.
4. Brenner BM, Rector FC. Brenner and Rector's The Kidney. 9th ed. Philadelphia, 
   PA: Saunders Elsevier; 2012.

The BUN Creatinine Ratio is a simple calculation that evaluates kidney function 
by comparing blood urea nitrogen (BUN) to serum creatinine levels. This ratio 
helps distinguish between different causes of kidney dysfunction:

- Normal ratio (10-20): Indicates healthy kidney function with appropriate 
  filtration of both BUN and creatinine
- Low ratio (<10): May suggest intrinsic renal disease, malnutrition, low 
  protein intake, liver disease, or overhydration
- High ratio (>20): May indicate prerenal azotemia (dehydration, heart failure), 
  gastrointestinal bleeding, high protein intake, or postrenal obstruction

This ratio is particularly useful in the initial evaluation of acute kidney 
injury to help determine the underlying cause and guide further diagnostic 
workup and treatment decisions.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any


class BunCreatinineRatioRequest(BaseModel):
    """
    Request model for BUN Creatinine Ratio calculation
    
    The BUN Creatinine Ratio evaluates kidney function by comparing two key markers:
    
    BUN (Blood Urea Nitrogen):
    - Normal range: 8-20 mg/dL (2.9-7.1 mmol/L)
    - Measures nitrogen-containing waste product from protein metabolism
    - Affected by protein intake, liver function, hydration status, and kidney function
    - Can be elevated in prerenal conditions (dehydration, heart failure)
    
    Serum Creatinine:
    - Normal range: 0.7-1.3 mg/dL (62-115 µmol/L)
    - Measures waste product from muscle metabolism
    - More specific marker of kidney function than BUN
    - Less affected by diet and hydration status
    - Varies with muscle mass, age, and gender
    
    Clinical Applications:
    - Distinguishing prerenal vs intrinsic renal vs postrenal causes of AKI
    - Initial assessment of kidney dysfunction
    - Monitoring response to treatment
    - Identifying patients needing further nephrology evaluation
    
    References (Vancouver style):
    1. Levey AS, Bosch JP, Lewis JB, Greene T, Rogers N, Roth D. A more accurate 
    method to estimate glomerular filtration rate from serum creatinine: a new 
    prediction equation. Modification of Diet in Renal Disease Study Group. 
    Ann Intern Med. 1999;130(6):461-470.
    2. National Kidney Foundation. K/DOQI clinical practice guidelines for chronic 
    kidney disease: evaluation, classification, and stratification. Am J Kidney 
    Dis. 2002;39(2 Suppl 1):S1-266.
    3. Schrier RW. Diseases of the Kidney and Urinary Tract. 8th ed. Philadelphia, 
    PA: Lippincott Williams & Wilkins; 2007.
    4. Brenner BM, Rector FC. Brenner and Rector's The Kidney. 9th ed. Philadelphia, 
    PA: Saunders Elsevier; 2012.
    """
    
    bun: float = Field(
        ...,
        description="Blood urea nitrogen level in mg/dL. Normal range: 8-20 mg/dL. Measures nitrogen waste from protein metabolism, affected by diet, hydration, and kidney function.",
        example=15.0,
        ge=1.0,
        le=200.0
    )
    
    creatinine: float = Field(
        ...,
        description="Serum creatinine level in mg/dL. Normal range: 0.7-1.3 mg/dL. More specific marker of kidney function, varies with muscle mass, age, and gender.",
        example=1.0,
        ge=0.1,
        le=20.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "bun": 15.0,
                "creatinine": 1.0
            }
        }


class BunCreatinineRatioResponse(BaseModel):
    """
    Response model for BUN Creatinine Ratio calculation
    
    The BUN Creatinine Ratio provides important diagnostic information:
    
    Ratio Interpretation:
    - Low (<10): Suggests intrinsic renal disease, malnutrition, liver disease, 
      or overhydration. May indicate acute tubular necrosis, glomerulonephritis, 
      or interstitial nephritis.
    - Normal (10-20): Indicates healthy kidney function with appropriate 
      filtration of both BUN and creatinine.
    - High (>20): May indicate prerenal azotemia (dehydration, heart failure, 
      shock), gastrointestinal bleeding, high protein intake, or postrenal 
      obstruction.
    
    Clinical Decision Making:
    - Helps distinguish between different causes of acute kidney injury
    - Guides initial management and further diagnostic workup
    - Should be interpreted alongside clinical context and other laboratory values
    - Not a substitute for comprehensive kidney function assessment (eGFR, urinalysis)
    
    Reference: National Kidney Foundation. K/DOQI clinical practice guidelines 
    for chronic kidney disease. Am J Kidney Dis. 2002;39(2 Suppl 1):S1-266.
    """
    
    result: float = Field(
        ...,
        description="BUN to creatinine ratio (calculated as BUN ÷ creatinine)",
        example=15.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the ratio",
        example="ratio"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and significance of the ratio result",
        example="Normal kidney function with appropriate filtration of both BUN and creatinine. This ratio indicates healthy renal physiology and adequate glomerular filtration rate."
    )
    
    stage: str = Field(
        ...,
        description="Classification category (Low, Normal, High)",
        example="Normal"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the ratio category",
        example="Normal BUN/Creatinine ratio"
    )
    
    clinical_recommendations: Dict[str, List[str]] = Field(
        ...,
        description="Categorized clinical recommendations based on the ratio result",
        example={
            "monitoring": [
                "Continue routine monitoring of kidney function",
                "Monitor trends in BUN and creatinine over time"
            ],
            "considerations": [
                "Normal kidney function indicated",
                "Maintain adequate hydration and avoid nephrotoxic agents"
            ]
        }
    )
    
    reference_values: Dict[str, Any] = Field(
        ...,
        description="Normal reference ranges and interpretation guidelines",
        example={
            "normal_bun_range": "8.0-20.0 mg/dL",
            "normal_creatinine_range": "0.7-1.3 mg/dL",
            "normal_ratio_range": "10.0-20.0",
            "ratio_interpretation": {
                "low": "<10 (intrinsic renal disease, malnutrition, liver disease)",
                "normal": "10-20 (normal kidney function)",
                "high": ">20 (prerenal azotemia, GI bleeding, high protein intake)"
            }
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 15.0,
                "unit": "ratio",
                "interpretation": "Normal kidney function with appropriate filtration of both BUN and creatinine. This ratio indicates healthy renal physiology and adequate glomerular filtration rate.",
                "stage": "Normal",
                "stage_description": "Normal BUN/Creatinine ratio",
                "clinical_recommendations": {
                    "monitoring": [
                        "Continue routine monitoring of kidney function",
                        "Monitor trends in BUN and creatinine over time"
                    ],
                    "considerations": [
                        "Normal kidney function indicated",
                        "Maintain adequate hydration and avoid nephrotoxic agents"
                    ]
                },
                "reference_values": {
                    "normal_bun_range": "8.0-20.0 mg/dL",
                    "normal_creatinine_range": "0.7-1.3 mg/dL",
                    "normal_ratio_range": "10.0-20.0",
                    "ratio_interpretation": {
                        "low": "<10 (intrinsic renal disease, malnutrition, liver disease)",
                        "normal": "10-20 (normal kidney function)",
                        "high": ">20 (prerenal azotemia, GI bleeding, high protein intake)"
                    }
                }
            }
        }