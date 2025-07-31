"""
Ottawa Heart Failure Risk Scale (OHFRS) Router

Endpoint for calculating Ottawa Heart Failure Risk Scale.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.ottawa_heart_failure_risk_scale import (
    OttawaHeartFailureRiskScaleRequest,
    OttawaHeartFailureRiskScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ottawa_heart_failure_risk_scale",
    response_model=OttawaHeartFailureRiskScaleResponse,
    summary="Calculate Ottawa Heart Failure Risk Scale (OHFRS)",
    description="Identifies emergency department heart failure patients at high risk for serious adverse events. Uses 10 clinical variables to stratify risk from low (2.8%) to very high (89%+).",
    response_description="The calculated ottawa heart failure risk scale with interpretation",
    operation_id="ottawa_heart_failure_risk_scale"
)
async def calculate_ottawa_heart_failure_risk_scale(request: OttawaHeartFailureRiskScaleRequest):
    """
    Calculates Ottawa Heart Failure Risk Scale (OHFRS)
    
    Identifies emergency department heart failure patients at high risk for serious 
    adverse events. High sensitivity (91.8-95.8%) for detecting patients at risk 
    within 14 days.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        OttawaHeartFailureRiskScaleResponse: Result with risk stratification
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ottawa_heart_failure_risk_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Ottawa Heart Failure Risk Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return OttawaHeartFailureRiskScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Ottawa Heart Failure Risk Scale",
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