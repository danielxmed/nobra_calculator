"""
Helps2B router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.infectious_disease import Helps2bRequest, Helps2bResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post("/helps2b", response_model=Helps2bResponse)
async def calculate_helps2b(request: Helps2bRequest):
    """
    Calculates 2HELPS2B Score for seizure risk in cEEG
    
    Args:
        request: Clinical and EEG parameters
        
    Returns:
        Helps2bResponse: Result with seizure risk
    """
    try:
        parameters = {
            "seizure_history": request.seizure_history.value,
            "epileptiform_discharges": request.epileptiform_discharges.value,
            "lateralized_periodic_discharges": request.lateralized_periodic_discharges.value,
            "bilateral_independent_periodic_discharges": request.bilateral_independent_periodic_discharges.value,
            "brief_potentially_ictal_rhythmic_discharges": request.brief_potentially_ictal_rhythmic_discharges.value,
            "burst_suppression": request.burst_suppression.value
        }
        
        result = calculator_service.calculate_score("helps2b", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HElPS2B",
                    "details": {"parameters": parameters}
                }
            )
        
        return Helps2bResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HElPS2B",
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