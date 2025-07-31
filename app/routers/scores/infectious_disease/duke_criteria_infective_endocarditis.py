"""
Duke Criteria for Infective Endocarditis Router

Endpoint for calculating Duke Criteria for Infective Endocarditis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.infectious_disease.duke_criteria_infective_endocarditis import (
    DukeCriteriaInfectiveEndocarditisRequest,
    DukeCriteriaInfectiveEndocarditisResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/duke_criteria_infective_endocarditis",
    response_model=DukeCriteriaInfectiveEndocarditisResponse,
    summary="Calculate Duke Criteria for Infective Endocarditis",
    description="Provides standardized diagnostic criteria for infective endocarditis based on clinical, microbiological, and echocardiographic findings. Classifies patients as having definite, possible, or rejected endocarditis.",
    response_description="The calculated duke criteria infective endocarditis with interpretation",
    operation_id="duke_criteria_infective_endocarditis"
)
async def calculate_duke_criteria_infective_endocarditis(request: DukeCriteriaInfectiveEndocarditisRequest):
    """
    Calculates Duke Criteria for Infective Endocarditis
    
    Provides standardized diagnostic criteria for infective endocarditis based on clinical, 
    microbiological, and echocardiographic findings. Classifies patients as having definite, 
    possible, or rejected endocarditis based on major and minor criteria.
    
    Args:
        request: Parameters needed for calculation (2 major + 5 minor criteria)
        
    Returns:
        DukeCriteriaInfectiveEndocarditisResponse: Result with diagnostic classification and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("duke_criteria_infective_endocarditis", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Duke Criteria for Infective Endocarditis",
                    "details": {"parameters": parameters}
                }
            )
        
        return DukeCriteriaInfectiveEndocarditisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Duke Criteria for Infective Endocarditis",
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