"""
CAROC System Models

Request and response models for Canadian Association of Radiologists and 
Osteoporosis Canada (CAROC) System calculation.

References (Vancouver style):
1. Siminoski K, Leslie WD, Frame H, Hodsman A, Josse RG, Khan A, et al. 
   Recommendations for bone mineral density reporting in Canada: a shift to 
   absolute fracture risk assessment. J Clin Densitom. 2007 Apr-Jun;10(2):120-3. 
   doi: 10.1016/j.jocd.2007.01.001.
2. Leslie WD, Berger C, Langsetmo L, Lix LM, Adachi JD, Hanley DA, et al. 
   Construction and validation of a simplified fracture risk assessment tool 
   for Canadian women and men: results from the CaMos and Manitoba cohorts. 
   Osteoporos Int. 2011 Jun;22(6):1873-83. doi: 10.1007/s00198-010-1445-5.
3. Papaioannou A, Morin S, Cheung AM, Atkinson S, Brown JP, Feldman S, et al. 
   2010 clinical practice guidelines for the diagnosis and management of 
   osteoporosis in Canada: summary. CMAJ. 2010 Nov 23;182(17):1864-73. 
   doi: 10.1503/cmaj.100771.

The CAROC System is a simplified fracture risk assessment tool that estimates 
10-year absolute fracture risk for major osteoporotic fractures. It categorizes 
patients into low (<10%), moderate (10-20%), or high (>20%) risk based on age, 
sex, femoral neck T-score, and clinical risk factors.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Dict, Any


class CAROCSystemRequest(BaseModel):
    """
    Request model for CAROC System
    
    The CAROC System uses 5 key factors to assess fracture risk:
    
    Demographics:
    - Sex: Risk thresholds differ between males and females
    - Age: 50-85 years (tool validated for this age range)
    
    Bone Mineral Density:
    - Femoral neck T-score: Primary measurement for risk assessment
    - Note: T-score ≤-2.5 at any site (spine, hip, femoral neck) = at least moderate risk
    
    Clinical Risk Factors:
    - Fragility fracture: Prior fracture from fall at standing height or less after age 40
    - Glucocorticoid use: ≥3 months cumulative in past year at ≥7.5 mg prednisone daily
    
    Risk Elevation Rules:
    - Either risk factor elevates risk by one category
    - Both risk factors = automatic high risk regardless of BMD
    
    CAROC vs FRAX:
    - CAROC is simpler and doesn't require computer access
    - Shows high concordance (88-89%) with Canadian FRAX
    - FRAX is preferred when available as it includes more risk factors
    
    References (Vancouver style):
    1. Leslie WD, et al. Osteoporos Int. 2011;22(6):1873-83.
    2. Papaioannou A, et al. CMAJ. 2010;182(17):1864-73.
    """
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient's biological sex. Risk thresholds differ between males and females",
        example="female"
    )
    
    age: int = Field(
        ...,
        ge=50,
        le=85,
        description="Patient's age in years. CAROC validated for ages 50-85",
        example=65
    )
    
    femoral_neck_t_score: float = Field(
        ...,
        ge=-5,
        le=2,
        description="Femoral neck T-score from DXA scan. Negative values indicate bone loss. T-score ≤-2.5 indicates osteoporosis",
        example=-2.1
    )
    
    fragility_fracture: Literal["yes", "no"] = Field(
        ...,
        description="History of fragility fracture after age 40 (fracture from fall at standing height or less). Elevates risk by one category",
        example="no"
    )
    
    glucocorticoid_use: Literal["yes", "no"] = Field(
        ...,
        description="Current systemic glucocorticoid therapy ≥3 months in past year at prednisone-equivalent dose ≥7.5 mg daily. Elevates risk by one category",
        example="no"
    )
    
    @validator('femoral_neck_t_score')
    def validate_t_score(cls, v):
        if v > 1:
            raise ValueError("T-scores above 1 are uncommon and should be verified")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "sex": "female",
                "age": 65,
                "femoral_neck_t_score": -2.1,
                "fragility_fracture": "no",
                "glucocorticoid_use": "no"
            }
        }


class CAROCSystemResponse(BaseModel):
    """
    Response model for CAROC System
    
    Risk Categories:
    - Low Risk: <10% 10-year fracture risk
    - Moderate Risk: 10-20% 10-year fracture risk
    - High Risk: >20% 10-year fracture risk
    
    Treatment Recommendations by Risk:
    
    Low Risk:
    - Lifestyle modifications (calcium, vitamin D, exercise)
    - Fall prevention strategies
    - Repeat BMD in 3-5 years
    
    Moderate Risk:
    - Consider pharmacotherapy based on patient factors
    - May benefit from additional risk assessment (FRAX)
    - Consider vertebral imaging if symptoms present
    
    High Risk:
    - Pharmacotherapy strongly recommended
    - First-line: bisphosphonates or denosumab
    - Comprehensive fracture prevention program
    
    Clinical Notes:
    - CAROC is a screening tool, not diagnostic
    - Consider additional factors not captured by CAROC
    - May underestimate risk in certain populations
    
    Reference: Papaioannou A, et al. CMAJ. 2010;182(17):1864-73.
    """
    
    result: str = Field(
        ...,
        description="Fracture risk category (Low Risk, Moderate Risk, High Risk)",
        example="Moderate Risk"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (category)",
        example="category"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and treatment recommendations based on risk category",
        example="Moderate risk of major osteoporotic fracture over the next 10 years. Consider pharmacologic therapy based on patient preferences, additional risk factors, and BMD trends. Ensure adequate calcium and vitamin D supplementation. Implement fall prevention strategies. Consider vertebral imaging if height loss or back pain present."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Moderate Risk, High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the 10-year fracture risk percentage",
        example="10-20% 10-year fracture risk"
    )
    
    details: Dict[str, Any] = Field(
        ...,
        description="Additional calculation details including base risk and modifiers",
        example={
            "base_risk_category": "Moderate Risk",
            "fragility_fracture": "no",
            "glucocorticoid_use": "no",
            "femoral_neck_t_score": -2.1,
            "estimated_10_year_risk": "10-20%",
            "automatic_moderate_risk": False
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Moderate Risk",
                "unit": "category",
                "interpretation": "Moderate risk of major osteoporotic fracture over the next 10 years. Consider pharmacologic therapy based on patient preferences, additional risk factors, and BMD trends. Ensure adequate calcium and vitamin D supplementation. Implement fall prevention strategies. Consider vertebral imaging if height loss or back pain present.",
                "stage": "Moderate Risk",
                "stage_description": "10-20% 10-year fracture risk",
                "details": {
                    "base_risk_category": "Moderate Risk",
                    "fragility_fracture": "no",
                    "glucocorticoid_use": "no",
                    "femoral_neck_t_score": -2.1,
                    "estimated_10_year_risk": "10-20%",
                    "automatic_moderate_risk": False
                }
            }
        }