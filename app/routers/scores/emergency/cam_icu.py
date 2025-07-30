"""
Confusion Assessment Method for the ICU (CAM-ICU) Router

Endpoint for calculating CAM-ICU delirium assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.cam_icu import (
    CamIcuRequest,
    CamIcuResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/cam_icu", response_model=CamIcuResponse)
async def calculate_cam_icu(request: CamIcuRequest):
    """
    Calculates Confusion Assessment Method for the ICU (CAM-ICU) Assessment
    
    The CAM-ICU is a validated bedside instrument for detecting delirium in critically ill 
    patients, including those receiving mechanical ventilation. It provides systematic 
    assessment of the four key features that define delirium and is recommended by the 
    2018 PADIS clinical practice guidelines for routine ICU delirium screening.
    
    **Clinical Background and Significance**:
    
    **Delirium in Critical Care**:
    - Affects 40-87% of ICU patients, with highest rates in mechanically ventilated patients
    - Associated with increased mortality (up to 3-fold increase), longer ICU and hospital stays
    - Leads to long-term cognitive dysfunction and functional disability in survivors
    - Often under-recognized without systematic screening tools like CAM-ICU
    - Economic burden estimated at $4-16 billion annually in the United States
    
    **CAM-ICU Development and Validation**:
    - Developed by Dr. E. Wesley Ely and colleagues at Vanderbilt University
    - Based on the original Confusion Assessment Method (CAM) adapted for ICU use
    - Extensively validated in mechanically ventilated and non-ventilated ICU patients
    - Demonstrates excellent sensitivity (95-100%) and specificity (89-93%)
    - Inter-rater reliability κ = 0.79-0.95 with proper training
    
    **Four-Feature Assessment Framework**:
    
    **Feature 1: Acute Onset or Fluctuating Course**:
    - **Clinical Significance**: Essential feature that must be present for delirium diagnosis
    - **Assessment Method**: Compare current mental status to baseline, review 24-hour documentation
    - **Key Indicators**: Sudden confusion, altered behavior from baseline, waxing/waning symptoms
    - **Clinical Context**: May indicate underlying precipitating factors (infection, medications, metabolic)
    - **Documentation**: Record baseline cognitive function, family input, nursing observations
    
    **Feature 2: Inattention (Letters Attention Test)**:
    - **Clinical Significance**: Core cognitive domain affected in all delirium subtypes
    - **Assessment Method**: Standardized CASABLANCA test (patient squeezes hand for letter "A")
    - **Scoring Criteria**: >2 errors out of 10 letters indicates significant inattention
    - **Alternative Tests**: Picture recognition test if hearing impairment present
    - **Clinical Insight**: Often the earliest detectable sign of developing delirium
    
    **Feature 3: Altered Level of Consciousness**:
    - **Clinical Significance**: Captures both hypoactive and hyperactive delirium presentations
    - **Assessment Method**: Richmond Agitation-Sedation Scale (RASS) evaluation
    - **Scoring Criteria**: Any RASS score ≠ 0 (not alert and calm) indicates altered consciousness
    - **Clinical Application**: Essential for identifying hypoactive delirium (often missed)
    - **Management Impact**: Guides sedation management and mechanical ventilation weaning
    
    **Feature 4: Disorganized Thinking**:
    - **Clinical Significance**: Reflects higher-order cognitive dysfunction and safety awareness
    - **Assessment Method**: Standardized yes/no questions plus two-step commands
    - **Scoring Criteria**: >1 error indicates disorganized thinking patterns
    - **Clinical Manifestations**: Illogical conversation, inappropriate responses, confusion
    - **Care Implications**: Affects capacity for medical decision-making and treatment compliance
    
    **Diagnostic Algorithm and Clinical Decision-Making**:
    
    **CAM-ICU Positive Criteria (All Required)**:
    1. **RASS ≥ -3**: Patient sufficiently awake for meaningful assessment
    2. **Feature 1 Present**: Acute onset or fluctuating mental status changes
    3. **Feature 2 Present**: Inattention demonstrated by >2 errors in attention test
    4. **Feature 3 OR 4 Present**: Either altered consciousness (RASS ≠ 0) or disorganized thinking (>1 error)
    
    **Clinical Management Based on Results**:
    
    **CAM-ICU Positive Management**:
    - **Immediate Assessment**: Comprehensive evaluation for underlying causes
    - **Medication Review**: Discontinue or minimize deliriogenic medications (benzodiazepines, anticholinergics)
    - **Environmental Optimization**: Noise reduction, natural light exposure, sleep-wake cycle maintenance
    - **Non-pharmacological Interventions**: Family involvement, reorientation, cognitive stimulation
    - **Pharmacological Treatment**: Consider antipsychotics for severe agitation if non-drug measures insufficient
    - **Monitoring**: Continue assessments every shift, watch for complications (falls, self-extubation)
    
    **CAM-ICU Negative Management**:
    - **Prevention Focus**: Maintain strategies to prevent delirium development
    - **Risk Factor Modification**: Address modifiable precipitants proactively
    - **Continued Monitoring**: Regular reassessment as delirium can fluctuate or develop
    - **Family Education**: Inform about delirium risk factors and prevention strategies
    
    **Implementation Standards and Quality Assurance**:
    
    **Training Requirements**:
    - Healthcare providers require formal CAM-ICU training and competency assessment
    - Initial training typically 1-2 hours with hands-on practice and case studies
    - Annual competency reassessment recommended for maintaining reliability
    - Web-based training modules available at www.icudelirium.org
    
    **Assessment Frequency and Documentation**:
    - **Routine Screening**: Minimum once per nursing shift for all ICU patients
    - **Additional Assessments**: With significant clinical changes or new symptoms
    - **Documentation Standards**: Record exact responses, assessment timing, clinical context
    - **Quality Metrics** Assessment compliance rates, inter-rater reliability, time to intervention
    
    **Special Populations and Considerations**:
    
    **Mechanically Ventilated Patients**:
    - CAM-ICU specifically validated for use with intubated patients
    - May use head nods or hand squeezes for responses
    - Sedation level assessment critical for determining assessment feasibility
    - Consider sedation interruption protocols to enable regular assessment
    
    **Elderly Patients**:
    - Higher baseline risk for delirium development
    - May have baseline cognitive impairment affecting assessment interpretation
    - Require careful attention to medication effects and metabolic factors
    - Family input particularly valuable for baseline cognitive assessment
    
    **Limitations and Clinical Context**:
    
    **Assessment Limitations**:
    - Cannot be performed in deeply sedated patients (RASS < -3)
    - May have reduced accuracy in severe baseline cognitive impairment
    - Requires adequate hearing and vision for standard administration
    - Cultural and language barriers may affect assessment validity
    
    **Clinical Context Factors**:
    - Recent procedures or medications may temporarily affect cognitive performance
    - Metabolic disturbances (hypoglycemia, electrolyte imbalances) can influence results
    - Sleep deprivation may mimic or contribute to delirium symptoms
    - Pain and discomfort can affect attention and cognitive performance
    
    **Research and Evidence Base**:
    
    **Validation Studies**:
    - Original validation in 38 mechanically ventilated patients (sensitivity 100%, specificity 98%)
    - Multi-center validation in 261 ICU patients (sensitivity 95%, specificity 89%)
    - Validated across diverse ICU populations and geographic regions
    - Demonstrated reliability in both medical and surgical ICU settings
    
    **Clinical Outcomes Research**:
    - Delirium detection associated with improved patient outcomes when coupled with management protocols
    - Quality improvement studies show reduced delirium rates with systematic screening
    - Economic analyses demonstrate cost-effectiveness of delirium prevention programs
    - Long-term cognitive outcome studies support early delirium recognition and intervention
    
    **PADIS Guidelines Integration**:
    - Recommended as preferred delirium assessment tool in 2018 PADIS guidelines
    - Part of comprehensive Pain, Agitation, Delirium, Immobility, and Sleep bundle
    - Integration with sedation protocols and early mobility programs
    - Quality indicator for ICU care and patient safety initiatives
    
    This calculator provides standardized CAM-ICU assessment with evidence-based interpretation 
    to support clinical decision-making, improve delirium recognition, and guide targeted 
    interventions in critically ill patients across diverse ICU settings.
    
    Args:
        request: CAM-ICU assessment parameters including RASS score and feature evaluations
        
    Returns:
        CamIcuResponse: Comprehensive delirium assessment with clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cam_icu", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CAM-ICU assessment",
                    "details": {"parameters": parameters}
                }
            )
        
        return CamIcuResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CAM-ICU assessment",
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