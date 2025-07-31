"""
Calcium Correction for Hypoalbuminemia and Hyperalbuminemia Router

Endpoint for calculating Calcium Correction.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.calcium_correction import (
    CalciumCorrectionRequest,
    CalciumCorrectionResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/calcium_correction",
    response_model=CalciumCorrectionResponse,
    summary="Calculate Calcium Correction for Hypoalbuminemia and Hype...",
    description="Calculates corrected calcium level for patients with hypoalbuminemia or hyperalbuminemia",
    response_description="The calculated calcium correction with interpretation",
    operation_id="calcium_correction"
)
async def calculate_calcium_correction(request: CalciumCorrectionRequest):
    """
    Calculates Calcium Correction for Hypoalbuminemia and Hyperalbuminemia
    
    Adjusts total serum calcium for abnormal albumin levels using the classic 
    Payne formula. Approximately 40% of serum calcium is bound to albumin, so 
    abnormal albumin levels can affect total calcium measurements.
    
    The formula corrects calcium to what it would be if albumin were normal:
    - US: Corrected Ca = [0.8 × (4 - Patient's Albumin)] + Serum Ca
    - SI: Corrected Ca = Total Ca + 0.02 × (40 - Albumin)
    
    Important limitations:
    - Formula accuracy is limited, especially in CKD/ESRD
    - Ionized calcium measurement is preferred when available
    - Recent evidence suggests abandoning correction formulas
    - Should not replace clinical judgment
    
    Args:
        request: Calcium and albumin values with unit system
        
    Returns:
        CalciumCorrectionResponse: Corrected calcium with interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("calcium_correction", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating calcium correction",
                    "details": {"parameters": parameters}
                }
            )
        
        return CalciumCorrectionResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for calcium correction",
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