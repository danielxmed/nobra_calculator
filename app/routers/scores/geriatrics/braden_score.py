"""
Braden Score for Pressure Ulcers Router

Endpoint for calculating Braden Score for pressure ulcer risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.geriatrics.braden_score import (
    BradenScoreRequest,
    BradenScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/braden_score",
    response_model=BradenScoreResponse,
    summary="Calculate Braden Score for Pressure Ulcers",
    description="Identifies patients at risk for pressure ulcers by assessing six key factors: sensory perception, moisture, activity, mobility, nutrition, and friction/shear",
    response_description="The calculated braden score with interpretation",
    operation_id="braden_score"
)
async def calculate_braden_score(request: BradenScoreRequest):
    """
    Calculates Braden Score for Pressure Ulcers
    
    Identifies patients at risk for pressure ulcers by assessing six key factors:
    sensory perception, moisture, activity, mobility, nutrition, and friction/shear.
    
    The score ranges from 6-23 points, with lower scores indicating higher risk:
    - 19-23 points: No risk
    - 15-18 points: Mild risk
    - 13-14 points: Moderate risk
    - 10-12 points: High risk
    - ≤9 points: Very high risk
    
    Args:
        request: Parameters for the six Braden subscales
        
    Returns:
        BradenScoreResponse: Total score with risk category and prevention recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("braden_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Braden Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return BradenScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Braden Score",
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