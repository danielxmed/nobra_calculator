"""
Ho Index for Ulcerative Colitis Router

Endpoint for calculating Ho Index score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.ho_index import (
    HoIndexRequest,
    HoIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ho_index",
    response_model=HoIndexResponse,
    summary="Calculate Ho Index for Ulcerative Colitis",
    description="Predicts outcome of medical therapy in severe ulcerative colitis by assessing risk "
                "of failure of corticosteroid therapy. The Ho Index uses three clinical parameters "
                "assessed on day 3 of admission: mean stool frequency, presence of colonic dilatation "
                "on abdominal X-ray (≥5.5cm), and hypoalbuminemia (≤3 g/dL). Scores of 0-1 indicate "
                "low risk (11% failure), 2-3 intermediate risk (45% failure), and ≥4 high risk (85% "
                "failure) of medical therapy failure, helping identify patients who may need early "
                "escalation to second-line medical therapy or surgery.",
    response_description="The calculated Ho Index score with risk stratification and management recommendations",
    operation_id="ho_index"
)
async def calculate_ho_index(request: HoIndexRequest):
    """
    Calculates Ho Index for Ulcerative Colitis
    
    Predicts medical therapy failure in acute severe ulcerative colitis 
    to guide early selection for second-line therapy or surgery.
    
    Args:
        request: Parameters needed for Ho Index calculation including stool frequency,
                 colonic dilatation, and albumin level on day 3 of admission
        
    Returns:
        HoIndexResponse: Score (0-9) with risk stratification and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ho_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Ho Index score",
                    "details": {"parameters": parameters}
                }
            )
        
        return HoIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Ho Index calculation",
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