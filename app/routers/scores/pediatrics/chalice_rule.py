"""
CHALICE (Children's Head injury ALgorithm for the prediction of Important Clinical Events) Rule Router

Endpoint for calculating CHALICE Rule for pediatric head trauma assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.chalice_rule import (
    ChaliceRuleRequest,
    ChaliceRuleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/chalice_rule", response_model=ChaliceRuleResponse)
async def calculate_chalice_rule(request: ChaliceRuleRequest):
    """
    Calculates CHALICE (Children's Head injury ALgorithm for the prediction of Important Clinical Events) Rule
    
    The CHALICE rule is a clinical decision tool developed to predict death, need for neurosurgical 
    intervention, or CT abnormality in children (<16 years) with head trauma. This highly sensitive 
    rule helps identify which pediatric patients require CT imaging after head injury.
    
    **CHALICE Rule Overview**:
    
    **Purpose**: 
    - Determine need for CT imaging in pediatric head trauma (<16 years)
    - Predict clinically important brain injuries requiring intervention
    - Standardize emergency department approach to pediatric head injury
    
    **Development and Validation**:
    - Derived from study of 22,772 children over 2.5 years
    - 98% sensitivity (95% CI: 96-100%) for clinically significant head injury
    - 87% specificity (95% CI: 86-87%)
    - CT scan rate: 14% (significant reduction from routine imaging)
    - 281 children had CT abnormalities, 137 required neurosurgery, 15 deaths
    
    **Clinical Criteria Categories**:
    
    **History Criteria** (any positive indicates CT need):
    1. **Witnessed loss of consciousness >5 minutes**
       - Duration must exceed 5 minutes
       - Must be observed by reliable witness
       - Brief LOC ≤5 minutes is not a positive criterion
    
    2. **Amnesia >5 minutes** (antegrade or retrograde)
       - Memory loss before or after injury exceeding 5 minutes
       - Can be difficult to assess in very young children
       - Both pre-traumatic and post-traumatic amnesia qualify
    
    3. **Abnormal drowsiness**
       - As reported by parent or primary caregiver
       - Subjective assessment of unusual sleepiness
       - Important parental concern indicator
    
    4. **≥3 vomits after head injury**
       - Three or more episodes post-trauma
       - May indicate increased intracranial pressure
       - Must be post-traumatic, not pre-existing
    
    5. **Suspicion of non-accidental injury**
       - Based on mechanism, injuries, or inconsistent history
       - Important safeguarding consideration
       - Requires careful documentation and appropriate referral
    
    6. **Seizure after head injury**
       - New-onset seizure following trauma
       - Must have no previous history of epilepsy
       - Post-traumatic seizures indicate brain injury
    
    **Examination Criteria** (any positive indicates CT need):
    1. **Glasgow Coma Score abnormal**
       - Age-dependent thresholds: <15 for <1 year, <14 for ≥1 year
       - Accounts for developmental differences in neurological assessment
       - Lower thresholds in infants reflect different normal ranges
    
    2. **Suspicion of penetrating/depressed skull injury**
       - Clinical assessment of skull integrity
       - Visible depression, penetrating wounds, palpable defects
       - High-risk mechanism requiring immediate imaging
    
    3. **Signs of basal skull fracture**
       - CSF rhinorrhea/otorrhea, panda eyes, Battle's sign, hemotympanum
       - Indicates significant skull base trauma
       - High association with intracranial injury
    
    4. **Positive focal neurologic sign**
       - Any new focal neurological deficit
       - Motor, sensory, or cranial nerve abnormalities
       - Indicates localized brain injury
    
    5. **Bruise/swelling/laceration >5 cm** (if <1 year old only)
       - Only applies to infants <1 year of age
       - Size threshold indicates significant trauma force
       - Reflects increased vulnerability in this age group
    
    **Mechanism Criteria** (any positive indicates CT need):
    1. **High-speed road traffic accident** (>40 mph/65 km/h)
       - High-energy mechanism associated with severe injuries
       - Includes pedestrian struck by vehicle at high speed
       - Speed threshold based on injury severity data
    
    2. **Fall from height >3 meters** (>10 feet)
       - Significant mechanism based on gravitational force
       - Height threshold based on injury outcome data
       - Common pediatric injury mechanism
    
    3. **High-speed injury from projectile/object**
       - High-velocity impact from objects or projectiles
       - Sports equipment, tools, or other high-energy impacts
       - Mechanism suggests significant force transmission
    
    **Clinical Decision Algorithm**:
    - **If ANY criterion is positive**: Proceed with head CT
    - **If NO criteria are positive**: Safe to monitor without CT
    - Consider clinical judgment and parental concerns in borderline cases
    - Rule designed for emergency department use
    
    **Performance Characteristics**:
    - **High Sensitivity (98%)**: Minimizes missed significant injuries
    - **Reasonable Specificity (87%)**: Reduces unnecessary CT scans
    - **Low CT Rate (14%)**: Significant reduction in imaging
    - **High NPV (>99%)**: Excellent negative predictive value
    
    **Clinical Applications**:
    - **Emergency Medicine**: Primary tool for pediatric head trauma triage
    - **Pediatrics**: Risk stratification in head-injured children
    - **Quality Improvement**: Standardized approach reducing variation
    - **Safety**: High sensitivity maintains patient safety
    
    **Comparison with Other Rules**:
    - **CHALICE**: 97-99% applicability, 98% sensitivity, 14% CT rate
    - **PECARN**: Higher sensitivity (99-100%) but lower applicability (74-76%)
    - **CATCH**: Different population focus and criteria set
    - **CHALICE advantages**: High applicability with excellent sensitivity
    
    **Implementation Considerations**:
    - Designed specifically for children <16 years
    - Age-specific GCS thresholds are critical
    - Bruise criterion only applies to infants <1 year
    - Consider parental concerns and clinical context
    - Requires clinical judgment for borderline cases
    
    **Clinical Impact**:
    - Standardizes pediatric head trauma assessment
    - Reduces unnecessary radiation exposure in children
    - Improves resource utilization in emergency departments
    - Maintains high safety standards through systematic approach
    - Facilitates evidence-based decision making
    
    This calculator implements the original CHALICE rule to provide systematic, evidence-based 
    guidance for CT imaging decisions in pediatric head trauma, helping clinicians balance 
    safety with appropriate resource utilization.
    
    Args:
        request: CHALICE rule parameters for pediatric head trauma assessment
        
    Returns:
        ChaliceRuleResponse: CT recommendation with detailed criteria analysis
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("chalice_rule", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CHALICE Rule",
                    "details": {"parameters": parameters}
                }
            )
        
        return ChaliceRuleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CHALICE Rule",
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