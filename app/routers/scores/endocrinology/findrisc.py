"""
FINDRISC (Finnish Diabetes Risk Score) Router

Endpoint for calculating FINDRISC.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.findrisc import (
    FindriscRequest,
    FindriscResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/findrisc",
    response_model=FindriscResponse,
    summary="Calculate FINDRISC (Finnish Diabetes Risk Score)",
    description="Identifies patients at high risk for type 2 diabetes within 10 years without the need for laboratory tests",
    response_description="The calculated findrisc with interpretation",
    operation_id="calculate_findrisc"
)
async def calculate_findrisc(request: FindriscRequest):
    """
    Calculates FINDRISC (Finnish Diabetes Risk Score)
    
    Identifies patients at high risk for type 2 diabetes within 10 years 
    without the need for laboratory tests.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        FindriscResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("findrisc", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating FINDRISC",
                    "details": {"parameters": parameters}
                }
            )
        
        return FindriscResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for FINDRISC",
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