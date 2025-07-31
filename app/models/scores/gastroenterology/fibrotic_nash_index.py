"""
Fibrotic NASH Index (FNI) Models

Request and response models for FNI calculation.

References (Vancouver style):
1. Tavaglione F, Jamialahmadi O, De Vincentis A, Qadri S, Mowlaei ME, Mancina RM, 
   et al. Development and Validation of a Score for Fibrotic Nonalcoholic 
   Steatohepatitis. Clin Gastroenterol Hepatol. 2023 Jun;21(6):1523-1532.e1. 
   doi: 10.1016/j.cgh.2022.03.044. PMID: 35436611.

The Fibrotic NASH Index (FNI) is a simple non-invasive score that uses routine 
laboratory values (AST, HbA1c, HDL cholesterol) to screen for fibrotic 
nonalcoholic steatohepatitis (NASH) in individuals at high risk for NAFLD. 
It was developed and validated in a large international cohort and is particularly 
useful in primary care and endocrinology settings for identifying patients who 
need hepatology referral.
"""

from pydantic import BaseModel, Field
from typing import Literal


class FibroticNashIndexRequest(BaseModel):
    """
    Request model for Fibrotic NASH Index (FNI) calculation
    
    The FNI uses three routine laboratory parameters to estimate the probability 
    of fibrotic NASH:
    
    Formula: FNI = e^x / (1 + e^x)
    Where x = -10.33 + 2.54 × ln(AST) + 3.86 × ln(HbA1c) - 1.66 × ln(HDL)
    
    Parameters:
    - AST: Aspartate aminotransferase in U/L
    - HbA1c: Hemoglobin A1c (glycated hemoglobin) in %
    - HDL: HDL cholesterol in mg/dL
    
    Interpretation:
    - FNI < 0.10: Low risk - Fibrotic NASH ruled out (NPV 0.93)
    - FNI 0.10-0.33: Indeterminate risk - Further evaluation needed
    - FNI > 0.33: High risk - Likely fibrotic NASH (Specificity ≥0.90)
    
    Clinical Use:
    - Designed for primary care and endocrinology/diabetology settings
    - Best for ruling out rather than diagnosing fibrotic NASH
    - Should NOT be used in patients with alcohol use disorder or known chronic liver disease
    - Performance maintained in patients with diabetes (AUROC 0.78-0.95)
    
    Reference: Tavaglione F, et al. Clin Gastroenterol Hepatol. 2023;21(6):1523-1532.e1.
    """
    
    ast: float = Field(
        ...,
        gt=0,
        le=1000,
        description="Aspartate aminotransferase (AST) level in U/L. Normal range typically 10-40 U/L. Higher values indicate liver injury",
        example=45
    )
    
    hba1c: float = Field(
        ...,
        ge=3,
        le=20,
        description="Hemoglobin A1c (glycated hemoglobin) in %. Reflects average blood glucose over past 2-3 months. Normal <5.7%, prediabetes 5.7-6.4%, diabetes ≥6.5%",
        example=6.8
    )
    
    hdl: float = Field(
        ...,
        gt=0,
        le=200,
        description="HDL cholesterol level in mg/dL. Higher values are protective. Normal: Men ≥40 mg/dL, Women ≥50 mg/dL",
        example=38
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "ast": 45,
                "hba1c": 6.8,
                "hdl": 38
            }
        }


class FibroticNashIndexResponse(BaseModel):
    """
    Response model for Fibrotic NASH Index (FNI) calculation
    
    The FNI provides a probability score (0-1) for fibrotic NASH:
    
    Risk Categories:
    - Low Risk (<0.10): 
      - Fibrotic NASH ruled out with high confidence
      - Negative predictive value 0.93
      - Sensitivity 0.89-0.99
    
    - Indeterminate Risk (0.10-0.33): 
      - Cannot rule in or rule out fibrotic NASH
      - Requires additional evaluation
    
    - High Risk (>0.33): 
      - High probability of fibrotic NASH
      - Specificity ≥0.90
      - Positive predictive value 0.57
    
    Clinical Implications:
    - FNI > 0.1 indicates 4-fold increased risk of severe liver disease vs general population
    - Online calculator available at: https://fniscore.github.io/
    
    Reference: Tavaglione F, et al. Clin Gastroenterol Hepatol. 2023;21(6):1523-1532.e1.
    """
    
    result: float = Field(
        ...,
        ge=0,
        le=1,
        description="FNI score representing probability of fibrotic NASH (0-1 or 0-100%)",
        example=0.125
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the FNI score",
        example="probability"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with management recommendations based on FNI score",
        example="Cannot rule in or rule out fibrotic NASH. Consider additional non-invasive tests (e.g., FIB-4, NAFLD fibrosis score). May warrant referral to hepatology for further evaluation."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Indeterminate Risk, High Risk)",
        example="Indeterminate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of risk category",
        example="Further evaluation needed"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 0.125,
                "unit": "probability",
                "interpretation": "Cannot rule in or rule out fibrotic NASH. Consider additional non-invasive tests (e.g., FIB-4, NAFLD fibrosis score). May warrant referral to hepatology for further evaluation.",
                "stage": "Indeterminate Risk",
                "stage_description": "Further evaluation needed"
            }
        }