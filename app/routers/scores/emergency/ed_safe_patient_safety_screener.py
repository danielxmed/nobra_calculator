"""
ED-SAFE Patient Safety Screener 3 (PSS-3) Router

Endpoint for calculating PSS-3 suicide risk screening.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.ed_safe_patient_safety_screener import (
    EdSafePatientSafetyScreenerRequest,
    EdSafePatientSafetyScreenerResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ed_safe_patient_safety_screener",
    response_model=EdSafePatientSafetyScreenerResponse,
    summary="Calculate ED-SAFE Patient Safety Screener 3 (PSS-3)",
    description="Screens for suicidality in emergency patients through universal screening with a validated 3-question tool. Designed for rapid assessment of suicide risk in the emergency department setting for patients with any chief complaint.",
    response_description="The calculated ed safe patient safety screener with interpretation",
    operation_id="calculate_ed_safe_patient_safety_screener"
)
async def calculate_ed_safe_patient_safety_screener(request: EdSafePatientSafetyScreenerRequest):
    """
    Calculates ED-SAFE Patient Safety Screener 3 (PSS-3)
    
    The PSS-3 is a brief, validated suicide risk screening tool designed for universal 
    use in emergency departments. It consists of three questions that can rapidly identify 
    patients at risk for suicide, including those presenting with non-psychiatric chief complaints.
    
    Key Clinical Features:
    - Universal screening tool for all ED patients ≥18 years old
    - Administered during triage or primary nursing assessment
    - Takes 1-2 minutes to complete
    - Doubles suicide risk detection rate (from 2.9% to 5.7%)
    - Strong agreement with established tools (Beck Scale: κ = 0.94-0.95)
    - Validated across diverse patient populations and chief complaints
    
    Screening Questions:
    1. Depression (past 2 weeks): "Over the past 2 weeks, have you felt down, depressed, or hopeless?"
    2. Suicidal ideation (past 2 weeks): "Over the past 2 weeks, have you had thoughts of killing yourself?"
    3. Suicide attempt history: "Have you ever in your lifetime made a suicide attempt?"
    
    Positive Screening Criteria:
    - YES to Question 2 (active suicidal ideation), OR
    - YES to Question 3 (lifetime suicide attempt)
    
    Clinical Response to Positive Screen:
    - Immediate further assessment by treating clinician
    - Patient should not be left alone (continuous monitoring)
    - Consider mental health consultation
    - Implement safety precautions and comprehensive risk assessment
    - Develop safety plan if appropriate
    - Consider ED-SAFE Secondary Screener (ESS-6) for risk stratification
    
    Implementation Context:
    - Part of comprehensive ED-SAFE suicide prevention protocol
    - Designed for fast-paced emergency department environment
    - Can identify at-risk patients who might otherwise go undetected
    - Cost-effective screening approach that fits existing ED workflow
    - Among non-psychiatric ED presentations, 3-12% have suicidal ideation
    
    Args:
        request: PSS-3 screening questions (depression, suicidal thoughts, suicide attempt history)
        
    Returns:
        EdSafePatientSafetyScreenerResponse: Screening result with clinical action recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ed_safe_patient_safety_screener", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ED-SAFE Patient Safety Screener",
                    "details": {"parameters": parameters}
                }
            )
        
        return EdSafePatientSafetyScreenerResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ED-SAFE Patient Safety Screener",
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