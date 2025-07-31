"""
Hamilton Anxiety Scale Router

Endpoint for calculating Hamilton Anxiety Scale (HAM-A).
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.hamilton_anxiety_scale import (
    HamiltonAnxietyScaleRequest,
    HamiltonAnxietyScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hamilton_anxiety_scale",
    response_model=HamiltonAnxietyScaleResponse,
    summary="Calculate Hamilton Anxiety Scale",
    description="Rates level of anxiety based on clinical questions. Assesses the severity of anxiety symptoms across 14 domains in patients already diagnosed with anxiety disorders.",
    response_description="The calculated hamilton anxiety scale with interpretation",
    operation_id="hamilton_anxiety_scale"
)
async def calculate_hamilton_anxiety_scale(request: HamiltonAnxietyScaleRequest):
    """
    Calculates Hamilton Anxiety Scale (HAM-A)
    
    The HAM-A is a clinician-rated scale that assesses the severity of anxiety 
    symptoms across 14 domains. Each item is rated 0-4 (not present to very severe), 
    with a total score range of 0-56. It's widely used for monitoring treatment 
    response and assessing symptom severity in patients with anxiety disorders.
    
    Args:
        request: Parameters for each of the 14 anxiety symptom domains
        
    Returns:
        HamiltonAnxietyScaleResponse: Result with anxiety severity level
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hamilton_anxiety_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Hamilton Anxiety Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return HamiltonAnxietyScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Hamilton Anxiety Scale",
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