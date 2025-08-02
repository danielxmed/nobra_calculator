"""
Modified NIH Stroke Scale (mNIHSS) Router

Endpoint for calculating Modified NIH Stroke Scale for stroke severity assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.modified_nih_stroke_scale import (
    ModifiedNihStrokeScaleRequest,
    ModifiedNihStrokeScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/modified_nih_stroke_scale",
    response_model=ModifiedNihStrokeScaleResponse,
    summary="Calculate Modified NIH Stroke Scale (mNIHSS)",
    description="Calculates the Modified NIH Stroke Scale (mNIHSS) for quantifying stroke severity with improved interrater reliability. "
                "This shortened, validated version of the original NIHSS removes redundant and poorly reliable items while maintaining "
                "equal validity for outcome prediction. The mNIHSS takes less time to complete (6 minutes vs 7-10 minutes) and "
                "demonstrates better performance in telemedicine applications and when abstracted from medical records. "
                "It provides objective assessment of neurological deficits across 11 domains to guide treatment decisions, "
                "monitor clinical changes, and predict functional outcomes in stroke patients.",
    response_description="The calculated mNIHSS score with stroke severity stratification and clinical management recommendations",
    operation_id="modified_nih_stroke_scale"
)
async def calculate_modified_nih_stroke_scale(request: ModifiedNihStrokeScaleRequest):
    """
    Calculates Modified NIH Stroke Scale (mNIHSS) for stroke severity assessment
    
    Provides objective, reliable assessment of stroke severity through evaluation of 
    11 neurological domains. The modified scale improves upon the original NIHSS 
    by removing redundant items and enhancing interrater reliability while 
    maintaining validity for clinical decision-making and outcome prediction.
    
    Args:
        request: Parameters needed for mNIHSS calculation
        
    Returns:
        ModifiedNihStrokeScaleResponse: mNIHSS score with clinical interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("modified_nih_stroke_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Modified NIH Stroke Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return ModifiedNihStrokeScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Modified NIH Stroke Scale",
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