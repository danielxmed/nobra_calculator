"""
Fuhrman Nuclear Grade Router

Endpoint for calculating Fuhrman Nuclear Grade for Clear Cell Renal Carcinoma.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.urology.fuhrman_nuclear_grade import (
    FuhrmanNuclearGradeRequest,
    FuhrmanNuclearGradeResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/fuhrman_nuclear_grade",
    response_model=FuhrmanNuclearGradeResponse,
    summary="Calculate Fuhrman Nuclear Grade for Clear Cell Renal Carc...",
    description="Provides prognostic grading system for clear cell renal cell carcinoma (RCC) based on nuclear morphology and cellular appearance. Independent predictor of cancer-specific survival that correlates nuclear grade with prognosis.",
    response_description="The calculated fuhrman nuclear grade with interpretation",
    operation_id="fuhrman_nuclear_grade"
)
async def calculate_fuhrman_nuclear_grade(request: FuhrmanNuclearGradeRequest):
    """
    Calculates Fuhrman Nuclear Grade for Clear Cell Renal Carcinoma
    
    Provides prognostic grading system based on nuclear morphology features including
    size, shape, nucleoli prominence, and presence of bizarre features. Grade ranges
    from 1-4 with higher grades indicating worse prognosis.
    
    Args:
        request: Parameters including nuclear diameter, shape, nucleoli, and bizarre features
        
    Returns:
        FuhrmanNuclearGradeResponse: Grade (1-4) with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("fuhrman_nuclear_grade", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Fuhrman Nuclear Grade",
                    "details": {"parameters": parameters}
                }
            )
        
        return FuhrmanNuclearGradeResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Fuhrman Nuclear Grade",
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