"""
DHAKA Score for Pediatric Dehydration Assessment Router

Endpoint for calculating DHAKA score for dehydration severity assessment in children.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.dhaka_score import (
    DhakaScoreRequest,
    DhakaScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/dhaka_score",
    response_model=DhakaScoreResponse,
    summary="Calculate Dehydration: Assessing Kids Accurately",
    description="Classifies dehydration severity in children under 5 years old with acute diarrhea using four clinical assessment parameters.",
    response_description="The calculated dhaka score with interpretation",
    operation_id="dhaka_score"
)
async def calculate_dhaka_score(request: DhakaScoreRequest):
    """
    Calculates DHAKA Score for Pediatric Dehydration Assessment
    
    The Dehydration: Assessing Kids Accurately (DHAKA) Score is a validated clinical 
    decision tool that classifies dehydration severity in children under 5 years old 
    with acute diarrhea. The score was developed to improve clinical assessment of 
    dehydration in resource-limited settings and has demonstrated superior accuracy 
    compared to the WHO Integrated Management of Childhood Illness (IMCI) algorithm.
    
    **Clinical Background and Development:**
    
    Dehydration due to diarrhea is a leading cause of child mortality worldwide, 
    particularly in low- and middle-income countries. Accurate assessment of 
    dehydration severity is crucial for appropriate management decisions, including 
    the choice between oral rehydration therapy and intravenous fluid resuscitation. 
    Traditional clinical assessment methods often lack precision and reliability, 
    leading to both under-treatment and over-treatment of dehydrated children.
    
    The DHAKA score was developed through a rigorous prospective cohort study 
    conducted at the International Centre for Diarrhoeal Disease Research in 
    Bangladesh. The study used recursive partitioning and logistic regression 
    analysis to identify the clinical variables most strongly associated with 
    objective measures of dehydration.
    
    **Evidence Base and Validation:**
    
    **Original Development Study:**
    The DHAKA score was derived from analysis of children under 60 months presenting 
    with acute diarrhea. The study used weight gain after rehydration as the criterion 
    standard for assessing dehydration severity, providing objective validation of 
    the clinical assessment tool.
    
    **External Validation:**
    A subsequent prospective cohort study externally validated the DHAKA score, 
    comparing its performance to the WHO IMCI algorithm. The validation study 
    included 496 children and demonstrated significantly superior accuracy and 
    reliability compared to existing assessment methods.
    
    **Performance Characteristics:**
    The DHAKA score demonstrated excellent inter-rater reliability (κ = 0.75, 95% CI 
    0.66-0.88) and superior diagnostic accuracy compared to the IMCI algorithm. Each 
    1-point increase in DHAKA score predicted a 0.6% increase in percentage dehydration 
    and increased the odds of both some and severe dehydration by a factor of 1.4.
    
    **DHAKA Score Components and Clinical Assessment:**
    
    **General Appearance (0-4 Points):**
    
    **Normal (0 points):**
    Child appears alert, active, and interactive. Makes appropriate eye contact, 
    responds normally to stimuli, and engages in age-appropriate behavior. This 
    indicates preserved mental status and minimal impact of dehydration on 
    neurological function.
    
    **Restless/Irritable (2 points):**
    Child appears fussy, difficult to console, or unusually restless. May be 
    more irritable than usual, crying more frequently, or showing decreased 
    tolerance for normal activities. This suggests mild to moderate dehydration 
    affecting behavior and comfort.
    
    **Lethargic/Unconscious (4 points):**
    Child appears drowsy, lethargic, or difficult to arouse. May have decreased 
    responsiveness to stimuli, appears weak or listless, or shows altered level 
    of consciousness. This indicates significant dehydration with neurological 
    impact requiring urgent intervention.
    
    **Respirations (0-2 Points):**
    
    **Normal (0 points):**
    Regular, unlabored breathing pattern appropriate for age. Respiratory rate 
    within normal limits without signs of distress. This indicates absence of 
    significant metabolic acidosis.
    
    **Deep (2 points):**
    Deep, rapid breathing pattern suggesting compensatory hyperventilation for 
    metabolic acidosis. Kussmaul respirations indicate significant dehydration 
    with acid-base disturbance requiring urgent correction.
    
    **Skin Pinch Test (0-4 Points):**
    
    **Assessment Technique:**
    Pinch skin on lateral abdominal wall between thumb and forefinger, lift 
    briefly, then release and observe return time. This test assesses skin 
    elasticity and subcutaneous tissue turgor as indicators of hydration status.
    
    **Normal (<2 seconds) (0 points):**
    Skin returns immediately to normal position, indicating good skin elasticity 
    and adequate hydration. Subcutaneous tissue maintains normal turgor.
    
    **Slow (2-5 seconds) (2 points):**
    Skin returns slowly to normal position, indicating decreased skin elasticity 
    and mild to moderate dehydration. Subcutaneous tissue shows reduced turgor.
    
    **Very Slow (>5 seconds) (4 points):**
    Skin returns very slowly or remains tented, indicating severe loss of skin 
    elasticity and significant dehydration. May indicate severe volume depletion 
    requiring immediate intervention.
    
    **Tears (0-2 Points):**
    
    **Assessment Technique:**
    Observe tear production during crying or distress. This requires that the 
    child cry during assessment, which may occur naturally during examination 
    or may need to be induced through appropriate stimulation.
    
    **Normal (0 points):**
    Normal tear production when child cries, with visible moisture in eyes. 
    Indicates adequate hydration and normal lacrimal gland function.
    
    **Decreased (1 point):**
    Reduced tear production when crying, with less visible moisture than expected. 
    Suggests mild to moderate dehydration affecting lacrimal secretion.
    
    **Absent (2 points):**
    No tears visible when child cries despite obvious distress. Indicates 
    significant dehydration with impaired lacrimal gland function.
    
    **Dehydration Classification and Management:**
    
    **No Dehydration (DHAKA 0-1): <3% Fluid Loss**
    
    **Clinical Characteristics:**
    - Child appears well with minimal symptoms
    - Normal or mildly increased fluid losses
    - Preserved oral intake and normal behavior
    - No significant clinical signs of volume depletion
    
    **Management Approach:**
    - Home management with caregiver supervision
    - Encourage continued breastfeeding and normal diet
    - Increase fluid intake with appropriate solutions
    - Zinc supplementation according to WHO recommendations
    - Monitor for progression or improvement
    
    **Follow-up Strategy:**
    - Return for reassessment if symptoms worsen
    - Routine follow-up in 24-48 hours if no improvement
    - Caregiver education about warning signs
    
    **Some Dehydration (DHAKA 2-3): 3-9% Fluid Loss**
    
    **Clinical Characteristics:**
    - Mild to moderate clinical signs of dehydration
    - Some behavioral changes or physical findings
    - May have decreased oral intake
    - Requires close monitoring and intervention
    
    **Management Approach:**
    - Supervised oral rehydration therapy (ORT)
    - WHO/UNICEF ORS solution administration
    - Close monitoring for response to therapy
    - Continue appropriate feeding once stable
    - Zinc supplementation and supportive care
    
    **ORT Protocol:**
    - Children <2 years: 75 mL/kg over 4 hours
    - Children ≥2 years: 50 mL/kg over 4 hours
    - Frequent small volumes to improve tolerance
    - Reassess after 4-6 hours of therapy
    
    **Severe Dehydration (DHAKA ≥4): ≥10% Fluid Loss**
    
    **Clinical Characteristics:**
    - Significant clinical signs of volume depletion
    - Altered mental status or severe behavioral changes
    - Poor oral intake or inability to retain fluids
    - Risk of hemodynamic compromise
    
    **Emergency Management:**
    - Immediate intravenous fluid resuscitation
    - Rapid assessment of vital signs and perfusion
    - Hospital admission for intensive monitoring
    - Correction of electrolyte abnormalities
    - Treatment of underlying complications
    
    **IV Fluid Protocol:**
    - Initial bolus: 20 mL/kg isotonic crystalloid
    - Maintenance plus deficit replacement over 6-8 hours
    - Monitor for fluid overload and electrolyte disturbances
    - Transition to ORT once clinically stable
    
    **Special Considerations and Clinical Context:**
    
    **Age-Specific Factors:**
    Infants under 6 months are at higher risk for rapid deterioration and should 
    have lower thresholds for admission and intensive monitoring. Older children 
    may have better compensatory mechanisms but still require careful assessment.
    
    **Malnutrition Impact:**
    Malnourished children may have altered clinical signs of dehydration, with 
    skin pinch tests being less reliable. Clinical judgment and additional 
    assessment parameters may be needed in these cases.
    
    **Concurrent Illness:**
    Children with fever, respiratory illness, or other concurrent conditions may 
    have modified presentations requiring adjusted interpretation of the DHAKA 
    score components.
    
    **Resource Considerations:**
    The DHAKA score was specifically designed for use in resource-limited settings 
    where sophisticated diagnostic tools may not be available. It relies on readily 
    available clinical assessment techniques that can be performed by healthcare 
    workers at various levels of training.
    
    **Quality Improvement and Training:**
    
    **Implementation Strategies:**
    Successful implementation requires training healthcare providers on proper 
    assessment techniques, particularly for skin pinch testing and recognition 
    of altered mental status in children.
    
    **Standardization Benefits:**
    The DHAKA score provides standardized assessment criteria that can reduce 
    practice variation and improve consistency in dehydration management across 
    different providers and settings.
    
    **Performance Monitoring:**
    Healthcare systems can use DHAKA score implementation to monitor quality 
    of dehydration assessment and track outcomes in pediatric diarrheal disease 
    management.
    
    **Limitations and Considerations:**
    
    **Scope of Validation:**
    The DHAKA score is validated specifically for children under 60 months with 
    acute diarrhea. It should not be used for older children, non-diarrheal 
    causes of dehydration, or chronic conditions.
    
    **Clinical Judgment Integration:**
    While the DHAKA score provides valuable objective assessment, it should be 
    used in conjunction with clinical judgment and consideration of individual 
    patient factors not captured by the scoring system.
    
    **Ongoing Research:**
    Further validation studies in diverse populations and settings will help 
    establish the generalizability of the DHAKA score and identify any needed 
    modifications for different contexts.
    
    **Future Directions:**
    Research into simplified versions, digital implementation tools, and 
    integration with other pediatric assessment protocols may enhance the 
    utility and adoption of the DHAKA score in various healthcare settings.
    
    Args:
        request: DHAKA score parameters including general appearance, respirations, 
                skin pinch test results, and tear production, with optional age 
                and diarrhea duration for clinical context
        
    Returns:
        DhakaScoreResponse: Comprehensive dehydration assessment including DHAKA 
        score, dehydration category, fluid loss estimation, management recommendations, 
        and caregiver education guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("dhaka_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating DHAKA Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return DhakaScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for DHAKA Score",
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