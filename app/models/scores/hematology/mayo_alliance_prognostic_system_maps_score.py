"""
Mayo Alliance Prognostic System (MAPS) Score Models

Request and response models for MAPS score calculation in systemic mastocytosis prognosis.

References (Vancouver style):
1. Pardanani A, Reichard KK, Zblewski D, Abdelrahman RA, Wassie EA, Koschmann J, et al. 
   Mayo alliance prognostic system for mastocytosis: clinical and hybrid clinical-molecular 
   models. Blood Adv. 2018 Nov 27;2(21):2964-2975. doi: 10.1182/bloodadvances.2018024768.
2. Valent P, Sotlar K, Blatt K, Hartmann K, Reiter A, Sadovnik I, et al. Proposed diagnostic 
   algorithm for patients with suspected mastocytosis: a proposal of the European Competence 
   Network on Mastocytosis. Allergy. 2014 Oct;69(10):1267-74. doi: 10.1111/all.12436.
3. Sperr WR, Kundi M, Alvarez-Twose I, van Anrooij B, Oude Elberink JN, Gorska A, et al. 
   International prognostic scoring system for mastocytosis (IPSM): a retrospective cohort 
   study. Lancet Haematol. 2019 Nov;6(11):e638-e649. doi: 10.1016/S2352-3026(19)30166-8.
4. Arber DA, Orazi A, Hasserjian R, Thiele J, Borowitz MJ, Le Beau MM, et al. The 2016 
   revision to the World Health Organization classification of myeloid neoplasms and acute 
   leukemia. Blood. 2016 May 19;127(20):2391-405. doi: 10.1182/blood-2016-03-643544.

The Mayo Alliance Prognostic System (MAPS) Score is a contemporary risk stratification 
tool for systemic mastocytosis that incorporates both clinical and molecular parameters 
to predict survival outcomes. Developed from analysis of 580 patients at Mayo Clinic, 
this scoring system provides accurate prognostic information to guide treatment decisions 
and patient counseling in systemic mastocytosis management.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class MayoAlliancePrognosticSystemMapsScoreRequest(BaseModel):
    """
    Request model for Mayo Alliance Prognostic System (MAPS) Score
    
    The MAPS Score provides contemporary risk stratification for systemic mastocytosis 
    using five clinical and molecular parameters that directly correlate with survival 
    outcomes.
    
    **Clinical Background:**
    
    Systemic mastocytosis (SM) is a clonal hematopoietic disorder characterized by 
    abnormal accumulation and activation of mast cells in various organs. The disease 
    exhibits significant clinical heterogeneity, ranging from indolent forms with 
    near-normal life expectancy to aggressive variants with poor survival. The MAPS 
    Score was developed to provide objective, evidence-based prognostic assessment 
    beyond traditional WHO morphologic classification.
    
    **Five Key Parameters:**
    
    1. **SM Type (WHO Classification)**:
       - **Indolent SM (ISM)**: Slow progression, good prognosis (0 points)
       - **Smoldering SM (SSM)**: Intermediate behavior, stable course (0 points)
       - **Advanced SM**: Including aggressive SM, SM-AHN, mast cell leukemia (2 points)
    
    2. **Age (>60 years)**:
       - Reflects decreased physiologic reserve and immune function (1 point if >60)
       - Associated with increased treatment complications and comorbidities
       - Important factor for treatment selection and intensity
    
    3. **Platelet Count (<150 ×10⁹/L)**:
       - Thrombocytopenia indicates bone marrow involvement or dysfunction (1 point)
       - May reflect advanced disease with cytopenias
       - Important for treatment safety and bleeding risk assessment
    
    4. **Serum Alkaline Phosphatase (Elevated)**:
       - Elevation suggests liver or bone involvement (1 point)
       - May indicate advanced disease with organ damage
       - Reflects disease burden and organ dysfunction
    
    5. **Adverse Mutations (ASXL1, RUNX1, NRAS)**:
       - Molecular markers associated with poor prognosis (1 point if present)
       - Indicate clonal evolution and genomic instability
       - May predict treatment resistance and disease progression
    
    **Risk Stratification:**
    
    **Low Risk (≤2 points):**
    - Median survival: 198 months (16.5 years)
    - 5-year survival: 99%
    - Excellent prognosis with standard care
    - Monitoring and supportive treatment sufficient
    
    **Intermediate Risk (3-4 points):**
    - Median survival: 36-85 months (3-7 years)
    - 5-year survival: 50-91%
    - Variable prognosis requiring individualized care
    - Consider earlier intervention and closer monitoring
    
    **High Risk (≥5 points):**
    - Median survival: 12 months (1 year)
    - 5-year survival: 4-24%
    - Poor prognosis requiring aggressive treatment
    - Consider clinical trials, targeted therapy, or transplant
    
    **Clinical Applications:**
    
    **Treatment Planning:**
    - Guide timing and intensity of therapeutic interventions
    - Inform decisions about clinical trial enrollment
    - Assist in stem cell transplant evaluation
    - Support palliative care discussions
    
    **Patient Counseling:**
    - Provide evidence-based prognostic information
    - Support shared decision-making processes
    - Guide advance care planning discussions
    - Inform family members about disease trajectory
    
    **Monitoring Strategy:**
    - Determine frequency of follow-up assessments
    - Guide laboratory and imaging surveillance schedules
    - Identify patients requiring specialized care
    - Plan for disease progression monitoring
    
    References (Vancouver style):
    1. Pardanani A, Reichard KK, Zblewski D, Abdelrahman RA, Wassie EA, Koschmann J, et al. 
       Mayo alliance prognostic system for mastocytosis: clinical and hybrid clinical-molecular 
       models. Blood Adv. 2018 Nov 27;2(21):2964-2975. doi: 10.1182/bloodadvances.2018024768.
    2. Valent P, Sotlar K, Blatt K, Hartmann K, Reiter A, Sadovnik I, et al. Proposed diagnostic 
       algorithm for patients with suspected mastocytosis: a proposal of the European Competence 
       Network on Mastocytosis. Allergy. 2014 Oct;69(10):1267-74. doi: 10.1111/all.12436.
    """
    
    sm_type: Literal["indolent_smoldering_sm", "advanced_sm"] = Field(
        ...,
        description="Type of systemic mastocytosis according to WHO classification. Indolent SM (ISM) and smoldering SM (SSM) have better prognosis (0 points) than advanced SM subtypes including aggressive SM, SM with associated hematologic neoplasm, and mast cell leukemia (2 points)",
        example="indolent_smoldering_sm"
    )
    
    patient_age: int = Field(
        ...,
        ge=18,
        le=100,
        description="Patient age in years. Age >60 years (1 point) is associated with worse prognosis due to decreased physiologic reserve, increased comorbidities, and treatment complications. Younger patients typically have better outcomes and treatment tolerance",
        example=55
    )
    
    platelet_count: float = Field(
        ...,
        ge=10,
        le=1000,
        description="Platelet count in ×10⁹/L. Thrombocytopenia <150 ×10⁹/L (1 point) indicates bone marrow involvement, advanced disease, or cytoreductive effects of mastocytosis. Normal or elevated counts suggest preserved bone marrow function",
        example=180
    )
    
    serum_alp: Literal["normal", "elevated"] = Field(
        ...,
        description="Serum alkaline phosphatase level relative to normal range. Elevated ALP (1 point) indicates possible liver involvement, bone disease, or other organ dysfunction in systemic mastocytosis. Normal levels suggest absence of significant organ damage",
        example="normal"
    )
    
    adverse_mutations: Literal["absent", "present"] = Field(
        ...,
        description="Presence of adverse mutations including ASXL1, RUNX1, and NRAS. These mutations (1 point if present) are associated with poor prognosis, clonal evolution, treatment resistance, and disease progression. Molecular testing enhances prognostic accuracy",
        example="absent"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "sm_type": "indolent_smoldering_sm",
                "patient_age": 55,
                "platelet_count": 180,
                "serum_alp": "normal",
                "adverse_mutations": "absent"
            }
        }


class MayoAlliancePrognosticSystemMapsScoreResponse(BaseModel):
    """
    Response model for Mayo Alliance Prognostic System (MAPS) Score
    
    Provides comprehensive prognostic assessment for systemic mastocytosis with 
    survival estimates, risk stratification, and management recommendations.
    
    **Risk Categories and Management:**
    
    **Low Risk (≤2 points):**
    - **Survival**: Median 198 months (16.5 years), 99% 5-year survival
    - **Approach**: Standard monitoring with supportive care
    - **Treatment**: Reserved for symptomatic disease or progression
    - **Monitoring**: Regular blood counts, chemistry panels, symptom assessment
    - **Patient Education**: Disease course understanding, when to seek care
    
    **Intermediate Risk (3-4 points):**
    - **Survival**: Median 36-85 months (3-7 years), 50-91% 5-year survival
    - **Approach**: Closer monitoring with earlier intervention consideration
    - **Treatment**: Consider treatment for symptomatic disease
    - **Monitoring**: Regular laboratory studies, bone marrow assessments, imaging
    - **Specialist Care**: Referral to mastocytosis centers recommended
    
    **High Risk (≥5 points):**
    - **Survival**: Median 12 months (1 year), 4-24% 5-year survival
    - **Approach**: Aggressive treatment and clinical trial consideration
    - **Treatment**: Targeted therapies, cytoreductive treatment, clinical trials
    - **Care Team**: Multidisciplinary care with hematology/oncology
    - **Palliative Care**: Consider early palliative care consultation
    
    **Treatment Considerations by Risk:**
    
    **Therapeutic Options:**
    - **Symptomatic Treatment**: Antihistamines, mast cell stabilizers, epinephrine
    - **Targeted Therapy**: KIT inhibitors (imatinib, dasatinib, midostaurin)
    - **Cytoreductive**: Hydroxyurea, interferon-alpha, cladribine
    - **Investigational**: Clinical trial agents, novel targeted therapies
    - **Transplant**: Allogeneic stem cell transplant in selected patients
    
    **Monitoring Requirements:**
    - **Laboratory**: CBC with differential, comprehensive metabolic panel, LFTs
    - **Biomarkers**: Serum tryptase levels, urinary histamine metabolites
    - **Imaging**: CT or MRI for organ involvement assessment
    - **Bone Marrow**: Morphology, cytogenetics, molecular studies
    - **Functional**: Symptom assessment, quality of life measures
    
    **Quality of Life Considerations:**
    - **Symptom Management**: Flushing, pruritus, gastrointestinal symptoms
    - **Psychological Support**: Coping with chronic disease, prognosis discussions
    - **Social Support**: Family education, support groups, resources
    - **Functional Assessment**: Work capacity, daily activities, exercise tolerance
    - **Advanced Care**: End-of-life planning for high-risk patients
    
    Reference: Pardanani A, et al. Blood Adv. 2018;2(21):2964-2975.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Comprehensive MAPS score assessment including component scores, risk stratification, survival estimates, and detailed management recommendations",
        example={
            "maps_score": 1,
            "component_scores": {
                "sm_type": 0,
                "age": 0,
                "platelets": 0,
                "serum_alp": 0,
                "adverse_mutations": 1
            },
            "component_breakdown": {
                "sm_type": "SM Type (indolent smoldering sm): 0 points",
                "age": "Age (55 years): 0 points",
                "platelets": "Platelets (180 ×10⁹/L): 0 points",
                "serum_alp": "Serum ALP (normal): 0 points",
                "adverse_mutations": "Adverse mutations (present): 1 points"
            },
            "risk_assessment": {
                "risk_category": "Low Risk",
                "median_survival": "198 months (16.5 years)",
                "five_year_survival_rate": "99%",
                "clinical_approach": "Standard monitoring and supportive care",
                "score_range": "1/6 points",
                "prognosis_summary": "Excellent prognosis with prolonged survival expected"
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
        description="Comprehensive clinical interpretation with prognostic assessment, survival estimates, management recommendations, and monitoring guidance",
        example="MAPS score of 1 indicates low risk systemic mastocytosis with excellent prognosis. Median survival is 198 months (16.5 years) with 5-year survival rate approaching 99%. These patients typically have indolent or smoldering disease with minimal adverse features. Standard monitoring and supportive care are usually sufficient, with treatment reserved for symptomatic disease or disease progression."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Intermediate Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the prognosis category",
        example="Excellent prognosis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "maps_score": 1,
                    "component_scores": {
                        "sm_type": 0,
                        "age": 0,
                        "platelets": 0,
                        "serum_alp": 0,
                        "adverse_mutations": 1
                    },
                    "component_breakdown": {
                        "sm_type": "SM Type (indolent smoldering sm): 0 points",
                        "age": "Age (55 years): 0 points",
                        "platelets": "Platelets (180 ×10⁹/L): 0 points",
                        "serum_alp": "Serum ALP (normal): 0 points",
                        "adverse_mutations": "Adverse mutations (present): 1 points"
                    },
                    "risk_assessment": {
                        "risk_category": "Low Risk",
                        "median_survival": "198 months (16.5 years)",
                        "five_year_survival_rate": "99%",
                        "clinical_approach": "Standard monitoring and supportive care",
                        "score_range": "1/6 points",
                        "prognosis_summary": "Excellent prognosis with prolonged survival expected"
                    }
                },
                "unit": "points",
                "interpretation": "MAPS score of 1 indicates low risk systemic mastocytosis with excellent prognosis. Median survival is 198 months (16.5 years) with 5-year survival rate approaching 99%. These patients typically have indolent or smoldering disease with minimal adverse features. Standard monitoring and supportive care are usually sufficient, with treatment reserved for symptomatic disease or disease progression. Regular follow-up with complete blood counts, serum chemistry panels, and symptom assessment is recommended. Patient education about disease course and when to seek medical attention is important for optimal long-term management.",
                "stage": "Low Risk",
                "stage_description": "Excellent prognosis"
            }
        }