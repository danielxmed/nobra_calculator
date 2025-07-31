"""
Bacterial Meningitis Score for Children Router

Endpoint for calculating Bacterial Meningitis Score for Children.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.infectious_disease.bacterial_meningitis_score import (
    BacterialMeningitisScoreRequest,
    BacterialMeningitisScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/bacterial_meningitis_score",
    response_model=BacterialMeningitisScoreResponse,
    summary="Calculate Bacterial Meningitis Score for Children",
    description="Predicts likelihood of bacterial (versus aseptic) meningitis in children with CSF pleocytosis. The score helps clinicians distinguish between bacterial and aseptic meningitis to support safe discharge decisions while maintaining appropriate caution for this serious condition.",
    response_description="The calculated bacterial meningitis score with interpretation",
    operation_id="calculate_bacterial_meningitis_score"
)
async def calculate_bacterial_meningitis_score(request: BacterialMeningitisScoreRequest):
    """
    Calculates Bacterial Meningitis Score for Children
    
    The Bacterial Meningitis Score for Children predicts the absence of bacterial 
    meningitis in pediatric patients with meningitis.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        BacterialMeningitisScoreResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("bacterial_meningitis_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Bacterial Meningitis Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return BacterialMeningitisScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Bacterial Meningitis Score",
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