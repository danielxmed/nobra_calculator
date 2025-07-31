"""
Hack's Impairment Index (HII) Router

Endpoint for calculating Hack's Impairment Index for alcohol-induced impairment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.hacks_impairment_index import (
    HacksImpairmentIndexRequest,
    HacksImpairmentIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hacks_impairment_index",
    response_model=HacksImpairmentIndexResponse,
    summary="Calculate Hack's Impairment Index (HII)",
    description="Provides a quantitative and standardized assessment of the degree of alcohol-induced impairment in emergency department patients. Creates an objective, serializable evaluation of clinical intoxication.",
    response_description="The calculated hacks impairment index with interpretation",
    operation_id="calculate_hacks_impairment_index"
)
async def calculate_hacks_impairment_index(request: HacksImpairmentIndexRequest):
    """
    Calculates Hack's Impairment Index (HII)
    
    Provides a quantitative assessment of alcohol-induced impairment in emergency 
    department patients. Evaluates five domains (speech/mentation, gross motor, 
    eye movement, coordination, fine motor) to create an objective measure superior 
    to blood alcohol levels for clinical impairment assessment.
    
    Args:
        request: Scores for each of the five domains (0-4) and number of tasks completed
        
    Returns:
        HacksImpairmentIndexResponse: HII score (0-15) with interpretation and estimated time to resolution
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hacks_impairment_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Hack's Impairment Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return HacksImpairmentIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Hack's Impairment Index",
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