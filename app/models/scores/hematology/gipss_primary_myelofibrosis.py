"""
GIPSS - Genetically Inspired Prognostic Scoring System for Primary Myelofibrosis Models

Request and response models for GIPSS calculation in primary myelofibrosis.

References (Vancouver style):
1. Tefferi A, Guglielmelli P, Nicolosi M, et al. GIPSS: genetically inspired prognostic scoring 
   system for primary myelofibrosis. Leukemia. 2018;32(7):1631-1642. doi: 10.1038/s41375-018-0107-z.
2. Passamonti F, Giorgino T, Mora B, et al. A clinical-molecular prognostic model to predict 
   survival in patients with post polycythemia vera and post essential thrombocythemia myelofibrosis. 
   Leukemia. 2017;31(12):2726-2731. doi: 10.1038/leu.2017.169.
3. Guglielmelli P, Lasho TL, Rotunno G, et al. MIPSS70: Mutation-Enhanced International Prognostic 
   Score System for transplantation-age patients with primary myelofibrosis. J Clin Oncol. 
   2018;36(4):310-318. doi: 10.1200/JCO.2017.76.4886.

The GIPSS (Genetically Inspired Prognostic Scoring System) represents a paradigm shift in 
myelofibrosis prognostication by relying exclusively on genetic markers rather than clinical 
parameters. This approach addresses key limitations of traditional scoring systems like DIPSS 
(Dynamic International Prognostic Scoring System) which incorporate subjective clinical variables 
such as constitutional symptoms and may be limited by inadequate bone marrow sampling in 
fibrotic marrows.

Developed through analysis of 641 patients with primary myelofibrosis, GIPSS identifies five 
independent genetic predictors of survival: very high-risk karyotype, unfavorable karyotype, 
absence of type 1/like CALR mutation, and presence of ASXL1, SRSF2, or U2AF1Q157 mutations. 
These factors were weighted by hazard ratios to create a four-tiered risk stratification system 
with significantly different survival outcomes.

Clinical Applications:
- Prognostic assessment for patients with primary myelofibrosis
- Allogeneic stem cell transplant decision-making and candidacy evaluation
- Treatment planning and intensity decisions
- Patient counseling and goals of care discussions
- Clinical trial stratification and endpoint prediction
- Long-term surveillance and monitoring strategies

Key Advantages over Clinical Scoring Systems:
- Eliminates subjective clinical assessment variables
- Can be performed on peripheral blood samples, avoiding bone marrow aspiration
- Provides objective, reproducible risk assessment
- Independent of clinical expertise in symptom assessment
- Particularly valuable in patients with dry bone marrow aspirations
- Superior predictive accuracy compared to DIPSS in discordant cases

Genetic Components and Biological Significance:

Karyotype Risk Classification:
- Favorable: Normal karyotype or isolated loss of chromosome Y
- Unfavorable: All other abnormalities except very high-risk
- Very High-Risk: Monosomal karyotype, inv(3), i(17q), -12, 11q23 rearrangements

Driver Mutations:
- Type 1/like CALR mutations: Associated with better prognosis, thrombocytosis, lower leukocyte count
- JAK2V617F: Most common driver mutation, associated with intermediate prognosis
- MPL mutations: Less common, associated with thrombocytosis and older age

High Molecular Risk (HMR) Mutations:
- ASXL1: Chromatin remodeling gene, associated with poor prognosis and increased blast transformation
- SRSF2: Splicing factor gene, associated with poor survival and increased transformation risk
- U2AF1Q157: Splicing factor gene, specific Q157 mutation associated with adverse outcomes

The GIPSS model demonstrates that genetic factors provide more robust prognostic information 
than clinical variables, supporting the transition toward precision medicine in myelofibrosis 
management. This approach enables more accurate identification of patients who would benefit 
from aggressive interventions like allogeneic transplantation versus those suitable for 
conservative management.
"""

from pydantic import BaseModel, Field
from typing import Literal


class GipssPrimaryMyelofibrosisRequest(BaseModel):
    """
    Request model for GIPSS - Genetically Inspired Prognostic Scoring System for Primary Myelofibrosis
    
    The GIPSS provides prognostic assessment for primary myelofibrosis patients based exclusively 
    on genetic markers, eliminating subjective clinical variables and providing objective risk 
    stratification for treatment planning decisions.
    
    **CLINICAL CONTEXT AND INDICATIONS**:
    
    **Primary Indication**: 
    - Patients with confirmed primary myelofibrosis requiring prognostic assessment
    
    **Clinical Applications**:
    - **Treatment Decision-Making**: Determine intensity of treatment approach and intervention timing
    - **Transplant Evaluation**: Identify candidates for allogeneic stem cell transplant
    - **Patient Counseling**: Provide evidence-based prognostic information for informed decision-making
    - **Clinical Trial Enrollment**: Risk stratification for research participation
    - **Long-term Planning**: Guide surveillance frequency and care coordination
    - **Resource Allocation**: Optimize healthcare resource utilization based on risk category
    
    **GENETIC PARAMETER INTERPRETATION GUIDE**:
    
    **CYTOGENETIC RISK CLASSIFICATION**:
    
    **Favorable Karyotype (0 points)**:
    - **Definition**: Normal karyotype (46,XX or 46,XY) or isolated loss of chromosome Y (-Y)
    - **Clinical Context**: Associated with better overall survival and lower transformation risk
    - **Frequency**: Approximately 70-80% of primary myelofibrosis patients
    - **Implications**: Generally indicates more indolent disease course with longer survival
    
    **Unfavorable Karyotype (1 point)**:
    - **Definition**: All other cytogenetic abnormalities except those classified as very high-risk
    - **Examples**: Isolated trisomy 8 (+8), del(20q), del(13q), +9, isolated complex (3-4 abnormalities)
    - **Clinical Context**: Intermediate prognostic impact with moderate survival reduction
    - **Frequency**: Approximately 15-20% of primary myelofibrosis patients
    - **Implications**: May benefit from closer monitoring and earlier intervention consideration
    
    **Very High-Risk Karyotype (2 points)**:
    - **Definition**: Monosomal karyotype, inv(3), i(17q), chromosome 12 abnormalities, 11q23 rearrangements
    - **Examples**: Monosomal (≥2 autosomal monosomies or single monosomy + structural abnormality)
    - **Clinical Context**: Associated with very poor survival and high transformation risk
    - **Frequency**: Approximately 5-10% of primary myelofibrosis patients
    - **Implications**: Strong indication for aggressive treatment including transplant evaluation
    
    **MOLECULAR GENETIC MARKERS**:
    
    **Type 1/like CALR Mutation Status**:
    
    **Present (0 points)**:
    - **Definition**: Type 1 (52bp deletion) or type 1-like CALR mutations in exon 9
    - **Clinical Context**: Associated with better survival, younger age, higher platelet count
    - **Frequency**: Approximately 25-30% of primary myelofibrosis patients
    - **Laboratory Features**: Often associated with thrombocytosis, lower leukocyte count
    - **Prognostic Impact**: Protective factor associated with improved overall survival
    
    **Absent (1 point)**:
    - **Definition**: No type 1/like CALR mutation detected
    - **Includes**: JAK2V617F-positive, MPL-positive, or triple-negative molecular status
    - **Clinical Context**: Less favorable prognosis compared to type 1 CALR-positive cases
    - **Implications**: May require more intensive monitoring and earlier treatment consideration
    
    **HIGH MOLECULAR RISK (HMR) MUTATIONS**:
    
    **ASXL1 (Additional Sex Combs-Like 1) Mutation**:
    
    **Present (1 point)**:
    - **Gene Function**: Chromatin remodeling and transcriptional regulation
    - **Mutation Type**: Typically frameshift or nonsense mutations leading to loss of function
    - **Clinical Impact**: Associated with poor overall survival and increased leukemic transformation
    - **Frequency**: Approximately 20-25% of primary myelofibrosis patients
    - **Laboratory Features**: May be associated with higher blast count and more severe cytopenias
    
    **SRSF2 (Serine/Arginine-Rich Splicing Factor 2) Mutation**:
    
    **Present (1 point)**:
    - **Gene Function**: RNA splicing regulation and mRNA processing
    - **Mutation Type**: Typically missense mutations affecting splicing activity
    - **Clinical Impact**: Associated with poor survival and increased transformation risk
    - **Frequency**: Approximately 15-20% of primary myelofibrosis patients
    - **Laboratory Features**: Often associated with ring sideroblasts if concurrent myelodysplasia
    
    **U2AF1Q157 (U2 Small Nuclear RNA Auxiliary Factor 1) Mutation**:
    
    **Present (1 point)**:
    - **Gene Function**: RNA splicing machinery component essential for intron recognition
    - **Mutation Specificity**: Specific Q157 amino acid position mutations (Q157R, Q157P)
    - **Clinical Impact**: Associated with adverse survival outcomes and transformation risk
    - **Frequency**: Approximately 5-10% of primary myelofibrosis patients
    - **Laboratory Features**: May be associated with dysplastic changes and cytopenias
    
    **CLINICAL DECISION SUPPORT FRAMEWORK**:
    
    **Genetic Testing Requirements**:
    - **Cytogenetics**: Conventional karyotyping or chromosomal microarray analysis
    - **Molecular Testing**: Next-generation sequencing panel or targeted mutation analysis
    - **Sample Types**: Peripheral blood or bone marrow (peripheral blood preferred for practical reasons)
    - **Quality Considerations**: Adequate sample quality and sufficient blast percentage for analysis
    
    **Risk Stratification and Management Approach**:
    
    **Low Risk (0 points)**:
    - **Management Strategy**: Conservative approach with observation and symptom-directed therapy
    - **Monitoring Frequency**: Every 6-12 months with complete blood count and clinical assessment
    - **Treatment Threshold**: Initiate therapy only for symptomatic disease or progressive organomegaly
    - **Transplant Consideration**: Generally not indicated unless disease progression occurs
    
    **Intermediate-1 Risk (1 point)**:
    - **Management Strategy**: Symptom-directed therapy with regular monitoring
    - **Monitoring Frequency**: Every 3-6 months with assessment for disease progression
    - **Treatment Options**: JAK inhibitors for symptomatic splenomegaly or constitutional symptoms
    - **Transplant Consideration**: Generally not indicated unless high-risk features develop
    
    **Intermediate-2 Risk (2 points)**:
    - **Management Strategy**: Active treatment consideration with transplant evaluation
    - **Monitoring Frequency**: Every 2-3 months with close surveillance for progression
    - **Treatment Approach**: Consider JAK inhibitors and evaluate transplant candidacy
    - **Transplant Consideration**: Discuss transplant options in appropriate candidates
    
    **High Risk (3-6 points)**:
    - **Management Strategy**: Aggressive treatment approach with urgent transplant evaluation
    - **Monitoring Frequency**: Every 1-2 months with intensive supportive care
    - **Treatment Approach**: JAK inhibitors for symptom control while pursuing transplant
    - **Transplant Consideration**: Strong indication for allogeneic transplant if eligible
    
    **Special Considerations**:
    
    **Age and Comorbidity Factors**:
    - Younger patients (<70 years) with high-risk disease are optimal transplant candidates
    - Older patients may benefit from palliative care focus with symptom management
    - Comorbidity assessment essential for treatment intensity decisions
    
    **Quality of Life Integration**:
    - Symptom burden assessment using validated tools (MPN-SAF, EORTC QLQ-C30)
    - Functional status evaluation for treatment tolerance and transplant eligibility
    - Patient preferences and goals of care discussions essential for decision-making
    
    **Disease Monitoring Parameters**:
    - Complete blood count with differential every 1-3 months based on risk category
    - Bone marrow biopsy annually or if clinical changes suggest progression
    - Molecular monitoring for additional mutations during follow-up
    - Spleen size assessment by physical examination or imaging
    
    References (Vancouver style):
    1. Tefferi A, Guglielmelli P, Nicolosi M, et al. GIPSS: genetically inspired prognostic scoring 
       system for primary myelofibrosis. Leukemia. 2018;32(7):1631-1642.
    2. Passamonti F, Giorgino T, Mora B, et al. A clinical-molecular prognostic model to predict 
       survival in patients with post polycythemia vera and post essential thrombocythemia myelofibrosis. 
       Leukemia. 2017;31(12):2726-2731.
    3. Guglielmelli P, Lasho TL, Rotunno G, et al. MIPSS70: Mutation-Enhanced International Prognostic 
       Score System for transplantation-age patients with primary myelofibrosis. J Clin Oncol. 
       2018;36(4):310-318.
    """
    
    karyotype_risk: Literal["favorable", "unfavorable", "very_high_risk"] = Field(
        ...,
        description="Cytogenetic risk classification: favorable=normal or -Y (0 pts), unfavorable=other abnormalities (1 pt), very_high_risk=monosomal/complex (2 pts)",
        example="favorable"
    )
    
    calr_type1_mutation: Literal["yes", "no"] = Field(
        ...,
        description="Presence of type 1/like CALR mutation in exon 9. Present=0 points (protective), absent=1 point",
        example="yes"
    )
    
    asxl1_mutation: Literal["yes", "no"] = Field(
        ...,
        description="Presence of ASXL1 (Additional Sex Combs-Like 1) mutation. Chromatin remodeling gene associated with poor prognosis. Present=1 point",
        example="no"
    )
    
    srsf2_mutation: Literal["yes", "no"] = Field(
        ...,
        description="Presence of SRSF2 (Serine/Arginine-Rich Splicing Factor 2) mutation. RNA splicing gene associated with poor survival. Present=1 point",
        example="no"
    )
    
    u2af1q157_mutation: Literal["yes", "no"] = Field(
        ...,
        description="Presence of U2AF1Q157 (U2 Small Nuclear RNA Auxiliary Factor 1) mutation at Q157 position. Splicing factor associated with adverse outcomes. Present=1 point",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "karyotype_risk": "favorable",
                "calr_type1_mutation": "yes",
                "asxl1_mutation": "no",
                "srsf2_mutation": "no",
                "u2af1q157_mutation": "no"
            }
        }


class GipssPrimaryMyelofibrosisResponse(BaseModel):
    """
    Response model for GIPSS - Genetically Inspired Prognostic Scoring System for Primary Myelofibrosis
    
    The response provides the calculated GIPSS score with detailed genetic component breakdown, 
    evidence-based survival predictions, and comprehensive clinical management recommendations 
    based on validated prognostic data from 641 primary myelofibrosis patients.
    
    **CLINICAL INTERPRETATION FRAMEWORK**:
    
    **GIPSS Score Components and Interpretation**:
    - **Total Score Range**: 0-6 points with four distinct risk categories
    - **Genetic Basis**: Exclusively based on cytogenetic and molecular genetic markers
    - **Clinical Utility**: Provides objective, reproducible prognostic assessment
    - **Validation**: Derived from large cohort with robust statistical validation
    
    **Risk Category Definitions and Survival Outcomes**:
    
    **Low Risk (0 points)**:
    - **Patient Population**: Approximately 15% of primary myelofibrosis patients
    - **Genetic Profile**: Favorable karyotype + type 1 CALR mutation + no HMR mutations
    - **Median Overall Survival**: 26.4 years (excellent long-term prognosis)
    - **5-Year Survival**: 94% (minimal early mortality risk)
    - **Clinical Characteristics**: Generally younger, lower symptom burden, less organomegaly
    
    **Intermediate-1 Risk (1 point)**:
    - **Patient Population**: Approximately 40% of primary myelofibrosis patients
    - **Genetic Profile**: Single adverse genetic factor (unfavorable karyotype OR absent CALR OR single HMR mutation)
    - **Median Overall Survival**: 8.0 years (good intermediate-term prognosis)
    - **5-Year Survival**: 73% (moderate survival probability)
    - **Clinical Characteristics**: Variable symptom burden, moderate disease activity
    
    **Intermediate-2 Risk (2 points)**:
    - **Patient Population**: Approximately 30% of primary myelofibrosis patients
    - **Genetic Profile**: Two adverse genetic factors with moderate cumulative risk
    - **Median Overall Survival**: 4.2 years (limited intermediate-term prognosis)
    - **5-Year Survival**: 40% (substantial early mortality risk)
    - **Clinical Characteristics**: Often symptomatic with organomegaly and constitutional symptoms
    
    **High Risk (3-6 points)**:
    - **Patient Population**: Approximately 15% of primary myelofibrosis patients
    - **Genetic Profile**: Multiple adverse genetic factors indicating aggressive disease biology
    - **Median Overall Survival**: 2.0 years (poor short-term prognosis)
    - **5-Year Survival**: 14% (high early mortality risk)
    - **Clinical Characteristics**: Severe symptoms, marked organomegaly, cytopenias, transformation risk
    
    **CLINICAL MANAGEMENT BY RISK CATEGORY**:
    
    **Low Risk Management Approach**:
    
    **Treatment Philosophy**:
    - Conservative management with observation and symptom-directed therapy
    - Focus on quality of life maintenance and monitoring for disease progression
    - Avoid unnecessary treatment-related toxicity in patients with excellent prognosis
    
    **Monitoring Strategy**:
    - **Frequency**: Every 6-12 months with complete blood count and clinical assessment
    - **Parameters**: Hemoglobin, platelet count, leukocyte count, spleen size, symptom assessment
    - **Imaging**: Annual spleen assessment by palpation or ultrasound if clinically indicated
    - **Molecular**: Consider repeat genetic testing if clinical progression occurs
    
    **Treatment Indications**:
    - **JAK Inhibitors**: Only for symptomatic splenomegaly or constitutional symptoms
    - **Anemia Management**: Supportive care with transfusions, erythropoietin stimulating agents
    - **Thrombocytopenia**: Platelet transfusions for bleeding or prior to procedures
    - **Infections**: Prompt treatment due to potential immune dysfunction
    
    **Intermediate-1 Risk Management Approach**:
    
    **Treatment Philosophy**:
    - Symptom-directed therapy with regular monitoring for disease progression
    - Balance between treatment benefits and potential toxicities
    - Consider patient preferences and functional status in treatment decisions
    
    **Monitoring Strategy**:
    - **Frequency**: Every 3-6 months with comprehensive disease assessment
    - **Parameters**: Complete blood count, liver function, symptom scales, spleen measurement
    - **Bone Marrow**: Annual or if clinical changes suggest progression or transformation
    - **Molecular**: Monitor for acquisition of additional high-risk mutations
    
    **Treatment Considerations**:
    - **JAK Inhibitors**: Consider for spleen size >5 cm below costal margin or symptoms
    - **Clinical Trials**: Appropriate candidates for novel therapy trials
    - **Supportive Care**: Comprehensive symptom management and quality of life optimization
    - **Transplant**: Generally not indicated unless progression to higher risk category
    
    **Intermediate-2 Risk Management Approach**:
    
    **Treatment Philosophy**:
    - Active treatment approach with consideration of aggressive interventions
    - Evaluate transplant candidacy in appropriate patients
    - Balance curative potential against treatment-related morbidity and mortality
    
    **Monitoring Strategy**:
    - **Frequency**: Every 2-3 months with intensive disease surveillance
    - **Parameters**: Complete blood count, bone marrow if indicated, molecular monitoring
    - **Transplant Evaluation**: HLA typing, donor search, transplant center referral
    - **Comorbidity Assessment**: Comprehensive evaluation of transplant eligibility
    
    **Treatment Approach**:
    - **JAK Inhibitors**: Standard therapy for symptom control and potential survival benefit
    - **Transplant Evaluation**: Discuss allogeneic stem cell transplant in eligible patients
    - **Clinical Trials**: Consider participation in investigational therapy studies
    - **Supportive Care**: Aggressive management of disease-related complications
    
    **High Risk Management Approach**:
    
    **Treatment Philosophy**:
    - Aggressive treatment with urgent transplant evaluation if eligible
    - Focus on curative approaches while managing disease-related complications
    - Palliative care integration for symptom management and quality of life
    
    **Monitoring Strategy**:
    - **Frequency**: Every 1-2 months with intensive monitoring and supportive care
    - **Parameters**: Complete blood count, bone marrow surveillance, molecular monitoring
    - **Transplant Urgency**: Expedited evaluation and donor search if appropriate
    - **Complication Management**: Proactive management of cytopenias, infections, bleeding
    
    **Treatment Approach**:
    - **Allogeneic Transplant**: Strong indication if age and performance status appropriate
    - **JAK Inhibitors**: For symptom control and potential survival benefit while pursuing transplant
    - **Clinical Trials**: High priority for investigational therapies and novel approaches
    - **Palliative Care**: Early integration for symptom management and goals of care discussions
    
    **SPECIAL CLINICAL CONSIDERATIONS**:
    
    **Age-Specific Management**:
    - **Younger Patients (<70 years)**: Optimal candidates for aggressive treatment including transplant
    - **Older Patients (≥70 years)**: Focus on symptom management and quality of life optimization
    - **Comorbidity Impact**: Significant comorbidities may preclude aggressive interventions
    
    **Transplant Decision-Making**:
    - **High-Risk Disease**: Strong indication for transplant evaluation regardless of age
    - **Intermediate-2 Risk**: Consider transplant in younger, fit patients with good performance status
    - **Lower Risk**: Transplant generally not indicated unless disease progression occurs
    
    **Quality of Life Assessment**:
    - **Symptom Scales**: Use validated tools like MPN-SAF (Myeloproliferative Neoplasm Symptom Assessment Form)
    - **Functional Status**: ECOG performance status and activities of daily living assessment
    - **Patient Preferences**: Incorporate patient values and treatment goals into decision-making
    
    **Long-term Monitoring Considerations**:
    - **Disease Progression**: Monitor for clinical and laboratory evidence of worsening disease
    - **Transformation Risk**: Surveillance for acute leukemia transformation (increased blast count)
    - **Treatment Toxicity**: Monitor for JAK inhibitor-related side effects and complications
    - **Survival Trends**: Regular reassessment of prognosis and adjustment of treatment approach
    
    Reference: Tefferi A, et al. Leukemia. 2018;32(7):1631-1642.
    """
    
    result: int = Field(
        ...,
        description="GIPSS total score calculated from genetic risk factors (0-6 points)",
        ge=0,
        le=6,
        example=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for GIPSS score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with genetic profile summary and evidence-based management recommendations",
        example="GIPSS score of 0 points based on: favorable karyotype; presence of type 1/like CALR mutation; absence of high molecular risk mutations. Risk category: Low Risk. Median overall survival: 26.4 years. 5-year survival: 94%. Excellent long-term prognosis with minimal therapeutic intervention indicated. Consider long-term observation with regular monitoring every 6-12 months. Focus on symptom management and quality of life. Allogeneic stem cell transplant not typically indicated. Monitor for disease progression or transformation."
    )
    
    stage: str = Field(
        ...,
        description="GIPSS risk category classification",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of prognosis category",
        example="Excellent prognosis"
    )
    
    median_survival_years: float = Field(
        ...,
        description="Predicted median overall survival in years based on GIPSS score",
        example=26.4
    )
    
    five_year_survival_percent: int = Field(
        ...,
        description="Predicted 5-year survival percentage based on GIPSS score",
        example=94
    )
    
    karyotype_points: int = Field(
        ...,
        description="Points contributed by cytogenetic risk classification (0-2 points)",
        ge=0,
        le=2,
        example=0
    )
    
    calr_points: int = Field(
        ...,
        description="Points contributed by CALR mutation status (0-1 points)",
        ge=0,
        le=1,
        example=0
    )
    
    asxl1_points: int = Field(
        ...,
        description="Points contributed by ASXL1 mutation presence (0-1 points)",
        ge=0,
        le=1,
        example=0
    )
    
    srsf2_points: int = Field(
        ...,
        description="Points contributed by SRSF2 mutation presence (0-1 points)",
        ge=0,
        le=1,
        example=0
    )
    
    u2af1q157_points: int = Field(
        ...,
        description="Points contributed by U2AF1Q157 mutation presence (0-1 points)",
        ge=0,
        le=1,
        example=0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "GIPSS score of 0 points based on: favorable karyotype; presence of type 1/like CALR mutation; absence of high molecular risk mutations. Risk category: Low Risk. Median overall survival: 26.4 years. 5-year survival: 94%. Excellent long-term prognosis with minimal therapeutic intervention indicated. Consider long-term observation with regular monitoring every 6-12 months. Focus on symptom management and quality of life. Allogeneic stem cell transplant not typically indicated. Monitor for disease progression or transformation.",
                "stage": "Low Risk",
                "stage_description": "Excellent prognosis",
                "median_survival_years": 26.4,
                "five_year_survival_percent": 94,
                "karyotype_points": 0,
                "calr_points": 0,
                "asxl1_points": 0,
                "srsf2_points": 0,
                "u2af1q157_points": 0
            }
        }