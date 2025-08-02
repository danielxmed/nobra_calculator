"""
Mehran Score for Post-PCI Contrast Nephropathy Router

Endpoint for calculating Mehran Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.mehran_score import (
    MehranScoreRequest,
    MehranScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mehran_score",
    response_model=MehranScoreResponse,
    summary="Calculate Mehran Score for Post-PCI Contrast Nephropathy",
    description="Calculates the Mehran Score to predict risk of contrast-induced "
                "nephropathy (CIN) after percutaneous coronary intervention (PCI). "
                "The score uses 8 clinical variables including hypotension, IABP use, "
                "congestive heart failure, age >75, anemia, diabetes, contrast volume, "
                "and eGFR to stratify patients into four risk categories (low, moderate, "
                "high, very high). CIN is defined as an increase ≥0.5 mg/dL (or ≥25%) "
                "in serum creatinine at 48 hours post-PCI. The score helps identify "
                "patients who may benefit from preventive measures such as hydration, "
                "N-acetylcysteine, sodium bicarbonate, and contrast volume minimization. "
                "Should not be used in patients on dialysis or with recent contrast "
                "exposure within 1 week. The score has been validated with excellent "
                "discrimination (C-statistic >0.8).",
    response_description="The calculated Mehran score with risk category and clinical recommendations",
    operation_id="mehran_score"
)
async def calculate_mehran_score(request: MehranScoreRequest):
    """
    Calculates Mehran Score for Post-PCI Contrast Nephropathy
    
    The Mehran Score predicts CIN risk after PCI to guide preventive strategies.
    Higher scores indicate greater risk and need for more aggressive prevention.
    
    Args:
        request: Clinical parameters for Mehran score calculation
        
    Returns:
        MehranScoreResponse: Calculated score with risk stratification and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mehran_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Mehran Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MehranScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Mehran Score calculation",
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