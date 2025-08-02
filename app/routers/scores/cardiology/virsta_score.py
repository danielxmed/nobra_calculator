"""
VIRSTA Score for Infective Endocarditis Risk Assessment Router

Endpoint for calculating VIRSTA Score for infective endocarditis risk stratification.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.virsta_score import (
    VirstaScoreRequest,
    VirstaScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/virsta_score",
    response_model=VirstaScoreResponse,
    summary="Calculate VIRSTA Score for Infective Endocarditis Risk Assessment",
    description="Calculates the VIRSTA Score to risk-stratify suspected infective endocarditis cases "
                "before obtaining echocardiography. This validated clinical decision tool uses 10 clinical "
                "criteria to identify patients at very low risk for infective endocarditis who may not "
                "require immediate echocardiographic evaluation. The score helps reduce unnecessary testing "
                "while maintaining diagnostic safety with a negative predictive value >99% for scores ≤1. "
                "Originally developed and validated in patients with Staphylococcus aureus bacteremia, "
                "the VIRSTA score demonstrates excellent discrimination ability (AUC 0.87-0.89). "
                "High-value criteria include valve disease/prosthetic valve (5 points) and injection drug "
                "use (5 points), while other criteria contribute 1-4 points. Clinical applications include "
                "emergency department triage, inpatient risk stratification, and resource optimization "
                "in suspected endocarditis cases.",
    response_description="VIRSTA score with risk stratification, echocardiography recommendations, and detailed component breakdown",
    operation_id="virsta_score"
)
async def calculate_virsta_score(request: VirstaScoreRequest):
    """
    Calculates VIRSTA Score for Infective Endocarditis Risk Assessment
    
    Risk-stratifies suspected infective endocarditis cases to guide echocardiographic 
    evaluation and reduce unnecessary testing while maintaining diagnostic safety.
    
    Args:
        request: Clinical criteria including valve disease, drug use, phenomena, and laboratory findings
        
    Returns:
        VirstaScoreResponse: VIRSTA score with risk category and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("virsta_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating VIRSTA Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return VirstaScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for VIRSTA Score",
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