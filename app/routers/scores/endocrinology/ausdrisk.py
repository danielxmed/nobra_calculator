"""
Australian Type 2 Diabetes Risk (AUSDRISK) Assessment Tool Router

Endpoint for calculating AUSDRISK score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.ausdrisk import (
    AusdriskRequest,
    AusdriskResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/ausdrisk", response_model=AusdriskResponse)
async def calculate_ausdrisk(request: AusdriskRequest):
    """
    Calculates Australian Type 2 Diabetes Risk (AUSDRISK) Assessment Tool
    
    Estimates 5-year risk of developing type 2 diabetes in Australian patients
    based on demographic, lifestyle and anthropometric measures.
    
    Args:
        request: Parameters needed for calculation including age, sex, ethnicity,
                 family history, glucose history, medications, smoking, physical
                 activity, and waist circumference category
        
    Returns:
        AusdriskResponse: Result with 5-year diabetes risk and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ausdrisk", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating AUSDRISK score",
                    "details": {"parameters": parameters}
                }
            )
        
        return AusdriskResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for AUSDRISK",
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