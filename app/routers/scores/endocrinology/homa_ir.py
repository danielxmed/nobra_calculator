"""
HOMA-IR (Homeostatic Model Assessment for Insulin Resistance) Router

Endpoint for calculating HOMA-IR score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.homa_ir import (
    HomaIrRequest,
    HomaIrResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/homa_ir",
    response_model=HomaIrResponse,
    summary="Calculate HOMA-IR Score",
    description="Approximates insulin resistance using fasting glucose and insulin levels. "
                "HOMA-IR (Homeostatic Model Assessment for Insulin Resistance) is a simple, "
                "non-invasive method to quantify insulin resistance from fasting laboratory values. "
                "The formula multiplies fasting insulin (μIU/mL) by fasting glucose (mg/dL) and "
                "divides by 405. Normal range is typically 0.7-2.0, with values >2.0 suggesting "
                "insulin resistance and increased risk for type 2 diabetes and metabolic syndrome. "
                "Should NOT be used in patients on insulin therapy.",
    response_description="The calculated HOMA-IR score with interpretation and risk stratification",
    operation_id="homa_ir"
)
async def calculate_homa_ir(request: HomaIrRequest):
    """
    Calculates HOMA-IR (Homeostatic Model Assessment for Insulin Resistance)
    
    Approximates insulin resistance to identify individuals at risk for 
    type 2 diabetes and metabolic syndrome.
    
    Args:
        request: Fasting insulin (μIU/mL) and fasting glucose (mg/dL) values
        
    Returns:
        HomaIrResponse: HOMA-IR score with interpretation and risk category
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("homa_ir", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HOMA-IR score",
                    "details": {"parameters": parameters}
                }
            )
        
        return HomaIrResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HOMA-IR calculation",
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