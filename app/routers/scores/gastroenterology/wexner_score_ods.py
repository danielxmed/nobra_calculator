"""
Wexner Score for Obstructed Defecation Syndrome (ODS) Router

Endpoint for calculating the Wexner Score for fecal incontinence severity assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.wexner_score_ods import (
    WexnerScoreOdsRequest,
    WexnerScoreOdsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/wexner_score_ods",
    response_model=WexnerScoreOdsResponse,
    summary="Calculate Wexner Score for Obstructed Defecation Syndrome",
    description="Calculates the Wexner Score (Cleveland Clinic Fecal Incontinence Score) for assessing "
                "fecal incontinence severity in patients with obstructed defecation syndrome. This validated "
                "scoring system evaluates five key aspects of incontinence using a standardized 5-point "
                "frequency scale, providing objective assessment of symptom severity and impact on quality "
                "of life. Scores range from 0 (perfect continence) to 20 (complete incontinence), with "
                "scores ≥10 indicating clinically significant incontinence requiring active management.",
    response_description="The calculated Wexner Score with severity classification and clinical management recommendations",
    operation_id="wexner_score_ods"
)
async def calculate_wexner_score_ods(request: WexnerScoreOdsRequest):
    """
    Calculates Wexner Score for Obstructed Defecation Syndrome (ODS)
    
    The Wexner Score is the most widely used and validated scoring system for assessing 
    fecal incontinence severity. It evaluates five parameters (solid stool incontinence, 
    liquid stool incontinence, gas incontinence, protective pad use, and lifestyle impact) 
    using a standardized frequency scale.
    
    Clinical Applications:
    - Assessment of fecal incontinence severity
    - Treatment planning and monitoring
    - Quality of life impact evaluation
    - Research and clinical trials
    
    Interpretation:
    - 0 points: Perfect continence (no treatment needed)
    - 1-9 points: Mild incontinence (conservative management)
    - 10-20 points: Clinical incontinence (requires active management)
    
    Args:
        request: Parameters including frequency scores for each incontinence aspect
        
    Returns:
        WexnerScoreOdsResponse: Result with clinical interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("wexner_score_ods", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Wexner Score for Obstructed Defecation Syndrome",
                    "details": {"parameters": parameters}
                }
            )
        
        return WexnerScoreOdsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Wexner Score calculation",
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
                "message": "Internal error in Wexner Score calculation",
                "details": {"error": str(e)}
            }
        )