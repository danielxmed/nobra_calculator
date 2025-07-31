"""
Bacterial Meningitis Score for Children Models

Request and response models for the Bacterial Meningitis Score calculation.

References (Vancouver style):
1. Nigrovic LE, Kuppermann N, Macias CG, Cannavino CR, Moro-Sutherland DM, Schremmer RD, 
   et al. Clinical prediction rule for identifying children with cerebrospinal fluid 
   pleocytosis at very low risk of bacterial meningitis. JAMA. 2007 Jan 3;297(1):52-60. 
   doi: 10.1001/jama.297.1.52.
2. Nigrovic LE, Malley R, Macias CG, Kanegaye JT, Moro-Sutherland DM, Schremmer RD, et al. 
   Effect of antibiotic pretreatment on cerebrospinal fluid profiles of children with 
   bacterial meningitis. Pediatrics. 2008 Oct;122(4):726-30. doi: 10.1542/peds.2007-3275.
3. Nigrovic LE, Malley R, Kuppermann N. Meta-analysis of bacterial meningitis score 
   validation studies. Arch Dis Child. 2012 Sep;97(9):799-805. 
   doi: 10.1136/archdischild-2012-301798.

The Bacterial Meningitis Score for Children is a clinical decision tool that predicts the 
likelihood of bacterial (versus aseptic) meningitis in children with CSF pleocytosis. The 
score helps clinicians distinguish between bacterial and aseptic meningitis to support safe 
discharge decisions while maintaining appropriate caution for this serious condition.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class BacterialMeningitisScoreRequest(BaseModel):
    """
    Request model for Bacterial Meningitis Score for Children
    
    The score uses five clinical and laboratory parameters to assess the risk of bacterial 
    meningitis in children with CSF pleocytosis:
    
    1. CSF Gram stain result (positive = 1 point)
    2. CSF absolute neutrophil count ≥1,000 cells/µL (1 point)
    3. CSF protein ≥80 mg/dL (1 point)
    4. Peripheral blood absolute neutrophil count ≥10,000 cells/µL (1 point)
    5. Seizure at or prior to initial presentation (1 point)
    
    Score interpretation:
    - 0 points: Very low risk of bacterial meningitis (~0.1% risk)
    - ≥1 point: Not very low risk, requires admission and parenteral antibiotics
    
    Important limitations:
    - Not recommended for patients <2 months old
    - Not effective for ruling out all nervous system infections (e.g., Lyme meningitis)
    - Clinical judgment should always supersede the score
    - Particular caution with infants with petechial rashes
    
    References (Vancouver style):
    1. Nigrovic LE, Kuppermann N, Macias CG, Cannavino CR, Moro-Sutherland DM, Schremmer RD, 
       et al. Clinical prediction rule for identifying children with cerebrospinal fluid 
       pleocytosis at very low risk of bacterial meningitis. JAMA. 2007 Jan 3;297(1):52-60. 
       doi: 10.1001/jama.297.1.52.
    """
    
    csf_gram_stain: Literal["negative", "positive"] = Field(
        ...,
        description="Cerebrospinal fluid (CSF) Gram stain result. Positive result scores 1 point",
        example="negative"
    )
    
    csf_anc: int = Field(
        ...,
        ge=0,
        le=50000,
        description="CSF absolute neutrophil count in cells/µL. Values ≥1,000 cells/µL score 1 point",
        example=500
    )
    
    csf_protein: float = Field(
        ...,
        ge=0,
        le=1000,
        description="CSF protein level in mg/dL. Values ≥80 mg/dL score 1 point",
        example=45.5
    )
    
    peripheral_blood_anc: int = Field(
        ...,
        ge=0,
        le=100000,
        description="Peripheral blood absolute neutrophil count in cells/µL. Values ≥10,000 cells/µL score 1 point",
        example=8500
    )
    
    seizure_at_presentation: Literal["no", "yes"] = Field(
        ...,
        description="Seizure at or prior to initial presentation. Presence scores 1 point",
        example="no"
    )
    
    @field_validator('csf_anc')
    def validate_csf_anc(cls, v):
        if v > 50000:
            raise ValueError("CSF ANC value seems unusually high (>50,000 cells/µL). Please verify.")
        return v
    
    @field_validator('csf_protein')
    def validate_csf_protein(cls, v):
        if v > 1000:
            raise ValueError("CSF protein value seems unusually high (>1000 mg/dL). Please verify.")
        return v
    
    @field_validator('peripheral_blood_anc')
    def validate_peripheral_anc(cls, v):
        if v > 100000:
            raise ValueError("Peripheral blood ANC value seems unusually high (>100,000 cells/µL). Please verify.")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "csf_gram_stain": "negative",
                "csf_anc": 500,
                "csf_protein": 45.5,
                "peripheral_blood_anc": 8500,
                "seizure_at_presentation": "no"
            }
        }


class BacterialMeningitisScoreResponse(BaseModel):
    """
    Response model for Bacterial Meningitis Score for Children
    
    The score ranges from 0 to 5 points and classifies patients into two risk categories:
    - 0 points: Very low risk of bacterial meningitis
    - ≥1 point: Not very low risk of bacterial meningitis
    
    Clinical application:
    - Score of 0: Consider discharge with close follow-up, possible single dose of 
      parenteral antibiotics while awaiting cultures
    - Score ≥1: Admission for parenteral antibiotics and monitoring recommended
    
    Reference: Nigrovic LE, et al. JAMA. 2007;297(1):52-60.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=5,
        description="Bacterial Meningitis Score (range: 0-5 points)",
        example=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on the score",
        example="Score of 0 indicates very low risk of bacterial meningitis (risk approximately 0.1%). Consider discharge with close follow-up. Clinical judgment should always supersede the score. Consider single dose of parenteral antibiotics (e.g., ceftriaxone) prior to discharge while awaiting bacterial cultures."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Very Low Risk or Not Very Low Risk)",
        example="Very Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Very low risk of bacterial meningitis"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "Score of 0 indicates very low risk of bacterial meningitis (risk approximately 0.1%). Consider discharge with close follow-up. Clinical judgment should always supersede the score. Consider single dose of parenteral antibiotics (e.g., ceftriaxone) prior to discharge while awaiting bacterial cultures.",
                "stage": "Very Low Risk",
                "stage_description": "Very low risk of bacterial meningitis"
            }
        }