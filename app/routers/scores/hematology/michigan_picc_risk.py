"""
Michigan Risk Score for PICC-Related Thrombosis Router

Endpoint for calculating Michigan PICC thrombosis risk.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.michigan_picc_risk import (
    MichiganPiccRiskRequest,
    MichiganPiccRiskResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/michigan_picc_risk",
    response_model=MichiganPiccRiskResponse,
    summary="Calculate Michigan Risk Score for PICC-Related Thrombosis",
    description="Predicts risk of deep vein thrombosis (DVT) in patients with peripherally inserted "
                "central catheter (PICC). Uses five clinical factors to stratify patients into four "
                "risk classes (I-IV) with thrombosis rates ranging from 0.9% to 4.7%. Helps guide "
                "decisions about PICC placement and alternative vascular access options. Validated "
                "in medical patients ≥18 years old.",
    response_description="The calculated Michigan Risk Score with risk class and thrombosis probability",
    operation_id="michigan_picc_risk"
)
async def calculate_michigan_picc_risk(request: MichiganPiccRiskRequest):
    """
    Calculates Michigan Risk Score for PICC-Related Thrombosis
    
    Stratifies patients into risk classes for PICC-associated DVT to help
    guide vascular access decisions and VTE prophylaxis strategies.
    
    Args:
        request: Clinical parameters including CVC presence, WBC count,
                PICC lumens, VTE history, and cancer status
        
    Returns:
        MichiganPiccRiskResponse: Risk score, class, and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("michigan_picc_risk", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Michigan PICC Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MichiganPiccRiskResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Michigan PICC Risk Score",
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