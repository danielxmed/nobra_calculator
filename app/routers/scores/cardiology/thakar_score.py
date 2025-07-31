"""
Thakar Score Router

Endpoint for calculating Thakar Score (Acute Renal Failure after Cardiac Surgery).
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.thakar_score import (
    ThakarScoreRequest,
    ThakarScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/thakar_score", 
    response_model=ThakarScoreResponse,
    summary="Calculate Thakar Score for AKI Risk",
    description="Predicts risk of acute kidney injury (AKI) requiring dialysis after cardiac surgery. "
                "The score was developed and validated in over 33,000 patients at the Cleveland Clinic Foundation "
                "and stratifies patients into five risk categories from very low (0.3-0.5%) to very high (>22%) risk.",
    response_description="The calculated Thakar score with risk stratification and clinical recommendations",
    operation_id="calculate_thakar_score"
)
async def calculate_thakar_score(request: ThakarScoreRequest):
    """
    Calculates Thakar Score for Acute Renal Failure after Cardiac Surgery
    
    Predicts risk of acute kidney injury (AKI) requiring dialysis after cardiac surgery.
    The score was developed and validated in over 33,000 patients at the Cleveland 
    Clinic Foundation and ranges from 0-17 points, stratifying patients into risk 
    categories from very low (0.3-0.5% risk) to very high (>22% risk).
    
    Args:
        request: Parameters needed for calculation including patient demographics,
                cardiac factors, comorbidities, surgical factors, and laboratory values
        
    Returns:
        ThakarScoreResponse: Result with clinical interpretation and risk stratification
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("thakar_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Thakar Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return ThakarScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Thakar Score",
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