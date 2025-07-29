"""
BALL Score for Relapsed/Refractory CLL Models

Request and response models for BALL Score calculation.

References (Vancouver style):
1. Soumerai JD, Ni A, Darif M, Londhe A, Xing G, Mun Y, et al. Prognostic risk score 
   for patients with relapsed or refractory chronic lymphocytic leukaemia treated with 
   targeted therapies or chemoimmunotherapy: a retrospective, pooled cohort study with 
   external validations. Lancet Haematol. 2019 Jul;6(7):e366-e374. 
   doi: 10.1016/S2352-3026(19)30085-7.
2. Gentile M, Morabito F, Del Poeta G, Mauro FR, Reda G, Sportoletti P, et al. 
   Survival risk score for real-life relapsed/refractory chronic lymphocytic leukemia 
   patients receiving ibrutinib. A campus CLL study. Leukemia. 2021 Jan;35(1):235-238. 
   doi: 10.1038/s41375-020-0816-y.
3. Soumerai JD, Ni A, Xing G, Huang J, Furman RR, Jones J, et al. Evaluation of the 
   CLL-IPI in relapsed and refractory chronic lymphocytic leukemia in idelalisib phase-3 
   trials. Leuk Lymphoma. 2019 Jun;60(6):1438-1446. doi: 10.1080/10428194.2018.1540782.

The BALL Score is a prognostic tool for patients with relapsed/refractory chronic 
lymphocytic leukemia (R/R CLL) receiving targeted therapies. BALL stands for:
Beta-2-microglobulin, Anemia, LDH, and Last therapy. The score stratifies patients 
into three risk groups with different 24-month overall survival rates.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class BallScoreRrCllRequest(BaseModel):
    """
    Request model for BALL Score for Relapsed/Refractory CLL
    
    The BALL Score uses 4 parameters to predict prognosis in R/R CLL patients:
    
    1. Beta-2-microglobulin: ≥5 mg/dL scores 1 point
    2. Anemia: Hgb <12 g/dL (men) or <11 g/dL (women) scores 1 point
    3. LDH: Above upper limit of normal scores 1 point
    4. Last therapy: <24 months since initiation scores 1 point
    
    Total score ranges from 0-4 points:
    - 0-1 points: Low risk (24-month OS: 89.7%)
    - 2-3 points: Intermediate risk (24-month OS: 79.5%)
    - 4 points: High risk (24-month OS: 55.8%)
    
    References:
    1. Soumerai JD, et al. Lancet Haematol. 2019;6(7):e366-e374.
    2. Gentile M, et al. Leukemia. 2021;35(1):235-238.
    """
    
    beta2_microglobulin: float = Field(
        ...,
        description="Beta-2-microglobulin level in mg/dL. Values ≥5 mg/dL score 1 point. Normal range typically 0.7-1.8 mg/dL",
        example=4.5,
        ge=0.1,
        le=50
    )
    
    hemoglobin: float = Field(
        ...,
        description="Hemoglobin level in g/dL. Anemia defined as <12 g/dL for men, <11 g/dL for women",
        example=11.5,
        ge=3,
        le=20
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient's biological sex. Used to determine anemia threshold (men: Hgb <12 g/dL, women: Hgb <11 g/dL)",
        example="male"
    )
    
    ldh: float = Field(
        ...,
        description="Lactate dehydrogenase (LDH) level in U/L. Compare to lab-specific upper limit of normal",
        example=250,
        ge=50,
        le=5000
    )
    
    ldh_upper_limit: float = Field(
        ...,
        description="Upper limit of normal for LDH in U/L (lab-specific). LDH above this value scores 1 point",
        example=245,
        ge=100,
        le=500
    )
    
    months_since_last_therapy: int = Field(
        ...,
        description="Months since initiation of last therapy. Values <24 months score 1 point",
        example=18,
        ge=0,
        le=600
    )
    
    @validator('beta2_microglobulin')
    def validate_beta2_microglobulin(cls, v):
        if v > 20:
            raise ValueError("Beta-2-microglobulin >20 mg/dL is extremely elevated. Please verify the value.")
        return v
    
    @validator('ldh')
    def validate_ldh(cls, v, values):
        if 'ldh_upper_limit' in values and v > values['ldh_upper_limit'] * 10:
            raise ValueError("LDH is >10x upper limit of normal. Please verify the value.")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "beta2_microglobulin": 4.5,
                "hemoglobin": 11.5,
                "sex": "male",
                "ldh": 250,
                "ldh_upper_limit": 245,
                "months_since_last_therapy": 18
            }
        }


class BallScoreRrCllResponse(BaseModel):
    """
    Response model for BALL Score for Relapsed/Refractory CLL
    
    The BALL Score stratifies R/R CLL patients into three risk groups:
    - Low risk (0-1 points): Best prognosis with targeted therapy
    - Intermediate risk (2-3 points): Moderate prognosis
    - High risk (4 points): Poor prognosis, consider clinical trials
    
    Reference: Soumerai JD, et al. Lancet Haematol. 2019;6(7):e366-e374.
    """
    
    result: int = Field(
        ...,
        description="BALL Score calculated from clinical and laboratory parameters (range: 0-4 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with 24-month overall survival estimate and management recommendations",
        example="Intermediate risk for mortality. Estimated 24-month overall survival: 79.5%. Patients require close monitoring and may benefit from more intensive surveillance."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Intermediate Risk, or High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk group",
        example="Intermediate risk group"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "Intermediate risk for mortality. Estimated 24-month overall survival: 79.5%. Patients require close monitoring and may benefit from more intensive surveillance.",
                "stage": "Intermediate Risk",
                "stage_description": "Intermediate risk group"
            }
        }