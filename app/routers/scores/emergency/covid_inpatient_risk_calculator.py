"""
COVID-19 Inpatient Risk Calculator (CIRC) Router

Endpoint for calculating CIRC risk assessment for COVID-19 hospitalized patients.

The CIRC predicts likelihood of inpatient mortality or severe disease progression 
in COVID-19 patients within 7 days of hospital admission using 23 clinical variables 
available at admission. This evidence-based tool supports risk stratification, 
resource allocation, and clinical decision-making in hospitalized COVID-19 patients.

Clinical Applications:
- Early identification of high-risk patients requiring intensive monitoring
- Resource allocation decisions during hospital surge capacity periods
- Clinical trial enrollment and treatment escalation decisions
- Goals of care discussions with patients and families
- Discharge planning and step-down care considerations

References (Vancouver style):
1. Garibaldi BT, Fiksel J, Muschelli J, Robinson ML, Rouhizadeh M, Perin J, et al. 
   Patient Trajectories Among Persons Hospitalized for COVID-19: A Cohort Study. 
   Ann Intern Med. 2021;174(1):33-41. doi: 10.7326/M20-3905.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.covid_inpatient_risk_calculator import (
    CovidInpatientRiskCalculatorRequest,
    CovidInpatientRiskCalculatorResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/covid_inpatient_risk_calculator", response_model=CovidInpatientRiskCalculatorResponse)
async def calculate_covid_inpatient_risk_calculator(request: CovidInpatientRiskCalculatorRequest):
    """
    Calculates COVID-19 Inpatient Risk Calculator (CIRC) for Hospitalized Patient Risk Assessment
    
    The CIRC provides evidence-based risk stratification for COVID-19 hospitalized patients 
    by predicting the 7-day probability of severe disease progression or mortality using 
    23 clinical variables available at hospital admission. This machine learning-derived 
    model supports clinical decision-making and resource allocation in COVID-19 care.
    
    Clinical Background and Model Development:
    Developed from 832 COVID-19 patients across 5 Johns Hopkins hospitals during March-April 2020, 
    representing one of the first comprehensive predictive models for COVID-19 progression. 
    The model achieved strong performance with AUC values of 0.85 at day 2, 0.79 at day 4, 
    and 0.79 at day 7, with optimal performance in the first 2 days of hospitalization.
    
    Primary Outcome Definition:
    Predicts progression to severe disease or death within 7 days, where severe disease 
    requires any of the following interventions:
    - High-flow nasal cannula oxygen therapy
    - Non-invasive positive pressure ventilation (NIPPV)
    - Invasive mechanical ventilation
    - Extracorporeal membrane oxygenation (ECMO)
    - Vasopressor support for hemodynamic instability
    
    23-Variable Risk Assessment Framework:
    
    Demographic and Social Risk Factors:
    - Age: Strongest predictor with exponential risk increase in older adults
    - Sex: Male sex associated with increased severity risk across populations
    - Race: Non-white race linked to increased risk due to complex social determinants
    - Nursing home admission: Strong predictor reflecting frailty and comorbidity burden
    
    Comorbidity and Physical Status:
    - BMI: Obesity (>30 kg/m²) significantly increases mechanical ventilation risk
    - Charlson Comorbidity Index: Quantifies pre-existing disease burden impact
    
    Clinical Presentation Profile:
    - Respiratory symptoms: Primary COVID-19 manifestation with prognostic significance
    - Gastrointestinal symptoms: Associated with increased disease severity
    - Constitutional symptoms: Indicates systemic inflammatory response magnitude
    - Loss of taste/smell: Paradoxically may indicate less severe disease course
    - Fever: Common presenting symptom with variable prognostic significance
    
    Physiologic Parameters:
    - Respiratory rate: Tachypnea (>24) indicates respiratory distress and severity
    - Pulse: Tachycardia may reflect hemodynamic stress or systemic inflammation
    
    Laboratory Risk Markers:
    - Hemoglobin: Anemia associated with increased mortality risk
    - White blood cell count: Leukocytosis may indicate superinfection or severe inflammation
    - Absolute lymphocyte count: Lymphopenia (<1.0) strongly predicts poor outcomes
    - Albumin: Hypoalbuminemia (<3.5) reflects nutritional status and inflammation
    - Creatinine: Kidney dysfunction associated with increased COVID-19 mortality
    - ALT: Hepatic involvement indicator and potential drug toxicity marker
    - D-dimer: Coagulopathy marker with thrombotic risk implications (>1.0 mg/L)
    - C-reactive protein: Systemic inflammation indicator with severity correlation
    - Ferritin: Hyperferritinemia (>500) indicates cytokine storm and poor prognosis
    - Troponin: Cardiac injury marker significantly increasing mortality risk
    
    Risk Stratification and Clinical Management:
    
    Low Risk (0-10%):
    - Standard monitoring protocols with routine vital signs and clinical assessment
    - Potential candidate for early discharge planning if hemodynamically stable
    - Standard laboratory monitoring and infection control measures
    - Regular outpatient follow-up arrangements with clear symptom monitoring
    
    Intermediate Risk (10-30%):
    - Enhanced monitoring with frequent vital signs and clinical assessments
    - Consider telemetry monitoring and step-down unit care if available
    - Proactive laboratory monitoring including inflammatory markers
    - Early warning system protocols for clinical deterioration detection
    
    High Risk (30-60%):
    - Intensive monitoring protocols with hourly assessments and close observation
    - ICU consultation for admission consideration and specialized care planning
    - Continuous cardiac and respiratory monitoring with frequent laboratory assessments
    - Goals of care discussions with patients and families regarding prognosis
    
    Very High Risk (>60%):
    - Urgent ICU consultation with likely transfer for maximal supportive care
    - Continuous invasive monitoring and preparation for advanced therapies
    - Immediate goals of care discussions with ethics consultation if needed
    - Priority resource allocation including ICU beds and critical care equipment
    
    Clinical Implementation Guidelines:
    
    Data Collection Requirements:
    - All 23 variables should be collected within first 24 hours of admission
    - Ensure accurate laboratory results and standardized vital sign measurements
    - Document symptom assessment using structured protocols
    - Consider timing of measurements relative to presentation and treatments
    
    Decision Support Integration:
    - Use as adjunct to comprehensive clinical assessment, not replacement for judgment
    - Integrate with institutional early warning systems and clinical protocols
    - Consider additional factors not in model (frailty, functional status, goals)
    - Regular reassessment as clinical condition and treatment response evolve
    
    Quality Assurance and Monitoring:
    - Track model performance and patient outcomes in local population
    - Use for quality improvement initiatives and resource planning decisions
    - Support clinical trial enrollment and treatment protocol implementation
    - Enable risk-adjusted outcome comparisons and institutional benchmarking
    
    Model Limitations and Considerations:
    - Developed during early pandemic with limited external validation
    - Performance may vary with different COVID-19 variants and treatment advances
    - Excludes pediatric patients and developed before widespread vaccination
    - Should be interpreted within context of evolving treatment standards
    
    Args:
        request: CovidInpatientRiskCalculatorRequest containing 23 clinical variables 
                including demographics, symptoms, vital signs, and laboratory values
        
    Returns:
        CovidInpatientRiskCalculatorResponse: Calculated risk probability with 
        comprehensive clinical interpretation, risk stratification, monitoring 
        recommendations, and detailed calculation breakdown
        
    Raises:
        HTTPException 422: Invalid parameters (age 18-120, valid categorical options, 
                          laboratory values within physiologic ranges)
        HTTPException 500: Calculation error or internal server error
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation using the calculator service
        result = calculator_service.calculate_score("covid_inpatient_risk_calculator", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating COVID-19 Inpatient Risk Calculator (CIRC)",
                    "details": {
                        "parameters": parameters,
                        "possible_causes": [
                            "Invalid parameter combination",
                            "Mathematical calculation error",
                            "Calculator module not found",
                            "Missing required clinical variables"
                        ]
                    }
                }
            )
        
        return CovidInpatientRiskCalculatorResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for COVID-19 Inpatient Risk Calculator",
                "details": {
                    "error": str(e),
                    "parameter_requirements": {
                        "age": "18-120 years",
                        "sex": "male or female",
                        "race": "white or non_white",
                        "nursing_home_admission": "yes or no",
                        "bmi": "15.0-60.0 kg/m²",
                        "charlson_score": "0-20 points",
                        "symptoms": "yes or no for each symptom category",
                        "vital_signs": "respiratory rate 8-50, pulse 40-200",
                        "laboratory_values": "within physiologic ranges for each parameter"
                    },
                    "note": "All 23 clinical variables are required for accurate risk assessment"
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
                "message": "Internal error in COVID-19 Inpatient Risk Calculator",
                "details": {
                    "error": str(e),
                    "suggestion": "Please verify all input parameters and try again"
                }
            }
        )