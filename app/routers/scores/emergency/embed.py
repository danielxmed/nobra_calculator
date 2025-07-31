"""
Emergency Department-Initiated Buprenorphine for Opioid Use Disorder (EMBED) Router

Endpoint for calculating EMBED assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.embed import (
    EmbedRequest,
    EmbedResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/embed", response_model=EmbedResponse)
async def calculate_embed(request: EmbedRequest):
    """
    Calculates Emergency Department-Initiated Buprenorphine (EMBED) Assessment
    
    Assesses opioid use disorder using DSM-5 criteria, evaluates withdrawal severity 
    with the Clinical Opiate Withdrawal Scale (COWS), and determines patient readiness 
    for ED-initiated buprenorphine treatment. Provides evidence-based recommendations 
    for buprenorphine induction approach.
    
    Args:
        request: Parameters needed for assessment including DSM-5 criteria, COWS score, 
                treatment readiness, and clinical factors
        
    Returns:
        EmbedResponse: Assessment result with treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("embed", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating EMBED assessment",
                    "details": {"parameters": parameters}
                }
            )
        
        return EmbedResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for EMBED assessment",
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
                "message": "Internal error in assessment",
                "details": {"error": str(e)}
            }
        )