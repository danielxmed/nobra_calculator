"""
Horowitz Index for Lung Function (P/F Ratio) Router

Endpoint for calculating Horowitz Index score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.horowitz_index import (
    HorowitzIndexRequest,
    HorowitzIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/horowitz_index",
    response_model=HorowitzIndexResponse,
    summary="Calculate Horowitz Index (P/F Ratio)",
    description="Assesses lung function by calculating the ratio of arterial oxygen partial pressure "
                "(PaO2) to fraction of inspired oxygen (FiO2). The P/F ratio, also known as the "
                "Horowitz Index or Carrico Index, is particularly useful in critically ill patients "
                "and is a key component in diagnosing and stratifying ARDS severity. Normal P/F ratio "
                "is >400 mmHg. The Berlin Definition classifies ARDS as: mild (200-300), moderate "
                "(100-200), and severe (≤100). Note that FiO2 must be entered as a decimal fraction "
                "(e.g., 0.5 for 50% oxygen), not as a percentage.",
    response_description="The calculated P/F ratio with ARDS severity classification and clinical interpretation",
    operation_id="horowitz_index"
)
async def calculate_horowitz_index(request: HorowitzIndexRequest):
    """
    Calculates Horowitz Index for Lung Function (P/F Ratio)
    
    Assesses oxygenation status in critically ill patients and helps 
    diagnose and stratify ARDS severity according to Berlin criteria.
    
    Args:
        request: PaO2 (mmHg) from ABG and FiO2 as decimal fraction
        
    Returns:
        HorowitzIndexResponse: P/F ratio with severity classification
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("horowitz_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Horowitz Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return HorowitzIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Horowitz Index calculation",
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