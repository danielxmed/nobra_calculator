"""
IMPACT Score for Outcomes in Head Injury Router

Endpoint for calculating IMPACT Score for traumatic brain injury prognosis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.impact_score import (
    ImpactScoreRequest,
    ImpactScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/impact_score",
    response_model=ImpactScoreResponse,
    summary="Calculate IMPACT Score for Outcomes in Head Injury",
    description="Predicts 6-month mortality and unfavorable outcomes after moderate to severe traumatic brain injury (TBI) using the International Mission on Prognosis and Analysis of Clinical Trials (IMPACT) prognostic models. The calculator offers three progressive models: Core (clinical variables only), Extended (adds CT findings and secondary injury factors), and Lab (adds laboratory values). Developed from 8,509 TBI patients with GCS ≤12, this validated tool assists clinicians in prognosis counseling, treatment planning, and family discussions. The score provides evidence-based risk stratification from very low risk (<10% mortality) to very high risk (>75% mortality), helping guide clinical decision-making and realistic expectation setting for patients with severe traumatic brain injury.",
    response_description="The calculated IMPACT Score probabilities for 6-month mortality and unfavorable outcomes with clinical interpretation and risk stratification",
    operation_id="impact_score"
)
async def calculate_impact_score(request: ImpactScoreRequest):
    """
    Calculates IMPACT Score for Outcomes in Head Injury
    
    Predicts 6-month mortality and unfavorable outcomes in patients with moderate 
    to severe traumatic brain injury using validated prognostic models. Assists 
    clinicians in evidence-based prognosis counseling and treatment planning.
    
    Args:
        request: Parameters including age, motor score, pupillary reactivity, model type,
                and optional CT findings and laboratory values depending on chosen model
        
    Returns:
        ImpactScoreResponse: Mortality and unfavorable outcome probabilities with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("impact_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating IMPACT Score for Outcomes in Head Injury",
                    "details": {"parameters": parameters}
                }
            )
        
        return ImpactScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for IMPACT Score for Outcomes in Head Injury",
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