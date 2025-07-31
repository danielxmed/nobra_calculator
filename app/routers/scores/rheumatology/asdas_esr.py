"""
Ankylosing Spondylitis Disease Activity Score with ESR (ASDAS-ESR) Router

Endpoint for calculating ASDAS-ESR.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.asdas_esr import (
    AsdasEsrRequest,
    AsdasEsrResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/asdas_esr",
    response_model=AsdasEsrResponse,
    summary="Calculate Ankylosing Spondylitis Disease Activity Score w...",
    description="Stratifies severity of ankylosing spondylitis (AS) using clinical and laboratory data, specifically ESR. The ASDAS-ESR is a composite index to assess disease activity in axial spondyloarthritis, combining patient-reported outcomes with laboratory measures to provide a comprehensive evaluation of disease activity.",
    response_description="The calculated asdas esr with interpretation",
    operation_id="calculate_asdas_esr"
)
async def calculate_asdas_esr(request: AsdasEsrRequest):
    """
    Calculates Ankylosing Spondylitis Disease Activity Score with ESR (ASDAS-ESR)
    
    Stratifies severity of ankylosing spondylitis (AS) using clinical and laboratory data, 
    specifically ESR. The ASDAS-ESR is a composite index to assess disease activity in 
    axial spondyloarthritis, combining patient-reported outcomes with laboratory measures 
    to provide a comprehensive evaluation of disease activity.
    
    Args:
        request: Parameters needed for calculation including back pain, morning stiffness,
                patient global assessment, peripheral pain, and ESR
        
    Returns:
        AsdasEsrResponse: Result with clinical interpretation and disease activity stage
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("asdas_esr", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ASDAS-ESR",
                    "details": {"parameters": parameters}
                }
            )
        
        return AsdasEsrResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ASDAS-ESR",
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