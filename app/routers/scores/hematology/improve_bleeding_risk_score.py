"""
IMPROVE Bleeding Risk Score Router

Endpoint for calculating IMPROVE Bleeding Risk Score for bleeding risk assessment 
in hospitalized medical patients considering anticoagulation therapy.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.improve_bleeding_risk_score import (
    ImproveBleedingRiskScoreRequest,
    ImproveBleedingRiskScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/improve_bleeding_risk_score",
    response_model=ImproveBleedingRiskScoreResponse,
    summary="Calculate IMPROVE Bleeding Risk Score",
    description="Calculates the IMPROVE Bleeding Risk Score for bleeding risk assessment at hospital admission in acutely ill medical patients. "
                "This validated clinical prediction tool was developed from an international database of 15,156 patients across 52 hospitals "
                "in 12 countries to predict major bleeding and clinically relevant non-major bleeding within 14 days of admission. "
                "The score uses 11 clinical variables to stratify patients into low (<7 points, 1.2% major bleeding rate) and high risk "
                "(≥7 points, 3.9% major bleeding rate) categories. This helps clinicians assess the risk-benefit ratio of pharmacological "
                "thromboprophylaxis and identify patients requiring enhanced bleeding monitoring. The score is particularly useful when "
                "considering anticoagulation therapy in hospitalized medical patients.",
    response_description="The calculated IMPROVE Bleeding Risk Score with bleeding risk stratification and clinical management recommendations",
    operation_id="improve_bleeding_risk_score"
)
async def calculate_improve_bleeding_risk_score(request: ImproveBleedingRiskScoreRequest):
    """
    Calculates IMPROVE Bleeding Risk Score
    
    The IMPROVE Bleeding Risk Score assesses bleeding risk at hospital admission for 
    acutely ill medical patients, particularly when considering anticoagulation therapy.
    It helps identify patients at high risk for bleeding complications and guides
    clinical decision-making regarding thromboprophylaxis.
    
    Args:
        request: Parameters needed for IMPROVE Bleeding Risk Score calculation
        
    Returns:
        ImproveBleedingRiskScoreResponse: Score with bleeding risk stratification and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("improve_bleeding_risk_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating IMPROVE Bleeding Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return ImproveBleedingRiskScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for IMPROVE Bleeding Risk Score",
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