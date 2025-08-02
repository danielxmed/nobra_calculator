"""
ROSE (Risk Stratification of Syncope in the Emergency Department) Rule Router

Endpoint for ROSE rule syncope risk stratification.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.rose_rule import (
    RoseRuleRequest,
    RoseRuleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/rose_rule",
    response_model=RoseRuleResponse,
    summary="ROSE (Risk Stratification of Syncope in the Emergency Department) Rule",
    description="Applies the validated ROSE rule to predict 1-month serious outcome or death in emergency department "
                "patients presenting with syncope. This evidence-based clinical decision tool evaluates 7 readily "
                "available criteria: BNP ≥300 pg/ml, bradycardia ≤50 bpm, positive fecal occult blood, anemia "
                "(hemoglobin ≤90 g/l), chest pain with syncope, Q wave on ECG (not lead III), and oxygen saturation "
                "≤94% on room air. ANY positive criterion indicates HIGH RISK requiring strong consideration for "
                "hospital admission and further workup. The rule demonstrates 87.2% sensitivity and 98.5% negative "
                "predictive value for serious outcomes. Essential for emergency physicians to distinguish high-risk "
                "patients requiring hospitalization from those who can be safely discharged with appropriate follow-up. "
                "Helps optimize resource utilization while maintaining patient safety in syncope evaluation.",
    response_description="ROSE rule risk assessment with clinical interpretation and evidence-based disposition recommendations",
    operation_id="rose_rule"
)
async def calculate_rose_rule(request: RoseRuleRequest):
    """
    ROSE (Risk Stratification of Syncope in the Emergency Department) Rule Assessment
    
    Applies the validated ROSE rule for evidence-based risk stratification of emergency 
    department patients presenting with syncope. This clinical decision tool helps 
    distinguish patients at high risk for serious outcomes who require hospitalization 
    from those who can be safely discharged with appropriate follow-up.
    
    Clinical Significance and Emergency Department Application:
    Syncope accounts for 1-2% of all emergency department visits and up to 6% of 
    hospital admissions, presenting significant challenges in risk stratification 
    and disposition planning. The ROSE rule addresses the critical need for objective, 
    evidence-based criteria to guide clinical decision-making in this common but 
    potentially serious presentation.
    
    Diagnostic Challenge in Syncope:
    Emergency physicians face the complex task of distinguishing benign vasovagal 
    syncope from potentially life-threatening cardiac, neurologic, or other serious 
    causes. Traditional clinical assessment alone often lacks sufficient sensitivity 
    and specificity for reliable risk stratification, leading to either unnecessary 
    admissions or potentially dangerous discharges.
    
    ROSE Rule Validation and Performance:
    
    Development and Validation:
    The ROSE rule was derived from a prospective observational study of 550 patients 
    and validated in 550 additional patients across multiple emergency departments. 
    The study included adults ≥16 years presenting with syncope defined as transient 
    loss of consciousness with spontaneous recovery.
    
    Primary Outcome Definition:
    Serious outcomes included death, myocardial infarction, arrhythmia requiring 
    intervention, structural heart disease diagnosis, pulmonary embolism, stroke, 
    subarachnoid hemorrhage, significant hemorrhage requiring transfusion, or any 
    condition requiring immediate intervention to prevent death or serious morbidity.
    
    Performance Characteristics:
    - Sensitivity: 87.2% for identifying patients with serious outcomes
    - Specificity: 65.5% for correctly identifying low-risk patients
    - Negative Predictive Value: 98.5% when no criteria are present
    - Positive Predictive Value: 27.9% when any criteria are present
    - Serious outcomes occurred in 7.1-7.3% of study patients
    
    ROSE Rule Criteria and Clinical Significance:
    
    The ROSE rule identifies HIGH RISK patients when ANY of the following are present:
    
    1. B-type Natriuretic Peptide (BNP) ≥300 pg/ml:
       - Strongest single predictor with odds ratio of 7.3
       - Associated with 36% of serious cardiovascular outcomes
       - Accounts for 89% of deaths in the validation study
       - Reflects cardiac stress, volume overload, or heart failure
       - Requires point-of-care testing capability
    
    2. Bradycardia ≤50 bpm in ED or Pre-hospital:
       - May indicate sick sinus syndrome or conduction abnormalities
       - Includes documentation by emergency medical services
       - Associated with increased risk of cardiac events and arrhythmias
       - May require pacemaker evaluation or electrophysiology consultation
    
    3. Positive Fecal Occult Blood Test:
       - Highest odds ratio (13.2) among all ROSE criteria
       - Indicates potential gastrointestinal bleeding contributing to syncope
       - Performed when clinical suspicion for GI bleeding exists
       - May reveal occult bleeding causing anemia and hypotension
    
    4. Anemia (Hemoglobin ≤90 g/l or ≤9.0 g/dl):
       - Corresponds to WHO definition of severe anemia
       - May contribute to decreased oxygen delivery and cardiac stress
       - Could indicate acute bleeding, chronic disease, or nutritional deficiency
       - Associated with increased mortality and cardiovascular events
    
    5. Chest Pain Associated with Syncope:
       - Suggests potential cardiac etiology requiring immediate evaluation
       - May indicate acute coronary syndrome, aortic dissection, or pulmonary embolism
       - Temporal association with syncope episode is crucial
       - Warrants comprehensive cardiac assessment and monitoring
    
    6. Q Wave on ECG (not in lead III):
       - Indicates prior myocardial infarction or structural heart disease
       - Lead III Q waves excluded due to potential positional artifacts
       - Suggests underlying coronary artery disease and increased cardiac risk
       - Associated with higher likelihood of cardiac arrhythmias and events
    
    7. Oxygen Saturation ≤94% on Room Air:
       - May indicate pulmonary embolism, heart failure, or other cardiopulmonary causes
       - Must be measured on room air without supplemental oxygen
       - Reflects impaired gas exchange or compromised cardiac output
       - Associated with serious underlying pathology requiring urgent evaluation
    
    Clinical Applications and Decision-Making Framework:
    
    High-Risk Patient Management (Any Positive Criteria):
    
    Immediate Assessment and Stabilization:
    - Continuous cardiac monitoring in emergency department setting
    - Intravenous access and hemodynamic monitoring
    - Serial cardiac biomarkers (troponin, CK-MB) every 6-8 hours
    - 12-lead ECG with rhythm strips and comparison to prior ECGs
    - Chest X-ray and additional imaging based on clinical presentation
    
    Targeted Evaluation Based on Positive Criteria:
    - Elevated BNP: Echocardiography, heart failure workup, cardiology consultation
    - Bradycardia: Extended rhythm monitoring, electrophysiology evaluation
    - Occult GI bleeding: Gastroenterology consultation, endoscopy consideration
    - Severe anemia: Complete blood count with differential, iron studies, hematology input
    - Chest pain: Acute coronary syndrome protocol, potential cardiac catheterization
    - Q waves on ECG: Echocardiography, stress testing, cardiology evaluation
    - Hypoxemia: CT pulmonary angiogram, arterial blood gas, pulmonary consultation
    
    Admission and Monitoring Recommendations:
    - Hospital admission with telemetry monitoring capability
    - Multidisciplinary consultation based on specific abnormalities identified
    - Medication reconciliation and optimization of cardiovascular medications
    - Risk stratification for additional procedures or interventions
    - Clear documentation of rationale for admission and treatment plan
    
    Low-Risk Patient Management (No Positive Criteria):
    
    Discharge Planning and Follow-up:
    - Ensure complete hemodynamic stability and symptom resolution
    - Arrange outpatient cardiology evaluation within 1-2 weeks
    - Primary care physician follow-up within 24-48 hours
    - Comprehensive patient education about warning signs and return precautions
    - Consider outpatient cardiac event monitoring if clinically indicated
    
    Patient Education and Safety Instructions:
    - Return immediately for recurrent syncope, chest pain, dyspnea, or palpitations
    - Avoid driving until cleared by cardiology or primary care physician
    - Medication review to identify potential contributors to syncope episodes
    - Lifestyle modifications including adequate hydration and gradual position changes
    - Follow-up compliance and importance of scheduled appointments
    
    Outpatient Evaluation Considerations:
    - Holter monitor or event recorder for rhythm assessment
    - Echocardiography if not performed during emergency department visit
    - Exercise stress testing for patients with suspected coronary artery disease
    - Tilt table testing for recurrent unexplained syncope in appropriate candidates
    - Medication adjustment based on findings and follow-up assessment
    
    Integration with Clinical Practice:
    
    Quality Assurance and Implementation:
    - Staff training on proper rule application and interpretation
    - Documentation standards for all ROSE criteria assessment
    - Regular monitoring of rule adherence and patient outcomes
    - Integration with electronic health record clinical decision support
    - Validation of performance in local patient population and healthcare system
    
    Clinical Judgment and Rule Limitations:
    - Use ROSE rule as adjunct to, not replacement for, comprehensive clinical assessment
    - Consider other validated syncope risk stratification tools when appropriate
    - Account for patient-specific factors, comorbidities, and social circumstances
    - Recognize that rule requires BNP testing which may not be universally available
    - Maintain flexibility for clinical concerns beyond rule criteria
    
    Resource Optimization and Patient Safety:
    - Balance patient safety with appropriate resource utilization
    - Reduce unnecessary admissions while maintaining sensitivity for serious outcomes
    - Improve emergency department flow and reduce overcrowding
    - Provide structured approach for resident and attending physician education
    - Support evidence-based decision-making in high-pressure clinical environment
    
    Continuous Quality Improvement:
    - Monitor outcomes for both admitted and discharged patients
    - Track adherence to rule recommendations and clinical outcomes
    - Identify opportunities for process improvement and education
    - Evaluate rule performance against institutional metrics and benchmarks
    - Adapt implementation based on local factors and patient population characteristics
    
    The ROSE rule represents a valuable evidence-based tool for emergency physicians 
    managing syncope patients, providing objective criteria for risk stratification 
    while supporting clinical decision-making and optimizing patient care outcomes.
    
    Args:
        request: ROSE rule assessment parameters for syncope risk stratification
        
    Returns:
        RoseRuleResponse: Risk assessment with comprehensive clinical guidance and disposition recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("rose_rule", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error applying ROSE rule for syncope risk stratification",
                    "details": {"parameters": parameters}
                }
            )
        
        return RoseRuleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ROSE rule assessment",
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
                "message": "Internal error in ROSE rule syncope risk assessment",
                "details": {"error": str(e)}
            }
        )