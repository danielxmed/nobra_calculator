"""
Four At router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology import FourAtRequest, FourAtResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post(
    "/four_at",
    response_model=FourAtResponse,
    summary="Calculate 4AT (4 A's Test) for Delirium Screening",
    description="Rapid clinical test for delirium detection in elderly patients. Includes cognitive test items, also suitable as a quick test for cognitive impairment.",
    response_description="The calculated four at with interpretation",
    operation_id="four_at"
)
async def calculate_four_at(request: FourAtRequest):
    """
    Calculates 4AT (4 A's Test) for delirium screening
    
    Args:
        request: 4AT test parameters
        
    Returns:
        FourAtResponse: Result with delirium probability
    """
    try:
        parameters = {
            "alertness": request.alertness.value,
            "amt4_errors": request.amt4_errors,
            "attention_months": request.attention_months.value,
            "acute_change": request.acute_change.value
        }
        
        result = calculator_service.calculate_score("four_at", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating 4AT",
                    "details": {"parameters": parameters}
                }
            )
        
        return FourAtResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for 4AT",
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