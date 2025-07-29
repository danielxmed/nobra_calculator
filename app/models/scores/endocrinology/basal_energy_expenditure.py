"""
Basal Energy Expenditure Models

Request and response models for Basal Energy Expenditure calculation.

References (Vancouver style):
1. Harris JA, Benedict FG. A biometric study of basal metabolism in man. 
   Washington DC: Carnegie Institute of Washington; 1919. Publication no. 279.
2. Roza AM, Shizgal HM. The Harris Benedict equation reevaluated: resting 
   energy requirements and the body cell mass. Am J Clin Nutr. 1984 Jul;40(1):168-82. 
   doi: 10.1093/ajcn/40.1.168.
3. Mifflin MD, St Jeor ST, Hill LA, Scott BJ, Daugherty SA, Koh YO. A new 
   predictive equation for resting energy expenditure in healthy individuals. 
   Am J Clin Nutr. 1990 Feb;51(2):241-7. doi: 10.1093/ajcn/51.2.241.

The Harris-Benedict equation estimates basal energy expenditure (BEE), which 
represents the minimum daily caloric requirements at rest. This can be adjusted 
by activity factors to calculate total daily energy expenditure (TDEE).
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Optional


class BasalEnergyExpenditureRequest(BaseModel):
    """
    Request model for Basal Energy Expenditure
    
    Uses the Harris-Benedict equation to calculate BEE:
    
    Men: BEE = 66.5 + (13.75 × weight in kg) + (5.003 × height in cm) - (6.775 × age)
    Women: BEE = 655.1 + (9.563 × weight in kg) + (1.850 × height in cm) - (4.676 × age)
    
    Activity Factors (optional):
    - Sedentary (little to no exercise): BEE × 1.2
    - Light exercise (1-3 days/week): BEE × 1.375
    - Moderate exercise (3-5 days/week): BEE × 1.55
    - Heavy exercise (6-7 days/week): BEE × 1.725
    - Very heavy exercise: BEE × 1.9
    
    References (Vancouver style):
    1. Harris JA, Benedict FG. A biometric study of basal metabolism in man. 
    Washington DC: Carnegie Institute of Washington; 1919. Publication no. 279.
    """
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Biological sex. Used to determine which Harris-Benedict equation to apply",
        example="male"
    )
    
    weight: float = Field(
        ...,
        description="Body weight in kilograms",
        gt=20,
        lt=300,
        example=70.0
    )
    
    height: float = Field(
        ...,
        description="Height in centimeters",
        gt=100,
        lt=250,
        example=175.0
    )
    
    age: int = Field(
        ...,
        description="Age in years",
        ge=18,
        le=120,
        example=30
    )
    
    activity_level: Optional[Literal["sedentary", "light", "moderate", "heavy", "very_heavy"]] = Field(
        None,
        description="Physical activity level for calculating Total Daily Energy Expenditure (TDEE). If not provided, only BEE is calculated",
        example="moderate"
    )
    
    @validator('weight')
    def validate_weight(cls, v):
        if v <= 20 or v >= 300:
            raise ValueError('Weight must be between 20 and 300 kg')
        return v
    
    @validator('height')
    def validate_height(cls, v):
        if v <= 100 or v >= 250:
            raise ValueError('Height must be between 100 and 250 cm')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "sex": "male",
                "weight": 70.0,
                "height": 175.0,
                "age": 30,
                "activity_level": "moderate"
            }
        }


class BasalEnergyExpenditureResponse(BaseModel):
    """
    Response model for Basal Energy Expenditure
    
    Returns either:
    - BEE (Basal Energy Expenditure) if no activity level specified
    - TDEE (Total Daily Energy Expenditure) if activity level is provided
    
    Reference: Harris JA, Benedict FG. Carnegie Institute of Washington; 1919.
    """
    
    result: float = Field(
        ...,
        description="Daily energy expenditure in kcal/day (either BEE or TDEE)",
        example=2418.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for energy expenditure",
        example="kcal/day"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including BEE classification and TDEE if applicable",
        example="Normal basal metabolic rate for most adults. Basal Energy Expenditure (BEE): 1560 kcal/day. Total Daily Energy Expenditure (TDEE) adjusted for moderate exercise (3-5 days/week): 2418 kcal/day."
    )
    
    stage: str = Field(
        ...,
        description="BEE classification (Low, Normal, High, Very High)",
        example="Normal"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the BEE category",
        example="Normal basal energy expenditure"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2418.0,
                "unit": "kcal/day",
                "interpretation": "Normal basal metabolic rate for most adults. Basal Energy Expenditure (BEE): 1560 kcal/day. Total Daily Energy Expenditure (TDEE) adjusted for moderate exercise (3-5 days/week): 2418 kcal/day.",
                "stage": "Normal",
                "stage_description": "Normal basal energy expenditure"
            }
        }