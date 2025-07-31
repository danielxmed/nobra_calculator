"""
Thakar Score Models

Request and response models for Thakar Score calculation.

References (Vancouver style):
1. Thakar CV, Arrigain S, Worley S, Yared JP, Paganini EP. A clinical score to predict 
   acute renal failure after cardiac surgery. J Am Soc Nephrol. 2005 Jan;16(1):162-8. 
   doi: 10.1681/ASN.2004040331.
2. Chertow GM, Levy EM, Hammermeister KE, Grover F, Daley J. Independent association 
   between acute renal failure and mortality following cardiac surgery. Am J Med. 1998 
   Apr;104(4):343-8. doi: 10.1016/s0002-9343(98)00058-8.
3. Bove T, Monaco F, Covello RD, Zangrillo A. Acute renal failure and cardiac surgery. 
   HSR Proc Intensive Care Cardiovasc Anesth. 2009;1(3):13-21.

The Thakar Score is a clinical decision tool that predicts the risk of acute kidney 
injury (AKI) requiring dialysis after cardiac surgery. It was developed and validated 
in over 33,000 patients at the Cleveland Clinic Foundation. The score ranges from 0-17 
points and stratifies patients into risk categories from very low (0.3-0.5% risk) to 
very high (>22% risk) for developing AKI requiring dialysis.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ThakarScoreRequest(BaseModel):
    """
    Request model for Thakar Score (Acute Renal Failure after Cardiac Surgery)
    
    The Thakar Score uses 10 clinical variables to assess AKI risk after cardiac surgery:
    
    Patient Demographics:
    - Gender: Female patients receive +1 point
    
    Cardiac Factors:
    - Congestive heart failure: +1 point if present
    - Left ventricular ejection fraction <35%: +1 point if present
    - Preoperative IABP use: +2 points if present
    
    Comorbidities:
    - COPD: +1 point if present
    - Insulin-requiring diabetes: +1 point if present
    - Previous cardiac surgery: +1 point if present
    
    Surgical Factors:
    - Emergency surgery: +2 points if present
    - Surgery type: Valve only (+1), CABG+valve or other (+2)
    
    Laboratory:
    - Preoperative creatinine: 1.2-2.0 mg/dL (+2), >2.0 mg/dL (+5)

    References (Vancouver style):
    1. Thakar CV, Arrigain S, Worley S, Yared JP, Paganini EP. A clinical score to predict 
    acute renal failure after cardiac surgery. J Am Soc Nephrol. 2005 Jan;16(1):162-8. 
    doi: 10.1681/ASN.2004040331.
    2. Chertow GM, Levy EM, Hammermeister KE, Grover F, Daley J. Independent association 
    between acute renal failure and mortality following cardiac surgery. Am J Med. 1998 
    Apr;104(4):343-8. doi: 10.1016/s0002-9343(98)00058-8.
    3. Bove T, Monaco F, Covello RD, Zangrillo A. Acute renal failure and cardiac surgery. 
    HSR Proc Intensive Care Cardiovasc Anesth. 2009;1(3):13-21.
    """
    
    gender: Literal["male", "female"] = Field(
        ...,
        description="Patient gender. Female gender scores +1 point",
        example="male"
    )
    
    congestive_heart_failure: Literal["no", "yes"] = Field(
        ...,
        description="Presence of congestive heart failure. Scores +1 point if yes",
        example="no"
    )
    
    left_ventricular_ejection_fraction_under_35: Literal["no", "yes"] = Field(
        ...,
        description="Left ventricular ejection fraction <35%. Scores +1 point if yes",
        example="no"
    )
    
    preoperative_iabp: Literal["no", "yes"] = Field(
        ...,
        description="Preoperative use of intra-aortic balloon pump (IABP). Scores +2 points if yes",
        example="no"
    )
    
    copd: Literal["no", "yes"] = Field(
        ...,
        description="Chronic obstructive pulmonary disease (COPD). Scores +1 point if yes",
        example="no"
    )
    
    insulin_requiring_diabetes: Literal["no", "yes"] = Field(
        ...,
        description="Insulin-requiring diabetes mellitus. Scores +1 point if yes",
        example="no"
    )
    
    previous_cardiac_surgery: Literal["no", "yes"] = Field(
        ...,
        description="Previous cardiac surgery. Scores +1 point if yes",
        example="no"
    )
    
    emergency_surgery: Literal["no", "yes"] = Field(
        ...,
        description="Emergency surgery (not elective). Scores +2 points if yes",
        example="no"
    )
    
    surgery_type: Literal["none", "valve_only", "cabg_and_valve", "other"] = Field(
        ...,
        description="Type of cardiac surgery performed. None (0 points), valve only (+1 point), CABG and valve (+2 points), other (+2 points)",
        example="none"
    )
    
    preoperative_creatinine: float = Field(
        ...,
        description="Preoperative serum creatinine level in mg/dL. <1.2 (0 points), 1.2-2.0 (+2 points), >2.0 (+5 points)",
        example=1.0,
        ge=0.1,
        le=20.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "gender": "male",
                "congestive_heart_failure": "no",
                "left_ventricular_ejection_fraction_under_35": "no",
                "preoperative_iabp": "no",
                "copd": "no",
                "insulin_requiring_diabetes": "no",
                "previous_cardiac_surgery": "no",
                "emergency_surgery": "no",
                "surgery_type": "none",
                "preoperative_creatinine": 1.0
            }
        }


class ThakarScoreResponse(BaseModel):
    """
    Response model for Thakar Score (Acute Renal Failure after Cardiac Surgery)
    
    The Thakar Score ranges from 0-17 points and classifies patients into risk categories:
    - Very Low Risk (0-2 points): 0.3-0.5% risk of AKI requiring dialysis
    - Low Risk (3-5 points): 1.8-3.3% risk of AKI requiring dialysis
    - Moderate Risk (6-8 points): 7.8-11.4% risk of AKI requiring dialysis
    - High Risk (9-13 points): 18.6-22.1% risk of AKI requiring dialysis
    - Very High Risk (>13 points): >22% risk of AKI requiring dialysis
    
    Reference: Thakar CV, et al. J Am Soc Nephrol. 2005;16(1):162-8.
    """
    
    result: int = Field(
        ...,
        description="Thakar score calculated from clinical variables (range: 0-17 points)",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and risk assessment based on the score",
        example="Score 3-5 points: Low risk (1.8-3.3% risk of AKI requiring dialysis). Standard perioperative renal monitoring is appropriate."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Very Low Risk, Low Risk, Moderate Risk, High Risk, Very High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Low risk for AKI requiring dialysis"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "Score 3-5 points: Low risk (1.8-3.3% risk of AKI requiring dialysis). Standard perioperative renal monitoring is appropriate.",
                "stage": "Low Risk",
                "stage_description": "Low risk for AKI requiring dialysis"
            }
        }