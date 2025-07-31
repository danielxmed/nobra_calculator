"""
Disease Activity Score-28 for Rheumatoid Arthritis with CRP (DAS28-CRP) Models

Request and response models for DAS28-CRP calculation.

References (Vancouver style):
1. van der Heijde DM, van 't Hof MA, van Riel PL, Theunisse LA, Lubberts EW, 
   van Leeuwen MA, et al. Judging disease activity in clinical practice in 
   rheumatoid arthritis: first step in the development of a disease activity score. 
   Ann Rheum Dis. 1990 Nov;49(11):916-20. doi: 10.1136/ard.49.11.916.
2. Prevoo ML, van 't Hof MA, Kuper HH, van Leeuwen MA, van de Putte LB, van Riel PL. 
   Modified disease activity scores that include twenty-eight-joint counts. 
   Development and validation in a prospective longitudinal study of patients with 
   rheumatoid arthritis. Arthritis Rheum. 1995 Jan;38(1):44-8. 
   doi: 10.1002/art.1780380107.
3. Fleischmann R, van der Heijde D, Koenig AS, Pedersen R, Tsai TF, Derzi M, et al. 
   How much does Disease Activity Score in 28 joints ESR and CRP calculations 
   underestimate disease activity compared to the Simplified Disease Activity Index? 
   Ann Rheum Dis. 2015 Jun;74(6):1132-7. doi: 10.1136/annrheumdis-2013-204920.

The DAS28-CRP is a composite measure used to assess disease activity in rheumatoid 
arthritis patients. It evaluates 28 joints for tenderness and swelling, incorporates 
the patient's global assessment of disease activity, and uses C-reactive protein (CRP) 
as the inflammatory marker. The score ranges from 0-10, with higher scores indicating 
greater disease activity. Cut-offs define remission (<2.6), low (2.6-3.2), moderate 
(3.2-5.1), and high (>5.1) disease activity states, supporting treat-to-target 
strategies in RA management.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Union


class Das28CrpRequest(BaseModel):
    """
    Request model for Disease Activity Score-28 for Rheumatoid Arthritis with CRP
    
    The DAS28-CRP assesses rheumatoid arthritis disease activity using 4 components:
    
    1. Tender Joint Count (TJC28): Number of tender joints out of 28 assessed joints
       - 28 joints include: shoulders (2), elbows (2), wrists (2), knees (2)
       - Hand joints: MCPs (10), PIPs (8), thumb IPs (2)
       - Range: 0-28 joints
    
    2. Swollen Joint Count (SJC28): Number of swollen joints out of 28 assessed joints
       - Same 28 joints as tender joint assessment
       - Range: 0-28 joints
    
    3. C-Reactive Protein (CRP): Inflammatory marker in mg/L
       - Normal range typically <3 mg/L
       - Range: 0-300 mg/L (for calculation purposes)
    
    4. Patient Global Health Assessment: Patient's overall assessment of disease activity
       - Scale: 0-10 (0 = very well, 10 = very poor)
       - Visual analog scale or numeric rating scale
    
    Formula: DAS28-CRP = 0.56*√(TJC28) + 0.28*√(SJC28) + 0.36*ln(CRP+1) + 0.014*GH*10 + 0.96

    References (Vancouver style):
    1. van der Heijde DM, van 't Hof MA, van Riel PL, Theunisse LA, Lubberts EW, 
       van Leeuwen MA, et al. Judging disease activity in clinical practice in 
       rheumatoid arthritis: first step in the development of a disease activity score. 
       Ann Rheum Dis. 1990 Nov;49(11):916-20. doi: 10.1136/ard.49.11.916.
    2. Prevoo ML, van 't Hof MA, Kuper HH, van Leeuwen MA, van de Putte LB, van Riel PL. 
       Modified disease activity scores that include twenty-eight-joint counts. 
       Development and validation in a prospective longitudinal study of patients with 
       rheumatoid arthritis. Arthritis Rheum. 1995 Jan;38(1):44-8.
    """
    
    tender_joint_count: int = Field(
        ...,
        description="Number of tender joints out of 28 assessed joints (shoulders, elbows, wrists, knees, MCPs, PIPs, thumb IPs)",
        ge=0,
        le=28,
        example=4
    )
    
    swollen_joint_count: int = Field(
        ...,
        description="Number of swollen joints out of 28 assessed joints (same joints as tender joint assessment)",
        ge=0,
        le=28,
        example=2
    )
    
    crp_level: Union[int, float] = Field(
        ...,
        description="C-reactive protein level in mg/L (normal <3 mg/L, elevated values indicate inflammation)",
        ge=0,
        le=300,
        example=15.5
    )
    
    patient_global_health: int = Field(
        ...,
        description="Patient's global assessment of disease activity on 0-10 scale (0 = very well, 10 = very poor)",
        ge=0,
        le=10,
        example=6
    )
    
    @field_validator('tender_joint_count', 'swollen_joint_count')
    def validate_joint_counts(cls, v):
        if not isinstance(v, int):
            raise ValueError("Joint counts must be integers")
        if v < 0 or v > 28:
            raise ValueError("Joint counts must be between 0 and 28")
        return v
    
    @field_validator('crp_level')
    def validate_crp_level(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError("CRP level must be a number")
        if v < 0 or v > 300:
            raise ValueError("CRP level must be between 0 and 300 mg/L")
        return v
    
    @field_validator('patient_global_health')
    def validate_global_health(cls, v):
        if not isinstance(v, int):
            raise ValueError("Patient global health must be an integer")
        if v < 0 or v > 10:
            raise ValueError("Patient global health must be between 0 and 10")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "tender_joint_count": 4,
                "swollen_joint_count": 2,
                "crp_level": 15.5,
                "patient_global_health": 6
            }
        }


class Das28CrpResponse(BaseModel):
    """
    Response model for Disease Activity Score-28 for Rheumatoid Arthritis with CRP
    
    The DAS28-CRP score ranges from 0-10 and classifies disease activity into:
    - Remission (<2.6): Minimal or no disease activity
    - Low (2.6-3.2): Low disease activity, effective therapy
    - Moderate (3.2-5.1): Moderate disease activity, consider treatment modification
    - High (>5.1): High disease activity, treatment intensification recommended
    
    Clinical significance:
    - Change ≥0.6: Moderate improvement
    - Change ≥1.2: Major improvement
    - Target: Remission (DAS28-CRP <2.6) or low disease activity
    
    Note: DAS28-CRP tends to give lower scores than DAS28-ESR for the same disease activity.
    
    Reference: van der Heijde DM, et al. Ann Rheum Dis. 1990;49(11):916-20.
    """
    
    result: float = Field(
        ...,
        description="DAS28-CRP score calculated from clinical and laboratory parameters (range: 0-10)",
        example=3.8
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and treatment recommendations based on disease activity level",
        example="Moderate disease activity. Consider treatment intensification or modification. Reassess treatment strategy to achieve lower disease activity."
    )
    
    stage: str = Field(
        ...,
        description="Disease activity category (Remission, Low, Moderate, High)",
        example="Moderate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the disease activity category",
        example="Moderate disease activity"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 3.8,
                "unit": "points",
                "interpretation": "Moderate disease activity. Consider treatment intensification or modification. Reassess treatment strategy to achieve lower disease activity.",
                "stage": "Moderate",
                "stage_description": "Moderate disease activity"
            }
        }