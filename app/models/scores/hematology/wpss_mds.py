"""
WPSS (WHO classification-based Prognostic Scoring System) for Myelodysplastic Syndrome Models

Request and response models for WPSS calculation for MDS prognosis.

References (Vancouver style):
1. Malcovati L, Germing U, Kuendgen A, et al. Time-dependent prognostic scoring system 
   for predicting survival and leukemic evolution in myelodysplastic syndromes. 
   J Clin Oncol. 2007;25(23):3503-3510. doi: 10.1200/JCO.2006.08.5696
2. Malcovati L, Della Porta MG, Strupp C, et al. Impact of the degree of anemia on the 
   outcome of patients with myelodysplastic syndrome and its integration into the WHO 
   classification-based Prognostic Scoring System (WPSS). Haematologica. 2011;96(10):1433-1440. 
   doi: 10.3324/haematol.2011.044602
3. Della Porta MG, Tuechler H, Malcovati L, et al. Validation of WHO classification-based 
   Prognostic Scoring System (WPSS) for myelodysplastic syndromes and comparison with the 
   revised International Prognostic Scoring System (IPSS-R). Leukemia. 2015;29(7):1502-1513. 
   doi: 10.1038/leu.2015.55

The WPSS is a time-dependent prognostic scoring system that combines WHO morphological 
classification, cytogenetics, and transfusion requirement to assess prognosis in 
myelodysplastic syndrome. Unlike the original IPSS, WPSS can be applied throughout 
the disease course and provides dynamic prognostic assessment.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any, List


class WpssMdsRequest(BaseModel):
    """
    Request model for WPSS (WHO classification-based Prognostic Scoring System) for MDS
    
    The WPSS evaluates prognosis in myelodysplastic syndrome using three key parameters:
    
    **SCORING COMPONENTS:**
    
    1. **WHO Morphological Category (0-3 points):**
       - 0 points: RA, RARS, or MDS with isolated del(5q)
       - 1 point: RCMD (Refractory Cytopenia with Multilineage Dysplasia)
       - 2 points: RAEB-1 (Refractory Anemia with Excess Blasts-1, 2-4% blasts)
       - 3 points: RAEB-2 (Refractory Anemia with Excess Blasts-2, 5-19% blasts)
    
    2. **Cytogenetic Risk Category (0-2 points):**
       - 0 points: Good (normal, -Y, del(5q), del(20q))
       - 1 point: Intermediate (all other abnormalities)
       - 2 points: Poor (complex ≥3 abnormalities, chromosome 7 anomalies)
    
    3. **Transfusion Requirement (0-1 points):**
       - 0 points: None (no regular transfusion requirement)
       - 1 point: Regular (≥1 RBC transfusion every 8 weeks over 4 months)
    
    **RISK STRATIFICATION:**
    
    Total Score 0-6 points stratifies patients into five risk groups:
    - 0 points: Very Low Risk (median survival 141 months)
    - 1 point: Low Risk (median survival 66 months)
    - 2 points: Intermediate Risk (median survival 48 months)
    - 3-4 points: High Risk (median survival 26 months)
    - 5-6 points: Very High Risk (median survival 9 months)
    
    **CLINICAL APPLICATIONS:**
    
    Prognostic Assessment:
    - Estimates overall survival probability
    - Predicts risk of leukemic transformation
    - Guides treatment decision-making
    - Monitors disease progression over time
    
    Treatment Planning:
    - Low risk: Watch and wait, supportive care
    - Intermediate risk: Consider early intervention
    - High risk: Intensive treatment, transplant evaluation
    
    **WHO MORPHOLOGICAL CATEGORIES:**
    
    RA (Refractory Anemia):
    - <5% blasts in bone marrow, <1% in peripheral blood
    - Unilineage dysplasia (erythroid only)
    - No ring sideroblasts or <15% of erythroid precursors
    
    RARS (Refractory Anemia with Ring Sideroblasts):
    - <5% blasts in bone marrow, <1% in peripheral blood
    - ≥15% ring sideroblasts of erythroid precursors
    - Unilineage dysplasia (erythroid only)
    
    MDS with isolated del(5q):
    - <5% blasts in bone marrow, <1% in peripheral blood
    - Isolated del(5q) cytogenetic abnormality
    - No Auer rods
    
    RCMD (Refractory Cytopenia with Multilineage Dysplasia):
    - <5% blasts in bone marrow, <1% in peripheral blood
    - Dysplasia in ≥10% of cells in 2 or more myeloid lineages
    - <15% ring sideroblasts
    
    RAEB-1 (Refractory Anemia with Excess Blasts-1):
    - 2-4% blasts in peripheral blood, 5-9% blasts in bone marrow
    - No Auer rods
    - Unilineage or multilineage dysplasia
    
    RAEB-2 (Refractory Anemia with Excess Blasts-2):
    - 5-19% blasts in peripheral blood, 10-19% blasts in bone marrow
    - Auer rods may be present
    - Unilineage or multilineage dysplasia
    
    **CYTOGENETIC RISK CATEGORIES:**
    
    Good Risk Cytogenetics:
    - Normal karyotype
    - Isolated -Y (loss of Y chromosome)
    - Isolated del(5q) (deletion 5q)
    - Isolated del(20q) (deletion 20q)
    
    Intermediate Risk Cytogenetics:
    - All other single or double abnormalities
    - +8 (trisomy 8)
    - +19 (trisomy 19)
    - i(17q) (isochromosome 17q)
    - Other single chromosome abnormalities
    
    Poor Risk Cytogenetics:
    - Complex karyotype (≥3 abnormalities)
    - Chromosome 7 abnormalities (-7, del(7q))
    - inv(3), t(3;3), del(3q)
    - Double including -7/del(7q)
    
    **ADVANTAGES OF WPSS:**
    
    Dynamic Assessment:
    - Can be calculated at any time during disease course
    - Not limited to diagnosis like original IPSS
    - Reflects disease evolution and treatment effects
    
    Clinical Validation:
    - Extensively validated in multiple cohorts
    - Superior prognostic accuracy compared to IPSS
    - Correlates with quality of life measures
    
    Treatment Guidance:
    - Helps select appropriate therapeutic strategies
    - Guides timing of interventions
    - Assists in transplant decision-making
    
    References (Vancouver style):
    1. Malcovati L, Germing U, Kuendgen A, et al. Time-dependent prognostic scoring system 
    for predicting survival and leukemic evolution in myelodysplastic syndromes. 
    J Clin Oncol. 2007;25(23):3503-3510. doi: 10.1200/JCO.2006.08.5696
    2. Malcovati L, Della Porta MG, Strupp C, et al. Impact of the degree of anemia on the 
    outcome of patients with myelodysplastic syndrome and its integration into the WHO 
    classification-based Prognostic Scoring System (WPSS). Haematologica. 2011;96(10):1433-1440.
    """
    
    who_category: Literal["ra_rars_del5q", "rcmd_rcmd_rs", "raeb_1", "raeb_2"] = Field(
        ...,
        description="WHO morphological classification of myelodysplastic syndrome. ra_rars_del5q: RA/RARS/isolated del(5q) (0 pts); rcmd_rcmd_rs: RCMD/RCMD-RS (1 pt); raeb_1: RAEB-1 with 2-4% blasts (2 pts); raeb_2: RAEB-2 with 5-19% blasts (3 pts)",
        example="rcmd_rcmd_rs"
    )
    
    karyotype: Literal["good", "intermediate", "poor"] = Field(
        ...,
        description="Cytogenetic risk category based on karyotype analysis. good: normal, -Y, del(5q), del(20q) (0 pts); intermediate: all other abnormalities (1 pt); poor: complex ≥3 abnormalities, chromosome 7 anomalies (2 pts)",
        example="good"
    )
    
    transfusion_requirement: Literal["none", "regular"] = Field(
        ...,
        description="Regular red blood cell transfusion requirement. none: no regular transfusion requirement (0 pts); regular: ≥1 RBC transfusion every 8 weeks over 4 months (1 pt)",
        example="none"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "who_category": "rcmd_rcmd_rs",
                "karyotype": "good",
                "transfusion_requirement": "none"
            }
        }


class WpssMdsResponse(BaseModel):
    """
    Response model for WPSS (WHO classification-based Prognostic Scoring System) for MDS
    
    The WPSS provides comprehensive prognostic assessment for myelodysplastic syndrome 
    patients. Results include total score, risk stratification, survival estimates, 
    and clinical management recommendations.
    
    **RISK CATEGORIES AND OUTCOMES:**
    
    Very Low Risk (0 points):
    - Median overall survival: 141 months (11.8 years)
    - Very low probability of leukemic transformation
    - Excellent prognosis with routine monitoring
    
    Low Risk (1 point):
    - Median overall survival: 66 months (5.5 years)
    - Low probability of leukemic transformation
    - Good prognosis with regular monitoring and supportive care
    
    Intermediate Risk (2 points):
    - Median overall survival: 48 months (4 years)
    - Moderate probability of leukemic transformation
    - Consider early therapeutic intervention
    
    High Risk (3-4 points):
    - Median overall survival: 26 months (2.2 years)
    - High probability of leukemic transformation
    - Intensive treatment strategies recommended
    
    Very High Risk (5-6 points):
    - Median overall survival: 9 months
    - Very high probability of leukemic transformation
    - Urgent consideration for intensive treatment
    
    **CLINICAL MANAGEMENT IMPLICATIONS:**
    
    Low Risk Management:
    - Watch and wait approach with regular monitoring
    - Supportive care for symptomatic anemia
    - ESAs (erythropoiesis-stimulating agents) consideration
    - Quality of life optimization
    
    Intermediate Risk Management:
    - Close monitoring with consideration for early intervention
    - Hypomethylating agents evaluation
    - Clinical trial participation
    - Support care optimization
    
    High Risk Management:
    - Urgent hematology-oncology consultation
    - Intensive treatment strategies
    - Allogeneic stem cell transplantation evaluation
    - Aggressive supportive care
    
    **PROGNOSTIC FACTORS:**
    
    Survival Predictors:
    - WHO morphological subtype (blast percentage)
    - Cytogenetic abnormalities (complexity and specific anomalies)
    - Transfusion dependency (iron overload, quality of life)
    
    Leukemic Transformation Risk:
    - Higher blast percentage increases risk
    - Poor cytogenetics accelerate transformation
    - Complex karyotype associated with rapid progression
    
    Reference: Malcovati L, et al. J Clin Oncol. 2007;25(23):3503-3510.
    """
    
    result: int = Field(
        ...,
        description="WPSS total score ranging from 0-6 points",
        ge=0,
        le=6,
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk category, survival estimate, and prognosis",
        example="WPSS score 1 point indicates Low Risk myelodysplastic syndrome with median overall survival of 66 months (5.5 years). Good prognosis."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification based on total score",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Good prognosis"
    )
    
    median_survival_months: int = Field(
        ...,
        description="Median overall survival in months for this risk category",
        example=66
    )
    
    median_survival_years: float = Field(
        ...,
        description="Median overall survival in years for this risk category",
        example=5.5
    )
    
    component_scores: Dict[str, int] = Field(
        ...,
        description="Breakdown of individual component scores contributing to total WPSS score",
        example={
            "who_category_score": 1,
            "karyotype_score": 0,
            "transfusion_score": 0
        }
    )
    
    risk_assessment: Dict[str, Any] = Field(
        ...,
        description="Detailed risk assessment including leukemic transformation risk and management urgency",
        example={
            "risk_category": "Low Risk",
            "median_survival": "66 months (5.5 years)",
            "leukemic_transformation_risk": "Low probability of leukemic transformation",
            "management_urgency": "Regular monitoring with supportive care",
            "prognosis": "Good prognosis"
        }
    )
    
    clinical_recommendations: Dict[str, Any] = Field(
        ...,
        description="Comprehensive clinical management recommendations based on risk stratification",
        example={
            "general_recommendations": [
                "Watch and wait approach with regular monitoring",
                "Supportive care for symptomatic anemia",
                "Monitor for disease progression",
                "Quality of life optimization"
            ],
            "monitoring_schedule": [
                "Complete blood count every 3-6 months",
                "Bone marrow assessment annually or if clinical change",
                "Iron overload monitoring if transfusion dependent"
            ],
            "treatment_considerations": [
                "ESAs (erythropoiesis-stimulating agents) for anemia",
                "Iron chelation if transfusion dependent",
                "Clinical trial participation"
            ],
            "follow_up": "WPSS can be recalculated throughout disease course as clinical parameters change"
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "WPSS score 1 point indicates Low Risk myelodysplastic syndrome with median overall survival of 66 months (5.5 years). Good prognosis.",
                "stage": "Low Risk",
                "stage_description": "Good prognosis",
                "median_survival_months": 66,
                "median_survival_years": 5.5,
                "component_scores": {
                    "who_category_score": 1,
                    "karyotype_score": 0,
                    "transfusion_score": 0
                },
                "risk_assessment": {
                    "risk_category": "Low Risk",
                    "median_survival": "66 months (5.5 years)",
                    "leukemic_transformation_risk": "Low probability of leukemic transformation",
                    "management_urgency": "Regular monitoring with supportive care",
                    "prognosis": "Good prognosis"
                },
                "clinical_recommendations": {
                    "general_recommendations": [
                        "Watch and wait approach with regular monitoring",
                        "Supportive care for symptomatic anemia",
                        "Monitor for disease progression",
                        "Quality of life optimization"
                    ],
                    "monitoring_schedule": [
                        "Complete blood count every 3-6 months",
                        "Bone marrow assessment annually or if clinical change",
                        "Iron overload monitoring if transfusion dependent"
                    ],
                    "treatment_considerations": [
                        "ESAs (erythropoiesis-stimulating agents) for anemia",
                        "Iron chelation if transfusion dependent",
                        "Clinical trial participation"
                    ],
                    "follow_up": "WPSS can be recalculated throughout disease course as clinical parameters change"
                }
            }
        }