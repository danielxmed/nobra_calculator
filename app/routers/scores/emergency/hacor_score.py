"""
HACOR Score Router

Endpoint for calculating HACOR Score for predicting non-invasive ventilation failure.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.hacor_score import (
    HacorScoreRequest,
    HacorScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hacor_score",
    response_model=HacorScoreResponse,
    summary="Calculate HACOR Score",
    description="Predicts non-invasive ventilation (NIV) failure in hypoxemic patients. HACOR stands for Heart rate, Acidosis, Consciousness, Oxygenation, and Respiratory rate. Best used in critically ill patients with acute hypoxic respiratory failure who require NIV, assessed 60 minutes after initiating NIV.",
    response_description="The calculated hacor score with interpretation",
    operation_id="hacor_score"
)
async def calculate_hacor_score(request: HacorScoreRequest):
    """
    Calculates HACOR Score for Predicting Non-Invasive Ventilation Failure
    
    The HACOR Score is a validated clinical prediction tool that assesses the risk 
    of non-invasive ventilation (NIV) failure in hypoxemic patients. HACOR stands 
    for Heart rate, Acidosis, Consciousness, Oxygenation, and Respiratory rate. 
    This evidence-based tool enables clinicians to make informed decisions about 
    respiratory support management and the timing of potential intubation.
    
    **Clinical Background**:
    Non-invasive ventilation has emerged as a cornerstone therapy for patients with 
    acute hypoxemic respiratory failure, offering the potential to avoid intubation 
    and its associated complications. However, NIV failure occurs in approximately 
    40-50% of patients and is associated with significantly increased mortality, 
    particularly when intubation is delayed. Early identification of patients at 
    high risk for NIV failure is crucial for optimizing clinical outcomes and 
    resource allocation in intensive care settings.
    
    **Development and Validation**:
    The HACOR score was derived from a prospective cohort study of 449 hypoxemic 
    patients receiving NIV and subsequently validated in 358 additional patients 
    across multiple centers. The score demonstrated excellent discriminative ability 
    with an area under the receiver operating characteristic curve (AUC) of 0.88-0.90 
    across different validation cohorts. The predictive accuracy is optimal when the 
    score is assessed 60 minutes after NIV initiation.
    
    **Five Key Clinical Parameters**:
    
    **1. Heart Rate (H)**:
    - **Clinical Rationale**: Tachycardia may indicate increased metabolic demands, 
      hemodynamic instability, respiratory distress, or inadequate respiratory support
    - **Physiologic Basis**: Elevated heart rate often reflects compensatory mechanisms 
      for respiratory or circulatory compromise
    - **Scoring Criteria**:
      - ≤120 beats/min: 0 points (normal to mild tachycardia)
      - ≥121 beats/min: 1 point (significant tachycardia)
    - **Clinical Assessment**: Measured during NIV support, typically at 60 minutes post-initiation
    
    **2. Acidosis (A) - Arterial pH**:
    - **Clinical Rationale**: Acidosis reflects inadequate ventilation, metabolic 
      derangements, or both, and serves as a strong predictor of respiratory failure
    - **Physiologic Basis**: Progressive acidosis indicates worsening respiratory or 
      metabolic failure despite NIV support
    - **Scoring Criteria**:
      - ≥7.35: 0 points (normal to mild alkalosis)
      - 7.30-7.34: 2 points (mild acidosis)
      - 7.25-7.29: 3 points (moderate acidosis)
      - <7.25: 4 points (severe acidosis)
    - **Clinical Assessment**: Arterial blood gas analysis during NIV support
    
    **3. Consciousness (C) - Glasgow Coma Scale**:
    - **Clinical Rationale**: Altered consciousness may indicate hypercapnia, hypoxemia, 
      or underlying neurological compromise that affects respiratory drive and NIV tolerance
    - **Physiologic Basis**: Decreased consciousness compromises patient cooperation 
      with NIV and may indicate advanced respiratory failure
    - **Scoring Criteria**:
      - 15: 0 points (normal consciousness, full cooperation)
      - 13-14: 2 points (mild alteration, some confusion)
      - 11-12: 5 points (moderate alteration, limited cooperation)
      - ≤10: 10 points (severe alteration, poor NIV tolerance)
    - **Clinical Assessment**: Standard Glasgow Coma Scale evaluation during NIV
    
    **4. Oxygenation (O) - PaO₂/FiO₂ Ratio**:
    - **Clinical Rationale**: The PaO₂/FiO₂ ratio reflects the severity of oxygenation 
      impairment and acute lung injury, with lower ratios indicating more severe disease
    - **Physiologic Basis**: Represents the efficiency of pulmonary gas exchange and 
      the severity of underlying respiratory pathology
    - **Scoring Criteria**:
      - ≥201 mmHg: 0 points (mild oxygenation impairment)
      - 176-200 mmHg: 2 points (moderate oxygenation impairment)
      - 151-175 mmHg: 3 points (moderate-severe impairment)
      - 126-150 mmHg: 4 points (severe oxygenation impairment)
      - 101-125 mmHg: 5 points (very severe impairment)
      - ≤100 mmHg: 6 points (critical oxygenation impairment)
    - **Clinical Assessment**: Arterial PaO₂ divided by fraction of inspired oxygen (FiO₂)
    
    **5. Respiratory Rate (R)**:
    - **Clinical Rationale**: Tachypnea may indicate increased work of breathing, 
      inadequate ventilatory support, or impending respiratory muscle fatigue
    - **Physiologic Basis**: Elevated respiratory rate often reflects respiratory 
      distress and compensatory mechanisms for inadequate gas exchange
    - **Scoring Criteria**:
      - ≤30 breaths/min: 0 points (normal to mild tachypnea)
      - 31-35 breaths/min: 1 point (moderate tachypnea)
      - 36-40 breaths/min: 2 points (severe tachypnea)
      - 41-45 breaths/min: 3 points (very severe tachypnea)
      - ≥46 breaths/min: 4 points (extreme tachypnea, respiratory distress)
    - **Clinical Assessment**: Respiratory rate measurement during NIV support
    
    **Risk Stratification and Clinical Management**:
    
    **Low Risk (Score ≤5)**:
    - **NIV Failure Probability**: Less than 20%
    - **Clinical Interpretation**: Good prognosis with current NIV support
    - **Management Approach**:
      - Continue NIV with standard monitoring protocols
      - Routine optimization of NIV settings for patient comfort and synchrony
      - Standard intensive care monitoring with regular assessment of gas exchange
      - Periodic reassessment of HACOR score at 12, 24, and 48 hours
      - Monitor for clinical deterioration including worsening oxygenation or increased work of breathing
      - Patient and family education about NIV compliance and comfort measures
    - **Follow-up**: Standard respiratory care protocols with routine clinical evaluation
    - **Resource Allocation**: Standard ICU-level monitoring and care
    
    **High Risk (Score >5)**:
    - **NIV Failure Probability**: Greater than 50%
    - **Clinical Interpretation**: Significant risk of NIV failure requiring escalation
    - **Management Approach**:
      - Consider early intubation within 12 hours to reduce hospital mortality
      - Intensive monitoring with immediate preparation for mechanical ventilation
      - Ensure immediate availability of experienced personnel and intubation equipment
      - ICU or high-dependency unit level care if not already provided
      - Optimize NIV settings (pressure support, PEEP, FiO₂) while preparing for potential intubation
      - Close monitoring for signs of respiratory fatigue, worsening hypoxemia, or hemodynamic compromise
      - Consider cardiothoracic or critical care consultation for complex cases
      - Initiate discussions with patient and family about escalation of care
    - **Evidence-Based Outcome**: Early intubation in high-risk patients associated with improved survival
    - **Resource Allocation**: High-intensity monitoring with dedicated nursing and respiratory therapy support
    
    **Clinical Decision-Making Applications**:
    
    **Optimal Timing Assessment**:
    - **Primary Assessment**: 60 minutes after NIV initiation (most predictive)
    - **Serial Assessments**: Reassessment at 12, 24, and 48 hours for trend analysis
    - **Dynamic Monitoring**: Continuous evaluation as patient condition evolves
    - **Threshold for Action**: Score >5 triggers consideration for early intubation
    
    **Patient Population and Indications**:
    - **Primary Indication**: Critically ill patients with acute hypoxic respiratory failure requiring NIV
    - **Validated Conditions**: Pneumonia, acute respiratory distress syndrome (ARDS), 
      COPD exacerbations, cardiogenic pulmonary edema
    - **Clinical Settings**: Intensive care units, emergency departments, respiratory care units
    - **Exclusion Criteria**: Patients with contraindications to NIV or those requiring immediate intubation
    
    **Quality Improvement and Standardization**:
    - **Decision Support**: Provides objective, standardized criteria for respiratory management decisions
    - **Resource Optimization**: Guides appropriate allocation of monitoring intensity and specialized care
    - **Clinical Protocols**: Supports development of evidence-based NIV failure prediction pathways
    - **Provider Education**: Standardizes approach to NIV management across healthcare teams
    - **Outcome Measurement**: Enables tracking of prediction accuracy and clinical outcomes
    
    **Research Foundation and Validation**:
    The HACOR score represents a significant advance in evidence-based respiratory care, 
    derived from rigorous prospective validation in over 800 patients across multiple 
    centers. The score demonstrates consistent accuracy across diverse patient populations 
    and clinical settings, with validation studies confirming its superior performance 
    compared to clinical judgment alone. Multiple independent validation studies have 
    confirmed the score's reliability and clinical utility.
    
    **Advantages of Objective Risk Assessment**:
    - **Evidence-Based**: Derived from comprehensive prospective clinical validation
    - **Objective Criteria**: Uses readily available, quantifiable physiological parameters
    - **Practical Implementation**: Simple bedside calculation with immediate results
    - **Superior Performance**: Demonstrates excellent discriminative ability (AUC 0.88-0.90)
    - **Actionable Results**: Provides clear risk stratification for clinical decision-making
    - **Standardized Approach**: Promotes consistent NIV management across providers and institutions
    
    **Important Clinical Considerations and Limitations**:
    - **Optimal Assessment Timing**: Score is most predictive when evaluated 60 minutes after NIV initiation
    - **Dynamic Patient Condition**: Patient status may change rapidly, requiring frequent reassessment
    - **Clinical Context Integration**: Score should complement comprehensive patient evaluation and clinical judgment
    - **Institutional Factors**: Consider local expertise, resources, and established protocols
    - **Patient Preferences**: Incorporate advance directives and goals of care discussions
    - **Technical Factors**: Requires accurate measurement and assessment of all clinical parameters
    - **Population Limitations**: Validated primarily in specific ICU populations with defined conditions
    - **Equipment Considerations**: Does not account for NIV device quality, interface fit, or patient tolerance
    
    **Educational and Training Applications**:
    The HACOR score provides an excellent framework for teaching evidence-based 
    respiratory care decision-making. It reinforces the importance of systematic 
    clinical assessment, objective risk stratification, and timely intervention in 
    respiratory failure management. The score helps clinicians develop structured 
    approaches to NIV management while emphasizing the critical relationship between 
    early recognition of failure risk and improved patient outcomes.
    
    **Future Directions and Research**:
    Ongoing research continues to refine the application of the HACOR score across 
    different patient populations and clinical settings. Areas of active investigation 
    include integration with other biomarkers, validation in pediatric populations, 
    application to post-extubation respiratory failure, and development of automated 
    scoring systems integrated with electronic health records.
    
    This calculator enables clinicians to make informed, evidence-based decisions 
    about respiratory support strategies, optimize healthcare resource utilization, 
    and improve patient outcomes through appropriate timing of respiratory interventions 
    and escalation of care when indicated.
    
    Args:
        request: HACOR Score parameters including heart rate, pH, GCS, PaO₂/FiO₂ ratio, 
                and respiratory rate
        
    Returns:
        HacorScoreResponse: NIV failure risk assessment with comprehensive clinical 
                          interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hacor_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HACOR Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return HacorScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HACOR Score Calculator",
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