"""
Ankylosing Spondylitis Disease Activity Score with ESR (ASDAS-ESR) Models

Request and response models for ASDAS-ESR calculation.

References (Vancouver style):
1. Lukas C, Landewé R, Sieper J, Dougados M, Davis J, Braun J, van der Linden S, 
   van der Heijde D. Development of an ASAS-endorsed disease activity score (ASDAS) 
   in patients with ankylosing spondylitis. Ann Rheum Dis. 2009 Jan;68(1):18-24. 
   doi: 10.1136/ard.2008.094870.
2. van der Heijde D, Lie E, Kvien TK, Sieper J, van den Bosch F, Listing J, Braun J, 
   Landewé R. ASDAS, a highly discriminatory ASAS-endorsed disease activity score in 
   patients with ankylosing spondylitis. Ann Rheum Dis. 2009 Dec;68(12):1811-8. 
   doi: 10.1136/ard.2008.100826.
3. Machado P, Landewé R, Lie E, Kvien TK, Braun J, Baker D, van der Heijde D. 
   Ankylosing Spondylitis Disease Activity Score (ASDAS): defining cut-off values 
   for disease activity states and improvement scores. Ann Rheum Dis. 2011 Jan;70(1):47-53. 
   doi: 10.1136/ard.2010.138594.

The ASDAS-ESR is a composite index to assess disease activity in axial spondyloarthritis 
(including ankylosing spondylitis). It combines patient-reported outcomes with laboratory 
measures (ESR) to provide a comprehensive evaluation of disease activity. The score uses 
four patient-reported parameters (each scored 0-10) plus the ESR value to calculate a 
composite score that stratifies patients into disease activity categories.
"""

from pydantic import BaseModel, Field


class AsdasEsrRequest(BaseModel):
    """
    Request model for Ankylosing Spondylitis Disease Activity Score with ESR (ASDAS-ESR)
    
    The ASDAS-ESR uses 5 variables to assess axial spondyloarthritis disease activity:
    
    Patient-Reported Outcomes (0-10 scale):
    - Back Pain: Overall level of AS neck, back, or hip pain
    - Morning Stiffness: Overall level of morning stiffness from time of waking
    - Patient Global: How active was spondylitis on average during the last week
    - Peripheral Pain: Overall level of pain/swelling in joints other than neck, back, or hips
    
    Laboratory Parameter:
    - ESR: Erythrocyte Sedimentation Rate in mm/hr
    
    Formula: ASDAS-ESR = 0.08 × Back Pain + 0.07 × Morning Stiffness + 0.11 × Patient Global + 
             0.09 × Peripheral Pain + 0.29 × √(ESR)
    
    Disease Activity Categories:
    - <1.3: Inactive disease
    - 1.3-2.1: Moderate disease activity
    - 2.1-3.5: High disease activity
    - >3.5: Very high disease activity
    
    References (Vancouver style):
    1. Lukas C, Landewé R, Sieper J, Dougados M, Davis J, Braun J, van der Linden S, 
    van der Heijde D. Development of an ASAS-endorsed disease activity score (ASDAS) 
    in patients with ankylosing spondylitis. Ann Rheum Dis. 2009 Jan;68(1):18-24. 
    doi: 10.1136/ard.2008.094870.
    2. van der Heijde D, Lie E, Kvien TK, Sieper J, van den Bosch F, Listing J, Braun J, 
    Landewé R. ASDAS, a highly discriminatory ASAS-endorsed disease activity score in 
    patients with ankylosing spondylitis. Ann Rheum Dis. 2009 Dec;68(12):1811-8. 
    doi: 10.1136/ard.2008.100826.
    3. Machado P, Landewé R, Lie E, Kvien TK, Braun J, Baker D, van der Heijde D. 
    Ankylosing Spondylitis Disease Activity Score (ASDAS): defining cut-off values 
    for disease activity states and improvement scores. Ann Rheum Dis. 2011 Jan;70(1):47-53. 
    doi: 10.1136/ard.2010.138594.
    """
    
    back_pain: int = Field(
        ...,
        description="Overall level of AS neck, back, or hip pain. Ask patient: 'How would you describe the overall level of AS neck, back, or hip pain you have had?' Scale: 0 (least severe) to 10 (most severe)",
        ge=0,
        le=10,
        example=3
    )
    
    morning_stiffness: int = Field(
        ...,
        description="Overall level of morning stiffness from time of waking. Ask patient: 'How would you describe the overall level of morning stiffness you have had from the time you wake up?' Scale: 0 (least severe) to 10 (most severe)",
        ge=0,
        le=10,
        example=4
    )
    
    patient_global: int = Field(
        ...,
        description="Patient global assessment of disease activity. Ask patient: 'How active was your spondylitis, on average, during the last week?' Scale: 0 (least severe) to 10 (most severe)",
        ge=0,
        le=10,
        example=5
    )
    
    peripheral_pain: int = Field(
        ...,
        description="Overall level of peripheral pain/swelling. Ask patient: 'How would you describe the overall level of pain/swelling in joints other than neck, back, or hips you have had?' Scale: 0 (least severe) to 10 (most severe)",
        ge=0,
        le=10,
        example=2
    )
    
    esr: int = Field(
        ...,
        description="Erythrocyte Sedimentation Rate measured by standard laboratory methods. Normal ranges vary by age and sex (typically <20 mm/hr for men <50 years, <30 mm/hr for men >50 years, <30 mm/hr for women <50 years, <40 mm/hr for women >50 years)",
        ge=0,
        le=200,
        example=25
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "back_pain": 3,
                "morning_stiffness": 4,
                "patient_global": 5,
                "peripheral_pain": 2,
                "esr": 25
            }
        }


class AsdasEsrResponse(BaseModel):
    """
    Response model for Ankylosing Spondylitis Disease Activity Score with ESR (ASDAS-ESR)
    
    The ASDAS-ESR score ranges typically from 0 to ~6 points and classifies patients into:
    - Inactive (<1.3 points): Minimal disease activity, continue current management
    - Moderate (1.3-2.1 points): Consider therapy optimization or biologics
    - High (2.1-3.5 points): Strongly consider biological therapy
    - Very High (>3.5 points): Urgent consideration for biological therapy or switching
    
    Improvement thresholds:
    - ≥1.1 units: Clinically important improvement
    - ≥2.0 units: Major improvement
    
    Reference: Lukas C, et al. Ann Rheum Dis. 2009;68(1):18-24.
    """
    
    result: float = Field(
        ...,
        description="ASDAS-ESR score calculated from clinical and laboratory parameters (range typically 0-6 points)",
        example=2.45
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on the score",
        example="Disease activity is high. Strongly consider biological therapy if not already initiated. Increase monitoring frequency and assess treatment response regularly."
    )
    
    stage: str = Field(
        ...,
        description="Disease activity category (Inactive, Moderate, High, Very High)",
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
                "result": 2.45,
                "unit": "points",
                "interpretation": "Disease activity is high. Strongly consider biological therapy if not already initiated. Increase monitoring frequency and assess treatment response regularly.",
                "stage": "High",
                "stage_description": "High disease activity"
            }
        }