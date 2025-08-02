"""
IV Drip Rate Calculator Router

Endpoint for calculating IV drip rate.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.iv_drip_rate_calculator import (
    IvDripRateCalculatorRequest,
    IvDripRateCalculatorResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/iv_drip_rate_calculator",
    response_model=IvDripRateCalculatorResponse,
    summary="Calculate IV Drip Rate",
    description="Calculates the IV infusion rate in drops per minute for gravity-fed intravenous administration when electronic pumps are unavailable. This essential tool determines the correct manual drip rate using the standard formula: (Volume × Drop factor) / Time. Critical for resource-limited settings, emergency situations, and as backup when infusion pumps malfunction. Supports all standard IV tubing drop factors (10, 15, 20, 60 gtts/mL) with safety guidance for different infusion rates.",
    response_description="The calculated drip rate in drops per minute with clinical interpretation, safety considerations, and monitoring guidance",
    operation_id="iv_drip_rate_calculator"
)
async def calculate_iv_drip_rate_calculator(request: IvDripRateCalculatorRequest):
    """
    Calculates IV Drip Rate
    
    Determines the correct drops per minute needed to deliver a specified volume of IV fluid 
    over a given time period using gravity-fed administration sets. Essential for healthcare 
    settings without electronic infusion pumps.
    
    Args:
        request: Parameters including volume (mL), time (minutes), and drop factor (gtts/mL)
        
    Returns:
        IvDripRateCalculatorResponse: Drip rate with clinical interpretation and safety guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("iv_drip_rate_calculator", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating IV Drip Rate",
                    "details": {"parameters": parameters}
                }
            )
        
        return IvDripRateCalculatorResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for IV Drip Rate Calculator",
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