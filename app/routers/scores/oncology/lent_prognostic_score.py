"""
LENT Prognostic Score for Malignant Pleural Effusion Router

Endpoint for calculating the LENT prognostic score to predict survival 
in patients with malignant pleural effusion.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.lent_prognostic_score import (
    LentPrognosticScoreRequest,
    LentPrognosticScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/lent_prognostic_score",
    response_model=LentPrognosticScoreResponse,
    summary="Calculate LENT Prognostic Score for Malignant Pleural Effusion",
    description="Calculates the LENT (LDH, ECOG, Neutrophil-to-lymphocyte ratio, Tumor type) Prognostic Score "
                "to predict survival in patients with malignant pleural effusion. This validated clinical decision "
                "tool uses four key parameters: pleural fluid LDH, ECOG performance status, neutrophil-to-lymphocyte "
                "ratio, and tumor type to stratify patients into low risk (median survival ~10.5 months), "
                "moderate risk (~4.3 months), or high risk (~1.5 months) categories. The score helps inform "
                "treatment decisions, guide discussions about prognosis and goals of care, and determine the "
                "appropriateness of aggressive interventions versus palliative approaches in patients with "
                "malignant pleural effusion.",
    response_description="The calculated LENT prognostic score with risk stratification, survival estimates, and evidence-based treatment recommendations for malignant pleural effusion management",
    operation_id="lent_prognostic_score"
)
async def calculate_lent_prognostic_score(request: LentPrognosticScoreRequest):
    """
    Calculates the LENT Prognostic Score for malignant pleural effusion
    
    The LENT Prognostic Score is a validated tool that predicts survival in patients 
    with malignant pleural effusion using four clinical and laboratory parameters. 
    It helps clinicians make informed decisions about treatment intensity, timing of 
    palliative care referral, and goals of care discussions.
    
    Args:
        request: Clinical and laboratory parameters for LENT score calculation
        
    Returns:
        LentPrognosticScoreResponse: Prognostic score with survival estimates and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("lent_prognostic_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating LENT Prognostic Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return LentPrognosticScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for LENT Prognostic Score calculation",
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
                "message": "Internal error in LENT Prognostic Score calculation",
                "details": {"error": str(e)}
            }
        )