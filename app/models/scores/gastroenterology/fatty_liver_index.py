"""
Fatty Liver Index Models

Request and response models for Fatty Liver Index calculation.

References (Vancouver style):
1. Bedogni G, Bellentani S, Miglioli L, Masutti F, Passalacqua M, Castiglione A, 
   Tiribelli C. The Fatty Liver Index: a simple and accurate predictor of hepatic 
   steatosis in the general population. BMC Gastroenterol. 2006 Nov 2;6:33. 
   doi: 10.1186/1471-230X-6-33.
2. Cuthbertson DJ, Weickert MO, Lythgoe D, Sprung VS, Dobson R, Shoajee-Moradie F, 
   et al. External validation of the fatty liver index and lipid accumulation product 
   indices, using 1H-magnetic resonance spectroscopy, to identify hepatic steatosis 
   in healthy controls and obese, insulin-resistant individuals. Eur J Endocrinol. 
   2014 Nov;171(5):561-9. doi: 10.1530/EJE-14-0112.
3. Koehler EM, Schouten JN, Hansen BE, Hofman A, Stricker BH, Janssen HL. External 
   validation of the fatty liver index for identifying nonalcoholic fatty liver 
   disease in a population-based study. Clin Gastroenterol Hepatol. 2013 Sep;11(9):1201-4. 
   doi: 10.1016/j.cgh.2012.12.031.

The Fatty Liver Index (FLI) is a simple and accurate predictor of hepatic steatosis 
that uses only four readily available measurements: triglycerides, BMI, GGT, and 
waist circumference. It provides a non-invasive method to rule in or rule out fatty 
liver disease with good diagnostic accuracy (AUROC 0.84).
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class FattyLiverIndexRequest(BaseModel):
    """
    Request model for Fatty Liver Index calculation
    
    The FLI uses 4 commonly available clinical parameters to predict fatty liver:
    
    1. Triglycerides: High levels of serum triglycerides are associated with fatty 
       liver, pancreatitis, and kidney disease. Normal range: <150 mg/dL.
    
    2. BMI (Body Mass Index): Calculated as weight(kg)/height(m)². Obesity is a 
       major risk factor for non-alcoholic fatty liver disease (NAFLD).
    
    3. GGT (Gamma-glutamyl transpeptidase): An enzyme found in liver tissue that 
       serves as a marker for liver function. Elevated in various liver diseases.
    
    4. Waist Circumference: Central obesity is particularly associated with NAFLD. 
       Measured at the midpoint between the lower costal margin and iliac crest.
    
    The formula uses natural logarithms for triglycerides and GGT values to account 
    for their non-linear relationships with fatty liver risk.
    
    References (Vancouver style):
    1. Bedogni G, Bellentani S, Miglioli L, Masutti F, Passalacqua M, Castiglione A, 
       Tiribelli C. The Fatty Liver Index: a simple and accurate predictor of hepatic 
       steatosis in the general population. BMC Gastroenterol. 2006 Nov 2;6:33.
    """
    
    triglycerides: float = Field(
        ...,
        gt=0,
        le=1000,
        description="Serum triglycerides level in mg/dL. High levels are associated with fatty liver disease. Normal: <150 mg/dL, Borderline high: 150-199 mg/dL, High: 200-499 mg/dL, Very high: ≥500 mg/dL",
        example=120.0
    )
    
    bmi: float = Field(
        ...,
        ge=10,
        le=60,
        description="Body Mass Index in kg/m². Categories: Underweight: <18.5, Normal: 18.5-24.9, Overweight: 25-29.9, Obese Class I: 30-34.9, Obese Class II: 35-39.9, Obese Class III: ≥40",
        example=26.5
    )
    
    ggt: float = Field(
        ...,
        gt=0,
        le=1000,
        description="Gamma-glutamyl transpeptidase in U/L. Enzyme marker for liver function. Normal range varies by sex: Men: 8-61 U/L, Women: 5-36 U/L. Elevated in various liver diseases",
        example=35.0
    )
    
    waist_circumference: float = Field(
        ...,
        ge=40,
        le=200,
        description="Waist circumference in cm, measured at midpoint between lower costal margin and iliac crest. Risk thresholds: Men: ≥94 cm (moderate risk), ≥102 cm (high risk); Women: ≥80 cm (moderate risk), ≥88 cm (high risk)",
        example=90.0
    )
    
    @field_validator('triglycerides', 'ggt')
    def validate_positive_lab_values(cls, v, info):
        if v <= 0:
            raise ValueError(f"{info.field_name} must be a positive value")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "triglycerides": 120.0,
                "bmi": 26.5,
                "ggt": 35.0,
                "waist_circumference": 90.0
            }
        }


class FattyLiverIndexResponse(BaseModel):
    """
    Response model for Fatty Liver Index calculation
    
    The FLI score ranges from 0 to 100 and has established cutoffs:
    - <30: Fatty liver ruled out (negative likelihood ratio = 0.2)
    - 30-60: Indeterminate (neither ruled in nor ruled out)
    - ≥60: Fatty liver ruled in (positive likelihood ratio = 4.3)
    
    Performance characteristics:
    - Accuracy (AUROC): 0.84 (95% CI 0.81-0.87)
    - At FLI ≥60: PPV 99%, NPV 15%
    - Validated in general population and externally validated in multiple cohorts
    
    Reference: Bedogni G, et al. BMC Gastroenterol. 2006;6:33.
    """
    
    result: float = Field(
        ...,
        description="Fatty Liver Index score (0-100 scale)",
        example=42.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended actions based on the FLI score",
        example="Fatty liver neither ruled in nor ruled out. Further evaluation may be needed."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Indeterminate Risk, High Risk)",
        example="Indeterminate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Inconclusive"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 42.5,
                "unit": "points",
                "interpretation": "Fatty liver neither ruled in nor ruled out. Further evaluation may be needed.",
                "stage": "Indeterminate Risk",
                "stage_description": "Inconclusive"
            }
        }