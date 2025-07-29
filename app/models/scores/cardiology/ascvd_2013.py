"""
ASCVD (Atherosclerotic Cardiovascular Disease) 2013 Risk Calculator Models

Request and response models for ASCVD 2013 risk calculation.

References (Vancouver style):
1. Goff DC Jr, Lloyd-Jones DM, Bennett G, Coady S, D'Agostino RB Sr, Gibbons R, et al. 
   2013 ACC/AHA guideline on the assessment of cardiovascular risk: a report of the 
   American College of Cardiology/American Heart Association Task Force on Practice 
   Guidelines. Circulation. 2014 Jun 24;129(25 Suppl 2):S49-73. 
   doi: 10.1161/01.cir.0000437741.48606.98.
2. Stone NJ, Robinson JG, Lichtenstein AH, Bairey Merz CN, Blum CB, Eckel RH, et al. 
   2013 ACC/AHA guideline on the treatment of blood cholesterol to reduce atherosclerotic 
   cardiovascular risk in adults: a report of the American College of Cardiology/American 
   Heart Association Task Force on Practice Guidelines. Circulation. 2014 Jun 24;129(25 
   Suppl 2):S1-45. doi: 10.1161/01.cir.0000437738.63853.7a.
3. Arnett DK, Blumenthal RS, Albert MA, Buroker AB, Goldberger ZD, Hahn EJ, et al. 
   2019 ACC/AHA Guideline on the Primary Prevention of Cardiovascular Disease: A Report 
   of the American College of Cardiology/American Heart Association Task Force on Clinical 
   Practice Guidelines. Circulation. 2019 Sep 10;140(11):e596-e646. 
   doi: 10.1161/CIR.0000000000000678.

The 2013 ASCVD Risk Calculator uses the Pooled Cohort Equations to estimate 10-year risk 
of a first atherosclerotic cardiovascular disease (ASCVD) event, defined as nonfatal 
myocardial infarction or coronary heart disease death, or fatal or nonfatal stroke. 
This calculator is intended for patients aged 40-79 years with no prior history of ASCVD.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class Ascvd2013Request(BaseModel):
    """
    Request model for ASCVD (Atherosclerotic Cardiovascular Disease) 2013 Risk Calculator
    
    The ASCVD Risk Calculator uses the Pooled Cohort Equations to estimate 10-year risk
    of a first ASCVD event (nonfatal MI, CHD death, or fatal/nonfatal stroke).
    
    Key Parameters:
    - Age: Must be between 40-79 years (outside this range, calculator not applicable)
    - Sex: Biological sex affects risk calculation
    - Race: Equations are race-specific for White and African American populations
    - Total Cholesterol: Range 130-320 mg/dL
    - HDL Cholesterol: Range 20-100 mg/dL  
    - Systolic BP: Range 90-200 mmHg
    - BP Treatment: Whether patient is on antihypertensive medication
    - Diabetes: Presence of diabetes mellitus
    - Smoker: Current smoking status
    
    Important Notes:
    - For patients of other races, the calculator uses White race coefficients
    - Not applicable for patients with prior ASCVD or LDL-C ≥190 mg/dL
    - May overestimate risk in some contemporary populations
    
    References (Vancouver style):
    1. Goff DC Jr, Lloyd-Jones DM, Bennett G, et al. 2013 ACC/AHA guideline on the 
       assessment of cardiovascular risk. Circulation. 2014;129(25 Suppl 2):S49-73.
    """
    
    age: int = Field(
        ...,
        ge=40,
        le=79,
        description="Patient's age in years. Must be between 40 and 79 years. Calculator not applicable outside this range",
        example=55
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient's biological sex. Affects risk calculation with sex-specific coefficients",
        example="male"
    )
    
    race: Literal["white", "african_american", "other"] = Field(
        ...,
        description="Patient's race. Pooled Cohort Equations have race-specific coefficients for White and African American populations. For 'other' races, White coefficients are used",
        example="white"
    )
    
    total_cholesterol: float = Field(
        ...,
        ge=130,
        le=320,
        description="Total cholesterol level in mg/dL. Valid range: 130-320 mg/dL",
        example=213
    )
    
    hdl_cholesterol: float = Field(
        ...,
        ge=20,
        le=100,
        description="HDL cholesterol level in mg/dL. Valid range: 20-100 mg/dL",
        example=50
    )
    
    systolic_bp: int = Field(
        ...,
        ge=90,
        le=200,
        description="Systolic blood pressure in mmHg. Valid range: 90-200 mmHg",
        example=120
    )
    
    bp_treatment: bool = Field(
        ...,
        description="Currently on blood pressure lowering medication (antihypertensive treatment)",
        example=False
    )
    
    diabetes: bool = Field(
        ...,
        description="History of diabetes mellitus (Type 1 or Type 2)",
        example=False
    )
    
    smoker: bool = Field(
        ...,
        description="Current smoker of cigarettes, cigars, or pipe. Former smokers who quit are considered non-smokers",
        example=False
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 55,
                "sex": "male",
                "race": "white",
                "total_cholesterol": 213,
                "hdl_cholesterol": 50,
                "systolic_bp": 120,
                "bp_treatment": False,
                "diabetes": False,
                "smoker": False
            }
        }


class Ascvd2013Response(BaseModel):
    """
    Response model for ASCVD 2013 Risk Calculator
    
    Returns the 10-year ASCVD risk percentage with clinical interpretation and 
    treatment recommendations based on 2013 ACC/AHA guidelines.
    
    Risk Categories:
    - Low Risk (<5%): Lifestyle modifications
    - Borderline Risk (5% to <7.5%): Consider risk enhancers, lifestyle modifications
    - Intermediate Risk (7.5% to <20%): Moderate- to high-intensity statin therapy
    - High Risk (≥20%): High-intensity statin therapy
    
    Reference: Goff DC Jr, et al. Circulation. 2014;129(25 Suppl 2):S49-73.
    """
    
    result: float = Field(
        ...,
        description="10-year ASCVD risk percentage calculated using Pooled Cohort Equations",
        example=5.3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk",
        example="%"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and treatment recommendations based on risk level",
        example="Borderline 10-year ASCVD risk. Consider risk-enhancing factors. Emphasize lifestyle modifications. For selected patients, consider moderate-intensity statin therapy after risk discussion."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Borderline Risk, Intermediate Risk, High Risk)",
        example="Borderline Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the risk category with percentage range",
        example="5.3% 10-year risk"
    )
    
    details: dict = Field(
        ...,
        description="Additional calculation details including race group used and baseline survival",
        example={
            "race_group": "white",
            "sex": "male",
            "individual_sum": 60.69,
            "mean_coefficient_sum": 61.18,
            "baseline_survival": 0.9144
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5.3,
                "unit": "%",
                "interpretation": "Borderline 10-year ASCVD risk. Consider risk-enhancing factors. Emphasize lifestyle modifications. For selected patients, consider moderate-intensity statin therapy after risk discussion.",
                "stage": "Borderline Risk",
                "stage_description": "5.3% 10-year risk",
                "details": {
                    "race_group": "white",
                    "sex": "male",
                    "individual_sum": 60.69,
                    "mean_coefficient_sum": 61.18,
                    "baseline_survival": 0.9144
                }
            }
        }