"""
Neuropathic Pain Scale (NPS) Router

Endpoint for calculating Neuropathic Pain Scale.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.neuropathic_pain_scale import (
    NeuropathicPainScaleRequest,
    NeuropathicPainScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/neuropathic_pain_scale",
    response_model=NeuropathicPainScaleResponse,
    summary="Calculate Neuropathic Pain Scale (NPS)",
    description="Quantifies severity of neuropathic pain using 10 specific pain quality dimensions. Only for patients already diagnosed with neuropathic pain.",
    response_description="The calculated neuropathic pain scale with interpretation",
    operation_id="neuropathic_pain_scale"
)
async def calculate_neuropathic_pain_scale(request: NeuropathicPainScaleRequest):
    """
    Calculates Neuropathic Pain Scale (NPS)
    
    Quantifies severity of neuropathic pain in patients who have already been 
    diagnosed with neuropathic pain. This scale assesses 10 distinct pain 
    qualities to provide a comprehensive pain assessment.
    
    Args:
        request: Parameters needed for calculation including 10 pain quality 
                ratings (0-10 each)
        
    Returns:
        NeuropathicPainScaleResponse: Total NPS score with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("neuropathic_pain_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Neuropathic Pain Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return NeuropathicPainScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Neuropathic Pain Scale",
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