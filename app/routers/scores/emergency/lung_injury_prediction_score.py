"""
Lung Injury Prediction Score (LIPS) Router

Endpoint for calculating LIPS to identify patients at risk for acute lung injury.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.lung_injury_prediction_score import (
    LungInjuryPredictionScoreRequest,
    LungInjuryPredictionScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/lung_injury_prediction_score",
    response_model=LungInjuryPredictionScoreResponse,
    summary="Calculate Lung Injury Prediction Score (LIPS)",
    description="Calculates the Lung Injury Prediction Score (LIPS) to identify patients at high risk for developing acute lung injury (ALI). "
                "This validated clinical tool uses predisposing conditions, high-risk procedures, and risk modifiers to stratify "
                "ALI risk and guide preventive strategies. Score >4 points indicates high risk requiring lung-protective measures, "
                "conservative fluid management, and close monitoring. The tool has 69% sensitivity and 78% specificity for ALI development.",
    response_description="The calculated LIPS score with risk assessment and comprehensive prevention strategies for acute lung injury",
    operation_id="lung_injury_prediction_score"
)
async def calculate_lung_injury_prediction_score(request: LungInjuryPredictionScoreRequest):
    """
    Calculates Lung Injury Prediction Score (LIPS) for acute lung injury risk assessment
    
    The LIPS identifies patients at risk for developing acute lung injury using predisposing
    conditions (shock, aspiration, sepsis, pneumonia, pancreatitis), high-risk surgery/trauma,
    and clinical risk modifiers. Developed and validated in multicenter studies with >5,000 patients.
    
    Clinical Applications:
    - Risk stratification within 24 hours of admission or ICU transfer
    - Guide implementation of lung-protective ventilation strategies  
    - Conservative fluid management for high-risk patients
    - Enrollment criteria for ALI prevention trials
    - Early identification before mechanical ventilation required
    
    Performance Characteristics:
    - Sensitivity: 69% for ALI development
    - Specificity: 78% for ALI development
    - Positive likelihood ratio: 3.1
    - Area under ROC curve: 0.84 (95% CI 0.80-0.89)
    - ALI typically develops within 2 days (median) of assessment
    
    Args:
        request: LIPS calculation parameters including predisposing conditions and risk factors
        
    Returns:
        LungInjuryPredictionScoreResponse: LIPS score with risk category and prevention strategies
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("lung_injury_prediction_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Lung Injury Prediction Score (LIPS)",
                    "details": {"parameters": parameters}
                }
            )
        
        return LungInjuryPredictionScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Lung Injury Prediction Score (LIPS)",
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
                "message": "Internal error in LIPS calculation",
                "details": {"error": str(e)}
            }
        )