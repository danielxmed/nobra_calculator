"""
Adult Self-Report Scale (ASRS v1.1) for ADHD Router

Endpoint for calculating ASRS v1.1 ADHD screening.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.asrs_v1_1_adhd import (
    AsrsV11AdhdRequest,
    AsrsV11AdhdResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/asrs_v1_1_adhd",
    response_model=AsrsV11AdhdResponse,
    summary="Calculate Adult Self-Report Scale (ASRS v1.1) for ADHD",
    description="Screens and diagnoses adult ADHD based on DSM-IV-TR criteria using an 18-question self-report questionnaire",
    response_description="The calculated asrs v1 1 adhd with interpretation",
    operation_id="asrs_v1_1_adhd"
)
async def calculate_asrs_v1_1_adhd(request: AsrsV11AdhdRequest):
    """
    Calculates Adult Self-Report Scale (ASRS v1.1) for ADHD
    
    An 18-question screening tool developed in collaboration with WHO and 
    Harvard Medical School to identify adult ADHD based on DSM-IV-TR criteria.
    Part A (questions 1-6) serves as the primary screener with weighted scoring.
    
    Args:
        request: ASRS v1.1 parameters (18 questions about ADHD symptoms)
        
    Returns:
        AsrsV11AdhdResponse: Screening result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("asrs_v1_1_adhd", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ASRS v1.1 for ADHD",
                    "details": {"parameters": parameters}
                }
            )
        
        return AsrsV11AdhdResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ASRS v1.1 for ADHD",
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