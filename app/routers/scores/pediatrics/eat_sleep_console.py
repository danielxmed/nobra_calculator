"""
Eat, Sleep, Console (ESC) Router

Endpoint for calculating Eat, Sleep, Console assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.eat_sleep_console import (
    EatSleepConsoleRequest,
    EatSleepConsoleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/eat_sleep_console",
    response_model=EatSleepConsoleResponse,
    summary="Calculate Eat, Sleep, Console (ESC)",
    description="Aids in management of infants with neonatal abstinence syndrome (NAS) by focusing on functional assessment rather than symptom scoring. Emphasizes nonpharmacologic interventions and family-centered care to optimize infant functioning.",
    response_description="The calculated eat sleep console with interpretation",
    operation_id="calculate_eat_sleep_console"
)
async def calculate_eat_sleep_console(request: EatSleepConsoleRequest):
    """
    Calculates Eat, Sleep, Console (ESC) Assessment
    
    The ESC approach is a function-based care model for managing neonatal abstinence 
    syndrome (NAS) that focuses on whether infants can perform three essential functions 
    with nonpharmacologic support. This evidence-based approach emphasizes family-centered 
    care, reduces medication use, and shortens hospital stays compared to traditional 
    symptom-based scoring systems.
    
    Args:
        request: Parameters needed for assessment including ability to eat adequately,
                sleep undisturbed, and be consoled with standard comfort measures
        
    Returns:
        EatSleepConsoleResponse: Result with clinical interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("eat_sleep_console", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Eat, Sleep, Console assessment",
                    "details": {"parameters": parameters}
                }
            )
        
        return EatSleepConsoleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Eat, Sleep, Console assessment",
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