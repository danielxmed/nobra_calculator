"""
Kt/V for Dialysis Adequacy Router

Endpoint for calculating Kt/V dialysis adequacy using the Daugirdas second-generation equation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.ktv_dialysis_adequacy import (
    KtvDialysisAdequacyRequest,
    KtvDialysisAdequacyResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ktv_dialysis_adequacy",
    response_model=KtvDialysisAdequacyResponse,
    summary="Calculate Kt/V for Dialysis Adequacy",
    description="Calculates the Kt/V for dialysis adequacy using the Daugirdas second-generation equation. "
                "This validated clinical tool quantifies the adequacy of both hemodialysis and peritoneal "
                "dialysis treatment by assessing urea clearance. The calculation provides critical guidance "
                "for optimizing dialysis prescriptions and monitoring treatment effectiveness. "
                "Hemodialysis target Kt/V ≥1.3 per session; peritoneal dialysis target Kt/V ≥1.7 per week.",
    response_description="The calculated Kt/V value with adequacy assessment, urea reduction ratio, and clinical recommendations for dialysis optimization",
    operation_id="ktv_dialysis_adequacy"
)
async def calculate_ktv_dialysis_adequacy(request: KtvDialysisAdequacyRequest):
    """
    Calculates Kt/V for Dialysis Adequacy
    
    The Kt/V calculation quantifies dialysis adequacy by measuring the fractional 
    clearance of urea from the body during a dialysis session. It uses the validated 
    Daugirdas second-generation equation that accounts for urea generation during 
    treatment and convective clearance from ultrafiltration.
    
    Clinical Applications:
    - Monthly monitoring for hemodialysis patients
    - Quarterly assessment for peritoneal dialysis patients
    - Optimization of dialysis prescriptions
    - Correlation with patient survival and morbidity outcomes
    
    Args:
        request: Parameters including pre/post-dialysis BUN, treatment time, 
                ultrafiltration volume, post-dialysis weight, and dialysis type
        
    Returns:
        KtvDialysisAdequacyResponse: Kt/V result with adequacy assessment and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ktv_dialysis_adequacy", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Kt/V for Dialysis Adequacy",
                    "details": {"parameters": parameters}
                }
            )
        
        return KtvDialysisAdequacyResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Kt/V Dialysis Adequacy calculation",
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
                "message": "Internal error in Kt/V calculation",
                "details": {"error": str(e)}
            }
        )