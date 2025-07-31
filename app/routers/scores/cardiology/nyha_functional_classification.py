"""
New York Heart Association (NYHA) Functional Classification for Heart Failure Router

Endpoint for calculating NYHA Functional Classification.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.nyha_functional_classification import (
    NyhaFunctionalClassificationRequest,
    NyhaFunctionalClassificationResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/nyha_functional_classification",
    response_model=NyhaFunctionalClassificationResponse,
    summary="Calculate New York Heart Association (NYHA) Fun...",
    description="Stratifies severity of heart failure by symptoms. Provides a simple way of classifying the extent of heart failure based on physical activity limitations and symptoms.",
    response_description="The calculated nyha functional classification with interpretation",
    operation_id="nyha_functional_classification"
)
async def calculate_nyha_functional_classification(request: NyhaFunctionalClassificationRequest):
    """
    Calculates New York Heart Association (NYHA) Functional Classification for Heart Failure
    
    The NYHA classification stratifies severity of heart failure by symptoms based on 
    physical activity limitations. It provides a simple way of classifying the extent 
    of heart failure and remains an important prognostic marker in clinical practice.
    
    Args:
        request: Physical ability selection (Class I-IV)
        
    Returns:
        NyhaFunctionalClassificationResponse: NYHA class with interpretation and MET capacity
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("nyha_functional_classification", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating NYHA Functional Classification",
                    "details": {"parameters": parameters}
                }
            )
        
        return NyhaFunctionalClassificationResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for NYHA Functional Classification",
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