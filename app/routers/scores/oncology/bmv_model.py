"""
Brain Metastasis Velocity (BMV) Model Router

Endpoint for calculating Brain Metastasis Velocity.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.bmv_model import (
    BmvModelRequest,
    BmvModelResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/bmv_model",
    response_model=BmvModelResponse,
    summary="Calculate Brain Metastasis Velocity (BMV) Model",
    description="Calculates rate of distant brain failure after stereotactic radiosurgery for brain metastasis to predict overall survival",
    response_description="The calculated bmv model with interpretation",
    operation_id="bmv_model"
)
async def calculate_bmv_model(request: BmvModelRequest):
    """
    Calculates Brain Metastasis Velocity (BMV) Model
    
    Calculates the rate of distant brain failure after stereotactic radiosurgery 
    to predict overall survival in patients with brain metastases.
    
    BMV = Number of new brain metastases / Time interval (years)
    
    Risk stratification:
    - Low BMV (<4): Median OS 12.4 months, consider localized therapy
    - Intermediate BMV (4-13): Median OS 8.2 months, individualized approach
    - High BMV (>13): Median OS 4.3 months, consider whole brain RT
    
    Args:
        request: Number of new metastases and time interval since initial SRS
        
    Returns:
        BmvModelResponse: BMV value with risk category and survival estimates
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("bmv_model", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Brain Metastasis Velocity",
                    "details": {"parameters": parameters}
                }
            )
        
        return BmvModelResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for BMV Model",
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