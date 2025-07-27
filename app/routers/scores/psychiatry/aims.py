"""
Aims router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry import AimsRequest, AimsResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post("/aims", response_model=AimsResponse)
async def calculate_aims(request: AimsRequest):
    """
    Calculates AIMS for tardive dyskinesia assessment
    
    Args:
        request: Parameters required for calculation (involuntary movement assessment items)
        
    Returns:
        AimsResponse: Result with tardive dyskinesia assessment
    """
    try:
        # Convert request to dictionary
        parameters = {
            "facial_muscles": request.facial_muscles,
            "lips_perioral": request.lips_perioral,
            "jaw": request.jaw,
            "tongue": request.tongue,
            "upper_extremities": request.upper_extremities,
            "lower_extremities": request.lower_extremities,
            "trunk_movements": request.trunk_movements,
            "global_severity": request.global_severity,
            "incapacitation": request.incapacitation,
            "patient_awareness": request.patient_awareness,
            "current_problems_teeth": request.current_problems_teeth.value,
            "dental_problems_interfere": request.dental_problems_interfere.value
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("aims", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating AIMS",
                    "details": {"parameters": parameters}
                }
            )
        
        return AimsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for AIMS",
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