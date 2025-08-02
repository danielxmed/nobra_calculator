"""
Urticaria Activity Score (UAS) Router

Endpoint for calculating Urticaria Activity Score (UAS).
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.dermatology.urticaria_activity_score import (
    UrticariaActivityScoreRequest,
    UrticariaActivityScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/urticaria_activity_score",
    response_model=UrticariaActivityScoreResponse,
    summary="Calculate Urticaria Activity Score (UAS)",
    description="Calculates the Urticaria Activity Score (UAS7) for stratifying severity of chronic spontaneous urticaria. "
                "This diary-based assessment tool evaluates wheals (hives) and itch intensity over 7 consecutive days. "
                "The UAS7 score ranges from 0-42 and helps monitor disease activity, assess treatment response, and guide "
                "therapeutic decisions. Scores <7 indicate adequate control, 7-15 suggest mild activity, 16-27 moderate activity, "
                "and >28 severe activity requiring intensive management. The UAS is recommended by international guidelines "
                "and is the primary endpoint in chronic urticaria clinical trials.",
    response_description="The calculated UAS7 score with clinical interpretation, severity classification, and daily score breakdown",
    operation_id="urticaria_activity_score"
)
async def calculate_urticaria_activity_score(request: UrticariaActivityScoreRequest):
    """
    Calculates Urticaria Activity Score (UAS)
    
    Stratifies severity of chronic spontaneous urticaria through diary-based assessment 
    of wheals and itch intensity over 7 consecutive days.
    
    Args:
        request: Daily scores for wheals and itch (0-3 each) for 7 consecutive days
        
    Returns:
        UrticariaActivityScoreResponse: UAS7 result with clinical interpretation and severity classification
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("urticaria_activity_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Urticaria Activity Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return UrticariaActivityScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Urticaria Activity Score",
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