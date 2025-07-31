"""
HAT (Hemorrhage After Thrombolysis) Score for Predicting Post-tPA Hemorrhage Router

Endpoint for calculating HAT Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.hat_score import (
    HatScoreRequest,
    HatScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hat_score",
    response_model=HatScoreResponse,
    summary="Calculate HAT Score for Post-tPA Hemorrhage Risk",
    description="Calculates the HAT (Hemorrhage After Thrombolysis) Score to predict intracerebral "
                "hemorrhage risk after tPA administration in acute ischemic stroke patients. The score "
                "uses three readily available parameters: diabetes/hyperglycemia (glucose >200 mg/dL), "
                "pre-tPA NIH Stroke Scale score, and presence of hypodensity on initial head CT. "
                "Scores range from 0-5 points, with higher scores indicating greater hemorrhage risk. "
                "Risk stratification: 0 points (2% symptomatic ICH), 1 point (5%), 2 points (10%), "
                "3 points (15%), >3 points (44%). Helps clinicians assess risk/benefit of tPA in "
                "borderline cases and identify patients requiring intensive monitoring.",
    response_description="The calculated HAT score with hemorrhage risk percentages and clinical recommendations",
    operation_id="calculate_hat_score"
)
async def calculate_hat_score(request: HatScoreRequest):
    """
    Calculates HAT Score for Post-tPA Hemorrhage Risk
    
    The HAT score helps predict hemorrhage risk after thrombolytic therapy,
    assisting in risk/benefit assessment and monitoring decisions.
    
    Args:
        request: Parameters needed for HAT score calculation
        
    Returns:
        HatScoreResponse: Result with hemorrhage risk assessment and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hat_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HAT Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return HatScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HAT score calculation",
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