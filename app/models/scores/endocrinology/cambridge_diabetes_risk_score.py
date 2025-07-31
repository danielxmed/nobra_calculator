"""
Cambridge Diabetes Risk Score Models

Request and response models for Cambridge Diabetes Risk Score calculation.

References (Vancouver style):
1. Griffin SJ, Little PS, Hales CN, Kinmonth AL, Wareham NJ. Diabetes risk score: 
   towards earlier detection of type 2 diabetes in general practice. Diabetes Metab 
   Res Rev. 2000 May-Jun;16(3):164-71. doi: 10.1002/1520-7560(200005/06)16:3<164::aid-dmrr103>3.0.co;2-r.
2. Wareham NJ, Griffin SJ. Risk scores for predicting type 2 diabetes: comparing 
   axes and spades. Diabetologia. 2011 May;54(5):994-5. doi: 10.1007/s00125-011-2101-0.
3. Rahman M, Simmons RK, Harding AH, Wareham NJ, Griffin SJ. A simple risk score 
   identifies individuals at high risk of developing Type 2 diabetes: a prospective 
   cohort study. Fam Pract. 2008 Jun;25(3):191-6. doi: 10.1093/fampra/cmn024.

The Cambridge Diabetes Risk Score is a screening tool that predicts the probability 
of having undiagnosed type 2 diabetes. It uses seven clinical and demographic factors 
in a logistic regression model to identify individuals who should undergo diabetes testing.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class CambridgeDiabetesRiskScoreRequest(BaseModel):
    """
    Request model for Cambridge Diabetes Risk Score
    
    The Cambridge Diabetes Risk Score uses 7 risk factors to predict undiagnosed diabetes:
    
    Gender:
    - Male sex confers higher risk (OR 2.41)
    - Female sex is the reference category
    
    Age Categories:
    - <45 years: reference category
    - 45-54 years: OR 3.39
    - 55-64 years: OR 6.02
    - ≥65 years: OR 8.94
    
    BMI Categories:
    - <25 kg/m²: reference category (normal weight)
    - 25-27.5 kg/m²: OR 2.01 (overweight)
    - 27.5-30 kg/m²: OR 3.29 (overweight)
    - ≥30 kg/m²: OR 8.42 (obese)
    
    Other Risk Factors:
    - Family history of diabetes: OR 2.07
    - Current smoking: OR 2.35
    - Antihypertensive medication: OR 3.39
    - Steroid medication: OR 8.92
    
    The score predicts current undiagnosed diabetes, not future diabetes risk.
    
    References (Vancouver style):
    1. Griffin SJ, Little PS, Hales CN, Kinmonth AL, Wareham NJ. Diabetes risk score: 
    towards earlier detection of type 2 diabetes in general practice. Diabetes Metab 
    Res Rev. 2000 May-Jun;16(3):164-71.
    """
    
    gender: Literal["male", "female"] = Field(
        ...,
        description="Patient's biological sex. Male sex increases diabetes risk (OR 2.41)",
        example="male"
    )
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient's age in years. Risk increases significantly with age, especially after 45",
        example=55
    )
    
    bmi_category: Literal["under_25", "25_to_27.5", "27.5_to_30", "30_or_more"] = Field(
        ...,
        description="BMI category: under_25 (normal), 25_to_27.5 (overweight), 27.5_to_30 (overweight), 30_or_more (obese). Higher BMI strongly increases risk",
        example="27.5_to_30"
    )
    
    family_history: Literal["yes", "no"] = Field(
        ...,
        description="Family history of diabetes in first-degree relatives (parents, siblings, children). Increases risk by OR 2.07",
        example="yes"
    )
    
    smoking_status: Literal["yes", "no"] = Field(
        ...,
        description="Current smoking status. Active smoking increases diabetes risk (OR 2.35)",
        example="no"
    )
    
    antihypertensive_use: Literal["yes", "no"] = Field(
        ...,
        description="Currently prescribed antihypertensive (blood pressure) medication. Associated with increased risk (OR 3.39)",
        example="yes"
    )
    
    steroid_use: Literal["yes", "no"] = Field(
        ...,
        description="Currently prescribed steroid medication (oral corticosteroids). Strongly increases risk (OR 8.92)",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "gender": "male",
                "age": 55,
                "bmi_category": "27.5_to_30",
                "family_history": "yes",
                "smoking_status": "no",
                "antihypertensive_use": "yes",
                "steroid_use": "no"
            }
        }


class CambridgeDiabetesRiskScoreResponse(BaseModel):
    """
    Response model for Cambridge Diabetes Risk Score
    
    The score provides a probability (0-1) of having undiagnosed type 2 diabetes.
    
    Key cutoff points:
    - 0.11 cutoff: 85% sensitivity, 51% specificity (captures most cases)
    - 0.29 cutoff: 51% sensitivity, 78% specificity (higher specificity)
    
    Clinical Application:
    - Low risk (<0.11): Routine screening may still be appropriate
    - Moderate risk (0.11-0.29): Consider diabetes screening
    - High risk (≥0.29): Strongly recommend immediate screening
    
    Screening Methods:
    - Fasting plasma glucose ≥126 mg/dL (7.0 mmol/L)
    - HbA1c ≥6.5% (48 mmol/mol)
    - 2-hour plasma glucose ≥200 mg/dL (11.1 mmol/L) during OGTT
    - Random plasma glucose ≥200 mg/dL (11.1 mmol/L) with symptoms
    
    Limitations:
    - Validated primarily in white English populations
    - May not generalize to other ethnic groups with different diabetes risk profiles
    - Predicts current undiagnosed diabetes, not future risk
    
    Reference: Griffin SJ, et al. Diabetes Metab Res Rev. 2000;16(3):164-71.
    """
    
    result: float = Field(
        ...,
        ge=0,
        le=1,
        description="Probability of having undiagnosed type 2 diabetes (0-1)",
        example=0.247
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (probability)",
        example="probability"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and screening recommendations based on risk level",
        example="Moderate risk of undiagnosed type 2 diabetes. Consider diabetes screening with fasting glucose or HbA1c. This range captures most individuals with undiagnosed diabetes."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Moderate Risk, High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Moderate probability of undiagnosed diabetes"
    )
    
    details: Dict[str, Any] = Field(
        ...,
        description="Additional calculation details including linear predictor and percentage risk",
        example={
            "linear_predictor": -1.137,
            "percentage_risk": 24.7,
            "sensitivity_at_0.11": "85%",
            "specificity_at_0.11": "51%",
            "sensitivity_at_0.29": "51%",
            "specificity_at_0.29": "78%"
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 0.247,
                "unit": "probability",
                "interpretation": "Moderate risk of undiagnosed type 2 diabetes. Consider diabetes screening with fasting glucose or HbA1c. This range captures most individuals with undiagnosed diabetes.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate probability of undiagnosed diabetes",
                "details": {
                    "linear_predictor": -1.137,
                    "percentage_risk": 24.7,
                    "sensitivity_at_0.11": "85%",
                    "specificity_at_0.11": "51%",
                    "sensitivity_at_0.29": "51%",
                    "specificity_at_0.29": "78%"
                }
            }
        }