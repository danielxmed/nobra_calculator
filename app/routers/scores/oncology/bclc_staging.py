"""
Barcelona-Clinic Liver Cancer (BCLC) Staging Router

Endpoint for calculating BCLC staging for hepatocellular carcinoma.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.bclc_staging import (
    BclcStagingRequest,
    BclcStagingResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/bclc_staging", response_model=BclcStagingResponse)
async def calculate_bclc_staging(request: BclcStagingRequest):
    """
    Calculates Barcelona-Clinic Liver Cancer (BCLC) Staging Classification
    
    The BCLC staging system is the most widely used staging classification for 
    hepatocellular carcinoma (HCC) as it integrates tumor characteristics, liver 
    function status, and performance status to both stage disease and guide 
    treatment decisions.
    
    Args:
        request: Parameters including performance status, Child-Pugh class, 
                tumor characteristics (size, number, invasion, spread)
        
    Returns:
        BclcStagingResponse: BCLC stage with treatment recommendations and prognosis
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("bclc_staging", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating BCLC staging",
                    "details": {"parameters": parameters}
                }
            )
        
        return BclcStagingResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for BCLC staging",
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