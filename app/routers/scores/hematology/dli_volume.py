"""
Donor Lymphocyte Infusion (DLI) Volume Router

Endpoint for calculating DLI Volume.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.dli_volume import (
    DliVolumeRequest,
    DliVolumeResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/dli_volume",
    response_model=DliVolumeResponse,
    summary="Calculate Donor Lymphocyte Infusion (DLI) Volume",
    description="Estimates total blood volume to process by apheresis to produce appropriate DLI dosage",
    response_description="The calculated dli volume with interpretation",
    operation_id="calculate_dli_volume"
)
async def calculate_dli_volume(request: DliVolumeRequest):
    """
    Calculates Donor Lymphocyte Infusion (DLI) Volume
    
    Estimates total blood volume to process by apheresis to produce appropriate DLI dosage.
    DLI is used primarily in allogeneic stem cell transplant recipients to treat disease 
    relapse by harnessing the graft-versus-leukemia effect.
    
    Args:
        request: Parameters needed for calculation including recipient weight, CD3+ dose,
                donor parameters, and collection efficiency
        
    Returns:
        DliVolumeResponse: Blood volume result with clinical interpretation and procedure recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("dli_volume", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating DLI Volume",
                    "details": {"parameters": parameters}
                }
            )
        
        return DliVolumeResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for DLI Volume",
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