"""
Canadian Syncope Risk Score Router

Endpoint for calculating Canadian Syncope Risk Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.canadian_syncope_risk_score import (
    CanadianSyncopeRiskScoreRequest,
    CanadianSyncopeRiskScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/canadian_syncope_risk_score",
    response_model=CanadianSyncopeRiskScoreResponse,
    summary="Calculate Canadian Syncope Risk Score",
    description="The Canadian Syncope Risk Score (CSRS) predicts 30-day serious adverse events in patients presenting with syncope to the emergency department. It helps identify low-risk patients who can be safely discharged and high-risk patients requiring further investigation or admission.",
    response_description="The calculated canadian syncope risk score with interpretation",
    operation_id="calculate_canadian_syncope_risk_score"
)
async def calculate_canadian_syncope_risk_score(request: CanadianSyncopeRiskScoreRequest):
    """
    Calculates Canadian Syncope Risk Score
    
    The CSRS predicts 30-day serious adverse events in patients presenting 
    with syncope to the emergency department, helping guide safe disposition decisions.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        CanadianSyncopeRiskScoreResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("canadian_syncope_risk_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Canadian Syncope Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CanadianSyncopeRiskScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Canadian Syncope Risk Score",
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