"""
Fleischner Society Guidelines for Incidental Pulmonary Nodules Router

Endpoint for calculating Fleischner Guidelines recommendations.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.fleischner_guidelines import (
    FleischnerGuidelinesRequest,
    FleischnerGuidelinesResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/fleischner_guidelines",
    response_model=FleischnerGuidelinesResponse,
    summary="Calculate Fleischner Society Guidelines for Incidental Pu...",
    description="Provides guidelines for management of solid and subsolid pulmonary nodules detected incidentally on CT",
    response_description="The calculated fleischner guidelines with interpretation",
    operation_id="fleischner_guidelines"
)
async def calculate_fleischner_guidelines(request: FleischnerGuidelinesRequest):
    """
    Calculates Fleischner Society Guidelines for Incidental Pulmonary Nodules
    
    Provides follow-up recommendations for incidentally detected pulmonary 
    nodules on CT based on the 2017 Fleischner Society Guidelines.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        FleischnerGuidelinesResponse: Result with follow-up recommendation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("fleischner_guidelines", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Fleischner Guidelines",
                    "details": {"parameters": parameters}
                }
            )
        
        return FleischnerGuidelinesResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Fleischner Guidelines",
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