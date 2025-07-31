"""
Disease Steps for Multiple Sclerosis Router

Endpoint for calculating Disease Steps for Multiple Sclerosis progression assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.disease_steps_ms import (
    DiseaseStepsMsRequest,
    DiseaseStepsMsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/disease_steps_ms", response_model=DiseaseStepsMsResponse)
async def calculate_disease_steps_ms(request: DiseaseStepsMsRequest):
    """
    Calculates Disease Steps for Multiple Sclerosis
    
    Assesses MS disease progression based on patient's ambulatory ability using 
    a simple and reproducible scale. The Disease Steps scale provides better 
    inter-rater reliability compared to EDSS and offers more uniform patient 
    distribution across disability levels. It focuses specifically on mobility 
    and walking function to track disease progression and guide therapeutic decisions.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        DiseaseStepsMsResponse: Disease progression assessment with functional interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("disease_steps_ms", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Disease Steps for Multiple Sclerosis",
                    "details": {"parameters": parameters}
                }
            )
        
        return DiseaseStepsMsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Disease Steps for Multiple Sclerosis",
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