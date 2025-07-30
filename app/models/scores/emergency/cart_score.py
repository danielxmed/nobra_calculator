"""
CART (Cardiac Arrest Risk Triage) Score Models

Request and response models for CART Score calculation.

References (Vancouver style):
1. Churpek MM, Yuen TC, Park SY, Meltzer DO, Hall JB, Edelson DP. Derivation of a cardiac arrest prediction model using ward vital signs. Crit Care Med. 2012 Jul;40(7):2102-8. doi: 10.1097/CCM.0b013e318250aa5a.
2. Churpek MM, Yuen TC, Winslow C, Hall J, Edelson DP. Multicenter development and validation of a risk stratification tool for ward patients. Am J Respir Crit Care Med. 2014 Sep 15;190(6):649-55. doi: 10.1164/rccm.201406-1022OC.
3. Churpek MM, Yuen TC, Winslow C, Meltzer DO, Kattan MW, Edelson DP. Multicenter comparison of machine learning methods and conventional regression for predicting clinical deterioration on the wards. Crit Care Med. 2016 Feb;44(2):368-74. doi: 10.1097/CCM.0000000000001571.

The CART (Cardiac Arrest Risk Triage) Score predicts the risk of in-hospital cardiac arrest within 48 hours using vital signs and age. It was developed to identify hospitalized patients at high risk for cardiac arrest who may benefit from intensive monitoring or early intervention.

The score uses four parameters:
1. Respiratory Rate: <21 (0 pts), 21-23 (8 pts), 24-25 (12 pts), 26-29 (15 pts), >29 (22 pts)
2. Heart Rate: <110 (0 pts), 110-139 (4 pts), >139 (13 pts)
3. Diastolic Blood Pressure: >49 (0 pts), 40-49 (4 pts), 35-39 (6 pts), <35 (13 pts)
4. Age: <55 (0 pts), 55-69 (4 pts), >69 (9 pts)

Clinical interpretation:
- Score ≤20: Low risk of cardiac arrest within 48 hours
- Score >20: High risk of cardiac arrest within 48 hours (consider intensive monitoring, rapid response team activation, or transfer to higher level of care)

The CART score has been validated across multiple hospital settings and shows 91.9% specificity for predicting cardiac arrest within 48 hours. It outperformed the Modified Early Warning Score (MEWS) in predicting cardiac arrest events.
"""

from pydantic import BaseModel, Field


class CartScoreRequest(BaseModel):
    """
    Request model for CART (Cardiac Arrest Risk Triage) Score calculation
    
    The CART Score predicts the risk of in-hospital cardiac arrest within 48 hours using:
    
    Parameters and Scoring:
    - Respiratory Rate (breaths/min): <21 (0), 21-23 (8), 24-25 (12), 26-29 (15), >29 (22)
    - Heart Rate (beats/min): <110 (0), 110-139 (4), >139 (13)
    - Diastolic Blood Pressure (mmHg): >49 (0), 40-49 (4), 35-39 (6), <35 (13)
    - Age (years): <55 (0), 55-69 (4), >69 (9)
    
    Risk Interpretation:
    - Score ≤20: Low risk of cardiac arrest
    - Score >20: High risk of cardiac arrest (intensive monitoring recommended)
    
    Clinical Applications:
    - Identify patients needing rapid response team activation
    - Guide decisions for intensive monitoring or ICU transfer
    - Trigger early interventions to prevent cardiac arrest
    - Risk stratification of hospitalized patients
    
    References (Vancouver style):
    1. Churpek MM, Yuen TC, Park SY, Meltzer DO, Hall JB, Edelson DP. Derivation of a cardiac arrest prediction model using ward vital signs. Crit Care Med. 2012 Jul;40(7):2102-8. doi: 10.1097/CCM.0b013e318250aa5a.
    2. Churpek MM, Yuen TC, Winslow C, Hall J, Edelson DP. Multicenter development and validation of a risk stratification tool for ward patients. Am J Respir Crit Care Med. 2014 Sep 15;190(6):649-55. doi: 10.1164/rccm.201406-1022OC.
    3. Churpek MM, Yuen TC, Winslow C, Meltzer DO, Kattan MW, Edelson DP. Multicenter comparison of machine learning methods and conventional regression for predicting clinical deterioration on the wards. Crit Care Med. 2016 Feb;44(2):368-74. doi: 10.1097/CCM.0000000000001571.
    """
    
    respiratory_rate: int = Field(
        ...,
        description="Respiratory rate in breaths per minute. Normal range is typically 12-20 breaths/min",
        ge=5,
        le=60,
        example=22
    )
    
    heart_rate: int = Field(
        ...,
        description="Heart rate in beats per minute. Normal range is typically 60-100 beats/min",
        ge=30,
        le=250,
        example=115
    )
    
    diastolic_bp: int = Field(
        ...,
        description="Diastolic blood pressure in mmHg. Normal range is typically 60-90 mmHg",
        ge=20,
        le=150,
        example=45
    )
    
    age: int = Field(
        ...,
        description="Patient age in years",
        ge=18,
        le=120,
        example=68
    )
    
    class Config:
        schema_extra = {
            "example": {
                "respiratory_rate": 22,
                "heart_rate": 115,
                "diastolic_bp": 45,
                "age": 68
            }
        }


class CartScoreResponse(BaseModel):
    """
    Response model for CART (Cardiac Arrest Risk Triage) Score calculation
    
    Returns the CART score and clinical interpretation for cardiac arrest risk assessment.
    
    Score Interpretation:
    - Score ≤20: Low risk of cardiac arrest within 48 hours
    - Score >20: High risk of cardiac arrest within 48 hours
    
    The response includes component scores showing how each vital sign and age 
    contributed to the total score, helping clinicians understand which parameters 
    are driving the risk assessment.
    
    Clinical Actions Based on Score:
    - Low Risk (≤20): Standard monitoring and care
    - High Risk (>20): Consider intensive monitoring, rapid response team activation, 
      or transfer to higher level of care
    
    Reference: Churpek MM, et al. Crit Care Med. 2012;40(7):2102-8.
    """
    
    result: int = Field(
        ...,
        description="CART Score (range 0-59 points) predicting 48-hour cardiac arrest risk",
        example=19
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on CART score",
        example="CART Score 19 indicates low risk of cardiac arrest within 48 hours. Standard monitoring and care appropriate. Continue routine assessments and interventions. The patient's vital signs suggest stable cardiac status."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk or High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Low risk of cardiac arrest"
    )
    
    component_scores: dict = Field(
        ...,
        description="Individual component scores showing contribution from each parameter",
        example={
            "respiratory_rate_score": 8,
            "heart_rate_score": 4,
            "diastolic_bp_score": 4,
            "age_score": 4
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 20,
                "unit": "points",
                "interpretation": "CART Score 20 indicates low risk of cardiac arrest within 48 hours. Standard monitoring and care appropriate. Continue routine assessments and interventions. The patient's vital signs suggest stable cardiac status.",
                "stage": "Low Risk",
                "stage_description": "Low risk of cardiac arrest",
                "component_scores": {
                    "respiratory_rate_score": 8,
                    "heart_rate_score": 4,
                    "diastolic_bp_score": 4,
                    "age_score": 4
                }
            }
        }