"""
FRACTURE Index Router

Endpoint for calculating FRACTURE Index.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.fracture_index import (
    FractureIndexRequest,
    FractureIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/fracture_index",
    response_model=FractureIndexResponse,
    summary="Calculate FRACTURE Index",
    description="Predicts 5-year hip fracture risk in postmenopausal women using clinical risk factors with or without bone mineral density measurements.",
    response_description="The calculated fracture index with interpretation",
    operation_id="fracture_index"
)
async def calculate_fracture_index(request: FractureIndexRequest):
    """
    Calculates FRACTURE Index
    
    Predicts 5-year hip fracture risk in postmenopausal women using clinical risk 
    factors with or without bone mineral density measurements.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        FractureIndexResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("fracture_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating FRACTURE Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return FractureIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for FRACTURE Index",
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