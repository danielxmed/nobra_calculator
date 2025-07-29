"""
American Diabetes Association (ADA) Risk Calculator Models

Request and response models for ADA diabetes risk assessment.

References (Vancouver style):
1. Bang H, Edwards AM, Bomback AS, Ballantyne CM, Brancati FL, Coresh J, Heiss G, 
   Hoogeveen RC, Pankow JS, Ballantyne CM, Astor BC. Development and validation of 
   a patient self-assessment score for diabetes risk. Ann Intern Med. 2009 Dec 
   1;151(11):775-83. doi: 10.7326/0003-4819-151-11-200912010-00005. PMID: 19949143; 
   PMCID: PMC2861618.
2. American Diabetes Association. 2. Classification and Diagnosis of Diabetes: 
   Standards of Medical Care in Diabetes—2021. Diabetes Care. 2021 Jan;44(Suppl 1):
   S15-S33. doi: 10.2337/dc21-S002. PMID: 33298413.
3. Herman WH, Smith PJ, Thompson TJ, Engelgau MM, Aubert RE. A new and simple 
   questionnaire to identify people at increased risk for undiagnosed diabetes. 
   Diabetes Care. 1995 Mar;18(3):382-7. doi: 10.2337/diacare.18.3.382. PMID: 7555482.

The American Diabetes Association (ADA) Risk Calculator is a clinical decision tool 
that uses 6 easily obtainable demographic and clinical variables to identify individuals 
at high risk for undiagnosed type 2 diabetes mellitus. Developed and validated by 
Bang et al. in 2009, this self-assessment tool allows for diabetes risk stratification 
without requiring laboratory tests or physical examinations.

The calculator uses a point-based scoring system (0-10 points total) based on:
- Age (0-3 points)
- Gender (0-1 points, with males at higher risk)
- Family history of diabetes (0-1 points)
- History of hypertension (0-1 points)
- Physical activity level (0-1 points, with inactivity increasing risk)
- Body Mass Index category (0-3 points)

Clinical Application:
The ADA Risk Calculator serves as a screening tool to identify individuals who would 
benefit from formal diabetes testing. It helps healthcare providers and individuals 
prioritize diabetes screening efforts and implement early prevention strategies.

Interpretation:
- Scores 0-3: Low risk (no immediate screening needed)
- Score 4: High risk for prediabetes (consider screening and lifestyle interventions)
- Scores 5-10: High risk for diabetes (recommend screening and prevention programs)

This tool is particularly valuable in primary care settings and community health 
screening programs where laboratory testing may not be immediately available.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AdaRiskCalculatorRequest(BaseModel):
    """
    Request model for American Diabetes Association (ADA) Risk Calculator
    
    The ADA Risk Calculator uses 6 clinical and demographic variables to assess 
    diabetes risk in adults:
    
    Risk Factors and Scoring:
    
    Age Categories (0-3 points):
    - <40 years: 0 points
    - 40-49 years: 1 point
    - 50-59 years: 2 points
    - ≥60 years: 3 points
    
    Gender (0-1 points):
    - Female: 0 points
    - Male: 1 point (males have higher risk)
    
    Family History (0-1 points):
    - No first-degree relative with diabetes: 0 points
    - First-degree relative with diabetes: 1 point
    
    Hypertension History (0-1 points):
    - No hypertension history: 0 points
    - History of hypertension: 1 point
    
    Physical Activity (0-1 points):
    - Physically active: 0 points
    - Not physically active: 1 point (inactivity increases risk)
    
    BMI Categories (0-3 points):
    - <25 kg/m²: 0 points
    - 25-29.9 kg/m²: 1 point
    - 30-39.9 kg/m²: 2 points
    - ≥40 kg/m²: 3 points
    
    Clinical Context:
    This calculator is designed for screening asymptomatic adults in community 
    and primary care settings. It provides risk stratification without requiring 
    laboratory tests, making it accessible for initial screening efforts.
    
    The tool should not replace clinical judgment or established diabetes screening 
    guidelines, but rather complement existing preventive care strategies.
    
    References (Vancouver style):
    1. Bang H, Edwards AM, Bomback AS, Ballantyne CM, Brancati FL, Coresh J, et al. 
    Development and validation of a patient self-assessment score for diabetes risk. 
    Ann Intern Med. 2009 Dec 1;151(11):775-83. doi: 10.7326/0003-4819-151-11-200912010-00005.
    2. American Diabetes Association. Classification and Diagnosis of Diabetes: 
    Standards of Medical Care in Diabetes—2021. Diabetes Care. 2021 Jan;44(Suppl 1):
    S15-S33. doi: 10.2337/dc21-S002.
    """
    
    age_category: Literal["under_40", "40_49", "50_59", "60_or_older"] = Field(
        ...,
        description="Patient age category. Diabetes risk increases with age: <40 years (0 pts), 40-49 years (1 pt), 50-59 years (2 pts), ≥60 years (3 pts)",
        example="40_49"
    )
    
    gender: Literal["female", "male"] = Field(
        ...,
        description="Patient gender. Males have higher diabetes risk than females: Female (0 pts), Male (1 pt)",
        example="male"
    )
    
    family_history_diabetes: Literal["no", "yes"] = Field(
        ...,
        description="First-degree relative (parent, sibling, or child) with diabetes. Family history indicates genetic predisposition: No (0 pts), Yes (1 pt)",
        example="yes"
    )
    
    hypertension: Literal["no", "yes"] = Field(
        ...,
        description="History of hypertension including self-reported history, prescribed antihypertensive medication, and/or blood pressure ≥140/90 mmHg. Hypertension is associated with insulin resistance: No (0 pts), Yes (1 pt)",
        example="no"
    )
    
    physically_active: Literal["yes", "no"] = Field(
        ...,
        description="Physically active as self-reported by patient. Regular physical activity reduces diabetes risk: Yes (0 pts), No (1 pt)",
        example="no"
    )
    
    bmi_category: Literal["under_25", "25_to_30", "30_to_40", "40_or_higher"] = Field(
        ...,
        description="Body Mass Index category in kg/m². Higher BMI strongly correlates with diabetes risk: <25 (0 pts), 25-29.9 (1 pt), 30-39.9 (2 pts), ≥40 (3 pts)",
        example="30_to_40"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_category": "40_49",
                "gender": "male",
                "family_history_diabetes": "yes",
                "hypertension": "no",
                "physically_active": "no",
                "bmi_category": "30_to_40"
            }
        }


class AdaRiskCalculatorResponse(BaseModel):
    """
    Response model for American Diabetes Association (ADA) Risk Calculator
    
    The ADA Risk Calculator provides diabetes risk stratification based on total score:
    
    Risk Categories and Recommendations:
    
    Low Risk (0-3 points):
    - Estimated diabetes risk: Low
    - Recommendation: Continue routine preventive care and healthy lifestyle counseling
    - Screening: No immediate diabetes screening needed
    - Follow-up: Reassess risk periodically as risk factors change
    
    High Risk for Prediabetes (4 points):
    - Estimated risk: Moderate risk for prediabetes
    - Recommendation: Consider diabetes screening with laboratory tests
    - Tests: Fasting plasma glucose, oral glucose tolerance test, or HbA1c
    - Intervention: Lifestyle interventions recommended for prevention
    
    High Risk for Diabetes (5-10 points):
    - Estimated risk: High risk for undiagnosed diabetes
    - Recommendation: Diabetes screening strongly recommended
    - Tests: Fasting plasma glucose, oral glucose tolerance test, or HbA1c
    - Intervention: Consider enrollment in diabetes prevention programs
    - Follow-up: If negative, retest at least every 3 years or more frequently
    
    Clinical Implementation:
    The ADA Risk Calculator is designed to be used as a first-line screening tool 
    in community health programs, primary care settings, and self-assessment scenarios. 
    It helps identify individuals who would benefit from formal diabetes testing and 
    early intervention strategies.
    
    The calculator has been validated in diverse populations and provides a practical 
    approach to diabetes risk assessment that can complement but not replace clinical 
    judgment and established screening guidelines.
    
    Reference: Bang H, et al. Ann Intern Med. 2009;151(11):775-83.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=10,
        description="ADA diabetes risk score calculated from demographic and clinical factors (range: 0-10 points)",
        example=5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with specific screening recommendations based on the calculated risk score",
        example="High risk for undiagnosed diabetes. Recommend screening with fasting glucose, oral glucose tolerance test, or HbA1c. Consider diabetes prevention programs and lifestyle interventions."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Low Risk, High Risk for Prediabetes, High Risk for Diabetes)",
        example="High Risk for Diabetes"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="High risk for diabetes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5,
                "unit": "points", 
                "interpretation": "High risk for undiagnosed diabetes. Recommend screening with fasting glucose, oral glucose tolerance test, or HbA1c. Consider diabetes prevention programs and lifestyle interventions.",
                "stage": "High Risk for Diabetes",
                "stage_description": "High risk for diabetes"
            }
        }