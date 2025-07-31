"""
Altitude-Adjusted PERC Rule Router

Endpoint for calculating Altitude-Adjusted PERC Rule.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.altitude_adjusted_perc import (
    AltitudeAdjustedPercRequest,
    AltitudeAdjustedPercResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/altitude_adjusted_perc",
    response_model=AltitudeAdjustedPercResponse,
    summary="Calculate Altitude-Adjusted PERC Rule",
    description="Rules out pulmonary embolism (PE) if no criteria are present; includes adjustment for high altitude (>4000 ft) by removing oxygen saturation criterion. Used in patients with low pretest probability of PE (<15%) who live at high altitude.",
    response_description="The calculated altitude adjusted perc with interpretation",
    operation_id="calculate_altitude_adjusted_perc"
)
async def calculate_altitude_adjusted_perc(request: AltitudeAdjustedPercRequest):
    """
    Calculates Altitude-Adjusted PERC Rule
    
    A clinical decision rule that helps rule out pulmonary embolism (PE) in patients 
    with low pretest probability (<15%) who live at high altitude (>4000 ft). This 
    modified version of the PERC rule removes the oxygen saturation criterion because 
    normal SaO₂ is naturally lower at high altitude, making it unreliable for PE 
    exclusion.
    
    Args:
        request: Clinical parameters for PERC rule evaluation
        
    Returns:
        AltitudeAdjustedPercResponse: PERC result with clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("altitude_adjusted_perc", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Altitude-Adjusted PERC Rule",
                    "details": {"parameters": parameters}
                }
            )
        
        return AltitudeAdjustedPercResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Altitude-Adjusted PERC Rule",
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