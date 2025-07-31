"""
ASA Physical Status Classification System Models

Pydantic models for ASA Physical Status Classification System endpoints.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AsaPhysicalStatusRequest(BaseModel):
    """Request model for ASA Physical Status Classification calculation"""
    
    physical_status: Literal["asa_1", "asa_2", "asa_3", "asa_4", "asa_5", "asa_6"] = Field(
        ..., 
        description="Patient's physical status based on systemic disease and functional limitations"
    )
    emergency_surgery: Literal["yes", "no"] = Field(
        ..., 
        description="Whether this is an emergency surgery (delay would significantly increase threat to life or body part)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "physical_status": "asa_2",
                "emergency_surgery": "no"
            }
        }


class AsaPhysicalStatusResponse(BaseModel):
    """Response model for ASA Physical Status Classification calculation"""
    
    result: str = Field(..., description="Final ASA Physical Status Classification with emergency modifier if applicable")
    unit: str = Field(..., description="Unit (empty for classification systems)")
    interpretation: str = Field(..., description="Clinical interpretation of the classification")
    stage: str = Field(..., description="ASA classification stage")
    stage_description: str = Field(..., description="Description of the ASA stage")

    class Config:
        json_schema_extra = {
            "example": {
                "result": "ASA II",
                "unit": "",
                "interpretation": "A patient with mild systemic disease without substantive functional limitations. Examples: current smoker, social alcohol drinker, pregnancy, obesity (BMI 30-40), well-controlled diabetes/hypertension, mild lung disease. Perioperative risk: Low risk. The ASA Physical Status Classification should be used alongside other factors such as type of surgery, patient frailty, and procedural complexity for comprehensive perioperative risk assessment.",
                "stage": "ASA II",
                "stage_description": "Patient with mild systemic disease"
            }
        }
