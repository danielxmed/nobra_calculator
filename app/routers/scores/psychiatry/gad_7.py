"""
GAD-7 (General Anxiety Disorder-7) Router

Endpoint for calculating GAD-7 anxiety assessment score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.gad_7 import (
    Gad7Request,
    Gad7Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/gad_7",
    response_model=Gad7Response,
    summary="Calculate GAD-7 (General Anxiety Disorder-7)",
    description="Measures anxiety severity and screens for generalized anxiety disorder",
    response_description="The calculated gad 7 with interpretation",
    operation_id="gad_7"
)
async def calculate_gad_7(request: Gad7Request):
    """
    Calculates GAD-7 (General Anxiety Disorder-7) Score
    
    Assesses anxiety severity using a validated 7-item questionnaire that evaluates 
    anxiety symptoms experienced over the past 2 weeks. Provides screening for 
    generalized anxiety disorder and other anxiety disorders.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        Gad7Response: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("gad_7", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating GAD-7 (General Anxiety Disorder-7)",
                    "details": {"parameters": parameters}
                }
            )
        
        return Gad7Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for GAD-7 (General Anxiety Disorder-7)",
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