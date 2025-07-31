"""
HAT (Hemorrhage After Thrombolysis) Score for Predicting Post-tPA Hemorrhage Models

Request and response models for HAT Score calculation.

References (Vancouver style):
1. Lou M, Safdar A, Mehdiratta M, Kumar S, Schlaug G, Caplan L, et al. The HAT Score: 
   a simple grading scale for predicting hemorrhage after thrombolysis. Neurology. 
   2008 Oct 28;71(18):1417-23. doi: 10.1212/01.wnl.0000330297.58334.dd.
2. Tsivgoulis G, Frey JL, Flaster M, Sharma VK, Lao AY, Hoover SL, et al. Pre-tissue 
   plasminogen activator blood pressure levels and risk of symptomatic intracerebral 
   hemorrhage. Stroke. 2009 Nov;40(11):3631-4. doi: 10.1161/STROKEAHA.109.564096.
3. Cucchiara B, Kasner SE, Tanne D, Levine SR, Demchuk A, Messe SR, et al. Validation 
   assessment of risk scores to predict postthrombolysis intracerebral haemorrhage. 
   Int J Stroke. 2011 Apr;6(2):109-11. doi: 10.1111/j.1747-4949.2010.00555.x.
4. Mazya M, Egido JA, Ford GA, Lees KR, Mikulik R, Toni D, et al. Predicting the risk 
   of symptomatic intracerebral hemorrhage in ischemic stroke treated with intravenous 
   alteplase: safe Implementation of Treatments in Stroke (SITS) symptomatic intracerebral 
   hemorrhage risk score. Stroke. 2012 Jun;43(6):1524-31. doi: 10.1161/STROKEAHA.111.644815.

The HAT (Hemorrhage After Thrombolysis) Score is a clinical prediction tool that estimates 
the risk of intracerebral hemorrhage following intravenous tissue plasminogen activator 
(tPA/alteplase) administration in acute ischemic stroke patients. The score uses three 
readily available clinical parameters to stratify patients into risk categories, helping 
clinicians make informed decisions about thrombolytic therapy.
"""

from pydantic import BaseModel, Field
from typing import Literal


class HatScoreRequest(BaseModel):
    """
    Request model for HAT (Hemorrhage After Thrombolysis) Score
    
    The HAT Score uses three clinical parameters to predict hemorrhage risk after tPA:
    
    1. Diabetes or hyperglycemia: History of diabetes mellitus OR initial glucose >200 mg/dL (1 point)
    2. NIH Stroke Scale: Pre-tPA severity assessment
       - <15: 0 points (mild to moderate stroke)
       - 15-20: 1 point (moderate to severe stroke)
       - >20: 2 points (severe stroke)
    3. CT hypodensity: Early ischemic changes on initial head CT
       - None: 0 points
       - <1/3 MCA territory: 1 point (limited early changes)
       - ≥1/3 MCA territory: 2 points (extensive early changes)
    
    Total score ranges from 0-5 points. Higher scores indicate greater hemorrhage risk.
    
    References (Vancouver style):
    1. Lou M, Safdar A, Mehdiratta M, Kumar S, Schlaug G, Caplan L, et al. The HAT Score: 
       a simple grading scale for predicting hemorrhage after thrombolysis. Neurology. 
       2008 Oct 28;71(18):1417-23. doi: 10.1212/01.wnl.0000330297.58334.dd.
    2. Cucchiara B, Kasner SE, Tanne D, Levine SR, Demchuk A, Messe SR, et al. Validation 
       assessment of risk scores to predict postthrombolysis intracerebral haemorrhage. 
       Int J Stroke. 2011 Apr;6(2):109-11. doi: 10.1111/j.1747-4949.2010.00555.x.
    """
    
    diabetes_or_glucose: Literal["no", "yes"] = Field(
        ...,
        description="History of diabetes mellitus OR initial blood glucose >200 mg/dL (>11.1 mmol/L). "
                    "Hyperglycemia is associated with increased hemorrhage risk after thrombolysis. "
                    "Scores 1 point if present.",
        example="no"
    )
    
    nihss_score: Literal["less_than_15", "15_to_20", "greater_than_20"] = Field(
        ...,
        description="Pre-tPA NIH Stroke Scale score indicating stroke severity. "
                    "Higher NIHSS scores correlate with larger infarcts and increased hemorrhage risk. "
                    "<15 = 0 points (mild-moderate), 15-20 = 1 point (moderate-severe), "
                    ">20 = 2 points (severe stroke).",
        example="less_than_15"
    )
    
    hypodensity_on_ct: Literal["no", "yes_less_than_one_third", "yes_one_third_or_more"] = Field(
        ...,
        description="Presence of easily visible hypodensity (early ischemic changes) on initial head CT. "
                    "Indicates extent of early infarction. No hypodensity = 0 points, "
                    "<1/3 MCA territory = 1 point (limited changes), "
                    "≥1/3 MCA territory = 2 points (extensive changes).",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "diabetes_or_glucose": "no",
                "nihss_score": "less_than_15",
                "hypodensity_on_ct": "no"
            }
        }


class HatScoreResponse(BaseModel):
    """
    Response model for HAT (Hemorrhage After Thrombolysis) Score
    
    The HAT Score stratifies post-tPA hemorrhage risk:
    - 0 points: Low risk (2% symptomatic ICH, 0% fatal)
    - 1 point: Low-moderate risk (5% symptomatic ICH, 3% fatal)
    - 2 points: Moderate risk (10% symptomatic ICH, 7% fatal)
    - 3 points: High risk (15% symptomatic ICH, 6% fatal)
    - 4-5 points: Very high risk (44% symptomatic ICH, 33% fatal)
    
    Symptomatic ICH is defined as hemorrhage causing clinical deterioration.
    The score helps objectify tPA risk but should not be the sole criterion for 
    withholding treatment in otherwise eligible patients.
    
    Reference: Lou M, et al. Neurology. 2008;71(18):1417-23.
    """
    
    result: int = Field(
        ...,
        description="HAT score calculated from clinical parameters (range: 0-5 points)",
        example=0,
        ge=0,
        le=5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of hemorrhage risk with specific percentages for "
                    "any hemorrhage, symptomatic ICH, and fatal hemorrhage",
        example="Low risk of hemorrhage after tPA. Any hemorrhage: 6%, Symptomatic ICH: 2%, "
                "Fatal hemorrhage: 0%. Benefits of tPA likely outweigh risks in eligible patients."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Low-Moderate Risk, Moderate Risk, High Risk, Very High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the hemorrhage risk level",
        example="Low hemorrhage risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "Low risk of hemorrhage after tPA. Any hemorrhage: 6%, Symptomatic ICH: 2%, "
                                  "Fatal hemorrhage: 0%. Benefits of tPA likely outweigh risks in eligible patients.",
                "stage": "Low Risk",
                "stage_description": "Low hemorrhage risk"
            }
        }