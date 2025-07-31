"""
ASTRAL Score for Ischemic Stroke Router

Endpoint for calculating ASTRAL Score for predicting 90-day poor outcome 
in patients with acute ischemic stroke.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.astral_score import (
    AstralScoreRequest,
    AstralScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/astral_score",
    response_model=AstralScoreResponse,
    summary="Calculate ASTRAL Score for Ischemic Stroke",
    description="Predicts 90-day poor outcome (mRS >2) in patients with acute ischemic stroke. The score combines age, NIHSS, timing, visual defects, glucose levels, and consciousness to stratify prognosis.",
    response_description="The calculated astral score with interpretation",
    operation_id="astral_score"
)
async def calculate_astral_score(request: AstralScoreRequest):
    """
    Calculates ASTRAL Score for Ischemic Stroke
    
    Predicts 90-day poor outcome (mRS >2) in patients with acute ischemic stroke.
    The ASTRAL score combines age, NIHSS score, time from onset to admission, 
    visual field defects, glucose abnormalities, and consciousness level to 
    stratify prognosis.
    
    **Clinical Use:**
    - Use only in patients admitted within 24 hours of stroke onset
    - Score should only be used for patients with pre-stroke independence (mRS 0-2)
    - Poor outcome defined as modified Rankin Scale (mRS) >2 at 90 days
    - Use in conjunction with clinical judgment, not as sole decision-making tool
    
    **Score Interpretation:**
    - 0-15 points: Low risk (better prognosis for functional independence)
    - 16-25 points: Moderate risk (requires careful monitoring and rehabilitation)
    - ≥26 points: High risk (significant disability/death risk, consider palliative care)
    
    Args:
        request: ASTRAL score parameters including age, NIHSS, timing, visual defects, 
                glucose abnormalities, and consciousness level
        
    Returns:
        AstralScoreResponse: Calculated score with clinical interpretation and risk stratification
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("astral_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ASTRAL Score for Ischemic Stroke",
                    "details": {"parameters": parameters}
                }
            )
        
        return AstralScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ASTRAL Score",
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
                "message": "Internal error in ASTRAL Score calculation",
                "details": {"error": str(e)}
            }
        )
