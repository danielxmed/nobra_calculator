"""
LRINEC Score for Necrotizing Soft Tissue Infection Router

Endpoint for calculating LRINEC score to screen for necrotizing fasciitis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.lrinec_score import (
    LrinecScoreRequest,
    LrinecScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/lrinec_score",
    response_model=LrinecScoreResponse,
    summary="Calculate LRINEC Score for Necrotizing Soft Tissue Infection",
    description="Calculates the Laboratory Risk Indicator for Necrotizing Fasciitis (LRINEC) score using six routine "
                "laboratory parameters to distinguish necrotizing fasciitis from other soft tissue infections. The score "
                "provides risk stratification to guide urgent surgical consultation decisions. Low risk (≤5 points) suggests "
                "<50% probability of necrotizing fasciitis, moderate risk (6-7 points) indicates 50-75% probability requiring "
                "urgent evaluation, and high risk (≥8 points) suggests >75% probability warranting immediate surgical "
                "intervention. Important limitation: 10% of patients with necrotizing fasciitis had scores <6 in the original "
                "study, so clinical judgment remains paramount and high suspicion should prompt surgical consultation regardless of score.",
    response_description="The calculated LRINEC score with risk stratification and detailed management recommendations",
    operation_id="lrinec_score"
)
async def calculate_lrinec_score(request: LrinecScoreRequest):
    """
    Calculates LRINEC Score for Necrotizing Soft Tissue Infection
    
    Provides laboratory-based risk assessment for necrotizing fasciitis using
    six routine parameters to guide urgent surgical consultation and management
    decisions in suspected soft tissue infections.
    
    Args:
        request: Laboratory parameters (CRP, WBC, hemoglobin, sodium, creatinine, glucose)
        
    Returns:
        LrinecScoreResponse: LRINEC score with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("lrinec_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating LRINEC Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return LrinecScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for LRINEC Score",
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