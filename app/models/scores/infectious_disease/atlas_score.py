"""
ATLAS Score for Clostridium Difficile Infection Models

Request and response models for ATLAS Score calculation.

References (Vancouver style):
1. Miller MA, Louie T, Mullane K, Weiss K, Lentnek A, Golan Y, et al. 
   Derivation and validation of a simple clinical bedside score (ATLAS) for 
   Clostridium difficile infection which predicts response to vancomycin therapy. 
   BMC Infect Dis. 2013;13:148.
2. Cohen SH, Gerding DN, Johnson S, Kelly CP, Loo VG, McDonald LC, et al. 
   Clinical practice guidelines for Clostridium difficile infection in adults: 
   2010 update by the society for healthcare epidemiology of America (SHEA) 
   and the infectious diseases society of America (IDSA). 
   Infect Control Hosp Epidemiol. 2010;31(5):431-55.

The ATLAS score predicts response to vancomycin therapy in patients with 
Clostridium difficile infection (CDI). It helps identify patients at high risk 
for treatment failure who may benefit from alternative therapeutic approaches.
"""

from pydantic import BaseModel, Field
from typing import List


class AtlasScoreRequest(BaseModel):
    """
    Request model for ATLAS Score
    
    The ATLAS score uses 5 clinical parameters to predict response to vancomycin 
    therapy in C. diff patients:
    
    Age ≥65 years: +1 point
    - Elderly patients have increased risk of treatment failure
    
    Treatment with Systemic Antibiotics: +2 points (highest weight)
    - Concomitant antibiotic use disrupts normal gut flora
    - Most significant predictor of treatment failure
    
    Leukocytosis >15,000/μL: +1 point
    - Indicates severe inflammatory response
    - Marker of disease severity
    
    Albumin <2.5 g/dL: +1 point
    - Reflects poor nutritional status and disease severity
    - Associated with worse outcomes
    
    Serum Creatinine >1.5× baseline: +1 point
    - Indicates renal dysfunction
    - May reflect systemic toxicity from CDI

    Score Interpretation:
    - 0-2 points: Low Risk (Good response to vancomycin expected)
    - 3-6 points: High Risk (Poor response to vancomycin expected)

    References (Vancouver style):
    1. Miller MA, Louie T, Mullane K, Weiss K, Lentnek A, Golan Y, et al. 
    Derivation and validation of a simple clinical bedside score (ATLAS) for 
    Clostridium difficile infection which predicts response to vancomycin therapy. 
    BMC Infect Dis. 2013;13:148.
    2. Cohen SH, Gerding DN, Johnson S, Kelly CP, Loo VG, McDonald LC, et al. 
    Clinical practice guidelines for Clostridium difficile infection in adults: 
    2010 update by the society for healthcare epidemiology of America (SHEA) 
    and the infectious diseases society of America (IDSA). 
    Infect Control Hosp Epidemiol. 2010;31(5):431-55.
    """
    
    age_65_or_older: bool = Field(
        ...,
        description="Patient is 65 years of age or older",
        example=True
    )
    
    systemic_antibiotics: bool = Field(
        ...,
        description="Currently on systemic antibiotic therapy (other than for C. diff treatment)",
        example=False
    )
    
    leukocytosis: bool = Field(
        ...,
        description="White blood cell count greater than 15,000 cells per microliter",
        example=True
    )
    
    low_albumin: bool = Field(
        ...,
        description="Serum albumin level less than 2.5 g/dL (25 g/L)",
        example=False
    )
    
    elevated_creatinine: bool = Field(
        ...,
        description="Serum creatinine level greater than 1.5 times the baseline/normal value",
        example=False
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_65_or_older": True,
                "systemic_antibiotics": False,
                "leukocytosis": True,
                "low_albumin": False,
                "elevated_creatinine": False
            }
        }


class AtlasScoreResponse(BaseModel):
    """
    Response model for ATLAS Score
    
    The ATLAS score stratifies patients with C. difficile infection into:
    - Low Risk (0-2 points): Good response to vancomycin therapy expected
    - High Risk (3-6 points): Poor response to vancomycin therapy expected
    
    High-risk patients may benefit from alternative therapies such as fidaxomicin 
    or fecal microbiota transplantation rather than standard vancomycin treatment.
    
    Reference: Miller MA, et al. BMC Infect Dis. 2013;13:148.
    """
    
    score: int = Field(
        ...,
        description="Total ATLAS score (0-6 points)",
        example=2,
        ge=0,
        le=6
    )
    
    max_score: int = Field(
        ...,
        description="Maximum possible score",
        example=6
    )
    
    result: str = Field(
        ...,
        description="Score result with units",
        example="2 points"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="points"
    )
    
    risk_level: str = Field(
        ...,
        description="Risk level classification for treatment response",
        example="Low Risk"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the score with treatment recommendations",
        example="Good response to vancomycin therapy expected. Low risk of treatment failure. Standard vancomycin therapy should be effective. Monitor clinical response."
    )
    
    management: str = Field(
        ...,
        description="Treatment management recommendations based on risk level",
        example="Standard vancomycin therapy should be effective. Monitor clinical response."
    )
    
    breakdown: List[str] = Field(
        ...,
        description="Breakdown of points contributing to the total score",
        example=["Age ≥65 years: +1", "Leukocytosis >15,000/μL: +1"]
    )
    
    ranges: dict = Field(
        ...,
        description="Score interpretation ranges",
        example={
            "low_risk": "0-2 points: Low Risk (Good response to vancomycin therapy expected)",
            "high_risk": "3-6 points: High Risk (Poor response to vancomycin therapy expected)"
        }
    )
    
    clinical_notes: List[str] = Field(
        ...,
        description="Important clinical notes and limitations",
        example=[
            "Derived and validated specifically for vancomycin therapy",
            "May not apply to other C. diff treatments",
            "Consider clinical judgment alongside score",
            "Not validated for pediatric patients"
        ]
    )
    
    class Config:
        schema_extra = {
            "example": {
                "score": 2,
                "max_score": 6,
                "result": "2 points",
                "unit": "points",
                "risk_level": "Low Risk",
                "interpretation": "Good response to vancomycin therapy expected. Low risk of treatment failure. Standard vancomycin therapy should be effective. Monitor clinical response.",
                "management": "Standard vancomycin therapy should be effective. Monitor clinical response.",
                "breakdown": ["Age ≥65 years: +1", "Leukocytosis >15,000/μL: +1"],
                "ranges": {
                    "low_risk": "0-2 points: Low Risk (Good response to vancomycin therapy expected)",
                    "high_risk": "3-6 points: High Risk (Poor response to vancomycin therapy expected)"
                },
                "clinical_notes": [
                    "Derived and validated specifically for vancomycin therapy",
                    "May not apply to other C. diff treatments",
                    "Consider clinical judgment alongside score",
                    "Not validated for pediatric patients"
                ]
            }
        }
