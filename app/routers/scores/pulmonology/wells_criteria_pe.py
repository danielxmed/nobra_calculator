"""
Wells' Criteria for Pulmonary Embolism Router

Endpoint for calculating Wells' Criteria for PE probability assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.wells_criteria_pe import (
    WellsCriteriaPeRequest,
    WellsCriteriaPeResponse,
)
from app.services.calculator_service import calculator_service


router = APIRouter()


@router.post(
    "/wells_criteria_pe",
    response_model=WellsCriteriaPeResponse,
    summary="Calculate Wells' Criteria for Pulmonary Embolism",
    description=(
        "Clinical pretest probability score for pulmonary embolism using seven bedside criteria; "
        "supports both 3-tier (low/intermediate/high) and 2-tier (PE unlikely/likely) interpretations "
        "to guide D-dimer testing and imaging decisions"
    ),
    response_description="The calculated Wells criteria PE score with interpretation",
    operation_id="wells_criteria_pe",
)
async def calculate_wells_criteria_pe(request: WellsCriteriaPeRequest):
    """
    Calculates Wells' Criteria for Pulmonary Embolism

    Provides the Wells score with detailed clinical interpretation aligned with 3-tier
    and 2-tier frameworks to guide diagnostic testing (D-dimer) and imaging (CT-PA).
    """
    try:
        parameters = request.dict()
        result = calculator_service.calculate_score("wells_criteria_pe", parameters)

        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Wells' Criteria for PE",
                    "details": {"parameters": parameters},
                },
            )

        return WellsCriteriaPeResponse(**result)

    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Wells' Criteria calculation",
                "details": {"error": str(e)},
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Internal error in Wells' Criteria calculation",
                "details": {"error": str(e)},
            },
        )

