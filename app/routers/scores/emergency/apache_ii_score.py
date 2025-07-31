"""
APACHE II Score Router

Endpoint for calculating APACHE II Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.apache_ii_score import (
    ApacheIiScoreRequest,
    ApacheIiScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/apache_ii_score",
    response_model=ApacheIiScoreResponse,
    summary="Calculate APACHE II Score",
    description="Estimates ICU mortality using physiological parameters, age, and chronic health status within 24 hours of ICU admission",
    response_description="The calculated apache ii score with interpretation",
    operation_id="apache_ii_score"
)
async def calculate_apache_ii_score(request: ApacheIiScoreRequest):
    """
    Calculates APACHE II Score
    
    The APACHE II (Acute Physiology and Chronic Health Evaluation II) score is a 
    severity-of-disease classification system used to estimate ICU mortality. It uses 
    the worst values from 12 physiological variables within the first 24 hours of 
    ICU admission, plus age and chronic health status.
    
    The score ranges from 0-71 points, with higher scores indicating higher mortality risk.
    It is one of the most widely used ICU scoring systems globally and serves as a 
    benchmark for comparing patient populations and ICU performance.
    
    Args:
        request: Parameters needed for APACHE II calculation including physiological 
                variables, age, and chronic health status
        
    Returns:
        ApacheIiScoreResponse: Result with clinical interpretation and mortality risk assessment
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("apache_ii_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating APACHE II Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return ApacheIiScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for APACHE II Score",
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