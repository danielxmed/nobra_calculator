"""
Osteoporosis Risk Assessment Instrument (ORAI) Router

Endpoint for calculating ORAI score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.orai import (
    OraiRequest,
    OraiResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/orai",
    response_model=OraiResponse,
    summary="Calculate Osteoporosis Risk Assessment Instrument (ORAI)",
    description="Identifies women at risk for osteoporosis and recommends bone densitometry. Uses age, weight, and current estrogen use to stratify risk in postmenopausal women.",
    response_description="The calculated orai with interpretation",
    operation_id="calculate_orai"
)
async def calculate_orai(request: OraiRequest):
    """
    Calculates Osteoporosis Risk Assessment Instrument (ORAI)
    
    Identifies women at risk for osteoporosis and recommends bone densitometry
    based on age, weight, and current estrogen use.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        OraiResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("orai", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ORAI score",
                    "details": {"parameters": parameters}
                }
            )
        
        return OraiResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ORAI score",
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