"""
International Prognostic Score for Asymptomatic Early-stage CLL (IPS-E) Models

Request and response models for IPS-E calculation.

References (Vancouver style):
1. Condoluci A, Terzi di Bergamo L, Langerbeins P, Hoechstetter MA, Herling CD, De Paoli L, 
   et al. International prognostic score for asymptomatic early-stage chronic lymphocytic 
   leukemia. Blood. 2020 May 21;135(21):1859-1869. doi: 10.1182/blood.2019003453.
2. Hallek M, Cheson BD, Catovsky D, Caligaris-Cappio F, Dighiero G, Döhner H, et al. 
   iwCLL guidelines for diagnosis, indications for treatment, response assessment, and 
   supportive management of CLL. Blood. 2018 Jun 21;131(25):2745-2760. 
   doi: 10.1182/blood-2017-09-806398.
3. Rai KR, Sawitsky A, Cronkite EP, Chanana AD, Levy RN, Pasternack BS. Clinical staging 
   of chronic lymphocytic leukemia. Blood. 1975 Aug;46(2):219-34. 
   doi: 10.1182/blood.V46.2.219.219.

The International Prognostic Score for Asymptomatic Early-stage CLL (IPS-E) is a validated 
prognostic tool developed to predict time to first treatment (TTFT) in patients with 
asymptomatic early-stage CLL. It uses three independent prognostic factors with equal 
weighting to stratify patients into low (score 0), intermediate (score 1), and high-risk 
(score 2-3) categories. The IPS-E was developed using data from 4,933 patients from 11 
international cohorts and demonstrates excellent discrimination for treatment-free 
survival prediction.
"""

from pydantic import BaseModel, Field
from typing import Literal


class IpsECllRequest(BaseModel):
    """
    Request model for International Prognostic Score for Asymptomatic Early-stage CLL (IPS-E)
    
    The IPS-E uses three independent prognostic factors to assess treatment risk:
    
    IGHV Mutational Status:
    - mutated: IGHV with <98% homology to germline sequences (0 points)
    - unmutated: IGHV with ≥98% homology to germline sequences (1 point)
    
    Absolute Lymphocyte Count:
    - 15_or_less: ≤15 × 10⁹/L at diagnosis (0 points)
    - greater_than_15: >15 × 10⁹/L at diagnosis (1 point)
    
    Palpable Lymph Nodes:
    - absent: No palpable lymph nodes on examination (0 points)
    - present: Palpable lymph nodes detected (1 point)
    
    Total score ranges from 0-3 points, stratifying patients into:
    - Low risk (score 0): 8.4% 5-year treatment risk
    - Intermediate risk (score 1): 28.4% 5-year treatment risk
    - High risk (score 2-3): 61.2% 5-year treatment risk

    References (Vancouver style):
    1. Condoluci A, Terzi di Bergamo L, Langerbeins P, Hoechstetter MA, Herling CD, De Paoli L, 
    et al. International prognostic score for asymptomatic early-stage chronic lymphocytic 
    leukemia. Blood. 2020 May 21;135(21):1859-1869. doi: 10.1182/blood.2019003453.
    2. Hallek M, Cheson BD, Catovsky D, Caligaris-Cappio F, Dighiero G, Döhner H, et al. 
    iwCLL guidelines for diagnosis, indications for treatment, response assessment, and 
    supportive management of CLL. Blood. 2018 Jun 21;131(25):2745-2760. 
    doi: 10.1182/blood-2017-09-806398.
    3. Rai KR, Sawitsky A, Cronkite EP, Chanana AD, Levy RN, Pasternack BS. Clinical staging 
    of chronic lymphocytic leukemia. Blood. 1975 Aug;46(2):219-34. 
    doi: 10.1182/blood.V46.2.219.219.
    """
    
    ighv_status: Literal["mutated", "unmutated"] = Field(
        ...,
        description="Immunoglobulin heavy variable gene (IGHV) mutational status. Unmutated IGHV (≥98% homology to germline) scores 1 point and indicates worse prognosis. Mutated IGHV (<98% homology) scores 0 points and indicates better prognosis",
        example="mutated"
    )
    
    lymphocyte_count: Literal["15_or_less", "greater_than_15"] = Field(
        ...,
        description="Absolute lymphocyte count at diagnosis in ×10⁹/L. Count >15×10⁹/L scores 1 point and represents higher tumor burden. Count ≤15×10⁹/L scores 0 points",
        example="15_or_less"
    )
    
    palpable_lymph_nodes: Literal["absent", "present"] = Field(
        ...,
        description="Presence of palpable lymph nodes on physical examination. Present lymph nodes score 1 point and indicate more advanced disease within early stages. Absent lymph nodes score 0 points",
        example="absent"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "ighv_status": "mutated",
                "lymphocyte_count": "15_or_less",
                "palpable_lymph_nodes": "absent"
            }
        }


class IpsECllResponse(BaseModel):
    """
    Response model for International Prognostic Score for Asymptomatic Early-stage CLL (IPS-E)
    
    The IPS-E score ranges from 0-3 points and provides risk stratification for time to first treatment:
    
    Risk Categories:
    - Low Risk (0 points): 5-year treatment risk 8.4%, 1-year risk <0.1%
    - Intermediate Risk (1 point): 5-year treatment risk 28.4%, 1-year risk 3.1%
    - High Risk (2-3 points): 5-year treatment risk 61.2%
    
    The score helps guide monitoring frequency and clinical trial eligibility for 
    asymptomatic early-stage CLL patients.
    
    Reference: Condoluci A, et al. Blood. 2020;135(21):1859-1869.
    """
    
    result: int = Field(
        ...,
        description="IPS-E score calculated from three prognostic factors (range: 0-3 points)",
        example=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with treatment risk prediction and monitoring recommendations",
        example="Excellent prognosis. 5-year cumulative risk for treatment need: 8.4%. 1-year risk <0.1%. These patients have very low likelihood of requiring treatment in the near future. Standard surveillance every 3-6 months is appropriate. Ideal candidates for observation without intervention. Clinical trials for early intervention are generally not indicated."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Low Risk, Intermediate Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the score range",
        example="Score 0 points"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "Excellent prognosis. 5-year cumulative risk for treatment need: 8.4%. 1-year risk <0.1%. These patients have very low likelihood of requiring treatment in the near future. Standard surveillance every 3-6 months is appropriate. Ideal candidates for observation without intervention. Clinical trials for early intervention are generally not indicated.",
                "stage": "Low Risk",
                "stage_description": "Score 0 points"
            }
        }