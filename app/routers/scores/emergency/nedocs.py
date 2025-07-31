"""
NEDOCS Score for Emergency Department Overcrowding Router

Endpoint for calculating NEDOCS Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.nedocs import (
    NedocsRequest,
    NedocsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/nedocs", response_model=NedocsResponse)
async def calculate_nedocs(request: NedocsRequest):
    """
    Calculates NEDOCS Score for Emergency Department Overcrowding
    
    Uses 7 objective parameters to estimate the severity of overcrowding in 
    emergency departments. The score ranges from 1-200 with 6 levels of 
    interpretation from "Not busy" to "Dangerously overcrowded".
    
    Args:
        request: Parameters needed for calculation including ED capacity,
                patient volumes, and wait times
        
    Returns:
        NedocsResponse: Result with overcrowding level interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("nedocs", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating NEDOCS Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return NedocsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for NEDOCS Score",
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