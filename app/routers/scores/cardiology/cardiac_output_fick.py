"""
Cardiac Output (Fick's Formula) Router

Endpoint for calculating cardiac output using Fick's principle.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.cardiac_output_fick import (
    CardiacOutputFickRequest,
    CardiacOutputFickResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/cardiac_output_fick",
    response_model=CardiacOutputFickResponse,
    summary="Calculate Cardiac Output (Fick's Formula)",
    description="Calculates cardiac output, cardiac index, and stroke volume using Fick's principle. The gold standard method for measuring cardiac output based on oxygen consumption and arteriovenous oxygen difference.",
    response_description="The calculated cardiac output fick with interpretation",
    operation_id="calculate_cardiac_output_fick"
)
async def calculate_cardiac_output_fick(request: CardiacOutputFickRequest):
    """
    Calculates Cardiac Output using Fick's Formula
    
    Calculates cardiac output, cardiac index, and stroke volume using Fick's principle.
    This is the gold standard method for measuring cardiac output in clinical practice,
    requiring arterial and mixed venous blood gas measurements.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        CardiacOutputFickResponse: Result with comprehensive cardiac measurements
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cardiac_output_fick", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Cardiac Output using Fick's Formula",
                    "details": {"parameters": parameters}
                }
            )
        
        return CardiacOutputFickResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Cardiac Output (Fick's Formula)",
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