"""
Abbreviated Mental Test (AMT-10) Models

Request and response models for AMT-10 calculation.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class Amt10Request(BaseModel):
    """Request model for Abbreviated Mental Test (AMT-10)"""
    age_correct: Literal["correct", "incorrect"] = Field(
        ..., 
        description="Patient correctly states their age",
        example="correct"
    )
    time_correct: Literal["correct", "incorrect"] = Field(
        ..., 
        description="Patient correctly states the time to the nearest hour",
        example="correct"
    )
    year_correct: Literal["correct", "incorrect"] = Field(
        ..., 
        description="Patient correctly states the current year",
        example="correct"
    )
    address_correct: Literal["correct", "incorrect"] = Field(
        ..., 
        description="Patient correctly states their home address or current location",
        example="correct"
    )
    recognition_correct: Literal["correct", "incorrect"] = Field(
        ..., 
        description="Patient correctly recognizes two people (doctor, nurse, family member, etc.)",
        example="correct"
    )
    dob_correct: Literal["correct", "incorrect"] = Field(
        ..., 
        description="Patient correctly states their date of birth (day and month sufficient)",
        example="correct"
    )
    wwi_correct: Literal["correct", "incorrect"] = Field(
        ..., 
        description="Patient correctly states the year World War I started (1914)",
        example="incorrect"
    )
    leader_correct: Literal["correct", "incorrect"] = Field(
        ..., 
        description="Patient correctly names the current monarch/president/prime minister",
        example="correct"
    )
    counting_correct: Literal["correct", "incorrect"] = Field(
        ..., 
        description="Patient correctly counts backwards from 20 to 1",
        example="correct"
    )
    recall_correct: Literal["correct", "incorrect"] = Field(
        ..., 
        description="Patient correctly recalls the address given earlier (e.g., '42 West Street')",
        example="correct"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_correct": "correct",
                "time_correct": "correct",
                "year_correct": "correct",
                "address_correct": "correct",
                "recognition_correct": "correct",
                "dob_correct": "correct",
                "wwi_correct": "incorrect",
                "leader_correct": "correct",
                "counting_correct": "correct",
                "recall_correct": "correct"
            }
        }


class Amt10Response(BaseModel):
    """Response model for Abbreviated Mental Test (AMT-10)"""
    result: int = Field(
        ..., 
        description="AMT-10 total score out of 10 points",
        example=8,
        ge=0,
        le=10
    )
    unit: str = Field(
        ..., 
        description="Result unit",
        example="points"
    )
    interpretation: str = Field(
        ..., 
        description="Clinical interpretation of the AMT-10 score",
        example="Score of 8-10 points indicates normal cognitive function. No significant cognitive impairment detected."
    )
    stage: Optional[str] = Field(
        None,
        description="Cognitive status classification",
        example="Normal"
    )
    stage_description: Optional[str] = Field(
        None,
        description="Cognitive status description",
        example="No cognitive impairment"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 8,
                "unit": "points",
                "interpretation": "Score of 8-10 points indicates normal cognitive function. No significant cognitive impairment detected.",
                "stage": "Normal",
                "stage_description": "No cognitive impairment"
            }
        }