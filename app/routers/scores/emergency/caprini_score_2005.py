"""
Caprini Score for Venous Thromboembolism (2005) Router

Endpoint for calculating Caprini Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.caprini_score_2005 import (
    CapriniScore2005Request,
    CapriniScore2005Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/caprini_score_2005",
    response_model=CapriniScore2005Response,
    summary="Calculate Caprini Score for Venous Thromboembolism (2005)",
    description="The Caprini Score stratifies risk of venous thromboembolism (VTE) in surgical patients, guiding prophylaxis decisions. It assesses multiple risk factors including age, surgery type, medical conditions, and mobility status to predict VTE risk and inform appropriate prevention strategies.",
    response_description="The calculated caprini score 2005 with interpretation",
    operation_id="caprini_score_2005"
)
async def calculate_caprini_score_2005(request: CapriniScore2005Request):
    """
    Calculates Caprini Score for Venous Thromboembolism (2005)
    
    The Caprini Score stratifies risk of venous thromboembolism (VTE) in surgical 
    and medical patients, guiding prophylaxis decisions. It is the most widely 
    validated VTE risk assessment tool recommended by ACCP guidelines.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        CapriniScore2005Response: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("caprini_score_2005", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Caprini Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CapriniScore2005Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Caprini Score",
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