"""
Modified Rankin Score 9Q (mRS-9Q) Router

Endpoint for calculating Modified Rankin Score 9Q for neurologic function assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.modified_rankin_score_9q import (
    ModifiedRankinScore9QRequest,
    ModifiedRankinScore9QResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/modified_rankin_score_9q",
    response_model=ModifiedRankinScore9QResponse,
    summary="Calculate Modified Rankin Score 9Q (mRS-9Q)",
    description="Calculates the Modified Rankin Score 9Q (mRS-9Q) using a structured 9-question yes/no interview "
                "that provides simple and reliable determination of the modified Rankin Scale score. This validated "
                "tool reduces subjectivity compared to traditional mRS assessment and can be administered by medical "
                "or non-medical personnel with excellent inter-rater reliability. The mRS-9Q can be completed in-person, "
                "by telephone, or via electronic survey in 5-10 minutes. It uses an algorithm-based approach to "
                "systematically determine functional disability levels from 0 (no symptoms) to 5 (severe disability) "
                "based on patient responses about work capacity, social function, daily living activities, and care needs.",
    response_description="The calculated mRS-9Q score with functional status assessment and care planning recommendations",
    operation_id="modified_rankin_score_9q"
)
async def calculate_modified_rankin_score_9q(request: ModifiedRankinScore9QRequest):
    """
    Calculates Modified Rankin Score 9Q (mRS-9Q) for neurologic function assessment
    
    Provides standardized, algorithm-based assessment of functional disability using 
    a structured 9-question interview. The tool offers improved reliability over 
    traditional mRS assessment methods and can be administered across various 
    settings by trained personnel.
    
    Args:
        request: Parameters needed for mRS-9Q calculation
        
    Returns:
        ModifiedRankinScore9QResponse: mRS-9Q score with clinical interpretation and care recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("modified_rankin_score_9q", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Modified Rankin Score 9Q",
                    "details": {"parameters": parameters}
                }
            )
        
        return ModifiedRankinScore9QResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Modified Rankin Score 9Q",
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