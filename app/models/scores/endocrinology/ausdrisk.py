"""
Australian Type 2 Diabetes Risk (AUSDRISK) Assessment Tool Models

Request and response models for AUSDRISK calculation.

References (Vancouver style):
1. Chen L, Magliano DJ, Balkau B, Colagiuri S, Zimmet PZ, Tonkin AM, et al. AUSDRISK: 
   an Australian Type 2 Diabetes Risk Assessment Tool based on demographic, lifestyle 
   and simple anthropometric measures. Med J Aust. 2010;192(4):197-202.

The AUSDRISK tool estimates 5-year risk of developing type 2 diabetes in Australian patients 
based on nine risk factors: age, sex, ethnicity, parental history of diabetes, history of 
high blood glucose, use of antihypertensive medications, smoking, physical inactivity, and 
waist circumference. A score ≥12 indicates increased diabetes risk requiring medical evaluation.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AusdriskRequest(BaseModel):
    """
    Request model for Australian Type 2 Diabetes Risk Assessment Tool (AUSDRISK)
    
    The AUSDRISK uses 9 variables to predict 5-year diabetes risk:
    
    Age Groups:
    - 25-34: 0 points
    - 35-44: 2 points
    - 45-54: 4 points
    - 55-64: 6 points
    - 65+: 8 points
    
    Sex:
    - Female: 0 points
    - Male: 3 points
    
    Ethnicity:
    - Southern European: 2 points
    - Asian: 2 points
    - Aboriginal/Torres Strait Islander: 2 points
    - Pacific Islander: 2 points
    - Other: 0 points
    
    Other Risk Factors:
    - Parental diabetes: 3 points if yes
    - High blood glucose history: 6 points if yes
    - Antihypertensive medication: 2 points if yes
    - Current smoker: 2 points if yes
    - Physical inactivity: 2 points if yes
    - Waist circumference: 0, 4, or 7 points based on category

    References (Vancouver style):
    1. Chen L, Magliano DJ, Balkau B, Colagiuri S, Zimmet PZ, Tonkin AM, et al. AUSDRISK: 
       an Australian Type 2 Diabetes Risk Assessment Tool based on demographic, lifestyle 
       and simple anthropometric measures. Med J Aust. 2010;192(4):197-202.
    """
    
    age: Literal["25-34", "35-44", "45-54", "55-64", "65+"] = Field(
        ...,
        description="Age group. 25-34 years scores 0 points, 35-44 scores 2 points, 45-54 scores 4 points, 55-64 scores 6 points, 65+ scores 8 points",
        example="45-54"
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Biological sex. Female scores 0 points, male scores 3 points",
        example="male"
    )
    
    ethnicity: Literal["southern_european", "asian", "aboriginal_torres_strait", "pacific_islander", "other"] = Field(
        ...,
        description="Ethnic background. Southern European, Asian, Aboriginal/Torres Strait Islander, and Pacific Islander score 2 points; other ethnicities score 0 points",
        example="other"
    )
    
    parental_diabetes: Literal["yes", "no"] = Field(
        ...,
        description="Family history of diabetes in parents. Scores 3 points if yes",
        example="no"
    )
    
    high_blood_glucose_history: Literal["yes", "no"] = Field(
        ...,
        description="History of high blood glucose levels (e.g., during pregnancy, illness, or health check). Scores 6 points if yes",
        example="no"
    )
    
    antihypertensive_medication: Literal["yes", "no"] = Field(
        ...,
        description="Currently taking medication for high blood pressure. Scores 2 points if yes",
        example="no"
    )
    
    current_smoker: Literal["yes", "no"] = Field(
        ...,
        description="Currently smoking cigarettes or other tobacco products on a daily basis. Scores 2 points if yes",
        example="no"
    )
    
    physical_activity: Literal["active", "inactive"] = Field(
        ...,
        description="Physical activity status. Active if ≥150 minutes/week of walking (continuous ≥10 min) or moderate/vigorous activity. Inactive scores 2 points",
        example="active"
    )
    
    waist_circumference_category: Literal["category_1", "category_2", "category_3"] = Field(
        ...,
        description="Waist circumference category based on ethnicity and sex-specific cut-points. Category 1 scores 0 points, category 2 scores 4 points, category 3 scores 7 points. For Aboriginal/Torres Strait Islander or Asian: Cat 1 = <90cm (men), <80cm (women); Cat 2 = 90-99cm (men), 80-89cm (women); Cat 3 = ≥100cm (men), ≥90cm (women). For other ethnicities: Cat 1 = <102cm (men), <88cm (women); Cat 2 = 102-109cm (men), 88-99cm (women); Cat 3 = ≥110cm (men), ≥100cm (women)",
        example="category_1"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": "45-54",
                "sex": "male",
                "ethnicity": "other",
                "parental_diabetes": "no",
                "high_blood_glucose_history": "no",
                "antihypertensive_medication": "yes",
                "current_smoker": "no",
                "physical_activity": "active",
                "waist_circumference_category": "category_2"
            }
        }


class AusdriskResponse(BaseModel):
    """
    Response model for Australian Type 2 Diabetes Risk Assessment Tool (AUSDRISK)
    
    The AUSDRISK score ranges from 0 to 35 points and stratifies patients into risk categories:
    - Low Risk (≤5 points): ~1 in 100 chance of diabetes within 5 years
    - Intermediate Risk (6-11 points): ~1 in 30-50 chance
    - High Risk (12-19 points): ~1 in 7-14 chance
    - Very High Risk (≥20 points): ~1 in 3 chance
    
    A score ≥12 has 74% sensitivity and 67.7% specificity for identifying diabetes risk.
    
    Reference: Chen L, et al. Med J Aust. 2010;192(4):197-202.
    """
    
    result: int = Field(
        ...,
        description="AUSDRISK score calculated from 9 risk factors (range: 0-35 points)",
        example=10
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommendations based on the score",
        example="Approximately 1 in 30 chance of developing type 2 diabetes within 5 years. Lifestyle modifications strongly recommended, consider consulting healthcare provider."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Intermediate Risk, High Risk, Very High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category with score range",
        example="9-11 points"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 10,
                "unit": "points",
                "interpretation": "Approximately 1 in 30 chance of developing type 2 diabetes within 5 years. Lifestyle modifications strongly recommended, consider consulting healthcare provider.",
                "stage": "Intermediate Risk",
                "stage_description": "9-11 points"
            }
        }