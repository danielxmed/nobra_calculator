"""
Abbreviated Injury Score (AIS) for Inhalation Injury Models

Request and response models for AIS Inhalation Injury calculation.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class AisInhalationInjuryRequest(BaseModel):
    """Request model for Abbreviated Injury Score (AIS) for Inhalation Injury"""
    bronchoscopic_findings: Literal[
        "grade_0", "grade_1", "grade_2", "grade_3", "grade_4"
    ] = Field(
        ..., 
        description="Bronchoscopic findings observed during flexible bronchoscopy",
        example="grade_2"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "bronchoscopic_findings": "grade_2"
            }
        }


class AisInhalationInjuryResponse(BaseModel):
    """Response model for Abbreviated Injury Score (AIS) for Inhalation Injury"""
    result: int = Field(
        ..., 
        description="AIS score for inhalation injury severity",
        example=2,
        ge=0,
        le=4
    )
    unit: str = Field(
        ..., 
        description="Result unit",
        example="points"
    )
    interpretation: str = Field(
        ..., 
        description="Clinical interpretation of the AIS score",
        example="Moderate erythema, carbonaceous deposits, bronchorrhea, or bronchial obstruction present. Moderate inhalation injury requiring close monitoring and supportive care."
    )
    stage: Optional[str] = Field(
        None,
        description="Grade classification",
        example="Grade 2"
    )
    stage_description: Optional[str] = Field(
        None,
        description="Grade description",
        example="Moderate inhalation injury"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "Moderate erythema, carbonaceous deposits, bronchorrhea, or bronchial obstruction present. Moderate inhalation injury requiring close monitoring and supportive care.",
                "stage": "Grade 2",
                "stage_description": "Moderate inhalation injury"
            }
        }