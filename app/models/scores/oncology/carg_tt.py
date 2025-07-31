"""
Cancer and Aging Research Group Chemotherapy Toxicity Tool (CARG-TT) Models

Request and response models for CARG-TT calculation.

References (Vancouver style):
1. Hurria A, Togawa K, Mohile SG, Owusu C, Klepin HD, Gross CP, et al. Predicting 
   chemotherapy toxicity in older adults with cancer: a prospective multicenter study. 
   J Clin Oncol. 2011 Sep 1;29(25):3457-65. doi: 10.1200/JCO.2011.34.7625.
2. Magnuson A, Sattar S, Nightingale G, Saracino R, Skoneczka J, Trevino KM, et al. 
   A practical guide to geriatric syndromes in older adults with cancer: A focus on 
   falls, cognition, polypharmacy, and depression. Am Soc Clin Oncol Educ Book. 
   2019 Jan;39:e96-e109. doi: 10.1200/EDBK_237641.
3. Extermann M, Boler I, Reich RR, Lyman GH, Brown RH, DeFelice J, et al. Predicting 
   the risk of chemotherapy toxicity in older patients: the Chemotherapy Risk Assessment 
   Scale for High-Age Patients (CRASH) score. Cancer. 2012 Jul 1;118(13):3377-86. 
   doi: 10.1002/cncr.26646.

The CARG-TT estimates the risk of severe chemotherapy-related side effects (Grade 3 
or greater toxicity) in older cancer patients (age >65). It uses 11 geriatric assessment 
variables, laboratory values, and patient characteristics to predict chemotherapy toxicity 
risk and is recommended by ASCO guidelines for geriatric oncology assessment.
"""

from pydantic import BaseModel, Field
from typing import Literal


class CargTtRequest(BaseModel):
    """
    Request model for Cancer and Aging Research Group Chemotherapy Toxicity Tool (CARG-TT)
    
    The CARG-TT is a validated clinical decision tool that predicts the risk of 
    severe (grade ≥3) chemotherapy-related toxicity in older adults with cancer 
    (age >65 years).
    
    The tool incorporates 11 variables:
    
    Patient Demographics:
    - Sex (male/female) - used for hemoglobin thresholds
    - Age ≥72 years (+2 points if yes)
    
    Cancer and Treatment Characteristics:
    - Gastrointestinal or genitourinary cancer (+2 points if yes)
    - Standard-dose chemotherapy vs. reduced dose (+2 points if standard)
    - Polychemotherapy (>1 drug) vs. single agent (+2 points if poly)
    
    Laboratory Values:
    - Low hemoglobin: males <11 g/dL, females <10 g/dL (+3 points if yes)
    - Creatinine clearance <34 mL/min (+3 points if yes)
    
    Geriatric Assessment Variables:
    - Hearing fair/poor/deaf vs. excellent/good (+2 points if impaired)
    - Falls in past 6 months (+3 points if yes)
    - Needs assistance with medication use (+1 point if yes)
    - Limited in walking one block or more (+2 points if yes)
    - Decreased social activity due to health (+1 point if yes)
    
    Risk Stratification:
    - Low Risk (0-5 points): 30% risk of grade ≥3 toxicity
    - Intermediate Risk (6-9 points): 52% risk of grade ≥3 toxicity
    - High Risk (10-23 points): 83% risk of grade ≥3 toxicity
    
    Clinical Applications:
    - Recommended by ASCO for geriatric oncology assessment
    - Helps guide treatment decisions (dose modification, supportive care)
    - Informs patient counseling about toxicity risk
    - Assists in monitoring intensity planning
    
    References (Vancouver style):
    1. Hurria A, Togawa K, Mohile SG, Owusu C, Klepin HD, Gross CP, et al. Predicting 
    chemotherapy toxicity in older adults with cancer: a prospective multicenter study. 
    J Clin Oncol. 2011 Sep 1;29(25):3457-65.
    """
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient sex (used for hemoglobin threshold determination: males <11 g/dL, females <10 g/dL)",
        example="female"
    )
    
    age_72_or_older: Literal["yes", "no"] = Field(
        ...,
        description="Patient age 72 years or older. Scores +2 points if yes",
        example="yes"
    )
    
    gi_gu_cancer: Literal["yes", "no"] = Field(
        ...,
        description="Gastrointestinal or genitourinary cancer type (vs. other cancer types). Scores +2 points if yes",
        example="no"
    )
    
    standard_dose_chemo: Literal["yes", "no"] = Field(
        ...,
        description="Standard-dose chemotherapy (100% of published dose vs. reduced dose <100%). Scores +2 points if yes",
        example="yes"
    )
    
    polychemotherapy: Literal["yes", "no"] = Field(
        ...,
        description="Polychemotherapy (combination of more than one chemotherapy drug vs. single agent). Scores +2 points if yes",
        example="no"
    )
    
    hemoglobin_low: Literal["yes", "no"] = Field(
        ...,
        description="Low hemoglobin based on sex-specific thresholds (males <11 g/dL, females <10 g/dL). Scores +3 points if yes",
        example="no"
    )
    
    creatinine_clearance_low: Literal["yes", "no"] = Field(
        ...,
        description="Creatinine clearance <34 mL/min (calculated using Cockcroft-Gault equation). Scores +3 points if yes",
        example="no"
    )
    
    hearing_impaired: Literal["yes", "no"] = Field(
        ...,
        description="Hearing rated as fair, poor, or totally deaf (vs. excellent or good). Scores +2 points if yes",
        example="no"
    )
    
    falls_past_6_months: Literal["yes", "no"] = Field(
        ...,
        description="History of one or more falls in the preceding 6 months. Scores +3 points if yes",
        example="no"
    )
    
    medication_assistance: Literal["yes", "no"] = Field(
        ...,
        description="Needs assistance with medication use (trouble taking medications as prescribed). Scores +1 point if yes",
        example="no"
    )
    
    walking_limited: Literal["yes", "no"] = Field(
        ...,
        description="Limited in walking one block or more due to health. Scores +2 points if yes",
        example="no"
    )
    
    social_activity_decreased: Literal["yes", "no"] = Field(
        ...,
        description="Decreased social activity because of physical or emotional health problems. Scores +1 point if yes",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "sex": "female",
                "age_72_or_older": "yes",
                "gi_gu_cancer": "no",
                "standard_dose_chemo": "yes",
                "polychemotherapy": "no",
                "hemoglobin_low": "no",
                "creatinine_clearance_low": "no",
                "hearing_impaired": "no",
                "falls_past_6_months": "no",
                "medication_assistance": "no",
                "walking_limited": "no",
                "social_activity_decreased": "no"
            }
        }


class CargTtResponse(BaseModel):
    """
    Response model for Cancer and Aging Research Group Chemotherapy Toxicity Tool (CARG-TT)
    
    The CARG-TT provides risk stratification for severe (grade ≥3) chemotherapy 
    toxicity in older adults with cancer:
    
    Risk Categories and Clinical Implications:
    - Low Risk (0-5 points): 30% toxicity risk - standard regimens generally appropriate
    - Intermediate Risk (6-9 points): 52% toxicity risk - consider dose reduction/enhanced support
    - High Risk (10-23 points): 83% toxicity risk - strongly consider dose reduction/alternative therapy
    
    Clinical Applications:
    - Treatment planning: guides dose modification decisions
    - Patient counseling: informs toxicity risk discussions
    - Supportive care: identifies patients needing enhanced monitoring
    - Research: standardizes geriatric assessment in oncology trials
    
    Implementation Considerations:
    - Recommended as part of comprehensive geriatric assessment
    - Should be used alongside clinical judgment
    - May inform treatment goals (curative vs. palliative intent)
    - Helps optimize benefit-to-risk ratio in older adults
    
    Performance Characteristics:
    - Developed and validated in 500 patients aged ≥65 years
    - C-statistic: 0.72 for predicting grade ≥3 toxicity
    - Recommended by ASCO guidelines for geriatric oncology
    - Complements other geriatric assessment tools (CRASH score)
    
    Reference: Hurria A, et al. J Clin Oncol. 2011;29(25):3457-65.
    """
    
    result: int = Field(
        ...,
        description="CARG-TT Score calculated from assessment variables (range: 0 to 23 points)",
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on toxicity risk category",
        example="Low risk of severe chemotherapy toxicity. Standard chemotherapy regimens can generally be considered. Monitor closely for side effects and provide supportive care as needed."
    )
    
    stage: str = Field(
        ...,
        description="Toxicity risk category (Low Risk, Intermediate Risk, or High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Percentage risk of grade ≥3 chemotherapy toxicity",
        example="30% risk of grade ≥3 toxicity"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "Low risk of severe chemotherapy toxicity. Standard chemotherapy regimens can generally be considered. Monitor closely for side effects and provide supportive care as needed.",
                "stage": "Low Risk",
                "stage_description": "30% risk of grade ≥3 toxicity"
            }
        }