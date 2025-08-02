"""
Systematic Coronary Risk Evaluation 2 (SCORE2) Router

Endpoint for calculating SCORE2.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.score2 import (
    Score2Request,
    Score2Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/score2",
    response_model=Score2Response,
    summary="Calculate Systematic Coronary Risk Evaluation 2 (SCORE2)",
    description="Predicts 10-year risk of cardiovascular disease (fatal and non-fatal myocardial infarction "
                "and stroke) in patients aged 40-69 without prior cardiovascular disease or diabetes. "
                "Uses sex-specific algorithms calibrated to four risk regions based on country-specific "
                "CVD mortality rates. Risk thresholds are age-specific with different cutoffs for patients "
                "<50 years versus 50-69 years. Replaces the original SCORE with improved risk prediction.",
    response_description="The calculated 10-year CVD risk percentage with age-specific risk stratification and treatment recommendations",
    operation_id="score2"
)
async def calculate_score2(request: Score2Request):
    """
    Calculates Systematic Coronary Risk Evaluation 2 (SCORE2)
    
    SCORE2 is the European guideline-recommended tool for cardiovascular risk 
    assessment in apparently healthy individuals. It provides more accurate risk 
    prediction than the original SCORE by including non-fatal events and using 
    contemporary data calibrated to specific regions.
    
    Args:
        request: Parameters including demographics, smoking status, blood pressure,
                cholesterol levels, and risk region
        
    Returns:
        Score2Response: 10-year CVD risk with interpretation and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("score2", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating SCORE2",
                    "details": {"parameters": parameters}
                }
            )
        
        return Score2Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for SCORE2",
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