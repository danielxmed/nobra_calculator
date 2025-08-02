"""
HITS (Hurt, Insult, Threaten, Scream) Score Router

Endpoint for HITS intimate partner violence screening.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.hits_score import (
    HitsScoreRequest,
    HitsScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hits_score",
    response_model=HitsScoreResponse,
    summary="Calculate HITS (Hurt, Insult, Threaten, Scream) Score",
    description="Screens for intimate partner violence in both women and men using a validated "
                "4-question frequency-based tool. The HITS instrument assesses how often partners "
                "engage in four types of abusive behaviors: physically Hurt, Insult/talk down, "
                "Threaten with harm, and Scream/curse. Each question is rated on a 5-point frequency "
                "scale from 'never' (1 point) to 'frequently' (5 points), with total scores ranging "
                "from 4-20. A score ≥11 indicates a positive screen requiring immediate safety "
                "assessment, documentation, resource provision, and follow-up care planning. This "
                "brief screening tool demonstrates good psychometric properties with internal "
                "consistency (α=0.80) and correlates well with the Conflict Tactics Scale (r=0.85), "
                "making it suitable for busy healthcare settings.",
    response_description="The calculated HITS score with screening result, identified abuse "
                        "behaviors, and safety assessment requirements",
    operation_id="hits_score"
)
async def calculate_hits_score(request: HitsScoreRequest):
    """
    Calculates HITS (Hurt, Insult, Threaten, Scream) Score
    
    Performs intimate partner violence screening using four frequency-based questions 
    that assess different types of abusive behaviors by current or former partners.
    
    Args:
        request: Four frequency questions about intimate partner violence behaviors
        
    Returns:
        HitsScoreResponse: Score (4-20) with screening result and safety assessment requirements
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hits_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HITS score",
                    "details": {"parameters": parameters}
                }
            )
        
        return HitsScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HITS score calculation",
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