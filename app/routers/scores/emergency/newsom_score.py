"""
Newsom Score for Non-traumatic Chest Pain Router

Endpoint for calculating Newsom Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.newsom_score import (
    NewsomScoreRequest,
    NewsomScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/newsom_score", response_model=NewsomScoreResponse)
async def calculate_newsom_score(request: NewsomScoreRequest):
    """
    Calculates Newsom Score for Non-traumatic Chest Pain
    
    Rules out need for chest X-ray in patients with non-traumatic chest pain.
    The score uses 12 clinical criteria to identify low-risk patients.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        NewsomScoreResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("newsom_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Newsom Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return NewsomScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Newsom Score",
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