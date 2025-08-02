"""
United Kingdom Model for End-Stage Liver Disease (UKELD) Models

Request and response models for UKELD calculation.

References (Vancouver style):
1. Neuberger J, Gimson A, Davies M, Akyol M, O'Grady J, Burroughs A, Hudson M. 
   Selection of patients for liver transplantation and allocation of donated livers in the UK. 
   Gut. 2008;57(2):252-7.
2. Barber K, Madden S, Allen J, Collett D, Neuberger J, Gimson A. 
   Elective liver transplant list mortality: development of a United Kingdom end-stage liver disease score. 
   Transplantation. 2011;92(4):469-76.

The United Kingdom Model for End-Stage Liver Disease (UKELD) is a scoring system that predicts 
mortality risk in patients with end-stage liver disease for liver transplant planning. It was 
developed specifically for the UK population and uses four laboratory parameters: INR, serum 
creatinine, serum bilirubin, and serum sodium.

The UKELD formula is:
UKELD = 5.395 × ln(INR) + 1.485 × ln(creatinine, µmol/L) + 3.13 × ln(bilirubin, µmol/L) 
        - 81.565 × ln(sodium, mmol/L) + 435

A score ≥49 is the cutoff for transplant eligibility in the UK, corresponding to >9% 1-year 
mortality without transplantation. A score ≥60 predicts approximately 50% 1-year mortality.
"""

from pydantic import BaseModel, Field
from typing import Union


class UkeldRequest(BaseModel):
    """
    Request model for United Kingdom Model for End-Stage Liver Disease (UKELD)
    
    The UKELD uses four laboratory parameters to predict mortality risk in end-stage liver disease:
    
    Laboratory Parameters:
    - INR (International Normalized Ratio): Measure of blood clotting time, reflecting liver 
      synthetic function. Normal range ~0.8-1.2, elevated in liver disease.
    - Serum Creatinine: Marker of kidney function in µmol/L. Normal range ~60-120 µmol/L for adults.
      Elevated levels indicate renal impairment, common in advanced liver disease.
    - Serum Bilirubin: Marker of liver function in µmol/L. Normal range ~5-20 µmol/L. 
      Elevated levels indicate impaired bilirubin metabolism and clearance.
    - Serum Sodium: Electrolyte balance in mmol/L. Normal range ~135-145 mmol/L. 
      Hyponatremia is common in advanced liver disease and indicates poor prognosis.
    
    Clinical Significance:
    The UKELD score determines eligibility for liver transplantation in the UK healthcare system.
    Higher scores indicate greater mortality risk and higher transplant priority.
    
    Formula: UKELD = 5.395×ln(INR) + 1.485×ln(creatinine) + 3.13×ln(bilirubin) - 81.565×ln(sodium) + 435
    
    References:
    1. Neuberger J, Gimson A, Davies M, Akyol M, O'Grady J, Burroughs A, Hudson M. 
       Selection of patients for liver transplantation and allocation of donated livers in the UK. 
       Gut. 2008;57(2):252-7.
    2. Barber K, Madden S, Allen J, Collett D, Neuberger J, Gimson A. 
       Elective liver transplant list mortality: development of a United Kingdom end-stage liver disease score. 
       Transplantation. 2011;92(4):469-76.
    """
    
    inr: float = Field(
        ...,
        description="International Normalized Ratio (INR) - measure of blood clotting time reflecting liver synthetic function. Normal range ~0.8-1.2, elevated in liver disease.",
        ge=0.8,
        le=10.0,
        example=2.1
    )
    
    creatinine_umol_l: float = Field(
        ...,
        description="Serum creatinine concentration in micromoles per liter (µmol/L) - marker of kidney function. Normal range ~60-120 µmol/L, elevated in renal impairment.",
        ge=30,
        le=800,
        example=120
    )
    
    bilirubin_umol_l: float = Field(
        ...,
        description="Serum bilirubin concentration in micromoles per liter (µmol/L) - marker of liver function. Normal range ~5-20 µmol/L, elevated in liver disease.",
        ge=5,
        le=1000,
        example=85
    )
    
    sodium_mmol_l: float = Field(
        ...,
        description="Serum sodium concentration in millimoles per liter (mmol/L) - electrolyte balance marker. Normal range ~135-145 mmol/L, hyponatremia common in advanced liver disease.",
        ge=120,
        le=150,
        example=135
    )
    
    class Config:
        schema_extra = {
            "example": {
                "inr": 2.1,
                "creatinine_umol_l": 120,
                "bilirubin_umol_l": 85,
                "sodium_mmol_l": 135
            }
        }


class UkeldResponse(BaseModel):
    """
    Response model for United Kingdom Model for End-Stage Liver Disease (UKELD)
    
    The UKELD score predicts mortality risk in end-stage liver disease patients and determines 
    transplant eligibility in the UK healthcare system:
    
    Score Interpretation:
    - <49 points: Below transplant threshold (low mortality risk, <9% 1-year mortality)
    - 49-59 points: Transplant eligible (moderate-high mortality risk, >9% 1-year mortality) 
    - ≥60 points: High priority transplant (very high mortality risk, ~50% 1-year mortality)
    
    Clinical Use:
    - Determine eligibility for liver transplantation in the UK
    - Estimate patient prognosis and 1-year mortality risk
    - Prioritize patients on liver transplant waiting lists
    - Guide timing of transplant evaluation and supportive care
    
    The UKELD was developed specifically for the UK population and may not be directly applicable 
    to other healthcare systems or populations. It excludes patients with hepatocellular carcinoma, 
    who may qualify for transplantation through other criteria.
    
    Reference: Neuberger J, et al. Gut. 2008;57(2):252-7.
    """
    
    result: float = Field(
        ...,
        description="UKELD score calculated from laboratory parameters (typical range: 30-80 points)",
        example=52.3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the UKELD score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with transplant eligibility determination and management recommendations based on the UKELD score",
        example="UKELD score of 52.3 meets the UK cutoff for transplant eligibility (≥49), indicating >9% 1-year mortality risk without transplantation. Patient should be evaluated for liver transplantation and placed on the waiting list if appropriate. Optimize medical management while awaiting transplant."
    )
    
    stage: str = Field(
        ...,
        description="Transplant eligibility category (Below Transplant Threshold, Transplant Eligible, High Priority Transplant)",
        example="Transplant Eligible"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the mortality risk level",
        example="Moderate to high mortality risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 52.3,
                "unit": "points",
                "interpretation": "UKELD score of 52.3 meets the UK cutoff for transplant eligibility (≥49), indicating >9% 1-year mortality risk without transplantation. Patient should be evaluated for liver transplantation and placed on the waiting list if appropriate. Optimize medical management while awaiting transplant.",
                "stage": "Transplant Eligible",
                "stage_description": "Moderate to high mortality risk"
            }
        }