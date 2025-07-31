"""
Neutrophil-Lymphocyte Ratio (NLR) Calculator Router

Endpoint for calculating Neutrophil-Lymphocyte Ratio.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.neutrophil_lymphocyte_ratio import (
    NeutrophilLymphocyteRatioRequest,
    NeutrophilLymphocyteRatioResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/neutrophil_lymphocyte_ratio", response_model=NeutrophilLymphocyteRatioResponse)
async def calculate_neutrophil_lymphocyte_ratio(request: NeutrophilLymphocyteRatioRequest):
    """
    Calculates Neutrophil-Lymphocyte Ratio (NLR)
    
    The NLR is a simple biomarker of systemic inflammation and physiological stress, 
    calculated by dividing neutrophil count by lymphocyte count. It provides more 
    information than white blood cell count alone and can be trended over time.
    
    Args:
        request: Parameters needed for calculation including count type
                (absolute or percentage) and neutrophil/lymphocyte counts
        
    Returns:
        NeutrophilLymphocyteRatioResponse: NLR ratio with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("neutrophil_lymphocyte_ratio", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Neutrophil-Lymphocyte Ratio",
                    "details": {"parameters": parameters}
                }
            )
        
        return NeutrophilLymphocyteRatioResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Neutrophil-Lymphocyte Ratio",
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