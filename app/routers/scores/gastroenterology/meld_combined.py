"""
Model for End-Stage Liver Disease (Combined MELD) Router

Endpoint for calculating Combined MELD score for liver transplant planning.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.meld_combined import (
    MeldCombinedRequest,
    MeldCombinedResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/meld_combined",
    response_model=MeldCombinedResponse,
    summary="Calculate Model for End-Stage Liver Disease (Combined MELD)",
    description="Calculates MELD score using multiple versions for liver transplant planning and end-stage liver "
                "disease severity assessment. Offers three versions: Original MELD (pre-2016, uses bilirubin, "
                "creatinine, INR), MELD-Na (includes sodium for improved prediction), and MELD 3.0 (current OPTN "
                "standard with albumin, age, and sex adjustments). Scores range from 6-40 points, with higher scores "
                "indicating greater disease severity and mortality risk. MELD ≥15 is generally the threshold for "
                "liver transplant consideration, with scores ≥30 indicating critical disease requiring urgent "
                "evaluation. This validated scoring system is the primary tool for organ allocation in liver "
                "transplantation and predicts 90-day mortality risk.",
    response_description="MELD score with disease severity stratification and transplant priority recommendations",
    operation_id="meld_combined"
)
async def calculate_meld_combined(request: MeldCombinedRequest):
    """
    Calculates Model for End-Stage Liver Disease (Combined MELD)
    
    Quantifies severity of chronic liver disease and predicts mortality risk
    using multiple MELD versions for optimal clinical decision-making.
    
    Args:
        request: Laboratory values and patient characteristics for MELD calculation
        
    Returns:
        MeldCombinedResponse: MELD score with severity assessment and transplant guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("meld_combined", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Combined MELD score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MeldCombinedResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Combined MELD score",
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