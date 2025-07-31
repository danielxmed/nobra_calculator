"""
Abbreviated Mental Test (AMT-10) Router

Endpoint for calculating AMT-10.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.geriatrics.amt_10 import (
    Amt10Request,
    Amt10Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/amt_10",
    response_model=Amt10Response,
    summary="Calculate Abbreviated Mental Test (AMT-10)",
    description="Assesses mental impairment in elderly patients through 10 questions evaluating various aspects of cognitive function including memory, attention, and orientation",
    response_description="The calculated amt 10 with interpretation",
    operation_id="calculate_amt_10"
)
async def calculate_amt_10(request: Amt10Request):
    """
    Calculates Abbreviated Mental Test (AMT-10)
    
    Assesses mental impairment in elderly patients through 10 questions evaluating 
    various aspects of cognitive function including memory, attention, and orientation.
    A score of <8 suggests cognitive impairment; <6 suggests delirium or dementia.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        Amt10Response: Result with clinical interpretation
    """
    try:
        parameters = request.dict()
        
        result = calculator_service.calculate_score("amt_10", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating AMT-10",
                    "details": {"parameters": parameters}
                }
            )
        
        return Amt10Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for AMT-10",
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