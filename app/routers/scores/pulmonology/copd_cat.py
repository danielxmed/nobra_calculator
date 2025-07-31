"""
COPD Assessment Test (CAT) Router

Endpoint for calculating COPD Assessment Test score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.copd_cat import (
    CopdCatRequest,
    CopdCatResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/copd_cat",
    response_model=CopdCatResponse,
    summary="Calculate COPD Assessment Test (CAT)",
    description="Quantifies the impact of COPD symptoms on patients' overall health and quality of life. The CAT is a patient-completed questionnaire that assesses multiple aspects of COPD including respiratory symptoms, activity limitations, confidence, and sleep quality.",
    response_description="The calculated copd cat with interpretation",
    operation_id="calculate_copd_cat"
)
async def calculate_copd_cat(request: CopdCatRequest):
    """
    Calculates COPD Assessment Test (CAT) score
    
    Quantifies the impact of COPD symptoms on patients' overall health and quality 
    of life. The CAT is an 8-item patient-completed questionnaire that assesses 
    respiratory symptoms, activity limitations, confidence, sleep quality, and energy.
    
    Args:
        request: Parameters including scores (0-5) for cough, phlegm, chest tightness,
                breathlessness, activities, confidence, sleep, and energy
        
    Returns:
        CopdCatResponse: Total CAT score (0-40) with impact level and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("copd_cat", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating COPD CAT score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CopdCatResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for COPD CAT score",
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