"""
Los Angeles Motor Scale (LAMS) Router

Endpoint for calculating Los Angeles Motor Scale stroke severity assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.los_angeles_motor_scale import (
    LosAngelesMotorScaleRequest,
    LosAngelesMotorScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/los_angeles_motor_scale",
    response_model=LosAngelesMotorScaleResponse,
    summary="Calculate Los Angeles Motor Scale (LAMS)",
    description="Rapidly stratifies stroke severity in the field using a 3-component motor assessment to identify patients "
                "with large vessel occlusion strokes. The LAMS is designed for prehospital use by emergency medical services "
                "to guide transport decisions and optimize stroke care. LAMS ≥4 indicates severe stroke with high probability "
                "of large vessel occlusion requiring direct transport to comprehensive stroke centers with endovascular "
                "capabilities. LAMS <4 suggests minor to moderate stroke appropriate for transport to nearest stroke-capable "
                "facility. The scale demonstrates excellent correlation with NIHSS (r=0.75) and high accuracy for LVO "
                "detection (81% sensitivity, 89% specificity), making it a validated tool for time-sensitive stroke triage.",
    response_description="The calculated LAMS score with stroke severity classification and detailed transport recommendations",
    operation_id="los_angeles_motor_scale"
)
async def calculate_los_angeles_motor_scale(request: LosAngelesMotorScaleRequest):
    """
    Calculates Los Angeles Motor Scale (LAMS) for stroke severity assessment
    
    Provides rapid prehospital stroke severity evaluation using motor examination
    components to identify large vessel occlusion and guide transport decisions
    according to evidence-based stroke care protocols.
    
    Args:
        request: Motor assessment components (facial droop, arm drift, grip strength)
        
    Returns:
        LosAngelesMotorScaleResponse: LAMS score with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("los_angeles_motor_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Los Angeles Motor Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return LosAngelesMotorScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Los Angeles Motor Scale",
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