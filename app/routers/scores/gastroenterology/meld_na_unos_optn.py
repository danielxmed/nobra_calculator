"""
MELD Na (UNOS/OPTN) Router

Endpoint for calculating MELD Na score for liver disease severity.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.meld_na_unos_optn import (
    MeldNaUnosOptnRequest,
    MeldNaUnosOptnResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/meld_na_unos_optn",
    response_model=MeldNaUnosOptnResponse,
    summary="Calculate MELD Na (UNOS/OPTN) Score",
    description="Calculates the MELD Na score to quantify end-stage liver disease severity "
                "for transplant allocation. This score has been used by UNOS/OPTN since "
                "January 2016, replacing the original MELD score. The calculation uses four "
                "laboratory values: creatinine (kidney function), bilirubin (bile clearance), "
                "INR (clotting function), and sodium (added to improve mortality prediction). "
                "Special adjustments: creatinine is set to 4.0 if patient received dialysis "
                "≥2 times in past week, all values <1.0 are set to 1.0, and sodium is "
                "bounded between 125-137 mEq/L. The sodium adjustment formula is only applied "
                "if initial MELD >11. Final score ranges from 6-40 and directly correlates "
                "with 3-month mortality risk: ≤9 (1.9%), 10-19 (6.0%), 20-29 (19.6%), "
                "30-39 (52.6%), ≥40 (71.3%). Higher scores indicate higher priority for "
                "liver transplant allocation.",
    response_description="The calculated MELD Na score with risk stratification and clinical recommendations",
    operation_id="meld_na_unos_optn"
)
async def calculate_meld_na_unos_optn(request: MeldNaUnosOptnRequest):
    """
    Calculates MELD Na (UNOS/OPTN) Score
    
    This score is the primary determinant of liver allocation priority in the United States,
    quantifying disease severity based on objective laboratory values.
    
    Args:
        request: Laboratory values and dialysis status for MELD Na calculation
        
    Returns:
        MeldNaUnosOptnResponse: Score with mortality risk and clinical guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("meld_na_unos_optn", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MELD Na score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MeldNaUnosOptnResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MELD Na calculation",
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