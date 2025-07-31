"""
NEXUS Chest CT Decision Instrument Router

Endpoint for calculating NEXUS Chest CT score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.nexus_chest_ct import (
    NexusChestCtRequest,
    NexusChestCtResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/nexus_chest_ct", response_model=NexusChestCtResponse)
async def calculate_nexus_chest_ct(request: NexusChestCtRequest):
    """
    Calculates NEXUS Chest CT Decision Instrument
    
    Identifies blunt trauma patients with clinically significant chest injuries
    requiring CT chest imaging. Uses 7 criteria to determine need for CT.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        NexusChestCtResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("nexus_chest_ct", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating NEXUS Chest CT score",
                    "details": {"parameters": parameters}
                }
            )
        
        return NexusChestCtResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for NEXUS Chest CT score",
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