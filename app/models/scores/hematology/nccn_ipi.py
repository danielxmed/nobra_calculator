"""
National Comprehensive Cancer Network International Prognostic Index (NCCN-IPI) Models

Request and response models for NCCN-IPI calculation.

References (Vancouver style):
1. Zhou Z, Sehn LH, Rademaker AW, Gordon LI, Lacasce AS, Crosby-Thompson A, et al. 
   An enhanced International Prognostic Index (NCCN-IPI) for patients with diffuse 
   large B-cell lymphoma treated in the rituximab era. Blood. 2014 Feb 6;123(6):837-42. 
   doi: 10.1182/blood-2013-09-524108.
2. Ruppert AS, Dixon JG, Salles G, Wall A, Cunningham D, Poeschel V, et al. 
   International prognostic indices in diffuse large B-cell lymphoma: a comparison 
   of IPI, R-IPI, and NCCN-IPI. Blood. 2020 Jun 4;135(23):2041-2048. 
   doi: 10.1182/blood.2019002729.
3. Gleeson M, Hawkes EA, Peckitt C, Wotherspoon A, Attygalle A, Sharma B, et al. 
   Prognostic indices in diffuse large B-cell lymphoma in the rituximab era: an 
   analysis of the UK National Cancer Research Institute R-CHOP 14 versus 21 phase 3 
   trial. Br J Haematol. 2021 Feb;192(6):1015-1019. doi: 10.1111/bjh.16691.

The NCCN-IPI is an enhanced prognostic index specifically developed for patients with 
diffuse large B-cell lymphoma (DLBCL) in the rituximab era. It provides superior 
prognostic discrimination compared to the conventional IPI, particularly for low and 
high-risk patients. The score uses refined age and LDH categories along with extranodal 
involvement, Ann Arbor stage, and ECOG performance status to predict overall survival.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional, Dict, Any


class NccnIpiRequest(BaseModel):
    """
    Request model for National Comprehensive Cancer Network International Prognostic Index (NCCN-IPI)
    
    The NCCN-IPI is a refined prognostic scoring system for DLBCL patients that uses:
    
    1. Age (0-3 points):
       - ≤40 years: 0 points
       - >40-60 years: 1 point
       - >60-75 years: 2 points
       - >75 years: 3 points
    
    2. LDH ratio (0-2 points):
       - Normal (≤1× ULN): 0 points
       - >1-3× ULN: 1 point
       - ≥3× ULN: 2 points
    
    3. Extranodal sites in major organs (0-1 point):
       - No involvement: 0 points
       - Involvement of bone marrow, CNS, liver/GI tract, or lung: 1 point
    
    4. Ann Arbor stage (0-1 point):
       - Stage I or II: 0 points
       - Stage III or IV: 1 point
    
    5. ECOG performance status (0-1 point):
       - ECOG 0 or 1: 0 points
       - ECOG ≥2: 1 point
    
    Total score ranges from 0-8 points, stratifying patients into four risk groups.
    
    References (Vancouver style):
    1. Zhou Z, Sehn LH, Rademaker AW, Gordon LI, Lacasce AS, Crosby-Thompson A, et al. 
       An enhanced International Prognostic Index (NCCN-IPI) for patients with diffuse 
       large B-cell lymphoma treated in the rituximab era. Blood. 2014 Feb 6;123(6):837-42. 
       doi: 10.1182/blood-2013-09-524108.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description=(
            "Patient age in years. Age is stratified into four categories for scoring: "
            "≤40 years (0 points), >40-60 years (1 point), >60-75 years (2 points), "
            ">75 years (3 points). Age is a strong prognostic factor in DLBCL."
        ),
        example=65
    )
    
    ldh_ratio: float = Field(
        ...,
        ge=0.1,
        le=20.0,
        description=(
            "LDH (lactate dehydrogenase) ratio compared to upper limit of normal (ULN). "
            "Calculate as: patient's LDH value / laboratory's upper limit of normal. "
            "For example, if patient's LDH is 450 U/L and ULN is 250 U/L, ratio = 1.8. "
            "Scoring: ≤1.0 (0 points), >1.0-3.0 (1 point), ≥3.0 (2 points). "
            "Elevated LDH indicates tumor burden and cell turnover."
        ),
        example=1.5
    )
    
    extranodal_sites: Literal["yes", "no"] = Field(
        ...,
        description=(
            "Presence of extranodal disease in major organs. Answer 'yes' if there is "
            "involvement of any of the following sites: bone marrow, central nervous system "
            "(CNS), liver, gastrointestinal (GI) tract, or lung. Other extranodal sites "
            "do not count for this parameter. Scores 1 point if 'yes', 0 points if 'no'."
        ),
        example="no"
    )
    
    ann_arbor_stage: Literal["I", "II", "III", "IV"] = Field(
        ...,
        description=(
            "Ann Arbor staging for lymphoma. Stage I: Single lymph node region. "
            "Stage II: Two or more lymph node regions on same side of diaphragm. "
            "Stage III: Lymph node regions on both sides of diaphragm. "
            "Stage IV: Diffuse/disseminated involvement of extralymphatic organs. "
            "Stages I-II score 0 points, stages III-IV score 1 point."
        ),
        example="III"
    )
    
    ecog_performance_status: int = Field(
        ...,
        ge=0,
        le=4,
        description=(
            "Eastern Cooperative Oncology Group (ECOG) performance status. "
            "0 = Fully active, able to carry on all pre-disease activities. "
            "1 = Restricted in physically strenuous activity but ambulatory. "
            "2 = Ambulatory and capable of all self-care but unable to work. "
            "3 = Capable of only limited self-care, confined to bed/chair >50% of waking hours. "
            "4 = Completely disabled, confined to bed/chair, no self-care. "
            "ECOG 0-1 scores 0 points, ECOG ≥2 scores 1 point."
        ),
        example=1
    )
    
    @field_validator('age')
    def validate_age(cls, v):
        """Ensure age is within reasonable adult range"""
        if v < 18:
            raise ValueError("NCCN-IPI is validated for adult patients (age ≥18 years)")
        return v
    
    @field_validator('ldh_ratio')
    def validate_ldh_ratio(cls, v):
        """Ensure LDH ratio is positive and reasonable"""
        if v < 0.1:
            raise ValueError("LDH ratio must be at least 0.1")
        if v > 20:
            raise ValueError(
                "LDH ratio exceeds 20. Please verify this extreme value."
            )
        return round(v, 2)
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 65,
                "ldh_ratio": 1.5,
                "extranodal_sites": "no",
                "ann_arbor_stage": "III",
                "ecog_performance_status": 1
            }
        }


class NccnIpiResponse(BaseModel):
    """
    Response model for National Comprehensive Cancer Network International Prognostic Index (NCCN-IPI)
    
    The NCCN-IPI score ranges from 0-8 points and stratifies patients into four risk groups:
    - Low risk (0-1 points): 5-year OS ~96%
    - Low-intermediate risk (2-3 points): 5-year OS ~82%
    - High-intermediate risk (4-5 points): 5-year OS ~64%
    - High risk (6-8 points): 5-year OS ~33%
    
    This enhanced index provides better discrimination than conventional IPI, particularly 
    for identifying patients with excellent prognosis (low risk) and poor prognosis (high risk).
    
    Reference: Zhou Z, et al. Blood. 2014;123(6):837-42.
    """
    
    result: int = Field(
        ...,
        description=(
            "NCCN-IPI total score calculated from the five prognostic factors "
            "(range: 0-8 points). Higher scores indicate worse prognosis."
        ),
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description=(
            "Clinical interpretation including risk group, 5-year overall survival estimate, "
            "and treatment recommendations based on the NCCN-IPI score"
        ),
        example=(
            "5-year overall survival: 82%. Good prognosis with standard therapy. "
            "Standard R-CHOP remains appropriate."
        )
    )
    
    stage: str = Field(
        ...,
        description=(
            "Risk group classification based on NCCN-IPI score "
            "(Low, Low-Intermediate, High-Intermediate, or High)"
        ),
        example="Low-Intermediate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Low-intermediate risk"
    )
    
    components: Optional[Dict[str, int]] = Field(
        None,
        description=(
            "Breakdown of points contributed by each component: age_points, ldh_points, "
            "extranodal_sites, ann_arbor_stage, and ecog_status"
        ),
        example={
            "age_points": 2,
            "ldh_points": 1,
            "extranodal_sites": 0,
            "ann_arbor_stage": 0,
            "ecog_status": 0
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": (
                    "5-year overall survival: 82%. Good prognosis with standard therapy. "
                    "Standard R-CHOP remains appropriate."
                ),
                "stage": "Low-Intermediate",
                "stage_description": "Low-intermediate risk",
                "components": {
                    "age_points": 2,
                    "ldh_points": 1,
                    "extranodal_sites": 0,
                    "ann_arbor_stage": 0,
                    "ecog_status": 0
                }
            }
        }