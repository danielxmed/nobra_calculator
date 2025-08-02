"""
MELD Score (Original, Pre-2016) Router

Endpoint for calculating MELD Score (Original) for liver disease severity.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.meld_score_original import (
    MeldScoreOriginalRequest,
    MeldScoreOriginalResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/meld_score_original",
    response_model=MeldScoreOriginalResponse,
    summary="Calculate MELD Score (Original, Pre-2016)",
    description="Calculates the original MELD score to quantify end-stage liver disease "
                "severity for transplant allocation. This is the pre-2016 version that does "
                "not include sodium. The calculation uses three laboratory values: creatinine "
                "(kidney function), bilirubin (bile clearance), and INR (clotting function). "
                "Special adjustments: creatinine is set to 4.0 if patient received dialysis "
                "≥2 times in past week, and all values <1.0 are set to 1.0. The formula is: "
                "MELD = (0.957 × ln(Cr) + 0.378 × ln(bili) + 1.120 × ln(INR) + 0.643) × 10. "
                "Final score ranges from 6-40 and correlates with 3-month mortality risk: "
                "≤9 (1.9%), 10-19 (6.0%), 20-29 (19.6%), 30-39 (52.6%), ≥40 (71.3%). "
                "Originally developed to predict mortality after TIPS procedures, it became "
                "the standard for liver allocation by UNOS in 2002. Replaced by MELD-Na in "
                "2016 to better account for hyponatremia's impact on mortality.",
    response_description="The calculated original MELD score with risk stratification and clinical recommendations",
    operation_id="meld_score_original"
)
async def calculate_meld_score_original(request: MeldScoreOriginalRequest):
    """
    Calculates MELD Score (Original, Pre-2016)
    
    This score was the standard for liver allocation from 2002-2016, providing an
    objective assessment of disease severity based on laboratory values.
    
    Args:
        request: Laboratory values and dialysis status for MELD calculation
        
    Returns:
        MeldScoreOriginalResponse: Score with mortality risk and clinical guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("meld_score_original", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MELD score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MeldScoreOriginalResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MELD calculation",
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