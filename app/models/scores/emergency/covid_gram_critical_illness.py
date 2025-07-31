"""
COVID-GRAM Critical Illness Risk Score Models

Request and response models for COVID-GRAM calculation.

References (Vancouver style):
1. Liang W, Liang H, Ou L, Chen B, Chen A, Li C, et al. Development and Validation 
   of a Clinical Risk Score to Predict the Occurrence of Critical Illness in 
   Hospitalized Patients With COVID-19. JAMA Intern Med. 2020;180(8):1081-1089. 
   doi:10.1001/jamainternmed.2020.2033

The COVID-GRAM Critical Illness Risk Score is a 10-variable clinical prediction model 
that estimates the risk of critical illness (ICU admission, invasive mechanical 
ventilation, or death) in hospitalized COVID-19 patients. It was developed from 
1590 patients and validated in 710 patients, achieving an AUC of 0.88 
(95% CI, 0.85-0.91) in the development cohort.

The score includes clinical symptoms (hemoptysis, dyspnea, unconsciousness), 
demographic factors (age), medical history (comorbidities, cancer), imaging 
(chest X-ray abnormalities), and laboratory values (neutrophil-lymphocyte ratio, 
lactate dehydrogenase, direct bilirubin).
"""

from pydantic import BaseModel, Field
from typing import Literal


class CovidGramCriticalIllnessRequest(BaseModel):
    """
    Request model for COVID-GRAM Critical Illness Risk Score
    
    The COVID-GRAM score uses 10 clinical variables to predict critical illness 
    (ICU admission, mechanical ventilation, or death) in hospitalized COVID-19 patients:
    
    Clinical Variables:
    - chest_xray_abnormality: Abnormal chest X-ray findings (yes/no)
    - age: Patient age in years (18-120)
    - hemoptysis: Coughing up blood (yes/no)
    - dyspnea: Shortness of breath (yes/no)
    - unconsciousness: Altered mental status or unconsciousness (yes/no)
    - number_of_comorbidities: Count of comorbid conditions (0-10)
    - cancer_history: Previous or current cancer diagnosis (yes/no)
    
    Laboratory Variables:
    - neutrophil_lymphocyte_ratio: Neutrophil count divided by lymphocyte count (0.5-50.0)
    - lactate_dehydrogenase: LDH level in U/L (100.0-2000.0)
    - direct_bilirubin: Direct bilirubin level in mg/dL (0.1-20.0)
    
    Scoring Formula:
    Risk Score = -146.5 + (chest X-ray abnormality × 27.1464) + (age × 0.6139) + 
                 (hemoptysis × 33.6210) + (dyspnea × 14.0569) + (unconsciousness × 34.4617) + 
                 (number of comorbidities × 10.3826) + (cancer history × 31.2211) + 
                 (neutrophil-lymphocyte ratio × 1.25) + (LDH × 0.0534) + (direct bilirubin × 3.0605)
    
    Probability = e^(Risk Score) / (1 + e^(Risk Score))
    
    Risk Categories:
    - Low Risk: <1.7% probability
    - Medium Risk: 1.7-40.4% probability  
    - High Risk: >40.4% probability
    
    References (Vancouver style):
    1. Liang W, Liang H, Ou L, Chen B, Chen A, Li C, et al. Development and Validation 
    of a Clinical Risk Score to Predict the Occurrence of Critical Illness in 
    Hospitalized Patients With COVID-19. JAMA Intern Med. 2020;180(8):1081-1089. 
    doi:10.1001/jamainternmed.2020.2033
    """
    
    chest_xray_abnormality: Literal["yes", "no"] = Field(
        ...,
        description="Chest X-ray abnormality present. Includes consolidation, ground-glass opacities, bilateral infiltrates, or other abnormal findings. Scores 27.1464 points if yes",
        example="yes"
    )
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in years. Each year of age adds 0.6139 points to the risk score",
        example=65
    )
    
    hemoptysis: Literal["yes", "no"] = Field(
        ...,
        description="Presence of hemoptysis (coughing up blood or blood-tinged sputum). Scores 33.6210 points if yes",
        example="no"
    )
    
    dyspnea: Literal["yes", "no"] = Field(
        ...,
        description="Presence of dyspnea (shortness of breath or difficulty breathing). Scores 14.0569 points if yes",
        example="yes"
    )
    
    unconsciousness: Literal["yes", "no"] = Field(
        ...,
        description="Presence of unconsciousness or altered mental status (confusion, delirium, coma). Scores 34.4617 points if yes",
        example="no"
    )
    
    number_of_comorbidities: int = Field(
        ...,
        ge=0,
        le=10,
        description="Total number of comorbid conditions (hypertension, diabetes, cardiovascular disease, chronic respiratory disease, etc.). Each comorbidity adds 10.3826 points",
        example=2
    )
    
    cancer_history: Literal["yes", "no"] = Field(
        ...,
        description="History of cancer (any type, previous or current diagnosis). Scores 31.2211 points if yes",
        example="no"
    )
    
    neutrophil_lymphocyte_ratio: float = Field(
        ...,
        ge=0.5,
        le=50.0,
        description="Neutrophil to lymphocyte ratio calculated from complete blood count. Each unit adds 1.25 points. Normal range is typically 1-3",
        example=3.5
    )
    
    lactate_dehydrogenase: float = Field(
        ...,
        ge=100.0,
        le=2000.0,
        description="Lactate dehydrogenase (LDH) level in U/L. Each unit adds 0.0534 points. Normal range is typically 140-280 U/L",
        example=450.0
    )
    
    direct_bilirubin: float = Field(
        ...,
        ge=0.1,
        le=20.0,
        description="Direct (conjugated) bilirubin level in mg/dL. Each unit adds 3.0605 points. Normal range is typically 0.0-0.3 mg/dL",
        example=0.5
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "chest_xray_abnormality": "yes",
                "age": 65,
                "hemoptysis": "no",
                "dyspnea": "yes",
                "unconsciousness": "no",
                "number_of_comorbidities": 2,
                "cancer_history": "no",
                "neutrophil_lymphocyte_ratio": 3.5,
                "lactate_dehydrogenase": 450.0,
                "direct_bilirubin": 0.5
            }
        }


class CovidGramCriticalIllnessResponse(BaseModel):
    """
    Response model for COVID-GRAM Critical Illness Risk Score
    
    The COVID-GRAM score provides a probability percentage for critical illness 
    (ICU admission, invasive mechanical ventilation, or death) in hospitalized 
    COVID-19 patients. The model has been validated with an AUC of 0.88 and 
    outperformed the CURB-65 model in COVID-19 patients.
    
    Risk Categories:
    - Low Risk (<1.7%): Standard monitoring and care
    - Medium Risk (1.7-40.4%): Enhanced monitoring with close observation
    - High Risk (>40.4%): Intensive monitoring and ICU consideration
    
    Reference: Liang W, et al. JAMA Intern Med. 2020;180(8):1081-1089.
    """
    
    result: float = Field(
        ...,
        description="COVID-GRAM critical illness risk probability as a percentage (0.1-99.9%)",
        example=25.3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk probability",
        example="%"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on the risk probability",
        example="Medium risk for critical illness. Enhanced monitoring and close observation are recommended. Intermediate probability of requiring ICU admission, mechanical ventilation, or death."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Low Risk, Medium Risk, High Risk)",
        example="Medium Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Medium risk of critical illness"
    )
    
    calculation_details: dict = Field(
        ...,
        description="Additional calculation details including linear predictor, risk factors, and recommendations",
        example={
            "linear_predictor": -0.85,
            "risk_factors_present": "Moderate risk factors for critical illness",
            "clinical_recommendations": "Enhanced monitoring with close observation",
            "monitoring_level": "Enhanced monitoring with frequent assessments",
            "critical_illness_components": [
                "ICU admission requirement",
                "Invasive mechanical ventilation",
                "Death"
            ]
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 25.3,
                "unit": "%",
                "interpretation": "Medium risk for critical illness. Enhanced monitoring and close observation are recommended. Intermediate probability of requiring ICU admission, mechanical ventilation, or death.",
                "stage": "Medium Risk",
                "stage_description": "Medium risk of critical illness",
                "calculation_details": {
                    "linear_predictor": -0.85,
                    "risk_factors_present": "Moderate risk factors for critical illness",
                    "clinical_recommendations": "Enhanced monitoring with close observation",
                    "monitoring_level": "Enhanced monitoring with frequent assessments",
                    "critical_illness_components": [
                        "ICU admission requirement",
                        "Invasive mechanical ventilation",
                        "Death"
                    ]
                }
            }
        }