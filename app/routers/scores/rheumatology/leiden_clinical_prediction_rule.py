"""
Leiden Clinical Prediction Rule for Undifferentiated Arthritis Router

Endpoint for calculating the likelihood of progression from undifferentiated arthritis 
to rheumatoid arthritis using the Leiden Clinical Prediction Rule.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.leiden_clinical_prediction_rule import (
    LeidenClinicalPredictionRuleRequest,
    LeidenClinicalPredictionRuleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/leiden_clinical_prediction_rule",
    response_model=LeidenClinicalPredictionRuleResponse,
    summary="Calculate Leiden Clinical Prediction Rule for Undifferentiated Arthritis",
    description="Calculates the Leiden Clinical Prediction Rule score to predict the likelihood of progression "
                "from undifferentiated arthritis to rheumatoid arthritis within one year. This validated clinical "
                "decision tool combines nine clinical and laboratory variables including age, sex, joint distribution, "
                "morning stiffness duration, joint counts, inflammatory markers, and autoantibody status. "
                "The score helps guide early treatment decisions with disease-modifying antirheumatic drugs (DMARDs) "
                "by stratifying patients into low risk (≤6.0 points), indeterminate risk (6.01-7.99 points), "
                "or high risk (≥8.0 points) categories. Early identification and treatment of high-risk patients "
                "can prevent joint damage and preserve long-term functional outcomes.",
    response_description="The calculated Leiden Clinical Prediction Rule score with risk stratification, progression likelihood, and evidence-based management recommendations for undifferentiated arthritis",
    operation_id="leiden_clinical_prediction_rule"
)
async def calculate_leiden_clinical_prediction_rule(request: LeidenClinicalPredictionRuleRequest):
    """
    Calculates the Leiden Clinical Prediction Rule score for undifferentiated arthritis
    
    The Leiden Clinical Prediction Rule was developed to predict which patients with 
    recent-onset undifferentiated arthritis will progress to rheumatoid arthritis within 
    one year. This evidence-based tool enables early identification of high-risk patients 
    who would benefit from prompt DMARD therapy to prevent joint damage and disability.
    
    Args:
        request: Clinical and laboratory parameters for prediction rule calculation
        
    Returns:
        LeidenClinicalPredictionRuleResponse: Risk score with clinical interpretation and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("leiden_clinical_prediction_rule", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Leiden Clinical Prediction Rule score",
                    "details": {"parameters": parameters}
                }
            )
        
        return LeidenClinicalPredictionRuleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Leiden Clinical Prediction Rule calculation",
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
                "message": "Internal error in Leiden Clinical Prediction Rule calculation",
                "details": {"error": str(e)}
            }
        )