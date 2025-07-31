"""
Cambridge Diabetes Risk Score Router

Endpoint for calculating Cambridge Diabetes Risk Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.cambridge_diabetes_risk_score import (
    CambridgeDiabetesRiskScoreRequest,
    CambridgeDiabetesRiskScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/cambridge_diabetes_risk_score",
    response_model=CambridgeDiabetesRiskScoreResponse,
    summary="Calculate Cambridge Diabetes Risk Score",
    description="Predicts risk of having previously undiagnosed type 2 diabetes based on clinical and demographic factors. Developed for population screening and identification of high-risk individuals who should undergo diabetes testing.",
    response_description="The calculated cambridge diabetes risk score with interpretation",
    operation_id="calculate_cambridge_diabetes_risk_score"
)
async def calculate_cambridge_diabetes_risk_score(request: CambridgeDiabetesRiskScoreRequest):
    """
    Calculates Cambridge Diabetes Risk Score
    
    Predicts the probability of having undiagnosed type 2 diabetes based on
    seven clinical and demographic risk factors. Developed for population
    screening to identify individuals who should undergo diabetes testing.
    
    The score uses a logistic regression model with the following factors:
    - Gender (male sex increases risk)
    - Age (risk increases significantly after age 45)
    - BMI category (higher BMI strongly increases risk)
    - Family history of diabetes
    - Current smoking status
    - Antihypertensive medication use
    - Steroid medication use
    
    Key cutoff points:
    - 0.11: 85% sensitivity, 51% specificity
    - 0.29: 51% sensitivity, 78% specificity
    
    Note: This score predicts current undiagnosed diabetes, not future diabetes risk.
    It was validated primarily in white English populations and may not generalize
    to other ethnic groups.
    
    Args:
        request: Risk factors for calculation
        
    Returns:
        CambridgeDiabetesRiskScoreResponse: Probability and risk interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cambridge_diabetes_risk_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Cambridge Diabetes Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CambridgeDiabetesRiskScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Cambridge Diabetes Risk Score",
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