"""
Bacterial Meningitis Score for Children Models

Request and response models for Bacterial Meningitis Score calculation.

References (Vancouver style):
1. Nigrovic LE, Kuppermann N, Macias CG, Cannavino CR, Moro-Sutherland DM, Schremmer RD, et al. 
   Clinical prediction rule for identifying children with cerebrospinal fluid pleocytosis at very low 
   risk of bacterial meningitis. JAMA. 2007 Jan 3;297(1):52-60. doi: 10.1001/jama.297.1.52.
2. Nigrovic LE, Malley R, Kuppermann N. Meta-analysis of bacterial meningitis score validation studies. 
   Arch Dis Child. 2012 Sep;97(9):799-805. doi: 10.1136/archdischild-2012-301798.

The Bacterial Meningitis Score is a clinical prediction rule designed to identify children with CSF 
pleocytosis who are at very low risk for bacterial meningitis, potentially avoiding unnecessary 
hospitalization and antibiotic treatment.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class BacterialMeningitisScoreRequest(BaseModel):
    """
    Request model for Bacterial Meningitis Score for Children
    
    The score uses 5 criteria to predict bacterial meningitis in children with CSF pleocytosis:
    1. Positive CSF Gram stain (1 point if positive)
    2. CSF absolute neutrophil count ≥1,000 cells/µL (1 point if yes)
    3. CSF protein ≥80 mg/dL (1 point if yes)
    4. Peripheral blood ANC ≥10,000 cells/µL (1 point if yes)
    5. Seizure at or prior to initial presentation (1 point if yes)
    
    A score of 0 indicates "Very Low Risk" while scores ≥1 indicate "Not Very Low Risk" for bacterial meningitis.
    
    References:
    1. Nigrovic LE, et al. JAMA. 2007;297(1):52-60.
    2. Nigrovic LE, et al. Arch Dis Child. 2012;97(9):799-805.
    """
    
    csf_gram_stain: Literal["negative", "positive"] = Field(
        ...,
        description="Cerebrospinal fluid (CSF) Gram stain result. Positive Gram stain scores 1 point",
        example="negative"
    )
    
    csf_anc: int = Field(
        ...,
        description="CSF absolute neutrophil count in cells/µL. Values ≥1,000 cells/µL score 1 point",
        example=500,
        ge=0,
        le=50000
    )
    
    csf_protein: float = Field(
        ...,
        description="CSF protein level in mg/dL. Values ≥80 mg/dL score 1 point",
        example=60.0,
        ge=0,
        le=1000
    )
    
    peripheral_blood_anc: int = Field(
        ...,
        description="Peripheral blood absolute neutrophil count in cells/µL. Values ≥10,000 cells/µL score 1 point",
        example=8000,
        ge=0,
        le=100000
    )
    
    seizure_at_presentation: Literal["no", "yes"] = Field(
        ...,
        description="Seizure at or prior to initial presentation. If yes, scores 1 point",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "csf_gram_stain": "negative",
                "csf_anc": 500,
                "csf_protein": 60.0,
                "peripheral_blood_anc": 8000,
                "seizure_at_presentation": "no"
            }
        }


class BacterialMeningitisScoreResponse(BaseModel):
    """
    Response model for Bacterial Meningitis Score for Children
    
    The score ranges from 0-6 points:
    - 0 points: Not Very Low Risk - Consider bacterial meningitis
    - 1-6 points: Very Low Risk - Bacterial meningitis very unlikely
    
    Reference: Nigrovic LE, et al. JAMA. 2007;297(1):52-60.
    """
    
    result: int = Field(
        ...,
        description="Bacterial Meningitis Score calculated from clinical and laboratory variables (range: 0-6 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on the score",
        example="Very Low Risk for bacterial meningitis. Consider outpatient management with close follow-up if clinically well-appearing."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Not Very Low Risk or Very Low Risk)",
        example="Very Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Bacterial meningitis very unlikely"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "Very Low Risk for bacterial meningitis. Consider outpatient management with close follow-up if clinically well-appearing.",
                "stage": "Very Low Risk",
                "stage_description": "Bacterial meningitis very unlikely"
            }
        }