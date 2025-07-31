"""
Framingham Risk Score for Hard Coronary Heart Disease Router

Endpoint for calculating Framingham Risk Score for Hard Coronary Heart Disease.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.framingham_risk_score import (
    FraminghamRiskScoreRequest,
    FraminghamRiskScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/framingham_risk_score",
    response_model=FraminghamRiskScoreResponse,
    summary="Calculate Framingham Risk Score for Hard Corona...",
    description="Estimates 10-year risk of myocardial infarction in patients aged 30-79 with no history of coronary heart disease or diabetes",
    response_description="The calculated framingham risk score with interpretation",
    operation_id="framingham_risk_score"
)
async def calculate_framingham_risk_score(request: FraminghamRiskScoreRequest):
    """
    Calculates Framingham Risk Score for Hard Coronary Heart Disease
    
    Estimates 10-year risk of myocardial infarction and coronary death in primary 
    prevention patients aged 30-79 without known coronary heart disease or diabetes.
    Uses gender-specific equations with established cardiovascular risk factors.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        FraminghamRiskScoreResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("framingham_risk_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Framingham Risk Score for Hard Coronary Heart Disease",
                    "details": {"parameters": parameters}
                }
            )
        
        return FraminghamRiskScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Framingham Risk Score for Hard Coronary Heart Disease",
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