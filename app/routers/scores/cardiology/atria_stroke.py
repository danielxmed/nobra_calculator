"""
ATRIA Stroke Risk Score Router

Endpoint for calculating ATRIA Stroke Risk Score for patients with atrial fibrillation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.atria_stroke import (
    AtriaStrokeRequest,
    AtriaStrokeResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/atria_stroke",
    response_model=AtriaStrokeResponse,
    summary="Calculate ATRIA Stroke Risk Score",
    description="Determines stroke risk in patients with atrial fibrillation. The ATRIA (Anticoagulation and Risk Factors in Atrial Fibrillation) stroke risk score predicts ischemic stroke and other thromboembolism in patients with atrial fibrillation, helping guide anticoagulation decisions.",
    response_description="The calculated atria stroke with interpretation",
    operation_id="calculate_atria_stroke"
)
async def calculate_atria_stroke(request: AtriaStrokeRequest):
    """
    Calculates ATRIA Stroke Risk Score
    
    Determines stroke risk in patients with atrial fibrillation. The ATRIA score
    predicts ischemic stroke and systemic thromboembolism, stratifying patients
    into low (<1%), intermediate (1-<2%), or high (≥2%) annual stroke risk categories.
    
    Args:
        request: Clinical parameters for ATRIA stroke risk calculation
        
    Returns:
        AtriaStrokeResponse: Calculated score with risk stratification and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("atria_stroke", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ATRIA Stroke Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return AtriaStrokeResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ATRIA Stroke Risk Score",
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