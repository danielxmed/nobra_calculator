"""
Trauma Score and Injury Severity Score (TRISS) Router

Endpoint for calculating TRISS to predict survival probability in trauma patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.triss import (
    TrissRequest,
    TrissResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/triss",
    response_model=TrissResponse,
    summary="Calculate Trauma Score and Injury Severity Score (TRISS)",
    description="Calculates the probability of survival for trauma patients using TRISS methodology. "
                "Combines physiological (Revised Trauma Score) and anatomical (Injury Severity Score) "
                "indices with patient age to predict survival probability. TRISS is primarily used for "
                "quality assurance and benchmarking in trauma care systems. Different coefficients are "
                "applied for blunt versus penetrating trauma. Note: TRISS is intended for population-based "
                "outcome analysis, not individual patient prognostication.",
    response_description="The calculated probability of survival with clinical interpretation",
    operation_id="triss"
)
async def calculate_triss(request: TrissRequest):
    """
    Calculates Trauma Score and Injury Severity Score (TRISS)
    
    TRISS estimates probability of survival using physiological and anatomical 
    parameters, helping translate different severities of injuries into a 
    quantitative characterization for quality assurance and research.
    
    Args:
        request: Parameters needed for TRISS calculation
        
    Returns:
        TrissResponse: Survival probability with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("triss", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating TRISS",
                    "details": {"parameters": parameters}
                }
            )
        
        return TrissResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for TRISS calculation",
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