"""
HEADS-ED Router

Endpoint for calculating HEADS-ED pediatric mental health screening score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.heads_ed import (
    HeadsEdRequest,
    HeadsEdResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/heads_ed",
    response_model=HeadsEdResponse,
    summary="Calculate HEADS-ED Score",
    description="Calculates the HEADS-ED score for pediatric mental health screening in the emergency department. "
                "This validated screening tool evaluates 7 domains (Home, Education, Activities/peers, Drugs/alcohol, "
                "Suicidality, Emotions/behaviors, Discharge resources) to identify mental health needs and guide "
                "referral decisions. Each domain is scored 0-2, with total scores ≥8 or suicidality score of 2 "
                "indicating need for psychiatric consultation. Designed for pediatric patients (ages 0-17) presenting "
                "to the emergency department with mental health concerns.",
    response_description="The calculated HEADS-ED score with risk stratification and consultation recommendations",
    operation_id="heads_ed"
)
async def calculate_heads_ed(request: HeadsEdRequest):
    """
    Calculates HEADS-ED pediatric mental health screening score
    
    The HEADS-ED is a rapid screening tool that helps identify mental health
    needs in pediatric emergency department patients and guide appropriate
    referrals and interventions.
    
    Args:
        request: Parameters for each of the 7 HEADS-ED domains
        
    Returns:
        HeadsEdResponse: Result with clinical interpretation and consultation recommendation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("heads_ed", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HEADS-ED score",
                    "details": {"parameters": parameters}
                }
            )
        
        return HeadsEdResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HEADS-ED score",
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