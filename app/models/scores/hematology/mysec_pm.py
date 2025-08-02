"""
Myelofibrosis Secondary to PV and ET-Prognostic Model (MYSEC-PM) Models

Request and response models for MYSEC-PM calculation.

References (Vancouver style):
1. Passamonti F, Giorgino T, Mora B, Guglielmelli P, Rumi E, Maffioli M, et al. 
   A clinical-molecular prognostic model to predict survival in patients with post 
   polycythemia vera and post essential thrombocythemia myelofibrosis. Leukemia. 
   2017;31(12):2726-2731. doi: 10.1038/leu.2017.169.
2. Guglielmelli P, Rotunno G, Pacilli A, Rumi E, Rosti V, Delaini F, et al. 
   Prognostic impact of bone marrow fibrosis in primary myelofibrosis. A study of 
   the AGIMM group on 490 patients. Am J Hematol. 2016;91(9):918-22. 
   doi: 10.1002/ajh.24423.
3. Tefferi A, Guglielmelli P, Lasho TL, Rotunno G, Finke C, Mannarelli C, et al. 
   MIPSS70+ Version 2.0: Mutation and Karyotype-Enhanced International Prognostic 
   Scoring System for Primary Myelofibrosis. J Clin Oncol. 2018;36(17):1769-1770. 
   doi: 10.1200/JCO.2018.78.9867.

The MYSEC-PM is a specialized prognostic model developed specifically for patients 
with myelofibrosis secondary to polycythemia vera (PV) and essential thrombocythemia (ET), 
providing superior risk stratification compared to models designed for primary myelofibrosis.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MysecPmRequest(BaseModel):
    """
    Request model for Myelofibrosis Secondary to PV and ET-Prognostic Model (MYSEC-PM)
    
    The MYSEC-PM represents a significant advancement in prognostic assessment for 
    patients with secondary myelofibrosis (SMF) following polycythemia vera (PV) 
    or essential thrombocythemia (ET). Unlike primary myelofibrosis models, the 
    MYSEC-PM was specifically developed and validated for secondary myelofibrosis, 
    incorporating both clinical parameters and molecular genetic information.
    
    Clinical Context and Development:
    
    Secondary myelofibrosis develops in approximately 4.9-6% of PV patients at 10 years 
    and 6-14% at 15 years, and in 0.8-4.9% of ET patients at 10 years and 4-11% at 15 years. 
    These patients have different biological characteristics and clinical outcomes compared 
    to primary myelofibrosis, necessitating specialized prognostic tools.
    
    Model Components and Scoring:
    
    Age (Continuous Variable):
    - Contributes 0.15 points per year of age
    - Unlike other models that use age cutoffs, MYSEC-PM treats age as continuous
    - Reflects the progressive nature of age-related risk in secondary myelofibrosis
    
    Hemoglobin Level (0-2 points):
    - <11 g/dL: 2 points (severe anemia indicating advanced disease)
    - ≥11 g/dL: 0 points (preserved red cell production)
    - Anemia reflects bone marrow failure and disease burden
    - Strong independent predictor of survival in secondary myelofibrosis
    
    Circulating Blasts (0-2 points):
    - ≥3%: 2 points (indicates accelerated phase or transformation risk)
    - <3%: 0 points (stable chronic phase disease)
    - Higher blast percentage suggests disease progression toward acute leukemia
    - Critical parameter for identifying patients at risk for blast transformation
    
    Platelet Count (0-1 point):
    - <150×10⁹/L: 1 point (thrombocytopenia indicating bone marrow failure)
    - ≥150×10⁹/L: 0 points (adequate platelet production)
    - Thrombocytopenia correlates with advanced fibrosis and poor prognosis
    - Important for bleeding risk assessment and treatment planning
    
    Constitutional Symptoms (0-1 point):
    - Present: 1 point (weight loss >10% in 6 months, night sweats, fever)
    - Absent: 0 points (no systemic symptoms)
    - Reflects cytokine-mediated systemic inflammation
    - Associated with reduced quality of life and survival
    
    CALR Mutation Status (0-2 points):
    - Unmutated: 2 points (poor prognostic factor)
    - Mutated: 0 points (better prognosis)
    - Unknown: 0 points (treated as non-risk factor)
    - CALR mutations are associated with better outcomes in myeloproliferative neoplasms
    - Essential molecular parameter for accurate risk stratification
    
    Risk Categories and Clinical Implications:
    
    Low Risk (<11 points):
    - Median survival: Not reached (excellent prognosis)
    - Management approach: Conservative with regular monitoring
    - Treatment strategy: Supportive care and symptom management
    - Transplant consideration: Not indicated due to excellent survival
    - Monitoring frequency: Every 3-6 months with routine assessments
    
    Intermediate-1 Risk (11-13.99 points):
    - Median survival: 9.3 years (95% CI: 8.1 to not reached)
    - Management approach: Active symptom management with quality of life focus
    - Treatment strategy: JAK inhibitor therapy for symptomatic disease
    - Transplant consideration: Generally deferred unless progression
    - Monitoring frequency: Every 2-4 months with comprehensive evaluation
    
    Intermediate-2 Risk (14-15.99 points):
    - Median survival: 4.4 years (95% CI: 3.2 to 7.9 years)
    - Management approach: Active treatment with transplant consideration
    - Treatment strategy: JAK inhibitors plus aggressive supportive care
    - Transplant consideration: Evaluation recommended if appropriate candidate
    - Monitoring frequency: Every 1-3 months with transplant readiness assessment
    
    High Risk (≥16 points):
    - Median survival: 2.0 years (95% CI: 1.7 to 3.9 years)
    - Management approach: Urgent intervention with intensive care
    - Treatment strategy: Immediate JAK inhibitor therapy and aggressive support
    - Transplant consideration: Urgent evaluation and prioritization
    - Monitoring frequency: Monthly or more frequent as clinically indicated
    
    Clinical Validation and Superiority:
    
    The MYSEC-PM has been extensively validated and shows superior performance 
    compared to IPSS and DIPSS in secondary myelofibrosis patients. Key validation 
    findings include:
    
    - Validated in 421 post-PV/post-ET patients treated with ruxolitinib
    - Superior risk stratification compared to primary myelofibrosis models
    - Maintained prognostic value when used over time and at ruxolitinib start
    - Enabled reclassification of patients from higher to lower risk categories
    - Adopted by NCCN and European guidelines for secondary myelofibrosis
    
    Molecular Testing Requirements:
    
    CALR mutation testing is essential for accurate MYSEC-PM calculation. Testing 
    should include comprehensive mutation analysis for:
    - CALR exon 9 mutations (type 1 and type 2 most common)
    - JAK2 V617F mutation status (for comparison and disease classification)
    - MPL mutations (for complete molecular characterization)
    
    Clinical Applications:
    
    Treatment Decision Making:
    - JAK inhibitor therapy initiation and timing
    - Allogeneic stem cell transplantation evaluation and urgency
    - Clinical trial enrollment based on risk category
    - Supportive care intensity and monitoring frequency
    
    Patient Counseling:
    - Prognosis communication with survival estimates
    - Treatment option discussions based on risk category
    - Quality of life considerations and symptom management
    - Family planning and genetic counseling as appropriate
    
    Limitations and Considerations:
    
    - Specifically designed for secondary myelofibrosis only
    - Should not be used for primary myelofibrosis (use IPSS, DIPSS, or MIPSS70)
    - Requires molecular testing for optimal accuracy
    - May need recalculation if disease parameters change significantly
    - Should be integrated with other clinical factors and patient preferences
    
    References (Vancouver style):
    1. Passamonti F, Giorgino T, Mora B, Guglielmelli P, Rumi E, Maffioli M, et al. 
    A clinical-molecular prognostic model to predict survival in patients with post 
    polycythemia vera and post essential thrombocythemia myelofibrosis. Leukemia. 
    2017;31(12):2726-2731. doi: 10.1038/leu.2017.169.
    2. Guglielmelli P, Rotunno G, Pacilli A, Rumi E, Rosti V, Delaini F, et al. 
    Prognostic impact of bone marrow fibrosis in primary myelofibrosis. A study of 
    the AGIMM group on 490 patients. Am J Hematol. 2016;91(9):918-22. 
    doi: 10.1002/ajh.24423.
    3. Tefferi A, Guglielmelli P, Lasho TL, Rotunno G, Finke C, Mannarelli C, et al. 
    MIPSS70+ Version 2.0: Mutation and Karyotype-Enhanced International Prognostic 
    Scoring System for Primary Myelofibrosis. J Clin Oncol. 2018;36(17):1769-1770. 
    doi: 10.1200/JCO.2018.78.9867.
    """
    
    age_years: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in years. Age contributes 0.15 points per year as a continuous variable, reflecting progressive age-related risk in secondary myelofibrosis",
        example=65
    )
    
    hemoglobin: float = Field(
        ...,
        ge=3.0,
        le=20.0,
        description="Hemoglobin level in g/dL. Values <11 g/dL score 2 points; ≥11 g/dL score 0 points. Severe anemia indicates advanced bone marrow failure and poor prognosis",
        example=9.5
    )
    
    circulating_blasts: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Percentage of circulating blasts in peripheral blood. Values ≥3% score 2 points; <3% score 0 points. Higher blast percentage indicates disease progression toward acute transformation",
        example=4.0
    )
    
    platelet_count: float = Field(
        ...,
        ge=1.0,
        le=2000.0,
        description="Platelet count in ×10⁹/L. Values <150×10⁹/L score 1 point; ≥150×10⁹/L score 0 points. Thrombocytopenia indicates advanced bone marrow failure and bleeding risk",
        example=120.0
    )
    
    constitutional_symptoms: Literal["yes", "no"] = Field(
        ...,
        description="Presence of constitutional symptoms (weight loss >10% in 6 months, night sweats, fever). Present scores 1 point; absent scores 0 points. Reflects systemic disease burden",
        example="yes"
    )
    
    calr_mutation_status: Literal["mutated", "unmutated", "unknown"] = Field(
        ...,
        description="CALR (Calreticulin) mutation status. Unmutated scores 2 points; mutated or unknown score 0 points. CALR mutations are associated with better prognosis in myeloproliferative neoplasms",
        example="unmutated"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_years": 65,
                "hemoglobin": 9.5,
                "circulating_blasts": 4.0,
                "platelet_count": 120.0,
                "constitutional_symptoms": "yes",
                "calr_mutation_status": "unmutated"
            }
        }


class MysecPmResponse(BaseModel):
    """
    Response model for Myelofibrosis Secondary to PV and ET-Prognostic Model (MYSEC-PM)
    
    The MYSEC-PM provides precise risk stratification for patients with secondary 
    myelofibrosis, enabling evidence-based treatment decisions and accurate prognostic 
    counseling. The model's four risk categories correspond to significantly different 
    survival outcomes and treatment recommendations.
    
    Risk Categories and Clinical Management:
    
    Low Risk (<11 points) - Excellent Prognosis:
    - Median survival not reached with excellent long-term outcomes
    - Conservative management approach with regular monitoring
    - Standard monitoring every 3-6 months with routine laboratory assessment
    - No indication for allogeneic stem cell transplantation
    - JAK inhibitor therapy only for symptomatic splenomegaly or constitutional symptoms
    - Focus on quality of life maintenance and symptom management
    - Consider clinical trial participation for novel therapeutic approaches
    - Long-term care planning with emphasis on comorbidity management
    
    Intermediate-1 Risk (11-13.99 points) - Good Prognosis:
    - Median survival 9.3 years with selective treatment interventions
    - Regular monitoring every 2-4 months with comprehensive assessment
    - JAK inhibitor therapy recommended for symptomatic disease management
    - Transplantation generally deferred unless disease progression occurs
    - Monitor for evolution to higher risk categories over time
    - Supportive care for anemia, thrombocytopenia, and other complications
    - Patient education about disease trajectory and treatment options
    - Quality of life optimization with symptom management
    
    Intermediate-2 Risk (14-15.99 points) - Intermediate Prognosis:
    - Median survival 4.4 years requiring active treatment strategy
    - Close monitoring every 1-3 months with detailed clinical evaluation
    - JAK inhibitor therapy strongly recommended for symptom control
    - Allogeneic stem cell transplantation evaluation strongly recommended
    - Early referral to transplant center for donor evaluation and preparation
    - Aggressive supportive care including transfusion support as needed
    - Consider clinical trial participation for experimental therapies
    - Multidisciplinary care coordination for optimal outcomes
    
    High Risk (≥16 points) - Poor Prognosis:
    - Median survival 2.0 years requiring urgent intervention
    - Intensive monitoring and comprehensive multidisciplinary care
    - Immediate allogeneic stem cell transplantation evaluation and referral
    - JAK inhibitor therapy for symptom palliation and potential survival benefit
    - Consider experimental therapies and investigational clinical trials
    - Aggressive supportive care with transfusion and infection management
    - Palliative care consultation for symptom management and quality of life
    - Urgent transplant center referral for immediate evaluation
    
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
    - Ruxolitinib most extensively studied with proven efficacy in secondary MF
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
    - Research participation to advance understanding of secondary MF biology
    
    Comparison with Primary Myelofibrosis Models:
    - MYSEC-PM superior to IPSS and DIPSS for secondary myelofibrosis patients
    - Enables better risk stratification and reclassification from higher to lower risk
    - Should not be used for primary myelofibrosis (use MIPSS70 or DIPSS instead)
    - Validated specifically in post-PV and post-ET patient populations
    - Adopted by international guidelines for secondary myelofibrosis management
    
    Reference: Passamonti F, et al. Leukemia. 2017;31(12):2726-2731.
    """
    
    result: float = Field(
        ...,
        description="MYSEC-PM risk score calculated from clinical and molecular parameters",
        example=17.75
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation with risk stratification and comprehensive management recommendations for secondary myelofibrosis",
        example="HIGH RISK SECONDARY MYELOFIBROSIS (MYSEC-PM Score: 17.75): Poor prognosis with median survival 2.0 years. MANAGEMENT: Intensive monitoring and aggressive treatment approach. TREATMENT: JAK inhibitor therapy for symptom palliation and potential survival benefit. Aggressive supportive care including transfusion support, infection prophylaxis, and management of complications. TRANSPLANT: Prioritize urgent allogeneic stem cell transplantation evaluation and referral to transplant center if appropriate candidate. Consider experimental therapies and clinical trial participation. PROGNOSIS: Poor survival outcomes requiring intensive multidisciplinary care and urgent transplant consideration."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification for secondary myelofibrosis",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="High risk secondary myelofibrosis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 17.75,
                "unit": "points",
                "interpretation": "HIGH RISK SECONDARY MYELOFIBROSIS (MYSEC-PM Score: 17.75): Poor prognosis with median survival 2.0 years. MANAGEMENT: Intensive monitoring and aggressive treatment approach. TREATMENT: JAK inhibitor therapy for symptom palliation and potential survival benefit. Aggressive supportive care including transfusion support, infection prophylaxis, and management of complications. TRANSPLANT: Prioritize urgent allogeneic stem cell transplantation evaluation and referral to transplant center if appropriate candidate. Consider experimental therapies and clinical trial participation. PROGNOSIS: Poor survival outcomes requiring intensive multidisciplinary care and urgent transplant consideration.",
                "stage": "High Risk",
                "stage_description": "High risk secondary myelofibrosis"
            }
        }