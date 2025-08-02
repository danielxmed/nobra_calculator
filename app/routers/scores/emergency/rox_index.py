"""
ROX Index for Intubation after HFNC Router

Endpoint for calculating ROX Index for HFNC failure prediction.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.rox_index import (
    RoxIndexRequest,
    RoxIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/rox_index",
    response_model=RoxIndexResponse,
    summary="Calculate ROX Index for Intubation after HFNC",
    description="Calculates the ROX Index to predict high-flow nasal cannula (HFNC) failure and need for "
                "intubation in patients with acute hypoxemic respiratory failure. The ROX Index combines "
                "oxygen saturation (SpO2), fraction of inspired oxygen (FiO2), and respiratory rate into "
                "a single predictive score using the formula: ROX = (SpO2/FiO2) / Respiratory Rate. "
                "This validated clinical decision tool provides early identification of patients at risk "
                "for HFNC treatment failure, enabling timely escalation to invasive mechanical ventilation "
                "and avoiding delayed intubation with its associated complications. The index demonstrates "
                "67% sensitivity and 72% specificity for predicting HFNC failure, with optimal cutoff "
                "values of 4.88 at 12+ hours and time-specific thresholds for earlier assessment. "
                "Results categorize patients into three risk levels: high risk (<3.85) requiring early "
                "intubation consideration, indeterminate risk (3.85-4.87) needing close monitoring and "
                "reassessment, and lower risk (≥4.88) indicating good HFNC response with continued therapy. "
                "Particularly valuable in intensive care units, emergency departments, and respiratory "
                "therapy for evidence-based respiratory support decisions and resource optimization.",
    response_description="ROX Index value with risk stratification and evidence-based clinical management recommendations",
    operation_id="rox_index"
)
async def calculate_rox_index(request: RoxIndexRequest):
    """
    ROX Index for HFNC Failure Prediction and Intubation Risk Assessment
    
    Calculates the validated ROX Index to predict high-flow nasal cannula (HFNC) 
    treatment outcomes in patients with acute hypoxemic respiratory failure (AHRF). 
    This evidence-based clinical decision tool enables early identification of 
    patients at risk for HFNC failure, supporting timely decisions about respiratory 
    support escalation and preventing delayed intubation with associated complications.
    
    Clinical Background and Rationale:
    Acute hypoxemic respiratory failure represents a common and challenging clinical 
    scenario in critical care medicine, with high-flow nasal cannula therapy emerging 
    as an important intermediate respiratory support option between conventional 
    oxygen therapy and invasive mechanical ventilation. However, identifying patients 
    who will benefit from HFNC versus those requiring early intubation remains a 
    critical clinical challenge.
    
    The ROX Index addresses this need by providing objective, quantitative assessment 
    of HFNC treatment response using three readily available clinical parameters: 
    oxygen saturation, fraction of inspired oxygen, and respiratory rate. This simple 
    bedside calculation enables healthcare providers to make evidence-based decisions 
    about respiratory support escalation.
    
    Development and Validation History:
    
    Original Development (2016):
    The ROX Index was initially developed by Roca et al. in a study of pneumonia 
    patients with hypoxemic respiratory failure receiving HFNC therapy. The original 
    validation demonstrated strong predictive capability for HFNC success versus failure.
    
    Expanded Validation (2019):
    Subsequent validation in a larger, more diverse patient population confirmed the 
    ROX Index's utility across various etiologies of acute hypoxemic respiratory 
    failure, establishing standardized cutoff values and time-specific thresholds.
    
    Meta-Analysis Evidence (2022):
    A systematic review and meta-analysis of 9 studies involving 1,933 patients 
    provided robust evidence for the ROX Index's performance characteristics, 
    demonstrating pooled sensitivity of 67% and specificity of 72% for predicting 
    HFNC failure.
    
    Formula and Calculation Methodology:
    
    ROX Index = (SpO2/FiO2 × 100) / Respiratory Rate
    
    Where:
    - SpO2: Pulse oximetry oxygen saturation (percentage)
    - FiO2: Fraction of inspired oxygen delivered by HFNC (0.21-1.0)
    - Respiratory Rate: Current spontaneous breathing frequency (breaths/min)
    
    The calculation provides a dimensionless index where higher values indicate 
    better respiratory function and lower risk of HFNC failure.
    
    Clinical Assessment Protocol and Timing:
    
    Optimal Measurement Timing:
    The ROX Index should be calculated at specific intervals after HFNC initiation 
    to maximize predictive accuracy:
    
    2-Hour Assessment:
    - Cutoff: 2.85 (98-99% specificity for HFNC failure)
    - Purpose: Early identification of high-risk patients
    - Clinical utility: Allows rapid recognition of poor HFNC response
    
    6-Hour Assessment:
    - Cutoff: 3.47 (98-99% specificity for HFNC failure)
    - Purpose: Intermediate assessment of treatment response
    - Clinical utility: Confirms early predictions and guides ongoing management
    
    12-Hour Assessment and Beyond:
    - Cutoff: 4.88 (optimal sensitivity and specificity balance)
    - Purpose: Definitive assessment of HFNC success probability
    - Clinical utility: Most reliable timepoint for long-term outcome prediction
    
    Serial Measurement Strategy:
    Serial ROX Index calculations provide enhanced predictive value compared to 
    single measurements, allowing assessment of treatment response trends and 
    dynamic clinical changes.
    
    Risk Stratification Framework and Clinical Management:
    
    High Risk for HFNC Failure (ROX <3.85):
    
    Clinical Significance:
    - Poor response to HFNC therapy with high likelihood of treatment failure
    - Significant risk for requiring intubation and invasive mechanical ventilation
    - Associated with prolonged ICU stay and increased morbidity if intubation delayed
    
    Immediate Management Actions:
    - Reassess and optimize HFNC settings (flow rate, FiO2, humidity, temperature)
    - Prepare for early intubation with experienced personnel and appropriate equipment
    - Consider alternative non-invasive respiratory support (CPAP, BiPAP, helmet ventilation)
    - Address reversible causes of respiratory failure (bronchospasm, volume overload, infection)
    - Implement close monitoring with continuous pulse oximetry and frequent vital signs
    
    Clinical Decision-Making:
    - Never delay intubation when clinical signs indicate impending respiratory decompensation
    - Consider patient factors including comorbidities, functional status, and goals of care
    - Ensure availability of experienced personnel for emergent airway management
    - Prepare post-intubation ventilator settings and sedation protocols
    
    Indeterminate Risk (ROX 3.85-4.87):
    
    Clinical Significance:
    - Uncertain prognosis requiring close monitoring and optimization
    - Potential for either HFNC success or failure depending on clinical trajectory
    - Critical window for intervention and treatment optimization
    
    Management Strategy:
    - Optimize HFNC therapy with maximum tolerated flow rates and appropriate FiO2
    - Aggressive treatment of underlying respiratory pathology and precipitating factors
    - Serial ROX Index measurements every 1-2 hours to assess treatment response trends
    - Consider adjunctive therapies (prone positioning, recruitment maneuvers, bronchodilators)
    - Maintain high level of clinical vigilance for signs of deterioration
    
    Monitoring Protocol:
    - Continuous assessment of work of breathing, mental status, and hemodynamic stability
    - Regular evaluation of patient comfort and tolerance of HFNC therapy
    - Consider additional diagnostic evaluation if underlying etiology unclear
    - Prepare for potential escalation while continuing optimization efforts
    
    Lower Risk for Intubation (ROX ≥4.88):
    
    Clinical Significance:
    - Good response to HFNC therapy with low probability of treatment failure
    - Excellent prognosis for avoiding invasive mechanical ventilation
    - Opportunity for continued respiratory support optimization and eventual weaning
    
    Continued Management:
    - Continue current HFNC therapy with standard monitoring protocols
    - Consider gradual weaning of FiO2 while maintaining target oxygen saturation (≥92%)
    - Plan for step-down to conventional oxygen therapy when clinically appropriate
    - Continue treatment of underlying respiratory pathology with routine follow-up
    
    De-escalation Planning:
    - Monitor for sustained improvement over 6-12 hours before initiating weaning
    - Gradual reduction in oxygen requirements with maintenance of adequate saturation
    - Consider transition to conventional nasal cannula or face mask when stable
    - Plan for discharge or transfer to lower acuity care setting when appropriate
    
    Special Population Considerations and Validation:
    
    COVID-19 Pneumonia:
    The ROX Index has been specifically validated in COVID-19 patients with acute 
    hypoxemic respiratory failure, demonstrating similar predictive performance 
    and clinical utility. Special considerations include higher baseline oxygen 
    requirements and potential for rapid clinical deterioration.
    
    Immunocompromised Patients:
    Performance may be reduced in immunocompromised populations, with ROX >4.88 
    potentially having lower predictive ability. Enhanced clinical monitoring 
    and lower thresholds for escalation may be appropriate.
    
    Post-Extubation Respiratory Failure:
    The ROX Index can be applied to patients developing respiratory failure after 
    planned extubation, though additional factors such as airway edema and 
    secretion management should be considered.
    
    Community-Acquired Pneumonia:
    Original validation population with robust predictive performance. Consider 
    pathogen-specific treatment optimization alongside ROX-guided management.
    
    Advanced Applications and Modifications:
    
    Modified ROX-HR Index:
    A modified version incorporating heart rate has been developed:
    ROX-HR = (ROX Index / Heart Rate) × 100
    
    This modification may provide enhanced early prediction capabilities, particularly 
    for identifying treatment failure within the first few hours of HFNC therapy.
    
    Integration with Other Predictive Tools:
    The ROX Index can be combined with other validated assessment tools:
    - SpO2/FiO2 ratio as standalone predictor
    - SOFA score for overall organ dysfunction assessment
    - APACHE II score for general ICU mortality prediction
    - Lung ultrasound findings for respiratory pathology assessment
    
    Clinical Decision Support Integration:
    Electronic health record integration with automated ROX Index calculation 
    and clinical decision support alerts can enhance adherence to evidence-based 
    protocols and improve patient outcomes.
    
    Quality Improvement and Implementation Considerations:
    
    Standardization of Practice:
    - Develop institutional protocols for ROX Index measurement timing and interpretation
    - Standardize HFNC equipment and settings across clinical areas
    - Implement training programs for healthcare providers on proper assessment techniques
    - Create documentation templates for consistent recording and trending
    
    Performance Monitoring:
    - Track correlation between ROX Index predictions and actual patient outcomes
    - Monitor adherence to ROX-guided management protocols
    - Evaluate impact on length of stay, intubation rates, and mortality
    - Identify opportunities for continuous quality improvement
    
    Resource Optimization:
    - Use ROX Index to guide appropriate level of care and monitoring intensity
    - Support efficient allocation of ICU beds and respiratory therapy resources
    - Enable earlier identification of patients suitable for step-down care
    - Reduce unnecessary intubations and associated complications
    
    Limitations and Important Clinical Considerations:
    
    Measurement Dependencies:
    - Requires accurate pulse oximetry with adequate perfusion and proper probe placement
    - Depends on stable HFNC settings for meaningful interpretation
    - May be affected by patient movement, poor cooperation, or technical factors
    
    Clinical Context Integration:
    - Should never replace comprehensive clinical assessment and judgment
    - May be less reliable in certain clinical scenarios (shock, severe anemia, carbon monoxide poisoning)
    - Requires interpretation within broader clinical context and patient-specific factors
    
    Validation Limitations:
    - Limited data in pediatric populations and certain comorbid conditions
    - Performance may vary with different HFNC devices and institutional practices
    - Ongoing research needed for optimization of cutoff values and timing
    
    The ROX Index represents a valuable, evidence-based tool for predicting HFNC 
    outcomes and guiding respiratory support decisions in critically ill patients 
    with acute hypoxemic respiratory failure, supporting optimal patient care and 
    resource utilization in critical care settings.
    
    Args:
        request: ROX Index calculation parameters including SpO2, FiO2, and respiratory rate
        
    Returns:
        RoxIndexResponse: ROX Index value with comprehensive risk assessment and clinical management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("rox_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ROX Index for HFNC failure prediction",
                    "details": {"parameters": parameters}
                }
            )
        
        return RoxIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ROX Index calculation",
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
                "message": "Internal error in ROX Index calculation",
                "details": {"error": str(e)}
            }
        )