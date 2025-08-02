"""
Urine Output and Fluid Balance Router

Endpoint for calculating urine output rate and fluid balance assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.urine_output_fluid_balance import (
    UrineOutputFluidBalanceRequest,
    UrineOutputFluidBalanceResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/urine_output_fluid_balance",
    response_model=UrineOutputFluidBalanceResponse,
    summary="Calculate Urine Output and Fluid Balance",
    description="Calculates urine output rate per kg body weight per hour and assesses fluid balance for monitoring renal function and fluid status. "
                "This tool helps identify oliguria, polyuria, and fluid imbalances in hospitalized patients, particularly those at risk for acute kidney injury. "
                "Normal urine output ranges from 1.0-2.0 mL/kg/hr. Oliguria is defined as <0.5 mL/kg/hr and may indicate acute kidney injury. "
                "The calculator also provides fluid balance assessment and 24-hour extrapolated values for clinical monitoring.",
    response_description="The calculated urine output rate with clinical interpretation, fluid balance, and 24-hour extrapolated output",
    operation_id="urine_output_fluid_balance"
)
async def calculate_urine_output_fluid_balance(request: UrineOutputFluidBalanceRequest):
    """
    Calculates Urine Output and Fluid Balance
    
    Assesses renal function and fluid status by calculating the urine output rate 
    per kg body weight per hour and determining net fluid balance.
    
    Args:
        request: Parameters including patient weight, urine output, collection period, and fluid intake
        
    Returns:
        UrineOutputFluidBalanceResponse: Result with clinical interpretation, fluid balance, and monitoring recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("urine_output_fluid_balance", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Urine Output and Fluid Balance",
                    "details": {"parameters": parameters}
                }
            )
        
        return UrineOutputFluidBalanceResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Urine Output and Fluid Balance calculation",
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