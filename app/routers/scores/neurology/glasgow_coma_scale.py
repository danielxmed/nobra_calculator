"""
Glasgow Coma Scale (GCS) Router

Endpoint for calculating Glasgow Coma Scale.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.glasgow_coma_scale import (
    GlasgowComaScaleRequest,
    GlasgowComaScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/glasgow_coma_scale",
    response_model=GlasgowComaScaleResponse,
    summary="Calculate Glasgow Coma Scale (GCS)",
    description="Clinical scale used to assess level of consciousness and neurological function in patients with acute brain injury. Evaluates three components: eye opening response (1-4), verbal response (1-5), and motor response (1-6) for a total score ranging from 3-15",
    response_description="The calculated glasgow coma scale with interpretation",
    operation_id="glasgow_coma_scale"
)
async def calculate_glasgow_coma_scale(request: GlasgowComaScaleRequest):
    """
    Calculates Glasgow Coma Scale (GCS)
    
    The Glasgow Coma Scale is a clinical scale used to reliably measure a person's 
    level of consciousness after a brain injury. It evaluates three aspects of 
    responsiveness: eye opening, verbal response, and motor response. The scale 
    provides standardized assessment across healthcare providers and settings.
    
    Args:
        request: Parameters including eye opening (1-4), verbal response (1-5), 
                and motor response (1-6)
        
    Returns:
        GlasgowComaScaleResponse: Total GCS score with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("glasgow_coma_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Glasgow Coma Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return GlasgowComaScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Glasgow Coma Scale",
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