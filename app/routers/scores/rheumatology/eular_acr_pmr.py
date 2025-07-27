"""
Eular Acr Pmr router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology import EularAcrPmrRequest, EularAcrPmrResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post("/eular_acr_2012_pmr", response_model=EularAcrPmrResponse)
async def calculate_eular_acr_2012_pmr(request: EularAcrPmrRequest):
    """
    Calculates EULAR/ACR 2012 PMR Classification Criteria
    
    Args:
        request: Parameters for PMR diagnosis
        
    Returns:
        EularAcrPmrResponse: Result with diagnostic probability
    """
    try:
        parameters = {
            "morning_stiffness": request.morning_stiffness.value,
            "hip_pain_limited_rom": request.hip_pain_limited_rom.value,
            "rf_or_acpa": request.rf_or_acpa.value,
            "other_joint_pain": request.other_joint_pain.value,
            "ultrasound_shoulder_hip": request.ultrasound_shoulder_hip.value,
            "ultrasound_both_shoulders": request.ultrasound_both_shoulders.value
        }
        
        result = calculator_service.calculate_score("eular_acr_2012_pmr", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating EULAR/ACR PMR",
                    "details": {"parameters": parameters}
                }
            )
        
        return EularAcrPmrResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for EULAR/ACR PMR",
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