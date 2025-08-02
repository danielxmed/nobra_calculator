"""
HEMORR₂HAGES Score for Major Bleeding Risk Models

Request and response models for HEMORR₂HAGES calculation.

References (Vancouver style):
1. Gage BF, Yan Y, Milligan PE, Waterman AD, Culverhouse R, Rich MW, et al. 
   Clinical classification schemes for predicting hemorrhage: results from the 
   National Registry of Atrial Fibrillation (NRAF). Am Heart J. 2006 Mar;151(3):713-9. 
   doi: 10.1016/j.ahj.2005.04.017.
2. Apostolakis S, Lane DA, Guo Y, Buller H, Lip GY. Performance of the 
   HEMORR(2)HAGES, ATRIA, and HAS-BLED bleeding risk-prediction scores in patients 
   with atrial fibrillation undergoing anticoagulation: the AMADEUS (evaluating the 
   use of SR34006 compared to warfarin or acenocoumarol in patients with atrial 
   fibrillation) study. J Am Coll Cardiol. 2012 Aug 28;60(9):861-7. 
   doi: 10.1016/j.jacc.2012.06.019.
3. Caldeira D, Costa J, Fernandes RM, Pinto FJ, Ferreira JJ. Performance of the 
   HAS-BLED high bleeding-risk category, compared to ATRIA and HEMORR2HAGES in 
   patients with atrial fibrillation: a systematic review and meta-analysis. 
   J Interv Card Electrophysiol. 2014 Dec;40(3):277-84. doi: 10.1007/s10840-014-9930-y.

The HEMORR₂HAGES score is a validated tool for assessing major bleeding risk in 
elderly patients with atrial fibrillation who are candidates for anticoagulation 
therapy. It incorporates 11 clinical factors to stratify patients into low (0-1), 
intermediate (2-3), or high (≥4) bleeding risk categories.
"""

from pydantic import BaseModel, Field
from typing import Literal


class Hemorr2hagesRequest(BaseModel):
    """
    Request model for HEMORR₂HAGES Score for Major Bleeding Risk
    
    The HEMORR₂HAGES score evaluates 11 risk factors for major bleeding:
    
    H - Hepatic or Renal Disease (1 point)
    E - Ethanol Abuse (1 point)
    M - Malignancy History (1 point)
    O - Older Age >75 years (1 point)
    R - Reduced Platelet Count or Function (1 point)
    R - Rebleeding Risk/Prior Major Bleed (2 points)
    H - Hypertension (Uncontrolled) (1 point)
    A - Anemia (1 point)
    G - Genetic Factors (1 point)
    E - Excessive Fall Risk (1 point)
    S - Stroke History (1 point)
    
    Total score ranges from 0-12 points. Higher scores indicate greater bleeding risk.
    
    References (Vancouver style):
    1. Gage BF, Yan Y, Milligan PE, Waterman AD, Culverhouse R, Rich MW, et al. 
       Clinical classification schemes for predicting hemorrhage: results from the 
       National Registry of Atrial Fibrillation (NRAF). Am Heart J. 2006 Mar;151(3):713-9.
    2. Apostolakis S, Lane DA, Guo Y, Buller H, Lip GY. Performance of the 
       HEMORR(2)HAGES, ATRIA, and HAS-BLED bleeding risk-prediction scores in patients 
       with atrial fibrillation undergoing anticoagulation: the AMADEUS study. 
       J Am Coll Cardiol. 2012 Aug 28;60(9):861-7.
    """
    
    hepatic_renal_disease: Literal["no", "yes"] = Field(
        ...,
        description="Presence of hepatic disease (cirrhosis, transaminases >3x normal) or renal disease (CrCl <30 mL/min, dialysis, transplant). Scores 1 point if yes",
        example="no"
    )
    
    ethanol_abuse: Literal["no", "yes"] = Field(
        ...,
        description="Current or recent history of ethanol (alcohol) abuse. Scores 1 point if yes",
        example="no"
    )
    
    malignancy: Literal["no", "yes"] = Field(
        ...,
        description="History of malignancy (cancer) at any time. Scores 1 point if yes",
        example="no"
    )
    
    older_age: Literal["no", "yes"] = Field(
        ...,
        description="Age greater than 75 years. Scores 1 point if yes",
        example="yes"
    )
    
    reduced_platelet: Literal["no", "yes"] = Field(
        ...,
        description="Reduced platelet count (<150,000) or function (includes aspirin use, other antiplatelet therapy, thrombocytopenia, or blood dyscrasia). Scores 1 point if yes",
        example="no"
    )
    
    rebleeding: Literal["no", "yes"] = Field(
        ...,
        description="Prior major bleeding episode requiring hospitalization or transfusion. This is the only criterion worth 2 points if yes",
        example="no"
    )
    
    hypertension: Literal["no", "yes"] = Field(
        ...,
        description="Uncontrolled hypertension (systolic BP >160 mmHg). Scores 1 point if yes",
        example="yes"
    )
    
    anemia: Literal["no", "yes"] = Field(
        ...,
        description="Anemia defined as hemoglobin <13 g/dL for men or <12 g/dL for women. Scores 1 point if yes",
        example="no"
    )
    
    genetic_factors: Literal["no", "yes"] = Field(
        ...,
        description="Genetic factors including CYP 2C9 single-nucleotide polymorphisms that affect warfarin metabolism. Scores 1 point if yes. Note: This may not be routinely available in clinical practice",
        example="no"
    )
    
    excessive_fall_risk: Literal["no", "yes"] = Field(
        ...,
        description="Patient at high risk for falls due to gait instability, cognitive impairment, or other factors. Scores 1 point if yes",
        example="no"
    )
    
    stroke: Literal["no", "yes"] = Field(
        ...,
        description="History of stroke (ischemic or hemorrhagic) or transient ischemic attack. Scores 1 point if yes",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "hepatic_renal_disease": "no",
                "ethanol_abuse": "no",
                "malignancy": "no",
                "older_age": "yes",
                "reduced_platelet": "no",
                "rebleeding": "no",
                "hypertension": "yes",
                "anemia": "no",
                "genetic_factors": "no",
                "excessive_fall_risk": "no",
                "stroke": "no"
            }
        }


class Hemorr2hagesResponse(BaseModel):
    """
    Response model for HEMORR₂HAGES Score for Major Bleeding Risk
    
    The score stratifies patients into three bleeding risk categories:
    - Low Risk (0-1 points): Low bleeding risk, anticoagulation benefit likely outweighs risk
    - Intermediate Risk (2-3 points): Moderate bleeding risk, careful assessment needed
    - High Risk (≥4 points): High bleeding risk, consider alternatives or intensive monitoring
    
    This tool should be used alongside stroke risk assessment tools (e.g., CHA₂DS₂-VASc) 
    to determine the net clinical benefit of anticoagulation in AF patients.
    
    Reference: Gage BF, et al. Am Heart J. 2006;151(3):713-9.
    """
    
    result: int = Field(
        ...,
        description="HEMORR₂HAGES total score (range: 0-12 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the bleeding risk and recommendations for anticoagulation management",
        example="Intermediate risk of major bleeding. Careful assessment of individual risk-benefit ratio is recommended. Consider patient preferences and close monitoring if anticoagulation is initiated."
    )
    
    stage: str = Field(
        ...,
        description="Bleeding risk category (Low Risk, Intermediate Risk, High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Score range description for the risk category",
        example="Score 2-3"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "Intermediate risk of major bleeding. Careful assessment of individual risk-benefit ratio is recommended. Consider patient preferences and close monitoring if anticoagulation is initiated.",
                "stage": "Intermediate Risk",
                "stage_description": "Score 2-3"
            }
        }