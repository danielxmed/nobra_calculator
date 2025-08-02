"""
Modified Early Warning Score (MEWS) for Clinical Deterioration Router

Endpoint for calculating MEWS to assess risk of clinical deterioration.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.modified_early_warning_score import (
    ModifiedEarlyWarningScoreRequest,
    ModifiedEarlyWarningScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/modified_early_warning_score",
    response_model=ModifiedEarlyWarningScoreResponse,
    summary="Calculate Modified Early Warning Score (MEWS)",
    description="Calculates the Modified Early Warning Score (MEWS) for clinical deterioration risk assessment. "
                "This physiological scoring system identifies patients at risk of clinical deterioration, ICU admission, "
                "or death using 5 readily available parameters: systolic blood pressure, heart rate, respiratory rate, "
                "temperature, and level of consciousness (AVPU scale). Scores ≥5 indicate high risk requiring immediate "
                "medical review and potential ICU consideration. The score is validated for use in both medical and "
                "surgical patient populations.",
    response_description="The calculated MEWS score with risk stratification and clinical monitoring recommendations",
    operation_id="modified_early_warning_score"
)
async def calculate_modified_early_warning_score(request: ModifiedEarlyWarningScoreRequest):
    """
    Calculates Modified Early Warning Score (MEWS) for Clinical Deterioration
    
    The MEWS is a physiological scoring system that identifies patients at risk of 
    clinical deterioration using vital signs and consciousness level. It helps healthcare 
    providers make objective decisions about monitoring frequency and need for escalation 
    of care.
    
    Args:
        request: Parameters including vital signs and consciousness level
        
    Returns:
        ModifiedEarlyWarningScoreResponse: MEWS score with risk assessment and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("modified_early_warning_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Modified Early Warning Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return ModifiedEarlyWarningScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Modified Early Warning Score",
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