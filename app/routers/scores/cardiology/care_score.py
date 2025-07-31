"""
Cardiac Anesthesia Risk Evaluation Score (CARE) Router

Endpoint for calculating CARE Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.care_score import (
    CareScoreRequest,
    CareScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/care_score",
    response_model=CareScoreResponse,
    summary="Calculate Cardiac Anesthesia Risk Evaluation Sc...",
    description="The CARE Score predicts mortality and morbidity after cardiac surgery. It is a simple risk classification based on clinical judgment and three clinical variables: comorbid conditions (controlled vs uncontrolled), surgical complexity, and urgency of the procedure.",
    response_description="The calculated care score with interpretation",
    operation_id="care_score"
)
async def calculate_care_score(request: CareScoreRequest):
    """
    Calculates Cardiac Anesthesia Risk Evaluation Score (CARE)
    
    The CARE Score predicts mortality and morbidity after cardiac surgery using 
    a simple clinical assessment. It demonstrates excellent predictive performance 
    with an AUC of 0.801 for mortality prediction.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        CareScoreResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("care_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CARE Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CareScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CARE Score",
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