"""
National Early Warning Score (NEWS) Router

Endpoint for calculating National Early Warning Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.news import (
    NewsRequest,
    NewsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/news", response_model=NewsResponse)
async def calculate_news(request: NewsRequest):
    """
    Calculates National Early Warning Score (NEWS)
    
    Determines the degree of illness of a patient and prompts critical care intervention.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        NewsResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("news", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating National Early Warning Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return NewsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for National Early Warning Score",
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