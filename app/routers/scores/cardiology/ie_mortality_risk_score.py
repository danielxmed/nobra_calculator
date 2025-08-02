"""
Infective Endocarditis (IE) Mortality Risk Score Router

Endpoint for calculating IE Mortality Risk Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.ie_mortality_risk_score import (
    IeMortalityRiskScoreRequest,
    IeMortalityRiskScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ie_mortality_risk_score",
    response_model=IeMortalityRiskScoreResponse,
    summary="Calculate Infective Endocarditis (IE) Mortality Risk Score",
    description="Calculates the IE Mortality Risk Score for 6-month mortality prediction in patients with infective endocarditis. "
                "This validated clinical tool was developed from the International Collaboration on Endocarditis (ICE) Prospective Cohort Study "
                "and incorporates 14 clinical parameters including host factors (age, dialysis history), IE characteristics (pathogen type, "
                "vegetation location), and complications (heart failure, stroke, paravalvular involvement). The score uses a logistic regression "
                "formula to predict mortality probability: 100 × [1/(1+exp(-(2.416×score+0.109×score²-4.849)))]. Risk categories include: "
                "Low Risk (≤10%), Moderate Risk (10-25%), High Risk (25-50%), and Very High Risk (>50%). This tool helps guide treatment "
                "intensity, surgical decision-making, and prognostic discussions with patients and families.",
    response_description="The calculated IE Mortality Risk Score with 6-month mortality probability percentage and risk-based management recommendations",
    operation_id="ie_mortality_risk_score"
)
async def calculate_ie_mortality_risk_score(request: IeMortalityRiskScoreRequest):
    """
    Calculates IE Mortality Risk Score for 6-month mortality prediction
    
    Predicts mortality risk in patients with infective endocarditis using validated 
    clinical parameters from the ICE study. Incorporates host factors, IE characteristics,
    and complications to provide prognostic information for clinical decision-making.
    
    Args:
        request: Parameters for IE mortality risk calculation (14 clinical variables)
        
    Returns:
        IeMortalityRiskScoreResponse: Mortality probability with risk category and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ie_mortality_risk_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating IE Mortality Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return IeMortalityRiskScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for IE Mortality Risk Score",
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