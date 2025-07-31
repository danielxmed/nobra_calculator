"""
NAFLD (Non-Alcoholic Fatty Liver Disease) Activity Score Router

Endpoint for calculating NAFLD Activity Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.nafld_activity_score import (
    NafldActivityScoreRequest,
    NafldActivityScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/nafld_activity_score", response_model=NafldActivityScoreResponse)
async def calculate_nafld_activity_score(request: NafldActivityScoreRequest):
    """
    Calculates NAFLD (Non-Alcoholic Fatty Liver Disease) Activity Score
    
    The NAS evaluates disease activity in NAFLD patients by scoring three histological 
    features on liver biopsy: steatosis (0-3), lobular inflammation (0-3), and 
    hepatocellular ballooning (0-2), yielding a total score of 0-8.
    
    Clinical significance:
    - NAS ≥5 strongly correlates with "definite NASH" diagnosis
    - NAS ≤2 correlates with "not NASH" 
    - NAS 3-4 is indeterminate and requires clinical correlation
    - A ≥2-point improvement in NAS is commonly used as a clinical trial endpoint
    
    Note: The NAS should not be used as a standalone diagnostic tool for NASH.
    Fibrosis is staged separately (0-4) and is not included in the NAS.
    
    Args:
        request: Parameters needed for calculation including steatosis percentage,
                lobular inflammation count, and ballooning severity
        
    Returns:
        NafldActivityScoreResponse: Result with total NAS score, component scores,
                                   and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("nafld_activity_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating NAFLD Activity Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return NafldActivityScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for NAFLD Activity Score",
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