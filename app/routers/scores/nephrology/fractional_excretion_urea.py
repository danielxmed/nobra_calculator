"""
Fractional Excretion of Urea (FEUrea) Router

Endpoint for calculating FEUrea.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.fractional_excretion_urea import (
    FractionalExcretionUreaRequest,
    FractionalExcretionUreaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/fractional_excretion_urea",
    response_model=FractionalExcretionUreaResponse,
    summary="Calculate Fractional Excretion of Urea (FEUrea)",
    description="Determines the cause of renal failure. Similar to FENa, but can be used in patients on diuretics. More sensitive and specific than FENa for differentiating prerenal azotemia from acute tubular necrosis.",
    response_description="The calculated fractional excretion urea with interpretation",
    operation_id="calculate_fractional_excretion_urea"
)
async def calculate_fractional_excretion_urea(request: FractionalExcretionUreaRequest):
    """
    Calculates Fractional Excretion of Urea (FEUrea)
    
    Determines the cause of renal failure. Similar to FENa, but can be used 
    in patients on diuretics. More sensitive and specific than FENa for 
    differentiating prerenal azotemia from acute tubular necrosis.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        FractionalExcretionUreaResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("fractional_excretion_urea", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Fractional Excretion of Urea",
                    "details": {"parameters": parameters}
                }
            )
        
        return FractionalExcretionUreaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Fractional Excretion of Urea",
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