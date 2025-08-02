"""
Multiple Myeloma International Staging System (ISS) Router

Endpoint for calculating ISS staging for multiple myeloma patients based on
serum β2 microglobulin and albumin levels.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.multiple_myeloma_iss import (
    MultipleMyelomaIssRequest,
    MultipleMyelomaIssResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/multiple_myeloma_iss",
    response_model=MultipleMyelomaIssResponse,
    summary="Calculate Multiple Myeloma ISS Stage",
    description="Calculates the International Staging System (ISS) stage for multiple myeloma patients using "
                "serum β2 microglobulin and albumin levels. This validated prognostic staging system classifies "
                "patients into three stages with distinct survival outcomes: Stage I (best prognosis, 62 months "
                "median survival), Stage II (intermediate prognosis, 44 months), and Stage III (poorest prognosis, "
                "29 months). The ISS is simpler and more objective than previous staging systems, using only two "
                "readily available laboratory parameters. It should only be used for newly diagnosed multiple "
                "myeloma patients and helps guide treatment planning and prognosis counseling.",
    response_description="ISS stage classification with detailed prognostic interpretation and clinical management recommendations",
    operation_id="multiple_myeloma_iss"
)
async def calculate_multiple_myeloma_iss(request: MultipleMyelomaIssRequest):
    """
    Calculates Multiple Myeloma International Staging System (ISS) Stage
    
    The ISS is a simple, reproducible staging system for multiple myeloma based on
    serum β2 microglobulin and albumin levels. It provides superior prognostic
    information compared to previous staging systems and helps guide treatment decisions.
    
    Args:
        request: Laboratory parameters including serum β2 microglobulin and albumin levels
        
    Returns:
        MultipleMyelomaIssResponse: ISS stage with prognostic information and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("multiple_myeloma_iss", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Multiple Myeloma ISS Stage",
                    "details": {"parameters": parameters}
                }
            )
        
        return MultipleMyelomaIssResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Multiple Myeloma ISS",
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