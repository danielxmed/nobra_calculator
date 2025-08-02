"""
Infant Scalp Score Router

Endpoint for calculating Infant Scalp Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.infant_scalp_score import (
    InfantScalpScoreRequest,
    InfantScalpScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/infant_scalp_score",
    response_model=InfantScalpScoreResponse,
    summary="Calculate Infant Scalp Score",
    description="Calculates the Infant Scalp Score (ISS) for traumatic brain injury risk assessment in infants ≤12 months old with isolated scalp hematoma after head trauma. "
                "This validated clinical tool stratifies risk for clinically important traumatic brain injury (ciTBI) or TBI on CT imaging to help guide neuroimaging decisions. "
                "The score uses three clinical variables: patient age (younger = higher risk), hematoma size (larger = higher risk), and hematoma location (non-frontal = higher risk). "
                "Scores 0-3 indicate low risk where clinical observation may be appropriate, while scores 4-8 indicate high risk requiring strong consideration for cranial CT imaging. "
                "This tool is particularly valuable for avoiding unnecessary radiation exposure in low-risk infants while ensuring appropriate imaging for those at higher risk.",
    response_description="The calculated Infant Scalp Score with risk stratification and clinical management recommendations for neuroimaging decisions",
    operation_id="infant_scalp_score"
)
async def calculate_infant_scalp_score(request: InfantScalpScoreRequest):
    """
    Calculates Infant Scalp Score for traumatic brain injury risk assessment
    
    Assesses risk of TBI in infants ≤12 months with isolated scalp hematoma after head trauma.
    Uses age, hematoma size, and location to stratify risk and guide neuroimaging decisions.
    
    Args:
        request: Parameters needed for ISS calculation (age, hematoma size, location)
        
    Returns:
        InfantScalpScoreResponse: Score with risk category and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("infant_scalp_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Infant Scalp Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return InfantScalpScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Infant Scalp Score",
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