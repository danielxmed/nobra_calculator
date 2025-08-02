"""
Modified Brain Injury Guideline (mBIG) Router

Endpoint for calculating mBIG classification for traumatic brain injury management.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.modified_brain_injury_guideline import (
    ModifiedBrainInjuryGuidelineRequest,
    ModifiedBrainInjuryGuidelineResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/modified_brain_injury_guideline",
    response_model=ModifiedBrainInjuryGuidelineResponse,
    summary="Calculate Modified Brain Injury Guideline (mBIG)",
    description="Calculates the Modified Brain Injury Guideline (mBIG) classification for traumatic brain injury "
                "management. This evidence-based algorithm stratifies patients with traumatic brain injury and "
                "intracranial hemorrhage into three management categories (mBIG 1, 2, 3) based on radiographic "
                "and clinical findings. The mBIG optimizes resource utilization by identifying patients who can "
                "be safely managed without neurosurgical consultation, repeat imaging, or hospital admission. "
                "It applies to patients with GCS 13-15, intracranial hemorrhage on CT, and no focal neurologic "
                "findings. Validation studies demonstrate significant cost savings and resource optimization "
                "while maintaining patient safety.",
    response_description="The mBIG classification category with detailed management recommendations and resource utilization guidance",
    operation_id="modified_brain_injury_guideline"
)
async def calculate_modified_brain_injury_guideline(request: ModifiedBrainInjuryGuidelineRequest):
    """
    Calculates Modified Brain Injury Guideline (mBIG) Classification
    
    The mBIG is an evidence-based algorithm for managing traumatic brain injury 
    patients with intracranial hemorrhage. It provides hierarchical criteria to 
    stratify patients into appropriate management categories, reducing unnecessary 
    resource utilization while maintaining safety.
    
    Args:
        request: Clinical and radiographic parameters from CT scan and patient assessment
        
    Returns:
        ModifiedBrainInjuryGuidelineResponse: mBIG category with management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("modified_brain_injury_guideline", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Modified Brain Injury Guideline",
                    "details": {"parameters": parameters}
                }
            )
        
        return ModifiedBrainInjuryGuidelineResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Modified Brain Injury Guideline",
                "details": {"error": str(e)}
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Internal error in calculation",
                "details": {"error": str(e)}
            }
        )