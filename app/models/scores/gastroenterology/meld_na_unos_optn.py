"""
MELD Na (UNOS/OPTN) Models

Request and response models for MELD Na score calculation.

References (Vancouver style):
1. Kim WR, Biggins SW, Kremers WK, Wiesner RH, Kamath PS, Benson JT, et al. 
   Hyponatremia and mortality among patients on the liver-transplant waiting list. 
   N Engl J Med. 2008 Sep 4;359(10):1018-26. doi: 10.1056/NEJMoa0801209.
2. Kamath PS, Kim WR; Advanced Liver Disease Study Group. The model for end-stage 
   liver disease (MELD). Hepatology. 2007 Mar;45(3):797-805. doi: 10.1002/hep.21563.
3. OPTN Policy 9: Allocation of Livers and Liver-Intestines. Organ Procurement and 
   Transplantation Network. Effective January 11, 2016. Available from: 
   https://optn.transplant.hrsa.gov/policies-bylaws/policies/
4. Biggins SW, Kim WR, Terrault NA, Saab S, Balan V, Schiano T, et al. Evidence-based 
   incorporation of serum sodium concentration into MELD. Gastroenterology. 2006 
   May;130(6):1652-60. doi: 10.1053/j.gastro.2006.02.010.

The MELD Na score quantifies end-stage liver disease for transplant planning by 
incorporating serum sodium into the original MELD score. It has been used by UNOS 
for liver allocation since January 2016, replacing the original MELD score to better 
predict 3-month mortality and prioritize the sickest patients for transplant.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MeldNaUnosOptnRequest(BaseModel):
    """
    Request model for MELD Na (UNOS/OPTN) Score
    
    The MELD Na score incorporates four laboratory values to assess liver disease severity:
    
    Laboratory Parameters:
    - Creatinine: Kidney function indicator (adjusted to 4.0 if on dialysis)
    - Bilirubin: Liver's ability to clear bile
    - INR: Liver's ability to produce clotting factors
    - Sodium: Added in 2016 to improve mortality prediction
    
    Calculation Rules:
    - All lab values <1.0 are set to 1.0
    - Creatinine set to 4.0 if dialysis ≥2 times in past week
    - Sodium bounded between 125-137 mEq/L
    - Final score bounded between 6-40
    
    Clinical Application:
    The score is used to prioritize liver transplant candidates based on 3-month 
    mortality risk. Higher scores indicate greater medical urgency and higher 
    priority for transplant allocation. The addition of sodium improved the model's 
    ability to predict waitlist mortality, particularly for patients with hyponatremia.
    
    References (Vancouver style):
    1. Kim WR, Biggins SW, Kremers WK, Wiesner RH, Kamath PS, Benson JT, et al. 
       Hyponatremia and mortality among patients on the liver-transplant waiting list. 
       N Engl J Med. 2008 Sep 4;359(10):1018-26. doi: 10.1056/NEJMoa0801209.
    """
    
    creatinine: float = Field(
        ...,
        ge=0.01,
        le=40.0,
        description="Serum creatinine in mg/dL. Normal range: 0.6-1.2 mg/dL. If patient has "
                    "received dialysis (hemodialysis, peritoneal dialysis, or CVVHD) at least "
                    "twice in the past week, the value will be automatically set to 4.0. "
                    "Values <1.0 are set to 1.0 for calculation.",
        example=1.2
    )
    
    bilirubin: float = Field(
        ...,
        ge=0.01,
        le=100.0,
        description="Total bilirubin in mg/dL. Normal range: 0.3-1.2 mg/dL. Elevated levels "
                    "indicate impaired liver function and bile clearance. Values <1.0 are "
                    "set to 1.0 for calculation. Higher values indicate worse liver function.",
        example=2.5
    )
    
    inr: float = Field(
        ...,
        ge=0.01,
        le=100.0,
        description="International Normalized Ratio (INR). Normal range: 0.8-1.2. Measures "
                    "blood clotting time and reflects liver's synthetic function. Values <1.0 "
                    "are set to 1.0 for calculation. Higher values indicate impaired clotting.",
        example=1.5
    )
    
    sodium: float = Field(
        ...,
        ge=100.0,
        le=150.0,
        description="Serum sodium in mEq/L. Normal range: 135-145 mEq/L. Low sodium "
                    "(hyponatremia) is associated with worse prognosis in cirrhosis. "
                    "Values <125 are set to 125, values >137 are set to 137 for calculation.",
        example=134.0
    )
    
    dialysis_twice_past_week: Literal["yes", "no"] = Field(
        ...,
        description="Has the patient received dialysis (hemodialysis, peritoneal dialysis, "
                    "or continuous venovenous hemodialysis/CVVHD) at least twice in the past "
                    "week? If yes, creatinine value is automatically set to 4.0 mg/dL.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "creatinine": 1.2,
                "bilirubin": 2.5,
                "inr": 1.5,
                "sodium": 134.0,
                "dialysis_twice_past_week": "no"
            }
        }


class MeldNaUnosOptnResponse(BaseModel):
    """
    Response model for MELD Na (UNOS/OPTN) Score
    
    The MELD Na score stratifies patients into risk categories based on 3-month mortality:
    - Score 6-9: ~1.9% mortality
    - Score 10-19: ~6.0% mortality
    - Score 20-29: ~19.6% mortality
    - Score 30-39: ~52.6% mortality
    - Score ≥40: ~71.3% mortality
    
    Clinical Implications:
    - Scores ≥10: Consider hepatology referral
    - Scores ≥15: Active transplant evaluation typically initiated
    - Scores ≥20: High priority for transplant
    - Scores ≥30: May require ICU-level care
    
    The score is recalculated regularly as lab values change and is the primary 
    determinant of liver allocation priority in the United States.
    
    Reference: OPTN Policy 9: Allocation of Livers and Liver-Intestines. 2016.
    """
    
    result: int = Field(
        ...,
        description="MELD Na score (range: 6-40). Higher scores indicate greater liver "
                    "disease severity and higher priority for transplant allocation.",
        example=18
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including 3-month mortality risk and management "
                    "recommendations based on the calculated score",
        example="3-month mortality approximately 6.0%. Moderate priority for liver transplant. "
                "Consider hepatology referral if not already established. Monitor labs regularly."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Moderate Risk, High Risk, Very High Risk, or "
                    "Extremely High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the score range for this risk category",
        example="MELD Na 10-19"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 18,
                "unit": "points",
                "interpretation": "3-month mortality approximately 6.0%. Moderate priority for "
                                "liver transplant. Consider hepatology referral if not already "
                                "established. Monitor labs regularly.",
                "stage": "Moderate Risk",
                "stage_description": "MELD Na 10-19"
            }
        }