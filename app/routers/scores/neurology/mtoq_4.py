"""
Migraine Treatment Optimization Questionnaire-4 (mTOQ-4) Router

Endpoint for calculating mTOQ-4 score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.mtoq_4 import (
    Mtoq4Request,
    Mtoq4Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mtoq_4",
    response_model=Mtoq4Response,
    summary="Calculate Migraine Treatment Optimization Questionnaire-4 (mTOQ-4)",
    description="Determines effectiveness of current migraine treatment plan to guide treatment "
                "optimization decisions. Assesses 4 key aspects: 2-hour pain freedom, 24-hour "
                "sustained relief, ability to plan activities, and feeling in control. Higher "
                "scores indicate better treatment optimization and lower risk of progression to "
                "chronic migraine. Scores <8 suggest need for treatment modification.",
    response_description="The calculated mTOQ-4 score with treatment efficacy category and recommendations",
    operation_id="mtoq_4"
)
async def calculate_mtoq_4(request: Mtoq4Request):
    """
    Calculates Migraine Treatment Optimization Questionnaire-4 (mTOQ-4)
    
    Evaluates acute migraine treatment effectiveness to identify patients
    who would benefit from treatment modifications and prevent chronification.
    
    Args:
        request: Responses to 4 questions about treatment effectiveness
        
    Returns:
        Mtoq4Response: Total score, efficacy category, and treatment guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mtoq_4", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating mTOQ-4 score",
                    "details": {"parameters": parameters}
                }
            )
        
        return Mtoq4Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for mTOQ-4 score",
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