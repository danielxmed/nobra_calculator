"""
CAGE Questions for Alcohol Use Router

Endpoint for calculating CAGE Questions for Alcohol Use.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.cage_questions import (
    CageQuestionsRequest,
    CageQuestionsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/cage_questions",
    response_model=CageQuestionsResponse,
    summary="Calculate CAGE Questions for Alcohol Use",
    description="Screens for excessive drinking and alcoholism. The CAGE questionnaire is a 4-question screening tool used to help assess a patient's alcohol use and determine if they have an alcohol use disorder.",
    response_description="The calculated cage questions with interpretation",
    operation_id="cage_questions"
)
async def calculate_cage_questions(request: CageQuestionsRequest):
    """
    Calculates CAGE Questions for Alcohol Use
    
    Screens for excessive drinking and alcoholism using a validated 4-question tool.
    The CAGE questionnaire has >90% sensitivity for alcohol disorders when scoring
    2 or more points. Each "yes" answer scores 1 point.
    
    The acronym CAGE stands for:
    - Cut down: Recognition of problematic drinking
    - Annoyed: Defensive reactions to feedback
    - Guilty: Emotional consequences of drinking
    - Eye-opener: Physical dependence indicator
    
    Special consideration: A positive eye-opener response alone warrants concern
    for physical dependence even with an otherwise negative screen.
    
    This is a screening tool, not a diagnostic test. Positive screens should
    prompt further evaluation with tools like AUDIT or clinical interview.
    
    Args:
        request: CAGE Questions parameters (4 yes/no questions)
        
    Returns:
        CageQuestionsResponse: Score (0-4) with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cage_questions", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CAGE Questions score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CageQuestionsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CAGE Questions",
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