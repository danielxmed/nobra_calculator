"""
Cancer and Aging Research Group Chemotherapy Toxicity Tool (CARG-TT) Router

Endpoint for calculating CARG-TT.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.carg_tt import (
    CargTtRequest,
    CargTtResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/carg_tt", response_model=CargTtResponse)
async def calculate_carg_tt(request: CargTtRequest):
    """
    Calculates Cancer and Aging Research Group Chemotherapy Toxicity Tool (CARG-TT)
    
    The CARG-TT estimates the risk of severe chemotherapy-related side effects 
    (Grade 3 or greater toxicity) in older cancer patients (age >65). It uses 
    11 geriatric assessment variables to predict chemotherapy toxicity risk.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        CargTtResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("carg_tt", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CARG-TT",
                    "details": {"parameters": parameters}
                }
            )
        
        return CargTtResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CARG-TT",
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