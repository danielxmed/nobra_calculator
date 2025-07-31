"""
BUN Creatinine Ratio Router

Endpoint for calculating BUN Creatinine Ratio.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.bun_creatinine_ratio import (
    BunCreatinineRatioRequest,
    BunCreatinineRatioResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/bun_creatinine_ratio",
    response_model=BunCreatinineRatioResponse,
    summary="Calculate BUN Creatinine Ratio",
    description="Evaluates kidney function by calculating the ratio of blood urea nitrogen (BUN) to serum creatinine, helping to distinguish between prerenal, intrinsic renal, and postrenal causes of kidney dysfunction.",
    response_description="The calculated bun creatinine ratio with interpretation",
    operation_id="bun_creatinine_ratio"
)
async def calculate_bun_creatinine_ratio(request: BunCreatinineRatioRequest):
    """
    Calculates BUN Creatinine Ratio
    
    Evaluates kidney function by calculating the ratio of blood urea nitrogen (BUN) 
    to serum creatinine, helping to distinguish between prerenal, intrinsic renal, 
    and postrenal causes of kidney dysfunction.
    
    The ratio interpretation:
    - Low (<10): May suggest intrinsic renal disease, malnutrition, liver disease, 
      or overhydration
    - Normal (10-20): Indicates healthy kidney function with appropriate filtration
    - High (>20): May indicate prerenal azotemia, GI bleeding, high protein intake, 
      or postrenal obstruction
    
    This calculation is particularly useful in the initial evaluation of acute 
    kidney injury to help determine the underlying cause and guide further 
    diagnostic workup and treatment decisions.
    
    Args:
        request: Parameters needed for BUN Creatinine Ratio calculation
        
    Returns:
        BunCreatinineRatioResponse: Result with clinical interpretation and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("bun_creatinine_ratio", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating BUN Creatinine Ratio",
                    "details": {"parameters": parameters}
                }
            )
        
        return BunCreatinineRatioResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for BUN Creatinine Ratio",
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