"""
Barnes Jewish Hospital Stroke Dysphagia Screen Router

Endpoint for calculating Barnes Jewish Hospital dysphagia screen for stroke patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.barnes_jewish_dysphagia import (
    BarnesJewishDysphagiaRequest,
    BarnesJewishDysphagiaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/barnes_jewish_dysphagia", response_model=BarnesJewishDysphagiaResponse)
async def calculate_barnes_jewish_dysphagia(request: BarnesJewishDysphagiaRequest):
    """
    Calculates Barnes Jewish Hospital Stroke Dysphagia Screen
    
    This validated bedside screening tool helps identify stroke patients at 
    risk for dysphagia and aspiration. It consists of preliminary neurological 
    screening questions followed by a water swallow test if the preliminary 
    screen is passed. Designed for use by non-speech pathology trained 
    healthcare professionals.
    
    Args:
        request: Parameters including neurological assessment and water test results
        
    Returns:
        BarnesJewishDysphagiaResponse: Pass/Fail result with clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("barnes_jewish_dysphagia", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Barnes Jewish dysphagia screen",
                    "details": {"parameters": parameters}
                }
            )
        
        return BarnesJewishDysphagiaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Barnes Jewish dysphagia screen",
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