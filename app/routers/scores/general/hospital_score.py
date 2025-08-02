"""
HOSPITAL Score for Readmissions Router

Endpoint for calculating HOSPITAL Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.general.hospital_score import (
    HospitalScoreRequest,
    HospitalScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hospital_score",
    response_model=HospitalScoreResponse,
    summary="Calculate HOSPITAL Score for Readmissions",
    description="Predicts potentially avoidable 30-day hospital readmissions in medical patients "
                "using seven readily available clinical predictors. The HOSPITAL acronym represents: "
                "Hemoglobin <12 g/dL, Oncology service discharge, Sodium <135 mEq/L, Procedure during "
                "stay, Index admission type (urgent/emergent), Time (previous admissions), and "
                "Admission Length of stay ≥5 days. Scores range from 0-13, with higher scores "
                "indicating greater readmission risk: low (0-4, 5.8%), intermediate (5-6, 12.0%), "
                "and high (≥7, 22.8%). Helps identify patients who may benefit from intensive "
                "transitional care interventions.",
    response_description="The calculated HOSPITAL score with risk stratification and intervention recommendations",
    operation_id="hospital_score"
)
async def calculate_hospital_score(request: HospitalScoreRequest):
    """
    Calculates HOSPITAL Score for Readmissions
    
    Predicts risk of potentially avoidable 30-day readmissions to help 
    target transitional care resources effectively.
    
    Args:
        request: Seven clinical parameters collected at discharge
        
    Returns:
        HospitalScoreResponse: Score (0-13) with risk category and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hospital_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HOSPITAL score",
                    "details": {"parameters": parameters}
                }
            )
        
        return HospitalScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HOSPITAL score calculation",
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