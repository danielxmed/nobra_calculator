"""
MDRD GFR Equation Router

Endpoint for calculating MDRD GFR.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.mdrd_gfr import (
    MdrdGfrRequest,
    MdrdGfrResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mdrd_gfr",
    response_model=MdrdGfrResponse,
    summary="Calculate MDRD GFR Equation",
    description="Calculates the estimated glomerular filtration rate (eGFR) using the MDRD "
                "(Modification of Diet in Renal Disease) equation. This equation estimates kidney "
                "function based on serum creatinine, age, sex, and race. The MDRD equation uses "
                "IDMS-traceable creatinine values and is normalized to 1.73 m² body surface area. "
                "While widely used, it's less accurate for GFR >60 mL/min/1.73 m² and tends to "
                "underestimate GFR in healthy individuals. The NKF/ASN now recommends the CKD-EPI "
                "2021 equation for improved accuracy and removal of race-based adjustments. Results "
                "are categorized into CKD stages (G1-G5) with specific monitoring and referral "
                "recommendations for each stage.",
    response_description="The calculated eGFR with CKD stage classification and clinical recommendations",
    operation_id="mdrd_gfr"
)
async def calculate_mdrd_gfr(request: MdrdGfrRequest):
    """
    Calculates MDRD GFR Equation
    
    The MDRD equation estimates kidney function for chronic kidney disease assessment
    and staging. It's particularly useful for patients with reduced kidney function
    but less accurate at higher GFR levels.
    
    Args:
        request: Serum creatinine, age, sex, and race parameters
        
    Returns:
        MdrdGfrResponse: Calculated eGFR with CKD stage and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mdrd_gfr", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MDRD GFR",
                    "details": {"parameters": parameters}
                }
            )
        
        return MdrdGfrResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MDRD GFR calculation",
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