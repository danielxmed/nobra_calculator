"""
International Prognostic Score for Asymptomatic Early-stage CLL (IPS-E) Router

Endpoint for calculating IPS-E.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.ips_e_cll import (
    IpsECllRequest,
    IpsECllResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ips_e_cll",
    response_model=IpsECllResponse,
    summary="Calculate International Prognostic Score for Asymptomatic Early-stage CLL (IPS-E)",
    description="Calculates the International Prognostic Score for Asymptomatic Early-stage CLL (IPS-E) to predict time to first treatment (TTFT) in patients with asymptomatic early-stage chronic lymphocytic leukemia. This validated prognostic tool uses three independent prognostic factors with equal weighting: unmutated IGHV status (≥98% homology, 1 point), absolute lymphocyte count >15×10⁹/L (1 point), and presence of palpable lymph nodes (1 point). The IPS-E stratifies patients into three risk categories based on the total score (0-3 points): Low Risk (score 0, 5-year treatment risk 8.4%, 1-year risk <0.1%), Intermediate Risk (score 1, 5-year treatment risk 28.4%, 1-year risk 3.1%), and High Risk (score 2-3, 5-year treatment risk 61.2%). Developed using individual patient data from 11 international cohorts (n=4,933), the IPS-E demonstrates excellent discrimination with C-index values of 0.74 in training and 0.70 in validation cohorts. This scoring system is specifically designed for asymptomatic early-stage CLL patients (Binet A, Rai 0-I) who meet iwCLL watch-and-wait criteria and helps optimize surveillance schedules, guide clinical trial eligibility, and improve patient counseling regarding treatment likelihood and timing.",
    response_description="The calculated IPS-E score with risk stratification and treatment timing predictions",
    operation_id="ips_e_cll"
)
async def calculate_ips_e_cll(request: IpsECllRequest):
    """
    Calculates IPS-E for time to first treatment prediction in asymptomatic early-stage CLL
    
    Predicts treatment risk using three independent prognostic factors to stratify 
    asymptomatic early-stage CLL patients into risk categories for monitoring guidance.
    
    Args:
        request: Clinical parameters for IPS-E calculation (3 prognostic factors)
        
    Returns:
        IpsECllResponse: IPS-E score with risk category and treatment risk predictions
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ips_e_cll", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating IPS-E",
                    "details": {"parameters": parameters}
                }
            )
        
        return IpsECllResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for IPS-E",
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