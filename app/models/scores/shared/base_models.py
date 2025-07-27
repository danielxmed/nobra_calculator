"""
Shared base models and enums used across multiple medical scores
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class SexType(str, Enum):
    """Enum for accepted sex types"""
    MALE = "male"
    FEMALE = "female"


class YesNoType(str, Enum):
    """Enum for yes/no responses"""
    YES = "yes"
    NO = "no"


class YesNoNAType(str, Enum):
    """Enum for yes/no/not applicable responses"""
    YES = "yes"
    NO = "no"
    NOT_APPLICABLE = "not_applicable"


class DiabetesType(str, Enum):
    """Enum for diabetes status"""
    YES = "yes"
    NO = "no"


class ScoreInfo(BaseModel):
    """Basic information of a medical score"""
    id: str = Field(..., description="Unique identifier of the medical score")
    title: str = Field(..., description="Full title of the medical score or calculator")
    description: str = Field(..., description="Brief description of what the score calculates and its clinical purpose")
    category: str = Field(..., description="Medical specialty or category (e.g., cardiology, nephrology, neurology)")
    version: Optional[str] = Field(None, description="Version year or revision of the score/equation")


class ScoreListResponse(BaseModel):
    """Response for listing available medical scores"""
    scores: List[ScoreInfo] = Field(..., description="Array of available medical scores with basic information")
    total: int = Field(..., description="Total number of available scores in the system")
    
    class Config:
        schema_extra = {
            "example": {
                "scores": [
                    {
                        "id": "ckd_epi_2021",
                        "title": "CKD-EPI 2021 - Estimated Glomerular Filtration Rate",
                        "description": "CKD-EPI 2021 equation to estimate glomerular filtration rate",
                        "category": "nephrology",
                        "version": "2021"
                    }
                ],
                "total": 1
            }
        }


class Parameter(BaseModel):
    """Model for score parameters with validation rules"""
    name: str = Field(..., description="Parameter name as used in the calculation")
    type: str = Field(..., description="Data type (string, integer, float, boolean)")
    required: bool = Field(..., description="Whether this parameter is mandatory for calculation")
    description: str = Field(..., description="Detailed description of the parameter and its clinical significance")
    options: Optional[List[str]] = Field(None, description="Valid options for string parameters (enum values)")
    validation: Optional[Dict[str, Any]] = Field(None, description="Validation rules including min/max values or enum constraints")
    unit: Optional[str] = Field(None, description="Unit of measurement for numeric parameters")


class ResultInfo(BaseModel):
    """Information about a score's calculated result"""
    name: str = Field(..., description="Name of the result variable")
    type: str = Field(..., description="Data type of the result (integer, float, string)")
    unit: str = Field(..., description="Unit of measurement or classification type")
    description: str = Field(..., description="Description of what the result represents clinically")


class InterpretationRange(BaseModel):
    """Interpretation range for score results with clinical significance"""
    min: float = Field(..., description="Minimum value of this interpretation range (inclusive)")
    max: Optional[float] = Field(None, description="Maximum value of this interpretation range (inclusive). Null means no upper limit.")
    stage: str = Field(..., description="Classification stage or risk level name")
    description: str = Field(..., description="Brief description of this stage or risk level")
    interpretation: str = Field(..., description="Detailed clinical interpretation and recommended actions for this range")


class Interpretation(BaseModel):
    """Model for score interpretations with clinical ranges"""
    ranges: List[InterpretationRange] = Field(..., description="Array of interpretation ranges with clinical significance")


class ScoreMetadataResponse(BaseModel):
    """
    Comprehensive metadata response for a medical score
    
    Provides complete information about a medical score including parameters, 
    interpretation ranges, references, and clinical notes.
    """
    id: str = Field(..., description="Unique identifier of the medical score")
    title: str = Field(..., description="Full title of the medical score")
    description: str = Field(..., description="Comprehensive description of the score's purpose and clinical application")
    category: str = Field(..., description="Medical specialty category")
    version: Optional[str] = Field(None, description="Version or year of the score")
    parameters: List[Parameter] = Field(..., description="Required parameters for calculation with validation rules")
    result: ResultInfo = Field(..., description="Information about the calculated result")
    interpretation: Interpretation = Field(..., description="Clinical interpretation ranges and recommendations")
    references: List[str] = Field(..., description="Scientific references and citations for the score")
    formula: str = Field(..., description="Mathematical formula or algorithm description")
    notes: List[str] = Field(..., description="Important clinical notes and considerations")


class ErrorResponse(BaseModel):
    """Standardized error response model"""
    error: str = Field(..., description="Error type classification")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error context and debugging information")
    
    class Config:
        schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid parameters provided",
                "details": {
                    "field": "age",
                    "value": 15,
                    "constraint": "must be >= 18"
                }
            }
        }


class HealthResponse(BaseModel):
    """Response for API health check endpoint"""
    status: str = Field(..., description="Current API operational status")
    message: str = Field(..., description="Status description message")
    version: str = Field(..., description="Current API version")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "message": "nobra_calculator API is running correctly",
                "version": "1.0.0"
            }
        }