"""
Psoriasis Area and Severity Index (PASI) Router

Endpoint for calculating PASI.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.pasi import (
    PasiRequest,
    PasiResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/pasi",
    response_model=PasiResponse,
    summary="Calculate Psoriasis Area and Severity Index (PASI)",
    description="Quantifies the severity of psoriasis by combining assessment of lesion severity "
                "and affected body surface area across four anatomical regions. This gold standard "
                "measurement tool, developed by Fredriksson and Pettersson in 1978, evaluates "
                "erythema (redness), induration (thickness), and desquamation (scaling) in the "
                "head/neck, upper limbs, trunk, and lower limbs regions. The PASI score ranges "
                "from 0-72 points, with higher scores indicating more severe disease. Clinical "
                "severity classifications include mild (<5), moderate (5-10), severe (10-20), "
                "and very severe (>20) psoriasis. This standardized assessment guides treatment "
                "decisions including eligibility for systemic therapies and biologics, monitors "
                "therapeutic response with validated improvement thresholds (PASI 50/75/90/100), "
                "and serves as the primary endpoint in clinical trials. The tool requires trained "
                "clinical assessment for optimal inter-rater reliability and should be interpreted "
                "alongside body surface area, quality of life measures, and patient-reported "
                "outcomes for comprehensive psoriasis management. PASI remains the most widely "
                "used and validated severity measure in dermatology practice worldwide, "
                "facilitating evidence-based treatment selection and outcome monitoring.",
    response_description="The calculated PASI score with severity classification and comprehensive treatment guidance",
    operation_id="pasi"
)
async def calculate_pasi(request: PasiRequest):
    """
    Calculates Psoriasis Area and Severity Index (PASI)
    
    This standardized tool quantifies psoriasis severity by evaluating clinical
    features across four body regions to guide treatment decisions.
    
    Args:
        request: Clinical assessment parameters for erythema, induration, 
                desquamation, and area involvement in each body region
        
    Returns:
        PasiResponse: Result with PASI score and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("pasi", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating PASI",
                    "details": {"parameters": parameters}
                }
            )
        
        return PasiResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for PASI",
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