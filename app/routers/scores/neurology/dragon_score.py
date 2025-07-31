"""
DRAGON Score for Post-TPA Stroke Outcome Router

Endpoint for calculating DRAGON Score for Post-TPA Stroke Outcome.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.dragon_score import (
    DragonScoreRequest,
    DragonScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/dragon_score",
    response_model=DragonScoreResponse,
    summary="Calculate DRAGON Score for Post-TPA Stroke Outcome",
    description="Predicts 3-month outcome (functional independence vs dependency) in ischemic stroke patients treated with tissue plasminogen activator (tPA). Helps identify patients who may benefit from additional therapeutic interventions.",
    response_description="The calculated dragon score with interpretation",
    operation_id="dragon_score"
)
async def calculate_dragon_score(request: DragonScoreRequest):
    """
    Calculates DRAGON Score for Post-TPA Stroke Outcome
    
    The DRAGON score predicts 3-month functional outcome (modified Rankin Scale 0-2) 
    in ischemic stroke patients treated with intravenous tissue plasminogen activator (tPA).
    
    The acronym DRAGON stands for:
    - D: Dense cerebral artery sign or early infarct signs on CT (0-2 points)
    - R: prestroke modified Rankin Scale >1 (0-1 points)
    - A: Age (<65: 0, 65-79: 1, ≥80: 2 points)
    - G: Glucose level >144 mg/dL (0-1 points)
    - O: Onset to treatment time >90 minutes (0-1 points)
    - N: baseline NIHSS score (0-4: 0, 5-9: 1, 10-15: 2, ≥16: 3 points)
    
    Score interpretation:
    - 0-1: Excellent prognosis (96% good outcome)
    - 2: Good prognosis (88% good outcome)
    - 3: Moderate prognosis (74% good outcome)
    - 8: Very poor prognosis (0% good outcome, 70% miserable outcome)
    - 9-10: Miserable prognosis (0% good outcome, 100% miserable outcome)
    
    Args:
        request: DRAGON score parameters (6 clinical variables)
        
    Returns:
        DragonScoreResponse: DRAGON score with prognostic interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("dragon_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating DRAGON Score for Post-TPA Stroke Outcome",
                    "details": {"parameters": parameters}
                }
            )
        
        return DragonScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for DRAGON Score for Post-TPA Stroke Outcome",
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