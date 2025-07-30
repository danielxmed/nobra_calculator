"""
Charlson Comorbidity Index (CCI) Models

Request and response models for Charlson Comorbidity Index calculation.

References (Vancouver style):
1. Charlson ME, Pompei P, Ales KL, MacKenzie CR. A new method of classifying prognostic 
   comorbidity in longitudinal studies: development and validation. J Chronic Dis. 1987;40(5):373-83.
2. Charlson M, Szatrowski TP, Peterson J, Gold J. Validation of a combined comorbidity index. 
   J Clin Epidemiol. 1994;47(11):1245-51.
3. Deyo RA, Cherkin DC, Ciol MA. Adapting a clinical comorbidity index for use with ICD-9-CM 
   administrative databases. J Clin Epidemiol. 1992;45(6):613-9.

The Charlson Comorbidity Index (CCI) predicts 10-year mortality for patients with multiple 
comorbid conditions. Developed in 1987, it uses 19 weighted comorbidity categories plus age 
adjustment to provide evidence-based prognosis estimation for clinical decision-making.

CCI Scoring System:

Age Adjustment:
- <50 years: 0 points
- 50-59 years: 1 point  
- 60-69 years: 2 points
- 70-79 years: 3 points
- ≥80 years: 4 points (maximum)

Comorbidity Categories:

1-Point Conditions:
- Myocardial infarction
- Congestive heart failure
- Peripheral vascular disease
- Cerebrovascular disease (stroke/TIA)
- Dementia
- Chronic pulmonary disease (COPD)
- Connective tissue disease
- Peptic ulcer disease
- Mild liver disease
- Diabetes mellitus (uncomplicated)

2-Point Conditions:
- Hemiplegia or paraplegia
- Moderate to severe chronic kidney disease
- Diabetes with end-organ damage
- Localized solid tumor
- Leukemia
- Lymphoma

3-Point Condition:
- Moderate to severe liver disease

6-Point Conditions:
- Metastatic solid tumor
- AIDS

10-Year Survival Calculation:
The formula 10-year survival = 0.983^(CCI × 0.9) is used, assuming a theoretical low-risk 
population with 98.3% baseline 10-year survival.

Clinical Interpretation:
- Score 0-1: Excellent prognosis (>90% 10-year survival)
- Score 2-3: Good prognosis (70-90% 10-year survival)  
- Score 4-5: Moderate prognosis (30-70% 10-year survival)
- Score ≥6: Poor prognosis (<30% 10-year survival)

Clinical Applications:
- Treatment intensity decisions
- Screening program eligibility
- Resource allocation planning
- Prognostic counseling
- Clinical research stratification
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class CharlsonComorbidityIndexRequest(BaseModel):
    """
    Request model for Charlson Comorbidity Index (CCI)
    
    The CCI uses patient age plus 19 comorbidity categories to predict 10-year survival. 
    Each comorbidity is weighted based on its impact on mortality risk, providing a 
    comprehensive assessment of patient prognosis.
    
    Age Component:
    Age is adjusted in 10-year increments with increasing point values reflecting higher 
    mortality risk in older patients. The maximum age adjustment is 4 points for patients 
    ≥80 years old.
    
    Comorbidity Categories by Point Value:
    
    1-Point Conditions (Moderate Impact):
    
    Myocardial Infarction:
    - History of heart attack documented by ECG, enzymes, or imaging
    - Includes both ST-elevation and non-ST-elevation MI
    - Prior silent MI counts if documented
    
    Congestive Heart Failure:
    - Clinical syndrome of heart failure regardless of ejection fraction
    - Includes both systolic and diastolic heart failure
    - Must have clinical documentation or objective evidence
    
    Peripheral Vascular Disease:
    - Includes aortic aneurysm, peripheral arterial disease, claudication
    - Documented by imaging, physical exam, or ankle-brachial index
    - History of revascularization procedures counts
    
    Cerebrovascular Disease:
    - Stroke (ischemic or hemorrhagic) or transient ischemic attack
    - Must have neurological sequelae or documented imaging changes
    - Includes both completed stroke and TIA with residual deficits
    
    Dementia:
    - Chronic cognitive impairment affecting daily activities
    - Includes Alzheimer's disease, vascular dementia, other dementias
    - Must be clinically diagnosed, not just mild cognitive impairment
    
    Chronic Pulmonary Disease:
    - COPD, chronic bronchitis, emphysema, severe asthma
    - Requires chronic symptoms and/or objective testing abnormalities
    - Includes chronic oxygen dependence or chronic steroid use
    
    Connective Tissue Disease:
    - Systemic lupus erythematosus, rheumatoid arthritis, systemic sclerosis
    - Polymyositis, dermatomyositis, mixed connective tissue disease
    - Must have clinical diagnosis with systemic manifestations
    
    Peptic Ulcer Disease:
    - History of peptic or duodenal ulcer requiring treatment
    - Includes complications like bleeding or perforation
    - Current or prior H. pylori treatment counts
    
    2-Point Conditions (Significant Impact):
    
    Hemiplegia:
    - Paralysis of one side of body from stroke or other cause
    - Includes paraplegia from spinal cord injury
    - Must have persistent neurological deficit
    
    Moderate to Severe Chronic Kidney Disease:
    - Estimated GFR <60 mL/min/1.73m² or dialysis dependence
    - CKD stages 3-5 or end-stage renal disease
    - Includes kidney transplant recipients
    
    Localized Solid Tumor:
    - Cancer without evidence of metastasis
    - Includes tumors treated with curative intent
    - History of cancer in remission >5 years may not count
    
    Leukemia:
    - Acute or chronic leukemia of any type
    - Includes active treatment or remission phase
    - Both lymphocytic and myeloid leukemias
    
    Lymphoma:
    - Hodgkin's or non-Hodgkin's lymphoma
    - Includes active disease or treatment phase
    - Multiple myeloma typically included in this category
    
    Liver Disease Categories (Mutually Exclusive):
    
    Mild Liver Disease (1 Point):
    - Chronic hepatitis, cirrhosis without portal hypertension
    - Hepatitis B or C without complications
    - Fatty liver disease with fibrosis
    
    Moderate to Severe Liver Disease (3 Points):
    - Cirrhosis with portal hypertension, varices, or ascites
    - Hepatic encephalopathy or hepatorenal syndrome
    - Liver transplant recipients
    
    Diabetes Categories (Mutually Exclusive):
    
    Uncomplicated Diabetes (1 Point):
    - Type 1 or Type 2 diabetes without end-organ damage
    - Well-controlled diabetes without complications
    - Gestational diabetes history does not count
    
    Diabetes with End-Organ Damage (2 Points):
    - Diabetic retinopathy, nephropathy, or neuropathy
    - History of diabetic ketoacidosis or hyperosmolar coma
    - Diabetes requiring insulin with complications
    
    6-Point Conditions (Severe Impact):
    
    Metastatic Solid Tumor:
    - Cancer with distant metastases
    - Stage IV solid tumors
    - Significantly impacts life expectancy
    
    AIDS:
    - Acquired immunodeficiency syndrome
    - HIV with opportunistic infections or CD4 <200
    - AIDS-defining illnesses present
    
    Clinical Decision Making:
    The CCI helps guide treatment intensity, screening decisions, and prognostic discussions. 
    Higher scores suggest focusing on comfort and quality of life, while lower scores support 
    aggressive interventions and preventive care.
    
    Important Considerations:
    - Liver disease and diabetes use mutually exclusive categories
    - Scoring based on current or historical diagnoses
    - Consider patient functional status alongside CCI score
    - Original validation in hospitalized medical patients
    - Subsequent validation across multiple healthcare settings
    
    References (Vancouver style):
    1. Charlson ME, Pompei P, Ales KL, MacKenzie CR. A new method of classifying prognostic 
    comorbidity in longitudinal studies: development and validation. J Chronic Dis. 1987;40(5):373-83.
    2. Charlson M, Szatrowski TP, Peterson J, Gold J. Validation of a combined comorbidity index. 
    J Clin Epidemiol. 1994;47(11):1245-51.
    """
    
    age: int = Field(
        ...,
        ge=0,
        le=120,
        description="Patient age in years. Age adjustment: <50y (0 pts), 50-59y (1 pt), 60-69y (2 pts), 70-79y (3 pts), ≥80y (4 pts)",
        example=65
    )
    
    myocardial_infarction: Literal["yes", "no"] = Field(
        ...,
        description="History of myocardial infarction documented by ECG, enzymes, or imaging. Includes STEMI and NSTEMI. Scores 1 point if present",
        example="no"
    )
    
    congestive_heart_failure: Literal["yes", "no"] = Field(
        ...,
        description="Clinical syndrome of heart failure (systolic or diastolic) with documentation or objective evidence. Scores 1 point if present",
        example="no"
    )
    
    peripheral_vascular_disease: Literal["yes", "no"] = Field(
        ...,
        description="Aortic aneurysm, peripheral arterial disease, claudication, or revascularization history. Scores 1 point if present",
        example="no"
    )
    
    cerebrovascular_disease: Literal["yes", "no"] = Field(
        ...,
        description="Stroke (ischemic/hemorrhagic) or TIA with neurological sequelae or documented imaging changes. Scores 1 point if present",
        example="no"
    )
    
    dementia: Literal["yes", "no"] = Field(
        ...,
        description="Chronic cognitive impairment affecting daily activities. Includes Alzheimer's, vascular, and other dementias. Scores 1 point if present",
        example="no"
    )
    
    chronic_pulmonary_disease: Literal["yes", "no"] = Field(
        ...,
        description="COPD, chronic bronchitis, emphysema, or severe asthma with chronic symptoms/testing abnormalities. Scores 1 point if present",
        example="no"
    )
    
    connective_tissue_disease: Literal["yes", "no"] = Field(
        ...,
        description="SLE, rheumatoid arthritis, systemic sclerosis, polymyositis, or mixed connective tissue disease. Scores 1 point if present",
        example="no"
    )
    
    peptic_ulcer_disease: Literal["yes", "no"] = Field(
        ...,
        description="History of peptic or duodenal ulcer requiring treatment, including complications or H. pylori treatment. Scores 1 point if present",
        example="no"
    )
    
    liver_disease: Literal["none", "mild", "moderate_severe"] = Field(
        ...,
        description="Liver disease severity. Mild (chronic hepatitis, uncomplicated cirrhosis) = 1 pt. Moderate-severe (portal hypertension, varices, ascites) = 3 pts. Mutually exclusive categories",
        example="none"
    )
    
    diabetes: Literal["none", "uncomplicated", "with_end_organ_damage"] = Field(
        ...,
        description="Diabetes severity. Uncomplicated (no end-organ damage) = 1 pt. With end-organ damage (retinopathy, nephropathy, neuropathy) = 2 pts. Mutually exclusive categories",
        example="none"
    )
    
    hemiplegia: Literal["yes", "no"] = Field(
        ...,
        description="Paralysis of one side of body from stroke or other cause, including paraplegia. Must have persistent deficit. Scores 2 points if present",
        example="no"
    )
    
    moderate_severe_ckd: Literal["yes", "no"] = Field(
        ...,
        description="CKD with eGFR <60 mL/min/1.73m², dialysis dependence, or kidney transplant (CKD stages 3-5). Scores 2 points if present",
        example="no"
    )
    
    localized_solid_tumor: Literal["yes", "no"] = Field(
        ...,
        description="Cancer without metastasis, treated with curative intent. Active disease or remission <5 years. Scores 2 points if present",
        example="no"
    )
    
    leukemia: Literal["yes", "no"] = Field(
        ...,
        description="Acute or chronic leukemia of any type (lymphocytic or myeloid) in active treatment or remission phase. Scores 2 points if present",
        example="no"
    )
    
    lymphoma: Literal["yes", "no"] = Field(
        ...,
        description="Hodgkin's or non-Hodgkin's lymphoma, including multiple myeloma in active disease or treatment phase. Scores 2 points if present",
        example="no"
    )
    
    metastatic_solid_tumor: Literal["yes", "no"] = Field(
        ...,
        description="Cancer with distant metastases (Stage IV solid tumors) significantly impacting life expectancy. Scores 6 points if present",
        example="no"
    )
    
    aids: Literal["yes", "no"] = Field(
        ...,
        description="AIDS with opportunistic infections, CD4 <200, or AIDS-defining illnesses. HIV alone without AIDS does not count. Scores 6 points if present",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "myocardial_infarction": "no",
                "congestive_heart_failure": "yes",
                "peripheral_vascular_disease": "no",
                "cerebrovascular_disease": "no",
                "dementia": "no",
                "chronic_pulmonary_disease": "yes",
                "connective_tissue_disease": "no",
                "peptic_ulcer_disease": "no",
                "liver_disease": "none",
                "diabetes": "uncomplicated",
                "hemiplegia": "no",
                "moderate_severe_ckd": "no",
                "localized_solid_tumor": "no",
                "leukemia": "no",
                "lymphoma": "no",
                "metastatic_solid_tumor": "no",
                "aids": "no"
            }
        }


class CharlsonComorbidityIndexResponse(BaseModel):
    """
    Response model for Charlson Comorbidity Index (CCI)
    
    The CCI provides a comprehensive assessment of comorbidity burden with quantitative 
    10-year survival predictions. The scoring system ranges from 0 to 37 points, with 
    higher scores indicating greater mortality risk and lower survival probability.
    
    Score Interpretation and Risk Categories:
    
    Low Risk (Score 0-1):
    - Minimal comorbidity burden
    - Excellent 10-year survival (>90%)
    - Aggressive screening and prevention recommended
    - Consider intensive treatments and procedures
    - Life expectancy minimally affected by comorbidities
    
    Moderate Risk (Score 2-3):
    - Moderate comorbidity burden  
    - Good 10-year survival (70-90%)
    - Standard screening and prevention appropriate
    - Consider patient preferences in treatment decisions
    - Moderate impact on life expectancy
    
    High Risk (Score 4-5):
    - Significant comorbidity burden
    - Reduced 10-year survival (30-70%)
    - Selective screening based on life expectancy
    - Focus on treatments with proven short-term benefit
    - Significant impact on life expectancy and function
    
    Very High Risk (Score ≥6):
    - Severe comorbidity burden
    - Poor 10-year survival (<30%)
    - Limited screening, focus on symptom management
    - Prioritize comfort and quality of life measures
    - Severe impact on life expectancy
    
    Clinical Applications:
    
    Treatment Decision Making:
    - Guide intensity of interventions based on prognosis
    - Balance potential benefits against remaining life expectancy
    - Consider patient values and goals of care
    
    Screening Programs:
    - Cancer screening may not benefit high-risk patients
    - Cardiovascular prevention strategies in context of prognosis  
    - Osteoporosis screening based on life expectancy
    
    Resource Allocation:
    - Prioritize intensive care resources
    - Plan rehabilitation and long-term care needs
    - Guide palliative care discussions
    
    Research Applications:
    - Stratify patients in clinical trials
    - Control for comorbidity burden in outcomes research
    - Compare populations across studies
    
    Limitations and Considerations:
    - Originally validated in hospitalized medical patients
    - May not reflect functional status or frailty
    - Consider patient preferences alongside numerical score
    - Some conditions may be under-weighted in modern medicine
    - Cultural and social factors not captured
    
    10-Year Survival Formula:
    The mathematical relationship 10-year survival = 0.983^(CCI × 0.9) assumes a 
    theoretical low-risk population with 98.3% baseline survival, derived from the 
    original validation cohort.
    
    Clinical Decision Framework:
    1. Calculate CCI score using current/historical diagnoses
    2. Estimate 10-year survival probability
    3. Consider functional status and patient goals
    4. Discuss prognosis and treatment options
    5. Make shared decisions about care intensity
    
    Quality Improvement Applications:
    - Risk adjustment for outcome comparisons
    - Population health management
    - Care pathway development
    - Provider performance assessment
    
    Reference: Charlson ME, et al. J Chronic Dis. 1987;40(5):373-83.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Comprehensive CCI assessment including score breakdown, survival probability, and clinical interpretation",
        example={
            "total_score": 5,
            "age_points": 2,
            "comorbidity_points": 3,
            "ten_year_survival_probability": 53.8,
            "ten_year_survival_percentage": "53.8%",
            "risk_category": "High Risk",
            "risk_description": "Significant comorbidity burden with reduced survival",
            "clinical_interpretation": "Reduced 10-year survival (30-70%). Significant impact from comorbidities.",
            "score_breakdown": {
                "age_assessment": {
                    "age": 65,
                    "points": 2,
                    "description": "Age 65 years (2 points)"
                },
                "comorbidity_assessment": {
                    "myocardial_infarction": {
                        "present": False,
                        "points": 0,
                        "description": "Myocardial infarction (1 point)"
                    },
                    "congestive_heart_failure": {
                        "present": True,
                        "points": 1,
                        "description": "Congestive heart failure (1 point)"
                    },
                    "chronic_pulmonary_disease": {
                        "present": True,
                        "points": 1,
                        "description": "Chronic pulmonary disease (1 point)"
                    },
                    "diabetes": {
                        "present": True,
                        "severity": "uncomplicated",
                        "points": 1,
                        "description": "Diabetes mellitus (1-2 points based on severity)"
                    }
                },
                "scoring_summary": {
                    "total_comorbidity_points": 3,
                    "age_adjustment_points": 2,
                    "maximum_possible_score": 37,
                    "formula": "10-year survival = 0.983^(CCI × 0.9)"
                }
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
        description="Clinical interpretation with survival probability and evidence-based recommendations for care planning",
        example="Charlson Comorbidity Index Score: 5 points. Predicted 10-year survival: 53.8%. Reduced 10-year survival (30-70%). Significant impact from comorbidities. Consider individual patient factors and treatment goals when making clinical decisions based on this assessment."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Minimal Comorbidity, Moderate Comorbidity, Significant Comorbidity, Severe Comorbidity)",
        example="Significant Comorbidity"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the comorbidity burden and prognosis",
        example="Significant comorbidity burden with reduced survival"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "total_score": 5,
                    "age_points": 2,
                    "comorbidity_points": 3,
                    "ten_year_survival_probability": 53.8,
                    "ten_year_survival_percentage": "53.8%",
                    "risk_category": "High Risk",
                    "risk_description": "Significant comorbidity burden with reduced survival",
                    "clinical_interpretation": "Reduced 10-year survival (30-70%). Significant impact from comorbidities.",
                    "score_breakdown": {
                        "age_assessment": {
                            "age": 65,
                            "points": 2,
                            "description": "Age 65 years (2 points)"
                        },
                        "comorbidity_assessment": {
                            "myocardial_infarction": {
                                "present": False,
                                "points": 0,
                                "description": "Myocardial infarction (1 point)"
                            },
                            "congestive_heart_failure": {
                                "present": True,
                                "points": 1,
                                "description": "Congestive heart failure (1 point)"
                            },
                            "peripheral_vascular_disease": {
                                "present": False,
                                "points": 0,
                                "description": "Peripheral vascular disease (1 point)"
                            },
                            "cerebrovascular_disease": {
                                "present": False,
                                "points": 0,
                                "description": "Cerebrovascular disease/TIA (1 point)"
                            },
                            "dementia": {
                                "present": False,
                                "points": 0,
                                "description": "Dementia (1 point)"
                            },
                            "chronic_pulmonary_disease": {
                                "present": True,
                                "points": 1,
                                "description": "Chronic pulmonary disease (1 point)"
                            },
                            "connective_tissue_disease": {
                                "present": False,
                                "points": 0,
                                "description": "Connective tissue disease (1 point)"
                            },
                            "peptic_ulcer_disease": {
                                "present": False,
                                "points": 0,
                                "description": "Peptic ulcer disease (1 point)"
                            },
                            "liver_disease": {
                                "present": False,
                                "severity": "none",
                                "points": 0,
                                "description": "Liver disease (1-3 points based on severity)"
                            },
                            "diabetes": {
                                "present": True,
                                "severity": "uncomplicated",
                                "points": 1,
                                "description": "Diabetes mellitus (1-2 points based on severity)"
                            },
                            "hemiplegia": {
                                "present": False,
                                "points": 0,
                                "description": "Hemiplegia (2 points)"
                            },
                            "moderate_severe_ckd": {
                                "present": False,
                                "points": 0,
                                "description": "Moderate to severe CKD (2 points)"
                            },
                            "localized_solid_tumor": {
                                "present": False,
                                "points": 0,
                                "description": "Localized solid tumor (2 points)"
                            },
                            "leukemia": {
                                "present": False,
                                "points": 0,
                                "description": "Leukemia (2 points)"
                            },
                            "lymphoma": {
                                "present": False,
                                "points": 0,
                                "description": "Lymphoma (2 points)"
                            },
                            "metastatic_solid_tumor": {
                                "present": False,
                                "points": 0,
                                "description": "Metastatic solid tumor (6 points)"
                            },
                            "aids": {
                                "present": False,
                                "points": 0,
                                "description": "AIDS (6 points)"
                            }
                        },
                        "scoring_summary": {
                            "total_comorbidity_points": 3,
                            "age_adjustment_points": 2,
                            "maximum_possible_score": 37,
                            "formula": "10-year survival = 0.983^(CCI × 0.9)"
                        }
                    }
                },
                "unit": "points",
                "interpretation": "Charlson Comorbidity Index Score: 5 points. Predicted 10-year survival: 53.8%. Reduced 10-year survival (30-70%). Significant impact from comorbidities. Consider individual patient factors and treatment goals when making clinical decisions based on this assessment.",
                "stage": "Significant Comorbidity",
                "stage_description": "Significant comorbidity burden with reduced survival"
            }
        }