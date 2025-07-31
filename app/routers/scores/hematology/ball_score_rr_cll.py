"""
BALL Score for Relapsed/Refractory CLL Router

Endpoint for calculating BALL Score for Relapsed/Refractory CLL.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.ball_score_rr_cll import (
    BallScoreRrCllRequest,
    BallScoreRrCllResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ball_score_rr_cll",
    response_model=BallScoreRrCllResponse,
    summary="Calculate BALL Score for Relapsed/Refractory CLL",
    description="Assesses prognosis of patients with relapsed/refractory chronic lymphocytic leukemia (R/R CLL) on targeted therapies. The BALL Score (β2-microglobulin, Anemia, LDH, Last Therapy) helps estimate survival outcomes in patients with R/R-CLL who require further treatment with targeted therapies.",
    response_description="The calculated ball score rr cll with interpretation",
    operation_id="calculate_ball_score_rr_cll"
)
async def calculate_ball_score_rr_cll(request: BallScoreRrCllRequest):
    """
    Calculates BALL Score for Relapsed/Refractory CLL
    
    Assesses prognosis of patients with relapsed/refractory chronic lymphocytic 
    leukemia (R/R CLL) on targeted therapies. The BALL Score stratifies patients 
    into risk groups based on 24-month overall survival.
    
    Args:
        request: Parameters needed for calculation including beta-2-microglobulin,
                hemoglobin, sex, LDH levels, and time since last therapy
        
    Returns:
        BallScoreRrCllResponse: Result with risk stratification and survival prognosis
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ball_score_rr_cll", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating BALL Score for R/R CLL",
                    "details": {"parameters": parameters}
                }
            )
        
        return BallScoreRrCllResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for BALL Score calculation",
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