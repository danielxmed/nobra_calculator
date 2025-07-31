"""
Canadian Transient Ischemic Attack (TIA) Score Router

Endpoint for calculating Canadian TIA Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.canadian_tia_score import (
    CanadianTiaScoreRequest,
    CanadianTiaScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/canadian_tia_score",
    response_model=CanadianTiaScoreResponse,
    summary="Calculate Canadian Transient Ischemic Attack (TIA) Score",
    description="The Canadian TIA Score identifies risk of stroke, carotid endarterectomy, or carotid artery stenting within 7 days in patients who experienced TIA symptoms. It incorporates 13 predictive variables from history, physical examination, and testing routinely performed in the emergency department.",
    response_description="The calculated canadian tia score with interpretation",
    operation_id="canadian_tia_score"
)
async def calculate_canadian_tia_score(request: CanadianTiaScoreRequest):
    """
    Calculates Canadian Transient Ischemic Attack (TIA) Score
    
    The Canadian TIA Score identifies risk of stroke, carotid endarterectomy, 
    or carotid artery stenting within 7 days in patients who experienced TIA symptoms.
    It is more accurate than ABCD² and ABCD²I scores for 7-day risk prediction.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        CanadianTiaScoreResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("canadian_tia_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Canadian TIA Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CanadianTiaScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Canadian TIA Score",
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