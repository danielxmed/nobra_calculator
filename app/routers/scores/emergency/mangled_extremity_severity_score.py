"""
Mangled Extremity Severity Score (MESS) Router

Endpoint for calculating MESS score for trauma extremity assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.mangled_extremity_severity_score import (
    MangledExtremitySeverityScoreRequest,
    MangledExtremitySeverityScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mangled_extremity_severity_score",
    response_model=MangledExtremitySeverityScoreResponse,
    summary="Calculate Mangled Extremity Severity Score (MESS)",
    description="Calculates the Mangled Extremity Severity Score (MESS), a validated trauma assessment "
                "tool that estimates viability of an extremity after severe trauma to guide critical "
                "decisions between limb salvage and primary amputation. Developed in 1990 by Johansen "
                "et al., MESS evaluates four key factors: limb ischemia (1-3 points, doubled if >6 hours), "
                "patient age (0-2 points), shock status (0-2 points), and injury mechanism (1-4 points). "
                "Total scores range from 1-14 points, with traditionally ≥7 points suggesting amputation, "
                "though modern practice often uses higher thresholds (8-9 points) due to advances in "
                "surgical techniques, vascular repair, and wound management. The tool was originally "
                "developed for lower extremity trauma and is less reliable for pediatric or upper "
                "extremity injuries. MESS serves as a prognostic guide to complement clinical judgment "
                "rather than a definitive decision-making tool. Essential for emergency department "
                "trauma assessment, surgical planning, resource allocation, and patient counseling in "
                "mangled extremity cases.",
    response_description="The calculated MESS score with comprehensive risk assessment, salvage likelihood, and detailed management recommendations",
    operation_id="mangled_extremity_severity_score"
)
async def calculate_mangled_extremity_severity_score(request: MangledExtremitySeverityScoreRequest):
    """
    Calculates MESS score for comprehensive trauma extremity assessment
    
    The Mangled Extremity Severity Score (MESS) is a validated, evidence-based trauma assessment
    tool specifically designed to guide critical treatment decisions for severely injured extremities.
    
    Historical Development and Clinical Context:
    The MESS was developed in 1990 by Johansen et al. in response to the need for objective criteria
    to predict amputation necessity following lower extremity trauma. Prior to its development,
    decisions regarding limb salvage versus amputation were largely subjective and varied significantly
    between surgeons and institutions. The score was derived from analysis of 25 patients with severe
    lower extremity trauma and subsequently validated in larger cohorts.
    
    Four-Factor Assessment Framework:
    
    1. Limb Ischemia (1-3 points, multiplied by 2 if >6 hours):
       The ischemia component evaluates neurovascular compromise, which is critical for limb viability.
       
       - Reduced Pulse, Normal Perfusion (1 point):
         Indicates mild vascular compromise with maintained tissue perfusion. May result from
         vascular spasm, minor vessel injury, or compartment syndrome. Generally associated
         with good salvage potential if addressed promptly.
       
       - Pulseless, Paresthesias, Slow Capillary Refill (2 points):
         Represents moderate vascular compromise with sensory changes and delayed perfusion.
         Indicates significant vascular injury requiring urgent surgical intervention. May be
         associated with compartment syndrome or major vessel disruption.
       
       - Cool, Paralyzed, Numb/Insensate (3 points):
         Signifies severe neurovascular compromise with complete loss of function. Indicates
         major vessel disruption, severe nerve injury, or prolonged ischemia. Associated with
         poor salvage prognosis without immediate intervention.
       
       Duration Factor (>6 hours = double points):
       The 6-hour threshold reflects the concept of "golden hour" for limb salvage, beyond which
       irreversible tissue damage occurs. Prolonged ischemia leads to muscle necrosis, nerve
       death, and systemic complications from reperfusion injury.
    
    2. Patient Age (0-2 points):
       Age reflects physiologic reserve, healing capacity, and ability to withstand major
       reconstructive procedures.
       
       - <30 years (0 points):
         Young patients have optimal healing capacity, better functional adaptation, and
         can tolerate extensive reconstructive procedures. Associated with best outcomes
         for complex limb salvage efforts.
       
       - 30-50 years (1 point):
         Middle-aged patients maintain good healing capacity but may have emerging
         comorbidities. Generally good candidates for limb salvage with appropriate
         surgical planning and realistic functional expectations.
       
       - ≥50 years (2 points):
         Older patients have reduced healing capacity, increased comorbidities, and may
         have difficulty with prolonged rehabilitation. Higher risk for complications
         and may benefit from prosthetic rehabilitation versus complex reconstruction.
    
    3. Shock Status (0-2 points):
       Systemic hemodynamic status affects healing, infection risk, and ability to undergo
       multiple procedures required for limb salvage.
       
       - No Shock, SBP >90 mmHg (0 points):
         Hemodynamically stable patients can tolerate complex procedures and have optimal
         healing conditions. Associated with best outcomes for limb salvage efforts.
       
       - Transient Hypotension (1 point):
         Patients who experienced temporary hypotension but respond to resuscitation.
         Indicates moderate physiologic stress but generally compatible with salvage
         efforts if other factors are favorable.
       
       - Persistent Hypotension (2 points):
         Ongoing hemodynamic instability indicates severe physiologic compromise.
         Associated with poor healing, increased infection risk, and may necessitate
         damage control approaches prioritizing life over limb.
    
    4. Injury Mechanism (1-4 points):
       Energy level determines extent of tissue damage, contamination, and complexity
       of reconstruction required.
       
       - Low Energy (1 point): Stab wounds, simple fractures, pistol gunshot wounds
         Limited tissue damage with discrete injury patterns. Generally amenable to
         straightforward repair with good functional outcomes.
       
       - Medium Energy (2 points): Open/multiple fractures, dislocations
         Moderate tissue damage requiring complex reconstruction. May involve multiple
         tissue types but generally salvageable with appropriate expertise.
       
       - High Energy (3 points): High-speed MVA, rifle gunshot wounds
         Extensive tissue damage with significant bone and soft tissue loss. Requires
         complex reconstructive techniques and prolonged rehabilitation.
       
       - Very High Energy (4 points): High-speed trauma with gross contamination
         Massive tissue destruction with significant contamination. Associated with
         highest complication rates and poorest functional outcomes even if salvaged.
    
    Score Interpretation and Clinical Decision-Making:
    
    Low Risk (1-6 points) - Limb Salvage Recommended:
    Scores in this range indicate good potential for successful limb preservation with
    functional outcomes superior to amputation. Patients should undergo aggressive
    salvage efforts including:
    - Immediate vascular repair for ischemic injuries
    - Fracture stabilization with appropriate fixation
    - Soft tissue reconstruction using local or free tissue transfer
    - Early rehabilitation and functional restoration
    
    Management priorities include rapid surgical intervention, multidisciplinary team
    involvement, and comprehensive rehabilitation planning to optimize functional outcomes.
    
    Borderline Risk (7 points) - Clinical Judgment Required:
    The traditional MESS threshold of 7 points requires careful consideration of multiple
    factors beyond the score itself:
    
    Patient Factors:
    - Age and overall health status
    - Functional expectations and lifestyle
    - Psychological readiness for reconstruction vs. prosthetic use
    - Social support systems for prolonged rehabilitation
    
    Institutional Factors:
    - Surgeon experience with complex reconstruction
    - Available resources for multidisciplinary care
    - Rehabilitation facilities and prosthetic services
    - Long-term follow-up capabilities
    
    Modern Considerations:
    Advances in surgical techniques since 1990 have improved salvage rates, leading many
    experts to recommend higher thresholds (8-9 points) for amputation consideration.
    These advances include:
    - Improved vascular reconstruction techniques
    - Advanced wound management and tissue transfer options
    - Better antibiotic prophylaxis and infection control
    - Enhanced rehabilitation and prosthetic technologies
    
    High Risk (8-14 points) - Amputation Often Appropriate:
    Higher scores suggest that primary amputation may provide better functional outcomes
    than attempted salvage. Considerations include:
    
    Advantages of Primary Amputation:
    - Shorter recovery time and hospital stay
    - Reduced risk of multiple procedures and complications
    - Predictable functional outcomes with modern prosthetics
    - Lower overall healthcare costs and resource utilization
    
    Salvage Considerations:
    Even with high scores, salvage may be considered in selected cases with:
    - Young, highly motivated patients
    - Experienced surgical teams
    - Excellent institutional resources
    - Realistic patient expectations
    - Strong social support systems
    
    Contemporary Clinical Applications:
    
    Emergency Department Use:
    MESS provides objective criteria for initial triage and surgical planning in the
    emergency setting. It facilitates communication between emergency physicians,
    trauma surgeons, orthopedic surgeons, and vascular surgeons regarding management
    priorities and resource allocation.
    
    Surgical Planning:
    The score helps guide surgical approach, including:
    - Timing of intervention (immediate vs. staged)
    - Type of reconstruction required
    - Need for multidisciplinary team involvement
    - Resource allocation and OR scheduling
    
    Patient and Family Communication:
    MESS provides evidence-based framework for discussing prognosis, treatment options,
    and expected outcomes with patients and families. It supports informed consent
    processes and shared decision-making.
    
    Quality Assurance and Research:
    The score facilitates standardized outcome assessment, quality improvement initiatives,
    and research comparing treatment approaches across institutions.
    
    Limitations and Contemporary Considerations:
    
    Validation Limitations:
    - Original development in relatively small cohort
    - Limited validation in diverse populations
    - Primarily studied in lower extremity trauma
    - Less reliable in pediatric and upper extremity injuries
    
    Modern Surgical Advances:
    - Improved vascular reconstruction techniques
    - Advanced microsurgical tissue transfer options
    - Better infection control and wound management
    - Enhanced rehabilitation and prosthetic technologies
    
    Psychosocial Factors:
    - Patient preferences and quality of life considerations
    - Psychological readiness for reconstruction vs. amputation
    - Social support systems and rehabilitation resources
    - Long-term functional expectations and lifestyle goals
    
    Implementation Recommendations:
    
    Clinical Decision-Making:
    - Use MESS as one component of comprehensive assessment
    - Consider patient-specific factors beyond the score
    - Involve multidisciplinary team in decision-making
    - Respect patient preferences and values
    
    Quality Assurance:
    - Regular audit of outcomes by MESS score ranges
    - Comparison of institutional results with published data
    - Continuous quality improvement based on outcome analysis
    - Staff education on proper score calculation and interpretation
    
    Research Applications:
    - Standardized outcome reporting in trauma research
    - Comparison of treatment approaches across institutions
    - Development of modified or enhanced scoring systems
    - Investigation of factors not captured in original score
    
    Future Directions:
    
    Score Enhancement:
    - Integration of modern imaging and laboratory markers
    - Incorporation of patient-reported outcome measures
    - Development of pediatric and upper extremity-specific versions
    - Validation in diverse populations and healthcare systems
    
    Technology Integration:
    - Electronic health record integration for automated calculation
    - Decision support systems for treatment recommendations
    - Mobile applications for bedside assessment
    - Artificial intelligence enhancement of prediction accuracy
    
    The MESS remains a valuable tool for trauma care despite its limitations, providing
    objective criteria to guide one of the most challenging decisions in trauma surgery.
    Its continued use should be coupled with clinical judgment, patient preferences,
    and consideration of advances in surgical and rehabilitation techniques.
    
    Args:
        request: MESS parameters including ischemia, duration, age, shock, and mechanism
        
    Returns:
        MangledExtremitySeverityScoreResponse: Comprehensive trauma assessment with salvage guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mangled_extremity_severity_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MESS score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MangledExtremitySeverityScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MESS calculation",
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
                "message": "Internal error in MESS calculation",
                "details": {"error": str(e)}
            }
        )