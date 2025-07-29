"""
Binet Staging System for Chronic Lymphocytic Leukemia (CLL) Models

Request and response models for Binet staging of chronic lymphocytic leukemia.

References (Vancouver style):
1. Binet JL, Auquier A, Dighiero G, Chastang C, Piguet H, Goasguen J, et al. 
   A new prognostic classification of chronic lymphocytic leukemia derived from 
   a multivariate survival analysis. Cancer. 1981 Jul 1;48(1):198-206. 
   doi: 10.1002/1097-0142(19810701)48:1<198::AID-CNCR2820480131>3.0.CO;2-9.
2. Hallek M, Cheson BD, Catovsky D, Caligaris-Cappio F, Dighiero G, Döhner H, et al. 
   iwCLL guidelines for diagnosis, indications for treatment, response assessment, 
   and supportive management of CLL. Blood. 2018 Jun 21;131(25):2745-2760. 
   doi: 10.1182/blood-2017-09-806398.
3. Rai KR, Sawitsky A, Cronkite EP, Chanana AD, Levy RN, Pasternack BS. 
   Clinical staging of chronic lymphocytic leukemia. Blood. 1975 Aug;46(2):219-34. 
   doi: 10.1182/blood.V46.2.219.219.

The Binet Staging System is the European standard for chronic lymphocytic leukemia 
staging, developed by Jacques-Louis Binet and colleagues in 1981. It provides a 
simple, reproducible classification based on physical examination and basic 
laboratory tests, without requiring imaging studies.

The system evaluates five lymphoid areas (cervical, axillary, and inguinal lymph 
nodes, plus spleen and liver) and hematologic parameters (hemoglobin and platelet 
count). It classifies patients into three stages with distinct prognostic 
implications:

- **Stage A (Low Risk)**: <3 lymphoid areas involved, normal blood counts
- **Stage B (Intermediate Risk)**: ≥3 lymphoid areas involved, normal blood counts  
- **Stage C (High Risk)**: Anemia and/or thrombocytopenia present

This staging system correlates with survival outcomes and helps guide treatment 
decisions in CLL management. It is comparable to the American Rai staging system 
and remains widely used in European clinical practice and research.
"""

from pydantic import BaseModel, Field
from typing import Literal


class BinetStagingCllRequest(BaseModel):
    """
    Request model for Binet Staging System for Chronic Lymphocytic Leukemia (CLL)
    
    The Binet staging system evaluates five specific lymphoid areas and hematologic 
    parameters to classify CLL patients into prognostic groups:
    
    **Lymphoid Areas Assessed (5 total):**
    
    **1. Cervical Lymphadenopathy:**
    - Enlarged lymph nodes in the neck region
    - Palpable on physical examination
    - May be unilateral or bilateral
    
    **2. Axillary Lymphadenopathy:**
    - Enlarged lymph nodes in the underarm (armpit) region
    - Assessed bilaterally during physical examination
    - May be associated with upper extremity symptoms
    
    **3. Inguinal Lymphadenopathy:**
    - Enlarged lymph nodes in the groin region
    - Palpable on examination of bilateral inguinal areas
    - May be associated with lower extremity lymphedema
    
    **4. Splenomegaly:**
    - Enlarged spleen extending below the left costal margin
    - Assessed by palpation and/or imaging
    - May cause left upper quadrant discomfort or early satiety
    
    **5. Hepatomegaly:**
    - Enlarged liver extending below the right costal margin
    - Assessed by palpation and/or imaging
    - May indicate advanced disease or portal hypertension
    
    **Hematologic Parameters:**
    
    **Hemoglobin Level:**
    - Normal: ≥10 g/dL (≥100 g/L)
    - Anemia: <10 g/dL (<100 g/L)
    - Anemia indicates Stage C regardless of lymphoid involvement
    
    **Platelet Count:**
    - Normal: ≥100×10³/mm³ (≥100×10⁹/L)
    - Thrombocytopenia: <100×10³/mm³ (<100×10⁹/L)
    - Thrombocytopenia indicates Stage C regardless of lymphoid involvement
    
    **Clinical Assessment Guidelines:**
    - Physical examination should be systematic and thorough
    - Lymph nodes >1 cm in diameter are typically considered enlarged
    - Organomegaly should be confirmed by imaging when clinically indicated
    - Laboratory values should be recent and representative of stable disease state
    
    References (Vancouver style):
    1. Binet JL, Auquier A, Dighiero G, Chastang C, Piguet H, Goasguen J, et al. 
    A new prognostic classification of chronic lymphocytic leukemia derived from 
    a multivariate survival analysis. Cancer. 1981 Jul 1;48(1):198-206. 
    doi: 10.1002/1097-0142(19810701)48:1<198::AID-CNCR2820480131>3.0.CO;2-9.
    2. Hallek M, Cheson BD, Catovsky D, Caligaris-Cappio F, Dighiero G, Döhner H, et al. 
    iwCLL guidelines for diagnosis, indications for treatment, response assessment, 
    and supportive management of CLL. Blood. 2018 Jun 21;131(25):2745-2760. 
    doi: 10.1182/blood-2017-09-806398.
    3. Rai KR, Sawitsky A, Cronkite EP, Chanana AD, Levy RN, Pasternack BS. 
    Clinical staging of chronic lymphocytic leukemia. Blood. 1975 Aug;46(2):219-34. 
    doi: 10.1182/blood.V46.2.219.219.
    """
    
    cervical_lymphadenopathy: Literal["yes", "no"] = Field(
        ...,
        description="Enlarged cervical lymph nodes (neck region). Consider nodes >1 cm diameter as enlarged.",
        example="no"
    )
    
    axillary_lymphadenopathy: Literal["yes", "no"] = Field(
        ...,
        description="Enlarged axillary lymph nodes (underarm region). Assess bilaterally during physical examination.",
        example="yes"
    )
    
    inguinal_lymphadenopathy: Literal["yes", "no"] = Field(
        ...,
        description="Enlarged inguinal lymph nodes (groin region). Palpable nodes in bilateral inguinal areas.",
        example="yes"
    )
    
    splenomegaly: Literal["yes", "no"] = Field(
        ...,
        description="Enlarged spleen extending below the left costal margin. May be confirmed by imaging if clinically indicated.",
        example="yes"
    )
    
    hepatomegaly: Literal["yes", "no"] = Field(
        ...,
        description="Enlarged liver extending below the right costal margin. May be confirmed by imaging if clinically indicated.",
        example="no"
    )
    
    hemoglobin: float = Field(
        ...,
        ge=3.0,
        le=20.0,
        description="Hemoglobin level in g/dL. Anemia is defined as <10 g/dL and indicates Stage C regardless of lymphoid involvement.",
        example=12.5
    )
    
    platelet_count: int = Field(
        ...,
        ge=10,
        le=1000,
        description="Platelet count in thousands per mm³ (×10³/mm³). Thrombocytopenia is defined as <100×10³/mm³ and indicates Stage C.",
        example=150
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "cervical_lymphadenopathy": "no",
                "axillary_lymphadenopathy": "yes",
                "inguinal_lymphadenopathy": "yes", 
                "splenomegaly": "yes",
                "hepatomegaly": "no",
                "hemoglobin": 12.5,
                "platelet_count": 150
            }
        }


class BinetStagingCllResponse(BaseModel):
    """
    Response model for Binet Staging System for Chronic Lymphocytic Leukemia (CLL)
    
    The Binet system classifies CLL patients into three prognostic stages:
    
    **Stage A (Low Risk)**:
    - <3 lymphoid areas involved
    - Normal hemoglobin (≥10 g/dL) and platelets (≥100×10³/mm³)
    - Estimated median overall survival: ~12 years
    - Favorable prognosis with watchful waiting approach
    
    **Stage B (Intermediate Risk)**:
    - ≥3 lymphoid areas involved  
    - Normal hemoglobin (≥10 g/dL) and platelets (≥100×10³/mm³)
    - Estimated median overall survival: ~7 years
    - Moderate prognosis requiring closer monitoring
    
    **Stage C (High Risk)**:
    - Anemia (hemoglobin <10 g/dL) and/or thrombocytopenia (platelets <100×10³/mm³)
    - Any number of lymphoid areas may be involved
    - Estimated median overall survival: 2-4 years
    - Poor prognosis typically requiring treatment consideration
    
    Note: Survival estimates are based on historical data and may be improved 
    with modern targeted therapies such as BTK inhibitors and BCL-2 inhibitors.
    
    Reference: Binet JL, et al. Cancer. 1981;48(1):198-206.
    """
    
    result: str = Field(
        ...,
        description="Binet staging classification for CLL (Stage A, Stage B, or Stage C)",
        example="Stage B"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the staging result",
        example="stage"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with prognosis and management recommendations based on Binet stage",
        example="Intermediate risk CLL with moderate prognosis. Estimated median overall survival: ~7 years. May require earlier treatment consideration. Monitor closely for disease progression and development of symptoms."
    )
    
    stage: str = Field(
        ...,
        description="Binet stage classification (Stage A, Stage B, or Stage C)",
        example="Stage B"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the stage criteria and risk level",
        example="Intermediate risk - ≥3 lymphoid areas involved, normal Hgb and platelets"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Stage B",
                "unit": "stage",
                "interpretation": "Intermediate risk CLL with moderate prognosis. Estimated median overall survival: ~7 years. May require earlier treatment consideration. Monitor closely for disease progression and development of symptoms.",
                "stage": "Stage B",
                "stage_description": "Intermediate risk - ≥3 lymphoid areas involved, normal Hgb and platelets"
            }
        }