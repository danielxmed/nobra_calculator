"""
CSHA Clinical Frailty Scale (CFS) Router

Endpoint for calculating Clinical Frailty Scale assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.geriatrics.clinical_frailty_scale import (
    ClinicalFrailtyScaleRequest,
    ClinicalFrailtyScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/clinical_frailty_scale", response_model=ClinicalFrailtyScaleResponse)
async def calculate_clinical_frailty_scale(request: ClinicalFrailtyScaleRequest):
    """
    Calculates CSHA Clinical Frailty Scale (CFS) Assessment
    
    The Clinical Frailty Scale is a validated 9-point judgement-based frailty assessment 
    tool that evaluates fitness, comorbidity, function, and cognition to predict survival, 
    mortality, need for institutional care, and other adverse outcomes in older adults 
    aged 65 and over.
    
    **Clinical Background:**
    
    The CFS was developed by the Canadian Study of Health and Aging and is one of the 
    most widely used frailty assessment tools globally. It has been validated across 
    multiple clinical settings and is predictive of mortality in 87% of studies. The 
    scale provides a standardized approach to frailty assessment that can be quickly 
    performed by healthcare professionals across various disciplines.
    
    **Assessment Methodology:**
    
    The CFS uses clinical judgement to assign patients to one of nine categories based 
    on their overall fitness, activity level, comorbidity burden, functional capacity, 
    and cognitive status. Unlike purely objective measures, the CFS incorporates the 
    clinician's holistic assessment of the patient's overall state.
    
    **Nine-Point Scale:**
    
    **1. Very Fit**: Robust, active, energetic, motivated. Exercise regularly. Fittest for age.
    
    **2. Fit**: No severe disease symptoms but less fit than category 1. Exercise occasionally.
    
    **3. Managing Well**: Medical problems well-controlled but not regularly active beyond walking.
    
    **4. Living with Very Mild Frailty**: Not dependent on daily help, but symptoms limit activities.
    
    **5. Living with Mild Frailty**: Need help with complex activities (finances, transportation).
    
    **6. Living with Moderate Frailty**: Need help with all outside activities and keeping house.
    
    **7. Living with Severe Frailty**: Completely dependent for personal care but stable.
    
    **8. Living with Very Severe Frailty**: Completely dependent, approaching end of life.
    
    **9. Terminally Ill**: Life expectancy under 6 months, not otherwise evidently frail.
    
    **Risk Stratification:**
    
    **Very Low Risk (CFS 1-3):**
    - 6-month mortality: <5-10%
    - Hospital readmission: <15-25%
    - Functional decline: <10-20%
    - Excellent candidates for intensive interventions
    - Focus on maintaining fitness and preventing decline
    
    **Mild Risk (CFS 4):**
    - 6-month mortality: 10-15%
    - Hospital readmission: 25-35%
    - Functional decline: 20-30%
    - Vulnerable but independent
    - Benefits from preventive interventions and monitoring
    
    **Moderate Risk (CFS 5-6):**
    - 6-month mortality: 15-25%
    - Hospital readmission: 35-45%
    - Functional decline: 30-50%
    - Limited independence, requires assistance
    - Consider comprehensive geriatric assessment
    
    **High Risk (CFS 7-8):**
    - 6-month mortality: 25-40%
    - Hospital readmission: 45-60%
    - Functional decline: 50-70%
    - High dependency, focus on comfort and appropriate care
    - Consider palliative care consultation
    
    **Very High Risk (CFS 9):**
    - 6-month mortality: >40%
    - Terminal illness with limited life expectancy
    - Focus on end-of-life care and family support
    - Palliative care indicated
    
    **Clinical Applications:**
    
    **Emergency Department:**
    - Risk stratification for older adults
    - Predicting adverse outcomes and length of stay
    - Guiding disposition decisions
    - Identifying patients needing comprehensive assessment
    
    **Surgical Settings:**
    - Preoperative risk assessment
    - Surgical decision-making and consent discussions
    - Predicting postoperative complications
    - Planning postoperative care and discharge
    
    **ICU Settings:**
    - Admission decisions and goals of care
    - Predicting ICU mortality and resource utilization
    - Family discussions about treatment limitations
    - Palliative care consultation triggers
    
    **Hospital Medicine:**
    - Discharge planning and resource allocation
    - Predicting readmission risk
    - Identifying patients for geriatric consultation
    - Care transition planning
    
    **Long-term Care:**
    - Placement decisions and level of care
    - Care planning and goal setting
    - Resource allocation and staffing
    - Family communication and education
    
    **Assessment Guidelines:**
    
    **Patient Requirements:**
    - Age 65 years or older (only validated population)
    - Assessment by trained healthcare professional
    - Consider visual chart to assist with classification
    - Account for baseline function before acute illness
    
    **Assessment Process:**
    - Review patient's usual functional status
    - Consider mobility, independence, comorbidities
    - Assess cognitive function and social support
    - Use clinical judgement for borderline cases
    - Document rationale for assigned level
    
    **Special Considerations:**
    
    **Dementia Patients:**
    - Cognitive impairment affects frailty assessment
    - Consider functional capacity in addition to physical fitness
    - May require input from caregivers for accurate assessment
    - Higher risk category even if physically robust
    
    **Acute Illness:**
    - Assess baseline function before current illness
    - Avoid assessing during acute decompensation
    - Consider recovery potential when assigning level
    - May need reassessment after acute phase
    
    **Cultural Considerations:**
    - Consider cultural differences in activity expectations
    - Account for social and family support systems
    - Understand cultural attitudes toward aging and independence
    - Adapt assessment approach as appropriate
    
    **Predictive Validity:**
    
    **Mortality Prediction:**
    - Validated predictor of 30-day, 6-month, and 1-year mortality
    - Performs well across multiple clinical settings
    - Predictive accuracy maintained across age groups
    - Independent predictor after adjustment for comorbidities
    
    **Functional Outcomes:**
    - Predicts functional decline and disability progression
    - Associated with falls, delirium, and complications
    - Predicts need for institutional care
    - Useful for rehabilitation potential assessment
    
    **Healthcare Utilization:**
    - Predicts length of hospital stay
    - Associated with readmission rates
    - Predicts emergency department visits
    - Useful for resource planning and allocation
    
    **Quality Assurance:**
    
    **Training Requirements:**
    - Healthcare professionals should receive training
    - Understand scale definitions and assessment principles
    - Practice with clinical vignettes and examples
    - Regular calibration exercises to maintain accuracy
    
    **Documentation Standards:**
    - Record CFS level with supporting rationale
    - Note any factors influencing assessment
    - Update assessment if clinical status changes
    - Use for care planning and communication
    
    **Inter-rater Reliability:**
    - Good agreement between trained assessors
    - Visual aids improve consistency
    - Regular training maintains reliability
    - Consider second opinion for borderline cases
    
    **Evidence Base:**
    
    The CFS has been extensively validated across multiple populations and clinical 
    settings. Key studies demonstrate its predictive validity for mortality, functional 
    decline, and healthcare utilization. The scale has been adopted internationally 
    and is recommended by multiple geriatric and emergency medicine societies.
    
    **Implementation Considerations:**
    
    **Workflow Integration:**
    - Incorporate into admission assessments
    - Include in multidisciplinary team discussions
    - Use for care planning and goal setting
    - Consider for quality improvement initiatives
    
    **Staff Education:**
    - Provide training on scale use and interpretation
    - Develop local protocols and guidelines
    - Share case examples and challenging scenarios
    - Regular competency assessment and updates
    
    **Technology Integration:**
    - Include in electronic health records
    - Develop clinical decision support tools
    - Create automated risk stratification alerts
    - Enable trend analysis and outcome tracking
    
    Args:
        request: Clinical Frailty Scale parameters including frailty level (1-9), 
                patient age (≥65 years), and optional dementia status
        
    Returns:
        ClinicalFrailtyScaleResponse: Comprehensive frailty assessment with risk 
        stratification, clinical recommendations, predictive outcomes, intervention 
        suitability, and care planning guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("clinical_frailty_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CSHA Clinical Frailty Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return ClinicalFrailtyScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CSHA Clinical Frailty Scale",
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