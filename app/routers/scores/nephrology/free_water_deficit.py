"""
Free Water Deficit in Hypernatremia Router

Endpoint for calculating Free Water Deficit in Hypernatremia.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.free_water_deficit import (
    FreeWaterDeficitRequest,
    FreeWaterDeficitResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/free_water_deficit",
    response_model=FreeWaterDeficitResponse,
    summary="Calculate Free Water Deficit in Hypernatremia",
    description="Calculates free water deficit by estimated total body water in patients with hypernatremia or dehydration",
    response_description="The calculated free water deficit with interpretation",
    operation_id="calculate_free_water_deficit"
)
async def calculate_free_water_deficit(request: FreeWaterDeficitRequest):
    """
    Calculates Free Water Deficit in Hypernatremia
    
    Estimates the amount of free water needed to correct hypernatremia based on 
    total body water and serum sodium levels. Uses patient-specific TBW fractions 
    based on age and sex to provide safe correction guidance.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        FreeWaterDeficitResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("free_water_deficit", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Free Water Deficit in Hypernatremia",
                    "details": {"parameters": parameters}
                }
            )
        
        return FreeWaterDeficitResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Free Water Deficit in Hypernatremia",
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