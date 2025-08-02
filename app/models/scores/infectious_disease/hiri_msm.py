"""
HIV Incidence Risk Index for MSM (HIRI-MSM) Models

Request and response models for HIRI-MSM calculation.

References (Vancouver style):
1. Smith DK, Pals SL, Herbst JH, Shinde S, Carey JW. Development of a clinical screening 
   index predictive of incident HIV infection among men who have sex with men in the 
   United States. J Acquir Immune Defic Syndr. 2012 Aug 1;60(4):421-7. 
   doi: 10.1097/QAI.0b013e318256b2f6.
2. Wilton J, Noor SW, Schnubb A, Lawless J, Hart TA, Grennan T, et al. High HIV risk 
   and syndemic burden regardless of referral source among MSM screening for a PrEP 
   demonstration project in Toronto, Canada. BMC Public Health. 2018 Mar 2;18(1):292. 
   doi: 10.1186/s12889-018-5180-8.
3. Jones J, Hoenigl M, Siegler AJ, Sullivan PS, Little S, Rosenberg E. Assessing the 
   Performance of 3 Human Immunodeficiency Virus Incidence Risk Scores in a Cohort of 
   Black and White Men Who Have Sex With Men in the South. Sex Transm Dis. 2017 
   May;44(5):297-302. doi: 10.1097/OLQ.0000000000000596.

The HIRI-MSM is a validated 7-item screening tool developed by the CDC to identify 
MSM at high risk for HIV infection who should be prioritized for pre-exposure 
prophylaxis (PrEP) and other intensive HIV prevention interventions.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class HiriMsmRequest(BaseModel):
    """
    Request model for HIV Incidence Risk Index for MSM (HIRI-MSM)
    
    The HIRI-MSM evaluates 7 risk factors over the last 6 months:
    
    1. Age (years):
       - <18: 0 points (note: tool designed for ≥18)
       - 18-28: 8 points
       - 29-40: 5 points
       - 41-48: 2 points
       - ≥49: 0 points
    
    2. Number of male sex partners:
       - 0-5: 0 points
       - 6-10: 4 points
       - >10: 7 points
    
    3. Receptive anal sex without condom:
       - No: 0 points
       - Yes (≥1 time): 10 points
    
    4. Number of HIV-positive male sex partners:
       - 0: 0 points
       - 1: 4 points
       - >1: 8 points
    
    5. Insertive anal sex without condom with HIV-positive partner:
       - 0-4 times: 0 points
       - ≥5 times: 6 points
    
    6. Methamphetamine use:
       - No: 0 points
       - Yes: 5 points
    
    7. Poppers (amyl nitrate) use:
       - No: 0 points
       - Yes: 3 points
    
    Total score ranges from 0 to 47 points.
    
    References (Vancouver style):
    1. Smith DK, Pals SL, Herbst JH, Shinde S, Carey JW. Development of a clinical screening 
       index predictive of incident HIV infection among men who have sex with men in the 
       United States. J Acquir Immune Defic Syndr. 2012 Aug 1;60(4):421-7.
    2. Wilton J, Noor SW, Schnubb A, Lawless J, Hart TA, Grennan T, et al. High HIV risk 
       and syndemic burden regardless of referral source among MSM screening for a PrEP 
       demonstration project in Toronto, Canada. BMC Public Health. 2018 Mar 2;18(1):292.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in years. Younger age (18-28) is associated with highest risk, "
                    "scoring 8 points. Must be ≥18 years old",
        example=25
    )
    
    num_male_partners: Literal["0_to_5", "6_to_10", "more_than_10"] = Field(
        ...,
        description="Number of male sex partners in last 6 months. 0-5 partners scores 0 points, "
                    "6-10 partners scores 4 points, >10 partners scores 7 points",
        example="6_to_10"
    )
    
    receptive_anal_no_condom: Literal["no", "yes"] = Field(
        ...,
        description="Any receptive anal sex without condom in last 6 months. Major risk factor "
                    "scoring 10 points if present",
        example="yes"
    )
    
    num_hiv_positive_partners: Literal["none", "one", "more_than_one"] = Field(
        ...,
        description="Number of HIV-positive male sex partners in last 6 months. None scores 0 points, "
                    "one scores 4 points, more than one scores 8 points",
        example="one"
    )
    
    insertive_anal_hiv_positive: Literal["0_to_4_times", "5_or_more_times"] = Field(
        ...,
        description="Insertive anal sex without condom with HIV-positive partner in last 6 months. "
                    "0-4 times scores 0 points, ≥5 times scores 6 points",
        example="0_to_4_times"
    )
    
    methamphetamine_use: Literal["no", "yes"] = Field(
        ...,
        description="Any methamphetamine use in last 6 months. Associated with increased HIV risk, "
                    "scores 5 points if present",
        example="no"
    )
    
    poppers_use: Literal["no", "yes"] = Field(
        ...,
        description="Any poppers (amyl nitrate) use in last 6 months. Associated with increased "
                    "HIV risk, scores 3 points if present",
        example="yes"
    )
    
    @validator('age')
    def validate_age(cls, v):
        if v < 18:
            raise ValueError('HIRI-MSM is designed for MSM aged 18 years and older')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "age": 25,
                "num_male_partners": "6_to_10",
                "receptive_anal_no_condom": "yes",
                "num_hiv_positive_partners": "one",
                "insertive_anal_hiv_positive": "0_to_4_times",
                "methamphetamine_use": "no",
                "poppers_use": "yes"
            }
        }


class HiriMsmResponse(BaseModel):
    """
    Response model for HIV Incidence Risk Index for MSM (HIRI-MSM)
    
    The HIRI-MSM stratifies MSM into risk categories:
    - Low Risk (<10 points): Standard HIV prevention counseling
    - High Risk (≥10 points): Consider PrEP and intensive prevention
    
    Clinical Application:
    - Score ≥10 has 84% sensitivity and 45% specificity for incident HIV
    - Recommended cutoff for PrEP consideration
    - Performance may vary by population and geographic region
    - Should be used alongside clinical judgment
    
    Reference: Smith DK, et al. J Acquir Immune Defic Syndr. 2012;60(4):421-7.
    """
    
    result: int = Field(
        ...,
        description="HIRI-MSM risk score for HIV incidence (range: 0-47 points)",
        example=17
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with prevention recommendations based on risk category",
        example="High HIV risk. This score has 84% sensitivity and 45% specificity for predicting incident HIV infection in the next 6 months. Strongly consider pre-exposure prophylaxis (PrEP) and intensive HIV prevention interventions. Discuss risk reduction strategies and increase HIV testing frequency."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk or High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the score range for the risk category",
        example="Score ≥10"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 17,
                "unit": "points",
                "interpretation": "High HIV risk. This score has 84% sensitivity and 45% specificity for predicting incident HIV infection in the next 6 months. Strongly consider pre-exposure prophylaxis (PrEP) and intensive HIV prevention interventions. Discuss risk reduction strategies and increase HIV testing frequency.",
                "stage": "High Risk",
                "stage_description": "Score ≥10"
            }
        }