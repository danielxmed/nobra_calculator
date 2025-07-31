"""
FUNC Score Router

Endpoint for calculating Functional Outcome in Patients With Primary ICH (FUNC) Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.func_score import (
    FuncScoreRequest,
    FuncScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/func_score",
    response_model=FuncScoreResponse,
    summary="Calculate Functional Outcome in Patients With Primary Int...",
    description="Identifies patients with intracerebral hemorrhage (ICH) who will achieve functional independence at 90 days and aids in clinical decision-making and goals of care discussions.",
    response_description="The calculated func score with interpretation",
    operation_id="calculate_func_score"
)
async def calculate_func_score(request: FuncScoreRequest):
    """
    Calculates FUNC Score for Primary Intracerebral Hemorrhage
    
    Predicts likelihood of achieving functional independence (Glasgow Outcome Score ≥4) 
    at 90 days following primary ICH. Uses ICH volume, age, location, GCS, and 
    pre-ICH cognitive status to provide prognostic guidance.
    
    Args:
        request: Parameters including ICH volume, age, location, GCS, and cognitive status
        
    Returns:
        FuncScoreResponse: Score (0-11 points) with prognosis and care recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("func_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating FUNC Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return FuncScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for FUNC Score",
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