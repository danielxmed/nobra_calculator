"""
Chemotherapy Risk Assessment Scale for High-Age Patients (CRASH) Score Models

Request and response models for CRASH score calculation.

References (Vancouver style):
1. Extermann M, Boler I, Reich RR, Lyman GH, Brown RH, DeFelice J, et al. Predicting 
   the risk of chemotherapy toxicity in older patients: the Chemotherapy Risk Assessment 
   Scale for High-Age Patients (CRASH) score. Cancer. 2012 Jul 1;118(13):3377-86. 
   doi: 10.1002/cncr.26646.
2. Extermann M, Reich RR, Sehovic M. Chemotoxicity recalibration in the common 
   terminology criteria for adverse events version 4.0 in older patients with cancer: 
   Development of a training set. J Geriatr Oncol. 2013 Oct;4(4):353-8. 
   doi: 10.1016/j.jgo.2013.04.001.

The CRASH score is a validated tool for predicting severe chemotherapy toxicity in 
older cancer patients (≥70 years). It separately assesses risk for hematologic 
(grade 4) and nonhematologic (grade 3/4) toxicities based on patient characteristics 
and chemotherapy regimen toxicity profiles.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class CrashScoreRequest(BaseModel):
    """
    Request model for Chemotherapy Risk Assessment Scale for High-Age Patients (CRASH) Score
    
    The CRASH score uses 8 clinical variables to predict chemotherapy toxicity risk:
    
    Hematologic toxicity predictors:
    - Diastolic BP: ≤72 mmHg (0 points), >72 mmHg (+1 point)
    - IADL score: 26-29 (0 points), 10-25 (+1 point)
    - LDH: 0-459 U/L (0 points), >459 U/L (+2 points)
    - Chemotherapy risk (hematologic): 0-0.44 (0 points), 0.45-0.57 (+1 point), >0.57 (+2 points)
    
    Nonhematologic toxicity predictors:
    - ECOG PS: 0 (0 points), 1-2 (+1 point), 3-4 (+2 points)
    - MMSE: 30 (0 points), <30 (+2 points)
    - MNA: 28-30 (0 points), <28 (+2 points)
    - Chemotherapy risk (nonhematologic): 0 (0 points), 1 (+1 point), 2 (+2 points)
    
    Combined score counts chemotherapy risk only once to avoid duplication.

    References (Vancouver style):
    1. Extermann M, Boler I, Reich RR, Lyman GH, Brown RH, DeFelice J, et al. Predicting 
    the risk of chemotherapy toxicity in older patients: the Chemotherapy Risk Assessment 
    Scale for High-Age Patients (CRASH) score. Cancer. 2012 Jul 1;118(13):3377-86. 
    doi: 10.1002/cncr.26646.
    """
    
    diastolic_bp: Literal["lte_72", "gt_72"] = Field(
        ...,
        description="Diastolic blood pressure. ≤72 mmHg scores 0 points, >72 mmHg scores +1 point",
        example="gt_72"
    )
    
    iadl_score: Literal["26_to_29", "10_to_25"] = Field(
        ...,
        description="Instrumental Activities of Daily Living (IADL) score. Range 0-29, higher scores indicate better function. 26-29 scores 0 points, 10-25 scores +1 point",
        example="26_to_29"
    )
    
    ldh: Literal["0_to_459", "gt_459"] = Field(
        ...,
        description="Lactate dehydrogenase (LDH) level in U/L. 0-459 U/L scores 0 points, >459 U/L scores +2 points",
        example="0_to_459"
    )
    
    chemo_risk_hematologic: Literal["0_to_0.44", "0.45_to_0.57", "gt_0.57"] = Field(
        ...,
        description="Chemotherapy risk score for hematologic toxicity based on regimen. 0-0.44 scores 0 points, 0.45-0.57 scores +1 point, >0.57 scores +2 points",
        example="0.45_to_0.57"
    )
    
    ecog_ps: Literal["0", "1_to_2", "3_to_4"] = Field(
        ...,
        description="ECOG Performance Status. 0 scores 0 points, 1-2 scores +1 point, 3-4 scores +2 points",
        example="1_to_2"
    )
    
    mmse: Literal["30", "lt_30"] = Field(
        ...,
        description="Mini Mental State Examination (MMSE) score. Perfect score of 30 scores 0 points, <30 scores +2 points",
        example="30"
    )
    
    mna: Literal["28_to_30", "lt_28"] = Field(
        ...,
        description="Mini Nutritional Assessment (MNA) score. 28-30 (normal) scores 0 points, <28 scores +2 points",
        example="28_to_30"
    )
    
    chemo_risk_nonhematologic: Literal["0", "1", "2"] = Field(
        ...,
        description="Chemotherapy risk score for nonhematologic toxicity based on regimen. 0 scores 0 points, 1 scores +1 point, 2 scores +2 points",
        example="1"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "diastolic_bp": "gt_72",
                "iadl_score": "26_to_29",
                "ldh": "0_to_459",
                "chemo_risk_hematologic": "0.45_to_0.57",
                "ecog_ps": "1_to_2",
                "mmse": "30",
                "mna": "28_to_30",
                "chemo_risk_nonhematologic": "1"
            }
        }


class CrashScoreSubscores(BaseModel):
    """Subscore details for CRASH score"""
    
    hematologic: Dict[str, Any] = Field(
        ...,
        description="Hematologic toxicity subscore details"
    )
    
    nonhematologic: Dict[str, Any] = Field(
        ...,
        description="Nonhematologic toxicity subscore details"
    )


class CrashScoreResult(BaseModel):
    """Result details for CRASH score"""
    
    combined_score: int = Field(
        ...,
        description="Combined CRASH score (0-16 points)",
        example=5
    )
    
    hematologic_score: int = Field(
        ...,
        description="Hematologic toxicity subscore (0-6 points)",
        example=2
    )
    
    nonhematologic_score: int = Field(
        ...,
        description="Nonhematologic toxicity subscore (0-8 points)",
        example=3
    )


class CrashScoreResponse(BaseModel):
    """
    Response model for Chemotherapy Risk Assessment Scale for High-Age Patients (CRASH) Score
    
    The CRASH score provides risk stratification for chemotherapy toxicity:
    
    Combined score risk categories:
    - Low (0-3 points): Low risk for severe toxicity
    - Low-Intermediate (4-6 points): Moderate risk, close monitoring advised
    - Intermediate-High (7-9 points): High risk, consider dose reduction
    - High (≥10 points): Very high risk, consider alternative therapy
    
    Toxicity definitions:
    - Hematologic: Grade 4 toxicity per CTCAE v3.0
    - Nonhematologic: Grade 3/4 toxicity per CTCAE v3.0
    
    Reference: Extermann M, et al. Cancer. 2012;118(13):3377-86.
    """
    
    result: CrashScoreResult = Field(
        ...,
        description="CRASH score results including combined and subscores"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the combined CRASH score",
        example="Low-intermediate risk for severe chemotherapy toxicity. Consider close monitoring and early intervention strategies."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low, Low-Intermediate, Intermediate-High, High)",
        example="Low-Intermediate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Low-intermediate risk"
    )
    
    subscores: CrashScoreSubscores = Field(
        ...,
        description="Detailed breakdown of hematologic and nonhematologic subscores"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "combined_score": 5,
                    "hematologic_score": 2,
                    "nonhematologic_score": 3
                },
                "unit": "points",
                "interpretation": "Low-intermediate risk for severe chemotherapy toxicity. Consider close monitoring and early intervention strategies.",
                "stage": "Low-Intermediate",
                "stage_description": "Low-intermediate risk",
                "subscores": {
                    "hematologic": {
                        "score": 2,
                        "risk": "Low-Intermediate",
                        "interpretation": "Low-intermediate risk (~23%) of grade 4 hematologic toxicity"
                    },
                    "nonhematologic": {
                        "score": 3,
                        "risk": "Low-Intermediate",
                        "interpretation": "Low-intermediate risk (~46%) of grade 3/4 nonhematologic toxicity"
                    }
                }
            }
        }