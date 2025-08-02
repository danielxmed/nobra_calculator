"""
MELD Score (Original, Pre-2016) Models

Request and response models for MELD Score (Original) calculation.

References (Vancouver style):
1. Kamath PS, Wiesner RH, Malinchoc M, Kremers W, Therneau TM, Kosberg CL, et al. 
   A model to predict survival in patients with end-stage liver disease. 
   Hepatology. 2001 Feb;33(2):464-70. doi: 10.1053/jhep.2001.22172.
2. Wiesner R, Edwards E, Freeman R, Harper A, Kim R, Kamath P, et al. Model for 
   end-stage liver disease (MELD) and allocation of donor livers. Gastroenterology. 
   2003 Jan;124(1):91-6. doi: 10.1053/gast.2003.50016.
3. Malinchoc M, Kamath PS, Gordon FD, Peine CJ, Rank J, ter Borg PC. A model to 
   predict poor survival in patients undergoing transjugular intrahepatic 
   portosystemic shunts. Hepatology. 2000 Apr;31(4):864-71. doi: 10.1053/he.2000.5852.

The original MELD score quantifies end-stage liver disease for transplant planning 
using three laboratory values: creatinine, bilirubin, and INR. This pre-2016 version 
does not include sodium and was replaced by MELD-Na in 2016 for UNOS allocation.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MeldScoreOriginalRequest(BaseModel):
    """
    Request model for MELD Score (Original, Pre-2016)
    
    The original MELD score uses three laboratory values to assess liver disease severity:
    
    Laboratory Parameters:
    - Creatinine: Kidney function indicator (adjusted to 4.0 if on dialysis)
    - Bilirubin: Liver's ability to clear bile
    - INR: Liver's ability to produce clotting factors
    
    Calculation Rules:
    - All lab values <1.0 are set to 1.0
    - Creatinine set to 4.0 if dialysis ≥2 times in past week
    - Final score bounded between 6-40
    
    Historical Context:
    Originally developed to predict mortality after TIPS procedures, MELD became the 
    standard for liver allocation by UNOS in 2002. It replaced the Child-Pugh score 
    due to its objective, reproducible nature based on laboratory values. The original 
    formula included etiology of liver disease, but this was removed for simplification.
    
    Clinical Application:
    The score predicts 3-month mortality in end-stage liver disease and determines 
    priority for liver transplant allocation. Values should be no more than 48 hours 
    old for accurate assessment.
    
    References (Vancouver style):
    1. Kamath PS, Wiesner RH, Malinchoc M, Kremers W, Therneau TM, Kosberg CL, et al. 
       A model to predict survival in patients with end-stage liver disease. 
       Hepatology. 2001 Feb;33(2):464-70. doi: 10.1053/jhep.2001.22172.
    """
    
    creatinine: float = Field(
        ...,
        ge=0.01,
        le=40.0,
        description="Serum creatinine in mg/dL. Normal range: 0.6-1.2 mg/dL. Reflects "
                    "kidney function, which is often impaired in advanced liver disease "
                    "(hepatorenal syndrome). If patient has received hemodialysis at least "
                    "twice in the past week, the value will be automatically set to 4.0. "
                    "Values <1.0 are set to 1.0 for calculation.",
        example=1.2
    )
    
    bilirubin: float = Field(
        ...,
        ge=0.00000001,
        le=50.0,
        description="Total bilirubin in mg/dL. Normal range: 0.3-1.2 mg/dL. Elevated "
                    "levels indicate impaired liver function and bile clearance. Direct "
                    "marker of liver synthetic and excretory function. Values <1.0 are "
                    "set to 1.0 for calculation.",
        example=2.5
    )
    
    inr: float = Field(
        ...,
        ge=0.1,
        le=20.0,
        description="International Normalized Ratio (INR). Normal range: 0.8-1.2. Measures "
                    "blood clotting time and reflects liver's synthetic function (production "
                    "of clotting factors). Prolonged INR indicates severe synthetic dysfunction. "
                    "Values <1.0 are set to 1.0 for calculation.",
        example=1.5
    )
    
    dialysis: Literal["yes", "no"] = Field(
        ...,
        description="Has the patient received hemodialysis at least twice in the past week? "
                    "This includes hemodialysis, peritoneal dialysis, or continuous venovenous "
                    "hemodialysis (CVVHD). If yes, creatinine value is automatically set to "
                    "4.0 mg/dL for calculation.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "creatinine": 1.2,
                "bilirubin": 2.5,
                "inr": 1.5,
                "dialysis": "no"
            }
        }


class MeldScoreOriginalResponse(BaseModel):
    """
    Response model for MELD Score (Original, Pre-2016)
    
    The MELD score stratifies patients into risk categories based on 3-month mortality:
    - Score 6-9: ~1.9% mortality
    - Score 10-19: ~6.0% mortality
    - Score 20-29: ~19.6% mortality
    - Score 30-39: ~52.6% mortality
    - Score ≥40: ~71.3% mortality
    
    Clinical Implications:
    - Scores ≥10: Consider hepatology referral and transplant evaluation
    - Scores ≥15: Active listing for transplant typically initiated
    - Scores ≥20: High priority for transplant
    - Scores ≥30: May require ICU-level care
    
    Limitations:
    - Does not account for complications like hepatic encephalopathy, ascites, or varices
    - May underestimate mortality in patients with hyponatremia (addressed in MELD-Na)
    - Not validated for acute liver failure or pediatric patients
    
    Reference: Wiesner R, et al. Gastroenterology. 2003;124(1):91-6.
    """
    
    result: int = Field(
        ...,
        description="Original MELD score (range: 6-40). Higher scores indicate greater "
                    "liver disease severity and higher priority for transplant allocation.",
        example=15
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including 3-month mortality risk and "
                    "management recommendations based on the calculated score",
        example="3-month mortality approximately 6.0%. Moderate priority for liver "
                "transplant. Consider hepatology referral if not established."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Moderate Risk, High Risk, Very High Risk, "
                    "or Extremely High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the score range for this risk category",
        example="MELD 10-19"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 15,
                "unit": "points",
                "interpretation": "3-month mortality approximately 6.0%. Moderate priority "
                                "for liver transplant. Consider hepatology referral if not "
                                "established.",
                "stage": "Moderate Risk",
                "stage_description": "MELD 10-19"
            }
        }