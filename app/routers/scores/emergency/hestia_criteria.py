"""
Hestia Criteria for Outpatient Pulmonary Embolism Treatment Router

Endpoint for calculating Hestia Criteria score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.hestia_criteria import (
    HestiaCriteriaRequest,
    HestiaCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hestia_criteria",
    response_model=HestiaCriteriaResponse,
    summary="Calculate Hestia Criteria for Outpatient PE Treatment",
    description="Calculates the Hestia Criteria to identify low-risk pulmonary embolism patients "
                "who may be safe for outpatient management. This validated clinical decision tool "
                "uses 11 exclusion criteria to assess hemodynamic stability, bleeding risk, oxygen "
                "requirements, social factors, and comorbidities. Unlike scoring systems, it functions "
                "as a checklist - all criteria must be absent (0 points) for a patient to be considered "
                "low risk. Patients meeting all criteria have shown excellent outcomes with outpatient "
                "treatment, including 0% mortality and 2% VTE recurrence rates. The tool helps reduce "
                "unnecessary hospitalizations while maintaining patient safety.",
    response_description="The calculated Hestia score with risk stratification and treatment recommendations",
    operation_id="hestia_criteria"
)
async def calculate_hestia_criteria(request: HestiaCriteriaRequest):
    """
    Calculates Hestia Criteria for Outpatient Pulmonary Embolism Treatment
    
    This tool helps identify PE patients who can be safely treated at home,
    reducing healthcare costs while maintaining excellent clinical outcomes.
    
    Args:
        request: Clinical parameters for Hestia Criteria assessment
        
    Returns:
        HestiaCriteriaResponse: Number of criteria met with treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hestia_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Hestia Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return HestiaCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Hestia Criteria",
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
                "message": "Internal error in Hestia Criteria calculation",
                "details": {"error": str(e)}
            }
        )