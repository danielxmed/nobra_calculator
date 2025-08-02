"""
Menza Score Models

Request and response models for Menza Score calculation.

References (Vancouver style):
1. Menza TW, Hughes JP, Celum CL, Golden MR. Prediction of HIV acquisition among 
   men who have sex with men. Sex Transm Dis. 2009 Sep;36(9):547-55. 
   doi: 10.1097/OLQ.0b013e3181a9cc41.
2. Jones J, Hoenigl M, Siegler AJ, Sullivan PS, Little S, Rosenberg E. Assessing 
   the Performance of 3 Human Immunodeficiency Virus Incidence Risk Scores in a 
   Cohort of Black and White Men Who Have Sex With Men in the South. Sex Transm 
   Dis. 2017 May;44(5):297-302. doi: 10.1097/OLQ.0000000000000596.
3. Luo Q, Dong Y, Chen H, Zeng W, Jiang Y, Chen X, et al. Factors Associated with 
   HIV Infection among Men Who Have Sex with Men: A Systematic Review and 
   Meta-analysis. Arch Sex Behav. 2023 Jul;52(5):2293-2322. 
   doi: 10.1007/s10508-023-02574-x.

The Menza Score is a risk prediction tool that estimates the 4-year probability of 
HIV acquisition among men who have sex with men (MSM). Developed using data from 
sexually transmitted infection (STI) clinics and validated in HIV prevention trials, 
it incorporates key behavioral and clinical risk factors to identify individuals who 
would benefit most from intensified HIV prevention interventions including pre-exposure 
prophylaxis (PrEP).
"""

from pydantic import BaseModel, Field
from typing import Literal


class MenzaScoreRequest(BaseModel):
    """
    Request model for Menza Score HIV risk prediction for MSM
    
    The Menza Score uses four key risk factors to predict 4-year HIV acquisition risk:
    
    Risk Factors and Point Values:
    1. STI History (gonorrhea, chlamydia, or syphilis): 4 points if yes
    2. Methamphetamine or nitrite use (prior 6 months): 11 points if yes
    3. Unprotected anal intercourse with HIV+/unknown partner (prior year): 1 point if yes
    4. 10+ male sexual partners (prior year): 3 points if yes
    
    Score Interpretation:
    - 0 points: <5% 4-year HIV risk
    - 1-3 points: 5-9% 4-year HIV risk
    - 4-11 points: 10-14% 4-year HIV risk
    - ≥12 points: >14% 4-year HIV risk
    
    Clinical Context:
    This score was developed using data from 1,903 MSM attending STI clinics (2001-2008) 
    and validated in 2,081 participants from Project Explore (1999-2003). In the development 
    cohort, annual HIV incidence was 2.57%. The score emphasizes substance use (particularly 
    methamphetamine and nitrites) as the most heavily weighted risk factors.
    
    References (Vancouver style):
    1. Menza TW, Hughes JP, Celum CL, Golden MR. Prediction of HIV acquisition among 
       men who have sex with men. Sex Transm Dis. 2009 Sep;36(9):547-55. 
       doi: 10.1097/OLQ.0b013e3181a9cc41.
    """
    
    sti_history: Literal["yes", "no"] = Field(
        ...,
        description="History of gonorrhea, chlamydia, or syphilis. These bacterial STIs indicate "
                    "sexual network risk and biological vulnerability to HIV through mucosal "
                    "inflammation and disruption. Any history of these infections scores 4 points.",
        example="no"
    )
    
    meth_nitrite_use: Literal["yes", "no"] = Field(
        ...,
        description="Methamphetamine or inhaled nitrite (poppers) use in the prior 6 months. "
                    "These substances are associated with increased sexual risk-taking behaviors, "
                    "prolonged sexual encounters, and impaired judgment. This is the most heavily "
                    "weighted factor at 11 points.",
        example="no"
    )
    
    unprotected_anal_intercourse: Literal["yes", "no"] = Field(
        ...,
        description="Unprotected anal intercourse with HIV-positive or unknown status partner in "
                    "the prior year. This represents direct exposure risk through the highest-risk "
                    "sexual activity for HIV transmission among MSM. Scores 1 point.",
        example="yes"
    )
    
    ten_plus_partners: Literal["yes", "no"] = Field(
        ...,
        description="10 or more male sexual partners in the prior year. Higher partner numbers "
                    "increase cumulative exposure risk and probability of encountering partners "
                    "with undiagnosed or untreated HIV. Scores 3 points.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "sti_history": "no",
                "meth_nitrite_use": "no",
                "unprotected_anal_intercourse": "yes",
                "ten_plus_partners": "no"
            }
        }


class MenzaScoreResponse(BaseModel):
    """
    Response model for Menza Score HIV risk prediction for MSM
    
    The Menza Score provides a 4-year HIV risk estimate to guide prevention interventions.
    Key applications include:
    - Identifying candidates for pre-exposure prophylaxis (PrEP)
    - Targeting intensified HIV prevention counseling
    - Determining HIV testing frequency
    - Resource allocation for prevention programs
    
    Important Limitations:
    - Should only be used for MSM populations
    - Not intended as sole criterion for PrEP eligibility
    - Based on behavioral data from 1999-2003
    - Validation studies showed decreased sensitivity for Black MSM
    - Individual risk may vary based on local HIV epidemiology
    
    Reference: Menza TW, et al. Sex Transm Dis. 2009;36(9):547-55.
    """
    
    result: int = Field(
        ...,
        description="Total Menza Score (range: 0-19 points)",
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including risk level, recommended interventions, "
                    "and prevention strategies based on the score",
        example="Moderate risk for HIV acquisition. Consider discussing pre-exposure prophylaxis "
                "(PrEP) and intensified HIV prevention counseling. Regular HIV testing recommended."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="4-year HIV risk percentage range",
        example="5-9% 4-year HIV risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "Moderate risk for HIV acquisition. Consider discussing "
                                "pre-exposure prophylaxis (PrEP) and intensified HIV prevention "
                                "counseling. Regular HIV testing recommended.",
                "stage": "Moderate Risk",
                "stage_description": "5-9% 4-year HIV risk"
            }
        }