"""
Systematic Coronary Risk Evaluation 2-Older Persons (SCORE2-OP) Router

Endpoint for calculating SCORE2-OP.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.score2_op import (
    Score2OpRequest,
    Score2OpResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/score2_op",
    response_model=Score2OpResponse,
    summary="Calculate Systematic Coronary Risk Evaluation 2-Older Persons (SCORE2-OP)",
    description="Predicts 5-year and 10-year risk of cardiovascular disease (fatal and non-fatal myocardial "
                "infarction and stroke) in patients aged 70-89 without prior cardiovascular disease. "
                "Uniquely accounts for competing risk of non-cardiovascular mortality which increases "
                "with age. Uses sex-specific algorithms calibrated to four European risk regions. "
                "Risk factor effects attenuate with age. Risk thresholds differ from SCORE2: "
                "Low-Moderate <7.5%, High 7.5-15%, Very High ≥15%. Treatment decisions should consider "
                "frailty, life expectancy, and patient preferences.",
    response_description="The calculated CVD risk percentage at specified time horizon with age-appropriate risk stratification and treatment recommendations",
    operation_id="score2_op"
)
async def calculate_score2_op(request: Score2OpRequest):
    """
    Calculates Systematic Coronary Risk Evaluation 2-Older Persons (SCORE2-OP)
    
    SCORE2-OP is specifically designed for cardiovascular risk assessment in 
    older persons, accounting for the unique challenges of risk prediction 
    in this population including competing mortality risks and attenuating 
    risk factor effects with age.
    
    Args:
        request: Parameters including demographics, diabetes status, smoking,
                blood pressure, cholesterol levels, risk region, and time horizon
        
    Returns:
        Score2OpResponse: CVD risk with interpretation and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("score2_op", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating SCORE2-OP",
                    "details": {"parameters": parameters}
                }
            )
        
        return Score2OpResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for SCORE2-OP",
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