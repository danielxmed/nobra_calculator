"""
Disease Steps for Multiple Sclerosis Models

Request and response models for Disease Steps for Multiple Sclerosis calculation.

References (Vancouver style):
1. Hohol MJ, Orav EJ, Weiner HL. Disease steps in multiple sclerosis: a simple approach 
   to evaluate disease progression. Neurology. 1995 Feb;45(2):251-5. 
   doi: 10.1212/wnl.45.2.251.
2. Learmonth YC, Motl RW, Sandroff BM, Pula JH, Cadavid D. Validation of patient 
   determined disease steps (PDDS) scale scores in persons with multiple sclerosis. 
   BMC Neurol. 2013 Apr 25;13:37. doi: 10.1186/1471-2377-13-37.
3. Hohol MJ, Orav EJ, Weiner HL. Disease steps in multiple sclerosis: a longitudinal 
   study comparing disease steps and EDSS to evaluate disease progression. Mult Scler. 
   1999 Oct;5(5):349-54. doi: 10.1177/135245859900500508.

The Disease Steps for Multiple Sclerosis is a simple and reproducible measure of 
different functional steps of MS progression based on ambulatory ability. It was 
developed as an alternative to the Expanded Disability Status Scale (EDSS) to provide 
better inter-rater reliability and more uniform patient distribution across disability 
levels. The scale ranges from 0 (normal) to 6 (wheelchair dependent) with an additional 
'U' category for unclassifiable patients. It focuses specifically on mobility and 
walking ability, making it particularly useful for tracking disease progression and 
guiding therapeutic decisions in multiple sclerosis patients.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, Union


class DiseaseStepsMsRequest(BaseModel):
    """
    Request model for Disease Steps for Multiple Sclerosis
    
    The Disease Steps scale assesses MS disease progression based on ambulatory ability:
    
    Disease Step Categories:
    - normal: Normal neurologic function, no activity limitations
    - mild_disability: Mild symptoms or signs, minimal functional impact
    - moderate_disability: Visibly abnormal gait, noticeable walking difficulties
    - early_cane: Intermittent use of unilateral support (cane occasionally)
    - late_cane: Continuous dependence on unilateral support (cane always)
    - bilateral_support: Requires two canes, crutches, or walker for ambulation
    - wheelchair: Confined to wheelchair, severely limited mobility
    - unclassifiable: Does not fit into standard categories
    
    Assessment Guidelines:
    - Focus on patient's typical ambulatory ability over past month
    - Consider the patient's usual function, not temporary fluctuations
    - Assess ability without assistive devices first, then with devices as needed
    - Consider both indoor and outdoor mobility when determining category
    - Factor in fatigue and other MS-related symptoms affecting mobility

    References (Vancouver style):
    1. Hohol MJ, Orav EJ, Weiner HL. Disease steps in multiple sclerosis: a simple approach 
       to evaluate disease progression. Neurology. 1995 Feb;45(2):251-5. 
       doi: 10.1212/wnl.45.2.251.
    2. Learmonth YC, Motl RW, Sandroff BM, Pula JH, Cadavid D. Validation of patient 
       determined disease steps (PDDS) scale scores in persons with multiple sclerosis. 
       BMC Neurol. 2013 Apr 25;13:37. doi: 10.1186/1471-2377-13-37.
    """
    
    disease_step: Literal[
        "normal", 
        "mild_disability", 
        "moderate_disability", 
        "early_cane", 
        "late_cane", 
        "bilateral_support", 
        "wheelchair", 
        "unclassifiable"
    ] = Field(
        ...,
        description="Patient's current disease step based on ambulatory ability assessment over the past month",
        example="moderate_disability"
    )
    
    @field_validator('disease_step')
    def validate_disease_step(cls, v):
        valid_steps = [
            "normal", "mild_disability", "moderate_disability", "early_cane", 
            "late_cane", "bilateral_support", "wheelchair", "unclassifiable"
        ]
        if v not in valid_steps:
            raise ValueError(f"disease_step must be one of: {valid_steps}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "disease_step": "moderate_disability"
            }
        }


class DiseaseStepsMsResponse(BaseModel):
    """
    Response model for Disease Steps for Multiple Sclerosis
    
    The Disease Steps scale provides scores from 0-6 (plus U for unclassifiable):
    - 0: Normal - No functional limitations
    - 1: Mild disability - Minor symptoms, normal function maintained
    - 2: Moderate disability - Visible gait abnormality, ambulatory without aid
    - 3: Early cane - Intermittent unilateral support needed
    - 4: Late cane - Continuous unilateral support required
    - 5: Bilateral support - Two canes/crutches/walker needed
    - 6: Wheelchair - Confined to wheelchair, limited mobility
    - U: Unclassifiable - Does not fit standard categories
    
    Clinical significance:
    - Simpler and more reliable than EDSS (inter-rater reliability: κ=0.8 vs κ=0.54)
    - Better patient distribution across disability levels
    - Useful for tracking progression and treatment response
    - Can guide therapeutic decision-making
    - Available as Patient-Determined Disease Steps (PDDS) for self-assessment
    
    Reference: Hohol MJ, et al. Neurology. 1995;45(2):251-5.
    """
    
    result: Union[int, str] = Field(
        ...,
        description="Disease Steps score (0-6) or 'U' for unclassifiable",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="step"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the disease step with functional assessment",
        example="Moderate disability with visibly abnormal gait. Patient has noticeable walking difficulties but remains ambulatory without assistance."
    )
    
    stage: str = Field(
        ...,
        description="Disease step category name",
        example="Moderate disability"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the disease step category",
        example="Visible abnormality of gait"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 2,
                "unit": "step",
                "interpretation": "Moderate disability with visibly abnormal gait. Patient has noticeable walking difficulties but remains ambulatory without assistance.",
                "stage": "Moderate disability",
                "stage_description": "Visible abnormality of gait"
            }
        }