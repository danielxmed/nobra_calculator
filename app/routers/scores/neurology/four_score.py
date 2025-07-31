"""
FOUR (Full Outline of UnResponsiveness) Score Router

Endpoint for calculating FOUR Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.four_score import (
    FourScoreRequest,
    FourScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/four_score",
    response_model=FourScoreResponse,
    summary="Calculate FOUR (Full Outline of UnResponsiveness) Score",
    description="Grades severity of coma; may be more accurate than Glasgow Coma Scale. Evaluates consciousness level through four components: eye response, motor response, brainstem reflexes, and respiration pattern.",
    response_description="The calculated four score with interpretation",
    operation_id="calculate_four_score"
)
async def calculate_four_score(request: FourScoreRequest):
    """
    Calculates FOUR (Full Outline of UnResponsiveness) Score
    
    Grades severity of coma; may be more accurate than Glasgow Coma Scale. 
    Evaluates consciousness level through four components: eye response, 
    motor response, brainstem reflexes, and respiration pattern.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        FourScoreResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("four_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating FOUR Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return FourScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for FOUR Score",
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