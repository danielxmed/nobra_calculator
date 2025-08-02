"""
Menza Score Router

Endpoint for calculating Menza Score for HIV risk prediction in MSM.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.infectious_disease.menza_score import (
    MenzaScoreRequest,
    MenzaScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/menza_score",
    response_model=MenzaScoreResponse,
    summary="Calculate Menza Score for HIV Risk",
    description="Calculates the Menza Score to predict 4-year HIV acquisition risk in men who have "
                "sex with men (MSM). This validated risk prediction tool uses four key behavioral "
                "and clinical factors: STI history (gonorrhea, chlamydia, or syphilis), substance "
                "use (methamphetamine or nitrites in past 6 months), unprotected anal intercourse "
                "with HIV-positive or unknown status partners, and number of male sexual partners. "
                "The score ranges from 0-19 points and stratifies individuals into risk categories: "
                "Low (<5% risk), Moderate (5-9%), High (10-14%), and Very High (>14% 4-year risk). "
                "Originally developed using STI clinic data (2001-2008) and validated in HIV "
                "prevention trials, the score helps identify candidates for pre-exposure prophylaxis "
                "(PrEP) and targeted prevention interventions. Note: The score should only be used "
                "for MSM populations and not as the sole criterion for PrEP eligibility. Validation "
                "studies showed decreased sensitivity for Black MSM.",
    response_description="The calculated Menza Score with risk stratification and prevention recommendations",
    operation_id="menza_score"
)
async def calculate_menza_score(request: MenzaScoreRequest):
    """
    Calculates Menza Score for HIV risk prediction in MSM
    
    This tool helps identify men who have sex with men at highest risk for HIV
    acquisition to guide prevention interventions including PrEP consideration.
    
    Args:
        request: Behavioral and clinical risk factors
        
    Returns:
        MenzaScoreResponse: Risk score with interpretation and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("menza_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Menza Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MenzaScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Menza Score",
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