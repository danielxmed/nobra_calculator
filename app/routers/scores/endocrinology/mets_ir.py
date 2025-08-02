"""
METS-IR Router

Endpoint for calculating Metabolic Score for Insulin Resistance.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.mets_ir import (
    MetsIrRequest,
    MetsIrResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mets_ir",
    response_model=MetsIrResponse,
    summary="Calculate Metabolic Score for Insulin Resistance (METS-IR)",
    description="Calculates the METS-IR to assess insulin resistance and predict type 2 diabetes "
                "risk using routine metabolic parameters. This non-insulin dependent marker uses "
                "fasting glucose, triglycerides, BMI, and HDL cholesterol in a logarithmic formula: "
                "(ln((2 × Glucose) + Triglycerides) × BMI) / ln(HDL). The score predicts visceral "
                "adiposity and incident type 2 diabetes with a cutoff of 50.39 distinguishing low "
                "risk (≤50.39) from high risk (>50.39) individuals. Developed and validated in "
                "Mexican and Asian populations, METS-IR offers a practical alternative to HOMA-IR "
                "for primary care settings where insulin measurements may not be readily available. "
                "The score has shown good correlation with metabolic syndrome components and "
                "cardiovascular risk. Note: All measurements should be taken in fasting state, and "
                "the score may need validation in other ethnic populations.",
    response_description="The calculated METS-IR score with risk stratification and clinical recommendations",
    operation_id="mets_ir"
)
async def calculate_mets_ir(request: MetsIrRequest):
    """
    Calculates METS-IR for insulin resistance and diabetes risk assessment
    
    This practical tool helps identify individuals at high risk for type 2 diabetes
    using readily available metabolic parameters without requiring insulin measurements.
    
    Args:
        request: Fasting glucose, triglycerides, BMI, and HDL cholesterol values
        
    Returns:
        MetsIrResponse: METS-IR score with risk interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mets_ir", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating METS-IR",
                    "details": {"parameters": parameters}
                }
            )
        
        return MetsIrResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for METS-IR",
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