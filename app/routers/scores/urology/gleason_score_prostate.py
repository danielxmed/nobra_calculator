"""
Gleason Score for Prostate Cancer Router

Endpoint for calculating Gleason Score for Prostate Cancer.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.urology.gleason_score_prostate import (
    GleasonScoreProstateRequest,
    GleasonScoreProstateResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/gleason_score_prostate",
    response_model=GleasonScoreProstateResponse,
    summary="Calculate Gleason Score for Prostate Cancer",
    description="Histologic grading system for prostate cancer based on microscopic tumor architecture patterns. Uses primary and secondary tumor patterns to predict prognosis and guide treatment decisions. The score combines the two most prevalent architectural patterns found in the tumor specimen.",
    response_description="The calculated gleason score prostate with interpretation",
    operation_id="calculate_gleason_score_prostate"
)
async def calculate_gleason_score_prostate(request: GleasonScoreProstateRequest):
    """
    Calculates Gleason Score for Prostate Cancer
    
    The Gleason Score is the most widely used histologic grading system for prostate cancer, 
    developed by Dr. Donald Gleason in the 1960s and modified by the International Society 
    of Urological Pathology (ISUP) in 2014. It evaluates the microscopic architecture of 
    prostate cancer cells based on how closely they resemble normal prostate tissue.
    
    The scoring system combines two grades representing the most prevalent tumor patterns:
    - Primary Grade (3-5): Most predominant pattern (>50% of tumor)
    - Secondary Grade (3-5): Second most common pattern (≥5% but <50%)
    
    Total scores range from 6-10, corresponding to ISUP Grade Groups 1-5, which guide 
    prognosis and treatment decisions. The distinction between 3+4=7 and 4+3=7 is 
    clinically significant for risk stratification.
    
    Args:
        request: Parameters including primary and secondary Gleason grades (3-5)
        
    Returns:
        GleasonScoreProstateResponse: Total Gleason score with grade group, prognosis, and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("gleason_score_prostate", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Gleason Score for Prostate Cancer",
                    "details": {"parameters": parameters}
                }
            )
        
        return GleasonScoreProstateResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Gleason Score",
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