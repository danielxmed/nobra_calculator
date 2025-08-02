"""
Rule of Nines Router

Endpoint for calculating Rule of Nines burn assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.rule_of_nines import (
    RuleOfNinesRequest,
    RuleOfNinesResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/rule_of_nines",
    response_model=RuleOfNinesResponse,
    summary="Calculate Rule of Nines Burn Assessment",
    description="Calculates total body surface area (TBSA) burned using the validated Rule of Nines methodology "
                "for rapid burn assessment in emergency settings. This essential tool divides the body into "
                "anatomical regions representing 9% (or multiples of 9%) of total body surface area, with "
                "age-specific adjustments for adults versus children/infants due to different body proportions. "
                "Adult percentages: head/neck 9%, each arm 9%, anterior torso 18%, posterior torso 18%, "
                "each leg 18%, genitalia 1%. Pediatric percentages: head/neck 18%, each arm 9%, anterior "
                "torso 18%, posterior torso 18%, each leg 13.5%, genitalia 1%. The assessment determines "
                "burn severity classification (minor <10%, moderate 10-19%, major 20-29%, severe ≥30% TBSA) "
                "and guides critical clinical decisions including fluid resuscitation requirements (≥10% TBSA "
                "in adults, ≥5% in children), burn center transfer criteria, and initial treatment planning. "
                "Results provide evidence-based recommendations for fluid management using Parkland formula, "
                "monitoring protocols, and appropriate level of care based on American Burn Association guidelines.",
    response_description="Rule of Nines TBSA calculation with burn severity classification and comprehensive clinical management recommendations",
    operation_id="rule_of_nines"
)
async def calculate_rule_of_nines(request: RuleOfNinesRequest):
    """
    Rule of Nines Burn Assessment and Total Body Surface Area Calculation
    
    Calculates the total body surface area (TBSA) burned using the validated Rule of Nines 
    methodology, providing rapid burn assessment critical for emergency clinical decision-making. 
    This standardized tool enables healthcare providers to quickly estimate burn severity, 
    determine fluid resuscitation requirements, assess burn center transfer needs, and guide 
    initial treatment planning in emergency and trauma settings.
    
    Historical Development and Clinical Validation:
    The Rule of Nines was originally developed by Pulaski and Tennison in 1947 and 
    subsequently refined and published by Alexander Burns Wallace in 1951. This tool 
    has become the international standard for rapid burn assessment due to its simplicity, 
    reliability, and clinical utility in emergency situations where immediate treatment 
    decisions are critical.
    
    The method has been extensively validated across diverse patient populations and 
    clinical settings, demonstrating consistent utility for initial burn assessment 
    despite recognized limitations in specific populations such as obese patients and 
    very young children.
    
    Anatomical Basis and Age-Specific Considerations:
    
    Adult Anatomical Proportions (Age >14 years):
    The Rule of Nines for adults is based on the anatomical reality that the human 
    body can be divided into regions that each represent approximately 9% of total 
    body surface area:
    
    - Head and Neck: 9% of TBSA
      * Includes face, scalp, ears, and neck
      * Anterior face and scalp: 4.5%
      * Posterior head and neck: 4.5%
    
    - Upper Extremities: 9% each (18% total)
      * Includes shoulder, upper arm, forearm, and hand
      * Each arm represents complete extremity from shoulder to fingertips
    
    - Torso: 36% total
      * Anterior torso (chest and abdomen): 18%
      * Posterior torso (back): 18%
    
    - Lower Extremities: 18% each (36% total)
      * Includes hip, thigh, knee, lower leg, and foot
      * Each leg represents complete extremity from hip to toes
    
    - Genitalia and Perineum: 1%
      * External genitalia and perineal region
    
    Total: 100% TBSA
    
    Pediatric Anatomical Proportions (Age ≤14 years):
    Children and infants have significantly different body proportions compared to 
    adults, with proportionally larger heads and smaller lower extremities. The 
    pediatric Rule of Nines adjusts for these developmental anatomy differences:
    
    - Head and Neck: 18% of TBSA (double adult proportion)
      * Reflects proportionally larger head size in children
      * Critical for accurate assessment in pediatric burn patients
    
    - Upper Extremities: 9% each (same as adults)
      * Arm proportions remain similar across age groups
    
    - Torso: 36% total (same as adults)
      * Anterior torso: 18%
      * Posterior torso: 18%
    
    - Lower Extremities: 13.5% each (27% total)
      * Significantly smaller proportion than adults
      * Reflects shorter leg length relative to total body size
    
    - Genitalia and Perineum: 1% (same as adults)
    
    Total: 100% TBSA
    
    Clinical Assessment Protocol and Methodology:
    
    Burn Depth Classification and TBSA Inclusion:
    Accurate TBSA calculation requires proper classification of burn depth, as only 
    certain burn types are included in the assessment:
    
    First-Degree Burns (Superficial):
    - Involve only the epidermis with erythema and pain
    - Typically excluded from TBSA calculations
    - Do not contribute to fluid resuscitation requirements
    - Heal spontaneously without scarring
    
    Second-Degree Burns (Partial Thickness):
    - Involve epidermis and varying degrees of dermis
    - Included in TBSA calculations
    - Subdivided into superficial and deep partial thickness
    - Require specialized wound care and monitoring
    
    Third-Degree Burns (Full Thickness):
    - Involve complete destruction of epidermis and dermis
    - Included in TBSA calculations
    - Appear white, brown, or charred with loss of sensation
    - Require surgical intervention for optimal healing
    
    Fourth-Degree Burns (Deep Full Thickness):
    - Extend beyond skin into subcutaneous tissue, muscle, or bone
    - Included in TBSA calculations
    - Life-threatening injuries requiring immediate surgical care
    
    Systematic Assessment Approach:
    1. Examine patient systematically by anatomical region
    2. Assess burn depth for each area using visual and tactile examination
    3. Estimate percentage of each body region affected by second-degree or deeper burns
    4. Document findings using standardized burn charts or body diagrams
    5. Calculate total TBSA using age-appropriate Rule of Nines percentages
    6. Consider alternative assessment methods for validation when indicated
    
    Clinical Decision-Making Framework and Treatment Thresholds:
    
    Fluid Resuscitation Requirements:
    The TBSA calculation directly determines the need for formal fluid resuscitation:
    
    Adult Patients:
    - Burns ≥10% TBSA require formal fluid resuscitation
    - Use Parkland Formula: 4 mL/kg/% TBSA of lactated Ringer's over 24 hours
    - Administer first half of calculated volume in first 8 hours post-burn
    - Monitor urine output target: 0.5-1 mL/kg/hour
    
    Pediatric Patients:
    - Burns ≥5% TBSA require formal fluid resuscitation
    - Same Parkland Formula with weight-based calculations
    - Monitor urine output target: 1-1.5 mL/kg/hour
    - Consider maintenance fluid requirements in addition to resuscitation
    
    Burn Severity Classification and Management Implications:
    
    Minor Burns (<10% TBSA):
    - Generally suitable for outpatient management
    - Comprehensive wound care and pain management
    - Tetanus prophylaxis and infection prevention
    - Structured follow-up within 24-48 hours
    - Patient education on wound care and warning signs
    
    Moderate Burns (10-19% TBSA):
    - Typically require hospital admission
    - Formal fluid resuscitation and hemodynamic monitoring
    - Specialized wound care and pain management
    - Early burn center consultation for care coordination
    - Nutritional assessment and infection surveillance
    
    Major Burns (20-29% TBSA):
    - Require immediate burn center transfer
    - Aggressive fluid resuscitation with invasive monitoring
    - Early surgical consultation for potential escharotomy
    - Comprehensive supportive care and complication prevention
    - Multidisciplinary team approach for optimal outcomes
    
    Severe Burns (≥30% TBSA):
    - Life-threatening injuries with significant mortality risk
    - Immediate intensive care and burn center management
    - Early airway assessment and respiratory support
    - Massive fluid resuscitation with careful monitoring
    - Early surgical intervention and aggressive supportive care
    
    Burn Center Transfer Criteria:
    
    American Burn Association Guidelines specify transfer criteria including:
    - Burns >10% TBSA in patients <10 or >50 years old
    - Burns >20% TBSA in other age groups
    - Full-thickness burns >5% TBSA in any age group
    - Burns involving face, hands, feet, genitalia, perineum, or major joints
    - Circumferential burns of extremities or chest
    - Electrical burns, chemical burns, or lightning injuries
    - Inhalation injury
    - Burns in patients with preexisting conditions affecting healing
    - Burns with concomitant trauma where burn poses greatest risk
    
    Special Clinical Considerations and Complications:
    
    Circumferential Burns:
    - Burns completely encircling an extremity or the torso
    - Risk for compartment syndrome requiring emergency escharotomy
    - Monitor distal perfusion, pulses, and compartment pressures
    - Immediate surgical consultation regardless of total TBSA
    
    Inhalation Injury:
    - Significantly increases morbidity and mortality
    - May require increased fluid resuscitation beyond standard formulas
    - Early assessment for airway compromise and respiratory support needs
    - Consider bronchoscopy for diagnosis and pulmonary toileting
    
    Electrical Burns:
    - May have extensive internal tissue damage despite small external burns
    - TBSA calculation may significantly underestimate true injury severity
    - Require cardiac monitoring and assessment for rhabdomyolysis
    - Entry and exit wounds should be carefully documented and managed
    
    Chemical Burns:
    - Require immediate and prolonged decontamination
    - Depth and extent of injury may evolve over time
    - Initial TBSA assessment may underestimate final burn size
    - Specific antidotes and treatments may be required
    
    Assessment Limitations and Alternative Methods:
    
    Rule of Nines Limitations:
    - Less accurate in obese patients due to altered body proportions
    - May be imprecise for very young children despite pediatric adjustments
    - Rapid estimation tool - not as precise as detailed assessment methods
    - Assumes standard body proportions that may not apply to all patients
    
    Alternative Assessment Methods:
    
    Lund-Browder Chart:
    - More accurate than Rule of Nines, especially for children
    - Provides age-specific body proportion adjustments
    - Recommended for definitive TBSA assessment in burn centers
    - More complex to use but provides greater precision
    
    Rule of Palms:
    - Patient's palm including fingers represents approximately 1% TBSA
    - Useful for estimating small or scattered burns
    - Can be combined with Rule of Nines for complex patterns
    - May overestimate by 10-20% in some studies
    
    Digital Assessment Tools:
    - Smartphone applications with burn mapping capabilities
    - Computer-assisted assessment programs
    - Digital photography with area analysis software
    - May reduce human error and improve assessment consistency
    
    Quality Assurance and Continuous Improvement:
    
    Assessment Validation:
    - Regular comparison of Rule of Nines estimates with more precise methods
    - Inter-observer reliability testing for assessment consistency
    - Correlation of initial estimates with final burn size after resuscitation
    - Documentation of factors affecting assessment accuracy
    
    Clinical Outcome Monitoring:
    - Fluid resuscitation adequacy and hemodynamic response
    - Hospital length of stay and resource utilization
    - Infection rates and wound healing outcomes
    - Functional recovery and quality of life measures
    - Mortality and morbidity correlations with TBSA estimates
    
    Staff Training and Education:
    - Regular burn assessment training for emergency providers
    - Standardized protocols for Rule of Nines application
    - Integration with simulation training and competency assessment
    - Ongoing education on burn care advances and best practices
    
    The Rule of Nines remains an essential tool for rapid burn assessment in 
    emergency medicine, providing critical information for immediate clinical 
    decision-making while serving as the foundation for comprehensive burn care 
    and optimal patient outcomes.
    
    Args:
        request: Rule of Nines assessment parameters including age group and percentage burns for each body region
        
    Returns:
        RuleOfNinesResponse: Total body surface area burned with comprehensive burn severity assessment and clinical management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("rule_of_nines", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Rule of Nines burn assessment",
                    "details": {"parameters": parameters}
                }
            )
        
        return RuleOfNinesResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Rule of Nines assessment",
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
                "message": "Internal error in Rule of Nines burn assessment",
                "details": {"error": str(e)}
            }
        )