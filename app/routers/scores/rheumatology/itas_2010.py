"""
Indian Takayasu Clinical Activity Score (ITAS2010) Router

Endpoint for calculating the ITAS2010 score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.itas_2010 import (
    Itas2010Request,
    Itas2010Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/itas_2010",
    response_model=Itas2010Response,
    summary="Calculate Indian Takayasu Clinical Activity Score (ITAS2010)",
    description="Calculates the Indian Takayasu Clinical Activity Score (ITAS2010), "
                "a validated clinical activity measure specifically developed for Takayasu arteritis. "
                "The score differentiates between active and inactive disease by assessing new or "
                "worsening symptoms within the past 3 months across multiple organ systems including "
                "systemic, abdominal, genitourinary, renal, neurological, and cardiovascular domains. "
                "The score incorporates 19 clinical items with seven key cardiovascular manifestations "
                "weighted at 2 points each due to their clinical significance. Developed from the "
                "Disease Extent Index and validated in over 300 TA patients with excellent "
                "inter-observer reliability (IRR 0.97). Scores <2 indicate inactive disease suitable "
                "for maintenance therapy, while scores ≥2 indicate active disease requiring treatment "
                "intensification or initiation of biological agents. This tool is essential for "
                "monitoring disease activity and guiding therapeutic decisions in Takayasu arteritis management.",
    response_description="The calculated ITAS2010 score with disease activity classification and clinical management recommendations",
    operation_id="itas_2010"
)
async def calculate_itas_2010(request: Itas2010Request):
    """
    Calculates Indian Takayasu Clinical Activity Score (ITAS2010)
    
    A validated clinical activity measure for differentiating between active and 
    inactive disease in Takayasu arteritis based on new or worsening symptoms 
    within the past 3 months.
    
    Args:
        request: Parameters needed for ITAS2010 calculation
        
    Returns:
        Itas2010Response: Result with disease activity classification and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("itas_2010", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ITAS2010 score",
                    "details": {"parameters": parameters}
                }
            )
        
        return Itas2010Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ITAS2010 score",
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