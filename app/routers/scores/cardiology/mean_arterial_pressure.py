"""
Mean Arterial Pressure (MAP) Router

Endpoint for calculating Mean Arterial Pressure.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.mean_arterial_pressure import (
    MeanArterialPressureRequest,
    MeanArterialPressureResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mean_arterial_pressure",
    response_model=MeanArterialPressureResponse,
    summary="Calculate Mean Arterial Pressure (MAP)",
    description="Calculates the Mean Arterial Pressure (MAP) from systolic and diastolic "
                "blood pressure measurements. MAP represents the average arterial pressure "
                "throughout one cardiac cycle and is calculated as (2 × Diastolic BP + "
                "Systolic BP) / 3. This accounts for the fact that approximately two-thirds "
                "of the cardiac cycle is spent in diastole. MAP is a critical parameter for "
                "assessing tissue perfusion, particularly in critical care settings. Normal "
                "MAP is 70-110 mmHg, with MAP ≥60 mmHg generally needed to maintain adequate "
                "organ perfusion and MAP ≥65 mmHg recommended in sepsis and septic shock. "
                "MAP is superior to systolic BP alone for evaluating tissue perfusion and "
                "guiding vasopressor therapy.",
    response_description="The calculated MAP with clinical interpretation and perfusion adequacy assessment",
    operation_id="mean_arterial_pressure"
)
async def calculate_mean_arterial_pressure(request: MeanArterialPressureRequest):
    """
    Calculates Mean Arterial Pressure (MAP)
    
    MAP is the average pressure in the arteries during one cardiac cycle,
    providing a better indicator of tissue perfusion than systolic BP alone.
    Used extensively in critical care for hemodynamic monitoring.
    
    Args:
        request: Systolic and diastolic blood pressure values
        
    Returns:
        MeanArterialPressureResponse: Calculated MAP with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mean_arterial_pressure", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Mean Arterial Pressure",
                    "details": {"parameters": parameters}
                }
            )
        
        return MeanArterialPressureResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MAP calculation",
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