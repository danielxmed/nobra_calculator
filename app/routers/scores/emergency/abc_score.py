"""
ABC Score for Massive Transfusion Router

Endpoint for calculating ABC Score for predicting massive transfusion requirements.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.abc_score import (
    AbcScoreRequest,
    AbcScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/abc_score", response_model=AbcScoreResponse)
async def calculate_abc_score(request: AbcScoreRequest):
    """
    Calculates ABC Score for Massive Transfusion
    
    Assessment of Blood Consumption (ABC) Score for predicting the necessity
    for massive transfusion in trauma patients using four clinical variables
    available at initial assessment. Score ≥2 indicates high risk requiring
    immediate activation of massive transfusion protocol.
    
    Args:
        request: Parameters needed for ABC Score calculation
        
    Returns:
        AbcScoreResponse: Result with clinical interpretation and risk stratification
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("abc_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ABC Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return AbcScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ABC Score",
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