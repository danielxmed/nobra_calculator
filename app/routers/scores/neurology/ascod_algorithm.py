"""
ASCOD Algorithm for Ischemic Stroke Router

Endpoint for calculating ASCOD Algorithm for Ischemic Stroke phenotype classification.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.ascod_algorithm import (
    AscodAlgorithmRequest,
    AscodAlgorithmResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ascod_algorithm",
    response_model=AscodAlgorithmResponse,
    summary="Calculate ASCOD Algorithm for Ischemic Stroke",
    description="Assigns phenotype in patients with ischemic stroke of uncertain causes by evaluating five main etiologic categories: Atherothrombosis, Small-vessel disease, Cardiac pathology, Other causes, and Dissection. Provides a comprehensive classification system that captures overlap between multiple underlying stroke mechanisms.",
    response_description="The calculated ascod algorithm with interpretation",
    operation_id="calculate_ascod_algorithm"
)
async def calculate_ascod_algorithm(request: AscodAlgorithmRequest):
    """
    Calculates ASCOD Algorithm for Ischemic Stroke
    
    Assigns phenotype in patients with ischemic stroke of uncertain causes by evaluating
    five main etiologic categories: Atherothrombosis, Small-vessel disease, Cardiac pathology,
    Other causes, and Dissection. Provides comprehensive stroke classification that captures
    overlapping mechanisms and guides targeted secondary prevention strategies.
    
    The ASCOD Algorithm is more detailed than traditional classification systems like TOAST,
    allowing for multiple contributing factors and providing nuanced assessment of stroke etiology.
    Each category is graded from 0 (no disease) to 9 (incomplete workup), with grades 1-3
    indicating different levels of causality.
    
    Args:
        request: ASCOD Algorithm parameters with causality grades for each category
        
    Returns:
        AscodAlgorithmResponse: ASCOD phenotype with clinical interpretation and management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ascod_algorithm", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ASCOD Algorithm for Ischemic Stroke",
                    "details": {"parameters": parameters}
                }
            )
        
        return AscodAlgorithmResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ASCOD Algorithm for Ischemic Stroke",
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
                "message": "Internal error in ASCOD Algorithm calculation",
                "details": {"error": str(e)}
            }
        )