"""
Duke Treadmill Score Router

Endpoint for calculating Duke Treadmill Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.duke_treadmill_score import (
    DukeTreadmillScoreRequest,
    DukeTreadmillScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/duke_treadmill_score",
    response_model=DukeTreadmillScoreResponse,
    summary="Calculate Duke Treadmill Score",
    description="Diagnoses and prognoses suspected coronary artery disease (CAD) based on treadmill exercise test. Uses exercise time, ST deviation, and angina to predict prognosis and guide further treatment decisions.",
    response_description="The calculated duke treadmill score with interpretation",
    operation_id="duke_treadmill_score"
)
async def calculate_duke_treadmill_score(request: DukeTreadmillScoreRequest):
    """
    Calculates Duke Treadmill Score
    
    Diagnoses and prognoses suspected coronary artery disease (CAD) based on treadmill 
    exercise test. Uses exercise time, ST deviation, and angina to predict prognosis 
    and guide further treatment decisions. Provides risk stratification for cardiac 
    events and helps determine need for further testing or invasive procedures.
    
    Args:
        request: Parameters needed for calculation (exercise time, ST deviation, angina index)
        
    Returns:
        DukeTreadmillScoreResponse: Result with risk stratification and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("duke_treadmill_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Duke Treadmill Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return DukeTreadmillScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Duke Treadmill Score",
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