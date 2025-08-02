"""
Transtubular Potassium Gradient (TTKG) Router

Endpoint for calculating TTKG to evaluate renal potassium handling.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.ttkg import (
    TtkgRequest,
    TtkgResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ttkg",
    response_model=TtkgResponse,
    summary="Calculate Transtubular Potassium Gradient (TTKG)",
    description="Calculates the Transtubular Potassium Gradient to evaluate renal potassium handling in patients "
                "with hyperkalemia or hypokalemia. TTKG estimates the ratio of potassium in the cortical collecting "
                "duct to that in the peritubular capillaries. Normal values are 8-9 with a normal diet. "
                "In hyperkalemia (K+ >5.0), TTKG ≥7 indicates appropriate renal response; <7 suggests hypoaldosteronism. "
                "In hypokalemia (K+ <3.5), TTKG <3 indicates appropriate conservation; ≥3 suggests renal K+ wasting.",
    response_description="The calculated TTKG value with clinical interpretation based on serum potassium status",
    operation_id="ttkg"
)
async def calculate_ttkg(request: TtkgRequest):
    """
    Calculates Transtubular Potassium Gradient (TTKG)
    
    TTKG helps differentiate between renal and non-renal causes of potassium disorders.
    The formula is: TTKG = (Urine K × Serum osmolality) / (Serum K × Urine osmolality)
    
    Args:
        request: Parameters needed for TTKG calculation
        
    Returns:
        TtkgResponse: TTKG result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ttkg", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating TTKG",
                    "details": {"parameters": parameters}
                }
            )
        
        return TtkgResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for TTKG calculation",
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