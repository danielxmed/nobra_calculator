"""
Danger Assessment Tool for Domestic Abuse Router

Endpoint for calculating danger assessment for intimate partner violence risk.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.danger_assessment_tool import (
    DangerAssessmentToolRequest,
    DangerAssessmentToolResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/danger_assessment_tool",
    response_model=DangerAssessmentToolResponse,
    summary="Calculate Danger Assessment Tool for Domestic Abuse",
    description="Predicts risk of death by intimate partner (IP) in violent intimate relationship. Validated lethality risk assessment instrument for intimate partner femicide developed by Dr. Jacquelyn Campbell at Johns Hopkins University.",
    response_description="The calculated danger assessment tool with interpretation",
    operation_id="calculate_danger_assessment_tool"
)
async def calculate_danger_assessment_tool(request: DangerAssessmentToolRequest):
    """
    Calculates Danger Assessment Tool for Domestic Abuse
    
    The Danger Assessment Tool is a validated lethality risk assessment instrument designed 
    to predict the risk of intimate partner femicide. Developed by Dr. Jacquelyn Campbell 
    at Johns Hopkins University, this evidence-based tool helps identify women at highest 
    risk of being killed by their intimate partners.
    
    **Clinical Background and Significance:**
    
    Intimate partner violence (IPV) is a significant public health problem affecting millions 
    of women worldwide. In the United States, approximately 3-4 million women are abused 
    annually, with 1,500-1,600 women killed by their intimate partners each year. The challenge 
    for healthcare providers, law enforcement, and social services is identifying those women 
    at highest risk of lethal violence.
    
    The Danger Assessment was developed through rigorous scientific research, including an 
    11-city case-control study that analyzed 310 intimate partner femicide cases compared 
    with 324 abused women controls. This landmark study identified key risk factors that 
    distinguish women who are murdered from those who experience non-lethal abuse.
    
    **Evidence Base and Validation:**
    
    **Original Development Study:**
    The foundational research involved comprehensive analysis of femicide cases across 11 cities, 
    examining factors present in lethal versus non-lethal intimate partner violence. The study 
    used multivariate analysis to identify independent risk factors and calculate adjusted 
    odds ratios, which form the basis for the weighted scoring system.
    
    **Validation Studies:**
    Multiple subsequent studies have validated the predictive ability of the Danger Assessment:
    - Demonstrated significant association between higher scores and femicide risk
    - Validated across diverse populations and geographic regions  
    - Shown to be effective in various settings (healthcare, law enforcement, advocacy)
    - Confirmed reliability and validity across different ethnic and socioeconomic groups
    
    **Clinical Utility Research:**
    Studies have demonstrated that use of the Danger Assessment:
    - Increases accurate identification of high-risk cases
    - Improves safety planning and resource allocation
    - Enhances communication between victims and professionals
    - Reduces victim minimization and denial of danger
    - Guides appropriate intervention intensity
    
    **Risk Factor Analysis and Interpretation:**
    
    **Highest Risk Factors (Adjusted Odds Ratios >4.0):**
    
    **Gun Ownership (OR 5.1):**
    Ownership of firearms by the perpetrator represents the single highest risk factor for 
    intimate partner femicide. Guns are used in approximately 50% of intimate partner homicides, 
    and their presence significantly increases lethality risk even when not directly threatened.
    
    **Strangulation History (OR 4.6):**
    Prior strangulation attempts are among the strongest predictors of future femicide. 
    Strangulation represents a clear escalation to potentially lethal violence and indicates 
    the perpetrator's willingness and ability to kill.
    
    **Weapon Threats (OR 4.3):**
    Threats or attempts to kill with a weapon demonstrate both lethal intent and access to 
    means. This factor indicates escalation beyond verbal threats to preparation for violence.
    
    **Death Threats (OR 4.0):**
    Direct threats to kill the victim represent explicit expression of lethal intent. These 
    threats often precede actual femicide attempts and should be taken seriously regardless 
    of perceived credibility.
    
    **Threats Against Children (OR 3.8):**
    Threats to kill children indicate potential for family annihilation and extreme violence. 
    This factor suggests the perpetrator views children as extensions of control over the victim.
    
    **Moderate to High Risk Factors (OR 2.0-3.9):**
    
    **Escalation Patterns:**
    - Increased violence frequency or severity (OR 2.3)
    - Violence during pregnancy (OR 3.2)
    - Perception that perpetrator might try to kill (OR 3.5)
    
    **Control and Jealousy:**
    - Violent and constant jealousy (OR 3.0)
    - Control over daily activities (OR 2.4)
    - Violence toward children (OR 2.8)
    
    **Additional Violence:**
    - Stalking behaviors, surveillance, property destruction (OR 2.0)
    - Forced sexual activity (OR 1.9)
    - Violence toward other family members (OR 1.9)
    
    **Psychological Factors:**
    - Suicide threats or attempts (OR 2.0)
    - Substance abuse during violence (OR 2.1)
    
    **Lower Risk Factors (OR <2.0):**
    - Presence of stepchildren (OR 1.6)
    - Recent job loss (OR 1.5)
    - General substance abuse (OR 1.7)
    
    **Risk Level Classifications and Clinical Response:**
    
    **Variable Danger (Weighted Score 0-7):**
    
    **Risk Characteristics:**
    - Represents majority of intimate partner violence cases
    - Lower immediate lethality risk but violence still significant
    - Risk factors may be present but limited in number or severity
    - Situation may escalate over time without intervention
    
    **Clinical Response:**
    - Comprehensive safety planning with victim
    - Resource information and referral coordination
    - Regular reassessment for changes in risk factors
    - Documentation of risk factors and safety plan
    - Support for victim decision-making and autonomy
    
    **Safety Planning Elements:**
    - Identification of safe places and trusted contacts
    - Emergency contact information and safety signals
    - Documentation of abuse for potential legal proceedings
    - Financial safety and independence planning
    - Technology safety and communication security
    
    **Increased Danger (Weighted Score 8-13):**
    
    **Risk Characteristics:**
    - Elevated risk requiring intensive intervention
    - Multiple risk factors or presence of moderate-risk factors
    - Clear escalation patterns or specific threats
    - Higher probability of severe injury or death without intervention
    
    **Clinical Response:**
    - Comprehensive safety assessment and planning
    - Coordinated community response activation
    - Enhanced monitoring and frequent contact
    - Legal advocacy and protection order assistance
    - Specialized domestic violence services engagement
    
    **Enhanced Safety Measures:**
    - Emergency relocation planning and shelter coordination
    - Law enforcement consultation and safety planning
    - Workplace safety assessment and notification
    - Child safety planning and potential custody considerations
    - Enhanced security measures and routine variations
    
    **Professional Coordination:**
    - Multidisciplinary team involvement
    - Regular case review and risk reassessment
    - Coordinated service delivery and communication
    - Documentation for potential criminal proceedings
    - Victim advocacy and support services
    
    **Extreme Danger (Weighted Score 14-20):**
    
    **Risk Characteristics:**
    - Immediate and severe risk of intimate partner homicide
    - Multiple high-risk factors present
    - Clear escalation to potentially lethal violence
    - Perpetrator demonstrates means, opportunity, and intent to kill
    
    **Emergency Response:**
    - Immediate safety assessment and crisis intervention
    - Emergency relocation or shelter placement
    - Law enforcement notification and protection
    - Emergency protection order procurement
    - Crisis counseling and support services
    
    **High-Risk Protocol Activation:**
    - Specialized high-risk domestic violence team involvement
    - Frequent safety contact and monitoring
    - Enhanced law enforcement response protocols
    - Priority access to shelter and emergency services
    - Coordinated criminal justice response
    
    **Comprehensive Safety Planning:**
    - Immediate escape route planning and practice
    - Emergency bag preparation and secure storage
    - Safe communication methods and code words
    - Child safety planning and emergency care arrangements
    - Legal protection and evidence preservation
    - Technology safety and location security
    
    **Clinical Considerations for Healthcare Providers:**
    
    **Assessment Environment:**
    - Conduct assessment in private, safe environment
    - Ensure confidentiality and safety of documentation
    - Be aware of perpetrator presence and potential surveillance
    - Use trauma-informed and culturally sensitive approaches
    - Respect victim autonomy and decision-making
    
    **Safety Protocols:**
    - Never conduct assessment in presence of suspected perpetrator
    - Secure storage of assessment results and documentation
    - Clear protocols for information sharing and reporting
    - Safety planning that respects victim's risk assessment
    - Understanding of mandatory reporting requirements and implications
    
    **Professional Response:**
    - Validation of victim's experiences and concerns
    - Non-judgmental support and information provision
    - Respect for victim's choices and decision-making timeline
    - Clear information about resources and options
    - Documentation that supports victim safety and legal needs
    
    **Training and Competency Requirements:**
    
    **Assessment Administration:**
    - Proper training in danger assessment methodology
    - Understanding of intimate partner violence dynamics
    - Knowledge of local resources and referral options
    - Trauma-informed care principles and practices
    - Cultural competency and sensitivity training
    
    **Interpretation and Response:**
    - Understanding of risk factor significance and interaction
    - Ability to develop appropriate safety planning responses
    - Knowledge of legal options and advocacy resources
    - Crisis intervention and de-escalation skills
    - Coordinated community response protocols
    
    **Limitations and Considerations:**
    
    **Tool Limitations:**
    - Cannot predict intimate partner homicide with absolute certainty
    - Risk factors can change rapidly requiring frequent reassessment
    - Victim's own risk perception is also important and should be considered
    - Tool was developed primarily for heterosexual relationships
    - May not capture all relevant risk factors for specific populations
    
    **Ethical Considerations:**
    - Victim safety and autonomy must be primary considerations
    - Assessment should empower rather than frighten victims
    - Results should support rather than override victim decision-making
    - Confidentiality and safety must be maintained in documentation
    - Cultural and individual differences must be respected
    
    **Implementation Best Practices:**
    
    **Organizational Requirements:**
    - Comprehensive staff training and competency assessment
    - Clear protocols for assessment, scoring, and response
    - Secure documentation and information sharing systems
    - Coordinated community partnerships and referral networks
    - Regular quality assurance and outcome monitoring
    
    **Continuous Improvement:**
    - Regular assessment of tool effectiveness and outcomes
    - Staff feedback and training updates
    - Community coordination and protocol refinement
    - Victim feedback incorporation and service improvement
    - Research participation and evidence base contribution
    
    **Legal and Ethical Framework:**
    
    **Professional Responsibilities:**
    - Understanding of mandatory reporting requirements and limitations
    - Ethical obligations for victim safety and confidentiality
    - Professional standards for domestic violence response
    - Documentation requirements for legal proceedings
    - Advocacy and support responsibilities
    
    **Legal Considerations:**
    - Evidence preservation and documentation standards
    - Confidentiality protections and limitations
    - Mandatory reporting requirements and processes
    - Legal advocacy and protection order assistance
    - Criminal justice system coordination and support
    
    Args:
        request: Danger Assessment parameters including all 20 validated risk factors 
                assessed as yes/no/not_applicable responses
        
    Returns:
        DangerAssessmentToolResponse: Comprehensive risk assessment including weighted 
        score, risk level classification, safety recommendations, and professional 
        guidance for intimate partner violence intervention
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("danger_assessment_tool", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Danger Assessment Tool",
                    "details": {"parameters": parameters}
                }
            )
        
        return DangerAssessmentToolResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Danger Assessment Tool",
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