"""
Hamilton Depression Rating Scale Router

Endpoint for calculating Hamilton Depression Rating Scale (HAM-D).
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.hamilton_depression_rating_scale import (
    HamiltonDepressionRatingScaleRequest,
    HamiltonDepressionRatingScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hamilton_depression_rating_scale",
    response_model=HamiltonDepressionRatingScaleResponse,
    summary="Calculate Hamilton Depression Rating Scale (HAM-D)",
    description="Assesses severity of depression symptoms. The 17-item version is a clinician-administered scale that measures depressive symptoms over the past week.",
    response_description="The calculated hamilton depression rating scale with interpretation",
    operation_id="hamilton_depression_rating_scale"
)
async def calculate_hamilton_depression_rating_scale(request: HamiltonDepressionRatingScaleRequest):
    """
    Calculates Hamilton Depression Rating Scale (HAM-D)
    
    The HAM-D is a clinician-administered 17-item scale that assesses the severity 
    of depressive symptoms over the past week. It evaluates mood, guilt, suicidal 
    ideation, insomnia, psychomotor symptoms, anxiety, somatic symptoms, and insight. 
    Widely used in clinical trials to measure treatment response.
    
    Args:
        request: Parameters for each of the 17 depressive symptom domains
        
    Returns:
        HamiltonDepressionRatingScaleResponse: Result with depression severity level
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hamilton_depression_rating_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Hamilton Depression Rating Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return HamiltonDepressionRatingScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Hamilton Depression Rating Scale",
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