"""
Alc router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology import AlcRequest, AlcResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post(
    "/alc",
    response_model=AlcResponse,
    summary="Calculate Absolute Lymphocyte Count (ALC)",
    description="Assesses lymphocyte count and predicts CD4 count in HIV patients",
    response_description="The calculated alc with interpretation",
    operation_id="calculate_alc"
)
async def calculate_alc(request: AlcRequest):
    """
    Calculate Absolute Lymphocyte Count (ALC) for HIV Monitoring and Immune Assessment
    
    The ALC serves as a surrogate marker for CD4+ T-cell count in HIV patients and provides
    critical information for immune status assessment, particularly in resource-limited settings.
    
    **Clinical Applications:**
    - HIV disease monitoring and staging
    - CD4+ T-cell count prediction when direct testing unavailable
    - Opportunistic infection risk assessment
    - Immune reconstitution evaluation
    - Hematological malignancy monitoring
    
    **Key Features:**
    - Validated correlation with CD4 counts in HIV patients
    - Cost-effective alternative to flow cytometry
    - Useful for monitoring antiretroviral therapy response
    - Guides timing of opportunistic infection prophylaxis
    
    **Interpretation:**
    - ALC <1,000: High likelihood CD4 <200 cells/mm³ (high infection risk)
    - ALC 1,000-2,000: Indeterminate zone, direct CD4 testing needed
    - ALC ≥2,000: High likelihood CD4 ≥200 cells/mm³ (lower infection risk)
    
    Args:
        request: AlcRequest containing white blood cell count and lymphocyte percentage
        
    Returns:
        AlcResponse: Calculated ALC with CD4 prediction and clinical interpretation
        
    Raises:
        422: Validation error for invalid input parameters
        500: Internal calculation error
    """
    try:
        # Convert request to dictionary
        parameters = {
            "wbc_count": request.white_blood_cells,
            "lymphocyte_percent": request.lymphocyte_percentage
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("alc", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ALC",
                    "details": {"parameters": parameters}
                }
            )
        
        return AlcResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ALC",
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