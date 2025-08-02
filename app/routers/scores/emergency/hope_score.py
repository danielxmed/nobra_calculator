"""
Hypothermia Outcome Prediction after ECLS (HOPE) Score Router

Endpoint for calculating HOPE Score for hypothermic cardiac arrest patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.hope_score import (
    HopeScoreRequest,
    HopeScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hope_score",
    response_model=HopeScoreResponse,
    summary="Calculate HOPE Score for Hypothermic Cardiac Arrest",
    description="Predicts survival probability for patients with hypothermic cardiac arrest undergoing "
                "extracorporeal life support (ECLS) rewarming to guide clinical decision-making. This validated "
                "tool uses six clinical parameters (sex, asphyxia, age, potassium, CPR duration, core temperature) "
                "to calculate survival probability with superior discrimination compared to serum potassium alone "
                "(AUC 0.895 vs 0.774). The score provides critical decision support with a 10% survival probability "
                "threshold: patients with ≥10% probability should receive ECLS rewarming, while those with <10% "
                "probability are unlikely to benefit from ECLS. The tool has been externally validated "
                "(AUC 0.825) with excellent negative predictive value (97%) and is recommended in 2021 European "
                "Resuscitation Council Guidelines. Most survivors (84%) achieve good neurological outcomes. The score "
                "replaces reliance on serum potassium cutoffs alone and enables more nuanced clinical decision-making "
                "for this critical patient population requiring immediate ECLS capability activation.",
    response_description="The calculated survival probability with ECLS recommendation and clinical guidance",
    operation_id="hope_score"
)
async def calculate_hope_score(request: HopeScoreRequest):
    """
    Calculates HOPE Score for Hypothermic Cardiac Arrest
    
    Predicts survival probability for hypothermic cardiac arrest patients undergoing 
    ECLS rewarming to guide clinical decision-making about initiating extracorporeal support.
    
    Args:
        request: Clinical parameters including demographics, mechanism, and physiological measures
        
    Returns:
        HopeScoreResponse: Survival probability with ECLS recommendation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hope_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HOPE Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return HopeScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HOPE Score calculation",
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