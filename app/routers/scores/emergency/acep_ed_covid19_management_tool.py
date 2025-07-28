"""Router for ACEP ED COVID-19 Management Tool"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency import (
    AcepEdCovid19ManagementToolRequest,
    AcepEdCovid19ManagementToolResponse,
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/acep_ed_covid19_management_tool",
    response_model=AcepEdCovid19ManagementToolResponse,
    summary="ACEP ED COVID-19 Management Tool",
    description="Determines recommended disposition for suspected or confirmed COVID-19 in adults",
    response_description="Disposition recommendation with interpretation",
)
async def calculate_acep_ed_covid19_management_tool(
    request: AcepEdCovid19ManagementToolRequest,
):
    """Calculate ACEP ED COVID-19 Management Tool"""
    try:
        params = {
            "severity": request.severity,
            "priest_score": request.priest_score,
            "risk_factors": request.risk_factors,
            "imaging_concerning": request.imaging_concerning == "yes",
            "labs_concerning": request.labs_concerning == "yes",
            "self_care_capable": request.self_care_capable == "yes",
        }
        result = calculator_service.calculate_score(
            "acep_ed_covid19_management_tool", params
        )
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ACEP ED COVID-19 Management Tool",
                    "details": {"parameters": params},
                },
            )
        return AcepEdCovid19ManagementToolResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={"error": "ValidationError", "message": str(e)},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "InternalServerError", "message": str(e)},
        )
