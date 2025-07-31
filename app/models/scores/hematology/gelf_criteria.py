"""
Groupe d'Etude des Lymphomes Folliculaires (GELF) Criteria Models

Request and response models for GELF Criteria calculation.

References (Vancouver style):
1. Brice P, Bastion Y, Lepage E, et al. Comparison in low-tumor-burden follicular 
   lymphomas between an initial no-treatment policy, prednimustine, or interferon alfa: 
   a randomized study from the Groupe d'Etude des Lymphomes Folliculaires. J Clin Oncol. 
   1997;15(3):1110-1117. doi: 10.1200/JCO.1997.15.3.1110
2. Solal-Céligny P, Roy P, Colombat P, et al. Follicular lymphoma international prognostic 
   index. Blood. 2004;104(5):1258-1265. doi: 10.1182/blood-2003-12-4434
3. Ardeshna KM, Smith P, Norton A, et al. Long-term effect of a watch and wait policy 
   versus immediate systemic treatment for asymptomatic advanced-stage non-Hodgkin lymphoma: 
   a randomised controlled trial. Lancet. 2003;362(9383):516-522. doi: 10.1016/S0140-6736(03)14110-4

The Groupe d'Etude des Lymphomes Folliculaires (GELF) Criteria is a clinical decision 
tool developed to determine whether patients with follicular lymphoma require immediate 
treatment or can be managed with active surveillance (watch and wait approach).

**Clinical Background**:
Follicular lymphoma is an indolent B-cell non-Hodgkin lymphoma that often presents in 
advanced stages but with a variable clinical course. Many patients with low tumor burden 
can be safely managed with active surveillance, while those with high tumor burden require 
immediate treatment. The GELF criteria were developed to standardize this important 
treatment decision and harmonize clinical trial populations.

**Historical Context**:
The GELF criteria were originally developed by the Groupe d'Etude des Lymphomes Folliculaires 
in the pre-rituximab era (1997) but remain relevant in the current treatment landscape. 
The criteria help distinguish between patients who can safely undergo watchful waiting 
versus those who require immediate therapeutic intervention.

**Nine GELF Criteria Parameters**:

**Anatomical/Mass Effect Criteria**:

**1. Tumor Mass >7cm**: 
- Any single nodal or extranodal tumor mass >7 cm in diameter
- Assessed by CT or PET-CT imaging
- Large masses may cause local symptoms or complications

**2. Multiple Large Nodal Sites**:
- Involvement of ≥3 nodal sites, each >3 cm in diameter
- Indicates extensive nodal disease burden
- Multiple large nodes suggest more aggressive disease behavior

**3. Splenic Enlargement**:
- Splenomegaly with inferior margin extending below the umbilical line
- Assessed by physical examination and imaging
- May cause abdominal discomfort, early satiety, or cytopenias

**4. Compression Syndrome**:
- Ureteral compression causing hydronephrosis
- Orbital compression affecting vision
- Gastrointestinal compression causing bowel obstruction
- Any compression requiring urgent intervention

**Systemic Disease Criteria**:

**5. B Symptoms**:
- Fever >38°C (100.4°F) for >3 consecutive days
- Drenching night sweats requiring clothing/bedding changes
- Unintentional weight loss >10% of body weight in 6 months
- Indicates systemic inflammatory response

**6. Serous Effusions**:
- Pleural effusion confirmed by imaging or thoracentesis
- Peritoneal effusion (ascites) confirmed by imaging or paracentesis
- Must be related to lymphoma, not other causes

**Hematologic/Leukemic Criteria**:

**7. Leukemic Phase**:
- >5.0 × 10⁹/L circulating malignant lymphoma cells in peripheral blood
- Confirmed by flow cytometry or morphologic assessment
- Indicates significant bone marrow involvement

**8. Granulocytopenia**:
- Absolute granulocyte count <1.0 × 10⁹/L
- Due to bone marrow involvement by lymphoma
- Increases infection risk requiring prompt treatment

**9. Thrombocytopenia**:
- Platelet count <100 × 10⁹/L  
- Due to bone marrow involvement or hypersplenism
- May cause bleeding complications

**Clinical Decision Framework**:

**Low Tumor Burden (No GELF Criteria Met)**:
- Active surveillance (watch and wait) is appropriate
- Regular monitoring every 3-6 months initially
- Treatment initiated when progression occurs or symptoms develop
- Excellent overall survival with this approach

**High Tumor Burden (≥1 GELF Criteria Met)**:
- Immediate treatment recommended
- Cannot safely undergo active surveillance
- Risk of rapid progression or complications
- Requires prompt initiation of systemic therapy

**Treatment Implications**:

**Active Surveillance Protocol**:
- Clinical assessment every 3-6 months initially, then 6-12 months
- CT scans every 6-12 months or when clinically indicated
- Complete blood counts to monitor for cytopenias
- Patient education about warning symptoms

**Immediate Treatment Options**:
- Rituximab-based regimens (R-CHOP, R-CVP, R-bendamustine)
- Choice depends on patient age, comorbidities, and preferences
- Consider clinical trial enrollment when appropriate
- Multidisciplinary team approach recommended

**Modern Clinical Context**:
While the GELF criteria remain important for standardizing treatment decisions, recent 
studies have shown some discordance between GELF criteria and actual treatment patterns 
in routine clinical practice. Clinicians often consider additional factors such as patient 
anxiety, comorbidities, rate of disease progression, and quality of life when making 
final treatment decisions.

**Prognostic Considerations**:
The GELF criteria should be used in conjunction with prognostic scoring systems such as 
the Follicular Lymphoma International Prognostic Index (FLIPI) for comprehensive risk 
assessment. The combination provides a more complete picture of disease biology and 
expected outcomes.

**Quality of Life and Patient Preferences**:
Treatment decisions should always incorporate patient preferences, quality of life 
considerations, and individual clinical circumstances. Some patients may prefer active 
treatment despite low tumor burden due to anxiety about disease progression, while others 
may prefer surveillance even with borderline GELF criteria if asymptomatic.

The GELF criteria provide a valuable framework for treatment decision-making in follicular 
lymphoma, helping to standardize care while allowing for individualized treatment approaches 
based on patient-specific factors and clinical judgment.
"""

from pydantic import BaseModel, Field
from typing import Literal


class GelfCriteriaRequest(BaseModel):
    """
    Request model for Groupe d'Etude des Lymphomes Folliculaires (GELF) Criteria
    
    The GELF Criteria determines whether patients with follicular lymphoma require 
    immediate treatment or can be managed with active surveillance. The assessment 
    is based on nine clinical parameters that indicate high tumor burden requiring 
    immediate therapeutic intervention.
    
    **Assessment Guidelines**:
    All parameters should be assessed at the time of initial diagnosis or when 
    considering treatment initiation. Each parameter should be carefully evaluated 
    based on clinical examination, laboratory results, and appropriate imaging studies.
    
    **Anatomical and Mass Effect Parameters**:
    
    **Tumor Mass >7cm**: Any single nodal or extranodal tumor mass exceeding 7 cm 
    in diameter as measured by CT or PET-CT imaging. Large masses may cause local 
    symptoms or complications requiring prompt treatment.
    
    **≥3 Nodal Sites >3cm**: Involvement of three or more nodal sites, each exceeding 
    3 cm in diameter. This indicates extensive nodal disease burden that may not be 
    suitable for radiation therapy alone and suggests need for systemic treatment.
    
    **Splenic Enlargement**: Splenomegaly with the inferior margin extending below 
    the umbilical line, assessed by physical examination and confirmed by imaging. 
    May cause abdominal symptoms, early satiety, or cytopenias due to hypersplenism.
    
    **Compression Syndrome**: Any anatomical compression requiring intervention, 
    including ureteral compression causing hydronephrosis, orbital compression 
    affecting vision, or gastrointestinal compression causing bowel obstruction.
    
    **Systemic Disease Parameters**:
    
    **B Symptoms**: Constitutional symptoms including fever >38°C for >3 consecutive 
    days, drenching night sweats requiring clothing/bedding changes, or unintentional 
    weight loss >10% of body weight in 6 months. These indicate systemic inflammatory 
    response and disease activity.
    
    **Serous Effusions**: Pleural or peritoneal effusions confirmed by imaging or 
    diagnostic procedures. Must be attributable to lymphoma rather than other causes 
    such as heart failure or liver disease.
    
    **Hematologic Parameters**:
    
    **Leukemic Phase**: >5.0 × 10⁹/L circulating malignant lymphoma cells in peripheral 
    blood, confirmed by flow cytometry or morphologic assessment. Indicates significant 
    bone marrow involvement.
    
    **Granulocytopenia**: Absolute granulocyte count <1.0 × 10⁹/L due to bone marrow 
    involvement by lymphoma. Increases infection risk and requires prompt treatment.
    
    **Thrombocytopenia**: Platelet count <100 × 10⁹/L due to bone marrow involvement 
    or hypersplenism. May cause bleeding complications requiring immediate attention.
    
    **Clinical Decision Framework**:
    - **No criteria met**: Active surveillance appropriate with regular monitoring
    - **≥1 criteria met**: High tumor burden requiring immediate treatment
    
    References (Vancouver style):
    1. Brice P, Bastion Y, Lepage E, et al. Comparison in low-tumor-burden follicular 
    lymphomas between an initial no-treatment policy, prednimustine, or interferon alfa: 
    a randomized study from the Groupe d'Etude des Lymphomes Folliculaires. J Clin Oncol. 
    1997;15(3):1110-1117. doi: 10.1200/JCO.1997.15.3.1110
    2. Ardeshna KM, Smith P, Norton A, et al. Long-term effect of a watch and wait policy 
    versus immediate systemic treatment for asymptomatic advanced-stage non-Hodgkin lymphoma: 
    a randomised controlled trial. Lancet. 2003;362(9383):516-522. doi: 10.1016/S0140-6736(03)14110-4
    """
    
    tumor_mass_over_7cm: Literal["yes", "no"] = Field(
        ...,
        description="Any nodal or extranodal tumor mass >7 cm diameter (assessed by CT/PET-CT imaging)",
        example="no"
    )
    
    three_or_more_nodal_sites: Literal["yes", "no"] = Field(
        ...,
        description="Involvement of ≥3 nodal sites, each >3 cm diameter (indicates extensive nodal disease)",
        example="no"
    )
    
    systemic_b_symptoms: Literal["yes", "no"] = Field(
        ...,
        description="B symptoms: fever >38°C for >3 days, drenching night sweats, or weight loss >10% in 6 months",
        example="no"
    )
    
    splenic_enlargement: Literal["yes", "no"] = Field(
        ...,
        description="Splenomegaly with inferior margin below umbilical line (by examination and imaging)",
        example="no"
    )
    
    compression_syndrome: Literal["yes", "no"] = Field(
        ...,
        description="Compression syndrome: ureteral, orbital, or gastrointestinal compression requiring intervention",
        example="no"
    )
    
    serous_effusion: Literal["yes", "no"] = Field(
        ...,
        description="Pleural or peritoneal serous effusion attributable to lymphoma (confirmed by imaging/procedures)",
        example="no"
    )
    
    leukemic_phase: Literal["yes", "no"] = Field(
        ...,
        description="Leukemic phase: >5.0 × 10⁹/L circulating malignant cells (confirmed by flow cytometry)",
        example="no"
    )
    
    granulocyte_count_low: Literal["yes", "no"] = Field(
        ...,
        description="Granulocytopenia: absolute granulocyte count <1.0 × 10⁹/L due to bone marrow involvement",
        example="no"
    )
    
    platelet_count_low: Literal["yes", "no"] = Field(
        ...,
        description="Thrombocytopenia: platelet count <100 × 10⁹/L due to bone marrow involvement or hypersplenism",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "tumor_mass_over_7cm": "no",
                "three_or_more_nodal_sites": "no",
                "systemic_b_symptoms": "no",
                "splenic_enlargement": "no",
                "compression_syndrome": "no",
                "serous_effusion": "no",
                "leukemic_phase": "no",
                "granulocyte_count_low": "no",
                "platelet_count_low": "no"
            }
        }


class GelfCriteriaResponse(BaseModel):
    """
    Response model for Groupe d'Etude des Lymphomes Folliculaires (GELF) Criteria
    
    Provides the GELF assessment with treatment recommendations based on tumor burden 
    evaluation. The response helps guide treatment decisions between active surveillance 
    and immediate therapy in patients with follicular lymphoma.
    
    **Clinical Decision Framework**:
    
    **Low Tumor Burden (No GELF Criteria Met)**:
    - **Management**: Active surveillance (watch and wait) is appropriate
    - **Monitoring**: Clinical assessment every 3-6 months initially, then every 6-12 months
    - **Imaging**: CT scans every 6-12 months or when clinically indicated
    - **Laboratory**: Regular CBC monitoring for development of cytopenias
    - **Patient Education**: Warning symptoms requiring immediate evaluation
    - **Outcomes**: Excellent overall survival with this approach
    
    **High Tumor Burden (≥1 GELF Criteria Met)**:
    - **Management**: Immediate treatment recommended rather than surveillance
    - **Treatment Options**: Rituximab-based regimens (R-CHOP, R-CVP, R-bendamustine)
    - **Selection Factors**: Patient age, comorbidities, performance status, preferences
    - **Staging**: Complete staging with PET-CT and bone marrow biopsy before treatment
    - **Team Approach**: Multidisciplinary discussion for optimal treatment planning
    - **Clinical Trials**: Consider enrollment when appropriate
    
    **Treatment Selection Considerations**:
    
    **For Immediate Treatment**:
    - **R-CHOP**: Younger patients, good performance status, need for rapid response
    - **R-CVP**: Older patients, comorbidities limiting anthracycline use
    - **R-Bendamustine**: Good efficacy with favorable toxicity profile
    - **Radiation**: Selected cases with limited-stage disease
    
    **For Active Surveillance**:
    - **Monitoring Schedule**: More frequent initially (every 3 months), then extend intervals
    - **Progression Criteria**: New GELF criteria, transformation, rapid growth (>50% in 3 months)
    - **Quality of Life**: Maintain excellent quality of life during surveillance
    - **Patient Anxiety**: Address concerns about not receiving immediate treatment
    
    **Prognostic Integration**:
    The GELF criteria should be combined with prognostic scoring systems like FLIPI 
    (Follicular Lymphoma International Prognostic Index) for comprehensive risk assessment:
    - **FLIPI Factors**: Age, stage, hemoglobin, LDH, number of nodal areas
    - **Combined Assessment**: GELF for treatment timing, FLIPI for long-term prognosis
    - **Risk Stratification**: Helps predict overall survival and disease behavior
    
    **Modern Clinical Context**:
    While GELF criteria provide standardized guidelines, recent studies show some 
    discordance with actual treatment patterns. Clinicians consider additional factors:
    - **Patient Preferences**: Anxiety about surveillance vs. treatment toxicity concerns
    - **Comorbidities**: Impact on treatment tolerance and life expectancy
    - **Social Factors**: Access to care, ability to comply with monitoring
    - **Disease Dynamics**: Rate of progression, transformation risk
    
    **Quality Measures and Follow-up**:
    - **Response Assessment**: PET-CT after 2-4 cycles of treatment
    - **Surveillance Guidelines**: National Comprehensive Cancer Network (NCCN) recommendations
    - **Long-term Monitoring**: Secondary malignancy risk, transformation surveillance
    - **Supportive Care**: Infection prophylaxis, immunization guidelines
    
    **Important Clinical Considerations**:
    - GELF criteria were developed in pre-rituximab era but remain clinically relevant
    - Should complement, not replace, clinical judgment and patient preferences
    - Regular reassessment during surveillance as clinical status may change
    - Consider second opinions for complex cases or treatment decisions
    - Document rationale for treatment decisions, especially when deviating from GELF recommendations
    
    Reference: Brice P, et al. J Clin Oncol. 1997;15(3):1110-1117.
    """
    
    result: str = Field(
        ...,
        description="GELF assessment result indicating treatment recommendation (Active Surveillance Appropriate or Immediate Therapy Recommended)",
        example="Active Surveillance Appropriate"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the assessment result",
        example="recommendation"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including criteria assessment, treatment recommendation, clinical guidance, and important considerations for follicular lymphoma management",
        example="No GELF criteria are met. GELF Assessment: Low tumor burden. Active surveillance (watch and wait) is appropriate. Regular monitoring recommended with treatment initiation when disease progression, transformation, or symptomatic disease develops. Clinical guidance: Monitor every 3-6 months initially, then every 6-12 months if stable. Consider FLIPI score for additional prognostic stratification. Patient education about symptoms requiring immediate evaluation is essential. Quality of life should be preserved during surveillance period. Important considerations: GELF criteria were developed to standardize treatment decisions in follicular lymphoma but should be used in conjunction with clinical judgment, patient preferences, and comorbidities. Consider FLIPI score for prognostic assessment. Recent studies suggest some discordance between GELF criteria and actual treatment patterns in routine practice. The criteria were developed in the pre-rituximab era but remain relevant for current management decisions."
    )
    
    stage: str = Field(
        ...,
        description="Tumor burden classification (Low Tumor Burden or High Tumor Burden)",
        example="Low Tumor Burden"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the tumor burden assessment",
        example="No GELF criteria met - watch and wait recommended"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Active Surveillance Appropriate",
                "unit": "recommendation",
                "interpretation": "No GELF criteria are met. GELF Assessment: Low tumor burden. Active surveillance (watch and wait) is appropriate. Regular monitoring recommended with treatment initiation when disease progression, transformation, or symptomatic disease develops. Clinical guidance: Monitor every 3-6 months initially, then every 6-12 months if stable. Consider FLIPI score for additional prognostic stratification. Patient education about symptoms requiring immediate evaluation is essential. Quality of life should be preserved during surveillance period. Important considerations: GELF criteria were developed to standardize treatment decisions in follicular lymphoma but should be used in conjunction with clinical judgment, patient preferences, and comorbidities. Consider FLIPI score for prognostic assessment. Recent studies suggest some discordance between GELF criteria and actual treatment patterns in routine practice. The criteria were developed in the pre-rituximab era but remain relevant for current management decisions.",
                "stage": "Low Tumor Burden",
                "stage_description": "No GELF criteria met - watch and wait recommended"
            }
        }