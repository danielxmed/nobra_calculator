"""
Age-Adjusted ESR/CRP for Rheumatoid Arthritis Router

Endpoint for calculating age-adjusted ESR and CRP upper limits.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.age_adjusted_esr_crp import (
    AgeAdjustedEsrCrpRequest,
    AgeAdjustedEsrCrpResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/age_adjusted_esr_crp", response_model=AgeAdjustedEsrCrpResponse)
async def calculate_age_adjusted_esr_crp(request: AgeAdjustedEsrCrpRequest):
    """
    Calculates Age-Adjusted ESR/CRP for Rheumatoid Arthritis
    
    Calculates age-adjusted ESR and CRP upper limits to account for the natural 
    increase in inflammatory markers with aging. This evidence-based approach 
    helps distinguish true disease activity from age-related increases, particularly 
    important in elderly patients with rheumatoid arthritis.
    
    The calculator uses validated formulas that account for both age and sex:
    - ESR: Male = Age ÷ 2, Female = (Age + 10) ÷ 2 mm/hr
    - CRP: Male = Age ÷ 50, Female = (Age ÷ 50) + 0.6 mg/dL
    
    Key Benefits:
    - Age-specific interpretation of inflammatory markers
    - Reduces overestimation of disease activity in elderly patients
    - Evidence-based approach validated in RA patients
    - Accounts for sex-specific differences in inflammatory markers
    
    Clinical Applications:
    - Disease activity assessment in rheumatoid arthritis
    - Monitoring treatment response in elderly patients
    - Distinguishing active inflammation from age-related increases
    - Supporting clinical decision-making in RA management
    
    Args:
        request: Parameters needed for age-adjusted ESR/CRP calculation
        
    Returns:
        AgeAdjustedEsrCrpResponse: Age-adjusted limits with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("age_adjusted_esr_crp", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Age-Adjusted ESR/CRP",
                    "details": {"parameters": parameters}
                }
            )
        
        return AgeAdjustedEsrCrpResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Age-Adjusted ESR/CRP",
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