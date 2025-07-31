"""
ATRIA Bleeding Risk Score Router

Endpoint for calculating ATRIA Bleeding Risk Score for patients on warfarin.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.atria_bleeding import (
    AtriaBleedingRequest,
    AtriaBleedingResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/atria_bleeding",
    response_model=AtriaBleedingResponse,
    summary="Calculate ATRIA Bleeding Risk Score",
    description="Determines bleeding risk for patients on warfarin therapy for atrial fibrillation. The score was developed and validated in the ATRIA (Anticoagulation and Risk Factors in Atrial Fibrillation) cohort and helps stratify patients into low, intermediate, and high risk categories for major hemorrhage.",
    response_description="The calculated atria bleeding with interpretation",
    operation_id="calculate_atria_bleeding"
)
async def calculate_atria_bleeding(request: AtriaBleedingRequest):
    """
    Calculates ATRIA Bleeding Risk Score
    
    Determines bleeding risk for patients on warfarin therapy for atrial fibrillation.
    The score stratifies patients into low (<1%), intermediate (2.6%), or high (5.8%)
    annual major hemorrhage risk categories.
    
    Args:
        request: Clinical parameters for ATRIA bleeding risk calculation
        
    Returns:
        AtriaBleedingResponse: Calculated score with risk stratification and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("atria_bleeding", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ATRIA Bleeding Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return AtriaBleedingResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ATRIA Bleeding Risk Score",
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