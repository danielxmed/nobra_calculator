"""
Cornell Assessment of Pediatric Delirium (CAPD) Router

Endpoint for calculating CAPD pediatric delirium screening assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.capd import (
    CapdRequest,
    CapdResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/capd",
    response_model=CapdResponse,
    summary="Calculate Cornell Assessment of Pediatric Delirium (CAPD)",
    description="Screens for delirium in pediatric patients through behavioral assessment of awareness, cognition, and psychomotor symptoms.",
    response_description="The calculated capd with interpretation",
    operation_id="calculate_capd"
)
async def calculate_capd(request: CapdRequest):
    """
    Calculates Cornell Assessment of Pediatric Delirium (CAPD) Screening
    
    The CAPD is a validated, rapid observational tool for screening delirium in pediatric 
    patients aged 0-21 years. It provides systematic assessment of eight behavioral domains 
    through routine nursing observations, requiring no patient participation and taking 
    less than 2 minutes to complete.
    
    **Clinical Background and Significance**:
    
    **Pediatric Delirium Epidemiology**:
    - Affects 20-25% of pediatric ICU patients across all age groups
    - Associated with increased mortality, longer ICU and hospital stays
    - Leads to functional disability and potential long-term neurodevelopmental impacts
    - Often under-recognized without systematic screening tools like CAPD
    - Can occur in patients from neonates to young adults (0-21 years)
    
    **CAPD Development and Validation**:
    - Developed specifically for pediatric populations with developmental considerations
    - Based on DSM-5 diagnostic criteria for delirium adapted for children
    - Extensively validated across pediatric age groups with developmental anchor points
    - Demonstrates excellent sensitivity (94.1%) overall with age-specific variations
    - Can be used in both developmentally normal and delayed children
    - Requires no patient participation, based on behavioral observations only
    
    **Eight-Domain Assessment Framework**:
    
    **Awareness and Cognitive Domains**:
    
    **Domain 1: Makes Eye Contact with Caregiver**:
    - **Clinical Significance**: Reflects social engagement and interpersonal awareness
    - **Assessment Method**: Observe during routine care interactions and comfort provision
    - **Developmental Context**: Varies from basic visual tracking in infants to complex social interaction in older children
    - **Scoring**: Always (0) to Never (4) - lower scores indicate better function
    - **Clinical Insight**: Eye contact reflects attention, social awareness, and connection with environment
    
    **Domain 2: Actions are Purposeful**:
    - **Clinical Significance**: Indicates cognitive organization and goal-directed behavior
    - **Assessment Method**: Observe during play, feeding, self-care, and interaction activities
    - **Developmental Context**: Age-appropriate purposeful behavior varies significantly across development
    - **Scoring**: Always (0) to Never (4) - higher scores suggest cognitive disorganization
    - **Clinical Insight**: Purposeful actions demonstrate intact executive function and cognitive planning
    
    **Domain 3: Aware of Surroundings**:
    - **Clinical Significance**: Assesses environmental awareness and orientation capacity
    - **Assessment Method**: Note responses to people, sounds, environmental changes, and medical activities
    - **Developmental Context**: Environmental awareness develops progressively with age and cognitive maturity
    - **Scoring**: Always (0) to Never (4) - reflects attention and consciousness level
    - **Clinical Insight**: Environmental awareness indicates intact attention and perceptual processing
    
    **Domain 4: Communicates Needs and Wants**:
    - **Clinical Significance**: Evaluates communication effectiveness and cognitive clarity
    - **Assessment Method**: Observe during care needs, comfort provision, and interactive activities
    - **Developmental Context**: Communication methods vary from crying and gestures to complex verbal expression
    - **Scoring**: Always (0) to Never (4) - considers age-appropriate communication capacity
    - **Clinical Insight**: Effective communication reflects cognitive organization and expressive abilities
    
    **Psychomotor Activity Domains**:
    
    **Domain 5: Restless**:
    - **Clinical Significance**: Assesses psychomotor agitation and hyperactive delirium features
    - **Assessment Method**: Observe during awake periods, care activities, and rest times
    - **Developmental Context**: Normal activity levels vary significantly by age and developmental stage
    - **Scoring**: Never (0) to Always (4) - higher scores indicate hyperactive symptoms
    - **Clinical Insight**: Restlessness may indicate hyperactive delirium subtype requiring specific management
    
    **Domain 6: Inconsolable**:
    - **Clinical Significance**: Evaluates emotional regulation and response to comfort measures
    - **Assessment Method**: Observe responses to comfort measures, caregiver presence, and soothing activities
    - **Developmental Context**: Comfort responsiveness varies by age, temperament, and developmental level
    - **Scoring**: Never (0) to Always (4) - reflects emotional dysregulation severity
    - **Clinical Insight**: Inconsolability suggests emotional dysregulation common in pediatric delirium
    
    **Domain 7: Underactive (Very Little Movement While Awake)**:
    - **Clinical Significance**: Assesses psychomotor retardation and hypoactive delirium features
    - **Assessment Method**: Observe movement patterns, spontaneous activity, and responses to stimulation
    - **Developmental Context**: Expected activity patterns vary dramatically across pediatric age groups
    - **Scoring**: Never (0) to Always (4) - higher scores suggest hypoactive presentation
    - **Clinical Insight**: Underactivity may indicate hypoactive delirium subtype, often missed without systematic assessment
    
    **Domain 8: Takes Long Time to Respond to Interactions**:
    - **Clinical Significance**: Evaluates processing speed and cognitive efficiency
    - **Assessment Method**: Observe response latency during interactions, care activities, and social engagement
    - **Developmental Context**: Expected response times vary by developmental stage and cognitive maturity
    - **Scoring**: Never (0) to Always (4) - reflects cognitive processing difficulties
    - **Clinical Insight**: Delayed responses indicate cognitive processing impairment affecting functional capacity
    
    **Scoring System and Clinical Decision-Making**:
    
    **Scoring Method**:
    - **Total Score Range**: 0-32 points (8 domains × 4 points each)
    - **Delirium Threshold**: ≥9 points indicates positive screen for delirium
    - **Score Optimization**: Threshold chosen to maximize sensitivity (94.1%) for delirium detection
    - **Severity Interpretation**: Higher scores suggest more severe delirium symptoms and greater functional impairment
    
    **Clinical Decision Framework**:
    - **CAPD Positive (≥9 points)**: Delirium likely present, trigger comprehensive evaluation and management protocols
    - **CAPD Negative (<9 points)**: Delirium unlikely at assessment time, continue prevention and monitoring strategies
    - **Score Trending**: Monitor score changes over time to assess intervention effectiveness and symptom progression
    - **Clinical Context**: Consider medical complexity, medications, and environmental factors in interpretation
    
    **Age-Specific Performance and Considerations**:
    
    **Pediatric Age Groups (0-13 years)**:
    - **Sensitivity**: 94.1% for delirium detection across most pediatric age ranges
    - **Specificity**: Good performance with acceptable false positive rates
    - **Developmental Anchor Points**: Guide age-appropriate behavioral expectations and scoring
    - **Special Populations**: Validated in both developmentally normal and delayed children
    - **Clinical Application**: Excellent screening performance supports routine clinical use
    
    **Adolescent Age Group (13-21 years)**:
    - **Sensitivity**: Reduced to 50% but maintains high specificity (98.1%)
    - **Clinical Implication**: May require additional assessment tools for comprehensive evaluation
    - **Developmental Factors**: Identity formation, independence seeking, and cooperation issues affect assessment
    - **Complementary Tools**: Consider adult delirium screening tools as supplementary assessment
    - **Clinical Recommendation**: Use clinical judgment and multiple assessment approaches
    
    **Implementation Standards and Quality Assurance**:
    
    **Assessment Requirements**:
    - **Frequency**: Perform every nursing shift for all pediatric patients at risk
    - **Duration**: Takes less than 2 minutes to complete by trained bedside nurses
    - **Method**: Based on behavioral observations during routine nursing care activities
    - **Participation**: No patient participation required, purely observational assessment
    - **Documentation**: Record assessment timing, clinical context, and influencing factors
    
    **Training and Competency Standards**:
    - **Initial Training**: Brief education on developmental anchor points and scoring guidelines
    - **Competency Assessment**: Demonstrate understanding of age-appropriate behavioral expectations
    - **Ongoing Education**: Regular updates on pediatric delirium recognition and management
    - **Quality Assurance**: Monitor inter-rater reliability and assessment compliance rates
    - **Reference Resources**: Developmental anchor point charts available for bedside use
    
    **Clinical Management Based on Results**:
    
    **CAPD Positive Management Framework**:
    - **Immediate Assessment**: Comprehensive medical evaluation for precipitating factors
    - **Medication Review**: Discontinue or minimize deliriogenic medications when possible
    - **Environmental Optimization**: Age-appropriate modifications for comfort and safety
    - **Family Involvement**: Engage family in comfort provision and familiar routine maintenance
    - **Multidisciplinary Care**: Coordinate with child life, physical therapy, and developmental specialists
    - **Monitoring**: Continue frequent assessments and document response to interventions
    
    **CAPD Negative Management Approach**:
    - **Prevention Focus**: Maintain strategies to prevent delirium development
    - **Risk Factor Management**: Address modifiable precipitants proactively
    - **Developmental Support**: Provide age-appropriate activities and environmental stimulation
    - **Family Education**: Inform about delirium risk factors and recognition signs
    - **Continued Surveillance**: Regular reassessment as delirium can develop rapidly
    
    **Age-Specific Management Considerations**:
    
    **Infants and Toddlers (0-3 years)**:
    - **Bonding Support**: Maintain parent-child attachment and bonding opportunities
    - **Routine Maintenance**: Support normal feeding, sleeping, and comfort routines
    - **Sensory Considerations**: Provide appropriate sensory stimulation without overwhelm
    - **Comfort Measures**: Use non-pharmacological approaches as primary intervention
    - **Development**: Support age-appropriate developmental activities and stimulation
    
    **Preschool and School-Age (3-13 years)**:
    - **Communication**: Provide age-appropriate explanations and reassurance about medical care
    - **Coping Support**: Use play therapy, art activities, and creative expression for emotional processing
    - **Educational Continuity**: Maintain learning activities and peer contact when possible
    - **Child Life Services**: Engage specialized child life professionals for developmental support
    - **Family Integration**: Support family involvement in care planning and comfort provision
    
    **Adolescents (13-21 years)**:
    - **Autonomy Respect**: Honor privacy needs and involve in care planning decisions
    - **Identity Support**: Address concerns about body image, peer relationships, and independence
    - **Technology Access**: Provide appropriate social connections and communication opportunities
    - **Transition Planning**: Consider transition to adult care models when developmentally appropriate
    - **Mental Health**: Address anxiety, depression, and adjustment issues associated with hospitalization
    
    **Special Populations and Considerations**:
    
    **Developmental Delays and Disabilities**:
    - **Baseline Assessment**: Evaluate behaviors relative to individual developmental baseline
    - **Adaptive Scoring**: Consider modified scoring based on cognitive and developmental capacity
    - **Caregiver Input**: Incorporate family and caregiver observations about behavioral changes
    - **Specialized Teams**: Involve developmental pediatrics and specialized nursing for assessment guidance
    - **Individualized Approach**: Tailor assessment and management to specific developmental needs
    
    **Cultural and Language Considerations**:
    - **Cultural Sensitivity**: Account for cultural differences in behavior expression and comfort measures
    - **Communication Barriers**: Focus on non-verbal behavioral observations when language barriers exist
    - **Family Practices**: Incorporate culturally appropriate comfort measures and care practices
    - **Interpreter Services**: Use professional interpreters for family communication and education
    - **Cultural Liaisons**: Engage cultural specialists when complex cultural factors influence care
    
    **Quality Improvement and Research Applications**:
    
    **Clinical Quality Metrics**:
    - **Incidence Tracking**: Monitor delirium rates by age group, unit, and risk factors
    - **Recognition Timeliness**: Measure time from symptom onset to delirium identification
    - **Assessment Compliance**: Track CAPD completion rates and documentation quality
    - **Outcome Correlation**: Analyze relationships between CAPD scores and clinical outcomes
    - **Intervention Effectiveness**: Evaluate impact of delirium management protocols on patient outcomes
    
    **Research Applications**:
    - **Prevention Studies**: Investigate pediatric delirium prevention strategies and interventions
    - **Developmental Research**: Explore age-specific delirium presentations and risk factors
    - **Family-Centered Care**: Study impact of family involvement on delirium outcomes
    - **Long-term Outcomes**: Assess neurodevelopmental consequences of pediatric delirium
    - **Implementation Science**: Study optimal approaches for CAPD implementation in clinical practice
    
    This calculator provides standardized CAPD assessment with comprehensive clinical interpretation 
    to support early delirium recognition, evidence-based management, and improved outcomes in 
    pediatric patients across diverse clinical settings and developmental stages.
    
    Args:
        request: CAPD assessment parameters including eight domain scores and patient age
        
    Returns:
        CapdResponse: Comprehensive pediatric delirium assessment with age-specific recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("capd", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CAPD assessment",
                    "details": {"parameters": parameters}
                }
            )
        
        return CapdResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CAPD assessment",
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