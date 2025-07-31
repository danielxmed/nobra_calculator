"""
Cardiac Power Output (CPO) Router

Endpoint for calculating cardiac power output.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.cardiac_power_output import (
    CardiacPowerOutputRequest,
    CardiacPowerOutputResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/cardiac_power_output",
    response_model=CardiacPowerOutputResponse,
    summary="Calculate Cardiac Power Output (CPO)",
    description="Calculates cardiac power output, the rate of energy output of the heart. Integrates both pressure and flow components of cardiac work. Strong hemodynamic predictor of mortality in cardiogenic shock.",
    response_description="The calculated cardiac power output with interpretation",
    operation_id="calculate_cardiac_power_output"
)
async def calculate_cardiac_power_output(request: CardiacPowerOutputRequest):
    """
    Calculates Cardiac Power Output (CPO)
    
    Calculates the rate of energy output of the heart by integrating both pressure 
    (mean arterial pressure) and flow (cardiac output) components of cardiac work.
    CPO is recognized as the strongest hemodynamic predictor of mortality in 
    cardiogenic shock.
    
    The calculator supports both:
    - Standard formula: CPO = (MAP × CO) / 451
    - Original Tan formula: CPO = [(MAP - RAP) × CO] / 451 (when RAP provided)
    
    Clinical significance:
    - Normal resting CPO: ~1.0 Watt
    - CPO <0.6W: Severe ventricular dysfunction with poor prognosis
    - CPO 0.6-1.0W: Moderately reduced cardiac function  
    - CPO ≥1.0W: Adequate cardiac function
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        CardiacPowerOutputResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cardiac_power_output", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Cardiac Power Output",
                    "details": {"parameters": parameters}
                }
            )
        
        return CardiacPowerOutputResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Cardiac Power Output",
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