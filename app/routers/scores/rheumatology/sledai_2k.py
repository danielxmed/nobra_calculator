"""
SLEDAI-2K (Systemic Lupus Erythematosus Disease Activity Index 2000) Router

Endpoint for calculating SLEDAI-2K score for SLE disease activity assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.sledai_2k import (
    Sledai2kRequest,
    Sledai2kResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/sledai_2k",
    response_model=Sledai2kResponse,
    summary="Calculate SLEDAI-2K Score",
    description="Calculates the Systemic Lupus Erythematosus Disease Activity Index 2000 (SLEDAI-2K) for "
                "assessing disease activity in SLE patients. This 24-item weighted index evaluates multiple "
                "organ systems including CNS, vascular, renal, musculoskeletal, dermatologic, immunologic, "
                "and constitutional manifestations. The SLEDAI-2K modification allows documentation of "
                "persistent disease activity in rash, alopecia, mucosal ulcers, and proteinuria. "
                "Scores range from 0-105, with ≥3-4 indicating active disease and ≥6 generally "
                "requiring therapy adjustment.",
    response_description="The calculated SLEDAI-2K score with disease activity staging and treatment recommendations",
    operation_id="sledai_2k"
)
async def calculate_sledai_2k(request: Sledai2kRequest):
    """
    Calculates SLEDAI-2K score for SLE disease activity assessment
    
    The SLEDAI-2K is a validated 24-item weighted index that helps clinicians:
    - Objectively measure SLE disease activity
    - Guide treatment decisions and monitor response
    - Stratify patients for clinical trials
    - Track disease progression over time
    
    Args:
        request: Parameters representing presence/absence of 24 clinical manifestations
        
    Returns:
        Sledai2kResponse: Total score with disease activity level and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("sledai_2k", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating SLEDAI-2K score",
                    "details": {"parameters": parameters}
                }
            )
        
        return Sledai2kResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for SLEDAI-2K calculation",
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