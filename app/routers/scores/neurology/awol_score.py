"""
AWOL Score for Delirium Router

Endpoint for calculating AWOL Score for Delirium.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.awol_score import (
    AwolScoreRequest,
    AwolScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/awol_score",
    response_model=AwolScoreResponse,
    summary="Calculate AWOL Score for Delirium",
    description="Predicts risk of delirium during hospitalization using age, cognitive function, orientation, and illness severity",
    response_description="The calculated awol score with interpretation",
    operation_id="awol_score"
)
async def calculate_awol_score(request: AwolScoreRequest):
    """
    Calculates AWOL Score for Delirium
    
    Predicts risk of delirium during hospitalization using four clinical factors:
    Age, World backward spelling, Orientation, and iLlness severity.
    
    Args:
        request: Parameters needed for calculation including age category,
                 cognitive function, orientation status, and illness severity
        
    Returns:
        AwolScoreResponse: Result with delirium risk percentage and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("awol_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating AWOL Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return AwolScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for AWOL Score",
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