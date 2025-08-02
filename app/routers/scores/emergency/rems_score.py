"""
REMS Score (Rapid Emergency Medicine Score) Router

Endpoint for calculating REMS Score for emergency department mortality risk prediction.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.rems_score import (
    RemsScoreRequest,
    RemsScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/rems_score",
    response_model=RemsScoreResponse,
    summary="Calculate REMS Score (Rapid Emergency Medicine Score)",
    description=(
        "Calculates the REMS (Rapid Emergency Medicine Score) for emergency department "
        "mortality risk prediction. REMS is an attenuated version of APACHE II designed "
        "for rapid calculation using six readily available clinical parameters: age, body "
        "temperature, mean arterial pressure, heart rate, respiratory rate, oxygen saturation, "
        "and Glasgow Coma Scale. The score ranges from 0-26 points and provides excellent "
        "discrimination for in-hospital mortality prediction, with every point increase "
        "associated with a 40% increase in mortality odds. REMS has been extensively validated "
        "across multiple patient populations including sepsis, trauma, COVID-19, and general "
        "emergency department patients, demonstrating superior or comparable performance to "
        "other emergency scoring systems like NEWS, qSOFA, and SIRS. The tool is particularly "
        "valuable for early risk stratification, triage decisions, and resource allocation "
        "in emergency settings."
    ),
    response_description="The calculated REMS score with mortality risk stratification, component scores breakdown, and clinical management recommendations",
    operation_id="rems_score"
)
async def calculate_rems_score(request: RemsScoreRequest):
    """
    Calculates REMS Score for emergency department mortality risk prediction
    
    The REMS (Rapid Emergency Medicine Score) is a validated emergency department 
    mortality risk prediction tool that uses six clinical parameters to assess 
    in-hospital mortality risk. It was developed as an attenuated version of 
    APACHE II for rapid calculation and has excellent predictive performance 
    across diverse patient populations.
    
    Args:
        request: Clinical parameters including age, vital signs, and Glasgow Coma Scale
        
    Returns:
        RemsScoreResponse: Total score, risk stratification, component breakdown, 
                          and clinical management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("rems_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating REMS Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return RemsScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for REMS Score",
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