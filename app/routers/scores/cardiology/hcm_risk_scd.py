"""
HCM Risk-SCD Router

Endpoint for calculating HCM Risk-SCD score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.hcm_risk_scd import (
    HcmRiskScdRequest,
    HcmRiskScdResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hcm_risk_scd",
    response_model=HcmRiskScdResponse,
    summary="Calculate HCM Risk-SCD",
    description="Calculates the HCM Risk-SCD score to estimate 5-year risk of sudden cardiac death "
                "in patients with hypertrophic cardiomyopathy. This validated risk prediction model "
                "uses 7 clinical parameters to provide individualized risk estimates that guide "
                "decisions regarding prophylactic ICD implantation. The model stratifies patients "
                "into low (<4%), intermediate (4-6%), and high (≥6%) risk categories. "
                "Developed from a multicenter cohort of 3,675 patients and validated internationally, "
                "it represents the first validated SCD risk model for HCM patients.",
    response_description="The calculated 5-year SCD risk percentage with risk stratification and ICD recommendations",
    operation_id="hcm_risk_scd"
)
async def calculate_hcm_risk_scd(request: HcmRiskScdRequest):
    """
    Calculates HCM Risk-SCD score
    
    The HCM Risk-SCD estimates 5-year sudden cardiac death risk in patients
    with hypertrophic cardiomyopathy to guide ICD implantation decisions.
    
    Args:
        request: Parameters needed for HCM Risk-SCD calculation
        
    Returns:
        HcmRiskScdResponse: 5-year SCD risk with clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hcm_risk_scd", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HCM Risk-SCD",
                    "details": {"parameters": parameters}
                }
            )
        
        return HcmRiskScdResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HCM Risk-SCD calculation",
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