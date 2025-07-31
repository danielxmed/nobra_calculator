"""
FeverPAIN Score for Strep Pharyngitis Router

Endpoint for calculating FeverPAIN Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.infectious_disease.feverpain_score import (
    FeverpainScoreRequest,
    FeverpainScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/feverpain_score",
    response_model=FeverpainScoreResponse,
    summary="Calculate FeverPAIN Score for Strep Pharyngitis",
    description="Predicts likelihood of streptococcal pharyngitis and guides antibiotic prescribing decisions.",
    response_description="The calculated feverpain score with interpretation",
    operation_id="feverpain_score"
)
async def calculate_feverpain_score(request: FeverpainScoreRequest):
    """
    Calculates FeverPAIN Score for Strep Pharyngitis
    
    The FeverPAIN score predicts likelihood of streptococcal pharyngitis in patients
    aged 3+ years. It helps guide antibiotic prescribing decisions and has been
    shown to reduce antibiotic use by 30% while maintaining clinical outcomes.
    
    Args:
        request: Clinical parameters for FeverPAIN calculation
        
    Returns:
        FeverpainScoreResponse: Score with strep likelihood and antibiotic guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("feverpain_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating FeverPAIN Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return FeverpainScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for FeverPAIN Score",
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