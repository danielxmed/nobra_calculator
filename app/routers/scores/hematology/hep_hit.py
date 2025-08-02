"""
HIT Expert Probability (HEP) Score for Heparin-Induced Thrombocytopenia Router

Endpoint for calculating HEP score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.hep_hit import (
    HepHitRequest,
    HepHitResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hep_hit",
    response_model=HepHitResponse,
    summary="Calculate HIT Expert Probability (HEP) Score",
    description="Calculates the HIT Expert Probability (HEP) Score for pre-test probability of "
                "heparin-induced thrombocytopenia. This scoring model, based on broad expert opinion "
                "from 26 HIT specialists, evaluates 8 clinical features to stratify patients into "
                "low, intermediate, or high probability categories. The HEP score helps reduce "
                "unnecessary use of alternative anticoagulants and guides clinical decision-making "
                "regarding HIT workup and empiric therapy.",
    response_description="The calculated HEP score with probability category and clinical management recommendations",
    operation_id="hep_hit"
)
async def calculate_hep_hit(request: HepHitRequest):
    """
    Calculates HIT Expert Probability (HEP) Score
    
    The HEP score is a validated pre-test clinical scoring model for HIT that 
    demonstrates superior performance compared to the 4Ts score, particularly 
    for less experienced clinicians and ICU patients.
    
    Args:
        request: Clinical parameters including platelet count changes, timing, 
                thrombosis, and other HIT features
        
    Returns:
        HepHitResponse: Score with probability category and management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hep_hit", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HEP score",
                    "details": {"parameters": parameters}
                }
            )
        
        return HepHitResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HEP score",
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