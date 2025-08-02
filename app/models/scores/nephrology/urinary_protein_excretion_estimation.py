"""
Urinary Protein Excretion Estimation Models

Request and response models for Urinary Protein Excretion Estimation calculation.

References (Vancouver style):
1. Ginsberg JM, Chang BS, Matarese RA, Garella S. Use of single voided urine samples 
   to estimate quantitative proteinuria. N Engl J Med. 1983;309(25):1543-6.
2. Wahbeh AM, Ewais MH, Elsharif ME. Comparison of 24-hour urinary protein and 
   protein-to-creatinine ratio in the assessment of proteinuria. 
   Saudi J Kidney Dis Transpl. 2009;20(3):443-7.

The Urinary Protein Excretion Estimation provides a convenient alternative to 24-hour 
urine collection for estimating daily protein excretion. It uses the protein/creatinine 
ratio from a single random daytime urine sample to estimate 24-hour proteinuria.

Formula: 24-hour Urinary Protein Excretion (g/day) = Urine Protein (mg/dL) / Urine Creatinine (mg/dL)

This method is based on the principle that creatinine excretion is relatively constant 
throughout the day in patients with stable renal function, making the protein/creatinine 
ratio a reliable indicator of daily protein excretion.

Clinical significance:
- <0.2 g/day: Normal protein excretion
- 0.2-3.5 g/day: Abnormal proteinuria requiring investigation
- >3.5 g/day: Nephrotic range proteinuria requiring urgent evaluation
"""

from pydantic import BaseModel, Field
from typing import Union


class UrinaryProteinExcretionEstimationRequest(BaseModel):
    """
    Request model for Urinary Protein Excretion Estimation
    
    This calculator estimates 24-hour urinary protein excretion using the protein/creatinine 
    ratio from a single random daytime urine sample. It provides a convenient alternative 
    to cumbersome 24-hour urine collection.
    
    Requirements for accurate results:
    - Random daytime urine sample (avoid overnight or first morning samples)
    - Same urine sample used for both protein and creatinine measurements
    - Patient must have stable renal function (stable GFR)
    - Not reliable in acute kidney injury or unstable kidney function
    
    Laboratory Parameters:
    - Urine Protein: Concentration of protein in urine sample (mg/dL). Normal values 
      are typically very low in healthy individuals.
    - Urine Creatinine: Concentration of creatinine in the same urine sample (mg/dL). 
      Reflects muscle mass and renal excretion, typically 50-300 mg/dL in random samples.
    
    Clinical Applications:
    - Screening for proteinuria in patients with diabetes, hypertension, or kidney disease
    - Monitoring progression of chronic kidney disease
    - Evaluating patients for nephrotic syndrome
    - Alternative to 24-hour urine collection when convenience is important
    
    Limitations:
    - Less accurate in patients with type 1 diabetes when ratio >3.5 g/g
    - Cannot be used with unstable kidney function
    - Consider 24-hour collection if proteinuria >10 g/day
    - Correlation is lowest for overnight samples
    
    References:
    1. Ginsberg JM, Chang BS, Matarese RA, Garella S. Use of single voided urine samples 
       to estimate quantitative proteinuria. N Engl J Med. 1983;309(25):1543-6.
    2. Wahbeh AM, Ewais MH, Elsharif ME. Comparison of 24-hour urinary protein and 
       protein-to-creatinine ratio in the assessment of proteinuria. 
       Saudi J Kidney Dis Transpl. 2009;20(3):443-7.
    """
    
    urine_protein_mg_dl: float = Field(
        ...,
        description="Urine protein concentration in milligrams per deciliter from random daytime urine sample. Normal values are typically <30 mg/dL in healthy individuals.",
        ge=0,
        le=1000,
        example=45.0
    )
    
    urine_creatinine_mg_dl: float = Field(
        ...,
        description="Urine creatinine concentration in milligrams per deciliter from the same urine sample. Typical range is 50-300 mg/dL, varies with muscle mass and hydration status.",
        ge=10,
        le=500,
        example=120.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "urine_protein_mg_dl": 45.0,
                "urine_creatinine_mg_dl": 120.0
            }
        }


class UrinaryProteinExcretionEstimationResponse(BaseModel):
    """
    Response model for Urinary Protein Excretion Estimation
    
    The estimated 24-hour urinary protein excretion provides important information about 
    kidney function and helps identify patients with significant proteinuria:
    
    Clinical Interpretation:
    - Normal (<0.2 g/day): No significant proteinuria, routine monitoring
    - Abnormal Proteinuria (0.2-3.5 g/day): Requires further investigation including:
      * Serum creatinine and eGFR
      * Complete urinalysis with microscopy
      * Assessment for diabetes, hypertension, other CKD causes
      * Nephrology consultation if persistent
    - Nephrotic Range (>3.5 g/day): Indicates significant glomerular disease requiring:
      * Urgent nephrology evaluation
      * Investigation for nephrotic syndrome causes
      * Consider renal biopsy
      * Check lipid profile and albumin levels
    
    Clinical Significance:
    Proteinuria is an important marker of kidney disease and cardiovascular risk. Early 
    detection and management can slow progression of chronic kidney disease and reduce 
    cardiovascular complications.
    
    Advantages over 24-hour collection:
    - More convenient for patients and healthcare providers
    - Eliminates collection errors and incomplete samples
    - Immediate results available
    - Suitable for outpatient screening and monitoring
    
    Reference: Ginsberg JM, et al. N Engl J Med. 1983;309(25):1543-6.
    """
    
    result: float = Field(
        ...,
        description="Estimated 24-hour urinary protein excretion in grams per day",
        example=0.38
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for protein excretion",
        example="g/day"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with recommendations based on the level of protein excretion",
        example="Estimated 24-hour protein excretion of 0.38 g/day indicates abnormal proteinuria (0.2-3.5 g/day). This level warrants further investigation to determine the underlying cause. Consider additional testing including serum creatinine, eGFR, urinalysis with microscopy, and nephrology consultation if persistent. Rule out diabetes, hypertension, and other causes of chronic kidney disease."
    )
    
    stage: str = Field(
        ...,
        description="Classification of proteinuria level (Normal, Abnormal Proteinuria, Nephrotic Range)",
        example="Abnormal Proteinuria"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the proteinuria classification",
        example="Investigate further"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0.38,
                "unit": "g/day",
                "interpretation": "Estimated 24-hour protein excretion of 0.38 g/day indicates abnormal proteinuria (0.2-3.5 g/day). This level warrants further investigation to determine the underlying cause. Consider additional testing including serum creatinine, eGFR, urinalysis with microscopy, and nephrology consultation if persistent. Rule out diabetes, hypertension, and other causes of chronic kidney disease.",
                "stage": "Abnormal Proteinuria",
                "stage_description": "Investigate further"
            }
        }