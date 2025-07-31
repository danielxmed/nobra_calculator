"""
Age-Adjusted D-dimer for Venous Thromboembolism (VTE) Router

Endpoint for calculating Age-Adjusted D-dimer cutoffs.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.age_adjusted_d_dimer import (
    AgeAdjustedDDimerRequest,
    AgeAdjustedDDimerResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/age_adjusted_d_dimer",
    response_model=AgeAdjustedDDimerResponse,
    summary="Calculate Age-Adjusted D-dimer for Venous Thromboembolism",
    description="Adjusts D-dimer cutoffs to help rule out VTE in patients ≥50 years old, improving specificity while maintaining sensitivity",
    response_description="The calculated age adjusted d dimer with interpretation",
    operation_id="age_adjusted_d_dimer"
)
async def calculate_age_adjusted_d_dimer(request: AgeAdjustedDDimerRequest):
    """
    Calculates Age-Adjusted D-dimer for Venous Thromboembolism (VTE)
    
    Adjusts D-dimer cutoff values based on patient age to improve specificity 
    in patients ≥50 years old while maintaining sensitivity for VTE detection. 
    This evidence-based approach helps reduce unnecessary imaging studies in 
    elderly patients with suspected VTE.
    
    The age-adjusted approach has been validated in multiple large studies 
    including the ADJUST-PE study and systematic reviews, showing improved 
    diagnostic accuracy in elderly patients.
    
    Key Benefits:
    - Improved specificity in elderly patients (≥50 years)
    - Reduced false positive rates and unnecessary imaging
    - Maintained sensitivity for VTE detection
    - Cost-effective diagnostic approach
    
    Formula:
    - FEU (Fibrinogen Equivalent Units): Age × 10 µg/L
    - DDU (D-dimer Units): Age × 5 µg/L
    
    Args:
        request: Parameters needed for age-adjusted D-dimer calculation
        
    Returns:
        AgeAdjustedDDimerResponse: Age-adjusted cutoff with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("age_adjusted_d_dimer", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Age-Adjusted D-dimer",
                    "details": {"parameters": parameters}
                }
            )
        
        return AgeAdjustedDDimerResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Age-Adjusted D-dimer",
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