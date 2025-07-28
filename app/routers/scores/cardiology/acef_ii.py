"""ACEF II Risk Score router"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology import AcefIiRequest, AcefIiResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post(
    "/acef_ii",
    response_model=AcefIiResponse,
    summary="Calculate ACEF II Risk Score",
    description="Predicts 30-day mortality after cardiac surgery",
    response_description="Calculated ACEF II score with risk interpretation",
)
async def calculate_acef_ii(request: AcefIiRequest):
    """Calculate ACEF II Risk Score"""
    try:
        params = {
            "age": request.age,
            "ejection_fraction": request.ejection_fraction,
            "serum_creatinine": request.serum_creatinine,
            "emergency_surgery": request.emergency_surgery,
            "hematocrit": request.hematocrit,
        }
        result = calculator_service.calculate_score("acef_ii", params)
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ACEF II",
                    "details": {"parameters": params},
                },
            )
        return AcefIiResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=422, detail={"error": "ValidationError", "message": str(e)})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "InternalServerError", "message": str(e)})
