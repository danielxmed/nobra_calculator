"""
Basal Energy Expenditure Router

Endpoint for calculating Basal Energy Expenditure using Harris-Benedict equation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.basal_energy_expenditure import (
    BasalEnergyExpenditureRequest,
    BasalEnergyExpenditureResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/basal_energy_expenditure",
    response_model=BasalEnergyExpenditureResponse,
    summary="Calculate Basal Energy Expenditure",
    description="Calculates daily energy expenditure using the Harris-Benedict equation. Estimates the minimum daily caloric requirements at rest (basal metabolic rate) and can be adjusted for activity level to determine total daily energy needs.",
    response_description="The calculated basal energy expenditure with interpretation",
    operation_id="basal_energy_expenditure"
)
async def calculate_basal_energy_expenditure(request: BasalEnergyExpenditureRequest):
    """
    Calculates Basal Energy Expenditure
    
    Uses the Harris-Benedict equation to estimate the minimum daily caloric 
    requirements at rest (basal metabolic rate). Can be adjusted for activity 
    level to determine Total Daily Energy Expenditure (TDEE).
    
    Args:
        request: Parameters including sex, weight, height, age, and optional activity level
        
    Returns:
        BasalEnergyExpenditureResponse: BEE or TDEE with interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("basal_energy_expenditure", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating basal energy expenditure",
                    "details": {"parameters": parameters}
                }
            )
        
        return BasalEnergyExpenditureResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for basal energy expenditure",
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