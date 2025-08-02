"""
Metroticket Calculator for HCC Router

Endpoint for calculating Metroticket HCC survival prediction.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.metroticket_hcc import (
    MetroticketHccRequest,
    MetroticketHccResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/metroticket_hcc",
    response_model=MetroticketHccResponse,
    summary="Calculate Metroticket HCC Survival Prediction",
    description="Calculates the Metroticket score for predicting 3 and 5-year survival after liver transplantation "
                "for patients with hepatocellular carcinoma (HCC), especially those beyond Milan criteria. "
                "The model uses the 'up-to-seven' criteria where the sum of largest tumor size (cm) and number "
                "of tumors should not exceed seven in absence of vascular invasion. Provides individualized "
                "survival predictions based on tumor characteristics including size, number, and vascular invasion status.",
    response_description="The calculated Metroticket score with survival predictions and clinical interpretation",
    operation_id="metroticket_hcc"
)
async def calculate_metroticket_hcc(request: MetroticketHccRequest):
    """
    Calculates Metroticket HCC Survival Prediction
    
    Predicts post-transplant survival for HCC patients using tumor characteristics.
    The up-to-seven criteria achieved 71.2% 5-year survival, comparable to Milan criteria.
    
    Args:
        request: Parameters including tumor size, number, and vascular invasion status
        
    Returns:
        MetroticketHccResponse: Survival predictions with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("metroticket_hcc", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Metroticket HCC score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MetroticketHccResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Metroticket HCC calculation",
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