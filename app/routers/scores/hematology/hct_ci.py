"""
Hematopoietic Cell Transplantation-specific Comorbidity Index (HCT-CI) Router

Endpoint for calculating HCT-CI score for HCT risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.hct_ci import (
    HctCiRequest,
    HctCiResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hct_ci",
    response_model=HctCiResponse,
    summary="Calculate HCT-CI Score",
    description="Calculates the Hematopoietic Cell Transplantation-specific Comorbidity Index (HCT-CI) "
                "to predict survival after HCT in patients with hematologic malignancies. "
                "The HCT-CI evaluates 17 comorbidity categories and assigns weighted scores (0-3 points each) "
                "based on their impact on non-relapse mortality. An optional age adjustment can be included "
                "(+1 point for age ≥40 years). The total score stratifies patients into three risk groups: "
                "Low (0 points, ~14% NRM), Intermediate (1-2 points, ~21% NRM), and High (≥3 points, ~41% NRM). "
                "This validated tool helps guide transplant eligibility decisions and conditioning regimen selection.",
    response_description="The calculated HCT-CI score with risk stratification and clinical recommendations",
    operation_id="hct_ci"
)
async def calculate_hct_ci(request: HctCiRequest):
    """
    Calculates Hematopoietic Cell Transplantation-specific Comorbidity Index (HCT-CI)
    
    The HCT-CI is a validated prognostic tool that predicts non-relapse mortality
    and overall survival in patients undergoing hematopoietic cell transplantation.
    It has been shown to be more sensitive than the Charlson Comorbidity Index
    for this specific patient population.
    
    Args:
        request: Parameters including 17 comorbidity categories and optional age adjustment
        
    Returns:
        HctCiResponse: HCT-CI score with risk stratification and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hct_ci", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HCT-CI score",
                    "details": {"parameters": parameters}
                }
            )
        
        return HctCiResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HCT-CI calculation",
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
                "message": "Internal error in HCT-CI calculation",
                "details": {"error": str(e)}
            }
        )