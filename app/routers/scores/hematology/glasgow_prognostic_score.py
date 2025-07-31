"""
Glasgow Prognostic Score (GPS) Router

Endpoint for calculating Glasgow Prognostic Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.glasgow_prognostic_score import (
    GlasgowPrognosticScoreRequest,
    GlasgowPrognosticScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/glasgow_prognostic_score",
    response_model=GlasgowPrognosticScoreResponse,
    summary="Calculate Glasgow Prognostic Score (GPS)",
    description="Inflammation and nutrition-based prognostic score for cancer patients using serum C-reactive protein and albumin levels. Predicts overall survival and disease-free survival across multiple cancer types including colorectal, hepatocellular carcinoma, sarcoma, and lung cancer.",
    response_description="The calculated glasgow prognostic score with interpretation",
    operation_id="glasgow_prognostic_score"
)
async def calculate_glasgow_prognostic_score(request: GlasgowPrognosticScoreRequest):
    """
    Calculates Glasgow Prognostic Score (GPS)
    
    The Glasgow Prognostic Score is an inflammation and nutrition-based prognostic 
    score for cancer patients using serum C-reactive protein and albumin levels. 
    It reflects both the presence of systemic inflammatory response (CRP) and 
    progressive nutritional decline (albumin) in cancer patients. The GPS has been 
    extensively validated across multiple cancer types and is one of the most 
    widely used systemic inflammation-based prognostic scores in oncology.
    
    Args:
        request: Parameters including CRP level (mg/dL), albumin level (g/dL),
                and score type (original or modified)
        
    Returns:
        GlasgowPrognosticScoreResponse: GPS score with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("glasgow_prognostic_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Glasgow Prognostic Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return GlasgowPrognosticScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Glasgow Prognostic Score",
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