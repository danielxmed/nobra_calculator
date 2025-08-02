"""
MAGGIC Risk Calculator for Heart Failure Models

Request and response models for MAGGIC risk calculation.

References (Vancouver style):
1. Pocock SJ, Ariti CA, McMurray JJ, Maggioni A, Køber L, Squire IB, et al. 
   Predicting survival in heart failure: a risk score based on 39 372 patients 
   from 30 studies. Eur Heart J. 2013 May;34(19):1404-13. 
   doi: 10.1093/eurheartj/ehs337.
2. Sartipy U, Dahlström U, Edner M, Lund LH. Predicting survival in heart failure: 
   validation of the MAGGIC heart failure risk score in 51,043 patients from the 
   Swedish heart failure registry. Eur J Heart Fail. 2014 Feb;16(2):173-9. 
   doi: 10.1111/ejhf.32.
3. Simpson J, Jhund PS, Silva Cardoso J, Martinez F, Mosterd A, Ramires F, et al. 
   Comparing LCZ696 with enalapril according to baseline risk using the MAGGIC and 
   EMPHASIS-HF risk scores: an analysis of mortality and morbidity in PARADIGM-HF. 
   J Am Coll Cardiol. 2015 Nov 10;66(19):2059-71. doi: 10.1016/j.jacc.2015.08.878.

The MAGGIC (Meta-Analysis Global Group In Chronic Heart Failure) risk calculator 
is a validated prognostic tool that estimates 1- and 3-year mortality in heart 
failure patients. Developed from a meta-analysis of 39,372 patients from 30 studies, 
it uses 13 clinical variables to provide accurate risk stratification applicable 
to both HFrEF and HFpEF patients. The score has been extensively validated with 
C-indices of 0.70-0.75 for mortality prediction across diverse populations.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MaggicRiskCalculatorRequest(BaseModel):
    """
    Request model for MAGGIC Risk Calculator for Heart Failure
    
    The MAGGIC risk score uses 13 clinical variables to estimate mortality risk:
    
    Demographics:
    - Age: Scored differently for HFrEF (EF ≤40%) vs HFpEF (EF >40%)
    - Gender: Male patients receive additional risk points
    
    Cardiac Parameters:
    - Ejection Fraction: Lower EF associated with higher mortality risk
      • ≥40%: 0 points (preserved)
      • 35-39%: 1 point (mildly reduced)
      • 30-34%: 2 points (moderately reduced)
      • 25-29%: 3 points (severely reduced)
      • 20-24%: 5 points (very severely reduced)
      • <20%: 6 points (extremely reduced)
    - NYHA Class: Functional capacity assessment
      • Class I: 0 points (no symptoms)
      • Class II: 2 points (slight limitation)
      • Class III: 6 points (marked limitation)
      • Class IV: 8 points (symptoms at rest)
    
    Laboratory Values:
    - Serum Creatinine: Kidney function assessment
      • ≤1.2 mg/dL: 0 points (normal)
      • 1.21-1.4: 1 point (mild elevation)
      • 1.41-1.8: 2 points (moderate elevation)
      • 1.81-2.3: 3 points (significant elevation)
      • 2.31-2.8: 4 points (severe elevation)
      • >2.8: 5 points (very severe elevation)
    
    Vital Signs:
    - Systolic Blood Pressure: Lower BP associated with worse prognosis
      • ≥140 mmHg: 0 points
      • 120-139: 1 point
      • 110-119: 2 points
      • 100-109: 3 points
      • <100: 5 points
    - BMI: Obesity paradox - higher BMI protective in heart failure
      • ≥30 kg/m²: 0 points (obese - protective)
      • 25-29.9: 1 point (overweight)
      • 22-24.9: 2 points (normal high)
      • 18-21.9: 3 points (normal low)
      • <18: 5 points (underweight - high risk)
    
    Comorbidities:
    - Diabetes: +3 points if present
    - COPD: +2 points if present
    - Current Smoking: +1 point if yes
    
    Disease History:
    - Heart Failure Duration >18 months: +2 points if yes
    
    Medications (lack of evidence-based therapy increases risk):
    - Not on Beta-blocker: +3 points
    - Not on ACE-I/ARB: +1 point

    References (Vancouver style):
    1. Pocock SJ, Ariti CA, McMurray JJ, Maggioni A, Køber L, Squire IB, et al. 
    Predicting survival in heart failure: a risk score based on 39 372 patients 
    from 30 studies. Eur Heart J. 2013 May;34(19):1404-13. doi: 10.1093/eurheartj/ehs337.
    2. Sartipy U, Dahlström U, Edner M, Lund LH. Predicting survival in heart failure: 
    validation of the MAGGIC heart failure risk score in 51,043 patients from the 
    Swedish heart failure registry. Eur J Heart Fail. 2014 Feb;16(2):173-9. 
    doi: 10.1111/ejhf.32.
    3. Simpson J, Jhund PS, Silva Cardoso J, Martinez F, Mosterd A, Ramires F, et al. 
    Comparing LCZ696 with enalapril according to baseline risk using the MAGGIC and 
    EMPHASIS-HF risk scores: an analysis of mortality and morbidity in PARADIGM-HF. 
    J Am Coll Cardiol. 2015 Nov 10;66(19):2059-71. doi: 10.1016/j.jacc.2015.08.878.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in years. Age scoring varies by ejection fraction category - higher age carries more risk in HFpEF than HFrEF",
        example=65
    )
    
    gender: Literal["male", "female"] = Field(
        ...,
        description="Patient gender. Male gender is associated with increased mortality risk (+1 point)",
        example="male"
    )
    
    ejection_fraction: int = Field(
        ...,
        ge=10,
        le=80,
        description="Left ventricular ejection fraction percentage. Lower EF associated with higher risk: ≥40% (0pts), 35-39% (1pt), 30-34% (2pts), 25-29% (3pts), 20-24% (5pts), <20% (6pts)",
        example=35
    )
    
    nyha_class: Literal["I", "II", "III", "IV"] = Field(
        ...,
        description="NYHA functional class. Higher class indicates worse functional capacity: Class I (0pts), II (2pts), III (6pts), IV (8pts)",
        example="III"
    )
    
    creatinine: float = Field(
        ...,
        ge=0.3,
        le=15.0,
        description="Serum creatinine level in mg/dL. Higher levels indicate worse kidney function and increased risk: ≤1.2 (0pts), 1.21-1.4 (1pt), 1.41-1.8 (2pts), 1.81-2.3 (3pts), 2.31-2.8 (4pts), >2.8 (5pts)",
        example=1.5
    )
    
    systolic_bp: int = Field(
        ...,
        ge=60,
        le=250,
        description="Systolic blood pressure in mmHg. Lower BP associated with worse prognosis: ≥140 (0pts), 120-139 (1pt), 110-119 (2pts), 100-109 (3pts), <100 (5pts)",
        example=110
    )
    
    bmi: float = Field(
        ...,
        ge=10.0,
        le=60.0,
        description="Body mass index in kg/m². Obesity paradox in heart failure - higher BMI is protective: ≥30 (0pts), 25-29.9 (1pt), 22-24.9 (2pts), 18-21.9 (3pts), <18 (5pts)",
        example=28.5
    )
    
    diabetes: Literal["yes", "no"] = Field(
        ...,
        description="Presence of diabetes mellitus. Diabetes increases mortality risk (+3 points if yes)",
        example="yes"
    )
    
    copd: Literal["yes", "no"] = Field(
        ...,
        description="Presence of chronic obstructive pulmonary disease. COPD increases mortality risk (+2 points if yes)",
        example="no"
    )
    
    current_smoker: Literal["yes", "no"] = Field(
        ...,
        description="Current smoking status. Active smoking increases mortality risk (+1 point if yes)",
        example="no"
    )
    
    hf_duration_over_18_months: Literal["yes", "no"] = Field(
        ...,
        description="Heart failure diagnosed more than 18 months ago. Longer duration indicates more established disease (+2 points if yes)",
        example="yes"
    )
    
    beta_blocker: Literal["yes", "no"] = Field(
        ...,
        description="Currently prescribed beta-blocker therapy. Lack of evidence-based beta-blocker therapy increases risk (+3 points if no)",
        example="yes"
    )
    
    ace_arb: Literal["yes", "no"] = Field(
        ...,
        description="Currently prescribed ACE inhibitor or ARB therapy. Lack of evidence-based ACE-I/ARB therapy increases risk (+1 point if no)",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "gender": "male",
                "ejection_fraction": 35,
                "nyha_class": "III",
                "creatinine": 1.5,
                "systolic_bp": 110,
                "bmi": 28.5,
                "diabetes": "yes",
                "copd": "no",
                "current_smoker": "no",
                "hf_duration_over_18_months": "yes",
                "beta_blocker": "yes",
                "ace_arb": "yes"
            }
        }


class MaggicRiskCalculatorResponse(BaseModel):
    """
    Response model for MAGGIC Risk Calculator for Heart Failure
    
    The MAGGIC score ranges from 0 to 50+ points with corresponding mortality estimates:
    - Low Risk (0-15 points): 1-year <5%, 3-year <15% mortality
    - Intermediate Risk (16-25 points): 1-year 5-15%, 3-year 15-40% mortality
    - High Risk (26-35 points): 1-year 15-40%, 3-year 40-70% mortality
    - Very High Risk (>35 points): 1-year >40%, 3-year >70% mortality
    
    The score helps guide:
    - Prognosis discussions with patients and families
    - Intensity of medical therapy and monitoring
    - Referral to advanced heart failure specialists
    - Consideration of device therapy (ICD/CRT)
    - Advanced therapy evaluation (transplant, mechanical support)
    - End-of-life care discussions when appropriate
    
    Reference: Pocock SJ, et al. Eur Heart J. 2013;34(19):1404-13.
    """
    
    result: int = Field(
        ...,
        description="MAGGIC risk score calculated from 13 clinical variables (range: 0-50+ points)",
        example=17
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with mortality estimates and management recommendations based on the risk category",
        example="Intermediate risk for 1-year (5-15%) and 3-year (15-40%) mortality. Consider optimized medical therapy and closer monitoring. Ensure maximal tolerated evidence-based therapy. Consider device therapy evaluation if indicated. Regular cardiology follow-up recommended."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Intermediate Risk, High Risk, Very High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Intermediate mortality risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 17,
                "unit": "points",
                "interpretation": "Intermediate risk for 1-year (5-15%) and 3-year (15-40%) mortality. Consider optimized medical therapy and closer monitoring. Ensure maximal tolerated evidence-based therapy. Consider device therapy evaluation if indicated. Regular cardiology follow-up recommended.",
                "stage": "Intermediate Risk",
                "stage_description": "Intermediate mortality risk"
            }
        }