"""
Dutch-English LEMS Tumor Association Prediction (DELTA-P) Score Router

Endpoint for calculating DELTA-P Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.delta_p_score import (
    DeltaPScoreRequest,
    DeltaPScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/delta_p_score",
    response_model=DeltaPScoreResponse,
    summary="Calculate Dutch-English LEMS Tumor Association Prediction",
    description="Predicts small-cell lung cancer (SCLC) in patients with Lambert-Eaton myasthenic syndrome (LEMS) using clinical parameters assessed at or within 3 months of onset. The score helps identify high-risk patients requiring intensive cancer screening.",
    response_description="The calculated delta p score with interpretation",
    operation_id="calculate_delta_p_score"
)
async def calculate_delta_p_score(request: DeltaPScoreRequest):
    """
    Calculates Dutch-English LEMS Tumor Association Prediction (DELTA-P) Score
    
    The DELTA-P Score is a validated clinical prediction tool for identifying 
    Lambert-Eaton myasthenic syndrome (LEMS) patients at high risk for underlying 
    small-cell lung cancer (SCLC). It uses 6 clinical parameters assessed at or 
    within 3 months of LEMS symptom onset to provide risk stratification for 
    appropriate cancer screening protocols.
    
    Args:
        request: Parameters needed for calculation including age at onset, smoking 
                status, weight loss, bulbar involvement, erectile dysfunction, 
                and Karnofsky performance status
        
    Returns:
        DeltaPScoreResponse: Result with clinical interpretation and screening recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("delta_p_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating DELTA-P Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return DeltaPScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for DELTA-P Score",
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