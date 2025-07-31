"""
Neck Disability Index (NDI) Router

Endpoint for calculating Neck Disability Index.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.ndi import (
    NdiRequest,
    NdiResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ndi",
    response_model=NdiResponse,
    summary="Calculate Neck Disability Index (NDI)",
    description="Assesses disability in patients with neck pain across 10 functional domains",
    response_description="The calculated ndi with interpretation",
    operation_id="ndi"
)
async def calculate_ndi(request: NdiRequest):
    """
    Calculates Neck Disability Index (NDI)
    
    Assesses disability in patients with neck pain across 10 functional domains.
    The NDI is the most widely used patient-reported outcome measure for neck pain.
    
    Args:
        request: Parameters needed for calculation (10 domain scores, each 0-5)
        
    Returns:
        NdiResponse: Result with disability level interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ndi", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Neck Disability Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return NdiResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Neck Disability Index",
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