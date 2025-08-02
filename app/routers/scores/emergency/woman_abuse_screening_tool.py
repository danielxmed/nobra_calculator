"""
Woman Abuse Screening Tool (WAST) Router

Endpoint for screening intimate partner violence using the validated WAST instrument.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.woman_abuse_screening_tool import (
    WomanAbuseScreeningToolRequest,
    WomanAbuseScreeningToolResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/woman_abuse_screening_tool",
    response_model=WomanAbuseScreeningToolResponse,
    summary="Calculate Woman Abuse Screening Tool (WAST)",
    description="Calculates the validated WAST score for screening intimate partner violence (domestic "
                "abuse) in healthcare settings. This evidence-based 8-question screening instrument "
                "assesses relationship dynamics, emotional impact of arguments, and history of physical, "
                "emotional, and sexual abuse to identify women at risk of domestic violence. The tool "
                "provides risk stratification (high, moderate, low) with specific clinical recommendations "
                "for safety assessment, intervention planning, resource provision, and follow-up care. "
                "IMPORTANT: Lower scores indicate HIGHER risk of domestic violence. The screening should "
                "be conducted in a private, confidential setting without the partner present, following "
                "trauma-informed care principles. Healthcare providers should have domestic violence "
                "resources readily available and follow institutional protocols for positive screens "
                "including safety planning and appropriate referrals to domestic violence services.",
    response_description="The calculated WAST score with risk assessment, safety recommendations, and comprehensive intervention guidance",
    operation_id="woman_abuse_screening_tool"
)
async def calculate_woman_abuse_screening_tool(request: WomanAbuseScreeningToolRequest):
    """
    Calculates Woman Abuse Screening Tool (WAST) for Intimate Partner Violence Screening
    
    The WAST is a validated 8-question screening instrument designed to detect intimate 
    partner violence (domestic abuse) in healthcare settings. Developed by Brown et al. 
    in 1996, this evidence-based tool provides systematic assessment of relationship 
    dynamics and abuse history to identify women at risk.
    
    Clinical Applications:
    - Systematic screening for intimate partner violence in healthcare settings
    - Risk stratification and safety assessment for domestic violence
    - Guide clinical decision-making for intervention and referral
    - Documentation of domestic violence screening in medical records
    - Support evidence-based approach to domestic violence identification
    
    Screening Domains (8 Questions):
    
    Relationship Dynamics:
    - Overall relationship tension and conflict levels
    - Difficulty resolving arguments and communication patterns
    - Emotional impact of relationship conflicts on self-esteem
    
    Violence and Fear Assessment:
    - Frequency of arguments escalating to physical violence
    - Pattern of feeling frightened by partner's words or actions
    
    Abuse History:
    - History of physical abuse by current or past intimate partner
    - History of emotional/psychological abuse patterns
    - History of sexual abuse or coercion
    
    Scoring and Risk Interpretation:
    
    Score 8-12 points (High Risk):
    - High probability of intimate partner violence
    - Immediate safety assessment and intervention planning required
    - Provide emergency resources and safety planning
    - Consider immediate referral to domestic violence services
    - Document findings and follow institutional protocols
    
    Score 13-17 points (Moderate Risk):
    - Moderate probability of intimate partner violence
    - Further assessment recommended to clarify risk level
    - Provide domestic violence resources and information
    - Consider referral to domestic violence counselor
    - Schedule follow-up screening and monitoring
    
    Score 18-24 points (Low Risk):
    - Low probability of intimate partner violence
    - Continue routine care with periodic re-screening
    - Provide general relationship health information
    - Remain alert for other indicators of domestic violence
    
    Critical Clinical Considerations:
    
    Administration Requirements:
    - Conduct screening in private, confidential setting
    - Ensure partner is not present during assessment
    - Use trauma-informed care principles throughout
    - Maintain patient safety and confidentiality
    
    Response to Positive Screens:
    - Validate patient experiences without judgment
    - Emphasize that abuse is not the patient's fault
    - Respect patient autonomy in decision-making
    - Provide immediate safety assessment if high risk
    - Have domestic violence resources readily available
    
    Legal and Ethical Considerations:
    - Follow mandatory reporting requirements per local laws
    - Respect patient confidentiality within legal limits
    - Document findings appropriately per institutional policy
    - Coordinate with domestic violence advocates when possible
    
    Important Limitations:
    - Designed specifically for intimate partner violence screening
    - May not detect all forms of domestic violence
    - Requires cultural sensitivity and appropriate language
    - Should complement, not replace, clinical judgment
    - Effectiveness depends on proper training and implementation
    
    Args:
        request: Assessment responses including relationship dynamics and abuse history
        
    Returns:
        WomanAbuseScreeningToolResponse: WAST score with risk assessment and intervention recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("woman_abuse_screening_tool", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Woman Abuse Screening Tool (WAST)",
                    "details": {"parameters": parameters}
                }
            )
        
        return WomanAbuseScreeningToolResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for WAST calculation",
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
                "message": "Internal error in WAST calculation",
                "details": {"error": str(e)}
            }
        )