"""
CKiD U25 eGFR Calculator Router

Endpoint for calculating CKiD U25 eGFR.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.ckid_u25_egfr import (
    CkidU25EgfrRequest,
    CkidU25EgfrResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ckid_u25_egfr",
    response_model=CkidU25EgfrResponse,
    summary="Calculate CKiD U25 eGFR Calculator",
    description="Estimates glomerular filtration rate based on creatinine and/or cystatin C in patients aged 1 to 25 years",
    response_description="The calculated ckid u25 egfr with interpretation",
    operation_id="calculate_ckid_u25_egfr"
)
async def calculate_ckid_u25_egfr(request: CkidU25EgfrRequest):
    """
    Calculates CKiD U25 eGFR
    
    The Chronic Kidney Disease in Children (CKiD) U25 eGFR Calculator estimates 
    glomerular filtration rate using age- and sex-dependent clinical equations 
    specifically developed for children and young adults aged 1 to 25 years 
    with chronic kidney disease.
    
    Args:
        request: CKiD U25 eGFR parameters for kidney function calculation
        
    Returns:
        CkidU25EgfrResponse: eGFR result with CKD staging and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ckid_u25_egfr", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CKiD U25 eGFR",
                    "details": {"parameters": parameters}
                }
            )
        
        return CkidU25EgfrResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CKiD U25 eGFR",
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