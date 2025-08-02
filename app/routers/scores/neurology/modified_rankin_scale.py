"""
Modified Rankin Scale (mRS) Router

Endpoint for calculating Modified Rankin Scale for neurologic disability assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.modified_rankin_scale import (
    ModifiedRankinScaleRequest,
    ModifiedRankinScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/modified_rankin_scale",
    response_model=ModifiedRankinScaleResponse,
    summary="Calculate Modified Rankin Scale (mRS)",
    description="Calculates the Modified Rankin Scale (mRS) for assessing the degree of disability or dependence in daily activities "
                "following stroke or other neurological conditions. This widely used functional outcome measure provides a common "
                "language for describing neurological disability across seven ordinal levels (0-6). The mRS is the most common "
                "primary endpoint in acute stroke trials and serves as a key quality indicator for stroke care programs. "
                "It helps guide treatment decisions, rehabilitation planning, discharge planning, and prognosis discussions. "
                "The scale ranges from no symptoms (0) to death (6), with scores 0-2 generally indicating functional independence "
                "and scores 3-6 representing increasing levels of dependence and disability.",
    response_description="The calculated mRS score with functional status assessment and care planning recommendations",
    operation_id="modified_rankin_scale"
)
async def calculate_modified_rankin_scale(request: ModifiedRankinScaleRequest):
    """
    Calculates Modified Rankin Scale (mRS) for neurologic disability assessment
    
    Provides standardized assessment of functional disability and dependence following 
    neurological events, particularly stroke. The scale is widely used in clinical 
    practice, research, and quality improvement initiatives to measure outcomes 
    and guide care planning decisions.
    
    Args:
        request: Parameters needed for mRS calculation
        
    Returns:
        ModifiedRankinScaleResponse: mRS score with clinical interpretation and care recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("modified_rankin_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Modified Rankin Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return ModifiedRankinScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Modified Rankin Scale",
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