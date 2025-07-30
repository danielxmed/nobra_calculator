"""
Canadian Diabetes Risk Assessment Questionnaire (CANRISK) Models

Request and response models for CANRISK calculation.

References (Vancouver style):
1. Robinson CA, Agarwal G, Nerenberg K. Validating the CANRISK prognostic model 
   for assessing diabetes risk in Canada's multi-ethnic population. Chronic Dis 
   Inj Can. 2011 Dec;32(1):19-31. PMID: 22153173.
2. Public Health Agency of Canada. CANRISK: The Canadian Diabetes Risk Questionnaire 
   User Guide for Pharmacists. Ottawa: Public Health Agency of Canada; 2011.
3. Anand SS, Samaan Z, Middleton C, Irvine J, Desai D, Schulze KM, et al. 
   A digital health intervention to lower cardiovascular risk: a randomized 
   clinical trial. JAMA Cardiol. 2016 Aug 1;1(5):601-6. doi: 10.1001/jamacardio.2016.1035.

CANRISK is a validated screening tool for undiagnosed type 2 diabetes and prediabetes
in Canadian adults aged 18-74 years, accounting for Canada's multi-ethnic population.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class CanriskRequest(BaseModel):
    """
    Request model for Canadian Diabetes Risk Assessment Questionnaire (CANRISK)
    
    CANRISK screens for undiagnosed type 2 diabetes mellitus and prediabetes in 
    Canadian adults aged 18-74 years. It was developed by the Canadian Task Force 
    on Preventive Health Care in partnership with the Public Health Agency of Canada.
    
    Scoring system (maximum 86 points):
    - Age: 0-15 points (18-44: 0, 45-54: 7, 55-64: 13, 65-74: 15)
    - Gender: 0-6 points (female: 0, male: 6)
    - BMI: 0-14 points (<25: 0, 25-29: 4, 30-34: 9, ≥35: 14)
    - Waist circumference: 0-6 points (gender-specific thresholds)
    - Physical activity: 0-1 point (active: 0, inactive: 1)
    - Diet: 0-2 points (daily fruits/vegetables: 0, not daily: 2)
    - Blood pressure: 0-4 points (no/unknown: 0, yes: 4)
    - Blood sugar history: 0-14 points (no/unknown: 0, yes: 14)
    - Large baby (females): 0-1 point (no/unknown: 0, yes: 1)
    - Family diabetes: 0-8 points (none: 0, increases with number of relatives)
    - Ethnicity: 0-11 points (varies by ethnic background)
    
    Risk categories:
    - Low risk: <21 points
    - Moderate risk: 21-32 points
    - High risk: ≥33 points
    
    References (Vancouver style):
    1. Robinson CA, Agarwal G, Nerenberg K. Validating the CANRISK prognostic model 
    for assessing diabetes risk in Canada's multi-ethnic population. Chronic Dis 
    Inj Can. 2011 Dec;32(1):19-31.
    """
    
    age: Literal["18-44", "45-54", "55-64", "65-74"] = Field(
        ...,
        description="Age range. Points: 18-44 (0), 45-54 (7), 55-64 (13), 65-74 (15)",
        example="45-54"
    )
    
    gender: Literal["female", "male"] = Field(
        ...,
        description="Biological sex. Points: female (0), male (6)",
        example="male"
    )
    
    bmi: Literal["under_25", "25_to_29", "30_to_34", "35_or_over"] = Field(
        ...,
        description="Body Mass Index (kg/m²) category. Points: <25 (0), 25-29 (4), 30-34 (9), ≥35 (14)",
        example="25_to_29"
    )
    
    waist_circumference: Literal["small", "medium", "large"] = Field(
        ...,
        description="""Waist circumference measured at belly button level:
        Men: small <94cm (0 points), medium 94-102cm (4 points), large >102cm (6 points)
        Women: small <80cm (0 points), medium 80-88cm (4 points), large >88cm (6 points)""",
        example="medium"
    )
    
    physical_activity: Literal["yes", "no"] = Field(
        ...,
        description="Do you do at least 30 minutes of physical activity every day? (e.g., brisk walking, gardening, cleaning). Points: yes (0), no (1)",
        example="yes"
    )
    
    vegetable_fruit_consumption: Literal["every_day", "not_every_day"] = Field(
        ...,
        description="How often do you eat vegetables or fruits? Points: every day (0), not every day (2)",
        example="every_day"
    )
    
    high_blood_pressure: Literal["yes", "no", "dont_know"] = Field(
        ...,
        description="Ever told by doctor/nurse you have high blood pressure OR taken BP medication? Points: no/don't know (0), yes (4)",
        example="no"
    )
    
    high_blood_sugar: Literal["yes", "no", "dont_know"] = Field(
        ...,
        description="Ever found to have high blood sugar? (e.g., health exam, illness, pregnancy). Points: no/don't know (0), yes (14)",
        example="no"
    )
    
    large_baby: Literal["yes", "no", "dont_know", "not_applicable"] = Field(
        ...,
        description="Ever given birth to baby weighing ≥4kg (9lbs)? For females only. Points: no/don't know/NA (0), yes (1)",
        example="not_applicable"
    )
    
    family_diabetes: Literal["no", "one_relative", "two_relatives", "three_relatives", "all_relatives", "dont_know"] = Field(
        ...,
        description="Mother, father, sister, or brother with diabetes? Points: no/don't know (0), one (2), two (4), three (6), all (8)",
        example="one_relative"
    )
    
    ethnicity: Literal["white", "south_asian", "east_asian", "other"] = Field(
        ...,
        description="""Biological mother/father ethnicity (choose highest if multiple apply):
        - White/Other: 0 points
        - East Asian (Chinese, Vietnamese, Filipino, Korean, etc.): 10 points
        - South Asian (East Indian, Pakistani, Sri Lankan, etc.): 11 points""",
        example="white"
    )
    
    @validator('large_baby')
    def validate_large_baby(cls, v, values):
        if 'gender' in values and values['gender'] == 'male' and v != 'not_applicable':
            raise ValueError("Large baby question only applies to females")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "age": "45-54",
                "gender": "male",
                "bmi": "25_to_29",
                "waist_circumference": "medium",
                "physical_activity": "yes",
                "vegetable_fruit_consumption": "every_day",
                "high_blood_pressure": "no",
                "high_blood_sugar": "no",
                "large_baby": "not_applicable",
                "family_diabetes": "one_relative",
                "ethnicity": "white"
            }
        }


class CanriskResponse(BaseModel):
    """
    Response model for Canadian Diabetes Risk Assessment Questionnaire (CANRISK)
    
    CANRISK categorizes diabetes risk into three levels:
    - Low risk (<21 points): Low probability of prediabetes/diabetes
    - Moderate risk (21-32 points): Moderate probability, screening may be indicated
    - High risk (≥33 points): High probability, immediate screening recommended
    
    Validation:
    - Developed and validated in 6,223 Canadians
    - 12% of validation cohort were Aboriginal people
    - Adjusted for Canada's multi-ethnic population
    - For First Nations and Métis <40 years, lower cutoff of 21 may be more sensitive
    
    Reference: Robinson CA, et al. Chronic Dis Inj Can. 2011;32(1):19-31.
    """
    
    result: int = Field(
        ...,
        description="CANRISK total risk score (0-86 points)",
        example=25
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (points)",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommendations based on risk category",
        example="You have a moderate risk of having prediabetes or type 2 diabetes. You should discuss your risk with a healthcare practitioner and consider lifestyle modifications. Screening with fasting glucose or HbA1c may be recommended."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Moderate Risk, or High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="Moderate risk of type 2 diabetes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 25,
                "unit": "points",
                "interpretation": "You have a moderate risk of having prediabetes or type 2 diabetes. You should discuss your risk with a healthcare practitioner and consider lifestyle modifications. Screening with fasting glucose or HbA1c may be recommended.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate risk of type 2 diabetes"
            }
        }