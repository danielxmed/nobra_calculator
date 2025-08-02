"""
Kinetic Estimated Glomerular Filtration Rate (keGFR) Models

Request and response models for keGFR calculation.

References (Vancouver style):
1. Chen S. Retooling the creatinine clearance equation to estimate kinetic GFR 
   when the plasma creatinine is changing acutely. J Am Soc Nephrol. 2013 
   May;24(6):877-88.
2. O'Sullivan ED, Doyle A. The clinical utility of kinetic glomerular filtration 
   rate. Clin Kidney J. 2017 Apr;10(2):202-208.
3. Pickering JW, Ralib AM, Endre ZH. Combining creatinine and volume kinetics 
   identifies missed cases of acute kidney injury following cardiac arrest. 
   Crit Care. 2013 Jan 14;17(1):R7.
4. Dewitte A, Joannès-Boyau O, Sidobre C, Fleureau C, Bats ML, Derache P, et al. 
   Kinetic eGFR and Novel AKI Biomarkers to Predict Renal Recovery. Clin J Am Soc 
   Nephrol. 2015 Nov 6;10(11):1900-10.

The Kinetic Estimated Glomerular Filtration Rate (keGFR) is a dynamic assessment 
tool that estimates GFR during periods of non-steady-state creatinine levels. 
Unlike traditional eGFR equations that assume steady-state conditions, keGFR 
accounts for changing creatinine levels over time, making it particularly valuable 
for early detection of acute kidney injury (AKI).

Key clinical applications:
- Early AKI detection (8-24 hours before traditional criteria)
- Assessment of kidney function during acute illness
- Risk stratification in ICU and post-operative patients
- Monitoring kidney function recovery

The calculation combines baseline eGFR (using MDRD equation) with kinetic factors 
including creatinine change over time, volume of distribution, and creatinine 
production rate. A keGFR <30 mL/min/1.73 m² has 90% specificity for AKI with 
71% sensitivity.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict


class KineticEgfrRequest(BaseModel):
    """
    Request model for Kinetic Estimated Glomerular Filtration Rate (keGFR)
    
    The keGFR calculation requires demographic information and two creatinine 
    measurements separated by a known time interval:
    
    Required Parameters:
    - Age: Patient age in years (18-120)
    - Sex: Biological sex for MDRD equation adjustment
    - Race: Race category for MDRD equation calibration
    - Baseline creatinine: Most recent stable creatinine before acute illness
    - First creatinine: Initial measurement during acute phase
    - Second creatinine: Follow-up measurement
    - Time interval: Hours between the two creatinine measurements
    
    Clinical Context:
    - Most useful when creatinine is changing rapidly (non-steady state)
    - Requires at least 1 hour between creatinine measurements
    - Maximum recommended interval is 7 days (168 hours)
    - Baseline creatinine should represent stable kidney function
    
    Advantages over Traditional eGFR:
    - Accounts for non-steady-state conditions
    - Earlier detection of AKI (median 13.2 hours faster for Stage 1)
    - Better correlation with measured creatinine clearance during AKI
    - High specificity (90%) for AKI when keGFR <30 mL/min/1.73 m²
    
    Limitations:
    - Requires two creatinine measurements
    - Assumes normal creatinine production rate
    - Less accurate with rapidly changing muscle mass
    - Not validated in pediatric patients or pregnancy
    
    References (Vancouver style):
    1. Chen S. Retooling the creatinine clearance equation to estimate kinetic GFR 
       when the plasma creatinine is changing acutely. J Am Soc Nephrol. 2013 
       May;24(6):877-88.
    2. O'Sullivan ED, Doyle A. The clinical utility of kinetic glomerular filtration 
       rate. Clin Kidney J. 2017 Apr;10(2):202-208.
    """
    
    age: int = Field(
        ...,
        description="Patient age in years. Used for MDRD equation calculation.",
        ge=18,
        le=120,
        example=65
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Biological sex of the patient. Female patients have lower eGFR "
                   "for the same creatinine level (0.742 factor in MDRD equation).",
        example="male"
    )
    
    race: Literal["black", "non_black"] = Field(
        ...,
        description="Race category for MDRD equation calibration. Black patients "
                   "have higher eGFR for the same creatinine level (1.212 factor).",
        example="non_black"
    )
    
    baseline_creatinine: float = Field(
        ...,
        description="Baseline serum creatinine in mg/dL from before acute illness. "
                   "Should represent stable kidney function. Use most recent available "
                   "value from when patient was clinically stable.",
        ge=0.1,
        le=15.0,
        example=1.2
    )
    
    creatinine_1: float = Field(
        ...,
        description="First creatinine measurement in mg/dL during acute phase. "
                   "This is the initial measurement in the kinetic assessment.",
        ge=0.1,
        le=25.0,
        example=1.8
    )
    
    creatinine_2: float = Field(
        ...,
        description="Second creatinine measurement in mg/dL. This should be obtained "
                   "after the first measurement with a known time interval.",
        ge=0.1,
        le=25.0,
        example=2.4
    )
    
    time_hours: float = Field(
        ...,
        description="Time between first and second creatinine measurements in hours. "
                   "Minimum 1 hour for accuracy, maximum 7 days (168 hours). "
                   "Shorter intervals may be more accurate for rapidly changing conditions.",
        ge=1,
        le=168,
        example=24.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "sex": "male",
                "race": "non_black",
                "baseline_creatinine": 1.2,
                "creatinine_1": 1.8,
                "creatinine_2": 2.4,
                "time_hours": 24.0
            }
        }


class KineticEgfrResponse(BaseModel):
    """
    Response model for Kinetic Estimated Glomerular Filtration Rate (keGFR)
    
    Provides the calculated keGFR with comparison to baseline eGFR and clinical 
    interpretation for AKI risk assessment. The result includes both absolute 
    values and change from baseline to aid clinical decision-making.
    
    Interpretation Guidelines:
    - keGFR ≥60: Low AKI risk, preserved kidney function
    - keGFR 30-59: Intermediate AKI risk, moderate impairment
    - keGFR 15-29: High AKI risk, severe impairment  
    - keGFR <15: Very high AKI risk, kidney failure
    - keGFR <30: 90% specific for AKI (71% sensitive)
    
    Clinical Actions by keGFR Level:
    - ≥60: Routine monitoring, nephrotoxin avoidance
    - 30-59: Increased monitoring, avoid nephrotoxins, optimize perfusion
    - 15-29: Close monitoring, nephrology consultation, RRT preparation
    - <15: Urgent nephrology consultation, consider immediate RRT
    
    Advantages in Clinical Practice:
    - Earlier AKI detection compared to traditional criteria
    - Objective risk stratification in acute settings
    - Guides intensity of monitoring and intervention
    - Predicts need for renal replacement therapy
    - Useful for triaging patients in ICU settings
    
    Reference: Chen S. J Am Soc Nephrol. 2013;24(6):877-88.
    """
    
    result: Dict[str, float] = Field(
        ...,
        description="keGFR calculation results including kinetic eGFR, baseline eGFR, and change",
        example={
            "kinetic_egfr": 35.2,
            "baseline_egfr": 58.7,
            "change_in_gfr": -23.5
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for GFR values",
        example="mL/min/1.73 m²"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including AKI risk assessment, percent change "
                   "from baseline, and management recommendations based on keGFR level",
        example="Kinetic eGFR: 35.2 mL/min/1.73 m² (baseline: 58.7). Change from baseline: -23.5 mL/min/1.73 m² (-40.0%). Moderate kidney impairment with intermediate AKI risk. Increase monitoring frequency, avoid nephrotoxins, ensure adequate perfusion, and consider nephrology consultation if deteriorating."
    )
    
    stage: str = Field(
        ...,
        description="AKI risk category (Low AKI Risk, Intermediate AKI Risk, High AKI Risk, Very High AKI Risk)",
        example="Intermediate AKI Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the kidney function level",
        example="Moderate kidney dysfunction"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "kinetic_egfr": 35.2,
                    "baseline_egfr": 58.7,
                    "change_in_gfr": -23.5
                },
                "unit": "mL/min/1.73 m²",
                "interpretation": "Kinetic eGFR: 35.2 mL/min/1.73 m² (baseline: 58.7). Change from baseline: -23.5 mL/min/1.73 m² (-40.0%). Moderate kidney impairment with intermediate AKI risk. Increase monitoring frequency, avoid nephrotoxins, ensure adequate perfusion, and consider nephrology consultation if deteriorating.",
                "stage": "Intermediate AKI Risk",
                "stage_description": "Moderate kidney dysfunction"
            }
        }