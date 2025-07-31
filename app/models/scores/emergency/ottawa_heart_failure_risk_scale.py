"""
Ottawa Heart Failure Risk Scale (OHFRS) Models

Request and response models for Ottawa Heart Failure Risk Scale calculation.

References (Vancouver style):
1. Stiell IG, Clement CM, Brison RJ, Rowe BH, Borgundvaag B, Aaron SD, et al. A risk 
   scoring system to identify emergency department patients with heart failure at high 
   risk for serious adverse events. Acad Emerg Med. 2013 Jan;20(1):17-26. doi: 
   10.1111/acem.12056. PMID: 23574475.
2. Stiell IG, Perry JJ, Clement CM, Brison RJ, Rowe BH, Aaron SD, et al. Prospective 
   and Explicit Clinical Validation of the Ottawa Heart Failure Risk Scale, With and 
   Without Use of Quantitative NT-proBNP. Acad Emerg Med. 2017 Mar;24(3):316-327. doi: 
   10.1111/acem.13141. PMID: 27976497.

The Ottawa Heart Failure Risk Scale (OHFRS) is a validated 10-point clinical tool 
that identifies emergency department patients with heart failure at high risk for 
serious adverse events within 14 days, with high sensitivity (91.8-95.8%).
"""

from pydantic import BaseModel, Field
from typing import Literal


class OttawaHeartFailureRiskScaleRequest(BaseModel):
    """
    Request model for Ottawa Heart Failure Risk Scale (OHFRS)
    
    The OHFRS uses 10 clinical variables to predict serious adverse events within 14 days:
    
    History (3 points total):
    - Stroke or TIA: 1 point
    - Intubation for respiratory distress: 2 points
    
    Examination (4 points total):
    - Heart rate ≥110/min on ED arrival: 2 points
    - SaO₂ <90% on arrival: 1 point
    - Heart rate ≥110/min during 3-minute walk test: 1 point
    
    Investigations (6 points total):
    - New ischemic changes on ECG: 2 points
    - Urea ≥12 mmol/L: 1 point
    - Serum CO₂ ≥35 mmol/L: 2 points
    - Troponin I or T elevated to MI level: 2 points
    - NT-proBNP ≥5,000 ng/L: 1 point
    
    Total possible score: 13 points

    References (Vancouver style):
    1. Stiell IG, Clement CM, Brison RJ, Rowe BH, Borgundvaag B, Aaron SD, et al. A risk 
    scoring system to identify emergency department patients with heart failure at high 
    risk for serious adverse events. Acad Emerg Med. 2013 Jan;20(1):17-26.
    2. Stiell IG, Perry JJ, Clement CM, Brison RJ, Rowe BH, Aaron SD, et al. Prospective 
    and Explicit Clinical Validation of the Ottawa Heart Failure Risk Scale, With and 
    Without Use of Quantitative NT-proBNP. Acad Emerg Med. 2017 Mar;24(3):316-327.
    """
    
    stroke_or_tia: Literal["yes", "no"] = Field(
        ...,
        description="History of stroke or transient ischemic attack (TIA). Scores 1 point if yes. Previous cerebrovascular event",
        example="no"
    )
    
    intubation_respiratory_distress: Literal["yes", "no"] = Field(
        ...,
        description="History of intubation for respiratory distress. Scores 2 points if yes. Previous severe respiratory failure requiring mechanical ventilation",
        example="no"
    )
    
    heart_rate_110_or_higher_arrival: Literal["yes", "no"] = Field(
        ...,
        description="Heart rate ≥110 beats per minute on emergency department arrival. Scores 2 points if yes. Tachycardia on presentation",
        example="no"
    )
    
    oxygen_saturation_less_than_90: Literal["yes", "no"] = Field(
        ...,
        description="Oxygen saturation (SaO₂) <90% on arrival. Scores 1 point if yes. Significant hypoxemia on presentation",
        example="no"
    )
    
    heart_rate_110_or_higher_walk_test: Literal["yes", "no"] = Field(
        ...,
        description="Heart rate ≥110 beats per minute during 3-minute walk test. Scores 1 point if yes. Exercise-induced tachycardia",
        example="no"
    )
    
    new_ischemic_changes_ecg: Literal["yes", "no"] = Field(
        ...,
        description="New ischemic changes on ECG (clinician interpretation). Scores 2 points if yes. ST depression, T-wave inversion, or new Q waves",
        example="no"
    )
    
    urea_12_or_higher: Literal["yes", "no"] = Field(
        ...,
        description="Urea ≥12 mmol/L (≥33.6 mg/dL). Scores 1 point if yes. Indicates kidney dysfunction or volume depletion",
        example="no"
    )
    
    serum_co2_35_or_higher: Literal["yes", "no"] = Field(
        ...,
        description="Serum CO₂ ≥35 mmol/L (≥35 mEq/L). Scores 2 points if yes. Respiratory acidosis or metabolic compensation",
        example="no"
    )
    
    troponin_elevated_mi_level: Literal["yes", "no"] = Field(
        ...,
        description="Troponin I or T elevated to myocardial infarction level. Scores 2 points if yes. Suggests acute coronary syndrome",
        example="no"
    )
    
    nt_probnp_5000_or_higher: Literal["yes", "no"] = Field(
        ...,
        description="NT-proBNP ≥5,000 ng/L (≥5,000 pg/mL). Scores 1 point if yes. Elevated natriuretic peptide indicating heart failure severity",
        example="yes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "stroke_or_tia": "no",
                "intubation_respiratory_distress": "no",
                "heart_rate_110_or_higher_arrival": "no",
                "oxygen_saturation_less_than_90": "no",
                "heart_rate_110_or_higher_walk_test": "no",
                "new_ischemic_changes_ecg": "no",
                "urea_12_or_higher": "no",
                "serum_co2_35_or_higher": "no",
                "troponin_elevated_mi_level": "no",
                "nt_probnp_5000_or_higher": "yes"
            }
        }


class OttawaHeartFailureRiskScaleResponse(BaseModel):
    """
    Response model for Ottawa Heart Failure Risk Scale (OHFRS)
    
    The OHFRS predicts serious adverse events within 14 days:
    - Low risk (0 points): 2.8% risk
    - Medium risk (1-2 points): 5.1-9.2% risk
    - High risk (3-4 points): 15.9-26.1% risk
    - Very high risk (5+ points): 39.8-89%+ risk
    
    Reference: Stiell IG, et al. Acad Emerg Med. 2013;20(1):17-26.
    """
    
    result: int = Field(
        ...,
        description="Ottawa Heart Failure Risk Scale score calculated from clinical variables (range: 0-13 points)",
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on the score",
        example="This patient has a medium risk (5.1-9.2%) of serious adverse events within 14 days. Consider closer monitoring and follow-up arrangements. The OHFRS has high sensitivity (91.8% without NT-proBNP, 95.8% with NT-proBNP) for detecting patients at risk."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low risk, Medium risk, High risk, or Very high risk)",
        example="Medium risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="5.1-9.2% risk of serious adverse events"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "This patient has a medium risk (5.1-9.2%) of serious adverse events within 14 days. Consider closer monitoring and follow-up arrangements. The OHFRS has high sensitivity (91.8% without NT-proBNP, 95.8% with NT-proBNP) for detecting patients at risk.",
                "stage": "Medium risk",
                "stage_description": "5.1-9.2% risk of serious adverse events"
            }
        }