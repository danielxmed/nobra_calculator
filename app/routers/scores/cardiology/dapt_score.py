"""
Dual Antiplatelet Therapy (DAPT) Score Router

Endpoint for calculating DAPT score for prolonged dual antiplatelet therapy.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.dapt_score import (
    DaptScoreRequest,
    DaptScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/dapt_score", response_model=DaptScoreResponse)
async def calculate_dapt_score(request: DaptScoreRequest):
    """
    Calculates Dual Antiplatelet Therapy (DAPT) Score
    
    Predicts which patients will benefit from prolonged DAPT after coronary stent placement.
    Developed from the DAPT Study randomized trial to predict combined ischemic and 
    bleeding risk for patients being considered for continued thienopyridine therapy beyond 1 year.
    
    Args:
        request: DAPT score parameters
        
    Returns:
        DaptScoreResponse: Score with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("dapt_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating DAPT score",
                    "details": {"parameters": parameters}
                }
            )
        
        return DaptScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for DAPT score",
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