"""
ROX Index for Intubation after HFNC Models

Request and response models for ROX Index calculation.

References (Vancouver style):
1. Roca O, Messika J, Caralt B, García-de-Acilu M, Sztrymf B, Ricard JD, Masclans JR. 
   Predicting success of high-flow nasal cannula in pneumonia patients with hypoxemic 
   respiratory failure: The utility of the ROX index. J Crit Care. 2016 Oct;35:200-5. 
   doi: 10.1016/j.jcrc.2016.05.022.
2. Roca O, Caralt B, Messika J, Samper M, Sztrymf B, Hernández G, García-de-Acilu M, 
   Frat JP, Masclans JR, Ricard JD. An Index Combining Respiratory Rate and Oxygenation 
   to Predict Outcome of Nasal High-Flow Therapy. Am J Respir Crit Care Med. 
   2019 Jun 1;199(11):1368-1376. doi: 10.1164/rccm.201803-0589OC.
3. Suliman LA, Abdelgawad TT, Farrag NS, Abdelwahab HW. Validity of ROX index in 
   prediction of risk of intubation in patients with COVID-19 pneumonia. Adv Respir Med. 
   2021;89(1):1-6. doi: 10.5603/ARM.a2020.0176.

The ROX Index is a validated clinical tool that predicts high-flow nasal cannula (HFNC) 
failure and need for intubation in patients with acute hypoxemic respiratory failure. 
It combines three readily available parameters to provide early and reliable prediction 
of treatment outcomes, helping clinicians make timely decisions about respiratory support 
escalation and avoiding delayed intubation with its associated complications.
"""

from pydantic import BaseModel, Field


class RoxIndexRequest(BaseModel):
    """
    Request model for ROX Index calculation for HFNC failure prediction
    
    The ROX Index is calculated as the ratio of SpO2/FiO2 to respiratory rate,
    providing a simple bedside tool for predicting high-flow nasal cannula success 
    or failure in patients with acute hypoxemic respiratory failure (AHRF).
    
    Clinical Background and Development:
    The ROX Index was originally developed and validated by Roca et al. in 2016 
    and subsequently refined in 2019. It addresses the critical clinical need for 
    early identification of HFNC treatment failure to prevent delayed intubation, 
    which is associated with prolonged duration of invasive mechanical ventilation 
    and worse clinical outcomes.
    
    Formula and Calculation:
    ROX Index = (SpO2/FiO2 × 100) / Respiratory Rate
    
    Where:
    - SpO2 is oxygen saturation measured by pulse oximetry (%)
    - FiO2 is fraction of inspired oxygen delivered by HFNC (0.21-1.0)
    - Respiratory Rate is current breathing frequency (breaths/min)
    
    Clinical Application and Timing:
    The ROX Index should be measured at specific time intervals after HFNC initiation:
    - 2 hours: Early assessment with cutoff of 2.85 (98-99% specificity)
    - 6 hours: Intermediate assessment with cutoff of 3.47 (98-99% specificity)
    - 12 hours: Standard assessment with cutoff of 3.85 (98-99% specificity)
    - 12+ hours: Optimal assessment with cutoff of 4.88 for continued success
    
    Interpretation Thresholds and Clinical Significance:
    
    High Risk for HFNC Failure (ROX <3.85):
    - Indicates poor response to HFNC therapy
    - High likelihood of requiring intubation and invasive mechanical ventilation
    - Prepare for early intubation and alternative respiratory support
    - Consider optimization of HFNC settings and treatment of underlying pathology
    - Monitor closely for signs of respiratory decompensation
    
    Indeterminate Risk (ROX 3.85-4.87):
    - Uncertain prognosis requiring close monitoring
    - Reassess ROX Index within 1-2 hours for trend assessment
    - Optimize HFNC settings and treat underlying respiratory condition
    - Maintain high vigilance for clinical deterioration
    - Be prepared for escalation to invasive ventilation if trending downward
    
    Lower Risk for Intubation (ROX ≥4.88):
    - Good response to HFNC therapy with low intubation risk
    - Continue current HFNC therapy with consideration for FiO2 weaning
    - Monitor for continued improvement and plan de-escalation
    - Maintain standard monitoring protocols
    - Excellent prognosis for avoiding invasive mechanical ventilation
    
    Performance Characteristics and Validation:
    
    Meta-Analysis Results (9 studies, 1,933 patients):
    - Pooled sensitivity: 67% (95% CI: 57-76%)
    - Pooled specificity: 72% (95% CI: 65-78%)
    - Prediction accuracy improves over time: AUC 0.679 at 2h, 0.703 at 6h, 0.759 at 12h
    - Positive predictive value for HFNC success: >80% when ROX ≥4.88 at 12-20 hours
    
    Optimal Confidence Interval: 4.2-5.4 for HFNC outcome prediction
    
    Patient Populations and Special Considerations:
    
    Validated Populations:
    - Acute hypoxemic respiratory failure from various etiologies
    - Community-acquired pneumonia and hospital-acquired pneumonia
    - COVID-19 pneumonia and viral respiratory infections
    - Acute respiratory distress syndrome (ARDS)
    - Post-extubation respiratory failure
    
    Special Population Considerations:
    - Immunocompromised patients: ROX >4.88 may have reduced predictive ability
    - Pediatric populations: Limited validation data available
    - Chronic respiratory disease: Consider baseline respiratory function
    - Neuromuscular disorders: May affect respiratory rate interpretation
    
    Clinical Decision-Making Framework:
    
    Assessment Protocol:
    1. Ensure accurate measurement of all three parameters on current HFNC settings
    2. Calculate ROX Index using standardized formula
    3. Interpret results based on time from HFNC initiation and clinical context
    4. Consider serial measurements for trend assessment
    5. Integrate with overall clinical assessment and other prognostic markers
    
    Management Based on ROX Index Results:
    
    High Risk (ROX <3.85):
    - Immediate reassessment of HFNC settings and patient positioning
    - Consider increasing flow rate, FiO2, or positive end-expiratory pressure
    - Prepare for early intubation with appropriate personnel and equipment
    - Address reversible causes of respiratory failure
    - Avoid delay in intubation if clinical deterioration evident
    
    Indeterminate Risk (ROX 3.85-4.87):
    - Optimize HFNC therapy with highest tolerated flow rates
    - Aggressive treatment of underlying respiratory pathology
    - Serial ROX measurements every 1-2 hours for trend monitoring
    - Consider prone positioning or recruitment maneuvers if appropriate
    - Maintain low threshold for escalation if ROX trends downward
    
    Lower Risk (ROX ≥4.88):
    - Continue current HFNC therapy with standard monitoring
    - Consider gradual weaning of FiO2 while maintaining adequate oxygenation
    - Plan for step-down to conventional oxygen therapy when appropriate
    - Continue treatment of underlying condition with routine follow-up
    
    Important Clinical Considerations and Limitations:
    
    Measurement Accuracy:
    - Ensure SpO2 measurement reflects true oxygenation (adequate perfusion, proper probe placement)
    - Verify FiO2 setting matches actual delivered concentration
    - Confirm respiratory rate count over appropriate time period (typically 1 minute)
    - Account for patient cooperation and measurement conditions
    
    Clinical Integration:
    - Never delay intubation when clinical signs indicate respiratory decompensation
    - Use ROX Index as adjunct to, not replacement for, comprehensive clinical assessment
    - Consider other prognostic markers and patient-specific factors
    - Account for goals of care and patient preferences in decision-making
    
    Technical Limitations:
    - Limited validation in certain patient populations (immunocompromised, pediatric)
    - May be less reliable with significant hemodynamic instability
    - Requires stable HFNC settings for accurate interpretation
    - Performance may vary with different HFNC devices and settings
    
    Quality Assurance:
    - Standardize measurement techniques across healthcare providers
    - Ensure consistent timing of assessments relative to HFNC initiation
    - Document clinical context and factors affecting interpretation
    - Validate measurements when results seem inconsistent with clinical presentation
    
    Enhanced Prediction Strategies:
    
    Modified ROX-HR Index:
    A modified version incorporates heart rate: ROX-HR = (ROX Index / Heart Rate) × 100
    This modification may provide enhanced early prediction capabilities for treatment failure.
    
    Serial Measurements:
    Trending ROX values over time provides more robust prediction than single measurements:
    - Improving trend: Good prognosis for HFNC success
    - Stable trend: Continue current management with close monitoring
    - Declining trend: Increased risk for HFNC failure requiring escalation
    
    Multi-Parameter Assessment:
    Consider ROX Index alongside other validated predictors:
    - SpO2/FiO2 ratio as standalone predictor
    - Clinical scores for respiratory failure severity
    - Laboratory markers of inflammation and organ dysfunction
    - Radiographic assessment of lung injury severity
    
    Resource Utilization and Healthcare Economics:
    
    Clinical Efficiency:
    - Enables objective risk stratification for respiratory support decisions
    - Supports appropriate resource allocation in intensive care units
    - May reduce unnecessary intubations and associated complications
    - Facilitates earlier discharge planning for low-risk patients
    
    Cost-Effectiveness:
    - Simple calculation requiring no additional equipment or testing
    - May reduce length of stay through optimized respiratory support decisions
    - Supports evidence-based care protocols and clinical guidelines
    - Enhances training and education for respiratory therapy management
    
    The ROX Index represents a valuable, evidence-based tool for predicting HFNC 
    outcomes and guiding respiratory support decisions in critically ill patients 
    with acute hypoxemic respiratory failure.
    
    References (Vancouver style):
    1. Roca O, Messika J, Caralt B, García-de-Acilu M, Sztrymf B, Ricard JD, Masclans JR. 
       Predicting success of high-flow nasal cannula in pneumonia patients with hypoxemic 
       respiratory failure: The utility of the ROX index. J Crit Care. 2016 Oct;35:200-5. 
       doi: 10.1016/j.jcrc.2016.05.022.
    2. Roca O, Caralt B, Messika J, Samper M, Sztrymf B, Hernández G, García-de-Acilu M, 
       Frat JP, Masclans JR, Ricard JD. An Index Combining Respiratory Rate and Oxygenation 
       to Predict Outcome of Nasal High-Flow Therapy. Am J Respir Crit Care Med. 
       2019 Jun 1;199(11):1368-1376. doi: 10.1164/rccm.201803-0589OC.
    3. Suliman LA, Abdelgawad TT, Farrag NS, Abdelwahab HW. Validity of ROX index in 
       prediction of risk of intubation in patients with COVID-19 pneumonia. Adv Respir Med. 
       2021;89(1):1-6. doi: 10.5603/ARM.a2020.0176.
    """
    
    spo2: int = Field(
        ...,
        ge=70,
        le=100,
        description="Pulse oximetry oxygen saturation measured on current HFNC settings. "
                   "Should reflect stable reading over 1-2 minutes with adequate perfusion and proper probe placement. "
                   "Range: 70-100% (values <85% suggest severe hypoxemia requiring urgent intervention)",
        example=92
    )
    
    fio2: float = Field(
        ...,
        ge=0.21,
        le=1.0,
        description="Fraction of inspired oxygen being delivered by HFNC system. "
                   "Enter as decimal fraction (0.21-1.0) where 0.21 = 21% oxygen (room air) and 1.0 = 100% oxygen. "
                   "Verify setting matches actual delivered concentration on HFNC device. "
                   "Common values: 0.21 (room air), 0.40 (40%), 0.60 (60%), 0.80 (80%), 1.0 (100%)",
        example=0.60
    )
    
    respiratory_rate: int = Field(
        ...,
        ge=10,
        le=50,
        description="Current respiratory rate in breaths per minute, counted over full 60-second period. "
                   "Should represent spontaneous breathing rate on current HFNC support. "
                   "Range: 10-50 breaths/min (normal: 12-20, tachypnea >20, severe tachypnea >30)",
        example=24
    )
    
    class Config:
        schema_extra = {
            "example": {
                "spo2": 92,
                "fio2": 0.60,
                "respiratory_rate": 24
            }
        }


class RoxIndexResponse(BaseModel):
    """
    Response model for ROX Index calculation for HFNC failure prediction
    
    The ROX Index provides evidence-based prediction of high-flow nasal cannula (HFNC) 
    treatment outcomes in patients with acute hypoxemic respiratory failure. Results 
    are categorized into three risk levels to guide clinical decision-making about 
    respiratory support escalation and timing of potential intubation.
    
    Risk Categories and Clinical Management:
    
    High Risk for HFNC Failure (ROX <3.85):
    - Immediate Clinical Actions:
      * Reassess and optimize HFNC settings (flow rate, FiO2, temperature)
      * Prepare for early intubation with appropriate personnel and equipment
      * Consider alternative respiratory support strategies (NIV, CPAP)
      * Address reversible causes of respiratory failure
      * Monitor closely for signs of respiratory decompensation
    
    - Patient Monitoring:
      * Continuous pulse oximetry and respiratory rate monitoring
      * Frequent reassessment of work of breathing and mental status
      * Serial blood gas analysis if clinically indicated
      * Hemodynamic monitoring for signs of cardiovascular compromise
    
    - Decision-Making Framework:
      * Never delay intubation if clinical deterioration evident
      * Consider patient factors (comorbidities, goals of care)
      * Ensure experienced personnel available for emergent intubation
      * Prepare for post-intubation management and ventilator settings
    
    Indeterminate Risk (ROX 3.85-4.87):
    - Optimization Strategies:
      * Maximize HFNC therapy with highest tolerated flow rates
      * Aggressive treatment of underlying respiratory pathology
      * Consider prone positioning or recruitment maneuvers
      * Optimize patient positioning and comfort measures
    
    - Monitoring Protocol:
      * Serial ROX measurements every 1-2 hours for trend assessment
      * Close clinical monitoring for signs of improvement or deterioration
      * Regular assessment of patient comfort and tolerance
      * Consider additional diagnostic evaluation if indicated
    
    - Escalation Planning:
      * Maintain low threshold for escalation if ROX trends downward
      * Prepare for potential intubation with appropriate resources
      * Consider early consultation with intensivist or pulmonologist
      * Document rationale for continued HFNC therapy versus escalation
    
    Lower Risk for Intubation (ROX ≥4.88):
    - Continued Management:
      * Continue current HFNC therapy with standard monitoring protocols
      * Consider gradual weaning of FiO2 while maintaining adequate oxygenation
      * Plan for step-down to conventional oxygen therapy when appropriate
      * Continue treatment of underlying respiratory pathology
    
    - De-escalation Planning:
      * Monitor for sustained improvement over 6-12 hours before weaning
      * Gradual reduction in FiO2 with target SpO2 ≥92% on lower concentrations
      * Consider transition to conventional nasal cannula or face mask
      * Plan for discharge or transfer to lower acuity unit when stable
    
    - Follow-up Considerations:
      * Regular reassessment to ensure sustained improvement
      * Patient education about respiratory symptoms and follow-up care
      * Consider outpatient pulmonary follow-up if indicated
      * Address underlying conditions contributing to respiratory failure
    
    Timing-Specific Interpretation Guidelines:
    
    Early Assessment (2-6 hours post-HFNC initiation):
    - Higher cutoff values (2.85-3.47) provide excellent specificity (98-99%)
    - Early identification of high-risk patients requiring close monitoring
    - Allow time for HFNC therapy to demonstrate effectiveness
    - Consider patient adaptation period and optimal positioning
    
    Standard Assessment (12+ hours post-HFNC initiation):
    - Standard cutoff value (4.88) provides optimal sensitivity and specificity
    - Most reliable timepoint for definitive outcome prediction
    - Consider accumulated clinical response and overall trajectory
    - Plan definitive management strategy based on sustained response
    
    Serial Measurement Interpretation:
    - Improving ROX trend: Excellent prognosis for HFNC success
    - Stable ROX trend: Continue current management with monitoring
    - Declining ROX trend: High concern for HFNC failure requiring escalation
    - Fluctuating values: Consider measurement accuracy and clinical factors
    
    Integration with Clinical Assessment:
    
    Supporting Clinical Indicators for HFNC Success:
    - Decreased work of breathing and accessory muscle use
    - Improved mental status and patient comfort
    - Stable hemodynamics without vasopressor requirements
    - Radiographic stabilization or improvement
    
    Warning Signs Despite Favorable ROX Index:
    - Persistent altered mental status or agitation
    - Hemodynamic instability or shock
    - Inability to protect airway or handle secretions
    - Patient exhaustion or inability to cooperate with therapy
    
    Documentation and Communication:
    
    Essential Documentation Elements:
    - Exact timing of ROX measurement relative to HFNC initiation
    - HFNC settings at time of measurement (flow rate, FiO2, temperature)
    - Clinical context and factors affecting interpretation
    - Serial ROX values and trends over time
    - Clinical response and overall patient trajectory
    
    Interdisciplinary Communication:
    - Clear communication of ROX results and clinical significance
    - Shared decision-making regarding escalation thresholds
    - Coordination with respiratory therapy for HFNC optimization
    - Early consultation with intensivist when indicated
    
    Quality Assurance and Continuous Improvement:
    
    Measurement Standardization:
    - Consistent timing of assessments across healthcare team
    - Standardized measurement techniques for accuracy
    - Regular calibration of pulse oximetry equipment
    - Documentation of factors affecting measurement reliability
    
    Outcome Tracking:
    - Monitor correlation between ROX predictions and actual outcomes
    - Track adherence to ROX-guided management protocols
    - Identify opportunities for process improvement
    - Evaluate impact on patient outcomes and resource utilization
    
    The ROX Index serves as a valuable objective tool to complement clinical 
    judgment in managing patients with acute hypoxemic respiratory failure on 
    HFNC therapy, supporting evidence-based decisions about respiratory support 
    escalation and optimizing patient outcomes.
    
    Reference: Roca O, et al. Am J Respir Crit Care Med. 2019;199(11):1368-1376.
    """
    
    result: float = Field(
        ...,
        description="Calculated ROX Index value from SpO2/FiO2 ratio divided by respiratory rate. "
                   "Higher values indicate better prognosis and lower risk of HFNC failure. "
                   "Typical range: 1.0-15.0, with values ≥4.88 associated with HFNC success",
        example=6.38
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the ROX Index result",
        example="index"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation of the ROX Index result with specific "
                   "recommendations for patient management, monitoring protocols, and respiratory "
                   "support decisions. Includes risk stratification guidance and next steps for clinical care.",
        example="Lower risk for intubation with good response to HFNC therapy. This ROX index "
                "value (6.38) suggests successful treatment with high-flow nasal cannula and low "
                "likelihood of requiring intubation. This value falls within the optimal confidence "
                "interval (4.2-5.4) for HFNC success prediction. Continue current HFNC therapy and "
                "consider weaning FiO2 as tolerated while maintaining adequate oxygenation."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification category for HFNC failure prediction",
        example="Lower Risk for Intubation"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category and recommended clinical action",
        example="Continue HFNC and wean FiO2"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6.38,
                "unit": "index",
                "interpretation": "Lower risk for intubation with good response to HFNC therapy. This ROX index value (6.38) suggests successful treatment with high-flow nasal cannula and low likelihood of requiring intubation. This value falls within the optimal confidence interval (4.2-5.4) for HFNC success prediction. Continue current HFNC therapy and consider weaning FiO2 as tolerated while maintaining adequate oxygenation. Monitor for continued improvement and plan for further de-escalation of respiratory support.",
                "stage": "Lower Risk for Intubation",
                "stage_description": "Continue HFNC and wean FiO2"
            }
        }