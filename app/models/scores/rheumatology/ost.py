"""
Osteoporosis Self Assessment Tool (OST) Models

Request and response models for OST calculation.

References (Vancouver style):
1. Koh LK, Sedrine WB, Torralba TP, Kung A, Fujiwara S, Chan SP, et al. A simple tool 
   to identify asian women at increased risk of osteoporosis. Osteoporos Int. 
   2001;12(8):699-705. doi: 10.1007/s001980170070. PMID: 11580084.
2. Adler RA, Tran MT, Petkov VI. Performance of the Osteoporosis Self-assessment 
   Screening Tool for osteoporosis in American men. Mayo Clin Proc. 2003 Jun;78(6):723-7. 
   doi: 10.4065/78.6.723. PMID: 12828971.
3. Richy F, Gourlay M, Ross PD, Sen SS, Radican L, De Ceulaer F, et al. Validation and 
   comparative evaluation of the osteoporosis self-assessment tool (OST) in a Caucasian 
   population from Belgium. QJM. 2004 Jan;97(1):39-46. doi: 10.1093/qjmed/hch002. 
   PMID: 14702510.
4. Richards JS, Lazzari AA, Teves Qualler DA, Desale S, Howard R, Kerr GS. Validation 
   of the osteoporosis self-assessment tool in US male veterans. J Clin Densitom. 2014 
   Jan-Mar;17(1):32-7. doi: 10.1016/j.jocd.2013.02.004. PMID: 23562111.

The OST is a simple screening tool that uses only age and body weight to identify 
individuals at risk for osteoporosis who may benefit from bone density testing. The 
tool has been validated in both women (91% sensitivity, 45% specificity) and men 
(93% sensitivity, 66% specificity) for predicting DXA-diagnosed osteoporosis.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class OstRequest(BaseModel):
    """
    Request model for Osteoporosis Self Assessment Tool (OST)
    
    The OST uses 2 simple variables to assess osteoporosis risk:
    
    Formula:
    OST = (weight in kg - age in years) × 0.2, truncated to integer
    
    Risk Categories for Women:
    - Low risk: OST > 1
    - Intermediate risk: OST -3 to 1
    - High risk: OST < -3
    
    Risk Categories for Men:
    - Low risk: OST > 3
    - Intermediate risk: OST -1 to 3
    - High risk: OST < -1

    References (Vancouver style):
    1. Koh LK, Sedrine WB, Torralba TP, Kung A, Fujiwara S, Chan SP, et al. A simple tool 
    to identify asian women at increased risk of osteoporosis. Osteoporos Int. 
    2001;12(8):699-705.
    2. Adler RA, Tran MT, Petkov VI. Performance of the Osteoporosis Self-assessment 
    Screening Tool for osteoporosis in American men. Mayo Clin Proc. 2003 Jun;78(6):723-7.
    """
    
    age: int = Field(
        ...,
        ge=40,
        le=120,
        description="Patient age in years. Must be between 40 and 120 years. The tool is validated for adults aged 40 years and older",
        example=65
    )
    
    weight: float = Field(
        ...,
        ge=20,
        le=200,
        description="Body weight in kilograms. Must be between 20 and 200 kg. If weight is in pounds, convert to kg by dividing by 2.205",
        example=70.5
    )
    
    sex: Literal["female", "male"] = Field(
        ...,
        description="Patient biological sex. Different risk thresholds apply for women and men. Women: 91% sensitivity, 45% specificity. Men: 93% sensitivity, 66% specificity",
        example="female"
    )
    
    @field_validator('age')
    def validate_age(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError("Age must be a number")
        return int(v)
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 65,
                "weight": 70.5,
                "sex": "female"
            }
        }


class OstResponse(BaseModel):
    """
    Response model for Osteoporosis Self Assessment Tool (OST)
    
    The OST score helps identify individuals who may benefit from bone density 
    testing (DXA scan). Different risk thresholds apply for women and men.
    
    Reference: Koh LK, et al. Osteoporos Int. 2001;12(8):699-705.
    """
    
    result: int = Field(
        ...,
        description="OST score calculated as (weight in kg - age in years) × 0.2, truncated to integer",
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended next steps based on the score and sex",
        example="This patient scores 1 on the OST scale for women, indicating intermediate risk of osteoporosis. Consider bone density testing (DXA scan) based on clinical judgment and other risk factors."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low risk, Intermediate risk, or High risk)",
        example="Intermediate risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Intermediate risk of osteoporosis"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "This patient scores 1 on the OST scale for women, indicating intermediate risk of osteoporosis. Consider bone density testing (DXA scan) based on clinical judgment and other risk factors.",
                "stage": "Intermediate risk",
                "stage_description": "Intermediate risk of osteoporosis"
            }
        }