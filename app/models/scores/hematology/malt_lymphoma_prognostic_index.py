"""
MALT Lymphoma Prognostic Index (MALT-IPI) Models

Request and response models for MALT-IPI calculation.

References (Vancouver style):
1. Thieblemont C, Cascione L, Conconi A, Kiesewetter B, Raderer M, Gaidano G, et al. 
   A MALT lymphoma prognostic index. Blood. 2017 Sep 21;130(12):1409-1417. 
   doi: 10.1182/blood-2017-03-771915.
2. Hong J, Lee Y, Park J, Kim SJ, Lim ST, Kim JS, et al. Validation of the MALT-lymphoma 
   international prognostic index (MALT-IPI) and extension of the prognostic model with 
   the addition of β2-microglobulin. Ann Hematol. 2019 Nov;98(11):2499-2507. 
   doi: 10.1007/s00277-019-03808-x.
3. Zucca E, Conconi A, Martinelli G, Bouabdallah R, Tucci A, Vitolo U, et al. Final Results 
   of the IELSG-19 Randomized Trial of Mucosa-Associated Lymphoid Tissue Lymphoma: Improved 
   Event-Free and Progression-Free Survival With Rituximab Plus Chlorambucil Versus Either 
   Agent Alone. J Clin Oncol. 2017 Jun 10;35(17):1905-1912. doi: 10.1200/JCO.2016.70.6994.

The MALT Lymphoma Prognostic Index (MALT-IPI) is a validated prognostic tool that identifies 
MALT lymphoma patients at risk for poor outcomes. It uses three simple clinical parameters: 
age ≥70 years, Ann Arbor stage III/IV, and elevated lactate dehydrogenase (LDH) level. The 
index stratifies patients into three risk groups (low, intermediate, high) predictive for 
event-free survival and overall survival. Developed using 401 patients from the IELSG-19 
randomized trial and validated in independent cohort (N=633).
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class MaltLymphomaPrognosticIndexRequest(BaseModel):
    """
    Request model for MALT Lymphoma Prognostic Index (MALT-IPI)
    
    The MALT-IPI is a simple, accessible prognostic tool that uses three clinical parameters
    to stratify MALT lymphoma patients into risk groups:
    
    1. Age:
       - <70 years: 0 points
       - ≥70 years: 1 point (HR 1.72, 95% CI 1.26-2.33)
    
    2. Lactate Dehydrogenase (LDH) Level:
       - Normal: 0 points
       - Elevated (above upper limit of normal): 1 point (HR 1.87, 95% CI 1.27-2.77)
    
    3. Ann Arbor Stage:
       - Stage I or II: 0 points
       - Stage III or IV: 1 point (HR 1.79, 95% CI 1.35-2.38)
    
    Risk Stratification:
    - 0 points: Low Risk (excellent prognosis)
    - 1 point: Intermediate Risk (moderate prognosis)
    - ≥2 points: High Risk (poor prognosis requiring aggressive treatment)
    
    Clinical Applications:
    - Prognostic assessment for newly diagnosed MALT lymphoma patients
    - Treatment planning and intensity decisions
    - Patient counseling regarding prognosis and outcomes
    - Clinical trial stratification
    - Follow-up monitoring frequency determination
    
    Validation:
    - Applicable to both gastric and non-gastric MALT lymphoma
    - Prognostic utility retained across different treatment regimens
    - Validated in multiple independent cohorts
    - Significantly discriminates progression-free, overall, and cause-specific survival
    
    References (Vancouver style):
    1. Thieblemont C, Cascione L, Conconi A, Kiesewetter B, Raderer M, Gaidano G, et al. 
       A MALT lymphoma prognostic index. Blood. 2017 Sep 21;130(12):1409-1417. 
       doi: 10.1182/blood-2017-03-771915.
    2. Hong J, Lee Y, Park J, Kim SJ, Lim ST, Kim JS, et al. Validation of the MALT-lymphoma 
       international prognostic index (MALT-IPI) and extension of the prognostic model with 
       the addition of β2-microglobulin. Ann Hematol. 2019 Nov;98(11):2499-2507. 
       doi: 10.1007/s00277-019-03808-x.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in years. Age ≥70 years is associated with worse prognosis and scores 1 point (HR 1.72, 95% CI 1.26-2.33)",
        example=65
    )
    
    ldh_level: Literal["normal", "elevated"] = Field(
        ...,
        description="Serum lactate dehydrogenase (LDH) level relative to institutional upper limit of normal. Elevated LDH scores 1 point and is associated with worse prognosis (HR 1.87, 95% CI 1.27-2.77)",
        example="normal"
    )
    
    ann_arbor_stage: Literal["I", "II", "III", "IV"] = Field(
        ...,
        description="Ann Arbor staging system for lymphomas. Stage III or IV disease scores 1 point and is associated with worse prognosis (HR 1.79, 95% CI 1.35-2.38). Stage I/II limited disease, Stage III/IV advanced disease",
        example="II"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "ldh_level": "normal",
                "ann_arbor_stage": "II"
            }
        }


class MaltLymphomaPrognosticIndexResponse(BaseModel):
    """
    Response model for MALT Lymphoma Prognostic Index (MALT-IPI)
    
    The MALT-IPI stratifies patients into three distinct risk groups with different prognoses:
    
    Low Risk (0 points):
    - 5-year overall survival: 96.7%
    - 5-year event-free survival: 76.0%
    - 5-year cause-specific survival: 98.2%
    - 5-year progression-free survival: 56.8%
    - Management: Conservative approaches, watchful waiting may be appropriate
    
    Intermediate Risk (1 point):
    - 5-year overall survival: 81.7%
    - 5-year event-free survival: 48.4%
    - 5-year cause-specific survival: 94.7%
    - 5-year progression-free survival: 48.0%
    - Management: Intensive monitoring, consider early intervention
    
    High Risk (≥2 points):
    - 5-year overall survival: 64.9%
    - 5-year event-free survival: 15.7%
    - 5-year cause-specific survival: 74.3%
    - 5-year progression-free survival: 22.7%
    - Management: Aggressive treatment approaches strongly recommended
    
    The MALT-IPI provides evidence-based risk stratification to guide treatment decisions,
    patient counseling, and monitoring strategies for MALT lymphoma patients.
    
    Reference: Thieblemont C, et al. Blood. 2017;130(12):1409-1417.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="MALT-IPI assessment results including total score, component scores, risk categories, and detailed survival outcomes",
        example={
            "total_score": 0,
            "age_score": 0,
            "ldh_score": 0,
            "stage_score": 0,
            "age_category": "Age <70 years: 65",
            "ldh_category": "LDH normal",
            "stage_category": "Ann Arbor stage II",
            "survival_outcomes": {
                "event_free_survival_5yr": "76.0%",
                "progression_free_survival_5yr": "56.8%",
                "cause_specific_survival_5yr": "98.2%",
                "overall_survival_5yr": "96.7%"
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with risk stratification, prognosis, survival outcomes, and treatment recommendations",
        example="Low risk MALT lymphoma with excellent prognosis. 5-year survival outcomes: overall survival 96.7%, event-free survival 76.0%, cause-specific survival 98.2%, and progression-free survival 56.8%. Conservative management approaches may be considered including watchful waiting or minimal intervention."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification category (Low Risk, Intermediate Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level and prognosis",
        example="Low risk of poor outcomes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "total_score": 0,
                    "age_score": 0,
                    "ldh_score": 0,
                    "stage_score": 0,
                    "age_category": "Age <70 years: 65",
                    "ldh_category": "LDH normal",
                    "stage_category": "Ann Arbor stage II",
                    "survival_outcomes": {
                        "event_free_survival_5yr": "76.0%",
                        "progression_free_survival_5yr": "56.8%",
                        "cause_specific_survival_5yr": "98.2%",
                        "overall_survival_5yr": "96.7%"
                    }
                },
                "unit": "points",
                "interpretation": "Low risk MALT lymphoma with excellent prognosis. 5-year survival outcomes: overall survival 96.7%, event-free survival 76.0%, cause-specific survival 98.2%, and progression-free survival 56.8%. Conservative management approaches may be considered including watchful waiting or minimal intervention.",
                "stage": "Low Risk",
                "stage_description": "Low risk of poor outcomes"
            }
        }