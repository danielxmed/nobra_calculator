"""
NEXUS Chest Decision Instrument for Blunt Chest Trauma Router

Endpoint for calculating NEXUS Chest score for blunt trauma.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.nexus_chest_blunt_trauma import (
    NexusChestBluntTraumaRequest,
    NexusChestBluntTraumaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/nexus_chest_blunt_trauma",
    response_model=NexusChestBluntTraumaResponse,
    summary="Calculate NEXUS Chest Decision Instrument for Blunt Chest...",
    description="Determines need for chest imaging in blunt trauma patients. Uses 7 criteria to identify patients at very low risk for thoracic injury who can potentially avoid chest x-ray. The score is 99% sensitive for clinically significant thoracic injury.",
    response_description="The calculated nexus chest blunt trauma with interpretation",
    operation_id="calculate_nexus_chest_blunt_trauma"
)
async def calculate_nexus_chest_blunt_trauma(request: NexusChestBluntTraumaRequest):
    """
    Calculates NEXUS Chest Decision Instrument for Blunt Chest Trauma
    
    Determines need for chest imaging in blunt trauma patients using 7 criteria.
    The score is 99% sensitive for clinically significant thoracic injury.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        NexusChestBluntTraumaResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("nexus_chest_blunt_trauma", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating NEXUS Chest score",
                    "details": {"parameters": parameters}
                }
            )
        
        return NexusChestBluntTraumaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for NEXUS Chest score",
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