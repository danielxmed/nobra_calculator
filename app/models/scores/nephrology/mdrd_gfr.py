"""
MDRD GFR Equation Models

Request and response models for MDRD GFR calculation.

References (Vancouver style):
1. Levey AS, Coresh J, Greene T, Stevens LA, Zhang YL, Hendriksen S, et al. Using 
   standardized serum creatinine values in the modification of diet in renal disease 
   study equation for estimating glomerular filtration rate. Ann Intern Med. 
   2006 Aug 15;145(4):247-54. doi: 10.7326/0003-4819-145-4-200608150-00004.
2. Levey AS, Bosch JP, Lewis JB, Greene T, Rogers N, Roth D. A more accurate method 
   to estimate glomerular filtration rate from serum creatinine: a new prediction 
   equation. Modification of Diet in Renal Disease Study Group. Ann Intern Med. 
   1999 Mar 16;130(6):461-70. doi: 10.7326/0003-4819-130-6-199903160-00002.
3. National Kidney Foundation. K/DOQI clinical practice guidelines for chronic kidney 
   disease: evaluation, classification, and stratification. Am J Kidney Dis. 
   2002 Feb;39(2 Suppl 1):S1-266.
4. Inker LA, Eneanya ND, Coresh J, Tighiouart H, Wang D, Sang Y, et al. New 
   creatinine- and cystatin C-based equations to estimate GFR without race. 
   N Engl J Med. 2021 Nov 4;385(19):1737-1749. doi: 10.1056/NEJMoa2102953.

The MDRD (Modification of Diet in Renal Disease) equation estimates glomerular 
filtration rate (GFR) based on serum creatinine, age, sex, and race. This version 
uses IDMS-traceable creatinine values. While still widely used, the CKD-EPI 2021 
equation is now preferred by NKF/ASN for its improved accuracy, especially at 
higher GFR levels and without race-based adjustments.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MdrdGfrRequest(BaseModel):
    """
    Request model for MDRD GFR Equation
    
    The MDRD equation estimates GFR using four variables:
    
    1. Serum Creatinine:
       - Must be IDMS-traceable (standardized) creatinine
       - Normal range: 0.7-1.3 mg/dL (varies by lab, age, sex, muscle mass)
       - Higher values indicate worse kidney function
    
    2. Age:
       - Kidney function naturally declines with age
       - Equation accounts for age-related GFR decline
       - Valid for ages 18-120 years
    
    3. Sex:
       - Females typically have lower muscle mass
       - Adjustment factor of 0.742 applied for females
    
    4. Race:
       - Historically, Black individuals were thought to have higher muscle mass
       - Adjustment factor of 1.212 if Black race identified
       - Note: The 2021 CKD-EPI equation removed race from GFR calculation
    
    Formula:
    GFR = 175 × (Serum Cr)^-1.154 × (age)^-0.203 × 1.212 (if Black) × 0.742 (if female)
    
    Important limitations:
    - Less accurate for GFR >60 mL/min/1.73 m²
    - Not validated for acute kidney injury
    - May underestimate GFR in healthy individuals
    - Race-based adjustment is controversial and being phased out
    
    References (Vancouver style):
    1. Levey AS, Coresh J, Greene T, Stevens LA, Zhang YL, Hendriksen S, et al. Using 
       standardized serum creatinine values in the modification of diet in renal disease 
       study equation for estimating glomerular filtration rate. Ann Intern Med. 
       2006 Aug 15;145(4):247-54. doi: 10.7326/0003-4819-145-4-200608150-00004.
    """
    
    creatinine: float = Field(
        ...,
        ge=0.1,
        le=20.0,
        description="Serum creatinine level in mg/dL. Must be IDMS-traceable (standardized) value. Normal range varies by age, sex, and muscle mass but typically 0.7-1.3 mg/dL",
        example=1.2
    )
    
    age: float = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in years. GFR naturally declines with age. Equation validated for adults 18 years and older",
        example=65
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient biological sex. Females receive adjustment factor of 0.742 due to typically lower muscle mass",
        example="male"
    )
    
    black_race: Literal["yes", "no"] = Field(
        ...,
        description="Whether patient identifies as Black/African American. Historically used adjustment factor of 1.212. Note: Race-based eGFR adjustments are being phased out in favor of race-free equations like CKD-EPI 2021",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "creatinine": 1.2,
                "age": 65,
                "sex": "male",
                "black_race": "no"
            }
        }


class MdrdGfrResponse(BaseModel):
    """
    Response model for MDRD GFR Equation
    
    The MDRD equation provides estimated GFR normalized to 1.73 m² body surface area.
    
    CKD Stages based on GFR (KDIGO 2012):
    - G1 (≥90): Normal or high - kidney damage with normal GFR
    - G2 (60-89): Mildly decreased - kidney damage with mild ↓ GFR
    - G3a (45-59): Mildly to moderately decreased
    - G3b (30-44): Moderately to severely decreased
    - G4 (15-29): Severely decreased
    - G5 (<15): Kidney failure
    
    Clinical recommendations vary by stage:
    - G1-G2: Annual monitoring if CKD risk factors
    - G3a: Monitor every 6 months, consider nephrology referral
    - G3b: Monitor every 3 months, nephrology referral recommended
    - G4: Monitor every 3 months, prepare for renal replacement therapy
    - G5: Immediate nephrology care, initiate dialysis/transplant if uremic
    
    Important notes:
    - CKD diagnosis requires GFR <60 or evidence of kidney damage for ≥3 months
    - Consider albuminuria and clinical context when interpreting results
    - MDRD less accurate at higher GFR levels (>60 mL/min/1.73 m²)
    
    Reference: KDIGO 2012 Clinical Practice Guideline for the Evaluation and Management 
    of Chronic Kidney Disease. Kidney Int Suppl. 2013;3(1):1-150.
    """
    
    result: float = Field(
        ...,
        description="Estimated GFR in mL/min/1.73 m². Represents kidney filtration function normalized to standard body surface area",
        example=72.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for GFR",
        example="mL/min/1.73 m²"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including CKD stage classification, monitoring recommendations, and referral guidance",
        example="Mildly reduced kidney function. If evidence of kidney damage, this represents CKD stage 2. Monitor annually."
    )
    
    stage: str = Field(
        ...,
        description="KDIGO CKD stage classification (G1-G5) based on GFR level",
        example="G2"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the GFR category",
        example="Mildly decreased"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 72.5,
                "unit": "mL/min/1.73 m²",
                "interpretation": "Mildly reduced kidney function. If evidence of kidney damage, this represents CKD stage 2. Monitor annually.",
                "stage": "G2",
                "stage_description": "Mildly decreased"
            }
        }