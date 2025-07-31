"""
DIRE Score for Opioid Treatment Router

Endpoint for calculating DIRE Score for assessing opioid treatment suitability.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.dire_score import (
    DireScoreRequest,
    DireScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/dire_score", response_model=DireScoreResponse)
async def calculate_dire_score(request: DireScoreRequest):
    """
    Calculates DIRE Score for Opioid Treatment
    
    Predicts compliance with opioid treatment for chronic non-cancer pain by 
    evaluating six domains: diagnosis severity, treatment intractability, 
    psychological risk, chemical health risk, reliability risk, and social 
    support risk. Each domain is scored 1-3 points (total range 7-21).
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        DireScoreResponse: Suitability assessment with clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("dire_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating DIRE Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return DireScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for DIRE Score",
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