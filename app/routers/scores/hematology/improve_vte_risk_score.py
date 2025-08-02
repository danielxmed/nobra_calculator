"""
IMPROVE VTE Risk Score Router

Endpoint for calculating IMPROVE VTE Risk Score for venous thromboembolism
risk assessment in hospitalized medical patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.improve_vte_risk_score import (
    ImproveVteRiskScoreRequest,
    ImproveVteRiskScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/improve_vte_risk_score",
    response_model=ImproveVteRiskScoreResponse,
    summary="Calculate IMPROVE VTE Risk Score",
    description="Calculates the IMPROVE VTE Risk Score for predicting 3-month risk of acute venous thromboembolism (VTE) "
                "in hospitalized medical patients. The IMPROVE (International Medical Prevention Registry on Venous "
                "Thromboembolism) Predictive score was developed from an international database to assess VTE risk and "
                "help identify patients who may not require pharmacological thromboprophylaxis. This validated clinical "
                "prediction tool uses 7 clinical variables to stratify patients into risk categories. Patients with "
                "scores <2 (representing <1% 3-month VTE risk) may not warrant pharmacologic thromboprophylaxis, while "
                "those with scores ≥2 should receive prophylaxis. The score provides specific VTE risk percentages: "
                "0 (0.4%), 1 (0.6%), 2 (1.0%), 3 (1.7%), 4 (2.9%), ≥5 (≥7.2%). This tool is particularly valuable "
                "for identifying low-risk medical patients who can safely avoid anticoagulation, thereby reducing "
                "unnecessary exposure to bleeding risk while maintaining appropriate prophylaxis for higher-risk patients.",
    response_description="The calculated IMPROVE VTE Risk Score with risk stratification and thromboprophylaxis recommendations",
    operation_id="improve_vte_risk_score"
)
async def calculate_improve_vte_risk_score(request: ImproveVteRiskScoreRequest):
    """
    Calculates IMPROVE VTE Risk Score
    
    The IMPROVE VTE Risk Score predicts 3-month risk of acute venous thromboembolism (VTE)
    in hospitalized medical patients. It helps identify patients who may not require
    pharmacological thromboprophylaxis and guides clinical decision-making regarding
    VTE prophylaxis strategies.
    
    Args:
        request: Parameters needed for IMPROVE VTE Risk Score calculation
        
    Returns:
        ImproveVteRiskScoreResponse: Score with VTE risk stratification and prophylaxis recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("improve_vte_risk_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating IMPROVE VTE Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return ImproveVteRiskScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for IMPROVE VTE Risk Score",
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