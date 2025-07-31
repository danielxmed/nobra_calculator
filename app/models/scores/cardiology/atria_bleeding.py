"""
ATRIA Bleeding Risk Score Models

Request and response models for ATRIA Bleeding Risk Score calculation.

References (Vancouver style):
1. Fang MC, Go AS, Chang Y, Borowsky LH, Pomernacki NK, Udaltsova N, et al. A new risk 
   scheme to predict warfarin-associated hemorrhage: The ATRIA (Anticoagulation and Risk 
   Factors in Atrial Fibrillation) Study. J Am Coll Cardiol. 2011 Jul 19;58(4):395-401. 
   doi: 10.1016/j.jacc.2011.03.031.
2. Roldán V, Marín F, Fernández H, Manzano-Fernández S, Gallego P, Valdés M, et al. 
   Predictive value of the HAS-BLED and ATRIA bleeding scores for the risk of serious 
   bleeding in a "real-world" population with atrial fibrillation receiving anticoagulant 
   therapy. Chest. 2013 Jan;143(1):179-184. doi: 10.1378/chest.12-0608.
3. Senoo K, Proietti M, Lane DA, Lip GY. Evaluation of the HAS-BLED, ATRIA, and ORBIT 
   Bleeding Risk Scores in Patients with Atrial Fibrillation Taking Warfarin. Am J Med. 
   2016 Jun;129(6):600-7. doi: 10.1016/j.amjmed.2015.10.001.

The ATRIA bleeding risk score was developed to stratify bleeding risk in patients with 
atrial fibrillation on warfarin therapy. It uses five clinical risk factors to predict 
the annual risk of major hemorrhage, helping clinicians balance the risks and benefits 
of anticoagulation therapy.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AtriaBleedingRequest(BaseModel):
    """
    Request model for ATRIA Bleeding Risk Score
    
    The ATRIA score uses 5 clinical variables to assess bleeding risk in patients 
    on warfarin for atrial fibrillation:
    
    - Anemia: Hemoglobin <13 g/dL in males or <12 g/dL in females (3 points)
    - Severe renal disease: GFR <30 mL/min or dialysis-dependent (3 points)
    - Age ≥75 years (2 points)
    - Prior hemorrhage: Any prior hemorrhage diagnosis (1 point)
    - Hypertension: History of hypertension (1 point)
    
    Total score ranges from 0-10 points.
    
    References (Vancouver style):
    1. Fang MC, Go AS, Chang Y, Borowsky LH, Pomernacki NK, Udaltsova N, et al. A new risk 
    scheme to predict warfarin-associated hemorrhage: The ATRIA (Anticoagulation and Risk 
    Factors in Atrial Fibrillation) Study. J Am Coll Cardiol. 2011 Jul 19;58(4):395-401. 
    doi: 10.1016/j.jacc.2011.03.031.
    """
    
    anemia: Literal["yes", "no"] = Field(
        ...,
        description="Presence of anemia (Hemoglobin <13 g/dL in males or <12 g/dL in females). This is the most heavily weighted risk factor, contributing 3 points to the total score.",
        example="no"
    )
    
    severe_renal_disease: Literal["yes", "no"] = Field(
        ...,
        description="Severe renal disease defined as GFR <30 mL/min or dialysis-dependent. This is another major risk factor, contributing 3 points to the total score.",
        example="no"
    )
    
    age_75_or_over: Literal["yes", "no"] = Field(
        ...,
        description="Age ≥75 years. Advanced age increases bleeding risk and contributes 2 points to the total score.",
        example="yes"
    )
    
    prior_hemorrhage: Literal["yes", "no"] = Field(
        ...,
        description="Any prior hemorrhage diagnosis (e.g., gastrointestinal bleed, intracranial hemorrhage, or other significant bleeding events). Contributes 1 point to the total score.",
        example="no"
    )
    
    hypertension: Literal["yes", "no"] = Field(
        ...,
        description="History of hypertension (diagnosed high blood pressure). Contributes 1 point to the total score.",
        example="yes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "anemia": "no",
                "severe_renal_disease": "no",
                "age_75_or_over": "yes",
                "prior_hemorrhage": "no",
                "hypertension": "yes"
            }
        }


class AtriaBleedingResponse(BaseModel):
    """
    Response model for ATRIA Bleeding Risk Score
    
    The ATRIA score stratifies patients into three risk categories:
    - Low risk (0-3 points): <1% annual major hemorrhage risk
    - Intermediate risk (4 points): 2.6% annual major hemorrhage risk
    - High risk (5-10 points): 5.8% annual major hemorrhage risk
    
    Major hemorrhage is defined as fatal bleeding, bleeding requiring ≥2 units of blood 
    transfusion, or hemorrhage into a critical anatomical site.
    
    Reference: Fang MC, et al. J Am Coll Cardiol. 2011;58(4):395-401.
    """
    
    result: int = Field(
        ...,
        description="ATRIA bleeding risk score calculated from clinical variables (range: 0-10 points)",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the bleeding risk and recommendations for anticoagulation management",
        example="Low risk (<1%) of major hemorrhage per year. These patients have the lowest bleeding risk on warfarin therapy. Consider standard anticoagulation management with regular INR monitoring."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low, Intermediate, or High)",
        example="Low"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Low bleeding risk"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "Low risk (<1%) of major hemorrhage per year. These patients have the lowest bleeding risk on warfarin therapy. Consider standard anticoagulation management with regular INR monitoring.",
                "stage": "Low",
                "stage_description": "Low bleeding risk"
            }
        }