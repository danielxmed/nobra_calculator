"""
Systematic Coronary Risk Evaluation 2-Diabetes (SCORE2-Diabetes) Router

Endpoint for calculating SCORE2-Diabetes.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.score2_diabetes import (
    Score2DiabetesRequest,
    Score2DiabetesResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/score2_diabetes",
    response_model=Score2DiabetesResponse,
    summary="Calculate Systematic Coronary Risk Evaluation 2-Diabetes (SCORE2-Diabetes)",
    description="Predicts 10-year risk of cardiovascular disease (fatal and non-fatal myocardial infarction "
                "and stroke) in patients aged 40-69 with type 2 diabetes and without prior cardiovascular disease. "
                "Extends SCORE2 by incorporating diabetes-specific variables (HbA1c, age at diagnosis, eGFR) "
                "for more accurate risk prediction. Uses sex-specific algorithms calibrated to four European "
                "risk regions. Risk thresholds are age-specific with different cutoffs for patients <50 years "
                "versus 50-69 years. Replaces SCORE2 for diabetic patients.",
    response_description="The calculated 10-year CVD risk percentage with age-specific risk stratification and treatment recommendations including diabetes-specific therapies",
    operation_id="score2_diabetes"
)
async def calculate_score2_diabetes(request: Score2DiabetesRequest):
    """
    Calculates Systematic Coronary Risk Evaluation 2-Diabetes (SCORE2-Diabetes)
    
    SCORE2-Diabetes is the European guideline-recommended tool for cardiovascular 
    risk assessment in patients with type 2 diabetes. It provides enhanced risk 
    prediction compared to SCORE2 by incorporating diabetes-specific factors and 
    was developed using data from over 229,000 diabetic patients across Europe.
    
    Args:
        request: Parameters including demographics, smoking status, blood pressure,
                cholesterol levels, diabetes-specific factors, and risk region
        
    Returns:
        Score2DiabetesResponse: 10-year CVD risk with interpretation and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("score2_diabetes", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating SCORE2-Diabetes",
                    "details": {"parameters": parameters}
                }
            )
        
        return Score2DiabetesResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for SCORE2-Diabetes",
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