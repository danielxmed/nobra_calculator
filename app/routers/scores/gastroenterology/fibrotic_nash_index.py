"""
Fibrotic NASH Index (FNI) Router

Endpoint for calculating FNI.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.fibrotic_nash_index import (
    FibroticNashIndexRequest,
    FibroticNashIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/fibrotic_nash_index", response_model=FibroticNashIndexResponse)
async def calculate_fibrotic_nash_index(request: FibroticNashIndexRequest):
    """
    Calculates Fibrotic NASH Index (FNI)
    
    The FNI is a simple non-invasive score that uses routine laboratory values 
    (AST, HbA1c, HDL cholesterol) to screen for fibrotic nonalcoholic 
    steatohepatitis (NASH) in individuals at high risk for NAFLD. It is 
    particularly useful in primary care and endocrinology settings for 
    identifying patients who need hepatology referral.
    
    Args:
        request: Laboratory parameters for FNI calculation
        
    Returns:
        FibroticNashIndexResponse: FNI probability score with risk category and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("fibrotic_nash_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Fibrotic NASH Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return FibroticNashIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Fibrotic NASH Index",
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