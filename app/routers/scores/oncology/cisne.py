"""
Clinical Index of Stable Febrile Neutropenia (CISNE) Router

Endpoint for calculating CISNE score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.cisne import (
    CisneRequest,
    CisneResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/cisne",
    response_model=CisneResponse,
    summary="Calculate Clinical Index of Stable Febrile Neutropenia",
    description="Identifies febrile neutropenia patients at low risk for serious complications. Used for adult outpatients with solid tumor, fever ≥38°C (100.4°F), and neutropenia (≤500 cells/mm³ or ≤1,000 cells/mm³ with expected decrease to 500).",
    response_description="The calculated cisne with interpretation",
    operation_id="calculate_cisne"
)
async def calculate_cisne(request: CisneRequest):
    """
    Calculates Clinical Index of Stable Febrile Neutropenia (CISNE)
    
    Identifies febrile neutropenia patients at low risk for serious complications.
    Used for stable adult outpatients with solid tumor, fever ≥38°C (100.4°F), 
    and neutropenia (≤500 cells/mm³).
    
    Args:
        request: Parameters including ECOG status, hyperglycemia, comorbidities, 
                mucositis, and monocyte count
        
    Returns:
        CisneResponse: CISNE score (0-8) with risk category and interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cisne", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CISNE score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CisneResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CISNE score",
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