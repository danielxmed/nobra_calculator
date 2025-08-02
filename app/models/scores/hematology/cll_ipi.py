"""
International Prognostic Index for Chronic Lymphocytic Leukemia (CLL-IPI) Models

Request and response models for CLL-IPI calculation.

References (Vancouver style):
1. An international prognostic index for patients with chronic lymphocytic leukaemia 
   (CLL-IPI): a meta-analysis of individual patient data. Lancet Oncol. 2016 Jul;17(7):779-90. 
   doi: 10.1016/S1470-2045(16)30029-8.
2. Condoluci A, Terzi di Bergamo L, Langerbeins P, et al. International prognostic score 
   for asymptomatic early-stage chronic lymphocytic leukemia. Blood. 2020 May 28;135(22):1859-1869. 
   doi: 10.1182/blood.2019003453.
3. Gentile M, Shanafelt TD, Rossi D, et al. Validation of the CLL-IPI and comparison with 
   the MDACC prognostic index in newly diagnosed patients. Blood. 2016 Oct 13;128(15):2093-2095. 
   doi: 10.1182/blood-2016-07-728261.

The CLL-IPI combines genetic (TP53 status, IGHV mutational status), biochemical 
(β2-microglobulin), and clinical parameters (age, clinical stage) to stratify CLL 
patients into four risk categories with significantly different overall survival rates. 
This validated prognostic model enables targeted patient management and treatment 
selection in chronic lymphocytic leukemia.
"""

from pydantic import BaseModel, Field
from typing import Literal


class CllIpiRequest(BaseModel):
    """
    Request model for International Prognostic Index for Chronic Lymphocytic Leukemia (CLL-IPI)
    
    The CLL-IPI uses five independent prognostic factors to predict overall survival in CLL:
    
    Genetic Factors:
    - TP53 status: Presence of del(17p) and/or TP53 mutation (4 points if abnormal)
    - IGHV mutational status: Immunoglobulin heavy chain variable region mutations (2 points if unmutated)
    
    Biochemical Factor:
    - β2-microglobulin: Serum level reflecting tumor burden (2 points if >3.5 mg/L)
    
    Clinical Factors:
    - Clinical stage: Binet or Rai staging system (1 point if advanced)
    - Age: Patient age at diagnosis (1 point if >65 years)
    
    Scoring System:
    - TP53 abnormal: 4 points (highest weight due to poor prognosis)
    - IGHV unmutated: 2 points (associated with aggressive disease)
    - β2-microglobulin elevated: 2 points (reflects tumor burden)
    - Advanced clinical stage: 1 point (higher disease burden)
    - Age >65 years: 1 point (decreased tolerance to treatment)
    
    Risk Categories (Total Score 0-10):
    - Low Risk (0-1): 5-year OS 93.2%
    - Intermediate Risk (2-3): 5-year OS 79.3%
    - High Risk (4-6): 5-year OS 63.3%
    - Very High Risk (7-10): 5-year OS 23.3%
    
    Clinical Applications:
    - Risk stratification for treatment planning
    - Patient counseling about prognosis
    - Clinical trial stratification
    - Guiding intensity of monitoring and treatment
    
    Important Notes:
    - Use for risk stratification, not treatment initiation decisions
    - Treatment should be based on iwCLL criteria
    - Genetic testing for TP53 and IGHV recommended before first treatment
    - Regular reassessment may be needed as disease evolves
    
    References (Vancouver style):
    1. An international prognostic index for patients with chronic lymphocytic leukaemia 
       (CLL-IPI): a meta-analysis of individual patient data. Lancet Oncol. 2016;17(7):779-90.
    2. Condoluci A, Terzi di Bergamo L, Langerbeins P, et al. International prognostic score 
       for asymptomatic early-stage chronic lymphocytic leukemia. Blood. 2020;135(22):1859-1869.
    3. Gentile M, Shanafelt TD, Rossi D, et al. Validation of the CLL-IPI and comparison with 
       the MDACC prognostic index in newly diagnosed patients. Blood. 2016;128(15):2093-2095.
    """
    
    tp53_status: Literal["normal", "abnormal"] = Field(
        ...,
        description="TP53 gene status including del(17p) and/or TP53 mutation. Normal = no abnormalities detected (0 points). Abnormal = del(17p) and/or TP53 mutation present (4 points - highest risk factor)",
        example="normal"
    )
    
    ighv_status: Literal["mutated", "unmutated"] = Field(
        ...,
        description="IGHV (immunoglobulin heavy chain variable) mutational status. Mutated = <98% homology to germline sequence, favorable prognosis (0 points). Unmutated = ≥98% homology to germline sequence, unfavorable prognosis (2 points)",
        example="mutated"
    )
    
    beta2_microglobulin: Literal["normal", "elevated"] = Field(
        ...,
        description="Serum β2-microglobulin concentration level reflecting tumor burden and kidney function. Normal = ≤3.5 mg/L (0 points). Elevated = >3.5 mg/L (2 points). Some laboratories use 3.0 mg/L cutoff",
        example="normal"
    )
    
    clinical_stage: Literal["early", "advanced"] = Field(
        ...,
        description="Clinical stage based on Binet or Rai staging systems. Early = Binet A or Rai 0 (limited disease, 0 points). Advanced = Binet B-C or Rai I-IV (more extensive disease, 1 point)",
        example="early"
    )
    
    age: Literal["65_or_younger", "older_than_65"] = Field(
        ...,
        description="Patient age category at diagnosis. 65 or younger = ≤65 years (0 points). Older than 65 = >65 years (1 point). Age affects treatment tolerance and outcomes",
        example="65_or_younger"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "tp53_status": "normal",
                "ighv_status": "mutated",
                "beta2_microglobulin": "normal",
                "clinical_stage": "early",
                "age": "65_or_younger"
            }
        }


class CllIpiResponse(BaseModel):
    """
    Response model for International Prognostic Index for Chronic Lymphocytic Leukemia (CLL-IPI)
    
    Returns the CLL-IPI score with risk stratification and survival predictions:
    
    Risk Categories and 5-Year Overall Survival:
    - Low Risk (0-1 points): 93.2% (95% CI 90.5-96.0%)
    - Intermediate Risk (2-3 points): 79.3% (95% CI 75.5-83.2%)
    - High Risk (4-6 points): 63.3% (95% CI 57.9-68.8%)
    - Very High Risk (7-10 points): 23.3% (95% CI 12.5-34.1%)
    
    Clinical Implications by Risk Group:
    
    Low Risk:
    - Excellent prognosis with prolonged survival expected
    - Watchful waiting appropriate for asymptomatic patients
    - Lower intensity treatments when therapy indicated
    - Standard monitoring intervals sufficient
    
    Intermediate Risk:
    - Good prognosis with moderate survival expectations
    - Standard treatment approaches appropriate
    - Consider patient preferences and comorbidities
    - Regular monitoring with standard intervals
    
    High Risk:
    - Unfavorable prognosis requiring closer monitoring
    - Consider more intensive treatment approaches
    - Clinical trial enrollment recommended
    - Earlier intervention may be beneficial
    
    Very High Risk:
    - Poor prognosis requiring aggressive management
    - Strong consideration for clinical trials
    - Novel targeted therapies preferred
    - Intensive treatment regimens and close monitoring
    - Supportive care measures essential
    
    The CLL-IPI has been validated across multiple studies and geographic regions, 
    maintaining prognostic relevance in the era of targeted therapies. It enables 
    personalized treatment approaches and improves patient counseling about prognosis.
    
    Reference: An international prognostic index for patients with chronic lymphocytic 
    leukaemia (CLL-IPI). Lancet Oncol. 2016;17(7):779-90.
    """
    
    result: int = Field(
        ...,
        description="CLL-IPI score calculated from five prognostic factors (range 0-10 points)",
        example=0,
        ge=0,
        le=10
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the CLL-IPI score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with prognosis and management recommendations based on risk category",
        example="Excellent prognosis with 5-year overall survival of 93.2% (95% CI 90.5-96.0%). These patients have favorable genetic and clinical characteristics with prolonged survival expected. Consider watchful waiting approach for asymptomatic patients. Lower intensity treatments may be appropriate when therapy is indicated."
    )
    
    stage: str = Field(
        ...,
        description="CLL-IPI risk category (Low Risk, Intermediate Risk, High Risk, Very High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the score range for this risk category",
        example="Score 0 points (0-1 points)"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0,
                "unit": "points", 
                "interpretation": "Excellent prognosis with 5-year overall survival of 93.2% (95% CI 90.5-96.0%). These patients have favorable genetic and clinical characteristics with prolonged survival expected. Consider watchful waiting approach for asymptomatic patients. Lower intensity treatments may be appropriate when therapy is indicated.",
                "stage": "Low Risk",
                "stage_description": "Score 0 points (0-1 points)"
            }
        }