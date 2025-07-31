"""
Neuropathic Pain Scale (NPS) Models

Request and response models for Neuropathic Pain Scale calculation.

Reference (Vancouver style):
Galer BS, Jensen MP. Development and preliminary validation of a pain measure specific 
to neuropathic pain: the Neuropathic Pain Scale. Neurology. 1997 Feb;48(2):332-8. 
doi: 10.1212/wnl.48.2.332.

The Neuropathic Pain Scale (NPS) is designed to assess distinct pain qualities associated 
with neuropathic pain. It is only for use in patients who have already been diagnosed 
with neuropathic pain and is useful for tracking pain severity over time and monitoring 
response to treatment.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class NeuropathicPainScaleRequest(BaseModel):
    """
    Request model for Neuropathic Pain Scale (NPS)
    
    The NPS assesses 10 specific pain qualities on a 0-10 scale. Each pain quality 
    captures a distinct aspect of neuropathic pain experience. The scale was developed 
    specifically for monitoring treatment response in patients with established 
    neuropathic pain.
    
    Pain Quality Domains:
    1. Overall pain intensity
    2. Sharp pain ('Like a knife')
    3. Hot/burning pain ('On fire')
    4. Dull/aching pain
    5. Cold/freezing pain ('Freezing')
    6. Skin sensitivity to light touch ('Raw skin')
    7. Itchy pain
    8. Overall unpleasantness ('Intolerable')
    9. Deep pain intensity
    10. Surface pain intensity
    
    Reference (Vancouver style):
    Galer BS, Jensen MP. Development and preliminary validation of a pain measure specific 
    to neuropathic pain: the Neuropathic Pain Scale. Neurology. 1997 Feb;48(2):332-8. 
    doi: 10.1212/wnl.48.2.332.
    """
    
    intensity: int = Field(
        ...,
        ge=0,
        le=10,
        description="How intense is the pain? Rate from 0 (no pain) to 10 (most pain imaginable)",
        example=6
    )
    
    sharp: int = Field(
        ...,
        ge=0,
        le=10,
        description="How sharp is the pain? ('Like a knife'). Rate from 0 (not sharp) to 10 (extremely sharp)",
        example=5
    )
    
    hot: int = Field(
        ...,
        ge=0,
        le=10,
        description="How hot is the pain? ('On fire'). Rate from 0 (not hot) to 10 (extremely hot)",
        example=4
    )
    
    dull: int = Field(
        ...,
        ge=0,
        le=10,
        description="How dull is the pain? Rate from 0 (not dull) to 10 (extremely dull)",
        example=3
    )
    
    cold: int = Field(
        ...,
        ge=0,
        le=10,
        description="How cold is the pain? ('Freezing'). Rate from 0 (not cold) to 10 (extremely cold)",
        example=2
    )
    
    sensitive: int = Field(
        ...,
        ge=0,
        le=10,
        description="How sensitive is the skin to light touch? ('Raw skin'). Rate from 0 (not sensitive) to 10 (extremely sensitive)",
        example=7
    )
    
    itchy: int = Field(
        ...,
        ge=0,
        le=10,
        description="How itchy is the pain? Rate from 0 (not itchy) to 10 (extremely itchy)",
        example=1
    )
    
    unpleasant: int = Field(
        ...,
        ge=0,
        le=10,
        description="How unpleasant is the pain? ('Intolerable'). Rate from 0 (not unpleasant) to 10 (intolerable)",
        example=7
    )
    
    deep_pain: int = Field(
        ...,
        ge=0,
        le=10,
        description="If the pain is deep, how intense is the deep pain? Rate from 0 (no deep pain) to 10 (most intense deep pain imaginable)",
        example=5
    )
    
    surface_pain: int = Field(
        ...,
        ge=0,
        le=10,
        description="If the pain is on the surface, how intense is the surface pain? Rate from 0 (no surface pain) to 10 (most intense surface pain imaginable)",
        example=6
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "intensity": 6,
                "sharp": 5,
                "hot": 4,
                "dull": 3,
                "cold": 2,
                "sensitive": 7,
                "itchy": 1,
                "unpleasant": 7,
                "deep_pain": 5,
                "surface_pain": 6
            }
        }


class NeuropathicPainScaleResponse(BaseModel):
    """
    Response model for Neuropathic Pain Scale (NPS)
    
    The total NPS score ranges from 0 to 100 points:
    - 10 pain qualities × 10 points each = 100 points
    
    Higher scores indicate worse neuropathic pain. The scale is useful for:
    - Tracking pain severity over time
    - Monitoring response to treatment
    - Comparing pain levels between visits
    - Assessing effectiveness of interventions
    
    Reference: Galer BS, Jensen MP. Neurology. 1997;48(2):332-8.
    """
    
    result: int = Field(
        ...,
        description="Total NPS score (0-100 points). Sum of all 10 pain quality scores",
        example=45
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the NPS score with treatment recommendations",
        example="NPS score of 45 indicates severe neuropathic pain symptoms. Comprehensive pain management strategy recommended. Consider referral to pain specialist or neurologist for optimization of treatment. Combination therapies and adjuvant medications may be necessary."
    )
    
    stage: str = Field(
        ...,
        description="Pain severity category (Mild, Moderate, Severe, or Very Severe)",
        example="Severe"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the pain severity level",
        example="Severe neuropathic pain"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 45,
                "unit": "points",
                "interpretation": "NPS score of 45 indicates severe neuropathic pain symptoms. Comprehensive pain management strategy recommended. Consider referral to pain specialist or neurologist for optimization of treatment. Combination therapies and adjuvant medications may be necessary.",
                "stage": "Severe",
                "stage_description": "Severe neuropathic pain"
            }
        }