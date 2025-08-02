"""
Karnofsky Performance Status Scale Router

Endpoint for calculating Karnofsky Performance Status Scale.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.karnofsky_performance_status import (
    KarnofskyPerformanceStatusRequest,
    KarnofskyPerformanceStatusResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/karnofsky_performance_status",
    response_model=KarnofskyPerformanceStatusResponse,
    summary="Calculate Karnofsky Performance Status Scale",
    description="Calculates the Karnofsky Performance Status Scale, a widely used tool in oncology to assess "
                "a patient's functional status and ability to tolerate cancer treatments. The scale ranges from "
                "0% (death) to 100% (normal activity with no symptoms) in 10% increments. Higher scores indicate "
                "better functional status and greater ability to tolerate aggressive treatments. This validated "
                "scale correlates with treatment tolerance, survival outcomes, and quality of life measures in "
                "cancer patients. Originally developed in 1949, it remains a standard assessment tool for treatment "
                "eligibility, clinical trial enrollment, and prognosis evaluation.",
    response_description="The Karnofsky Performance Status with functional assessment, treatment eligibility, and clinical recommendations",
    operation_id="karnofsky_performance_status"
)
async def calculate_karnofsky_performance_status(request: KarnofskyPerformanceStatusRequest):
    """
    Calculates Karnofsky Performance Status Scale
    
    The Karnofsky Performance Status Scale assesses functional status in cancer patients
    using an 11-point scale (0-100% in 10% increments). It provides valuable information
    for treatment planning, prognosis assessment, and quality of life evaluation.
    
    Clinical Applications:
    - Treatment eligibility assessment (especially for clinical trials)
    - Chemotherapy tolerance prediction
    - Prognosis evaluation and survival prediction
    - Quality of life assessment
    - Treatment intensity decisions
    
    Interpretation Guidelines:
    - 80-100%: Excellent performance status, suitable for aggressive treatments
    - 60-70%: Good performance status, suitable for standard treatments
    - 40-50%: Poor performance status, consider palliative treatments
    - 10-30%: Very poor performance status, focus on comfort care
    - 0%: Death
    
    Args:
        request: Karnofsky Performance Status parameters
        
    Returns:
        KarnofskyPerformanceStatusResponse: Performance status with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("karnofsky_performance_status", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Karnofsky Performance Status Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return KarnofskyPerformanceStatusResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Karnofsky Performance Status Scale",
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