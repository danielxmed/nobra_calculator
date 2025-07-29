"""
Asymptomatic Myeloma Prognosis Models

Request and response models for Asymptomatic Myeloma Prognosis calculation.

References (Vancouver style):
1. Kyle RA, Remstein ED, Therneau TM, Dispenzieri A, Kurtin PJ, Hodnefield JM, et al. 
   Clinical course and prognosis of smoldering (asymptomatic) multiple myeloma. 
   N Engl J Med. 2007;356(25):2582-90.
2. Rajkumar SV, Landgren O, Mateos MV. Smoldering multiple myeloma. Blood. 2015;125(20):3069-75.
3. Mateos MV, Kumar S, Dimopoulos MA, González-Calle V, Kastritis E, Hajek R, et al. 
   International Myeloma Working Group risk stratification model for smoldering multiple myeloma (SMM). 
   Blood Cancer J. 2020;10(10):102.

The Asymptomatic Myeloma Prognosis score predicts risk of progression of asymptomatic 
(smoldering) multiple myeloma to active myeloma or amyloidosis. This score stratifies 
patients into three risk groups based on bone marrow plasmacytosis percentage and 
serum monoclonal protein level, helping identify patients who would benefit from 
closer monitoring or early intervention.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AsymptomaticMyelomaPrognosisRequest(BaseModel):
    """
    Request model for Asymptomatic Myeloma Prognosis
    
    This score uses two key parameters to stratify risk:
    
    Bone Marrow Plasmacytosis:
    - <10%: Lower percentage of plasma cells in bone marrow
    - ≥10%: Higher percentage of plasma cells in bone marrow (≥10%)
    
    Serum Monoclonal Protein:
    - <3: Lower serum M-protein level (<3 g/dL)
    - ≥3: Higher serum M-protein level (≥3 g/dL)
    
    Risk Groups:
    - Low Risk: Both factors low (<10% and <3 g/dL)
      * Median time to progression: ~117 months
      * Annual risk: 2-3%
    - Intermediate Risk: One factor high
      * Median time to progression: ~60-75 months  
      * Annual risk: 5-7%
    - High Risk: Both factors high (≥10% and ≥3 g/dL)
      * Median time to progression: ~26-27 months
      * Annual risk: 15-20%

    References (Vancouver style):
    1. Kyle RA, Remstein ED, Therneau TM, Dispenzieri A, Kurtin PJ, Hodnefield JM, et al. 
    Clinical course and prognosis of smoldering (asymptomatic) multiple myeloma. 
    N Engl J Med. 2007;356(25):2582-90.
    2. Rajkumar SV, Landgren O, Mateos MV. Smoldering multiple myeloma. Blood. 2015;125(20):3069-75.
    3. Mateos MV, Kumar S, Dimopoulos MA, González-Calle V, Kastritis E, Hajek R, et al. 
    International Myeloma Working Group risk stratification model for smoldering multiple myeloma (SMM). 
    Blood Cancer J. 2020;10(10):102.
    """
    
    bone_marrow_plasmacytosis: Literal["≥10%", "<10%"] = Field(
        ...,
        description="Average percentage of plasma cells from bone marrow aspirate and core biopsy. ≥10% indicates higher risk",
        example="<10%"
    )
    
    serum_monoclonal_protein: Literal["≥3", "<3"] = Field(
        ...,
        description="Serum monoclonal protein level on serum protein electrophoresis (g/dL). ≥3 g/dL indicates higher risk",
        example="<3"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "bone_marrow_plasmacytosis": "<10%",
                "serum_monoclonal_protein": "<3"
            }
        }


class AsymptomaticMyelomaPrognosisResponse(BaseModel):
    """
    Response model for Asymptomatic Myeloma Prognosis
    
    The score stratifies patients into three risk groups:
    - Low Risk: Both factors low (bone marrow <10% AND serum M-protein <3 g/dL)
    - Intermediate Risk: One factor high 
    - High Risk: Both factors high (bone marrow ≥10% AND serum M-protein ≥3 g/dL)
    
    Higher risk groups have shorter median time to progression and higher annual 
    risk of progression to symptomatic multiple myeloma.
    
    Reference: Kyle RA, et al. N Engl J Med. 2007;356(25):2582-90.
    """
    
    result: str = Field(
        ...,
        description="Risk group classification for progression to symptomatic multiple myeloma",
        example="Low Risk"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with median time to progression and annual risk estimates",
        example="Lowest risk of progression to symptomatic multiple myeloma. Median time to progression approximately 117 months. Annual risk of progression approximately 2-3%."
    )
    
    stage: str = Field(
        ...,
        description="Risk group classification",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the criteria for this risk group",
        example="Both bone marrow plasmacytosis <10% and serum M-protein <3 g/dL"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Low Risk",
                "unit": "",
                "interpretation": "Lowest risk of progression to symptomatic multiple myeloma. Median time to progression approximately 117 months. Annual risk of progression approximately 2-3%.",
                "stage": "Low Risk",
                "stage_description": "Both bone marrow plasmacytosis <10% and serum M-protein <3 g/dL"
            }
        }
