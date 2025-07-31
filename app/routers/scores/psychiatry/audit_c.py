"""
AUDIT-C for Alcohol Use Router

Endpoint for calculating AUDIT-C alcohol screening score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.audit_c import (
    AuditCRequest,
    AuditCResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/audit_c",
    response_model=AuditCResponse,
    summary="Calculate AUDIT-C for Alcohol Use",
    description="Identifies at-risk drinkers (i.e., binge drinking) who may not be alcohol dependent. A brief 3-question alcohol screen derived from the full AUDIT questionnaire.",
    response_description="The calculated audit c with interpretation",
    operation_id="calculate_audit_c"
)
async def calculate_audit_c(request: AuditCRequest):
    """
    Calculates AUDIT-C for Alcohol Use
    
    Identifies at-risk drinkers who may not be alcohol dependent using a brief 
    3-question screening tool. Scores ≥4 for males and ≥3 for females suggest 
    alcohol misuse. Higher scores indicate greater severity.
    
    Args:
        request: Parameters including alcohol consumption patterns and sex
        
    Returns:
        AuditCResponse: Score (0-12) with interpretation based on sex-specific cutoffs
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("audit_c", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating AUDIT-C score",
                    "details": {"parameters": parameters}
                }
            )
        
        return AuditCResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for AUDIT-C",
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