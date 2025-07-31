"""
COVID Home Safely Now (CHOSEN) Risk Score Router

Endpoint for calculating CHOSEN Risk Score to assess COVID-19 patient discharge suitability.

The CHOSEN Risk Score provides evidence-based criteria for determining whether 
COVID-19 patients can be safely discharged home by predicting 14-day risk of 
clinical deterioration, need for supplemental oxygen, ICU-level care, or mortality.

Clinical Applications:
- Objective discharge criteria during COVID-19 pandemic periods
- Risk stratification for home-based care program eligibility
- Resource allocation support during hospital surge capacity
- Clinical decision support for safe discharge planning

References (Vancouver style):
1. Levine DM, Ouchi K, Blanchfield B, Diamond A, Licurse A, Pu CT, et al. 
   Hospital-level care at home for acutely ill adults: a pilot randomized 
   controlled trial. J Gen Intern Med. 2018;33(5):729-736.
2. Levine DM, Ouchi K, Blanchfield B, Saenz A, Burke K, Paz M, et al. 
   Hospital-Level Care at Home for Acutely Ill Adults: A Randomized Controlled Trial. 
   Ann Intern Med. 2020;172(2):77-85.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.chosen_covid_discharge import (
    ChosenCovidDischargeRequest,
    ChosenCovidDischargeResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/chosen_covid_discharge",
    response_model=ChosenCovidDischargeResponse,
    summary="Calculate COVID Home Safely Now",
    description="Predicts suitability for discharge in COVID-19 patients by assessing risk of needing supplemental oxygen, ICU-level care, or death within 14 days",
    response_description="The calculated chosen covid discharge with interpretation",
    operation_id="chosen_covid_discharge"
)
async def calculate_chosen_covid_discharge(request: ChosenCovidDischargeRequest):
    """
    Calculates COVID Home Safely Now (CHOSEN) Risk Score for Discharge Suitability
    
    The CHOSEN Risk Score provides objective, evidence-based criteria for assessing 
    COVID-19 patient suitability for home discharge by predicting 14-day risk of 
    clinical deterioration requiring re-hospitalization, supplemental oxygen therapy, 
    ICU-level interventions, or mortality.
    
    Clinical Background and Validation:
    Developed during the COVID-19 pandemic to address critical needs for objective 
    discharge criteria when hospital capacity management was essential. The tool 
    demonstrated 83% sensitivity and 82% specificity in original validation studies 
    for predicting patients suitable for home-based care programs.
    
    Two-Version Scoring System:
    
    Full CHOSEN Score (with albumin laboratory value):
    - Age stratification: 18-45 years (5 pts), 46-59 years (2 pts), 60-73 years (1 pt), >73 years (0 pts)
    - Oxygen saturation: <94% (0 pts), 94-96% (9 pts), 97-98% (14 pts), >98% (21 pts)  
    - Albumin level: <2.8 g/dL (0 pts), 2.8-3.3 g/dL (5 pts), 3.4-3.7 g/dL (15 pts), >3.7 g/dL (29 pts)
    - Total possible: 0-55 points
    - Discharge threshold: ≥30 points indicates likely suitability for home discharge
    
    Modified CHOSEN Score (when albumin unavailable):
    - Age stratification: Same as full score (0-5 pts)
    - Oxygen saturation: Same as full score (0-21 pts)
    - Respiratory rate: ≤20 breaths/min (10 pts), 21-24 breaths/min (5 pts), ≥25 breaths/min (0 pts)
    - Total possible: 0-36 points  
    - Discharge threshold: ≥20 points indicates likely suitability for home discharge
    
    Clinical Variable Significance:
    
    Age Assessment:
    Reflects epidemiological risk patterns observed throughout the COVID-19 pandemic, 
    with younger patients demonstrating lower risk of severe disease progression, 
    hospitalization requirements, and mortality outcomes.
    
    Oxygen Saturation Evaluation:
    Serves as primary objective measure of respiratory function and COVID-19 disease 
    severity. Hypoxemia strongly correlates with increased risk of clinical deterioration, 
    need for respiratory support, and poor outcomes.
    
    Albumin Level (Full Score):
    Functions as both nutritional marker and inflammatory indicator. Hypoalbuminemia 
    reflects systemic inflammation, poor nutritional status, and reduced physiologic 
    reserve - all associated with worse COVID-19 outcomes and increased mortality risk.
    
    Respiratory Rate (Modified Score):
    Alternative indicator of respiratory distress and disease severity when laboratory 
    values unavailable. Tachypnea suggests increased respiratory effort and potential 
    for clinical deterioration requiring enhanced monitoring.
    
    Clinical Interpretation Framework:
    
    High Risk (Below Threshold):
    - Unlikely suitable for discharge - continued inpatient management recommended
    - Elevated risk for clinical deterioration within 14 days
    - High probability of requiring supplemental oxygen, ICU care, or mortality risk
    - Comprehensive inpatient monitoring and optimization of medical therapy indicated
    
    Borderline Risk (Near Threshold):
    - Clinical judgment required for individualized discharge decision
    - Intermediate risk necessitating consideration of additional factors
    - Assessment of social support, comorbidities, and follow-up accessibility
    - Enhanced monitoring protocols if discharge pursued
    
    Low Risk (Above Threshold):
    - Likely suitable for home discharge with appropriate follow-up arrangements
    - Low risk for clinical deterioration with proper monitoring and support
    - Standard discharge planning with symptom monitoring education
    - Routine outpatient follow-up and care coordination
    
    Implementation Considerations:
    
    Patient Selection Criteria:
    - Adult COVID-19 patients being considered for hospital discharge
    - Stable vital signs with room air oxygen saturation measurement
    - Availability of albumin level (preferred) or respiratory rate assessment
    - Appropriate social support systems for home-based care
    
    Clinical Decision Integration:
    - Use as adjunct to comprehensive clinical assessment, not replacement
    - Consider patient preference, social circumstances, and resource availability
    - Evaluate additional risk factors beyond score components
    - Maintain clear communication with patient and family regarding discharge plan
    
    Quality Assurance Requirements:
    - Accurate vital sign measurement using calibrated equipment
    - Current laboratory values reflecting patient status
    - Documentation of clinical reasoning and additional factors
    - Clear follow-up arrangements and emergency contact information
    
    Pandemic-Specific Applications:
    - Particularly valuable during hospital surge periods when capacity constrained
    - Supports efficient resource allocation while maintaining patient safety
    - Enables objective criteria for home-based care program enrollment
    - Assists with triage decisions during high-volume periods
    
    Follow-up and Monitoring:
    - Arrange appropriate outpatient follow-up within recommended timeframes
    - Provide clear symptom monitoring guidelines and warning sign recognition
    - Consider telemedicine options for convenience and infection control
    - Ensure primary care provider notification and care coordination
    
    Safety Considerations:
    - Tool developed for COVID-19 patients specifically during pandemic conditions
    - Validate score components with comprehensive clinical assessment
    - Consider evolving treatment standards and variant-specific characteristics
    - Monitor outcomes and adjust implementation based on local experience
    
    Args:
        request: ChosenCovidDischargeRequest containing age, oxygen saturation, 
                and either albumin level (for full score) or respiratory rate 
                (for modified score)
        
    Returns:
        ChosenCovidDischargeResponse: Calculated CHOSEN score with comprehensive 
        clinical interpretation, discharge recommendations, and detailed calculation 
        information including risk stratification and monitoring guidance
        
    Raises:
        HTTPException 422: Invalid parameters (age 18-120 years, SpO2 80-100%, 
                          albumin 1.0-6.0 g/dL, respiratory rate 8-50 breaths/min)
        HTTPException 500: Calculation error or internal server error
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation using the calculator service
        result = calculator_service.calculate_score("chosen_covid_discharge", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CHOSEN Risk Score",
                    "details": {
                        "parameters": parameters,
                        "possible_causes": [
                            "Invalid parameter combination",
                            "Mathematical calculation error",
                            "Calculator module not found",
                            "Missing required albumin_level or respiratory_rate"
                        ]
                    }
                }
            )
        
        return ChosenCovidDischargeResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CHOSEN Risk Score calculation",
                "details": {
                    "error": str(e),
                    "parameter_requirements": {
                        "age": "18-120 years",
                        "oxygen_saturation": "80-100%",
                        "albumin_level": "1.0-6.0 g/dL (optional, for full score)",
                        "respiratory_rate": "8-50 breaths/min (optional, for modified score)"
                    },
                    "calculation_requirements": "Either albumin_level or respiratory_rate must be provided"
                }
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Internal error in CHOSEN Risk Score calculation",
                "details": {
                    "error": str(e),
                    "suggestion": "Please verify input parameters and try again"
                }
            }
        )