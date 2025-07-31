"""
Dual Antiplatelet Therapy (DAPT) Score Models

Request and response models for DAPT score calculation.

References (Vancouver style):
1. Yeh RW, Secemsky EA, Kereiakes DJ, Normand SLT, Gershlick AH, Cohen DJ, et al. 
   Development and Validation of a Prediction Rule for Benefit and Harm of Dual 
   Antiplatelet Therapy Beyond 1 Year After Percutaneous Coronary Intervention. 
   JAMA. 2016;315(16):1735-49. doi: 10.1001/jama.2016.3775.
2. Levine GN, Bates ER, Bittl JA, Brindis RG, Fihn SD, Fleisher LA, et al. 
   2016 ACC/AHA Guideline Focused Update on Duration of Dual Antiplatelet Therapy 
   in Patients With Coronary Artery Disease. Circulation. 2016;134(10):e123-55. 
   doi: 10.1161/CIR.0000000000000404.
3. Costa F, van Klaveren D, James S, Heg D, Räber L, Feres F, et al. Derivation and 
   validation of the predicting bleeding complications in patients undergoing stent 
   implantation and subsequent dual antiplatelet therapy (PRECISE-DAPT) score: a pooled 
   analysis of individual-patient datasets from clinical trials. Lancet. 2017;389(10073):1025-1034. 
   doi: 10.1016/S0140-6736(17)30397-5.

The DAPT Score predicts which patients will benefit from prolonged dual antiplatelet 
therapy after coronary stent placement. Developed from the DAPT Study randomized trial 
data with 11,648 patients, it uses nine clinical variables to identify patients with 
high ischemic but low bleeding risk (score ≥2) who benefit from extended DAPT, and 
those with high bleeding but low ischemic risk (score <2) who may be harmed by 
prolonged DAPT duration.
"""

from pydantic import BaseModel, Field
from typing import Literal


class DaptScoreRequest(BaseModel):
    """
    Request model for Dual Antiplatelet Therapy (DAPT) Score
    
    The DAPT Score uses nine clinical variables to predict benefit/risk ratio for 
    prolonged DAPT beyond 12 months after coronary stent placement:
    
    Age Scoring:
    - <65 years: 0 points
    - 65-74 years: -1 point
    - ≥75 years: -2 points
    
    Clinical Risk Factors (each "yes" response adds points):
    - Diabetes mellitus: +1 point
    - Current cigarette smoking: +1 point
    - Prior myocardial infarction or prior PCI: +1 point
    - Stent diameter <3 mm: +1 point
    - Congestive heart failure or LVEF <30%: +2 points
    - Saphenous vein graft PCI: +2 points
    - Myocardial infarction at presentation: +1 point
    
    Special Consideration:
    - Paclitaxel-eluting stent: -1 point (reduces score)
    
    Score Interpretation:
    - Score ≥2: Favorable benefit/risk ratio for prolonged DAPT
    - Score <2: Unfavorable benefit/risk ratio for prolonged DAPT
    
    Clinical Application:
    - Applies to patients who completed 12 months of DAPT without major events
    - Helps guide decision for continuing DAPT beyond standard duration
    - Balances ischemic benefit against bleeding risk
    - Should be used with clinical judgment and patient preferences

    References (Vancouver style):
    1. Yeh RW, Secemsky EA, Kereiakes DJ, Normand SLT, Gershlick AH, Cohen DJ, et al. 
       Development and Validation of a Prediction Rule for Benefit and Harm of Dual 
       Antiplatelet Therapy Beyond 1 Year After Percutaneous Coronary Intervention. 
       JAMA. 2016;315(16):1735-49. doi: 10.1001/jama.2016.3775.
    2. Levine GN, Bates ER, Bittl JA, Brindis RG, Fihn SD, Fleisher LA, et al. 
       2016 ACC/AHA Guideline Focused Update on Duration of Dual Antiplatelet Therapy 
       in Patients With Coronary Artery Disease. Circulation. 2016;134(10):e123-55.
    3. Costa F, van Klaveren D, James S, Heg D, Räber L, Feres F, et al. Derivation and 
       validation of the predicting bleeding complications in patients undergoing stent 
       implantation and subsequent dual antiplatelet therapy (PRECISE-DAPT) score: a pooled 
       analysis of individual-patient datasets from clinical trials. Lancet. 2017;389(10073):1025-1034.
    """
    
    age: int = Field(
        ...,
        description="Patient age in years. Scoring: <65 years (0 pts), 65-74 years (-1 pt), ≥75 years (-2 pts)",
        ge=18,
        le=120,
        example=67
    )
    
    diabetes_mellitus: Literal["yes", "no"] = Field(
        ...,
        description="History of diabetes mellitus. Scoring: Yes (+1 pt), No (0 pts)",
        example="yes"
    )
    
    current_smoking: Literal["yes", "no"] = Field(
        ...,
        description="Current cigarette smoking. Scoring: Yes (+1 pt), No (0 pts)",
        example="no"
    )
    
    prior_mi_or_pci: Literal["yes", "no"] = Field(
        ...,
        description="Prior myocardial infarction or prior percutaneous coronary intervention. Scoring: Yes (+1 pt), No (0 pts)",
        example="yes"
    )
    
    stent_diameter_small: Literal["yes", "no"] = Field(
        ...,
        description="Stent diameter <3 mm (small stent). Scoring: Yes (+1 pt), No (0 pts)",
        example="no"
    )
    
    chf_or_low_ef: Literal["yes", "no"] = Field(
        ...,
        description="History of congestive heart failure or left ventricular ejection fraction <30%. Scoring: Yes (+2 pts), No (0 pts)",
        example="no"
    )
    
    vein_graft_pci: Literal["yes", "no"] = Field(
        ...,
        description="Saphenous vein graft percutaneous coronary intervention. Scoring: Yes (+2 pts), No (0 pts)",
        example="no"
    )
    
    paclitaxel_eluting_stent: Literal["yes", "no"] = Field(
        ...,
        description="Paclitaxel-eluting stent used. Scoring: Yes (-1 pt), No (0 pts)",
        example="no"
    )
    
    mi_at_presentation: Literal["yes", "no"] = Field(
        ...,
        description="Myocardial infarction at presentation (index event). Scoring: Yes (+1 pt), No (0 pts)",
        example="yes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 67,
                "diabetes_mellitus": "yes",
                "current_smoking": "no",
                "prior_mi_or_pci": "yes",
                "stent_diameter_small": "no",
                "chf_or_low_ef": "no",
                "vein_graft_pci": "no",
                "paclitaxel_eluting_stent": "no",
                "mi_at_presentation": "yes"
            }
        }


class DaptScoreResponse(BaseModel):
    """
    Response model for Dual Antiplatelet Therapy (DAPT) Score
    
    The DAPT Score ranges from approximately -2 to +10 points and stratifies patients 
    into two categories based on benefit/risk ratio for prolonged DAPT:
    
    Score Categories:
    - Low Score (<2 points): Unfavorable benefit/risk ratio
      * High bleeding risk and low ischemic risk
      * Consider discontinuing DAPT at 12 months
      * Number needed to treat (NNT) to prevent ischemic event: 169
      * Number needed to harm (NNH) to cause bleeding: 69
      * Risk of bleeding complications outweighs ischemic benefits
    
    - High Score (≥2 points): Favorable benefit/risk ratio
      * High ischemic risk and low bleeding risk
      * Consider continuing DAPT beyond 12 months (up to 30 months)
      * Number needed to treat (NNT) to prevent ischemic event: 33
      * Number needed to harm (NNH) to cause bleeding: 263
      * Ischemic benefits outweigh bleeding risks
    
    Clinical Decision Making:
    - Patients with high DAPT scores derived ischemic benefit from extending DAPT
    - Patients with low DAPT scores were harmed by prolonging DAPT duration
    - Should be used in conjunction with clinical judgment and patient preferences
    - Consider individual bleeding and ischemic risk factors not captured in score
    - Applies to patients who completed 12 months of DAPT without major events
    
    Important Considerations:
    - Score developed from DAPT Study randomized trial (n=11,648 patients)
    - Validated in patients who completed 12 months of DAPT without events
    - Does not apply to patients with recent bleeding or ischemic events
    - Consider patient preferences and quality of life in decision making
    - Regular reassessment of bleeding and ischemic risk is recommended
    
    Reference: Yeh RW, et al. JAMA. 2016;315(16):1735-49.
    """
    
    result: int = Field(
        ...,
        description="DAPT score for prolonged dual antiplatelet therapy benefit (-2 to +10 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on score",
        example="DAPT score ≥2 indicates favorable benefit/risk ratio for prolonged DAPT. High ischemic risk and low bleeding risk. Consider continuing DAPT beyond 12 months. NNT to prevent ischemic event: 33, NNH to cause bleeding: 263."
    )
    
    stage: str = Field(
        ...,
        description="Score category (Low Score (<2) or High Score (≥2))",
        example="High Score (≥2)"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the benefit/risk ratio",
        example="Favorable benefit/risk ratio"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "DAPT score ≥2 indicates favorable benefit/risk ratio for prolonged DAPT. High ischemic risk and low bleeding risk. Consider continuing DAPT beyond 12 months. NNT to prevent ischemic event: 33, NNH to cause bleeding: 263.",
                "stage": "High Score (≥2)",
                "stage_description": "Favorable benefit/risk ratio"
            }
        }