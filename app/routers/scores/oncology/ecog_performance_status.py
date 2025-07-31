"""
Eastern Cooperative Oncology Group (ECOG) Performance Status Router

Endpoint for calculating ECOG Performance Status.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.ecog_performance_status import (
    EcogPerformanceStatusRequest,
    EcogPerformanceStatusResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ecog_performance_status",
    response_model=EcogPerformanceStatusResponse,
    summary="Calculate Eastern Cooperative Oncology Group",
    description="Determines patient's ability to tolerate therapies in severe illness, specifically for chemotherapy. Simple 5-point scale that describes patient's level of functioning in terms of their ability to care for themselves, daily activity, and physical ability.",
    response_description="The calculated ecog performance status with interpretation",
    operation_id="calculate_ecog_performance_status"
)
async def calculate_ecog_performance_status(request: EcogPerformanceStatusRequest):
    """
    Calculates Eastern Cooperative Oncology Group (ECOG) Performance Status
    
    The ECOG Performance Status is a fundamental assessment tool in oncology that 
    describes a patient's level of functioning in terms of their ability to care 
    for themselves, daily activity, and physical ability. This simple 5-point scale 
    (0-4) is critical for determining treatment eligibility, prognosis, and care 
    planning in cancer patients.
    
    Args:
        request: Parameters needed for assessment including the patient's current 
                performance status level based on functional assessment
        
    Returns:
        EcogPerformanceStatusResponse: Result with clinical interpretation and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ecog_performance_status", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ECOG Performance Status",
                    "details": {"parameters": parameters}
                }
            )
        
        return EcogPerformanceStatusResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ECOG Performance Status",
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