"""
Adverse Childhood Experiences (ACE) Score Router

Endpoint for calculating Adverse Childhood Experiences (ACE) Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.ace_score import (
    AceScoreRequest,
    AceScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ace_score",
    response_model=AceScoreResponse,
    summary="Calculate Adverse Childhood Experiences (ACE) Score",
    description="Screens for adverse childhood experiences to assess risk of health problems in adulthood",
    response_description="The calculated ace score with interpretation",
    operation_id="calculate_ace_score"
)
async def calculate_ace_score(request: AceScoreRequest):
    """
    Calculates Adverse Childhood Experiences (ACE) Score
    
    Screens for adverse childhood experiences to assess risk of health problems 
    in adulthood. The ACE Score is based on the seminal CDC-Kaiser Permanente 
    study that found strong correlations between childhood trauma and adult 
    health outcomes.
    
    The score evaluates 10 categories of adverse experiences during the first 
    18 years of life, including abuse, neglect, and household dysfunction. 
    Each category contributes 1 point to the total score (range 0-10).
    
    Higher scores are associated with increased risks of mental health disorders, 
    substance abuse, chronic diseases, and other health problems in adulthood.
    
    Args:
        request: Parameters needed for ACE Score calculation
        
    Returns:
        AceScoreResponse: Result with clinical interpretation and risk assessment
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ace_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ACE Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return AceScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ACE Score",
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