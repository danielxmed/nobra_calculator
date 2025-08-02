"""
Phoenix Sepsis Score Router

Endpoint for calculating Phoenix Sepsis Score for pediatric sepsis and septic shock diagnosis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.phoenix_sepsis_score import (
    PhoenixSepsisScoreRequest,
    PhoenixSepsisScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/phoenix_sepsis_score",
    response_model=PhoenixSepsisScoreResponse,
    summary="Calculate Phoenix Sepsis Score",
    description=(
        "Calculates the Phoenix Sepsis Score for pediatric sepsis and septic shock diagnosis. "
        "This is the first data-driven international consensus criteria for pediatric sepsis, "
        "developed by the SCCM Pediatric Sepsis Definition Task Force and published in JAMA 2024. "
        "The score evaluates organ dysfunction across four systems (respiratory, cardiovascular, "
        "coagulation, neurologic) to identify potentially life-threatening organ dysfunction in "
        "children with suspected infection. A score ≥2 points with suspected infection meets "
        "sepsis criteria, and septic shock requires sepsis with cardiovascular subscore ≥1. "
        "The tool provides standardized criteria for clinical care, quality improvement, and research applications."
    ),
    response_description="The calculated Phoenix Sepsis Score with organ system subscores, diagnostic classification (No Sepsis/Sepsis/Septic Shock), and clinical management recommendations",
    operation_id="phoenix_sepsis_score"
)
async def calculate_phoenix_sepsis_score(request: PhoenixSepsisScoreRequest):
    """
    Calculates Phoenix Sepsis Score for pediatric sepsis diagnosis
    
    The Phoenix Sepsis Score is the first data-driven international consensus criteria 
    for pediatric sepsis and septic shock, replacing previous SIRS-based definitions 
    with superior predictive value. It evaluates organ dysfunction across four key 
    systems to standardize sepsis recognition in children.
    
    Args:
        request: Parameters including age, infection status, and organ system assessments
        
    Returns:
        PhoenixSepsisScoreResponse: Total score, component subscores, diagnostic classification, 
                                   and clinical management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("phoenix_sepsis_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Phoenix Sepsis Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return PhoenixSepsisScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Phoenix Sepsis Score",
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