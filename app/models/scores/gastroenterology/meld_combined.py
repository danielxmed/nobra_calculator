"""
Model for End-Stage Liver Disease (Combined MELD) Models

Request and response models for Combined MELD assessment.

References (Vancouver style):
1. Kamath PS, Wiesner RH, Malinchoc M, Kremers W, Therneau TM, Kosberg CL, et al. 
   A model to predict survival in patients with end-stage liver disease. 
   Hepatology. 2001 Feb;33(2):464-70. doi: 10.1053/jhep.2001.22172.
2. Wiesner R, Edwards E, Freeman R, Harper A, Kim R, Kamath P, et al. Model for 
   end-stage liver disease (MELD) and allocation of donor livers. Gastroenterology. 
   2003 Jan;124(1):91-6. doi: 10.1053/gast.2003.50016.
3. Kim WR, Biggins SW, Kremers WK, Wiesner RH, Kamath PS, Benson JT, et al. 
   Hyponatremia and mortality among patients on the liver-transplant waiting list. 
   N Engl J Med. 2008 Sep 4;359(10):1018-26. doi: 10.1056/NEJMoa0801209.
4. Kim WR, Mannalithara A, Heimbach JK, Kamath PS, Asrani SK, Biggins SW, et al. 
   MELD 3.0: The Model for End-Stage Liver Disease Updated for the Modern Era. 
   Gastroenterology. 2021 Dec;161(6):1887-1895.e4. doi: 10.1053/j.gastro.2021.08.050.

The Model for End-Stage Liver Disease (MELD) is a numerical scoring system 
ranging from 6-40 that quantifies the severity of chronic liver disease and 
predicts 90-day mortality risk. It is the primary tool used for organ allocation 
in liver transplantation. This combined calculator offers three versions: 
Original MELD, MELD-Na (includes sodium), and MELD 3.0 (current standard with 
albumin, age, and sex adjustments).
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Optional


class MeldCombinedRequest(BaseModel):
    """
    Request model for Model for End-Stage Liver Disease (Combined MELD)
    
    The Combined MELD calculator offers three versions for liver transplant 
    planning and mortality risk assessment:
    
    Original MELD (Pre-2016):
    - Uses: bilirubin, creatinine, INR
    - Formula: 3.78×ln(bilirubin) + 11.2×ln(INR) + 9.57×ln(creatinine) + 6.43
    - Range: 6-40 points
    
    MELD-Na (UNOS/OPTN version):
    - Adds: sodium to original MELD
    - Improves prediction by incorporating hyponatremia
    - Better stratifies patients with similar MELD scores
    
    MELD 3.0 (Current Standard, effective 2023):
    - Adds: albumin, age, sex to MELD-Na components
    - More accurate mortality prediction, especially for women
    - Current OPTN standard for liver transplant allocation
    - Different formulas for ages 12-18 vs ≥18 years
    
    Parameter Requirements by Version:
    - original: bilirubin, creatinine, inr, dialysis_twice_in_week
    - meld_na: all original parameters + sodium
    - meld_3_0: all meld_na parameters + albumin, age, sex
    
    Clinical Interpretation:
    - 6-9: Mild disease, low mortality risk (<2%)
    - 10-14: Moderate disease, intermediate risk (6-20%)
    - 15-19: Severe disease, high risk (>20%), transplant threshold
    - 20-29: Very severe disease, very high risk (>50%)
    - 30-40: Critical disease, extremely high risk (>80%)

    References (Vancouver style):
    1. Kamath PS, Wiesner RH, Malinchoc M, Kremers W, Therneau TM, Kosberg CL, et al. 
       A model to predict survival in patients with end-stage liver disease. 
       Hepatology. 2001 Feb;33(2):464-70. doi: 10.1053/jhep.2001.22172.
    2. Wiesner R, Edwards E, Freeman R, Harper A, Kim R, Kamath P, et al. Model for 
       end-stage liver disease (MELD) and allocation of donor livers. Gastroenterology. 
       2003 Jan;124(1):91-6. doi: 10.1053/gast.2003.50016.
    3. Kim WR, Biggins SW, Kremers WK, Wiesner RH, Kamath PS, Benson JT, et al. 
       Hyponatremia and mortality among patients on the liver-transplant waiting list. 
       N Engl J Med. 2008 Sep 4;359(10):1018-26. doi: 10.1056/NEJMoa0801209.
    4. Kim WR, Mannalithara A, Heimbach JK, Kamath PS, Asrani SK, Biggins SW, et al. 
       MELD 3.0: The Model for End-Stage Liver Disease Updated for the Modern Era. 
       Gastroenterology. 2021 Dec;161(6):1887-1895.e4. doi: 10.1053/j.gastro.2021.08.050.
    """
    
    meld_version: Literal["original", "meld_na", "meld_3_0"] = Field(
        ...,
        description="MELD version to calculate. Original (pre-2016), MELD-Na (includes sodium), or MELD 3.0 (current standard with albumin, age, sex)",
        example="meld_3_0"
    )
    
    bilirubin: float = Field(
        ...,
        ge=0.1,
        le=50.0,
        description="Serum bilirubin in mg/dL. Minimum value of 1.0 mg/dL used in calculations. Recent lab value within 48 hours preferred",
        example=2.5
    )
    
    creatinine: float = Field(
        ...,
        ge=0.1,
        le=15.0,
        description="Serum creatinine in mg/dL. Minimum value of 1.0 mg/dL used in calculations. Maximum of 4.0 mg/dL applied if higher",
        example=1.2
    )
    
    inr: float = Field(
        ...,
        ge=0.8,
        le=10.0,
        description="International Normalized Ratio (INR) for prothrombin time. Minimum value of 1.0 used in calculations",
        example=1.5
    )
    
    sodium: Optional[float] = Field(
        None,
        ge=120,
        le=160,
        description="Serum sodium in mEq/L. Required for MELD-Na and MELD 3.0. Clamped between 125-137 mEq/L for calculations",
        example=135
    )
    
    albumin: Optional[float] = Field(
        None,
        ge=1.0,
        le=6.0,
        description="Serum albumin in g/dL. Required for MELD 3.0. Clamped between 1.5-3.5 g/dL for calculations",
        example=3.0
    )
    
    age: Optional[int] = Field(
        None,
        ge=12,
        le=120,
        description="Patient age in years. Required for MELD 3.0. Different formulas apply for ages 12-18 vs ≥18 years",
        example=45
    )
    
    sex: Optional[Literal["male", "female"]] = Field(
        None,
        description="Patient sex. Required for MELD 3.0. Female patients receive 1.33 coefficient adjustment",
        example="male"
    )
    
    dialysis_twice_in_week: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Patient received dialysis at least twice in the past week. If yes, creatinine is set to 4.0 mg/dL for calculations",
        example="no"
    )
    
    @validator('sodium')
    def sodium_required_for_versions(cls, v, values):
        if values.get('meld_version') in ['meld_na', 'meld_3_0'] and v is None:
            raise ValueError('sodium is required for MELD-Na and MELD 3.0')
        return v
    
    @validator('albumin')
    def albumin_required_for_meld_3_0(cls, v, values):
        if values.get('meld_version') == 'meld_3_0' and v is None:
            raise ValueError('albumin is required for MELD 3.0')
        return v
    
    @validator('age')
    def age_required_for_meld_3_0(cls, v, values):
        if values.get('meld_version') == 'meld_3_0' and v is None:
            raise ValueError('age is required for MELD 3.0')
        return v
    
    @validator('sex')
    def sex_required_for_meld_3_0(cls, v, values):
        if values.get('meld_version') == 'meld_3_0' and v is None:
            raise ValueError('sex is required for MELD 3.0')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "meld_version": "meld_3_0",
                "bilirubin": 2.5,
                "creatinine": 1.2,
                "inr": 1.5,
                "sodium": 135,
                "albumin": 3.0,
                "age": 45,
                "sex": "male",
                "dialysis_twice_in_week": "no"
            }
        }


class MeldCombinedResponse(BaseModel):
    """
    Response model for Model for End-Stage Liver Disease (Combined MELD)
    
    The MELD score ranges from 6-40 points and stratifies liver disease severity:
    
    Mild Disease (6-9 points):
    - Low 90-day mortality risk (<2%)
    - Generally not considered for transplantation
    - Monitor and manage underlying liver disease
    
    Moderate Disease (10-14 points):
    - Intermediate mortality risk (6-20%)
    - May consider transplantation evaluation
    - Regular monitoring and medical management
    
    Severe Disease (15-19 points):
    - High mortality risk (>20%)
    - Strong indication for transplantation evaluation
    - MELD ≥15 is generally the transplant threshold
    
    Very Severe Disease (20-29 points):
    - Very high mortality risk (>50%)
    - High priority for liver transplantation
    - Close monitoring and intensive management
    
    Critical Disease (30-40 points):
    - Extremely high mortality risk (>80%)
    - Highest priority for transplantation
    - Consider intensive care and urgent evaluation
    
    Version-Specific Information:
    - Original MELD: Based on bilirubin, creatinine, INR
    - MELD-Na: Incorporates sodium for better prediction
    - MELD 3.0: Current standard with sex, age, albumin adjustments
    
    Reference: Kamath PS, et al. Hepatology. 2001;33(2):464-70.
    """
    
    result: int = Field(
        ...,
        ge=6,
        le=40,
        description="MELD score indicating severity of liver disease and transplant priority (6-40 points)",
        example=18
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with mortality risk and transplant recommendations",
        example="Severe liver disease with high mortality risk (>20%). Strong indication for liver transplantation evaluation. MELD ≥15 is generally the threshold for transplant consideration."
    )
    
    stage: str = Field(
        ...,
        description="Disease severity category (Mild Disease, Moderate Disease, Severe Disease, Very Severe Disease, Critical Disease)",
        example="Severe Disease"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of mortality risk level",
        example="High mortality risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 18,
                "unit": "points",
                "interpretation": "Severe liver disease with high mortality risk (>20%). Strong indication for liver transplantation evaluation. MELD ≥15 is generally the threshold for transplant consideration.",
                "stage": "Severe Disease",
                "stage_description": "High mortality risk"
            }
        }