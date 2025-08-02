"""
Infant Scalp Score Models

Request and response models for Infant Scalp Score calculation.

References (Vancouver style):
1. Schutzman SA, Nigrovic LE, Mannix R, et al. The Infant Scalp Score: A Validated 
   Tool to Stratify Risk of Traumatic Brain Injury in Infants With Isolated Scalp 
   Hematoma. Acad Emerg Med. 2021;28(1):16-24. doi: 10.1111/acem.14087.
2. Kuppermann N, Holmes JF, Dayan PS, et al. Identification of children at very low 
   risk of clinically-important brain injuries after head trauma: a prospective 
   cohort study. Lancet. 2009;374(9696):1160-1170. doi: 10.1016/S0140-6736(09)61558-0.
3. Greenberg JK, Jeffe DB, Carpenter CR, et al. North American Survey of the Management 
   of Minor Head Injury in Children. J Trauma Acute Care Surg. 2018;84(4):613-619.

The Infant Scalp Score (ISS) is a validated clinical tool specifically designed for 
infants ≤12 months old who present with isolated scalp hematoma after head trauma 
but are otherwise asymptomatic. The score stratifies risk for clinically important 
traumatic brain injury (ciTBI) or TBI on computed tomography (CT) to help guide 
clinical decision-making. This tool is particularly valuable in the pediatric emergency 
setting where infants are difficult to assess clinically and are most sensitive to 
ionizing radiation effects.
"""

from pydantic import BaseModel, Field
from typing import Literal


class InfantScalpScoreRequest(BaseModel):
    """
    Request model for Infant Scalp Score calculation
    
    Assesses risk of traumatic brain injury in infants ≤12 months with isolated 
    scalp hematoma after head trauma. The score uses three key clinical variables:
    
    Patient Age Categories (younger = higher risk):
    - >12 months: 0 points (though score is validated for ≤12 months)
    - 6-11 months: 1 point
    - 3-5 months: 2 points
    - 0-2 months: 3 points
    
    Hematoma Size Categories (larger = higher risk):
    - None: 0 points
    - Small (barely palpable): 1 point
    - Medium (easily palpable): 2 points
    - Large (boggy consistency): 3 points
    
    Hematoma Location Categories (non-frontal = higher risk):
    - Frontal: 0 points
    - Occipital: 1 point
    - Temporal/Parietal: 2 points (highest risk location)
    
    Risk Stratification:
    - Score 0-3: Low risk of TBI
    - Score 4-8: High risk of TBI (consider CT imaging)
    
    Important Limitations:
    - Only for asymptomatic infants (no LOC, seizures, mental status changes)
    - Not for suspected non-accidental trauma
    - Must have isolated scalp hematoma
    
    References (Vancouver style):
    1. Schutzman SA, Nigrovic LE, Mannix R, et al. The Infant Scalp Score: A Validated 
       Tool to Stratify Risk of Traumatic Brain Injury in Infants With Isolated Scalp 
       Hematoma. Acad Emerg Med. 2021;28(1):16-24. doi: 10.1111/acem.14087.
    2. Kuppermann N, Holmes JF, Dayan PS, et al. Identification of children at very low 
       risk of clinically-important brain injuries after head trauma: a prospective 
       cohort study. Lancet. 2009;374(9696):1160-1170.
    """
    
    patient_age_months: Literal["over_12_months", "6_to_11_months", "3_to_5_months", "0_to_2_months"] = Field(
        ...,
        description="Patient age in months. Younger infants have higher risk for traumatic brain injury due to anatomical and physiological factors. Scores: >12 months (0), 6-11 months (1), 3-5 months (2), 0-2 months (3)",
        example="6_to_11_months"
    )
    
    hematoma_size: Literal["none", "small_barely_palpable", "medium_easily_palpable", "large_boggy_consistency"] = Field(
        ...,
        description="Size and consistency of scalp hematoma. Larger hematomas indicate greater force of impact and increased risk of underlying brain injury. Scores: None (0), Small/barely palpable (1), Medium/easily palpable (2), Large/boggy consistency (3)",
        example="medium_easily_palpable"
    )
    
    hematoma_location: Literal["frontal", "occipital", "temporal_parietal"] = Field(
        ...,
        description="Anatomical location of scalp hematoma. Non-frontal locations, particularly temporal/parietal, carry higher risk for underlying TBI. Scores: Frontal (0), Occipital (1), Temporal/Parietal (2)",
        example="temporal_parietal"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "patient_age_months": "6_to_11_months",
                "hematoma_size": "medium_easily_palpable",
                "hematoma_location": "temporal_parietal"
            }
        }


class InfantScalpScoreResponse(BaseModel):
    """
    Response model for Infant Scalp Score calculation
    
    Returns the Infant Scalp Score with risk stratification and clinical management 
    recommendations for infants with isolated scalp hematoma after head trauma.
    
    Risk Categories:
    - Low Risk (0-3 points): Clinical observation may be appropriate
    - High Risk (4-8 points): Strong consideration for cranial CT imaging
    
    The ISS provides validated risk stratification that helps clinicians make 
    evidence-based decisions about neuroimaging in infants with isolated scalp 
    hematomas. The tool is particularly valuable for avoiding unnecessary radiation 
    exposure in low-risk infants while ensuring appropriate imaging for those at 
    higher risk of clinically important traumatic brain injury.
    
    Reference: Schutzman SA, et al. Acad Emerg Med. 2021;28(1):16-24.
    """
    
    result: int = Field(
        ...,
        description="Infant Scalp Score calculated from age, hematoma size, and location (range 0-8 points)",
        example=5,
        ge=0,
        le=8
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on the risk score",
        example="High risk of traumatic brain injury. Strong consideration for cranial CT imaging to evaluate for clinically important traumatic brain injury or TBI."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category with score range",
        example="Score 5 points (4-8 points)"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5,
                "unit": "points",
                "interpretation": "High risk of traumatic brain injury. Strong consideration for cranial CT imaging to evaluate for clinically important traumatic brain injury or TBI.",
                "stage": "High Risk",
                "stage_description": "Score 5 points (4-8 points)"
            }
        }