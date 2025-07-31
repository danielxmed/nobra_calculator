"""
Disease Activity Score-28 for Rheumatoid Arthritis with CRP (DAS28-CRP) Router

Endpoint for calculating DAS28-CRP for rheumatoid arthritis disease activity assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.das28_crp import (
    Das28CrpRequest,
    Das28CrpResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/das28_crp", response_model=Das28CrpResponse)
async def calculate_das28_crp(request: Das28CrpRequest):
    """
    Calculates Disease Activity Score-28 for Rheumatoid Arthritis with CRP
    
    Assesses disease activity in rheumatoid arthritis patients using a composite 
    measure that includes tender joint count, swollen joint count, C-reactive 
    protein level, and patient's global assessment. The score supports 
    treat-to-target strategies by categorizing disease activity into remission, 
    low, moderate, and high activity levels.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        Das28CrpResponse: Disease activity assessment with treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("das28_crp", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating DAS28-CRP score",
                    "details": {"parameters": parameters}
                }
            )
        
        return Das28CrpResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for DAS28-CRP score",
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