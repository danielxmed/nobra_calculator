"""
Veterans Aging Cohort Study-Charlson Comorbidity Index (VACS-CCI) Models

Request and response models for VACS-CCI calculation.

References (Vancouver style):
1. Justice AC, Lasky E, McGinnis KA, Skanderson M, Conigliaro J, Fultz SL, et al. 
   Medical disease and alcohol use among veterans with human immunodeficiency infection: 
   A comparison of disease measurement strategies. Med Care. 2006 Apr;44(4):S52-60. 
   doi: 10.1097/01.mlr.0000208140.93199.44.
2. McGinnis KA, Fultz SL, Skanderson M, Conigliaro J, Bryant K, Justice AC. 
   Hepatocellular carcinoma and non-Hodgkin's lymphoma: the roles of HIV, hepatitis C 
   infection, and alcohol abuse. J Clin Oncol. 2006 Nov 20;24(33):5005-9. 
   doi: 10.1200/JCO.2006.05.7984.
3. Tate JP, Justice AC, Hughes MD, Bonnet F, Reiss P, Mocroft A, et al. An internationally 
   generalizable risk index for mortality after one year of antiretroviral therapy. 
   AIDS. 2013 Feb 20;27(4):563-72. doi: 10.1097/QAD.0b013e32835c5b67.
4. Charlson ME, Pompei P, Ales KL, MacKenzie CR. A new method of classifying prognostic 
   comorbidity in longitudinal studies: development and validation. J Chronic Dis. 
   1987;40(5):373-83. doi: 10.1016/0021-9681(87)90171-8.

The Veterans Aging Cohort Study-Charlson Comorbidity Index (VACS-CCI) combines the 
VACS Index with the Charlson Comorbidity Index to provide enhanced mortality risk 
prediction for patients with HIV. This integrated tool incorporates HIV-specific 
biomarkers, general health indicators, and comprehensive comorbidity assessment to 
estimate 5-year all-cause mortality risk as a percentage from 0-100%.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class VacsCciRequest(BaseModel):
    """
    Request model for Veterans Aging Cohort Study-Charlson Comorbidity Index (VACS-CCI)
    
    The VACS-CCI is an integrated prognostic tool that combines the Veterans Aging 
    Cohort Study (VACS) Index with the Charlson Comorbidity Index to provide enhanced 
    mortality risk prediction for patients with HIV. This comprehensive assessment 
    incorporates HIV-specific biomarkers, general health indicators, and comprehensive 
    comorbidity evaluation.
    
    **SCIENTIFIC BACKGROUND:**
    
    The VACS-CCI was developed to address limitations of using either HIV-specific 
    or general health markers alone for mortality prediction in HIV-infected patients. 
    By combining the VACS Index (which captures HIV disease severity and organ 
    system injury) with the Charlson Comorbidity Index (which captures burden of 
    non-HIV comorbidities), this tool provides more accurate risk stratification.
    
    **COMPONENT OVERVIEW:**
    
    **1. VACS Index Components:**
    - **Demographics**: Age (most influential factor)
    - **HIV-specific markers**: CD4 count, HIV viral load
    - **Organ system injury**: Hemoglobin, FIB-4 (liver), eGFR (kidney)
    - **Co-infections**: Hepatitis C status
    
    **2. Charlson Comorbidity Index Components:**
    - **Cardiovascular**: Myocardial infarction, congestive heart failure, 
      peripheral vascular disease, cerebrovascular disease
    - **Neurological**: Dementia, hemiplegia/paraplegia
    - **Pulmonary**: Chronic pulmonary disease
    - **Rheumatologic**: Rheumatic disease
    - **Gastrointestinal**: Peptic ulcer disease, liver disease (mild vs moderate/severe)
    - **Endocrine**: Diabetes (uncomplicated vs with complications)
    - **Renal**: Moderate to severe renal disease
    - **Oncologic**: Any malignancy, metastatic solid tumor
    - **Immunologic**: AIDS diagnosis
    
    **DETAILED PARAMETER DESCRIPTIONS:**
    
    **Demographics and HIV Parameters:**
    
    **Age (years):**
    - Most influential single factor in mortality prediction
    - Progressive risk increase with advancing age
    - Used in both VACS scoring and FIB-4 calculation
    
    **Sex and Race:**
    - Required for accurate eGFR calculation using CKD-EPI equation
    - Race adjustment: Black patients have 15.9% higher eGFR for same creatinine
    - Sex differences: Different creatinine thresholds and coefficients
    
    **CD4 T-Cell Count (cells/μL):**
    - Primary marker of HIV-related immunodeficiency
    - Lower counts indicate more advanced HIV disease
    - Values <200 cells/μL indicate AIDS-defining immunodeficiency
    - Normal range: 500-1200 cells/μL in HIV-uninfected individuals
    
    **HIV-1 RNA Viral Load (log10 copies/mL):**
    - Measure of viral replication and treatment effectiveness
    - Undetectable: <1.3 log10 copies/mL (goal of antiretroviral therapy)
    - Detectable viral load indicates ongoing HIV replication
    - Higher viral loads associated with faster disease progression
    
    **Laboratory Parameters:**
    
    **Hemoglobin (g/dL):**
    - Marker of anemia and overall health status
    - Lower values increase mortality risk in HIV patients
    - Normal ranges: Men 13.8-17.2 g/dL, Women 12.1-15.1 g/dL
    - HIV-related anemia may indicate disease progression or medication effects
    
    **Liver Function Parameters (for FIB-4 calculation):**
    - **AST (Aspartate Aminotransferase)**: Liver enzyme, elevated in liver injury
    - **ALT (Alanine Aminotransferase)**: More liver-specific enzyme
    - **Platelets**: Reduced in liver disease and portal hypertension
    - **FIB-4 Formula**: (Age × AST) / (Platelets × √ALT)
    - **FIB-4 Interpretation**: <1.45 low risk, 1.45-3.25 intermediate, >3.25 high risk for fibrosis
    
    **Kidney Function:**
    - **Serum Creatinine**: Waste product filtered by kidneys
    - **eGFR Calculation**: CKD-EPI equation incorporating age, sex, race, creatinine
    - **eGFR Categories**: ≥90 normal, 60-89 mild decrease, 30-59 moderate decrease, <30 severe
    
    **Charlson Comorbidity Components:**
    
    **Weight 1 Conditions (1 point each):**
    - **Myocardial Infarction**: History of heart attack
    - **Congestive Heart Failure**: Heart failure diagnosis or symptoms
    - **Peripheral Vascular Disease**: Claudication, bypass, gangrene, acute arterial insufficiency
    - **Cerebrovascular Disease**: Stroke, TIA, or carotid endarterectomy
    - **Dementia**: Chronic cognitive disorder
    - **Chronic Pulmonary Disease**: COPD, asthma, bronchiectasis, pulmonary fibrosis
    - **Rheumatic Disease**: SLE, polymyositis, mixed connective tissue disease, polymyalgia rheumatica
    - **Peptic Ulcer Disease**: History of peptic, gastric, or duodenal ulcer
    - **Mild Liver Disease**: Chronic hepatitis, cirrhosis without portal hypertension
    - **Diabetes**: Diabetes mellitus without complications
    
    **Weight 2 Conditions (2 points each):**
    - **Diabetes with Complications**: Retinopathy, neuropathy, nephropathy, or ketoacidosis
    - **Hemiplegia**: Paraplegia or hemiplegia from any cause
    - **Renal Disease**: Moderate to severe chronic kidney disease, dialysis, transplant
    - **Any Malignancy**: Leukemia, lymphoma, solid organ tumors
    
    **Weight 3 Conditions (3 points each):**
    - **Moderate/Severe Liver Disease**: Portal hypertension, varices, ascites, encephalopathy
    
    **Weight 6 Conditions (6 points each):**
    - **Metastatic Solid Tumor**: Documented metastases from solid organ cancer
    - **AIDS**: AIDS-defining illness diagnosis
    
    **SCORE INTERPRETATION:**
    
    **Score Range**: 0-100% mortality risk
    **Risk Categories**:
    - **0-25%**: Low risk - routine care appropriate
    - **26-50%**: Moderate risk - enhanced monitoring recommended
    - **51-75%**: High risk - intensive management needed
    - **76-100%**: Very high risk - maximum interventions required
    
    **CLINICAL APPLICATIONS:**
    
    **Risk Stratification:**
    - Identify patients at highest mortality risk for intensive interventions
    - Guide frequency of monitoring and preventive care
    - Prioritize resources for high-risk patients
    
    **Treatment Planning:**
    - Inform discussions about treatment intensity and goals
    - Guide timing of interventions for comorbid conditions
    - Support shared decision-making with patients and families
    
    **Prognosis Communication:**
    - Structured approach to discussing life expectancy
    - Evidence-based framework for advance care planning
    - Support for end-of-life discussions when appropriate
    
    **Quality Improvement:**
    - Standardized mortality risk assessment across providers
    - Population health management and quality metrics
    - Research tool for clinical trials and outcomes studies
    
    **IMPORTANT CONSIDERATIONS:**
    
    **Clinical Context:**
    - Should complement, not replace, clinical judgment
    - Consider individual patient factors not captured in the index
    - Regular reassessment as clinical status and comorbidities change
    
    **Modifiable Risk Factors:**
    - HIV viral suppression through optimal antiretroviral therapy
    - Management of individual Charlson comorbidities
    - Preventive care and lifestyle interventions
    - Treatment of substance use disorders
    
    **Limitations:**
    - Developed primarily in male veteran populations
    - May not fully capture all mortality determinants in diverse populations
    - Requires accurate clinical history and current laboratory values
    - Static snapshot that may not reflect dynamic changes over time
    
    References (Vancouver style):
    1. Justice AC, Lasky E, McGinnis KA, et al. Med Care. 2006;44(4):S52-60.
    2. Tate JP, Justice AC, Hughes MD, et al. AIDS. 2013;27(4):563-72.
    3. Charlson ME, Pompei P, Ales KL, MacKenzie CR. J Chronic Dis. 1987;40(5):373-83.
    """
    
    age: int = Field(
        ...,
        description="Patient age in years (most influential factor in mortality prediction, used in both VACS scoring and FIB-4 calculation)",
        ge=18,
        le=100,
        example=55
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient sex for accurate eGFR calculation using CKD-EPI equation. Different creatinine thresholds and coefficients used for males vs females",
        example="male"
    )
    
    race: Literal["black", "non_black"] = Field(
        ...,
        description="Patient race for eGFR calculation. Black patients have 15.9% higher eGFR for same creatinine level per CKD-EPI equation",
        example="non_black"
    )
    
    cd4_count: int = Field(
        ...,
        description="CD4 T-cell count in cells/μL. Primary marker of HIV-related immunodeficiency. <200 cells/μL indicates AIDS-defining immunodeficiency. Normal range 500-1200 cells/μL",
        ge=0,
        le=2000,
        example=250
    )
    
    hiv_rna_log: float = Field(
        ...,
        description="HIV-1 RNA viral load in log10 copies/mL. Measures viral replication and treatment effectiveness. <1.3 log10 = undetectable (goal of therapy). Higher levels indicate disease progression",
        ge=0.0,
        le=7.0,
        example=2.5
    )
    
    hemoglobin: float = Field(
        ...,
        description="Hemoglobin level in g/dL. Marker of anemia and overall health. Lower values increase mortality risk. Normal: Men 13.8-17.2, Women 12.1-15.1 g/dL",
        ge=5.0,
        le=20.0,
        example=11.5
    )
    
    platelets: int = Field(
        ...,
        description="Platelet count in ×10³/μL. Used in FIB-4 calculation for liver fibrosis assessment. Low platelets may indicate liver disease or portal hypertension. Normal: 150-450 ×10³/μL",
        ge=10,
        le=1000,
        example=180
    )
    
    ast: int = Field(
        ...,
        description="Aspartate aminotransferase in U/L. Liver enzyme used in FIB-4 calculation. Elevated levels indicate liver injury. Normal: 10-40 U/L",
        ge=10,
        le=500,
        example=45
    )
    
    alt: int = Field(
        ...,
        description="Alanine aminotransferase in U/L. More liver-specific enzyme used in FIB-4 calculation. Elevated levels suggest hepatocellular injury. Normal: 7-56 U/L",
        ge=10,
        le=500,
        example=35
    )
    
    creatinine: float = Field(
        ...,
        description="Serum creatinine in mg/dL. Kidney function marker used for eGFR calculation. Higher values indicate reduced kidney function. Normal: Men 0.74-1.35, Women 0.59-1.04 mg/dL",
        ge=0.5,
        le=10.0,
        example=1.2
    )
    
    hepatitis_c: Literal["yes", "no"] = Field(
        ...,
        description="Hepatitis C virus co-infection status. Significant comorbidity that accelerates liver disease progression and increases mortality risk in HIV patients",
        example="yes"
    )
    
    # Charlson Comorbidity Index Components (Weight 1)
    myocardial_infarction: Literal["yes", "no"] = Field(
        ...,
        description="History of myocardial infarction (heart attack). Charlson weight: 1 point. Includes documented MI on ECG, enzyme evidence, or clinical diagnosis",
        example="no"
    )
    
    congestive_heart_failure: Literal["yes", "no"] = Field(
        ...,
        description="History of congestive heart failure. Charlson weight: 1 point. Includes systolic or diastolic dysfunction, clinical heart failure symptoms, or heart failure medications",
        example="no"
    )
    
    peripheral_vascular_disease: Literal["yes", "no"] = Field(
        ...,
        description="History of peripheral vascular disease. Charlson weight: 1 point. Includes claudication, bypass surgery, gangrene, or acute arterial insufficiency",
        example="no"
    )
    
    cerebrovascular_disease: Literal["yes", "no"] = Field(
        ...,
        description="History of cerebrovascular disease. Charlson weight: 1 point. Includes stroke, transient ischemic attack (TIA), or carotid endarterectomy",
        example="no"
    )
    
    dementia: Literal["yes", "no"] = Field(
        ...,
        description="History of dementia. Charlson weight: 1 point. Includes Alzheimer's disease, vascular dementia, or other chronic cognitive disorders",
        example="no"
    )
    
    chronic_pulmonary_disease: Literal["yes", "no"] = Field(
        ...,
        description="History of chronic pulmonary disease. Charlson weight: 1 point. Includes COPD, asthma, bronchiectasis, or pulmonary fibrosis",
        example="no"
    )
    
    rheumatic_disease: Literal["yes", "no"] = Field(
        ...,
        description="History of rheumatic disease. Charlson weight: 1 point. Includes SLE, polymyositis, mixed connective tissue disease, polymyalgia rheumatica",
        example="no"
    )
    
    peptic_ulcer_disease: Literal["yes", "no"] = Field(
        ...,
        description="History of peptic ulcer disease. Charlson weight: 1 point. Includes peptic, gastric, or duodenal ulcer requiring treatment",
        example="no"
    )
    
    mild_liver_disease: Literal["yes", "no"] = Field(
        ...,
        description="History of mild liver disease. Charlson weight: 1 point. Includes chronic hepatitis or cirrhosis without portal hypertension",
        example="no"
    )
    
    diabetes: Literal["yes", "no"] = Field(
        ...,
        description="History of diabetes mellitus without complications. Charlson weight: 1 point. Includes type 1 or type 2 diabetes managed with diet, oral agents, or insulin without organ damage",
        example="no"
    )
    
    # Charlson Comorbidity Index Components (Weight 2)
    diabetes_complications: Literal["yes", "no"] = Field(
        ...,
        description="History of diabetes with complications. Charlson weight: 2 points. Includes retinopathy, neuropathy, nephropathy, or history of ketoacidosis",
        example="no"
    )
    
    hemiplegia: Literal["yes", "no"] = Field(
        ...,
        description="History of hemiplegia or paraplegia. Charlson weight: 2 points. Includes paralysis from any cause affecting limbs",
        example="no"
    )
    
    renal_disease: Literal["yes", "no"] = Field(
        ...,
        description="History of moderate to severe renal disease. Charlson weight: 2 points. Includes chronic kidney disease stage 3-5, dialysis, or kidney transplant",
        example="no"
    )
    
    any_malignancy: Literal["yes", "no"] = Field(
        ...,
        description="History of any malignancy. Charlson weight: 2 points. Includes leukemia, lymphoma, and solid organ tumors (excludes skin cancer)",
        example="no"
    )
    
    # Charlson Comorbidity Index Components (Weight 3)
    moderate_severe_liver_disease: Literal["yes", "no"] = Field(
        ...,
        description="History of moderate to severe liver disease. Charlson weight: 3 points. Includes portal hypertension, varices, ascites, or encephalopathy",
        example="no"
    )
    
    # Charlson Comorbidity Index Components (Weight 6)
    metastatic_solid_tumor: Literal["yes", "no"] = Field(
        ...,
        description="History of metastatic solid tumor. Charlson weight: 6 points. Includes documented metastases from any solid organ cancer",
        example="no"
    )
    
    aids: Literal["yes", "no"] = Field(
        ...,
        description="AIDS diagnosis. Charlson weight: 6 points. Includes any AIDS-defining illness or clinical AIDS diagnosis",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 55,
                "sex": "male",
                "race": "non_black",
                "cd4_count": 250,
                "hiv_rna_log": 2.5,
                "hemoglobin": 11.5,
                "platelets": 180,
                "ast": 45,
                "alt": 35,
                "creatinine": 1.2,
                "hepatitis_c": "yes",
                "myocardial_infarction": "no",
                "congestive_heart_failure": "no",
                "peripheral_vascular_disease": "no",
                "cerebrovascular_disease": "no",
                "dementia": "no",
                "chronic_pulmonary_disease": "no",
                "rheumatic_disease": "no",
                "peptic_ulcer_disease": "no",
                "mild_liver_disease": "no",
                "diabetes": "no",
                "diabetes_complications": "no",
                "hemiplegia": "no",
                "renal_disease": "no",
                "any_malignancy": "no",
                "moderate_severe_liver_disease": "no",
                "metastatic_solid_tumor": "no",
                "aids": "yes"
            }
        }


class VacsCciResponse(BaseModel):
    """
    Response model for Veterans Aging Cohort Study-Charlson Comorbidity Index (VACS-CCI)
    
    The VACS-CCI provides enhanced mortality risk prediction by combining HIV-specific 
    biomarkers with comprehensive comorbidity assessment. The response includes the 
    percentage mortality risk, detailed component scoring breakdown, and clinical 
    interpretation with management recommendations.
    
    **SCORE INTERPRETATION:**
    
    **Total Score Range:** 0-100% (5-year all-cause mortality risk)
    **Risk Categories:**
    - **Low Risk (0-25%):** Excellent prognosis, routine care appropriate
    - **Moderate Risk (26-50%):** Enhanced monitoring and preventive care recommended
    - **High Risk (51-75%):** Intensive management and multidisciplinary care needed
    - **Very High Risk (76-100%):** Maximum interventions and palliative care consideration
    
    **COMPONENT BREAKDOWN:**
    
    **VACS Score Components:**
    - Incorporates HIV-specific markers (CD4, viral load)
    - Includes organ system injury markers (hemoglobin, FIB-4, eGFR)
    - Accounts for age and hepatitis C co-infection
    
    **Charlson Score Components:**
    - Weighted assessment of non-HIV comorbidities
    - Higher weights for more severe conditions
    - Comprehensive coverage of major organ systems
    
    **Composite Biomarkers:**
    - **FIB-4**: Liver fibrosis assessment using age, AST, ALT, platelets
    - **eGFR**: Kidney function using CKD-EPI equation with demographics
    
    **CLINICAL UTILITY:**
    
    **Risk Stratification:**
    - Identifies patients requiring intensive monitoring and intervention
    - Guides resource allocation and care planning
    - Supports population health management
    
    **Treatment Decisions:**
    - Informs discussions about treatment intensity and goals
    - Guides timing of interventions for comorbid conditions
    - Supports shared decision-making processes
    
    **Prognosis Communication:**
    - Evidence-based framework for life expectancy discussions
    - Structured approach to advance care planning
    - Support for end-of-life conversations when appropriate
    
    **IMPORTANT CLINICAL CONSIDERATIONS:**
    
    **Dynamic Assessment:**
    - Score should be recalculated with updated clinical data
    - Treatment responses can significantly improve risk over time
    - Regular monitoring allows tracking of disease progression or improvement
    
    **Modifiable Risk Factors:**
    - HIV viral suppression through optimal antiretroviral therapy
    - Treatment of hepatitis C co-infection
    - Management of individual Charlson comorbidities
    - Preventive care and lifestyle interventions
    
    **Individual Context:**
    - Consider patient goals, preferences, and values
    - Account for social determinants of health
    - Use in conjunction with comprehensive clinical assessment
    - Recognize limitations in diverse populations
    
    Reference: Justice AC, et al. Med Care. 2006;44(4):S52-60.
    """
    
    result: float = Field(
        ...,
        description="VACS-CCI mortality risk score as percentage (0-100% 5-year all-cause mortality risk)",
        example=45.2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="percentage"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk stratification and management recommendations based on mortality risk percentage",
        example="VACS-CCI score: 45.2%. Moderate 5-year mortality risk. Enhanced monitoring and proactive management of comorbidities recommended. Consider intensified preventive interventions and specialist consultations."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Low Risk, Moderate Risk, High Risk, Very High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the mortality risk category",
        example="Moderate mortality risk"
    )
    
    component_scores: Dict[str, float] = Field(
        ...,
        description="Breakdown of score contributions from VACS components, Charlson components, and linear predictor",
        example={
            "vacs_score": 12.5,
            "charlson_score": 7.0,
            "linear_predictor": 19.5
        }
    )
    
    composite_biomarkers: Dict[str, float] = Field(
        ...,
        description="Calculated composite biomarkers: FIB-4 for liver fibrosis assessment and eGFR for kidney function",
        example={
            "fib4": 2.8,
            "egfr": 75.2
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 45.2,
                "unit": "percentage",
                "interpretation": "VACS-CCI score: 45.2%. Moderate 5-year mortality risk. Enhanced monitoring and proactive management of comorbidities recommended. Consider intensified preventive interventions and specialist consultations.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate mortality risk",
                "component_scores": {
                    "vacs_score": 12.5,
                    "charlson_score": 7.0,
                    "linear_predictor": 19.5
                },
                "composite_biomarkers": {
                    "fib4": 2.8,
                    "egfr": 75.2
                }
            }
        }