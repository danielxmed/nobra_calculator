"""
Veterans Aging Cohort Study (VACS) 2.0 Index Models

Request and response models for VACS 2.0 Index calculation.

References (Vancouver style):
1. Justice AC, McGinnis KA, Skanderson M, Chang CC, Gibert CL, Goetz MB, et al. 
   Towards a combined prognostic index for survival in HIV infection: the role of 
   'non-HIV' biomarkers. HIV Med. 2010 Feb;11(2):143-51. doi: 10.1111/j.1468-1293.2009.00757.x.
2. Tate JP, Justice AC, Hughes MD, Bonnet F, Reiss P, Mocroft A, et al. An internationally 
   generalizable risk index for mortality after one year of antiretroviral therapy. 
   AIDS. 2013 Feb 20;27(4):563-72. doi: 10.1097/QAD.0b013e32835c5b67.
3. Justice AC, Erlandson KM, Hunt PW, Gibert CL, Goetz MB, Petersen M, et al. Development 
   and validation of a prognostic index for 1-year mortality in HIV-infected adults. 
   Med Care. 2013 Dec;51(12):1054-64. doi: 10.1097/MLR.0000000000000020.
4. Rodriguez-Barradas MC, Tate JP, Justice AC, Gibert CL, Goetz MB, Bryant KJ, et al. 
   Albumin, white blood cell count, and body mass index improve discrimination of mortality 
   in HIV-positive individuals. AIDS. 2019 Apr 24;33(6):903-912. doi: 10.1097/QAD.0000000000002140.

The Veterans Aging Cohort Study (VACS) 2.0 Index is an improved prognostic tool that 
estimates 5-year all-cause mortality risk in patients with HIV. Building upon the original 
VACS Index, version 2.0 incorporates additional biomarkers (albumin, white blood cell count, 
and body mass index) for enhanced discrimination of mortality risk across diverse patient 
populations. The index combines HIV-specific indicators (CD4 count, viral load) with general 
health biomarkers and composite measures of organ system injury (FIB-4 for liver function, 
eGFR for kidney function) to provide comprehensive risk assessment.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class Vacs20IndexRequest(BaseModel):
    """
    Request model for Veterans Aging Cohort Study (VACS) 2.0 Index
    
    The VACS 2.0 Index is a validated prognostic tool that estimates 5-year all-cause 
    mortality risk in patients with HIV by combining HIV-specific biomarkers with general 
    health indicators and composite measures of organ system injury.
    
    **SCIENTIFIC BACKGROUND:**
    
    The VACS Index was developed through analysis of the Veterans Aging Cohort Study, 
    one of the largest observational cohorts of HIV-infected individuals. Version 2.0 
    represents an enhancement of the original index with improved discrimination and 
    generalizability across diverse populations.
    
    **KEY IMPROVEMENTS IN VERSION 2.0:**
    
    **Enhanced Biomarkers:**
    - **Albumin**: Marker of nutritional status, inflammation, and liver synthesis
    - **White Blood Cell Count**: Indicator of immune activation and inflammation
    - **Body Mass Index**: Nutritional and metabolic health indicator
    
    **CALCULATION COMPONENTS:**
    
    **1. Age:**
    - Single most influential factor in mortality prediction
    - Progressive risk increase with advancing age
    - Age 30 years: ~32 points, Age 75 years: ~59 points
    
    **2. HIV-Specific Biomarkers:**
    
    **CD4 T-Cell Count (cells/μL):**
    - Primary marker of immune system function in HIV
    - Lower counts indicate more advanced immunodeficiency
    - Range: 10-900 cells/μL contributes ~23 points to total score
    - Values <200 cells/μL indicate AIDS-defining immunodeficiency
    
    **HIV-1 RNA Viral Load (log10 copies/mL):**
    - Measure of viral replication and treatment effectiveness
    - Detectable viral load indicates ongoing HIV replication
    - Range: 1.3-5.0 log10 copies/mL contributes ~18 points
    - Undetectable: <1.3 log10 copies/mL (goal of antiretroviral therapy)
    
    **3. Organ System Injury Biomarkers:**
    
    **Hemoglobin (g/dL):**
    - Marker of anemia and overall health status
    - Lower values indicate anemia, which increases mortality risk
    - Range: 9-16 g/dL contributes ~16 points to score
    - Normal ranges: Men 13.8-17.2 g/dL, Women 12.1-15.1 g/dL
    
    **Liver Function (AST, ALT, Platelets for FIB-4):**
    - **AST (Aspartate Aminotransferase)**: Liver enzyme, elevated in liver injury
    - **ALT (Alanine Aminotransferase)**: More specific liver enzyme
    - **Platelets**: Reduced in liver disease and portal hypertension
    - **FIB-4 Calculation**: (Age × AST) / (Platelets × √ALT)
    - FIB-4 range: 0.5-7.5 contributes ~20 points to total score
    - FIB-4 >3.25 suggests significant liver fibrosis
    
    **Kidney Function (Creatinine for eGFR):**
    - **Serum Creatinine**: Waste product filtered by kidneys
    - **eGFR Calculation**: Using CKD-EPI equation incorporating age, sex, race
    - eGFR range: 0-180 mL/min/1.73m² contributes ~16 points
    - eGFR <60 mL/min/1.73m² indicates chronic kidney disease
    
    **4. Additional Health Indicators:**
    
    **Albumin (g/dL):**
    - Second most influential factor after age
    - Marker of nutritional status, liver synthesis, and inflammation
    - Range: 2.0-5.0 g/dL contributes ~26 points (second highest range)
    - Low albumin (<3.5 g/dL) indicates malnutrition or liver dysfunction
    
    **White Blood Cell Count (×10³/μL):**
    - Indicator of immune activation and systemic inflammation
    - Elevated WBC may indicate ongoing immune activation in HIV
    - Normal range: 4.0-11.0 ×10³/μL
    
    **Body Mass Index (kg/m²):**
    - Nutritional and metabolic health indicator
    - Range: 15-35 kg/m² contributes ~20 points to score
    - BMI <18.5 kg/m² indicates underweight (higher mortality risk)
    - BMI 18.5-24.9 kg/m² considered normal weight
    
    **5. Co-infections:**
    
    **Hepatitis C Virus (HCV) Co-infection:**
    - Significant comorbidity in HIV-infected individuals
    - Adds 6 points to total score if present
    - Accelerates liver disease progression and increases mortality
    
    **SCORE INTERPRETATION:**
    
    **Score Range**: 0-164 points (theoretical maximum)
    **Typical Range**: 80% of patients score 0-50 points
    **Risk Relationship**: Mortality risk approximately doubles for every 10-unit increase
    
    **Risk Categories:**
    - **0-25 points**: Low risk, routine care and monitoring
    - **26-50 points**: Moderate risk, enhanced monitoring recommended
    - **51-75 points**: High risk, intensive management needed
    - **76+ points**: Very high risk, aggressive interventions required
    
    **CLINICAL APPLICATIONS:**
    
    **Risk Stratification:**
    - Identify patients at highest risk for mortality
    - Guide intensity of monitoring and interventions
    - Inform prognosis discussions with patients
    
    **Treatment Planning:**
    - Prioritize aggressive HIV treatment in high-risk patients
    - Guide timing of interventions for comorbid conditions
    - Identify candidates for enhanced preventive care
    
    **Research and Quality Improvement:**
    - Standardized mortality risk assessment tool
    - Outcome prediction for clinical trials
    - Quality metrics for HIV care programs
    
    **VALIDATION AND PERFORMANCE:**
    
    **International Validation:**
    - Validated across multiple international HIV cohorts
    - Demonstrates consistent performance in diverse populations
    - Superior discrimination compared to CD4/viral load alone
    
    **Discrimination Performance:**
    - C-statistic of 0.83 for 5-year all-cause mortality
    - Highest discrimination for AIDS-related deaths (0.91)
    - Good performance for liver-related (0.91) and respiratory deaths (0.89)
    
    **IMPORTANT CONSIDERATIONS:**
    
    **Clinical Context:**
    - Should complement, not replace, clinical judgment
    - Consider individual patient factors not captured in the index
    - Regular reassessment as clinical status changes
    
    **Limitations:**
    - Developed primarily in male veteran populations
    - May not fully capture all mortality determinants
    - Requires regular laboratory monitoring for accuracy
    
    **Updates from VACS 1.0:**
    - Improved discrimination across patient subgroups
    - Enhanced generalizability to non-veteran populations
    - Better calibration for mortality prediction
    
    References (Vancouver style):
    1. Justice AC, McGinnis KA, Skanderson M, et al. HIV Med. 2010;11(2):143-51.
    2. Tate JP, Justice AC, Hughes MD, et al. AIDS. 2013;27(4):563-72.
    3. Rodriguez-Barradas MC, Tate JP, Justice AC, et al. AIDS. 2019;33(6):903-912.
    """
    
    age: int = Field(
        ...,
        description="Patient age in years (most influential factor, contributes 27-point range to score)",
        ge=18,
        le=100,
        example=45
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient sex for accurate eGFR calculation using CKD-EPI equation",
        example="male"
    )
    
    race: Literal["black", "non_black"] = Field(
        ...,
        description="Patient race for eGFR calculation. Black race multiplier (1.159) applied per CKD-EPI equation",
        example="non_black"
    )
    
    cd4_count: int = Field(
        ...,
        description="CD4 T-cell count in cells/μL. Primary marker of HIV-related immunodeficiency. <200 cells/μL indicates AIDS-defining immunodeficiency. Range 10-900 contributes ~23 points to score",
        ge=0,
        le=2000,
        example=350
    )
    
    hiv_rna_log: float = Field(
        ...,
        description="HIV-1 RNA viral load in log10 copies/mL. Measures viral replication and treatment effectiveness. <1.3 log10 = undetectable (goal of therapy). Range 1.3-5.0 contributes ~18 points to score",
        ge=0.0,
        le=7.0,
        example=1.5
    )
    
    hemoglobin: float = Field(
        ...,
        description="Hemoglobin level in g/dL. Marker of anemia and overall health. Lower values increase mortality risk. Normal: Men 13.8-17.2, Women 12.1-15.1 g/dL. Range 9-16 contributes ~16 points",
        ge=5.0,
        le=20.0,
        example=13.5
    )
    
    platelets: int = Field(
        ...,
        description="Platelet count in ×10³/μL. Used in FIB-4 calculation for liver fibrosis assessment. Low platelets may indicate liver disease, portal hypertension, or bone marrow suppression. Normal: 150-450 ×10³/μL",
        ge=10,
        le=1000,
        example=250
    )
    
    ast: int = Field(
        ...,
        description="Aspartate aminotransferase in U/L. Liver enzyme used in FIB-4 calculation. Elevated levels indicate liver injury. Normal: 10-40 U/L. Used with ALT, platelets, and age to calculate liver fibrosis risk",
        ge=10,
        le=500,
        example=35
    )
    
    alt: int = Field(
        ...,
        description="Alanine aminotransferase in U/L. More liver-specific enzyme used in FIB-4 calculation. Elevated levels suggest hepatocellular injury. Normal: 7-56 U/L. Combined with AST, platelets, age for FIB-4",
        ge=10,
        le=500,
        example=30
    )
    
    creatinine: float = Field(
        ...,
        description="Serum creatinine in mg/dL. Kidney function marker used for eGFR calculation. Higher values indicate reduced kidney function. Normal: Men 0.74-1.35, Women 0.59-1.04 mg/dL",
        ge=0.5,
        le=10.0,
        example=1.0
    )
    
    albumin: float = Field(
        ...,
        description="Serum albumin in g/dL. Second most influential factor (26-point range). Marker of nutritional status, liver synthesis, and inflammation. Low levels (<3.5 g/dL) indicate malnutrition or liver dysfunction. Normal: 3.4-5.4 g/dL",
        ge=1.0,
        le=6.0,
        example=4.0
    )
    
    wbc_count: float = Field(
        ...,
        description="White blood cell count in ×10³/μL. Indicator of immune activation and systemic inflammation. Elevated WBC may suggest ongoing immune activation in HIV patients. Normal: 4.0-11.0 ×10³/μL",
        ge=1.0,
        le=50.0,
        example=6.5
    )
    
    bmi: float = Field(
        ...,
        description="Body mass index in kg/m². Nutritional and metabolic health indicator. Range 15-35 contributes ~20 points. <18.5 underweight, 18.5-24.9 normal, 25-29.9 overweight, ≥30 obese",
        ge=10.0,
        le=50.0,
        example=24.5
    )
    
    hepatitis_c: Literal["yes", "no"] = Field(
        ...,
        description="Hepatitis C virus co-infection status. Significant comorbidity that accelerates liver disease progression. Adds 6 points to total score if present. Least influential single factor in index",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 45,
                "sex": "male",
                "race": "non_black",
                "cd4_count": 350,
                "hiv_rna_log": 1.5,
                "hemoglobin": 13.5,
                "platelets": 250,
                "ast": 35,
                "alt": 30,
                "creatinine": 1.0,
                "albumin": 4.0,
                "wbc_count": 6.5,
                "bmi": 24.5,
                "hepatitis_c": "no"
            }
        }


class Vacs20IndexResponse(BaseModel):
    """
    Response model for Veterans Aging Cohort Study (VACS) 2.0 Index
    
    The VACS 2.0 Index provides a comprehensive mortality risk assessment for HIV-infected 
    individuals by combining multiple clinical and laboratory parameters into a single 
    prognostic score. The response includes the total score, risk stratification, component 
    scores, and clinical interpretation.
    
    **SCORE INTERPRETATION:**
    
    **Total Score Range:** 0-164 points (theoretical maximum)
    **Typical Patient Range:** 80% of patients score 0-50 points
    **Risk Relationship:** Mortality risk approximately doubles for every 10-unit increase
    
    **Risk Categories:**
    - **Low Risk (0-25 points):** Excellent prognosis, routine care appropriate
    - **Moderate Risk (26-50 points):** Enhanced monitoring and preventive care recommended
    - **High Risk (51-75 points):** Intensive management and multidisciplinary care needed
    - **Very High Risk (76+ points):** Aggressive interventions and end-of-life planning consideration
    
    **COMPONENT SCORE CONTRIBUTIONS:**
    
    **Major Contributors (Highest Impact):**
    - **Age**: 27-point range (Age 30: ~32 pts, Age 75: ~59 pts)
    - **Albumin**: 26-point range (2.0 g/dL: ~65 pts, 5.0 g/dL: ~39 pts)
    
    **Moderate Contributors:**
    - **CD4 Count**: ~23-point range (Lower CD4 = higher points)
    - **FIB-4 Score**: ~20-point range (Higher FIB-4 = higher points)
    - **BMI**: ~20-point range (Lower BMI = higher risk in HIV)
    - **HIV RNA**: ~18-point range (Higher viral load = higher points)
    
    **Minor Contributors:**
    - **Hemoglobin**: ~16-point range (Lower Hgb = higher points)
    - **eGFR**: ~16-point range (Lower eGFR = higher points)
    - **WBC Count**: Variable contribution
    - **Hepatitis C**: 6 points if positive (lowest single contributor)
    
    **COMPOSITE BIOMARKERS:**
    
    **FIB-4 (Fibrosis-4 Index):**
    - Calculation: (Age × AST) / (Platelets × √ALT)
    - Interpretation: <1.45 low risk, 1.45-3.25 intermediate, >3.25 high risk for fibrosis
    - Validated marker of liver fibrosis in HIV/HCV co-infected patients
    
    **eGFR (Estimated Glomerular Filtration Rate):**
    - Calculation: CKD-EPI equation using creatinine, age, sex, race
    - Interpretation: ≥90 normal, 60-89 mild decrease, 30-59 moderate decrease, <30 severe decrease
    - Primary measure of kidney function
    
    **MORTALITY RISK ESTIMATION:**
    
    **Baseline Risk Model:**
    - Based on research showing VACS score of 38 = 1% 5-year mortality risk
    - Exponential relationship: risk doubles for every 10-unit score increase
    - Maximum estimated risk capped at 95%
    
    **Risk Factors by Score:**
    - Score 28: ~0.5% 5-year mortality
    - Score 38: ~1.0% 5-year mortality (baseline)
    - Score 48: ~2.0% 5-year mortality
    - Score 58: ~4.0% 5-year mortality
    - Score 68: ~8.0% 5-year mortality
    - Score 78: ~16.0% 5-year mortality
    
    **CLINICAL APPLICATIONS:**
    
    **Risk Stratification:**
    - Identify patients requiring intensive monitoring
    - Guide frequency of clinical visits and laboratory monitoring
    - Prioritize preventive interventions and comorbidity management
    
    **Treatment Decisions:**
    - Inform discussions about treatment intensity
    - Guide timing of interventions for age-related conditions
    - Support shared decision-making with patients
    
    **Prognosis Communication:**
    - Structured approach to discussing life expectancy
    - Evidence-based framework for end-of-life planning
    - Support for advance directive discussions
    
    **Quality Improvement:**
    - Standardized risk assessment across providers
    - Quality metrics for HIV care programs
    - Population health management tool
    
    **IMPORTANT CLINICAL CONSIDERATIONS:**
    
    **Dynamic Assessment:**
    - Score should be recalculated with updated laboratory values
    - Treatment responses can significantly improve scores over time
    - Regular monitoring allows tracking of disease progression or improvement
    
    **Modifiable Risk Factors:**
    - HIV viral suppression (optimize antiretroviral therapy)
    - Nutritional status improvement (albumin, BMI optimization)
    - Comorbidity management (liver disease, kidney disease treatment)
    - Substance use disorder treatment
    - Preventive care implementation
    
    **Individual Context:**
    - Consider patient goals and preferences
    - Account for factors not captured in the index
    - Use in conjunction with clinical judgment
    - Consider social determinants of health
    
    Reference: Rodriguez-Barradas MC, et al. AIDS. 2019;33(6):903-912.
    """
    
    result: float = Field(
        ...,
        description="Total VACS 2.0 Index score in points (range 0-164, typical range 0-50 for 80% of patients)",
        example=32.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk stratification and management recommendations based on total score",
        example="VACS 2.0 Index score: 32.5 points. Moderate disease burden. Consider enhanced monitoring and preventive interventions. Optimize HIV therapy and address modifiable risk factors."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Low Risk, Moderate Risk, High Risk, Very High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Moderate 5-year mortality risk"
    )
    
    component_scores: Dict[str, float] = Field(
        ...,
        description="Breakdown of score contributions from each component parameter",
        example={
            "age_score": 14.0,
            "cd4_score": 8.5,
            "hiv_rna_score": 2.0,
            "hemoglobin_score": 1.5,
            "fib4_score": 2.0,
            "egfr_score": 1.0,
            "albumin_score": 2.0,
            "wbc_score": 0.5,
            "bmi_score": 1.0,
            "hcv_score": 0.0
        }
    )
    
    composite_biomarkers: Dict[str, float] = Field(
        ...,
        description="Calculated composite biomarkers used in scoring (FIB-4 and eGFR)",
        example={
            "fib4": 1.25,
            "egfr": 95.0
        }
    )
    
    mortality_risk_5year: str = Field(
        ...,
        description="Estimated 5-year all-cause mortality risk based on VACS 2.0 score",
        example="Approximately 1.8% 5-year mortality risk"
    )
    
    clinical_recommendations: Dict[str, Any] = Field(
        ...,
        description="Detailed clinical management recommendations based on risk stratification",
        example={
            "monitoring_frequency": "Enhanced monitoring recommended",
            "interventions": [
                "Optimize antiretroviral therapy for viral suppression",
                "Address modifiable risk factors (nutrition, substance use)",
                "Implement age-appropriate preventive care",
                "Monitor for treatment-related complications"
            ],
            "follow_up": [
                "Reassess VACS score every 6-12 months",
                "Monitor CD4 count and viral load every 3-6 months",
                "Annual comprehensive metabolic panel and liver function tests",
                "Consider specialist referrals for significant comorbidities"
            ],
            "counseling_points": [
                "Discuss importance of medication adherence",
                "Review lifestyle modifications for risk reduction",
                "Provide education on HIV progression and prognosis",
                "Address any concerns about life expectancy"
            ]
        }
    )
    
    important_considerations: Dict[str, Any] = Field(
        ...,
        description="Critical information about score interpretation and limitations",
        example={
            "validation": "Validated across international HIV cohorts with C-statistic of 0.83",
            "updates": "Version 2.0 represents improvement over original VACS Index",
            "limitations": [
                "Developed primarily in male veteran populations",
                "Requires regular laboratory monitoring for accuracy",
                "Should complement clinical judgment, not replace comprehensive evaluation"
            ],
            "modifiable_factors": [
                "HIV viral suppression through optimal antiretroviral therapy",
                "Nutritional status improvement (albumin, BMI)",
                "Hepatitis C treatment if co-infected",
                "Management of kidney and liver disease"
            ],
            "reassessment": "Score should be recalculated with updated laboratory values to track disease progression or improvement over time"
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 32.5,
                "unit": "points",
                "interpretation": "VACS 2.0 Index score: 32.5 points. Moderate disease burden. Consider enhanced monitoring and preventive interventions. Optimize HIV therapy and address modifiable risk factors.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate 5-year mortality risk",
                "component_scores": {
                    "age_score": 14.0,
                    "cd4_score": 8.5,
                    "hiv_rna_score": 2.0,
                    "hemoglobin_score": 1.5,
                    "fib4_score": 2.0,
                    "egfr_score": 1.0,
                    "albumin_score": 2.0,
                    "wbc_score": 0.5,
                    "bmi_score": 1.0,
                    "hcv_score": 0.0
                },
                "composite_biomarkers": {
                    "fib4": 1.25,
                    "egfr": 95.0
                },
                "mortality_risk_5year": "Approximately 1.8% 5-year mortality risk",
                "clinical_recommendations": {
                    "monitoring_frequency": "Enhanced monitoring recommended",
                    "interventions": [
                        "Optimize antiretroviral therapy for viral suppression",
                        "Address modifiable risk factors (nutrition, substance use)",
                        "Implement age-appropriate preventive care",
                        "Monitor for treatment-related complications"
                    ],
                    "follow_up": [
                        "Reassess VACS score every 6-12 months",
                        "Monitor CD4 count and viral load every 3-6 months",
                        "Annual comprehensive metabolic panel and liver function tests",
                        "Consider specialist referrals for significant comorbidities"
                    ],
                    "counseling_points": [
                        "Discuss importance of medication adherence",
                        "Review lifestyle modifications for risk reduction",
                        "Provide education on HIV progression and prognosis",
                        "Address any concerns about life expectancy"
                    ]
                },
                "important_considerations": {
                    "validation": "Validated across international HIV cohorts with C-statistic of 0.83",
                    "updates": "Version 2.0 represents improvement over original VACS Index",
                    "limitations": [
                        "Developed primarily in male veteran populations",
                        "Requires regular laboratory monitoring for accuracy",
                        "Should complement clinical judgment, not replace comprehensive evaluation"
                    ],
                    "modifiable_factors": [
                        "HIV viral suppression through optimal antiretroviral therapy",
                        "Nutritional status improvement (albumin, BMI)",
                        "Hepatitis C treatment if co-infected",
                        "Management of kidney and liver disease"
                    ],
                    "reassessment": "Score should be recalculated with updated laboratory values to track disease progression or improvement over time"
                }
            }
        }