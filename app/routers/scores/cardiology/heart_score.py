"""
HEART Score Router

Endpoint for calculating HEART Score for Major Cardiac Events.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.heart_score import (
    HeartScoreRequest,
    HeartScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/heart_score",
    response_model=HeartScoreResponse,
    summary="Calculate HEART Score for Major Cardiac Events",
    description="Calculates the HEART Score to predict 6-week risk of major adverse cardiac events (MACE) "
                "in patients presenting to the emergency department with chest pain. The score evaluates "
                "5 components: History, EKG, Age, Risk factors, and Troponin. Low-risk patients (0-3 points) "
                "have <2% MACE risk and can be safely discharged. Moderate-risk patients (4-6 points) have "
                "12-17% MACE risk and require observation. High-risk patients (7-10 points) have 50-65% "
                "MACE risk and may benefit from early invasive strategies. Superior to TIMI and GRACE scores "
                "with c-statistic of 0.83.",
    response_description="The calculated HEART score with risk stratification and disposition recommendations",
    operation_id="heart_score"
)
async def calculate_heart_score(request: HeartScoreRequest):
    """
    Calculates HEART Score for Major Cardiac Events
    
    The HEART Score helps risk-stratify chest pain patients in the ED
    to guide disposition decisions and identify those needing urgent
    cardiac intervention.
    
    Args:
        request: Parameters for HEART score components
        
    Returns:
        HeartScoreResponse: Result with risk stratification and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("heart_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HEART Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return HeartScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HEART Score",
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