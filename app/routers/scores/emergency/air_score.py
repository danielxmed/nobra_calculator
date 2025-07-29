"""
Appendicitis Inflammatory Response (AIR) Score Router

Endpoint for calculating Appendicitis Inflammatory Response (AIR) Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.air_score import (
    AirScoreRequest,
    AirScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/air_score", response_model=AirScoreResponse)
async def calculate_air_score(request: AirScoreRequest):
    """
    Calculates Appendicitis Inflammatory Response (AIR) Score
    
    The AIR Score diagnoses appendicitis based on clinical and laboratory findings 
    using seven variables: vomiting, right iliac fossa pain, rebound tenderness, 
    fever, polymorphonuclear leukocyte percentage, white blood cell count, and 
    C-reactive protein level.
    
    The score is designed with high sensitivity for advanced appendicitis, which 
    is most clinically important to identify. It uses objective inflammatory 
    variables and clinical signs of peritoneal irritation to provide three risk 
    categories:
    
    - Low Risk (0-4 points): Outpatient follow-up if unaltered general condition
    - Indeterminate Risk (5-8 points): Admit for observation and serial reassessment
    - High Risk (9-12 points): Surgical consultation recommended
    
    The score performs well across age groups from 2-96 years and is particularly 
    effective in children and women, though may be less specific in elderly patients.
    
    Args:
        request: Clinical and laboratory parameters needed for AIR Score calculation
        
    Returns:
        AirScoreResponse: AIR Score result with risk stratification and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("air_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Appendicitis Inflammatory Response (AIR) Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return AirScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Appendicitis Inflammatory Response (AIR) Score",
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
