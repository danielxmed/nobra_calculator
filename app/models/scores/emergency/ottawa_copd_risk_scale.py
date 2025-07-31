"""
Ottawa COPD Risk Scale Models

Request and response models for Ottawa COPD Risk Scale calculation.

References (Vancouver style):
1. Stiell IG, Clement CM, Aaron SD, Rowe BH, Perry JJ, Brison RJ, et al. Clinical 
   characteristics associated with adverse events in patients with exacerbation of chronic 
   obstructive pulmonary disease: a prospective cohort study. CMAJ. 2014 Oct 7;186(15):E563-73. 
   doi: 10.1503/cmaj.140677. PMID: 25225226; PMCID: PMC4186913.
2. Stiell IG, Perry JJ, Clement CM, Brison RJ, Rowe BH, Aaron SD, et al. Clinical validation 
   of a risk scale for serious outcomes among patients with chronic obstructive pulmonary 
   disease managed in the emergency department. CMAJ. 2018 Oct 15;190(41):E1202-E1211. 
   doi: 10.1503/cmaj.180232. PMID: 30322856; PMCID: PMC6194243.

The Ottawa COPD Risk Scale is a validated 10-point clinical tool that predicts serious 
adverse events in emergency department patients with COPD exacerbation. It stratifies 
risk from low (2.2%) to very high (75.6%) and can help guide disposition decisions.
"""

from pydantic import BaseModel, Field
from typing import Literal


class OttawaCopdRiskScaleRequest(BaseModel):
    """
    Request model for Ottawa COPD Risk Scale
    
    The Ottawa COPD Risk Scale uses 10 clinical variables to predict serious adverse 
    events within 30 days:
    
    History (4 points total):
    - Coronary bypass graft: 1 point
    - Peripheral vascular intervention: 1 point
    - Intubation for respiratory distress: 2 points
    
    Examination (4 points total):
    - Heart rate ≥110/min on ED arrival: 2 points
    - Too ill to do walk test after ED treatment: 2 points
    
    Investigations (8 points total):
    - Acute ischemic changes on ECG: 2 points
    - Pulmonary congestion on chest x-ray: 1 point
    - Hemoglobin <10 g/dL: 3 points
    - Urea ≥12 mmol/L: 1 point
    - Serum CO2 ≥35 mEq/L: 1 point
    
    Total possible score: 16 points

    References (Vancouver style):
    1. Stiell IG, Clement CM, Aaron SD, Rowe BH, Perry JJ, Brison RJ, et al. Clinical 
    characteristics associated with adverse events in patients with exacerbation of chronic 
    obstructive pulmonary disease: a prospective cohort study. CMAJ. 2014 Oct 7;186(15):E563-73.
    2. Stiell IG, Perry JJ, Clement CM, Brison RJ, Rowe BH, Aaron SD, et al. Clinical validation 
    of a risk scale for serious outcomes among patients with chronic obstructive pulmonary 
    disease managed in the emergency department. CMAJ. 2018 Oct 15;190(41):E1202-E1211.
    """
    
    coronary_bypass_graft: Literal["yes", "no"] = Field(
        ...,
        description="History of coronary bypass graft (CABG). Scores 1 point if yes. This is a major cardiac surgical procedure",
        example="no"
    )
    
    peripheral_vascular_intervention: Literal["yes", "no"] = Field(
        ...,
        description="History of intervention for peripheral vascular disease (angioplasty, stenting, bypass surgery). Scores 1 point if yes",
        example="no"
    )
    
    intubation_respiratory_distress: Literal["yes", "no"] = Field(
        ...,
        description="History of intubation for respiratory distress. Scores 2 points if yes. This indicates previous severe respiratory failure",
        example="no"
    )
    
    heart_rate_110_or_higher: Literal["yes", "no"] = Field(
        ...,
        description="Heart rate ≥110 beats per minute on emergency department arrival. Scores 2 points if yes",
        example="yes"
    )
    
    too_ill_for_walk_test: Literal["yes", "no"] = Field(
        ...,
        description="Too ill to do walk test after emergency department treatment. Scores 2 points if yes. Indicates severe functional impairment",
        example="no"
    )
    
    acute_ischemic_changes_ecg: Literal["yes", "no"] = Field(
        ...,
        description="Acute ischemic changes on ECG (clinician interpretation). Scores 2 points if yes. Includes ST depression, T-wave inversion, or Q waves",
        example="no"
    )
    
    pulmonary_congestion_xray: Literal["yes", "no"] = Field(
        ...,
        description="Pulmonary congestion on chest x-ray (clinician interpretation). Scores 1 point if yes. Includes pulmonary edema or vascular congestion",
        example="no"
    )
    
    hemoglobin_less_than_10: Literal["yes", "no"] = Field(
        ...,
        description="Hemoglobin <10 g/dL (<100 g/L). Scores 3 points if yes. This indicates significant anemia",
        example="no"
    )
    
    urea_12_or_higher: Literal["yes", "no"] = Field(
        ...,
        description="Urea ≥12 mmol/L (≥33.6 mg/dL). Scores 1 point if yes. Indicates kidney dysfunction or dehydration",
        example="no"
    )
    
    serum_co2_35_or_higher: Literal["yes", "no"] = Field(
        ...,
        description="Serum CO2 ≥35 mEq/L (≥35 mmol/L). Scores 1 point if yes. Indicates respiratory acidosis or compensation",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "coronary_bypass_graft": "no",
                "peripheral_vascular_intervention": "no",
                "intubation_respiratory_distress": "no",
                "heart_rate_110_or_higher": "yes",
                "too_ill_for_walk_test": "no",
                "acute_ischemic_changes_ecg": "no",
                "pulmonary_congestion_xray": "no",
                "hemoglobin_less_than_10": "no",
                "urea_12_or_higher": "no",
                "serum_co2_35_or_higher": "no"
            }
        }


class OttawaCopdRiskScaleResponse(BaseModel):
    """
    Response model for Ottawa COPD Risk Scale
    
    The Ottawa COPD Risk Scale predicts serious adverse events within 30 days:
    - Low risk (0 points): 2.2% risk
    - Medium risk (1-2 points): 4.0-7.2% risk
    - High risk (3-4 points): 12.5-20.9% risk
    - Very high risk (5-8 points): 32.9-75.6% risk
    
    Reference: Stiell IG, et al. CMAJ. 2014;186(15):E563-73.
    """
    
    result: int = Field(
        ...,
        description="Ottawa COPD Risk Scale score calculated from clinical variables (range: 0-16 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on the score",
        example="This patient has a medium risk (4.0-7.2%) of serious adverse events within 30 days. Consider closer monitoring and follow-up arrangements. Serious adverse events include death, admission to monitored unit, intubation, noninvasive ventilation, myocardial infarction, or relapse requiring hospital admission within 14 days."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low risk, Medium risk, High risk, Very high risk, or Extremely high risk)",
        example="Medium risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="4.0-7.2% risk of serious adverse events"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "This patient has a medium risk (4.0-7.2%) of serious adverse events within 30 days. Consider closer monitoring and follow-up arrangements. Serious adverse events include death, admission to monitored unit, intubation, noninvasive ventilation, myocardial infarction, or relapse requiring hospital admission within 14 days.",
                "stage": "Medium risk",
                "stage_description": "4.0-7.2% risk of serious adverse events"
            }
        }