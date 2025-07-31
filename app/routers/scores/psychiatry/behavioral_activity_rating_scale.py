"""
Behavioral Activity Rating Scale (BARS) Router

Endpoint for calculating BARS to screen for agitation in emergency and psychiatric settings.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.behavioral_activity_rating_scale import (
    BehavioralActivityRatingScaleRequest,
    BehavioralActivityRatingScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/behavioral_activity_rating_scale",
    response_model=BehavioralActivityRatingScaleResponse,
    summary="Calculate Behavioral Activity Rating Scale (BARS)",
    description="Screens patients for agitation in emergency care and psychiatric settings using a 7-point observational scale",
    response_description="The calculated behavioral activity rating scale with interpretation",
    operation_id="calculate_behavioral_activity_rating_scale"
)
async def calculate_behavioral_activity_rating_scale(request: BehavioralActivityRatingScaleRequest):
    """
    Calculates Behavioral Activity Rating Scale (BARS)
    
    The BARS is a validated 7-point observational scale used to assess behavioral activity 
    and agitation in patients in emergency care and psychiatric settings.
    
    **Scale Overview:**
    - **1**: Difficult or unable to arouse (hypoactive)
    - **2**: Asleep but responds normally to verbal or physical contact
    - **3**: Drowsy, appears sedated
    - **4**: Quiet and awake (normal level of activity) - *Therapeutic target*
    - **5**: Signs of over activity; calms down with instructions (mild agitation)
    - **6**: Extremely or continuously active; does not require restraint (moderate agitation)
    - **7**: Violent behavior requiring restraint (severe agitation)
    
    **Clinical Features:**
    - **Observational tool**: Does not require patient participation or verbal responses
    - **Rapid assessment**: Can be completed in seconds to minutes
    - **High reliability**: Excellent inter-rater and intra-rater reliability demonstrated
    - **Multi-disciplinary**: Can be used by nurses, physicians, and other healthcare staff
    - **Emergency-focused**: Designed for acute care settings where rapid assessment is critical
    
    **Clinical Thresholds:**
    - **Scores ≤4**: Generally indicate stable or controlled behavior
    - **Scores >4**: Typically warrant clinical evaluation and possible intervention
    - **Score 7**: Requires immediate emergency intervention and safety protocols
    
    **Applications:**
    - Emergency department triage and monitoring
    - Psychiatric inpatient unit assessments
    - Medication response evaluation
    - De-escalation effectiveness monitoring
    - Research studies on agitation interventions
    
    **Validation:**
    The BARS was validated in multiple studies showing moderate correlation with other 
    agitation measures (PANSS agitation items, CGI-S) and virtually perfect inter- and 
    intra-rater reliability. It demonstrates superior treatment effect size compared to 
    other agitation rating scales.
    
    Args:
        request: BARS assessment parameters (observed activity level)
        
    Returns:
        BehavioralActivityRatingScaleResponse: BARS score with clinical interpretation and management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("behavioral_activity_rating_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Behavioral Activity Rating Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return BehavioralActivityRatingScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for BARS calculation",
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