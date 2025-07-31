"""
Apfel Score for Postoperative Nausea and Vomiting Router

Endpoint for calculating Apfel Score for PONV risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.anesthesiology.apfel_score_ponv import (
    ApfelScorePonvRequest,
    ApfelScorePonvResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/apfel_score_ponv", response_model=ApfelScorePonvResponse, summary="Calculate Apfel Score for PONV", description="Calculates Apfel Score for Postoperative Nausea and Vomiting", response_description="Apfel Score result with clinical interpretation and prophylactic recommendations", operation_id="apfel_score_ponv")
async def calculate_apfel_score_ponv(request: ApfelScorePonvRequest):
    """
    Calculates Apfel Score for Postoperative Nausea and Vomiting
    
    The Apfel Score is one of the most widely validated and used risk assessment tools 
    for postoperative nausea and vomiting (PONV). It uses four simple clinical factors 
    to predict 24-hour PONV risk and guide prophylactic antiemetic therapy decisions:
    
    - Female gender (1 point)
    - Non-smoking status (1 point)
    - History of motion sickness or PONV (1 point)
    - Use of postoperative opioids (1 point)
    
    Score ranges from 0-4 points with corresponding PONV risk:
    - 0 points: ~10% risk (Very Low Risk)
    - 1 point: ~20% risk (Low Risk)
    - 2 points: ~40% risk (Moderate Risk)
    - 3 points: ~60% risk (High Risk)
    - 4 points: ~80% risk (Very High Risk)
    
    Args:
        request: Parameters needed for Apfel Score calculation
        
    Returns:
        ApfelScorePonvResponse: Result with clinical interpretation and prophylactic recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("apfel_score_ponv", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Apfel Score for PONV",
                    "details": {"parameters": parameters}
                }
            )
        
        return ApfelScorePonvResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Apfel Score for PONV",
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
