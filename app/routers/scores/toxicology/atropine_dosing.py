"""
Atropine Dosing for Cholinesterase Inhibitor Toxicity Router

Endpoint for calculating atropine dosing for cholinesterase inhibitor toxicity.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.toxicology.atropine_dosing import (
    AtropineDosingRequest,
    AtropineDosingResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/atropine_dosing", response_model=AtropineDosingResponse)
async def calculate_atropine_dosing(request: AtropineDosingRequest):
    """
    Calculates Atropine Dosing for Cholinesterase Inhibitor Toxicity
    
    Doses atropine for cholinesterase inhibitor toxicity from prescription drugs, 
    nerve gas, or insecticides. Provides initial dosing recommendations based on 
    patient type (adult/pediatric) and severity, along with escalation protocol 
    and continuous infusion calculations.
    
    Args:
        request: Parameters including patient type, severity, and weight (if pediatric)
        
    Returns:
        AtropineDosingResponse: Complete dosing recommendations with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("atropine_dosing", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Atropine Dosing",
                    "details": {"parameters": parameters}
                }
            )
        
        return AtropineDosingResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Atropine Dosing",
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