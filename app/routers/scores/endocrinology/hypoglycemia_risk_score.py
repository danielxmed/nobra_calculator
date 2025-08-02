"""
Hypoglycemia Risk Score Router

Endpoint for calculating Hypoglycemia Risk Score for T2DM patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.hypoglycemia_risk_score import (
    HypoglycemiaRiskScoreRequest,
    HypoglycemiaRiskScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hypoglycemia_risk_score",
    response_model=HypoglycemiaRiskScoreResponse,
    summary="Calculate Hypoglycemia Risk Score",
    description="Predicts 12-month risk of hypoglycemic episodes requiring emergency department visits "
                "or hospitalizations in Type 2 Diabetes Mellitus (T2DM) patients. This validated tool "
                "was developed for population management to identify high-risk patients who would benefit "
                "from targeted interventions such as medication regimen simplification, continuous glucose "
                "monitoring, enhanced diabetes education, and specialist referrals. The score stratifies "
                "patients into Low Risk (<1%), Intermediate Risk (1-5%), and High Risk (>5%) categories "
                "based on six clinical parameters: previous hypoglycemia admissions, emergency department "
                "visits, insulin use, sulfonylurea use, severe kidney disease (eGFR ≤29), and advanced age (≥77 years). "
                "High-risk patients have either ≥3 previous hypoglycemia admissions or 1-2 previous admissions "
                "with current insulin use. This tool is intended for healthcare systems and population health "
                "management rather than individual patient risk assessment.",
    response_description="The calculated risk category with clinical recommendations and population management guidance",
    operation_id="hypoglycemia_risk_score"
)
async def calculate_hypoglycemia_risk_score(request: HypoglycemiaRiskScoreRequest):
    """
    Calculates Hypoglycemia Risk Score
    
    Predicts 12-month risk of hypoglycemia-related emergency care in T2DM patients
    for population management and targeted intervention planning.
    
    Args:
        request: Clinical parameters including previous hypoglycemia admissions, medications, and comorbidities
        
    Returns:
        HypoglycemiaRiskScoreResponse: Risk category with clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hypoglycemia_risk_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Hypoglycemia Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return HypoglycemiaRiskScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Hypoglycemia Risk Score calculation",
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