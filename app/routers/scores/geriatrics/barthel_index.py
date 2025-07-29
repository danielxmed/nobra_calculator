"""
Barthel Index for Activities of Daily Living (ADL) Router

Endpoint for calculating Barthel Index for functional independence assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.geriatrics.barthel_index import (
    BarthelIndexRequest,
    BarthelIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/barthel_index", response_model=BarthelIndexResponse)
async def calculate_barthel_index(request: BarthelIndexRequest):
    """
    Calculates Barthel Index for Activities of Daily Living (ADL)
    
    The Barthel Index is the most widely used assessment tool for measuring 
    performance in basic activities of daily living. It evaluates 10 activities 
    to determine functional independence, with scores ranging from 0 (totally 
    dependent) to 100 (fully independent). Particularly useful in rehabilitation 
    settings and for monitoring functional recovery in stroke patients.
    
    Args:
        request: Parameters for 10 activities of daily living
        
    Returns:
        BarthelIndexResponse: Total score with functional independence assessment
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("barthel_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Barthel Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return BarthelIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Barthel Index",
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