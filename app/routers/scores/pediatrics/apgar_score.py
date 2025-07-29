"""
APGAR Score Router

Endpoint for calculating APGAR Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.apgar_score import (
    ApgarScoreRequest,
    ApgarScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/apgar_score", response_model=ApgarScoreResponse)
async def calculate_apgar_score(request: ApgarScoreRequest):
    """
    Calculates APGAR Score
    
    Assesses neonatal vitality at 1 and 5 minutes after birth using 5 clinical criteria:
    Activity/muscle tone, Pulse, Grimace reflex, Appearance/color, and Respirations.
    
    The APGAR Score was developed by Dr. Virginia Apgar in 1952 and is the standard
    method for evaluating newborn health immediately after birth. Each of the five
    criteria is scored 0, 1, or 2 points, for a total possible score of 10.
    
    - Score 7-10: Normal condition, reassuring
    - Score 4-6: Moderate distress, may need assistance
    - Score 0-3: Severe distress, immediate medical attention required
    
    Args:
        request: Parameters needed for calculation including activity/muscle tone,
                pulse, grimace reflex, appearance/color, and respirations
        
    Returns:
        ApgarScoreResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("apgar_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating APGAR Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return ApgarScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for APGAR Score",
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
