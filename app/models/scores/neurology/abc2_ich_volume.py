"""
ABC/2 Formula for Intracerebral Hemorrhage Volume Models

Request and response models for ABC/2 ICH Volume calculation.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class Abc2IchVolumeRequest(BaseModel):
    """Request model for ABC/2 Formula for Intracerebral Hemorrhage Volume"""
    hemorrhage_shape: Literal["round_ellipsoid", "irregular_multinodular"] = Field(
        ...,
        description="Shape of the hemorrhage on CT scan",
        example="round_ellipsoid"
    )
    length_a: float = Field(
        ...,
        ge=0.1,
        le=20.0,
        description="Greatest hemorrhage diameter (A) on CT slice with largest area",
        example=3.2
    )
    width_b: float = Field(
        ...,
        ge=0.1,
        le=20.0,
        description="Diameter 90 degrees to A on the same CT slice (B)",
        example=2.8
    )
    weighted_slices: float = Field(
        ...,
        ge=0.5,
        le=50.0,
        description="Number of CT slices weighted by hemorrhage area (C): >75% area = 1 slice, 25-75% = 0.5 slice, <25% = 0 slice",
        example=4.5
    )
    slice_thickness: float = Field(
        ...,
        ge=1.0,
        le=15.0,
        description="CT slice thickness",
        example=5.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "hemorrhage_shape": "round_ellipsoid",
                "length_a": 3.2,
                "width_b": 2.8,
                "weighted_slices": 4.5,
                "slice_thickness": 5.0
            }
        }


class Abc2IchVolumeResponse(BaseModel):
    """Response model for ABC/2 Formula for Intracerebral Hemorrhage Volume"""
    result: float = Field(
        ...,
        description="Estimated intracerebral hemorrhage volume",
        example=20.16
    )
    unit: str = Field(
        ...,
        description="Unit of measurement",
        example="cm³"
    )
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the hemorrhage volume",
        example="Moderate ICH volume. Monitor closely for expansion and neurological changes. Consider surgical evaluation based on clinical condition."
    )
    stage: Optional[str] = Field(
        None,
        description="Volume stage classification",
        example="Moderate"
    )
    stage_description: Optional[str] = Field(
        None,
        description="Description of the volume stage",
        example="Moderate volume hemorrhage"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 20.16,
                "unit": "cm³",
                "interpretation": "Moderate ICH volume. Monitor closely for expansion and neurological changes. Consider surgical evaluation based on clinical condition.",
                "stage": "Moderate",
                "stage_description": "Moderate volume hemorrhage"
            }
        }
