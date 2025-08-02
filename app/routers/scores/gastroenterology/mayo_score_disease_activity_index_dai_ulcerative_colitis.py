"""
Mayo Score/Disease Activity Index (DAI) for Ulcerative Colitis Router

Endpoint for calculating Mayo DAI score for ulcerative colitis severity assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.mayo_score_disease_activity_index_dai_ulcerative_colitis import (
    MayoScoreDiseaseActivityIndexDaiUlcerativeColitisRequest,
    MayoScoreDiseaseActivityIndexDaiUlcerativeColitisResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mayo_score_disease_activity_index_dai_ulcerative_colitis",
    response_model=MayoScoreDiseaseActivityIndexDaiUlcerativeColitisResponse,
    summary="Calculate Mayo Score/Disease Activity Index (DAI) for Ulcerative Colitis",
    description="Calculates the Mayo Score/Disease Activity Index (DAI) for ulcerative colitis severity "
                "assessment using four clinical and endoscopic parameters. Originally developed in 1987 "
                "by Schroeder et al., this is the most widely adopted disease activity index for ulcerative "
                "colitis in clinical trials (49.5% adoption rate). The scale evaluates stool frequency "
                "increase compared to baseline, rectal bleeding severity, endoscopic mucosal appearance, "
                "and physician's global assessment. Each component is scored 0-3 points for a total range "
                "of 0-12 points. Remission is defined as total score ≤2 with no individual component >1 "
                "point. The tool provides standardized assessment for treatment monitoring, clinical trial "
                "endpoints, and therapeutic decision-making. Scores correlate closely with quality of life "
                "measures and guide treatment escalation or de-escalation. A clinically meaningful change "
                "is defined as ≥3 point reduction in total score, while mucosal healing is defined as "
                "endoscopic subscore 0-1. Regular reassessment is recommended to monitor treatment response "
                "and optimize patient outcomes in ulcerative colitis management.",
    response_description="The calculated Mayo DAI score with disease activity classification and detailed management recommendations",
    operation_id="mayo_score_disease_activity_index_dai_ulcerative_colitis"
)
async def calculate_mayo_score_disease_activity_index_dai_ulcerative_colitis(request: MayoScoreDiseaseActivityIndexDaiUlcerativeColitisRequest):
    """
    Calculates Mayo Score/Disease Activity Index (DAI) for Ulcerative Colitis
    
    The Mayo Score/Disease Activity Index (DAI) is the gold standard tool for assessing 
    ulcerative colitis disease activity and treatment response in both clinical practice 
    and research settings.
    
    Args:
        request: Mayo DAI parameters including stool frequency, rectal bleeding, mucosal appearance, and physician assessment
        
    Returns:
        MayoScoreDiseaseActivityIndexDaiUlcerativeColitisResponse: Calculated Mayo DAI score with 
        disease activity classification and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mayo_score_disease_activity_index_dai_ulcerative_colitis", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Mayo Score/Disease Activity Index (DAI) for Ulcerative Colitis",
                    "details": {"parameters": parameters}
                }
            )
        
        return MayoScoreDiseaseActivityIndexDaiUlcerativeColitisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Mayo Score/Disease Activity Index (DAI) for Ulcerative Colitis",
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