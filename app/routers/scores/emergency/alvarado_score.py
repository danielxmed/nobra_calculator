"""
Alvarado Score for Acute Appendicitis Router

Endpoint for calculating Alvarado Score for Acute Appendicitis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.alvarado_score import (
    AlvaradoScoreRequest,
    AlvaradoScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/alvarado_score",
    response_model=AlvaradoScoreResponse,
    summary="Calculate Alvarado Score for Acute Appendicitis",
    description="Predicts likelihood of acute appendicitis based on clinical symptoms, signs, and laboratory findings. Uses the MANTRELS mnemonic to assess 8 clinical factors for diagnosis of appendicitis.",
    response_description="The calculated alvarado score with interpretation",
    operation_id="calculate_alvarado_score"
)
async def calculate_alvarado_score(request: AlvaradoScoreRequest):
    """
    Calculates Alvarado Score for Acute Appendicitis
    
    The Alvarado Score is a clinical decision rule that uses 8 clinical variables 
    organized by the MANTRELS mnemonic to assess the probability of acute appendicitis. 
    It helps clinicians determine appropriate management strategies ranging from discharge 
    to immediate surgical consultation based on the calculated risk.
    
    The score ranges from 0-10 points:
    - 0-3 points: Low probability (consider discharge)
    - 4-6 points: Intermediate probability (consider observation/imaging)
    - 7-8 points: High probability (surgical consultation)
    - 9-10 points: Very high probability (immediate surgery consultation)
    
    Args:
        request: MANTRELS clinical parameters for appendicitis assessment
        
    Returns:
        AlvaradoScoreResponse: Score result with clinical interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("alvarado_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Alvarado Score for Acute Appendicitis",
                    "details": {"parameters": parameters}
                }
            )
        
        return AlvaradoScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Alvarado Score for Acute Appendicitis",
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