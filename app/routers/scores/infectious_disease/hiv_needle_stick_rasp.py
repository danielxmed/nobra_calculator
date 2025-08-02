"""
HIV Needle Stick Risk Assessment Stratification Protocol (RASP) Router

Endpoint for calculating HIV Needle Stick RASP score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.infectious_disease.hiv_needle_stick_rasp import (
    HivNeedleStickRaspRequest,
    HivNeedleStickRaspResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hiv_needle_stick_rasp",
    response_model=HivNeedleStickRaspResponse,
    summary="Calculate HIV Needle Stick RASP Score",
    description="Quantifies HIV transmission risk following needle stick injuries or other potential HIV exposures "
                "by multiplying risk factors across four domains: source patient HIV status, type of body fluid, "
                "transmission route, and volume of exposure. The calculated risk (expressed as 1 in X) helps guide "
                "decisions about post-exposure prophylaxis (PEP) initiation. PEP is definitely indicated for risks "
                "≥1/1000, recommended for risks 1/1001-1/10000, optional for risks 1/10001-1/100000, and not "
                "indicated for risks ≤1/100000.",
    response_description="The calculated HIV transmission risk ratio with PEP recommendations based on risk level",
    operation_id="hiv_needle_stick_rasp"
)
async def calculate_hiv_needle_stick_rasp(request: HivNeedleStickRaspRequest):
    """
    Calculates HIV Needle Stick Risk Assessment Stratification Protocol (RASP)
    
    Quantifies HIV exposure risk to guide post-exposure prophylaxis decisions 
    following needle stick injuries or other potential HIV exposures.
    
    Args:
        request: Parameters needed for RASP calculation including source HIV status,
                 body fluid type, transmission route, and exposure volume
        
    Returns:
        HivNeedleStickRaspResponse: Risk ratio (1 in X) with PEP recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hiv_needle_stick_rasp", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HIV Needle Stick RASP score",
                    "details": {"parameters": parameters}
                }
            )
        
        return HivNeedleStickRaspResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HIV Needle Stick RASP calculation",
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