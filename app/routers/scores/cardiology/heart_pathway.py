"""
HEART Pathway Router

Endpoint for calculating HEART Pathway for Early Discharge in Acute Chest Pain.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.heart_pathway import (
    HeartPathwayRequest,
    HeartPathwayResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/heart_pathway",
    response_model=HeartPathwayResponse,
    summary="Calculate HEART Pathway for Early Discharge",
    description="Calculates the HEART Pathway for identifying emergency department patients with acute chest pain "
                "safe for early discharge. Combines the HEART score (History, ECG, Age, Risk factors, Troponin) "
                "with serial troponin measurements at 0 and 3 hours. Low-risk patients (HEART score ≤3) with "
                "negative serial troponins have <2% 30-day MACE risk and can be safely discharged. High-risk "
                "patients (HEART score ≥4 or positive troponin) require admission for further cardiac evaluation. "
                "Validated in multiple studies with >99% NPV for 30-day major adverse cardiac events.",
    response_description="The calculated HEART score with pathway recommendations and 30-day MACE risk stratification",
    operation_id="heart_pathway"
)
async def calculate_heart_pathway(request: HeartPathwayRequest):
    """
    Calculates HEART Pathway for early discharge decision in acute chest pain
    
    The HEART Pathway helps identify low-risk chest pain patients who can be
    safely discharged from the emergency department without admission or
    extensive cardiac testing.
    
    Args:
        request: Parameters for HEART score components and troponin results
        
    Returns:
        HeartPathwayResponse: Result with risk stratification and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("heart_pathway", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HEART Pathway",
                    "details": {"parameters": parameters}
                }
            )
        
        return HeartPathwayResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HEART Pathway",
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