"""
Fisher Grading Scale for Subarachnoid Hemorrhage (SAH) Router

Endpoint for calculating Fisher Grading Scale.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.fisher_grading_scale import (
    FisherGradingScaleRequest,
    FisherGradingScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/fisher_grading_scale",
    response_model=FisherGradingScaleResponse,
    summary="Calculate Fisher Grading Scale for Subarachnoid Hemorrhage",
    description="Assesses risk of vasospasm in SAH based on amount and distribution of blood on CT",
    response_description="The calculated fisher grading scale with interpretation",
    operation_id="calculate_fisher_grading_scale"
)
async def calculate_fisher_grading_scale(request: FisherGradingScaleRequest):
    """
    Calculates Fisher Grading Scale for Subarachnoid Hemorrhage (SAH)
    
    Assesses risk of vasospasm in SAH based on amount and distribution 
    of blood on CT scan.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        FisherGradingScaleResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("fisher_grading_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Fisher Grading Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return FisherGradingScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Fisher Grading Scale",
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