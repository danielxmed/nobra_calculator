"""
Fractional Excretion of Sodium (FENa) Router

Endpoint for calculating FENa.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.fractional_excretion_sodium import (
    FractionalExcretionSodiumRequest,
    FractionalExcretionSodiumResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/fractional_excretion_sodium",
    response_model=FractionalExcretionSodiumResponse,
    summary="Calculate Fractional Excretion of Sodium (FENa)",
    description="Determines if renal failure is due to pre-renal or intrinsic pathology. Calculates the percentage of filtered sodium that is excreted in the urine.",
    response_description="The calculated fractional excretion sodium with interpretation",
    operation_id="calculate_fractional_excretion_sodium"
)
async def calculate_fractional_excretion_sodium(request: FractionalExcretionSodiumRequest):
    """
    Calculates Fractional Excretion of Sodium (FENa)
    
    Determines if renal failure is due to pre-renal or intrinsic pathology. 
    Calculates the percentage of filtered sodium that is excreted in the urine.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        FractionalExcretionSodiumResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("fractional_excretion_sodium", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Fractional Excretion of Sodium",
                    "details": {"parameters": parameters}
                }
            )
        
        return FractionalExcretionSodiumResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Fractional Excretion of Sodium",
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