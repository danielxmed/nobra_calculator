"""
Mutation-Enhanced International Prognostic Score System (MIPSS70/MIPSS70+) Router

Endpoint for calculating MIPSS70/MIPSS70+ for primary myelofibrosis risk stratification.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.mipss70 import (
    Mipss70Request,
    Mipss70Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mipss70",
    response_model=Mipss70Response,
    summary="Calculate MIPSS70/MIPSS70+ Score",
    description="Calculates the Mutation-Enhanced International Prognostic Score System (MIPSS70/MIPSS70+) for risk stratification in patients with primary myelofibrosis. This enhanced prognostic system incorporates clinical, laboratory, and molecular genetic parameters to provide superior prognostic accuracy for transplantation-age patients (≤70 years). The score ranges from 0-10 points and classifies patients into four risk categories (Low, Intermediate-1, Intermediate-2, High) to guide treatment decisions including timing of allogeneic stem cell transplantation, JAK inhibitor therapy, and supportive care measures.",
    response_description="The calculated MIPSS70/MIPSS70+ score with risk stratification, prognosis, and comprehensive treatment recommendations",
    operation_id="mipss70"
)
async def calculate_mipss70(request: Mipss70Request):
    """
    Calculates Mutation-Enhanced International Prognostic Score System (MIPSS70/MIPSS70+)
    
    Risk stratification system for primary myelofibrosis incorporating molecular genetics
    to improve prognostic accuracy and guide transplantation decisions.
    
    Args:
        request: Clinical, laboratory, and molecular parameters for calculation
        
    Returns:
        Mipss70Response: Score with detailed risk stratification and treatment guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mipss70", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MIPSS70/MIPSS70+ Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return Mipss70Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MIPSS70/MIPSS70+ Score",
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