"""
Disease Activity Score-28 for Rheumatoid Arthritis with ESR (DAS28-ESR) Models

Request and response models for DAS28-ESR calculation.

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
3. Tamhane A, Redden DT, McGwin G Jr, Brown EE, Westfall AO, Reynolds RJ, et al. 
   Comparison of the disease activity score using erythrocyte sedimentation rate 
   and C-reactive protein in African Americans with rheumatoid arthritis. J Rheumatol. 
   2013 Nov;40(11):1812-22. doi: 10.3899/jrheum.121225.

The DAS28-ESR is a composite measure used to assess disease activity in rheumatoid 
arthritis patients. It evaluates 28 joints for tenderness and swelling, incorporates 
the patient's global assessment of disease activity, and uses erythrocyte sedimentation 
rate (ESR) as the inflammatory marker. The score ranges from 0-10, with higher scores 
indicating greater disease activity. Cut-offs define remission (<2.6), low (2.6-3.2), 
moderate (3.2-5.1), and high (>5.1) disease activity states, supporting treat-to-target 
strategies in RA management.
"""

from pydantic import BaseModel, Field, field_validator


class Das28EsrRequest(BaseModel):
    """
    Request model for Disease Activity Score-28 for Rheumatoid Arthritis with ESR
    
    The DAS28-ESR assesses rheumatoid arthritis disease activity using 4 components:
    
    1. Tender Joint Count (TJC28): Number of tender joints out of 28 assessed joints
       - 28 joints include: shoulders (2), elbows (2), wrists (2), knees (2)
       - Hand joints: MCPs (10), PIPs (8), thumb IPs (2)
       - Range: 0-28 joints
    
    2. Swollen Joint Count (SJC28): Number of swollen joints out of 28 assessed joints
       - Same 28 joints as tender joint assessment
       - Range: 0-28 joints
    
    3. Erythrocyte Sedimentation Rate (ESR): Inflammatory marker in mm/hr
       - Normal ranges: Men <50y: <15 mm/hr, >50y: <20 mm/hr; Women <50y: <20 mm/hr, >50y: <30 mm/hr
       - Range: 1-200 mm/hr (minimum 1 for logarithm calculation)
    
    4. Patient Global Health Assessment: Patient's overall assessment of disease activity
       - Scale: 0-10 (0 = very well, 10 = very poor)
       - Visual analog scale or numeric rating scale
    
    Formula: DAS28-ESR = 0.56*√(TJC28) + 0.28*√(SJC28) + 0.70*ln(ESR) + 0.014*GH*10

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
        example=6
    )
    
    swollen_joint_count: int = Field(
        ...,
        description="Number of swollen joints out of 28 assessed joints (same joints as tender joint assessment)",
        ge=0,
        le=28,
        example=4
    )
    
    esr_level: int = Field(
        ...,
        description="Erythrocyte sedimentation rate in mm/hr (normal: men <50y: <15, >50y: <20; women <50y: <20, >50y: <30)",
        ge=1,
        le=200,
        example=45
    )
    
    patient_global_health: int = Field(
        ...,
        description="Patient's global assessment of disease activity on 0-10 scale (0 = very well, 10 = very poor)",
        ge=0,
        le=10,
        example=7
    )
    
    @field_validator('tender_joint_count', 'swollen_joint_count')
    def validate_joint_counts(cls, v):
        if not isinstance(v, int):
            raise ValueError("Joint counts must be integers")
        if v < 0 or v > 28:
            raise ValueError("Joint counts must be between 0 and 28")
        return v
    
    @field_validator('esr_level')
    def validate_esr_level(cls, v):
        if not isinstance(v, int):
            raise ValueError("ESR level must be an integer")
        if v < 1 or v > 200:
            raise ValueError("ESR level must be between 1 and 200 mm/hr")
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
                "tender_joint_count": 6,
                "swollen_joint_count": 4,
                "esr_level": 45,
                "patient_global_health": 7
            }
        }


class Das28EsrResponse(BaseModel):
    """
    Response model for Disease Activity Score-28 for Rheumatoid Arthritis with ESR
    
    The DAS28-ESR score ranges from 0-10 and classifies disease activity into:
    - Remission (<2.6): Minimal or no disease activity
    - Low (2.6-3.2): Low disease activity, effective therapy
    - Moderate (3.2-5.1): Moderate disease activity, consider treatment modification
    - High (>5.1): High disease activity, treatment intensification recommended
    
    Clinical significance:
    - Change ≥0.6: Moderate improvement
    - Change ≥1.2: Major improvement
    - Target: Remission (DAS28-ESR <2.6) or low disease activity
    
    Note: DAS28-ESR tends to give higher scores than DAS28-CRP for the same disease activity.
    ESR may be elevated by factors other than RA (age, gender, anemia, infection).
    
    Reference: van der Heijde DM, et al. Ann Rheum Dis. 1990;49(11):916-20.
    """
    
    result: float = Field(
        ...,
        description="DAS28-ESR score calculated from clinical and laboratory parameters (range: 0-10)",
        example=5.8
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and treatment recommendations based on disease activity level",
        example="High disease activity. Treatment intensification or change is strongly recommended. Consider combination therapy or biologic agents."
    )
    
    stage: str = Field(
        ...,
        description="Disease activity category (Remission, Low, Moderate, High)",
        example="High"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the disease activity category",
        example="High disease activity"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 5.8,
                "unit": "points",
                "interpretation": "High disease activity. Treatment intensification or change is strongly recommended. Consider combination therapy or biologic agents.",
                "stage": "High",
                "stage_description": "High disease activity"
            }
        }