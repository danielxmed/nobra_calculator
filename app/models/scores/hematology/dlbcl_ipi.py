"""
International Prognostic Index for Diffuse Large B-cell Lymphoma (IPI and R-IPI) Models

Request and response models for DLBCL IPI calculation.

References (Vancouver style):
1. A predictive model for aggressive non-Hodgkin's lymphoma. The International Non-Hodgkin's 
   Lymphoma Prognostic Factors Project. N Engl J Med. 1993 Sep 30;329(14):987-94. 
   doi: 10.1056/NEJM199309303291402.
2. The revised International Prognostic Index (R-IPI) is a better predictor of outcome than 
   the standard IPI for patients with diffuse large B-cell lymphoma treated with R-CHOP. 
   Blood. 2007 Mar 1;109(5):1857-61. doi: 10.1182/blood-2006-08-038257.
3. International prognostic indices in diffuse large B-cell lymphoma: a comparison of IPI, 
   R-IPI, and NCCN-IPI. Blood. 2020 Jun 11;135(23):2041-2048. 
   doi: 10.1182/blood.2019002729.

The International Prognostic Index (IPI) for DLBCL uses five independent risk factors to 
predict overall survival and stratify patients into risk groups. Each factor contributes 
1 point to the total score (range 0-5). The original IPI identifies 4 risk groups, while 
the Revised IPI (R-IPI) redistributes patients into 3 groups with better discrimination 
in the rituximab era. The IPI remains the most widely used prognostic tool for DLBCL.
"""

from pydantic import BaseModel, Field
from typing import Literal


class DlbclIpiRequest(BaseModel):
    """
    Request model for International Prognostic Index for Diffuse Large B-cell Lymphoma (IPI and R-IPI)
    
    The IPI uses five independent risk factors to assess prognosis in DLBCL patients:
    
    Age Categories:
    - 60_or_younger: Age ≤60 years (0 points)
    - older_than_60: Age >60 years (1 point)
    
    LDH Level:
    - normal: LDH ≤ upper limit of normal (0 points)
    - elevated: LDH > upper limit of normal (1 point)
    
    Ann Arbor Stage:
    - stage_i_ii: Limited disease, stages I-II (0 points)
    - stage_iii_iv: Advanced disease, stages III-IV (1 point)
    
    ECOG Performance Status:
    - 0_1: ECOG 0-1, good performance status (0 points)
    - 2_or_higher: ECOG ≥2, impaired performance status (1 point)
    
    Extranodal Sites:
    - 0_1_sites: 0-1 extranodal sites (0 points)
    - more_than_1: >1 extranodal site (1 point)

    Total score ranges from 0-5 points. Original IPI stratifies into 4 risk groups:
    Low (0-1), Low-Intermediate (2), High-Intermediate (3), High (4-5).
    R-IPI redistributes into 3 groups: Very Good (0-1), Good (2), Poor (3-5).

    References (Vancouver style):
    1. A predictive model for aggressive non-Hodgkin's lymphoma. The International Non-Hodgkin's 
    Lymphoma Prognostic Factors Project. N Engl J Med. 1993 Sep 30;329(14):987-94. 
    doi: 10.1056/NEJM199309303291402.
    2. The revised International Prognostic Index (R-IPI) is a better predictor of outcome than 
    the standard IPI for patients with diffuse large B-cell lymphoma treated with R-CHOP. 
    Blood. 2007 Mar 1;109(5):1857-61. doi: 10.1182/blood-2006-08-038257.
    3. International prognostic indices in diffuse large B-cell lymphoma: a comparison of IPI, 
    R-IPI, and NCCN-IPI. Blood. 2020 Jun 11;135(23):2041-2048. 
    doi: 10.1182/blood.2019002729.
    """
    
    age: Literal["60_or_younger", "older_than_60"] = Field(
        ...,
        description="Patient age at diagnosis. Age >60 years scores 1 point, ≤60 years scores 0 points",
        example="60_or_younger"
    )
    
    ldh_level: Literal["normal", "elevated"] = Field(
        ...,
        description="Serum lactate dehydrogenase (LDH) level relative to upper limit of normal. Elevated LDH scores 1 point, normal scores 0 points",
        example="elevated"
    )
    
    ann_arbor_stage: Literal["stage_i_ii", "stage_iii_iv"] = Field(
        ...,
        description="Ann Arbor staging for lymphoma extent. Stages III-IV (advanced disease) score 1 point, stages I-II (limited disease) score 0 points",
        example="stage_i_ii"
    )
    
    ecog_performance_status: Literal["0_1", "2_or_higher"] = Field(
        ...,
        description="Eastern Cooperative Oncology Group (ECOG) performance status. ECOG ≥2 (impaired function) scores 1 point, ECOG 0-1 (good function) scores 0 points. ECOG 0=fully active, 1=restricted in strenuous activity, 2=ambulatory >50% of time, 3=confined to bed/chair >50% of time, 4=completely disabled",
        example="0_1"
    )
    
    extranodal_sites: Literal["0_1_sites", "more_than_1"] = Field(
        ...,
        description="Number of extranodal disease sites. More than 1 extranodal site scores 1 point, 0-1 sites score 0 points. Extranodal sites include CNS, bone marrow, liver, lungs, GI tract, bone, kidney, skin, and other organs",
        example="0_1_sites"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": "60_or_younger",
                "ldh_level": "elevated",
                "ann_arbor_stage": "stage_i_ii",
                "ecog_performance_status": "0_1",
                "extranodal_sites": "0_1_sites"
            }
        }


class DlbclIpiResponse(BaseModel):
    """
    Response model for International Prognostic Index for Diffuse Large B-cell Lymphoma (IPI and R-IPI)
    
    The IPI score ranges from 0-5 points and provides risk stratification:
    
    Original IPI (4 risk groups):
    - Low Risk (0-1 points): 5-year OS ~73%
    - Low-Intermediate Risk (2 points): 5-year OS ~51%
    - High-Intermediate Risk (3 points): 5-year OS ~43%
    - High Risk (4-5 points): 5-year OS ~26%
    
    Revised IPI (R-IPI, 3 risk groups):
    - Very Good (0-1 points): 4-year PFS 94%, OS 94%
    - Good (2 points): Intermediate outcomes
    - Poor (3-5 points): Lowest survival rates
    
    Reference: The International Non-Hodgkin's Lymphoma Prognostic Factors Project. N Engl J Med. 1993;329(14):987-94.
    """
    
    result: int = Field(
        ...,
        description="IPI score calculated from five risk factors (range: 0-5 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with both IPI and R-IPI risk stratification and treatment recommendations",
        example="Good prognosis. IPI Low-Intermediate Risk: 5-year OS ~51%. R-IPI Good: Intermediate survival outcomes. Standard R-CHOP therapy recommended. Consider standard treatment approaches with close monitoring for response assessment."
    )
    
    stage: str = Field(
        ...,
        description="Risk category with both IPI and R-IPI classification",
        example="Low-Intermediate Risk (IPI) / Good (R-IPI)"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the score range",
        example="Score 2 points"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "Good prognosis. IPI Low-Intermediate Risk: 5-year OS ~51%. R-IPI Good: Intermediate survival outcomes. Standard R-CHOP therapy recommended. Consider standard treatment approaches with close monitoring for response assessment.",
                "stage": "Low-Intermediate Risk (IPI) / Good (R-IPI)",
                "stage_description": "Score 2 points"
            }
        }