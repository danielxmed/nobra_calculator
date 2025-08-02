"""
Prostate Tumor Volume & Density Router

Endpoint for calculating Prostate Tumor Volume & Density.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.prostate_tumor_volume_density import (
    ProstateTumorVolumeDensityRequest,
    ProstateTumorVolumeDensityResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/prostate_tumor_volume_density",
    response_model=ProstateTumorVolumeDensityResponse,
    summary="Calculate Prostate Tumor Volume & Density",
    description="Calculates prostate volume using the ellipsoid formula and PSA density to help "
                "distinguish between benign prostatic hyperplasia (BPH) and prostate cancer. "
                "This essential urological tool uses three prostate dimensions (length, width, height) "
                "and serum PSA levels to compute prostate volume and PSA density. The ellipsoid "
                "formula (Length × Width × Height × π/6) provides accurate volume estimates "
                "validated against surgical specimens. PSA density (PSA ÷ Volume) enhances "
                "diagnostic accuracy beyond PSA alone, particularly in the 4-10 ng/mL 'gray zone' "
                "where cancer risk is uncertain. Risk stratification includes low (<0.10), "
                "intermediate (0.10-0.15), high (0.15-0.20), and very high (>0.20 ng/mL²) "
                "categories guiding biopsy decisions. This tool assists in treatment planning, "
                "active surveillance decisions, and patient counseling by providing objective "
                "risk assessment based on validated clinical thresholds.",
    response_description="The calculated prostate volume and PSA density with comprehensive risk stratification",
    operation_id="prostate_tumor_volume_density"
)
async def calculate_prostate_tumor_volume_density(request: ProstateTumorVolumeDensityRequest):
    """
    Calculates Prostate Tumor Volume & Density
    
    This tool helps assess prostate cancer risk by calculating prostate volume
    and PSA density to guide biopsy decisions and treatment planning.
    
    Args:
        request: Prostate dimensions (length, width, height) and PSA value
        
    Returns:
        ProstateTumorVolumeDensityResponse: Result with volume, PSA density, and risk assessment
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("prostate_tumor_volume_density", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Prostate Tumor Volume & Density",
                    "details": {"parameters": parameters}
                }
            )
        
        return ProstateTumorVolumeDensityResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Prostate Tumor Volume & Density",
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