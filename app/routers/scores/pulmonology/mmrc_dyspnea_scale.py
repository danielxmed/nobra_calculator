"""
mMRC (Modified Medical Research Council) Dyspnea Scale Router

Endpoint for calculating mMRC Dyspnea Scale functional disability assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.mmrc_dyspnea_scale import (
    MmrcDyspneaScaleRequest,
    MmrcDyspneaScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mmrc_dyspnea_scale",
    response_model=MmrcDyspneaScaleResponse,
    summary="Calculate mMRC (Modified Medical Research Council) Dyspnea Scale",
    description="Stratifies severity of dyspnea in respiratory diseases, particularly COPD, based on functional "
                "disability due to breathlessness. The mMRC scale ranges from Grade 0 (dyspnea only with strenuous "
                "exercise) to Grade 4 (too dyspneic to leave house or breathless when dressing). This validated tool "
                "has high inter-rater reliability (98%) and correlates with health-related quality of life measures. "
                "It is widely used in COPD assessment as part of GOLD guidelines and as a component of the BODE Index "
                "for prognosis. The scale helps clinicians assess baseline functional impairment and monitor disease "
                "progression in patients with respiratory conditions.",
    response_description="mMRC dyspnea grade with functional limitation assessment and clinical interpretation",
    operation_id="mmrc_dyspnea_scale"
)
async def calculate_mmrc_dyspnea_scale(request: MmrcDyspneaScaleRequest):
    """
    Calculates mMRC (Modified Medical Research Council) Dyspnea Scale
    
    Assesses the degree of baseline functional disability due to dyspnea
    in patients with respiratory diseases, particularly COPD.
    
    Args:
        request: Patient's dyspnea grade based on functional limitation
        
    Returns:
        MmrcDyspneaScaleResponse: Grade with functional disability assessment
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mmrc_dyspnea_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating mMRC Dyspnea Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return MmrcDyspneaScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for mMRC Dyspnea Scale",
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