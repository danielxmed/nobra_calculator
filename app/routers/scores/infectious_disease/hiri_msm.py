"""
HIV Incidence Risk Index for MSM (HIRI-MSM) Router

Endpoint for calculating HIRI-MSM score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.infectious_disease.hiri_msm import (
    HiriMsmRequest,
    HiriMsmResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hiri_msm",
    response_model=HiriMsmResponse,
    summary="Calculate HIV Incidence Risk Index for MSM (HIRI-MSM)",
    description="Calculates the HIV Incidence Risk Index for men who have sex with men (MSM) to "
                "identify those at high risk for HIV infection. This CDC-developed 7-item screening "
                "tool evaluates behavioral and demographic risk factors over the past 6 months. "
                "A score ≥10 indicates high risk and helps prioritize candidates for pre-exposure "
                "prophylaxis (PrEP) and other intensive HIV prevention interventions. The tool has "
                "84% sensitivity and 45% specificity for predicting incident HIV infection.",
    response_description="The calculated HIRI-MSM score with risk category and prevention recommendations",
    operation_id="hiri_msm"
)
async def calculate_hiri_msm(request: HiriMsmRequest):
    """
    Calculates HIV Incidence Risk Index for MSM (HIRI-MSM)
    
    The HIRI-MSM helps healthcare providers identify MSM who would benefit most 
    from intensive HIV prevention interventions, particularly PrEP initiation.
    
    Args:
        request: Behavioral and demographic risk factors assessed over past 6 months
        
    Returns:
        HiriMsmResponse: Risk score with category and prevention recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hiri_msm", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HIRI-MSM score",
                    "details": {"parameters": parameters}
                }
            )
        
        return HiriMsmResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HIRI-MSM score",
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