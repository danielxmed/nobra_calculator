"""
Jones Criteria for Acute Rheumatic Fever Diagnosis Router

Endpoint for calculating Jones criteria for acute rheumatic fever diagnosis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.jones_criteria_acute_rheumatic_fever import (
    JonesCriteriaAcuteRheumaticFeverRequest,
    JonesCriteriaAcuteRheumaticFeverResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/jones_criteria_acute_rheumatic_fever",
    response_model=JonesCriteriaAcuteRheumaticFeverResponse,
    summary="Calculate Jones Criteria for Acute Rheumatic Fever",
    description="Diagnoses acute rheumatic fever using the revised 2015 Jones criteria with population risk stratification. This evidence-based tool requires documentation of antecedent group A streptococcal infection plus either 2 major criteria OR 1 major + 2 minor criteria. The criteria account for global variations in disease presentation, with different thresholds for low-risk versus moderate-high risk populations. Essential for early diagnosis and prevention of long-term cardiac complications through prompt treatment and secondary prophylaxis.",
    response_description="The diagnostic conclusion with criteria analysis, treatment recommendations, and clinical guidance for acute rheumatic fever management",
    operation_id="jones_criteria_acute_rheumatic_fever"
)
async def calculate_jones_criteria_acute_rheumatic_fever(request: JonesCriteriaAcuteRheumaticFeverRequest):
    """
    Calculates Jones Criteria for Acute Rheumatic Fever Diagnosis
    
    Applies the revised 2015 Jones criteria to systematically diagnose acute rheumatic fever,
    a delayed autoimmune sequela of group A streptococcal pharyngitis. The criteria incorporate
    population risk stratification to improve diagnostic accuracy across different global settings
    while maintaining sensitivity for this potentially serious condition.
    
    Args:
        request: Clinical parameters including population risk, streptococcal evidence, and major/minor criteria
        
    Returns:
        JonesCriteriaAcuteRheumaticFeverResponse: Diagnostic conclusion with treatment guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("jones_criteria_acute_rheumatic_fever", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Jones Criteria for Acute Rheumatic Fever",
                    "details": {"parameters": parameters}
                }
            )
        
        return JonesCriteriaAcuteRheumaticFeverResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Jones Criteria for Acute Rheumatic Fever",
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