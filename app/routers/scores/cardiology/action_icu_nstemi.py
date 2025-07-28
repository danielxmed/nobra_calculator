"""
ACTION ICU Score for Intensive Care in NSTEMI Router

Endpoint for calculating ACTION ICU score for NSTEMI complications.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.action_icu_nstemi import (
    ActionIcuNstemiRequest,
    ActionIcuNstemiResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/action_icu_nstemi", response_model=ActionIcuNstemiResponse)
async def calculate_action_icu_nstemi(request: ActionIcuNstemiRequest):
    """
    Calculates ACTION ICU Score for Intensive Care in NSTEMI
    
    This calculator implements the ACTION ICU score, a simple risk prediction tool 
    to identify patients with non-ST-segment elevation myocardial infarction (NSTEMI) 
    who are at high risk for developing complications that would require intensive 
    care unit (ICU) management.
    
    The score uses 9 readily available clinical variables to stratify patients into 
    low, intermediate, and high-risk categories for ICU-level complications, including:
    - Cardiogenic shock
    - Mechanical ventilation
    - Mechanical circulatory support
    - Cardiac arrest
    - Other serious in-hospital complications
    
    Clinical Applications:
    - ICU admission decision-making for NSTEMI patients
    - Healthcare resource allocation and planning
    - Risk stratification for clinical monitoring intensity
    - Early identification of high-risk patients
    
    Risk Categories:
    - Low risk (0-3 points): Standard cardiac monitoring on telemetry unit
    - Intermediate risk (4-7 points): Enhanced monitoring, consider step-down unit
    - High risk (8-20 points): Consider direct ICU admission
    
    Important Notes:
    - This calculator is not externally validated and should be used with caution
    - Intended for use in emergency patients with NSTEMI
    - Should be used in conjunction with clinical judgment
    - Results should guide, not replace, clinical decision-making
    
    Args:
        request: Parameters including age, creatinine, heart rate, blood pressure,
                troponin ratio, heart failure signs, ST depression, revascularization 
                history, and chronic lung disease
        
    Returns:
        ActionIcuNstemiResponse: Risk score with clinical interpretation and 
                                recommended care level
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("action_icu_nstemi", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ACTION ICU Score for Intensive Care in NSTEMI",
                    "details": {"parameters": parameters}
                }
            )
        
        return ActionIcuNstemiResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ACTION ICU Score for Intensive Care in NSTEMI",
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