"""
Duke Activity Status Index (DASI) Router

Endpoint for calculating Duke Activity Status Index.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.duke_activity_status_index import (
    DukeActivityStatusIndexRequest,
    DukeActivityStatusIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/duke_activity_status_index", response_model=DukeActivityStatusIndexResponse)
async def calculate_duke_activity_status_index(request: DukeActivityStatusIndexRequest):
    """
    Calculates Duke Activity Status Index (DASI)
    
    Estimates functional capacity through assessment of 12 daily activities.
    Each activity has a specific weight based on its metabolic cost (MET value).
    The DASI score ranges from 0 to 58.2 points and correlates with VO2 max
    and estimated METs from cardiopulmonary exercise testing.
    
    Args:
        request: Parameters needed for calculation (12 activity parameters)
        
    Returns:
        DukeActivityStatusIndexResponse: Result with clinical interpretation and estimated METs
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("duke_activity_status_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Duke Activity Status Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return DukeActivityStatusIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Duke Activity Status Index",
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