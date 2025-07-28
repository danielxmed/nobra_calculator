"""
ADAPT Protocol Models

Request and response models for ADAPT Protocol calculation.

References (Vancouver style):
1. Than M, Flaws D, Sanders S, Doust J, Glasziou P, Kline J, Aldous S, Troughton R, 
   Reid C, Parsonage WA, Frampton C, Greenslade JH, Deely JM, Hess E, Sadiq AB, 
   Singleton R, Shopland R, Vercoe L, Woolhouse-Williams M, Ardagh M, Bossuyt P, 
   Bannister L, Cullen L. Development and validation of the Emergency Department 
   Assessment of Chest pain Score and 2 h accelerated diagnostic protocol. Emerg Med 
   Australas. 2014 Feb;26(1):34-44. doi: 10.1111/1742-6723.12164.
2. Cullen L, Mueller C, Parsonage WA, Wildi K, Greenslade JH, Twerenbold R, Aldous S, 
   Meller B, Tate JR, Reichlin T, Hammett CJ, Zellweger C, Ungerer JP, Rubini Gimenez M, 
   Troughton R, Murray K, Brown AF, Mueller M, George P, Mosimann T, Flaws DF, Reiter M, 
   Lamanna A, Haaf P, Pemberton CJ, Richards AM, Chu K, Reid CM, Peacock WF, Jaffe AS, 
   Florkowski C, Deely JM, Than M. Validation of high-sensitivity troponin I in a 2-hour 
   diagnostic strategy to assess 30-day outcomes in emergency department patients with 
   possible acute coronary syndrome. J Am Coll Cardiol. 2013 Oct 1;62(14):1242-9. 
   doi: 10.1016/j.jacc.2013.02.078.

The ADAPT Protocol (Accelerated Diagnostic Protocol to Assess Patients with Chest Pain 
Symptoms Using Contemporary Troponins as the Only Biomarker) is a clinical decision tool 
that assesses chest pain patients at 2 hours for risk of cardiac event. It uses a binary 
decision tree approach to stratify patients into low risk (0-0.3% risk of major cardiac 
event in 30 days) or high risk categories based on troponin levels, ECG changes, and 
TIMI risk factors.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AdaptProtocolRequest(BaseModel):
    """
    Request model for ADAPT Protocol for Cardiac Event Risk
    
    The ADAPT Protocol uses 7 clinical variables to assess cardiac event risk at 2 hours:
    
    Biomarker and ECG:
    - Abnormal troponin at 0 or 2 hours: High risk if positive
    - Ischemic changes on ECG: High risk if present
    
    TIMI Risk Factors (any positive = high risk):
    - Age ≥65 years
    - ≥3 CAD risk factors (hypertension, hypercholesterolemia, diabetes, 
      family history of coronary artery disease, or current smoker)
    - Known CAD (stenosis ≥50%)
    - Aspirin use in past 7 days
    - Severe angina (≥2 episodes in 24 hours or persisting discomfort)
    
    Low Risk: None of the above criteria present (0-0.3% risk of MACE in 30 days)
    High Risk: Any of the above criteria present (elevated risk of MACE in 30 days)

    References (Vancouver style):
    1. Than M, Flaws D, Sanders S, Doust J, Glasziou P, Kline J, Aldous S, Troughton R, 
    Reid C, Parsonage WA, Frampton C, Greenslade JH, Deely JM, Hess E, Sadiq AB, 
    Singleton R, Shopland R, Vercoe L, Woolhouse-Williams M, Ardagh M, Bossuyt P, 
    Bannister L, Cullen L. Development and validation of the Emergency Department 
    Assessment of Chest pain Score and 2 h accelerated diagnostic protocol. Emerg Med 
    Australas. 2014 Feb;26(1):34-44. doi: 10.1111/1742-6723.12164.
    2. Cullen L, Mueller C, Parsonage WA, Wildi K, Greenslade JH, Twerenbold R, Aldous S, 
    Meller B, Tate JR, Reichlin T, Hammett CJ, Zellweger C, Ungerer JP, Rubini Gimenez M, 
    Troughton R, Murray K, Brown AF, Mueller M, George P, Mosimann T, Flaws DF, Reiter M, 
    Lamanna A, Haaf P, Pemberton CJ, Richards AM, Chu K, Reid CM, Peacock WF, Jaffe AS, 
    Florkowski C, Deely JM, Than M. Validation of high-sensitivity troponin I in a 2-hour 
    diagnostic strategy to assess 30-day outcomes in emergency department patients with 
    possible acute coronary syndrome. J Am Coll Cardiol. 2013 Oct 1;62(14):1242-9. 
    doi: 10.1016/j.jacc.2013.02.078.
    """
    
    abnormal_troponin: Literal["no", "yes"] = Field(
        ...,
        description="Abnormal troponin at 0 or 2 hours. High risk if yes",
        example="no"
    )
    
    ischemic_changes_ecg: Literal["no", "yes"] = Field(
        ...,
        description="Ischemic changes on ECG (ST depression, T-wave inversion, etc.). High risk if yes",
        example="no"
    )
    
    age_65_or_older: Literal["no", "yes"] = Field(
        ...,
        description="Patient age ≥65 years. TIMI risk factor - high risk if yes",
        example="no"
    )
    
    three_or_more_cad_risk_factors: Literal["no", "yes"] = Field(
        ...,
        description="≥3 CAD risk factors (hypertension, hypercholesterolemia, diabetes, family history of CAD, or current smoker). TIMI risk factor - high risk if yes",
        example="no"
    )
    
    known_cad: Literal["no", "yes"] = Field(
        ...,
        description="Known coronary artery disease (stenosis ≥50%). TIMI risk factor - high risk if yes",
        example="no"
    )
    
    aspirin_use_past_7_days: Literal["no", "yes"] = Field(
        ...,
        description="Aspirin use in past 7 days. TIMI risk factor - high risk if yes",
        example="no"
    )
    
    severe_angina: Literal["no", "yes"] = Field(
        ...,
        description="Severe angina (≥2 episodes in 24 hours or persisting discomfort). TIMI risk factor - high risk if yes",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "abnormal_troponin": "no",
                "ischemic_changes_ecg": "no",
                "age_65_or_older": "no",
                "three_or_more_cad_risk_factors": "no",
                "known_cad": "no",
                "aspirin_use_past_7_days": "no",
                "severe_angina": "no"
            }
        }


class AdaptProtocolResponse(BaseModel):
    """
    Response model for ADAPT Protocol for Cardiac Event Risk
    
    The ADAPT Protocol stratifies patients into two risk categories:
    - Low Risk: 0-0.3% risk of major cardiac event in 30 days
    - High Risk: Elevated risk of major cardiac event in 30 days
    
    Low risk patients can be safely discharged with outpatient follow-up.
    High risk patients require further cardiac evaluation and monitoring.
    
    Reference: Than M, et al. Emerg Med Australas. 2014;26(1):34-44.
    """
    
    result: str = Field(
        ...,
        description="ADAPT Protocol risk stratification result (Low Risk or High Risk)",
        example="Low Risk"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on the risk level",
        example="0-0.3% risk of major cardiac event in 30 days. Patient can be safely discharged from the emergency department with appropriate outpatient follow-up."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk or High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Low risk for major cardiac event"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Low Risk",
                "unit": "",
                "interpretation": "0-0.3% risk of major cardiac event in 30 days. Patient can be safely discharged from the emergency department with appropriate outpatient follow-up.",
                "stage": "Low Risk",
                "stage_description": "Low risk for major cardiac event"
            }
        }