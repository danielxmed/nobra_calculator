"""
Acute Decompensated Heart Failure National Registry (ADHERE) Algorithm Models

Request and response models for ADHERE Algorithm calculation.

References (Vancouver style):
1. Fonarow GC, Adams KF Jr, Abraham WT, Yancy CW, Boscardin WJ; ADHERE Scientific 
   Advisory Committee. Risk stratification for in-hospital mortality in acutely 
   decompensated heart failure: classification and regression tree analysis. JAMA. 
   2005 Feb 2;293(5):572-80. doi: 10.1001/jama.293.5.572.
2. Abraham WT, Fonarow GC, Albert NM, Stough WG, Gheorghiade M, Greenberg BH, et al. 
   Predictors of in-hospital mortality in patients hospitalized for heart failure: 
   insights from the Organized Program to Initiate Lifesaving Treatment in 
   Hospitalized Patients with Heart Failure (OPTIMIZE-HF). J Am Coll Cardiol. 
   2008 Jul 29;52(5):347-56. doi: 10.1016/j.jacc.2008.04.028.

The ADHERE Algorithm is a simple decision tree-based risk stratification tool 
derived from the Acute Decompensated Heart Failure National Registry, which 
included over 65,000 hospitalizations for heart failure. This algorithm uses 
three readily available clinical parameters (BUN, systolic blood pressure, and 
serum creatinine) to predict in-hospital mortality risk in patients hospitalized 
with acute decompensated heart failure.

The algorithm was developed using classification and regression tree (CART) 
analysis and provides a straightforward approach to risk stratification that 
can guide clinical decision-making regarding level of care, monitoring intensity, 
and therapeutic interventions. Blood urea nitrogen (BUN) was identified as the 
strongest single predictor of in-hospital mortality in the ADHERE registry.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AdhereAlgorithmRequest(BaseModel):
    """
    Request model for Acute Decompensated Heart Failure National Registry (ADHERE) Algorithm
    
    The ADHERE Algorithm uses a simple decision tree with three clinical parameters:
    
    Blood Urea Nitrogen (BUN):
    - under_43: BUN <43 mg/dL (15.35 mmol/L) - Low risk pathway
    - 43_or_over: BUN ≥43 mg/dL (15.35 mmol/L) - Continue to next step
    
    Systolic Blood Pressure (assessed only if BUN ≥43 mg/dL):
    - 115_or_over: SBP ≥115 mmHg - Intermediate risk
    - under_115: SBP <115 mmHg - Continue to next step
    
    Serum Creatinine (assessed only if BUN ≥43 mg/dL and SBP <115 mmHg):
    - under_2_75: Creatinine <2.75 mg/dL (243.1 μmol/L) - Intermediate-high risk
    - 2_75_or_over: Creatinine ≥2.75 mg/dL (243.1 μmol/L) - High risk
    
    Decision Tree Logic:
    1. If BUN <43 mg/dL → Low Risk (2.1-2.3% mortality)
    2. If BUN ≥43 mg/dL and SBP ≥115 mmHg → Intermediate Risk (5.5-6.4% mortality)
    3. If BUN ≥43 mg/dL, SBP <115 mmHg, and creatinine <2.75 mg/dL → Intermediate-High Risk (12.4-12.8% mortality)
    4. If BUN ≥43 mg/dL, SBP <115 mmHg, and creatinine ≥2.75 mg/dL → High Risk (19.8-21.9% mortality)

    References (Vancouver style):
    1. Fonarow GC, Adams KF Jr, Abraham WT, Yancy CW, Boscardin WJ; ADHERE Scientific 
    Advisory Committee. Risk stratification for in-hospital mortality in acutely 
    decompensated heart failure: classification and regression tree analysis. JAMA. 
    2005 Feb 2;293(5):572-80. doi: 10.1001/jama.293.5.572.
    2. Abraham WT, Fonarow GC, Albert NM, Stough WG, Gheorghiade M, Greenberg BH, et al. 
    Predictors of in-hospital mortality in patients hospitalized for heart failure: 
    insights from the Organized Program to Initiate Lifesaving Treatment in 
    Hospitalized Patients with Heart Failure (OPTIMIZE-HF). J Am Coll Cardiol. 
    2008 Jul 29;52(5):347-56. doi: 10.1016/j.jacc.2008.04.028.
    """
    
    bun: Literal["under_43", "43_or_over"] = Field(
        ...,
        description="Blood urea nitrogen level at admission. Under 43 mg/dL indicates low risk, 43 mg/dL or over requires further evaluation with systolic blood pressure",
        example="under_43"
    )
    
    systolic_bp: Literal["115_or_over", "under_115"] = Field(
        ...,
        description="Systolic blood pressure at admission in mmHg. Only assessed when BUN ≥43 mg/dL. 115 mmHg or over indicates intermediate risk, under 115 mmHg requires further evaluation with creatinine",
        example="115_or_over"
    )
    
    creatinine: Literal["under_2_75", "2_75_or_over"] = Field(
        ...,
        description="Serum creatinine level at admission in mg/dL. Only assessed when BUN ≥43 mg/dL and SBP <115 mmHg. Under 2.75 mg/dL indicates intermediate-high risk, 2.75 mg/dL or over indicates high risk",
        example="under_2_75"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "bun": "under_43",
                "systolic_bp": "115_or_over",
                "creatinine": "under_2_75"
            }
        }


class AdhereAlgorithmResponse(BaseModel):
    """
    Response model for Acute Decompensated Heart Failure National Registry (ADHERE) Algorithm
    
    The ADHERE Algorithm stratifies patients into four risk categories:
    - Low Risk (0): BUN <43 mg/dL - 2.1-2.3% in-hospital mortality
    - Intermediate Risk (1): BUN ≥43 mg/dL and SBP ≥115 mmHg - 5.5-6.4% mortality
    - Intermediate-High Risk (2): BUN ≥43 mg/dL, SBP <115 mmHg, creatinine <2.75 mg/dL - 12.4-12.8% mortality
    - High Risk (3): BUN ≥43 mg/dL, SBP <115 mmHg, creatinine ≥2.75 mg/dL - 19.8-21.9% mortality
    
    This decision tree algorithm guides clinical decision-making regarding level of care,
    monitoring intensity, and therapeutic interventions for patients hospitalized with
    acute decompensated heart failure.
    
    Reference: Fonarow GC, et al. JAMA. 2005;293(5):572-80.
    """
    
    result: int = Field(
        ...,
        description="ADHERE Algorithm risk level (0=Low, 1=Intermediate, 2=Intermediate-High, 3=High)",
        example=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk level",
        example="risk_level"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on the risk category",
        example="Low risk of in-hospital mortality (2.1-2.3%). Standard heart failure management on general medical ward is appropriate. Monitor response to therapy and optimize guideline-directed medical therapy."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Intermediate Risk, Intermediate-High Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the clinical criteria for this risk category",
        example="BUN <43 mg/dL"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 0,
                "unit": "risk_level",
                "interpretation": "Low risk of in-hospital mortality (2.1-2.3%). Standard heart failure management on general medical ward is appropriate. Monitor response to therapy and optimize guideline-directed medical therapy.",
                "stage": "Low Risk",
                "stage_description": "BUN <43 mg/dL"
            }
        }