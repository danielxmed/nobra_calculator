"""
Abbreviated Mental Test 4 (AMT-4) Router

Endpoint for calculating AMT-4 cognitive screening score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.geriatrics.amt_4 import (
    Amt4Request,
    Amt4Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/amt_4",
    response_model=Amt4Response,
    summary="Calculate Abbreviated Mental Test 4 (AMT-4)",
    description="Assesses mental impairment and cognitive function in elderly patients using four simple questions",
    response_description="The calculated amt 4 with interpretation",
    operation_id="amt_4"
)
async def calculate_amt_4(request: Amt4Request):
    """
    Calculates Abbreviated Mental Test 4 (AMT-4)
    
    Rapid cognitive screening tool for elderly patients using four simple questions
    about age, date of birth, place, and year. Scores range from 0-4 points, with
    4/4 indicating normal cognition and <4 suggesting cognitive impairment.
    
    Args:
        request: Parameters needed for AMT-4 calculation
        
    Returns:
        Amt4Response: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("amt_4", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating AMT-4",
                    "details": {"parameters": parameters}
                }
            )
        
        return Amt4Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for AMT-4",
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