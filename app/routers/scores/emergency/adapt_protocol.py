"""
ADAPT Protocol Router

Endpoint for calculating ADAPT Protocol for Cardiac Event Risk.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.adapt_protocol import (
    AdaptProtocolRequest,
    AdaptProtocolResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/adapt_protocol", response_model=AdaptProtocolResponse)
async def calculate_adapt_protocol(request: AdaptProtocolRequest):
    """
    Calculates ADAPT Protocol for Cardiac Event Risk
    
    The ADAPT Protocol (Accelerated Diagnostic Protocol to Assess Patients with Chest Pain 
    Symptoms Using Contemporary Troponins as the Only Biomarker) assesses chest pain patients 
    at 2 hours for risk of cardiac event. It uses a binary decision tree approach to stratify 
    patients into low risk (0-0.3% risk of major cardiac event in 30 days) or high risk 
    categories based on troponin levels, ECG changes, and TIMI risk factors.
    
    Args:
        request: Parameters needed for calculation including troponin levels,
                ECG changes, and TIMI risk factors
        
    Returns:
        AdaptProtocolResponse: Result with clinical interpretation and risk stratification
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("adapt_protocol", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ADAPT Protocol",
                    "details": {"parameters": parameters}
                }
            )
        
        return AdaptProtocolResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ADAPT Protocol",
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