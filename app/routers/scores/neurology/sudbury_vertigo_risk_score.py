"""
Sudbury Vertigo Risk Score Router

Endpoint for calculating Sudbury Vertigo Risk Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.sudbury_vertigo_risk_score import (
    SudburyVertigoRiskScoreRequest,
    SudburyVertigoRiskScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/sudbury_vertigo_risk_score",
    response_model=SudburyVertigoRiskScoreResponse,
    summary="Calculate Sudbury Vertigo Risk Score",
    description="Identifies vertigo patients at higher risk for serious central diagnosis including stroke, TIA, "
                "vertebral artery dissection, or brain tumor in the emergency department. Uses 7 clinical variables "
                "to stratify patients into risk categories. A score <5 has 100% sensitivity for ruling out serious "
                "causes of vertigo. The score ranges from -4 to 17 points, with higher scores indicating greater risk.",
    response_description="The calculated Sudbury Vertigo Risk Score with risk stratification and clinical recommendations",
    operation_id="sudbury_vertigo_risk_score"
)
async def calculate_sudbury_vertigo_risk_score(request: SudburyVertigoRiskScoreRequest):
    """
    Calculates Sudbury Vertigo Risk Score
    
    The Sudbury Vertigo Risk Score is a clinical decision tool designed to help identify 
    patients at risk for serious causes of vertigo in the emergency department setting.
    It stratifies patients into low, moderate, and high risk categories for serious 
    central causes of vertigo.
    
    Args:
        request: Parameters for score calculation including demographics, risk factors,
                and clinical findings
        
    Returns:
        SudburyVertigoRiskScoreResponse: Calculated score with risk stratification
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("sudbury_vertigo_risk_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Sudbury Vertigo Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return SudburyVertigoRiskScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Sudbury Vertigo Risk Score",
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