"""
FINDRISC (Finnish Diabetes Risk Score) Models

Request and response models for FINDRISC calculation.

References (Vancouver style):
1. Lindström J, Tuomilehto J. The diabetes risk score: a practical tool to predict type 2 
   diabetes risk. Diabetes Care. 2003 Mar;26(3):725-31. doi: 10.2337/diacare.26.3.725.
2. Saaristo T, Peltonen M, Lindström J, Saarikoski L, Sundvall J, Eriksson JG, et al. 
   Cross-sectional evaluation of the Finnish Diabetes Risk Score: a tool to identify 
   undetected type 2 diabetes, abnormal glucose tolerance and metabolic syndrome. 
   Diab Vasc Dis Res. 2005 May;2(2):67-72. doi: 10.3132/dvdr.2005.011.
3. Tankova T, Chakarova N, Atanassova I, Dakovska L. Evaluation of the Finnish Diabetes 
   Risk Score as a screening tool for impaired fasting glucose, impaired glucose tolerance 
   and undetected diabetes. Diabetes Res Clin Pract. 2011 Apr;92(1):46-52. 
   doi: 10.1016/j.diabres.2010.12.020.

The FINDRISC is a non-invasive screening tool that uses 8 simple questions to assess 
the 10-year risk of developing type 2 diabetes. It was developed using data from the 
Finnish population and has been validated internationally. The score requires no laboratory 
tests and can be self-administered, making it ideal for population screening.
"""

from pydantic import BaseModel, Field
from typing import Literal


class FindriscRequest(BaseModel):
    """
    Request model for FINDRISC (Finnish Diabetes Risk Score)
    
    The FINDRISC uses 8 clinical and lifestyle variables to assess diabetes risk:
    
    Age Categories:
    - under_45: Age <45 years (0 points)
    - 45_to_54: Age 45-54 years (2 points)
    - 55_to_64: Age 55-64 years (3 points)
    - over_64: Age >64 years (4 points)
    
    BMI Categories:
    - under_25: BMI <25 kg/m² (0 points)
    - 25_to_30: BMI 25-30 kg/m² (1 point)
    - over_30: BMI ≥30 kg/m² (3 points)
    
    Waist Circumference Categories:
    - normal: Men <94cm, Women <80cm (0 points)
    - elevated: Men 94-102cm, Women 80-88cm (3 points)
    - high: Men ≥102cm, Women ≥88cm (4 points)
    
    Other Variables:
    - Physical activity at least 30 min/day (No = 2 points)
    - Daily fruit/vegetable consumption (No = 1 point)
    - Blood pressure medication (Yes = 2 points)
    - History of high blood glucose (Yes = 5 points)
    - Family history of diabetes (2nd degree = 3 points, 1st degree = 5 points)

    References (Vancouver style):
    1. Lindström J, Tuomilehto J. The diabetes risk score: a practical tool to predict type 2 
    diabetes risk. Diabetes Care. 2003 Mar;26(3):725-31. doi: 10.2337/diacare.26.3.725.
    2. Saaristo T, Peltonen M, Lindström J, Saarikoski L, Sundvall J, Eriksson JG, et al. 
    Cross-sectional evaluation of the Finnish Diabetes Risk Score: a tool to identify 
    undetected type 2 diabetes, abnormal glucose tolerance and metabolic syndrome. 
    Diab Vasc Dis Res. 2005 May;2(2):67-72. doi: 10.3132/dvdr.2005.011.
    3. Tankova T, Chakarova N, Atanassova I, Dakovska L. Evaluation of the Finnish Diabetes 
    Risk Score as a screening tool for impaired fasting glucose, impaired glucose tolerance 
    and undetected diabetes. Diabetes Res Clin Pract. 2011 Apr;92(1):46-52. 
    doi: 10.1016/j.diabres.2010.12.020.
    """
    
    age: Literal["under_45", "45_to_54", "55_to_64", "over_64"] = Field(
        ...,
        description="Patient age category. Under 45 years scores 0 points, 45-54 years scores 2 points, 55-64 years scores 3 points, over 64 years scores 4 points",
        example="45_to_54"
    )
    
    bmi: Literal["under_25", "25_to_30", "over_30"] = Field(
        ...,
        description="Body Mass Index category. Under 25 kg/m² scores 0 points, 25-30 kg/m² scores 1 point, 30 kg/m² or more scores 3 points",
        example="25_to_30"
    )
    
    waist_circumference: Literal["normal", "elevated", "high"] = Field(
        ...,
        description="Waist circumference category. Normal (Men <94cm, Women <80cm) scores 0 points, Elevated (Men 94-102cm, Women 80-88cm) scores 3 points, High (Men ≥102cm, Women ≥88cm) scores 4 points",
        example="normal"
    )
    
    gender: Literal["male", "female"] = Field(
        ...,
        description="Patient gender. Required for waist circumference thresholds interpretation",
        example="male"
    )
    
    physical_activity: Literal["yes", "no"] = Field(
        ...,
        description="Physical activity at least 30 minutes per day or ≥4 hours per week. Scores 0 points if yes, 2 points if no",
        example="yes"
    )
    
    fruit_vegetable_consumption: Literal["yes", "no"] = Field(
        ...,
        description="Daily consumption of fruits, vegetables, or berries. Scores 0 points if yes, 1 point if no",
        example="yes"
    )
    
    blood_pressure_medication: Literal["yes", "no"] = Field(
        ...,
        description="History of taking antihypertensive medication regularly. Scores 2 points if yes, 0 points if no",
        example="no"
    )
    
    high_blood_glucose_history: Literal["yes", "no"] = Field(
        ...,
        description="History of high blood glucose discovered during health examination, illness, or pregnancy. Scores 5 points if yes, 0 points if no",
        example="no"
    )
    
    family_diabetes_history: Literal["none", "second_degree", "first_degree"] = Field(
        ...,
        description="Family history of diabetes. None scores 0 points, 2nd degree relatives (grandparents, aunts, uncles, cousins) scores 3 points, 1st degree relatives (parents, siblings, children) scores 5 points",
        example="none"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": "45_to_54",
                "bmi": "25_to_30",
                "waist_circumference": "normal",
                "gender": "male",
                "physical_activity": "yes",
                "fruit_vegetable_consumption": "yes",
                "blood_pressure_medication": "no",
                "high_blood_glucose_history": "no",
                "family_diabetes_history": "none"
            }
        }


class FindriscResponse(BaseModel):
    """
    Response model for FINDRISC (Finnish Diabetes Risk Score)
    
    The FINDRISC score ranges from 0 to 26 points and classifies patients into:
    - Very Low (0-3 points): 1% 10-year diabetes risk
    - Low (4-8 points): 4% 10-year diabetes risk
    - Moderate (9-12 points): 17% 10-year diabetes risk
    - High (13-20 points): 33% 10-year diabetes risk
    - Very High (≥21 points): 50% 10-year diabetes risk
    
    Reference: Lindström J, Tuomilehto J. Diabetes Care. 2003;26(3):725-31.
    """
    
    result: int = Field(
        ...,
        description="FINDRISC score calculated from clinical and lifestyle variables (range: 0-26 points)",
        example=6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with gender-specific 10-year diabetes risk and recommended actions",
        example="Estimated 1 in 25 will develop diabetes within 10 years. 10-year risk: 0.8%"
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Very Low, Low, Moderate, High, Very High)",
        example="Low"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Low risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": "Estimated 1 in 25 will develop diabetes within 10 years. 10-year risk: 0.8%",
                "stage": "Low",
                "stage_description": "Low risk"
            }
        }