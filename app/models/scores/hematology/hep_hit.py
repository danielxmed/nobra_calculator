"""
HIT Expert Probability (HEP) Score for Heparin-Induced Thrombocytopenia Models

Request and response models for HEP score calculation.

References (Vancouver style):
1. Cuker A, Arepally G, Crowther MA, Rice L, Datko F, Hook K, et al. The HIT Expert 
   Probability (HEP) Score: a novel pre-test probability model for heparin-induced 
   thrombocytopenia based on broad expert opinion. J Thromb Haemost. 2010 Dec;8(12):2642-50. 
   doi: 10.1111/j.1538-7836.2010.04059.x.
2. Joseph J, Rabbolini D, Enjeti AK, Favaloro E, Kopp S, McRae S, et al. Prospective 
   comparison of the HEP score and 4Ts score for the diagnosis of heparin-induced 
   thrombocytopenia. Blood Adv. 2018 Nov 27;2(22):3155-3162. 
   doi: 10.1182/bloodadvances.2018023077.
3. Lillo-Le Louet A, Boutouyrie P, Alhenc-Gelas M, Le Beller C, Gautier I, Aiach M, et al. 
   External validation of the HIT Expert Probability (HEP) score. Thromb Haemost. 
   2015 Mar;113(3):633-40. doi: 10.1160/TH14-06-0478.

The HEP score is a pre-test clinical scoring model for heparin-induced thrombocytopenia 
based on broad expert opinion from 26 HIT experts. It evaluates 8 clinical features to 
stratify patients into low, intermediate, or high probability of HIT, helping guide 
decisions about alternative anticoagulation and laboratory testing.
"""

from pydantic import BaseModel, Field
from typing import Literal


class HepHitRequest(BaseModel):
    """
    Request model for HIT Expert Probability (HEP) Score
    
    The HEP score evaluates 8 clinical features to determine pre-test probability of HIT:
    
    1. Magnitude of Platelet Fall:
       - <30%: -1 point
       - 30-50%: 1 point
       - >50%: 3 points
    
    2. Timing of Platelet Fall:
       - <4 days (without recent heparin): -1 point
       - Day 4 (recent heparin exposure): 2 points
       - Days 5-10 (without recent heparin): 3 points
       - Days 11-14: 2 points
       - >14 days: -1 point
    
    3. Nadir Platelet Count:
       - ≤20 × 10⁹/L: -2 points
       - >20 × 10⁹/L: 2 points
    
    4. Thrombosis:
       - New VTE/ATE ≥4 days after heparin: 3 points
       - Progression of pre-existing VTE/ATE: 2 points
       - None: 0 points
    
    5. Skin Necrosis at Injection Sites: 3 points if present
    6. Acute Systemic Reaction after IV Heparin: 2 points if present
    7. Bleeding/Petechiae: -1 point if present
    8. Other Causes of Thrombocytopenia:
       - Definite other cause: -3 points
       - Possible other cause: -1 point
       - None apparent: 0 points
    
    Total score ranges from -7 to +15 points.
    
    References (Vancouver style):
    1. Cuker A, Arepally G, Crowther MA, Rice L, Datko F, Hook K, et al. The HIT Expert 
       Probability (HEP) Score: a novel pre-test probability model for heparin-induced 
       thrombocytopenia based on broad expert opinion. J Thromb Haemost. 2010 Dec;8(12):2642-50.
    2. Joseph J, Rabbolini D, Enjeti AK, Favaloro E, Kopp S, McRae S, et al. Prospective 
       comparison of the HEP score and 4Ts score for the diagnosis of heparin-induced 
       thrombocytopenia. Blood Adv. 2018 Nov 27;2(22):3155-3162.
    """
    
    magnitude_fall: Literal["less_than_30", "30_to_50", "greater_than_50"] = Field(
        ...,
        description="Magnitude of platelet count fall from baseline. Less than 30% scores -1 point, "
                    "30-50% scores 1 point, greater than 50% scores 3 points",
        example="greater_than_50"
    )
    
    timing_platelet_fall: Literal["less_than_4_days", "4_days", "5_to_10_days", "11_to_14_days", "greater_than_14_days"] = Field(
        ...,
        description="Timing of platelet count fall. <4 days without recent heparin scores -1, "
                    "day 4 with recent heparin scores 2, days 5-10 scores 3, days 11-14 scores 2, "
                    ">14 days scores -1",
        example="5_to_10_days"
    )
    
    nadir_platelet_count: Literal["20_or_less", "greater_than_20"] = Field(
        ...,
        description="Lowest platelet count reached. ≤20 × 10⁹/L scores -2 points, >20 × 10⁹/L scores 2 points",
        example="greater_than_20"
    )
    
    thrombosis: Literal["new_vte_ate", "progression_vte_ate", "none"] = Field(
        ...,
        description="Presence and type of thrombosis. New VTE/ATE ≥4 days after heparin scores 3 points, "
                    "progression of pre-existing VTE/ATE scores 2 points, none scores 0 points",
        example="none"
    )
    
    skin_necrosis: Literal["yes", "no"] = Field(
        ...,
        description="Skin necrosis at heparin injection sites. Scores 3 points if present",
        example="no"
    )
    
    acute_systemic_reaction: Literal["yes", "no"] = Field(
        ...,
        description="Acute systemic reaction (fever, chills, hypertension) after IV heparin bolus. "
                    "Scores 2 points if present",
        example="no"
    )
    
    bleeding: Literal["yes", "no"] = Field(
        ...,
        description="Presence of bleeding or petechiae. Scores -1 point if present as it suggests "
                    "alternative causes of thrombocytopenia",
        example="no"
    )
    
    other_causes_thrombocytopenia: Literal["definite", "possible", "none"] = Field(
        ...,
        description="Presence of other causes of thrombocytopenia (sepsis, DIC, medications, etc). "
                    "Definite other cause scores -3 points, possible scores -1 point, none scores 0 points",
        example="none"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "magnitude_fall": "greater_than_50",
                "timing_platelet_fall": "5_to_10_days",
                "nadir_platelet_count": "greater_than_20",
                "thrombosis": "new_vte_ate",
                "skin_necrosis": "no",
                "acute_systemic_reaction": "no",
                "bleeding": "no",
                "other_causes_thrombocytopenia": "none"
            }
        }


class HepHitResponse(BaseModel):
    """
    Response model for HIT Expert Probability (HEP) Score
    
    The HEP score stratifies patients into risk categories for HIT:
    - Low Probability (<2 points): 100% sensitivity, effectively rules out HIT
    - Intermediate Probability (2-4 points): Requires further testing
    - High Probability (≥5 points): 86% sensitivity, 88% specificity
    
    Clinical Application:
    - Low risk patients can avoid unnecessary alternative anticoagulation
    - Intermediate risk patients require HIT antibody testing
    - High risk patients should have heparin stopped and alternative anticoagulation started
    - Superior to 4Ts score for less experienced clinicians and ICU patients
    
    Reference: Cuker A, et al. J Thromb Haemost. 2010;8(12):2642-50.
    """
    
    result: int = Field(
        ...,
        description="HEP score for pre-test probability of HIT (range: -7 to +15 points)",
        example=6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with management recommendations based on probability category",
        example="High probability of HIT. At cutoff of 5, the HEP score has 86% sensitivity and 88% specificity. Consider immediate cessation of heparin and initiation of alternative anticoagulation while awaiting confirmatory testing."
    )
    
    stage: str = Field(
        ...,
        description="Probability category (Low Probability, Intermediate Probability, or High Probability)",
        example="High Probability"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the score range for the probability category",
        example="Score ≥5"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": "High probability of HIT. At cutoff of 5, the HEP score has 86% sensitivity and 88% specificity. Consider immediate cessation of heparin and initiation of alternative anticoagulation while awaiting confirmatory testing.",
                "stage": "High Probability",
                "stage_description": "Score ≥5"
            }
        }