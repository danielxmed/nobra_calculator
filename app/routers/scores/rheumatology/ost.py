"""
Osteoporosis Self Assessment Tool (OST) Router

Endpoint for calculating OST score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.ost import (
    OstRequest,
    OstResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/ost", response_model=OstResponse)
async def calculate_ost(request: OstRequest):
    """
    Calculates Osteoporosis Self Assessment Tool (OST)
    
    Predicts risk of osteoporosis based on age and body weight.
    Different risk thresholds apply for men and women.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        OstResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ost", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating OST score",
                    "details": {"parameters": parameters}
                }
            )
        
        return OstResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for OST score",
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