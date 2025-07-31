"""
Cardiovascular Risk in Orthotopic Liver Transplantation (CAR-OLT) Models

Request and response models for CAR-OLT calculation.

References (Vancouver style):
1. VanWagner LB, Ning H, Whitsett M, Levitsky J, Uttal S, Wilkins JT, Abecassis MM, 
   Ladner DP, Skaro AI, Lloyd-Jones DM. A point-based prediction model for cardiovascular 
   risk in orthotopic liver transplantation: The CAR-OLT score. Hepatology. 2017 Dec;66(6):1968-1979. 
   doi: 10.1002/hep.29329.
2. VanWagner LB, Serper M, Kang R, Levitsky J, Hohmann S, Abecassis M, Skaro A, 
   Lloyd-Jones DM. Factors Associated With Major Adverse Cardiovascular Events After 
   Liver Transplantation Among a National Sample. Am J Transplant. 2016 Sep;16(9):2684-94. 
   doi: 10.1111/ajt.13779.

The CAR-OLT score is a point-based prediction model that estimates the 1-year risk of 
death or hospitalization related to a major cardiovascular event (myocardial infarction, 
cardiac revascularization, heart failure, atrial fibrillation, cardiac arrest, pulmonary 
embolism, or stroke) after orthotopic liver transplantation. The score ranges from -6 to 
over 60 points, incorporating 12 clinical variables easily obtained at the point of care.
"""

from pydantic import BaseModel, Field
from typing import Literal


class CarOltRequest(BaseModel):
    """
    Request model for Cardiovascular Risk in Orthotopic Liver Transplantation (CAR-OLT)
    
    The CAR-OLT score uses 12 clinical variables to predict 1-year cardiovascular risk 
    after liver transplantation:
    
    Demographics:
    - Age category: Under 45 (0 points), 45-49 (-6 points), 50-54 (-4 points), 
      55-59 (+2 points), 60-64 (+5 points), ≥65 (+8 points)
    - Sex: Male (0 points), Female (+1 point)
    - Race: Other (0 points), White (+7 points), Black (+10 points)
    
    Socioeconomic factors:
    - Working status: Working for income (0 points), Not working (+10 points)
    - Education: College or higher (0 points), High school or less/unknown (+5 points)
    
    Medical conditions (yes/no):
    - Atrial fibrillation (+25 points if yes)
    - Respiratory failure on ventilator (+13 points if yes)
    - Pulmonary hypertension (+9 points if yes)
    - Hepatocellular carcinoma (0 points if yes, +6 points if no)
    - Hypertension (+4 points if yes)
    - Diabetes (+4 points if yes)
    - Heart failure (+7 points if yes)

    References (Vancouver style):
    1. VanWagner LB, Ning H, Whitsett M, Levitsky J, Uttal S, Wilkins JT, Abecassis MM, 
    Ladner DP, Skaro AI, Lloyd-Jones DM. A point-based prediction model for cardiovascular 
    risk in orthotopic liver transplantation: The CAR-OLT score. Hepatology. 2017 Dec;66(6):1968-1979. 
    doi: 10.1002/hep.29329.
    2. VanWagner LB, Serper M, Kang R, Levitsky J, Hohmann S, Abecassis M, Skaro A, 
    Lloyd-Jones DM. Factors Associated With Major Adverse Cardiovascular Events After 
    Liver Transplantation Among a National Sample. Am J Transplant. 2016 Sep;16(9):2684-94. 
    doi: 10.1111/ajt.13779.
    """
    
    age_category: Literal["under_45", "45_to_49", "50_to_54", "55_to_59", "60_to_64", "65_or_over"] = Field(
        ...,
        description="Patient age category at time of transplant. Under 45 scores 0 points, 45-49 scores -6 points, 50-54 scores -4 points, 55-59 scores +2 points, 60-64 scores +5 points, 65 or over scores +8 points",
        example="55_to_59"
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient sex. Male scores 0 points, female scores +1 point",
        example="male"
    )
    
    race: Literal["white", "black", "other"] = Field(
        ...,
        description="Patient race. Other races score 0 points, white scores +7 points, black scores +10 points",
        example="white"
    )
    
    working_status: Literal["yes", "no"] = Field(
        ...,
        description="Employment status - working for income. Working scores 0 points, not working scores +10 points",
        example="no"
    )
    
    education: Literal["college_or_higher", "high_school_or_less_unknown"] = Field(
        ...,
        description="Education level. College or higher scores 0 points, high school or less/unknown scores +5 points",
        example="high_school_or_less_unknown"
    )
    
    atrial_fibrillation: Literal["yes", "no"] = Field(
        ...,
        description="History of atrial fibrillation. Scores +25 points if yes",
        example="no"
    )
    
    respiratory_failure_ventilator: Literal["yes", "no"] = Field(
        ...,
        description="Respiratory failure requiring ventilator support. Scores +13 points if yes",
        example="no"
    )
    
    pulmonary_hypertension: Literal["yes", "no"] = Field(
        ...,
        description="Presence of pulmonary hypertension. Scores +9 points if yes",
        example="no"
    )
    
    hepatocellular_carcinoma: Literal["yes", "no"] = Field(
        ...,
        description="Presence of hepatocellular carcinoma (HCC). Scores 0 points if yes, +6 points if no",
        example="yes"
    )
    
    hypertension: Literal["yes", "no"] = Field(
        ...,
        description="History of hypertension. Scores +4 points if yes",
        example="yes"
    )
    
    diabetes: Literal["yes", "no"] = Field(
        ...,
        description="History of diabetes mellitus. Scores +4 points if yes",
        example="no"
    )
    
    heart_failure: Literal["yes", "no"] = Field(
        ...,
        description="History of heart failure. Scores +7 points if yes",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age_category": "55_to_59",
                "sex": "male",
                "race": "white",
                "working_status": "no",
                "education": "high_school_or_less_unknown",
                "atrial_fibrillation": "no",
                "respiratory_failure_ventilator": "no",
                "pulmonary_hypertension": "no",
                "hepatocellular_carcinoma": "yes",
                "hypertension": "yes",
                "diabetes": "no",
                "heart_failure": "no"
            }
        }


class CarOltResponse(BaseModel):
    """
    Response model for Cardiovascular Risk in Orthotopic Liver Transplantation (CAR-OLT)
    
    The CAR-OLT score provides risk stratification for 1-year cardiovascular events:
    - Very Low (<10 points): <5% risk
    - Low (10-15 points): 6-8% risk  
    - Moderate (16-30 points): 10-26% risk
    - High (31-36 points): 30-38% risk
    - Very High (≥37 points): ≥40% risk
    
    Major cardiovascular events include: MI, cardiac revascularization (PCI or CABG), 
    heart failure, atrial fibrillation, cardiac arrest, pulmonary embolism, or stroke.
    
    Reference: VanWagner LB, et al. Hepatology. 2017;66(6):1968-1979.
    """
    
    result: int = Field(
        ...,
        description="CAR-OLT score calculated from clinical variables (range: -6 to over 60 points)",
        example=22
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of 1-year cardiovascular risk after liver transplantation",
        example="10-26% 1-year risk of death or hospitalization related to a major cardiovascular event (MI, cardiac revascularization, heart failure, atrial fibrillation, cardiac arrest, pulmonary embolism, or stroke) after liver transplantation"
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Very Low, Low, Moderate, High, Very High)",
        example="Moderate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Moderate cardiovascular risk"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 22,
                "unit": "points",
                "interpretation": "10-26% 1-year risk of death or hospitalization related to a major cardiovascular event (MI, cardiac revascularization, heart failure, atrial fibrillation, cardiac arrest, pulmonary embolism, or stroke) after liver transplantation",
                "stage": "Moderate",
                "stage_description": "Moderate cardiovascular risk"
            }
        }