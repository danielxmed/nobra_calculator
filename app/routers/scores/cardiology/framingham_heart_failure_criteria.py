"""
Framingham Heart Failure Diagnostic Criteria Router

Endpoint for calculating Framingham Heart Failure Diagnostic Criteria.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.framingham_heart_failure_criteria import (
    FraminghamHeartFailureCriteriaRequest,
    FraminghamHeartFailureCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/framingham_heart_failure_criteria",
    response_model=FraminghamHeartFailureCriteriaResponse,
    summary="Calculate Framingham Heart Failure Diagnostic C...",
    description="Diagnoses heart failure based on major and minor criteria. Requires at least 2 major criteria or 1 major criterion plus 2 minor criteria.",
    response_description="The calculated framingham heart failure criteria with interpretation",
    operation_id="framingham_heart_failure_criteria"
)
async def calculate_framingham_heart_failure_criteria(request: FraminghamHeartFailureCriteriaRequest):
    """
    Calculates Framingham Heart Failure Diagnostic Criteria
    
    Diagnoses heart failure based on major and minor criteria. Requires at least 
    2 major criteria or 1 major criterion plus 2 minor criteria.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        FraminghamHeartFailureCriteriaResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("framingham_heart_failure_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Framingham Heart Failure Diagnostic Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return FraminghamHeartFailureCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Framingham Heart Failure Diagnostic Criteria",
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