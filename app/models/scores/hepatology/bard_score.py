"""
BARD Score for NAFLD Fibrosis Models

Request and response models for BARD score calculation.

References (Vancouver style):
1. Harrison SA, Oliver D, Arnold HL, Gogia S, Neuschwander-Tetri BA. Development 
   and validation of a simple NAFLD clinical scoring system for identifying 
   patients without advanced disease. Gut. 2008 Oct;57(10):1441-7. 
   doi: 10.1136/gut.2007.146019.
2. Raszeja-Wyszomirska J, Szymanik B, Ławniczak M, Kajor M, Chwist A, Milkiewicz P, 
   et al. Validation of the BARD scoring system in Polish patients with nonalcoholic 
   fatty liver disease (NAFLD). BMC Gastroenterol. 2010 Jun 17;10:67. 
   doi: 10.1186/1471-230X-10-67.
3. Cichoż-Lach H, Celiński K, Prozorow-Król B, Swatek J, Słomka M, Lach T. The 
   BARD score and the NAFLD fibrosis score in the assessment of advanced liver 
   fibrosis in nonalcoholic fatty liver disease. Med Sci Monit. 2012 Dec;18(12):CR735-40. 
   doi: 10.12659/msm.883601.

The BARD score is a simple non-invasive scoring system that uses BMI, AST/ALT ratio, 
and diabetes status to predict the risk of advanced fibrosis (F3-F4) in patients 
with non-alcoholic fatty liver disease (NAFLD). It has a high negative predictive 
value (96%) for scores 0-1, making it useful for identifying patients who are 
unlikely to have advanced fibrosis and may not require liver biopsy.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class BardScoreRequest(BaseModel):
    """
    Request model for BARD Score for NAFLD Fibrosis
    
    The BARD score uses three clinical parameters to assess fibrosis risk:
    
    Scoring System:
    - BMI ≥28 kg/m²: 1 point
    - AST/ALT ratio ≥0.8: 2 points
    - Diabetes mellitus: 1 point
    
    Total score ranges from 0-4 points:
    - Score 0-1: Low risk of advanced fibrosis
    - Score 2-4: High risk of advanced fibrosis
    
    BARD stands for BMI, AST/ALT Ratio, Diabetes
    
    References (Vancouver style):
    1. Harrison SA, Oliver D, Arnold HL, Gogia S, Neuschwander-Tetri BA. Development 
    and validation of a simple NAFLD clinical scoring system for identifying 
    patients without advanced disease. Gut. 2008 Oct;57(10):1441-7. 
    doi: 10.1136/gut.2007.146019.
    """
    
    bmi: float = Field(
        ...,
        description="Body Mass Index calculated as weight(kg)/height(m)². Scores 1 point if ≥28 kg/m²",
        gt=10,
        lt=70,
        example=29.5
    )
    
    ast: float = Field(
        ...,
        description="Aspartate aminotransferase (AST) in U/L. Used to calculate AST/ALT ratio",
        gt=0,
        le=5000,
        example=45
    )
    
    alt: float = Field(
        ...,
        description="Alanine aminotransferase (ALT) in U/L. Used to calculate AST/ALT ratio. Scores 2 points if AST/ALT ≥0.8",
        gt=0,
        le=5000,
        example=50
    )
    
    diabetes: Literal["yes", "no"] = Field(
        ...,
        description="Presence of type 2 diabetes mellitus. Scores 1 point if present",
        example="yes"
    )
    
    @field_validator('alt')
    def validate_alt_not_zero(cls, v):
        if v == 0:
            raise ValueError('ALT cannot be zero (division by zero in AST/ALT ratio)')
        return v
    
    @field_validator('ast', 'alt')
    def validate_liver_enzymes(cls, v):
        if v <= 0:
            raise ValueError('Liver enzymes must be positive values')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "bmi": 29.5,
                "ast": 45,
                "alt": 50,
                "diabetes": "yes"
            }
        }


class BardScoreResponse(BaseModel):
    """
    Response model for BARD Score for NAFLD Fibrosis
    
    The BARD score interpretation:
    - Score 0-1: Low risk of advanced fibrosis (NPV 96%)
    - Score 2-4: High risk of advanced fibrosis (OR 17, 95% CI 9.2-31.9)
    
    Reference: Harrison SA, et al. Gut. 2008;57(10):1441-7.
    """
    
    result: int = Field(
        ...,
        description="BARD score (0-4 points)",
        ge=0,
        le=4,
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including risk assessment and recommendations",
        example="Score 2-4 indicates high risk of advanced fibrosis (F3-F4). Odds ratio 17 (95% CI 9.2-31.9) for advanced fibrosis. Consider liver biopsy or non-invasive imaging (e.g., FibroScan) for further evaluation."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk or High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="High risk of advanced fibrosis"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "Score 2-4 indicates high risk of advanced fibrosis (F3-F4). Odds ratio 17 (95% CI 9.2-31.9) for advanced fibrosis. Consider liver biopsy or non-invasive imaging (e.g., FibroScan) for further evaluation.",
                "stage": "High Risk",
                "stage_description": "High risk of advanced fibrosis"
            }
        }