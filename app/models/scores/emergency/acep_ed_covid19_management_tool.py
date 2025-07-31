"""Models for ACEP ED COVID-19 Management Tool"""

from typing import Optional
from pydantic import BaseModel, Field
from typing_extensions import Literal

from app.models.shared import YesNoType


class AcepEdCovid19ManagementToolRequest(BaseModel):
    """Request model for ACEP ED COVID-19 Management Tool

    Provides parameters required to determine recommended disposition for adults with
    suspected or confirmed SARS-CoV-2 infection in the emergency department. The
    tool integrates NIH severity classification with the PRIEST score and patient
    risk factors to guide diagnostic workup and management.

    References:
    1. American College of Emergency Physicians. ACEP Emergency Department COVID-19 Management Tool. Fall 2023.
    2. MDCalc. ACEP ED COVID-19 Management Tool. https://www.mdcalc.com/calc/10333/acep-ed-covid-19-management-tool
    """

    severity: Literal["mild", "moderate", "severe", "critical"] = Field(
        ..., description="Clinical severity based on NIH criteria"
    )
    priest_score: int = Field(
        ..., ge=0, le=30, description="PRIEST score estimating risk of adverse outcome"
    )
    risk_factors: int = Field(
        ..., ge=0, le=20, description="Number of high-risk comorbid conditions"
    )
    imaging_concerning: YesNoType = Field(
        ..., description="Presence of concerning imaging findings"
    )
    labs_concerning: YesNoType = Field(
        ..., description="Presence of concerning laboratory results"
    )
    self_care_capable: YesNoType = Field(
        ..., description="Patient able to care for self and has adequate resources at home"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "severity": "mild",
                "priest_score": 3,
                "risk_factors": 0,
                "imaging_concerning": "no",
                "labs_concerning": "no",
                "self_care_capable": "yes",
            }
        }


class AcepEdCovid19ManagementToolResponse(BaseModel):
    """Response model for ACEP ED COVID-19 Management Tool"""

    result: str = Field(..., description="Recommended disposition")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Clinical interpretation")
    stage: str = Field(..., description="Disposition classification")
    stage_description: str = Field(..., description="Short description of disposition level")

    class Config:
        json_schema_extra = {
            "example": {
                "result": "Discharge",
                "unit": "disposition",
                "interpretation": "Safe for discharge with return precautions and follow-up.",
                "stage": "Discharge",
                "stage_description": "Mild disease with low risk of progression",
            }
        }
