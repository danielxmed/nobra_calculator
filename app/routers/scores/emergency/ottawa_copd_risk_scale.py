"""
Ottawa COPD Risk Scale Router

Endpoint for calculating Ottawa COPD Risk Scale.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.ottawa_copd_risk_scale import (
    OttawaCopdRiskScaleRequest,
    OttawaCopdRiskScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ottawa_copd_risk_scale",
    response_model=OttawaCopdRiskScaleResponse,
    summary="Calculate Ottawa COPD Risk Scale",
    description="Predicts 30-day mortality or serious adverse events (MI, intubation, etc) in emergency department COPD patients. Uses 10 clinical variables to stratify risk from low (2.2%) to very high (75.6%).",
    response_description="The calculated ottawa copd risk scale with interpretation",
    operation_id="ottawa_copd_risk_scale"
)
async def calculate_ottawa_copd_risk_scale(request: OttawaCopdRiskScaleRequest):
    """
    Calculates Ottawa COPD Risk Scale
    
    Predicts 30-day mortality or serious adverse events (MI, intubation, etc) in 
    emergency department COPD patients. Stratifies risk from low (2.2%) to very high (75.6%).
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        OttawaCopdRiskScaleResponse: Result with risk stratification
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ottawa_copd_risk_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Ottawa COPD Risk Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return OttawaCopdRiskScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Ottawa COPD Risk Scale",
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