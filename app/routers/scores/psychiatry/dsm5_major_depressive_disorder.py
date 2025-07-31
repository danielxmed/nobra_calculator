"""
DSM-5 Criteria for Major Depressive Disorder Router

Endpoint for calculating DSM-5 Major Depressive Disorder diagnostic criteria.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.dsm5_major_depressive_disorder import (
    Dsm5MajorDepressiveDisorderRequest,
    Dsm5MajorDepressiveDisorderResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/dsm5_major_depressive_disorder",
    response_model=Dsm5MajorDepressiveDisorderResponse,
    summary="Calculate DSM-5 Criteria for Major Depressive Disorder",
    description="Diagnostic criteria for major depressive disorder (MDD) based on DSM-5. Evaluates presence of core symptoms, duration, functional impairment, and exclusion criteria for major depressive episodes.",
    response_description="The calculated dsm5 major depressive disorder with interpretation",
    operation_id="calculate_dsm5_major_depressive_disorder"
)
async def calculate_dsm5_major_depressive_disorder(request: Dsm5MajorDepressiveDisorderRequest):
    """
    Calculates DSM-5 Criteria for Major Depressive Disorder
    
    Diagnostic criteria checker for major depressive disorder (MDD) based on DSM-5.
    Evaluates presence of core symptoms, duration, functional impairment, and exclusion
    criteria for major depressive episodes.
    
    Args:
        request: DSM-5 MDD diagnostic parameters
        
    Returns:
        Dsm5MajorDepressiveDisorderResponse: Diagnostic result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("dsm5_major_depressive_disorder", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating DSM-5 Major Depressive Disorder",
                    "details": {"parameters": parameters}
                }
            )
        
        return Dsm5MajorDepressiveDisorderResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for DSM-5 Major Depressive Disorder",
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