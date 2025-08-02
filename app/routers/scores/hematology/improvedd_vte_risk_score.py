"""
IMPROVEDD VTE Risk Score Router

Endpoint for calculating IMPROVEDD VTE Risk Score for enhanced venous thromboembolism
risk assessment in hospitalized medical patients with D-dimer incorporation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.improvedd_vte_risk_score import (
    ImprovedVteRiskScoreRequest,
    ImprovedVteRiskScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/improvedd_vte_risk_score",
    response_model=ImprovedVteRiskScoreResponse,
    summary="Calculate IMPROVEDD VTE Risk Score",
    description="Calculates the IMPROVEDD VTE Risk Score for predicting 77-day risk of acute venous thromboembolism (VTE) "
                "in hospitalized medical patients by incorporating D-dimer levels into the IMPROVE Risk Score. The IMPROVEDD "
                "(IMPROVE + D-dimer) score enhances the original IMPROVE VTE risk assessment by adding D-dimer ≥2× upper limit "
                "of normal as an additional risk factor worth 2 points. This validated clinical prediction tool was developed "
                "from the APEX trial involving 7,441 hospitalized medically ill patients. The addition of D-dimer significantly "
                "improves VTE risk discrimination (ΔAUC: 0.06, p=0.0006) and reclassification compared to the original IMPROVE "
                "score. Patients with scores <2 (representing low VTE risk) may not warrant pharmacologic thromboprophylaxis, "
                "while those with scores ≥2 should receive prophylaxis. The score provides specific 77-day VTE risk percentages: "
                "0 (0.5%), 1 (0.7%), 2 (1.0%), 3 (1.4%), 4 (1.9%), ≥5 (≥2.7%). An IMPROVEDD score ≥2 identifies patients "
                "with heightened VTE risk through 77 days, helping clinicians make more informed decisions about extended "
                "thromboprophylaxis duration in acutely ill medical patients.",
    response_description="The calculated IMPROVEDD VTE Risk Score with enhanced risk stratification and thromboprophylaxis recommendations",
    operation_id="improvedd_vte_risk_score"
)
async def calculate_improvedd_vte_risk_score(request: ImprovedVteRiskScoreRequest):
    """
    Calculates IMPROVEDD VTE Risk Score
    
    The IMPROVEDD VTE Risk Score predicts 77-day risk of acute venous thromboembolism (VTE)
    in hospitalized medical patients by incorporating D-dimer levels into the original
    IMPROVE Risk Score. This enhanced tool helps identify patients who may benefit from
    extended thromboprophylaxis duration and guides clinical decision-making regarding
    VTE prophylaxis strategies.
    
    Args:
        request: Parameters needed for IMPROVEDD VTE Risk Score calculation
        
    Returns:
        ImprovedVteRiskScoreResponse: Score with enhanced VTE risk stratification and prophylaxis recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("improvedd_vte_risk_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating IMPROVEDD VTE Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return ImprovedVteRiskScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for IMPROVEDD VTE Risk Score",
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