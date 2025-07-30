"""
BWH Egg Freezing Counseling Tool (EFCT) Models

Request and response models for BWH Egg Freezing Counseling Tool calculation.

References (Vancouver style):
1. Goldman RH, Racowsky C, Farland LV, Munné S, Ribustello L, Fox JH. Predicting the likelihood 
   of live birth for elective oocyte cryopreservation: a counseling tool for physicians and 
   patients. Hum Reprod. 2017 Apr 1;32(4):853-859. doi: 10.1093/humrep/dex008.
2. Doyle JO, Richter KS, Lim J, Stillman RJ, Graham JR, Tucker MJ. Successful elective and 
   medically indicated oocyte vitrification and warming for autologous in vitro fertilization, 
   with predicted birth probabilities for fertility preservation according to number of 
   cryopreserved oocytes and age at retrieval. Fertil Steril. 2016 Feb;105(2):459-66.e2. 
   doi: 10.1016/j.fertnstert.2015.10.026.
3. Harton GL, Munné S, Surrey M, Grifo J, Kaplan B, McCulloh DH, Griffin DK, Wells D; 
   PGD Practitioners Group. Diminished effect of maternal age on implantation after 
   preimplantation genetic diagnosis with array comparative genomic hybridization. 
   Fertil Steril. 2013 Dec;100(6):1695-703. doi: 10.1016/j.fertnstert.2013.07.2002.

The BWH Egg Freezing Counseling Tool (EFCT) was developed at Brigham and Women's Hospital 
to provide evidence-based counseling for women considering elective egg freezing. It predicts 
the probability of achieving at least one, two, or three live births based on a woman's age 
at the time of egg freezing and the number of mature eggs retrieved.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class BwhEggFreezingCounselingToolRequest(BaseModel):
    """
    Request model for BWH Egg Freezing Counseling Tool (EFCT)
    
    The EFCT uses two key parameters to predict live birth probability:
    
    1. Age: The woman's age at the time of egg retrieval and freezing
       - Range: 24-44 years
       - Impact: Younger age is associated with higher egg quality and better outcomes
       - Note: The model is less reliable for women ≥39 years due to limited data
    
    2. Number of mature eggs: The total number of mature (MII) oocytes retrieved and frozen
       - Range: 1-100 eggs
       - Impact: More eggs increase the probability of success
       - Note: Assumes standard vitrification techniques are used
    
    The tool calculates probabilities based on:
    - Age-specific blastocyst formation rates
    - Age-specific rates of chromosomally normal (euploid) embryos
    - Live birth rate per euploid blastocyst (approximately 60%)
    
    Important considerations:
    - Designed for elective egg freezing in healthy women
    - May overestimate success rates for medical egg freezing (e.g., cancer patients)
    - Assumes experienced embryology laboratory with good vitrification outcomes
    - Results are probabilities, not guarantees
    
    References (Vancouver style):
    1. Goldman RH, Racowsky C, Farland LV, Munné S, Ribustello L, Fox JH. Predicting the 
    likelihood of live birth for elective oocyte cryopreservation: a counseling tool for 
    physicians and patients. Hum Reprod. 2017 Apr 1;32(4):853-859. doi: 10.1093/humrep/dex008.
    """
    
    age: int = Field(
        ...,
        ge=24, le=44,
        description="Woman's age at time of egg freezing. Must be between 24 and 44 years. Younger women generally have better outcomes due to higher egg quality.",
        example=32
    )
    
    number_of_mature_eggs: int = Field(
        ...,
        ge=1, le=100,
        description="Number of mature (MII) eggs retrieved and frozen. More eggs increase the probability of success. Typical retrieval yields 8-15 eggs per cycle.",
        example=15
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 32,
                "number_of_mature_eggs": 15
            }
        }


class BwhEggFreezingCounselingToolResponse(BaseModel):
    """
    Response model for BWH Egg Freezing Counseling Tool (EFCT)
    
    The EFCT provides probability estimates for achieving live births through frozen eggs:
    
    Probability Calculations:
    - Based on age-specific rates of blastocyst formation and euploidy
    - Uses formula: P(Livebirth) = 1 - [1 - 0.6 × P(Euploid) × P(Blast)]^(Number of eggs)
    - Provides cumulative probabilities for multiple children
    
    Result Interpretation:
    - <10%: Very low probability - consider additional cycles or alternatives
    - 10-30%: Low probability - additional cycles would improve chances
    - 30-50%: Moderate probability - reasonable chance of success
    - 50-70%: Good probability - favorable odds
    - >70%: Excellent probability - very favorable prognosis
    
    Clinical Use:
    - Helps inform decision-making about egg freezing
    - Guides discussions about number of cycles needed
    - Sets realistic expectations for outcomes
    - Should be used alongside other clinical factors
    
    Limitations:
    - Not validated prospectively
    - Based on elective egg freezing data
    - Less accurate for women ≥39 years
    - Assumes optimal laboratory conditions
    
    Reference: Goldman RH, et al. Hum Reprod. 2017;32(4):853-859.
    """
    
    result: Dict[str, float] = Field(
        ...,
        description="Calculated probabilities for different numbers of live births",
        example={
            "at_least_one_live_birth": 0.654,
            "at_least_two_live_births": 0.342,
            "at_least_three_live_births": 0.147
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the results",
        example="probability"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the calculated probabilities with counseling guidance",
        example="With a 65.4% chance of at least one live birth, the probability of success is good. These are favorable odds, though additional eggs could further improve your chances if you desire multiple children or want additional reassurance."
    )
    
    stage: str = Field(
        ...,
        description="Probability category (Very Low, Low, Moderate, Good, Excellent)",
        example="Good"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the probability category",
        example="Good probability of live birth"
    )
    
    details: Dict[str, Any] = Field(
        ...,
        description="Additional calculation details including intermediate probabilities",
        example={
            "p_blast": 0.425,
            "p_euploid": 0.518,
            "p_live_birth_per_egg": 0.132,
            "age": 32,
            "number_of_eggs": 15
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": {
                    "at_least_one_live_birth": 0.654,
                    "at_least_two_live_births": 0.342,
                    "at_least_three_live_births": 0.147
                },
                "unit": "probability",
                "interpretation": "With a 65.4% chance of at least one live birth, the probability of success is good. These are favorable odds, though additional eggs could further improve your chances if you desire multiple children or want additional reassurance.",
                "stage": "Good",
                "stage_description": "Good probability of live birth",
                "details": {
                    "p_blast": 0.425,
                    "p_euploid": 0.518,
                    "p_live_birth_per_egg": 0.132,
                    "age": 32,
                    "number_of_eggs": 15
                }
            }
        }