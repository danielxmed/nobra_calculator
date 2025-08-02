"""
Mutation-Enhanced International Prognostic Score System (MIPSS70/MIPSS70+) Models

Request and response models for MIPSS70/MIPSS70+ calculation.

References (Vancouver style):
1. Guglielmelli P, Lasho TL, Rotunno G, Mudireddy M, Mannarelli C, Nicolosi M, et al. 
   MIPSS70: Mutation-Enhanced International Prognostic Score System for transplantation-age 
   patients with primary myelofibrosis. J Clin Oncol. 2018;36(4):310-318. 
   doi: 10.1200/JCO.2017.76.4886.
2. Tefferi A, Guglielmelli P, Lasho TL, Rotunno G, Finke C, Mannarelli C, et al. 
   MIPSS70+ Version 2.0: Mutation and Karyotype-Enhanced International Prognostic 
   Scoring System for Primary Myelofibrosis. J Clin Oncol. 2018;36(17):1769-1770. 
   doi: 10.1200/JCO.2018.78.9867.
3. Passamonti F, Cervantes F, Vannucchi AM, Morra E, Rumi E, Pereira A, et al. 
   A dynamic prognostic model to predict survival in primary myelofibrosis: a study 
   by the IWG-MRT (International Working Group for Myeloproliferative Neoplasms 
   Research and Treatment). Blood. 2010;115(9):1703-8. doi: 10.1182/blood-2009-09-245837.

The MIPSS70/MIPSS70+ scoring system is specifically designed for transplantation-age 
patients (≤70 years) with primary myelofibrosis, incorporating molecular genetic 
information to improve prognostic accuracy beyond traditional clinical factors.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class Mipss70Request(BaseModel):
    """
    Request model for Mutation-Enhanced International Prognostic Score System (MIPSS70/MIPSS70+)
    
    The MIPSS70/MIPSS70+ scoring system represents a significant advancement in prognostic 
    assessment for patients with primary myelofibrosis (PMF), specifically designed for 
    transplantation-age patients (≤70 years). This system integrates traditional clinical 
    and laboratory parameters with molecular genetic information to provide superior 
    prognostic accuracy compared to earlier scoring systems.
    
    Clinical Parameters (Traditional Risk Factors):
    
    Age (0-2 points):
    - Age >65 years: 2 points
    - Age ≤65 years: 0 points
    - Older age is consistently associated with worse prognosis in myelofibrosis
    - Age threshold reflects increased treatment-related mortality and reduced tolerance
    
    Hemoglobin Level (0-1 point):
    - Hemoglobin <10 g/dL: 1 point
    - Hemoglobin ≥10 g/dL: 0 points
    - Anemia reflects disease burden and bone marrow failure
    - Independent predictor of survival and quality of life
    
    White Blood Cell Count (0-2 points):
    - WBC >25×10⁹/L: 2 points
    - WBC ≤25×10⁹/L: 0 points
    - Extreme leukocytosis indicates aggressive disease biology
    - Associated with increased risk of leukemic transformation
    
    Platelet Count (0-2 points):
    - Platelets <100×10⁹/L: 2 points
    - Platelets ≥100×10⁹/L: 0 points
    - Thrombocytopenia indicates advanced bone marrow failure
    - Strong predictor of bleeding complications and poor survival
    
    Circulating Blasts (0-1 point):
    - Blasts >2%: 1 point
    - Blasts ≤2%: 0 points
    - Peripheral blast count reflects disease progression toward acute leukemia
    - Early indicator of accelerated phase transformation
    
    Constitutional Symptoms (0-1 point):
    - Present: 1 point (weight loss >10% in 6 months, night sweats, fever)
    - Absent: 0 points
    - Reflects cytokine-mediated systemic inflammation
    - Associated with reduced quality of life and survival
    
    Molecular Parameters (Enhanced Risk Stratification):
    
    High Molecular Risk Mutations (0-1 point):
    - Present: 1 point
    - Absent: 0 points
    - Includes: ASXL1, EZH2, SRSF2, IDH1, IDH2 mutations
    - These mutations independently predict poor survival
    - Essential for accurate risk stratification in modern era
    
    Very High Molecular Risk (MIPSS70+ Only) (0-1 point):
    - Present: 1 point (≥2 high-risk mutations or specific high-risk patterns)
    - Absent: 0 points
    - Represents the highest molecular risk category
    - Associated with very poor prognosis and urgent transplant consideration
    
    Risk Categories and Clinical Implications:
    
    Low Risk (0-2 points):
    - Median survival >20 years
    - Excellent prognosis with conservative management approach
    - Standard monitoring every 3-6 months sufficient
    - Allogeneic transplantation not indicated due to excellent survival
    - JAK inhibitors only for symptomatic disease
    - Focus on quality of life and symptom management
    
    Intermediate-1 Risk (3-4 points):
    - Median survival 8-20 years
    - Good prognosis with selective treatment interventions
    - Regular monitoring every 2-4 months recommended
    - JAK inhibitor therapy for symptomatic splenomegaly or constitutional symptoms
    - Transplantation generally deferred unless disease progression
    - Long-term disease management strategy appropriate
    
    Intermediate-2 Risk (5-6 points):
    - Median survival 4-8 years
    - Intermediate prognosis requiring active treatment consideration
    - Close monitoring every 1-3 months with comprehensive assessments
    - JAK inhibitor therapy recommended for symptom control
    - Allogeneic transplantation evaluation strongly recommended
    - Timing of transplant referral is critical for optimal outcomes
    
    High Risk (≥7 points):
    - Median survival <4 years
    - Poor prognosis requiring urgent intervention
    - Intensive monitoring and aggressive treatment approach
    - Immediate allogeneic transplantation evaluation and referral
    - Consider experimental therapies and clinical trials
    - Palliative care consultation for advanced disease management
    
    Clinical Decision Making and Treatment Planning:
    
    Transplantation Considerations:
    - MIPSS70 specifically designed for transplant-eligible patients
    - Risk stratification guides timing of transplant evaluation and referral
    - Higher risk categories warrant urgent transplant consideration
    - Age, performance status, and comorbidities influence transplant eligibility
    - Early referral allows for optimal donor identification and preparation
    
    JAK Inhibitor Therapy:
    - Primary therapy for symptom management across all risk categories
    - May provide survival benefit in addition to symptom relief
    - Consider early initiation in intermediate and high-risk patients
    - Monitor for treatment response and potential complications
    - Discontinuation may be necessary if disease progression occurs
    
    Clinical Trial Participation:
    - Encourage enrollment in appropriate clinical trials
    - Particularly important for high-risk patients with limited options
    - Novel therapeutic approaches may offer survival benefits
    - Consider combination therapies and investigational agents
    
    Supportive Care Measures:
    - Comprehensive management of cytopenias and complications
    - Transfusion support for severe anemia and thrombocytopenia
    - Infection prevention and management in neutropenic patients
    - Nutritional support and management of constitutional symptoms
    - Psychosocial support for patients and families
    
    Molecular Testing Requirements:
    - Next-generation sequencing panel including high-risk mutations
    - Essential for accurate MIPSS70/MIPSS70+ calculation
    - Should include ASXL1, EZH2, SRSF2, IDH1, IDH2 at minimum
    - Karyotype analysis recommended for MIPSS70+ version
    - Repeat testing may be needed if disease progression occurs
    
    Limitations and Considerations:
    - Designed specifically for patients ≤70 years of age
    - May not be applicable to older patients with different risk profiles
    - Molecular testing availability may limit implementation
    - Dynamic scoring over time may be needed as disease evolves
    - Should be integrated with other clinical factors and patient preferences
    
    References (Vancouver style):
    1. Guglielmelli P, Lasho TL, Rotunno G, Mudireddy M, Mannarelli C, Nicolosi M, et al. 
    MIPSS70: Mutation-Enhanced International Prognostic Score System for transplantation-age 
    patients with primary myelofibrosis. J Clin Oncol. 2018;36(4):310-318. 
    doi: 10.1200/JCO.2017.76.4886.
    2. Tefferi A, Guglielmelli P, Lasho TL, Rotunno G, Finke C, Mannarelli C, et al. 
    MIPSS70+ Version 2.0: Mutation and Karyotype-Enhanced International Prognostic 
    Scoring System for Primary Myelofibrosis. J Clin Oncol. 2018;36(17):1769-1770. 
    doi: 10.1200/JCO.2018.78.9867.
    3. Passamonti F, Cervantes F, Vannucchi AM, Morra E, Rumi E, Pereira A, et al. 
    A dynamic prognostic model to predict survival in primary myelofibrosis: a study 
    by the IWG-MRT (International Working Group for Myeloproliferative Neoplasms 
    Research and Treatment). Blood. 2010;115(9):1703-8. doi: 10.1182/blood-2009-09-245837.
    """
    
    age_years: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in years. Age >65 years scores 2 points; ≤65 years scores 0 points. Older age is associated with worse prognosis and increased treatment-related mortality",
        example=68
    )
    
    hemoglobin: float = Field(
        ...,
        ge=3.0,
        le=20.0,
        description="Hemoglobin level in g/dL. Values <10 g/dL score 1 point; ≥10 g/dL score 0 points. Anemia reflects disease burden and bone marrow failure",
        example=9.2
    )
    
    white_blood_count: float = Field(
        ...,
        ge=0.1,
        le=500.0,
        description="White blood cell count in ×10⁹/L. Values >25×10⁹/L score 2 points; ≤25×10⁹/L score 0 points. Extreme leukocytosis indicates aggressive disease",
        example=28.5
    )
    
    platelet_count: float = Field(
        ...,
        ge=1.0,
        le=2000.0,
        description="Platelet count in ×10⁹/L. Values <100×10⁹/L score 2 points; ≥100×10⁹/L score 0 points. Thrombocytopenia indicates advanced bone marrow failure",
        example=85.0
    )
    
    circulating_blasts: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Percentage of circulating blasts in peripheral blood. Values >2% score 1 point; ≤2% score 0 points. Higher blast percentage indicates disease progression",
        example=3.5
    )
    
    constitutional_symptoms: Literal["yes", "no"] = Field(
        ...,
        description="Presence of constitutional symptoms (weight loss >10% in 6 months, night sweats, fever). Present scores 1 point; absent scores 0 points",
        example="yes"
    )
    
    high_molecular_risk_mutations: Literal["yes", "no"] = Field(
        ...,
        description="Presence of high molecular risk mutations (ASXL1, EZH2, SRSF2, IDH1/2). Present scores 1 point; absent scores 0 points. Essential for accurate risk stratification",
        example="yes"
    )
    
    very_high_molecular_risk: Optional[Literal["yes", "no", "unknown"]] = Field(
        "unknown",
        description="Presence of very high molecular risk (≥2 high-risk mutations or specific patterns). Used in MIPSS70+ version. Present scores 1 point; absent scores 0 points",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_years": 68,
                "hemoglobin": 9.2,
                "white_blood_count": 28.5,
                "platelet_count": 85.0,
                "circulating_blasts": 3.5,
                "constitutional_symptoms": "yes",
                "high_molecular_risk_mutations": "yes",
                "very_high_molecular_risk": "no"
            }
        }


class Mipss70Response(BaseModel):
    """
    Response model for Mutation-Enhanced International Prognostic Score System (MIPSS70/MIPSS70+)
    
    The MIPSS70/MIPSS70+ scoring system provides comprehensive risk stratification for 
    primary myelofibrosis patients ≤70 years, enabling precise treatment planning and 
    transplantation decision-making based on molecular-enhanced prognostic assessment.
    
    Risk Categories and Clinical Management:
    
    Low Risk (0-2 points) - Excellent Prognosis:
    - Median survival exceeding 20 years with conservative management
    - Standard monitoring every 3-6 months with routine laboratory assessment
    - No indication for allogeneic stem cell transplantation
    - JAK inhibitor therapy only for symptomatic splenomegaly or constitutional symptoms
    - Focus on quality of life maintenance and symptom management
    - Consider clinical trial participation for novel therapeutic approaches
    - Long-term care planning with emphasis on comorbidity management
    
    Intermediate-1 Risk (3-4 points) - Good Prognosis:
    - Median survival 8-20 years with selective treatment interventions
    - Regular monitoring every 2-4 months with comprehensive assessment
    - JAK inhibitor therapy recommended for symptomatic disease
    - Transplantation generally deferred unless disease progression occurs
    - Monitor for evolution to higher risk categories over time
    - Supportive care for anemia, thrombocytopenia, and other complications
    - Patient education about disease trajectory and treatment options
    
    Intermediate-2 Risk (5-6 points) - Intermediate Prognosis:
    - Median survival 4-8 years requiring active treatment strategy
    - Close monitoring every 1-3 months with detailed clinical evaluation
    - JAK inhibitor therapy strongly recommended for symptom control
    - Allogeneic stem cell transplantation evaluation strongly recommended
    - Early referral to transplant center for donor evaluation and preparation
    - Aggressive supportive care including transfusion support as needed
    - Consider clinical trial participation for experimental therapies
    
    High Risk (≥7 points) - Poor Prognosis:
    - Median survival less than 4 years requiring urgent intervention
    - Intensive monitoring and comprehensive multidisciplinary care
    - Immediate allogeneic stem cell transplantation evaluation and referral
    - JAK inhibitor therapy for symptom palliation and bridge to transplant
    - Consider experimental therapies and investigational clinical trials
    - Aggressive supportive care with transfusion and infection management
    - Palliative care consultation for symptom management and quality of life
    
    Treatment Decision Framework:
    
    Allogeneic Stem Cell Transplantation:
    - Primary curative option for intermediate-2 and high-risk patients
    - Consider patient age, performance status, and comorbidity profile
    - HLA-typed donor identification and availability assessment
    - Timing critical to balance disease progression against transplant risks
    - Reduced-intensity conditioning may be appropriate for older patients
    - Post-transplant monitoring for graft-versus-host disease and relapse
    
    JAK Inhibitor Therapy:
    - First-line treatment for symptomatic disease across all risk categories
    - Ruxolitinib most extensively studied with proven efficacy
    - Monitor for dose-limiting cytopenias and adjust therapy accordingly
    - May provide survival benefit in addition to symptom improvement
    - Consider combination with other targeted therapies in clinical trials
    - Long-term monitoring for treatment response and resistance development
    
    Supportive Care Interventions:
    - Comprehensive management of disease-related complications
    - Transfusion support for severe anemia and thrombocytopenia
    - Iron chelation therapy for patients requiring chronic transfusions
    - Prophylactic antimicrobial therapy for neutropenic patients
    - Nutritional support and management of constitutional symptoms
    - Splenectomy consideration for massive splenomegaly and hypersplenism
    
    Clinical Trial Considerations:
    - Encourage participation in appropriate clinical trials for all risk categories
    - Novel agents targeting aberrant signaling pathways under investigation
    - Combination therapies may offer synergistic benefits
    - Early-phase trials for high-risk patients with limited standard options
    - Correlative studies to identify biomarkers of treatment response
    
    Long-term Monitoring and Follow-up:
    - Regular assessment of disease status and treatment response
    - Monitoring for leukemic transformation and secondary malignancies
    - Quality of life assessment and psychosocial support
    - Comorbidity management and preventive care measures
    - Family counseling and genetic counseling as appropriate
    - End-of-life planning discussions for patients with advanced disease
    
    Molecular Testing and Reassessment:
    - Baseline comprehensive molecular profiling essential for accurate scoring
    - Consider repeat testing if significant clinical deterioration occurs
    - Monitor for emergence of new high-risk mutations over time
    - Integrate molecular findings with clinical parameters for treatment decisions
    - Research participation to advance understanding of disease biology
    
    Reference: Guglielmelli P, et al. J Clin Oncol. 2018;36(4):310-318.
    """
    
    result: int = Field(
        ...,
        description="MIPSS70/MIPSS70+ risk score (range 0-10 points)",
        example=8
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation with risk stratification and comprehensive management recommendations",
        example="HIGH RISK PRIMARY MYELOFIBROSIS (MIPSS70+ Score: 8): Poor prognosis with median survival less than 4 years. MANAGEMENT: Intensive monitoring and aggressive treatment approach. TREATMENT: JAK inhibitor therapy for symptom palliation. Aggressive supportive care including transfusion support, infection prophylaxis, and management of complications. TRANSPLANT: Prioritize urgent allogeneic stem cell transplantation evaluation and referral to transplant center. Consider experimental therapies and clinical trial participation. PROGNOSIS: Poor survival outcomes requiring intensive multidisciplinary care and early transplant consideration."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="High risk primary myelofibrosis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 8,
                "unit": "points",
                "interpretation": "HIGH RISK PRIMARY MYELOFIBROSIS (MIPSS70+ Score: 8): Poor prognosis with median survival less than 4 years. MANAGEMENT: Intensive monitoring and aggressive treatment approach. TREATMENT: JAK inhibitor therapy for symptom palliation. Aggressive supportive care including transfusion support, infection prophylaxis, and management of complications. TRANSPLANT: Prioritize urgent allogeneic stem cell transplantation evaluation and referral to transplant center. Consider experimental therapies and clinical trial participation. PROGNOSIS: Poor survival outcomes requiring intensive multidisciplinary care and early transplant consideration.",
                "stage": "High Risk",
                "stage_description": "High risk primary myelofibrosis"
            }
        }