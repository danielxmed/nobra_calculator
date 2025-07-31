"""
National Early Warning Score (NEWS) 2 Router

Endpoint for calculating National Early Warning Score 2.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.news_2 import (
    News2Request,
    News2Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/news_2",
    response_model=News2Response,
    summary="Calculate National Early Warning Score (NEWS) 2",
    description="Determines the degree of illness of a patient and prompts critical care intervention. Recommended by NHS over original NEWS with improved oxygen saturation scoring for hypercapnic respiratory failure patients.",
    response_description="The calculated news 2 with interpretation",
    operation_id="calculate_news_2"
)
async def calculate_news_2(request: News2Request):
    """
    Calculates National Early Warning Score (NEWS) 2
    
    Determines the degree of illness of a patient and prompts critical care intervention.
    NEWS 2 improves upon the original NEWS by adjusting oxygen saturation scoring for 
    patients with hypercapnic respiratory failure.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        News2Response: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("news_2", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating National Early Warning Score 2",
                    "details": {"parameters": parameters}
                }
            )
        
        return News2Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for National Early Warning Score 2",
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