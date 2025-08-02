"""
Quick COVID-19 Severity Index (qCSI) Models

Request and response models for qCSI calculation.

References (Vancouver style):
1. Haimovich AD, Ravindra NG, Stoytchev S, Young HP, Wilson FP, van Dijk D, et al. 
   Development and Validation of the Quick COVID-19 Severity Index: A Prognostic Tool 
   for Early Clinical Decompensation. Ann Emerg Med. 2020 Oct;76(4):442-453. 
   doi: 10.1016/j.annemergmed.2020.07.022.
2. Liao X, Wang B, Kang Y. Novel coronavirus infection during the 2019-2020 epidemic: 
   preparing intensive care units-the experience in Sichuan Province, China. Intensive Care Med. 
   2020 Apr;46(4):357-360. doi: 10.1007/s00134-020-05954-2.
3. Covino M, De Matteis G, Santoro M, Sabia L, Simeoni B, Candelli M, et al. 
   Clinical characteristics and prognostic factors in COVID-19 patients aged ≥80 years. 
   Geriatr Gerontol Int. 2020 Jul;20(7):704-708. doi: 10.1111/ggi.13960.

The Quick COVID-19 Severity Index (qCSI) is a validated prognostic tool developed to predict 
24-hour risk of critical respiratory failure in emergency department patients admitted with 
COVID-19. Created by Haimovich et al. during the early phase of the COVID-19 pandemic, this 
simple bedside assessment tool uses three readily available clinical variables to identify 
patients at risk for respiratory decompensation, enabling early intervention and appropriate 
resource allocation.

Clinical Background and Development:
The qCSI was developed in response to the urgent clinical need for rapid risk stratification 
of COVID-19 patients presenting to emergency departments during the pandemic. The tool was 
derived from a large observational cohort study of 1,792 COVID-19 patients admitted across 
a 9-ED health system, of whom 620 (35%) experienced respiratory failure. The primary outcome 
was respiratory failure within 24 hours of admission, defined as oxygen requirement >10 L/min 
by low-flow device, high-flow device, noninvasive or invasive ventilation, or death.

Clinical Applications:
- Early identification of COVID-19 patients at risk for respiratory deterioration
- Resource allocation and staffing decisions in emergency departments
- Triaging patients for appropriate level of care and monitoring intensity
- Supporting clinical decision-making for COVID-19 management protocols
- Quality improvement initiatives for COVID-19 care pathways
- Research stratification and clinical trial enrollment
- Pandemic preparedness and capacity planning
- ICU admission prediction and bed management

qCSI Score Components:
The qCSI utilizes three simple bedside clinical variables:

1. Respiratory Rate (breaths per minute):
   - Easily measured at bedside without equipment
   - Reflects respiratory distress and metabolic compensation
   - Higher rates indicate increased risk of deterioration
   - Normal range typically 12-20 breaths/min for adults

2. Lowest Oxygen Saturation in First 4 Hours (%):
   - Minimum pulse oximetry reading during initial ED stay
   - Reflects severity of pulmonary involvement
   - Lower saturations indicate higher risk of respiratory failure
   - Should be measured on current oxygen supplementation

3. Oxygen Flow Rate (L/min):
   - Current oxygen requirement at time of assessment
   - Indicates severity of hypoxemia and oxygen dependence
   - Room air = 0 L/min, supplemental oxygen ranges 1-15 L/min
   - Higher flow rates indicate more severe respiratory compromise

Risk Stratification and Clinical Outcomes:
The qCSI stratifies patients into three risk categories for 24-hour respiratory failure:

Low Risk (qCSI ≤3 points):
- <5% risk of critical respiratory failure within 24 hours
- Sensitivity 79% and specificity 78% for respiratory decompensation
- Suitable for standard ward monitoring with routine COVID-19 protocols
- May be candidates for early discharge if other factors permit
- Requires regular monitoring but less intensive resource allocation

Intermediate Risk (qCSI 4-6 points):
- Moderate risk requiring enhanced monitoring and observation
- Consider higher level of care and more frequent assessments
- May benefit from telemetry monitoring and respiratory therapy consultation
- Prepare for potential escalation of care within 24 hours
- Enhanced nursing ratios and increased observation frequency

High Risk (qCSI ≥7 points):
- High risk for critical respiratory failure requiring intensive management
- Consider ICU consultation and advanced respiratory support preparation
- Frequent monitoring with hourly respiratory assessments
- Prepare for high-flow oxygen, noninvasive ventilation, or intubation
- May require immediate escalation to higher level of care

Validation and Performance:
The qCSI demonstrated strong predictive performance in validation studies:
- AUC 0.761 for ICU admission prediction
- Superior performance compared to CURB-65 (AUC 0.629) for ICU prediction
- Good performance for in-hospital mortality prediction
- Consistent results across diverse emergency department settings
- Simple calculation enhances clinical usability and rapid implementation

Clinical Implementation Guidelines:
- Calculate for all COVID-19 patients being admitted from the emergency department
- Use initial vital signs and lowest oxygen saturation in first 4 hours
- Reassess if clinical condition changes significantly
- Integrate with existing COVID-19 protocols and care pathways
- Document score and rationale for level of care decisions
- Train healthcare providers on proper measurement techniques
- Use as part of comprehensive clinical assessment, not in isolation

Important Clinical Considerations:
- Designed specifically for COVID-19 patients in emergency department setting
- Predicts respiratory failure, not overall mortality or length of stay
- Should be used in conjunction with clinical judgment and patient factors
- May have different performance in vaccinated vs. unvaccinated patients
- Consider variant-specific characteristics and local COVID-19 epidemiology
- Results should be interpreted in context of overall clinical condition

Treatment Implications by Risk Level:
Low Risk: Standard ward monitoring, routine COVID-19 protocols, consider discharge planning
Intermediate Risk: Enhanced monitoring, frequent assessments, prepare for escalation
High Risk: Intensive monitoring, ICU consultation, advanced respiratory support preparation

Quality Assurance and Monitoring:
- Regular training on proper vital sign measurement techniques
- Audit compliance with qCSI-triggered interventions and monitoring protocols
- Monitor outcomes and quality metrics for qCSI-stratified patients
- Integrate into electronic health record systems for automated calculation
- Use for performance improvement initiatives and COVID-19 care optimization

The qCSI represents an important advancement in COVID-19 care by providing evidence-based 
risk stratification that enables proactive management and optimal resource utilization, 
ultimately improving patient outcomes through early identification and intervention.
"""

from pydantic import BaseModel, Field


class QcsiRequest(BaseModel):
    """
    Request model for Quick COVID-19 Severity Index (qCSI)
    
    The qCSI provides rapid risk assessment for COVID-19 patients being admitted from the 
    emergency department to predict 24-hour risk of critical respiratory failure. This 
    validated tool uses three simple bedside measurements to stratify patients and guide 
    clinical decision-making for appropriate level of care and monitoring intensity.
    
    Clinical Assessment Guidelines:
    
    1. Respiratory Rate Assessment:
       - Count respirations for a full minute when possible for accuracy
       - Observe natural breathing pattern without patient awareness if possible
       - Document if patient is in distress or using accessory muscles
       - Consider baseline respiratory rate and underlying conditions
       - Normal adult range: 12-20 breaths per minute
    
    2. Oxygen Saturation Monitoring:
       - Record lowest pulse oximetry reading during first 4 hours in ED
       - Use continuous monitoring if available for accurate minimum detection
       - Ensure proper probe placement and adequate perfusion
       - Document if patient is receiving supplemental oxygen during measurement
       - Consider altitude and chronic conditions affecting baseline saturation
    
    3. Oxygen Flow Rate Assessment:
       - Record current oxygen requirement at time of qCSI calculation
       - Use 0 L/min for patients on room air (no supplemental oxygen)
       - Include all forms of oxygen delivery (nasal cannula, face mask, etc.)
       - Document delivery method and patient tolerance
       - Consider weaning trials and oxygen response patterns
    
    Clinical Context and Timing:
    - Calculate for all COVID-19 patients being admitted from emergency department
    - Use measurements from initial emergency department evaluation
    - Reassess if clinical condition changes significantly
    - Document time of assessment and clinical circumstances
    - Consider trend patterns rather than single measurements when possible
    
    Interpretation Framework:
    - Low risk (≤3): Standard ward monitoring with routine protocols
    - Intermediate risk (4-6): Enhanced monitoring and frequent assessments
    - High risk (≥7): Intensive monitoring and preparation for respiratory support
    - Always integrate with clinical judgment and patient-specific factors
    
    Quality Assurance:
    - Verify accuracy of vital sign measurements and oxygen requirements
    - Ensure proper measurement techniques and documentation
    - Document rationale for clinical decisions based on qCSI results
    - Plan appropriate monitoring and escalation protocols based on risk level
    
    References: See module docstring for complete citation list.
    """
    
    respiratory_rate: int = Field(
        ...,
        ge=8,
        le=60,
        description="Respiratory rate in breaths per minute. Count for a full minute when possible for accuracy. Higher rates indicate increased risk of respiratory deterioration in COVID-19 patients.",
        example=22
    )
    
    lowest_oxygen_saturation: int = Field(
        ...,
        ge=50,
        le=100,
        description="Lowest pulse oximetry reading during the initial 4 hours in the emergency department (%). Lower saturations indicate higher risk of respiratory failure within 24 hours.",
        example=94
    )
    
    oxygen_flow_rate: int = Field(
        ...,
        ge=0,
        le=15,
        description="Current oxygen flow rate in liters per minute. Use 0 for room air (no supplemental oxygen). Higher flow rates indicate more severe respiratory compromise and increased risk.",
        example=2
    )
    
    class Config:
        schema_extra = {
            "example": {
                "respiratory_rate": 22,
                "lowest_oxygen_saturation": 94,
                "oxygen_flow_rate": 2
            }
        }


class QcsiResponse(BaseModel):
    """
    Response model for Quick COVID-19 Severity Index (qCSI)
    
    The qCSI score provides critical risk stratification for COVID-19 patients, enabling 
    proactive identification of those at risk for respiratory deterioration within 24 hours. 
    Understanding qCSI results is essential for appropriate resource allocation, monitoring 
    intensity, and timely intervention to prevent clinical decompensation.
    
    Risk Category Interpretation and Clinical Management:
    
    Low Risk (qCSI ≤3 points, <5% respiratory failure risk):
    - Excellent prognosis with minimal risk of 24-hour respiratory deterioration
    - Suitable for standard ward monitoring with routine COVID-19 protocols
    - Regular vital signs monitoring every 4-6 hours with standard nursing care
    - Consider early discharge planning if other clinical factors permit
    - Standard COVID-19 treatment protocols with monitoring for clinical changes
    - Patient education on warning signs and when to seek immediate care
    
    Intermediate Risk (qCSI 4-6 points, moderate respiratory failure risk):
    - Moderate risk requiring enhanced monitoring and observation protocols
    - Consider higher level of care with increased nursing surveillance
    - More frequent vital signs monitoring every 2-4 hours with respiratory focus
    - Enhanced nursing ratios and respiratory therapy consultation
    - Prepare for potential escalation of care within 24-hour period
    - Consider telemetry monitoring for continuous assessment
    
    High Risk (qCSI ≥7 points, high respiratory failure risk):
    - High risk for critical respiratory failure requiring intensive management
    - Immediate consideration for ICU consultation and higher level of care
    - Hourly respiratory assessments with continuous monitoring
    - Prepare for advanced respiratory support including high-flow oxygen, NIV, or intubation
    - Enhanced staffing and immediate access to respiratory support equipment
    - Proactive planning for potential mechanical ventilation needs
    
    Immediate Clinical Actions by Risk Level:
    
    Low Risk Management:
    - Standard ward admission with routine COVID-19 protocols
    - Regular monitoring with standard nursing assessments
    - Continue current oxygen therapy and supportive care
    - Monitor for clinical deterioration and reassess qCSI if condition changes
    - Consider discharge planning if other factors permit
    
    Intermediate Risk Management:
    - Enhanced monitoring with more frequent respiratory assessments
    - Consider step-down unit or higher acuity ward placement
    - Respiratory therapy consultation for optimization of oxygen delivery
    - Prepare for potential escalation and ensure equipment availability
    - Close communication with rapid response team and intensivists
    
    High Risk Management:
    - Immediate ICU consultation and consideration for higher level of care
    - Continuous monitoring with hourly respiratory assessments
    - Prepare high-flow oxygen, noninvasive ventilation equipment
    - Ensure immediate availability of intubation equipment and expertise
    - Proactive communication with critical care and respiratory therapy
    - Consider prone positioning and other advanced respiratory interventions
    
    Clinical Decision Support:
    
    Monitoring and Assessment:
    - Serial qCSI calculations to track clinical progression
    - Continuous pulse oximetry and respiratory rate monitoring
    - Regular assessment of work of breathing and accessory muscle use
    - Blood gas analysis for patients with deteriorating respiratory status
    - Chest imaging to assess for pneumonia progression
    
    Oxygen Therapy Optimization:
    - Titrate oxygen to maintain target saturations (typically >90-94%)
    - Consider high-flow nasal cannula for patients requiring >6 L/min
    - Evaluate for noninvasive ventilation in appropriate candidates
    - Monitor for CO2 retention in patients with chronic lung disease
    - Assess patient comfort and tolerance of respiratory support
    
    Resource Allocation:
    - Staff assignment based on qCSI risk level and monitoring requirements
    - Equipment preparation and availability based on predicted needs
    - Bed placement decisions incorporating qCSI risk stratification
    - Early communication with specialty services based on risk level
    - Capacity planning and patient flow optimization
    
    Quality Assurance and Documentation:
    - Document qCSI score calculation and clinical interpretation
    - Record rationale for level of care and monitoring decisions
    - Plan systematic reassessment schedule based on risk level
    - Monitor outcomes and validate qCSI performance in local population
    
    Follow-up and Monitoring:
    - Reassess qCSI if clinical condition changes significantly
    - Serial evaluations to track improvement or deterioration
    - Adjust level of care and monitoring based on clinical response
    - Document response to interventions and treatment modifications
    
    Limitations and Clinical Judgment:
    - qCSI predicts respiratory failure, not overall mortality or complications
    - Consider patient-specific factors not captured in the scoring system
    - May have different performance in vaccinated vs. unvaccinated patients
    - Should supplement, not replace, comprehensive clinical assessment
    - Consider local COVID-19 epidemiology and variant characteristics
    
    The qCSI enables evidence-based risk stratification that improves resource allocation, 
    enhances patient safety through proactive monitoring, and supports optimal outcomes 
    through early identification and intervention for COVID-19 patients at risk for 
    respiratory deterioration.
    
    Reference: See module docstring for complete citation list.
    """
    
    result: int = Field(
        ...,
        description="qCSI score calculated from respiratory parameters. Score ranges from 0 to 12 points, with higher scores indicating greater risk of critical respiratory failure within 24 hours.",
        example=5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the qCSI score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including respiratory failure risk category, monitoring recommendations, level of care guidance, and resource allocation based on the calculated qCSI score.",
        example="Intermediate risk for critical respiratory failure within 24 hours. Enhanced monitoring recommended with frequent respiratory assessments every 2-4 hours. Consider higher level of care, telemetry monitoring, and preparedness for respiratory support. Implement close observation protocols and ensure availability of oxygen therapy equipment."
    )
    
    stage: str = Field(
        ...,
        description="qCSI risk category (Low Risk, Intermediate Risk, or High Risk) with associated clinical significance for COVID-19 management",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the respiratory failure risk level associated with the calculated qCSI score",
        example="Intermediate risk for respiratory failure"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5,
                "unit": "points",
                "interpretation": "Intermediate risk for critical respiratory failure within 24 hours. Enhanced monitoring recommended with frequent respiratory assessments every 2-4 hours. Consider higher level of care, telemetry monitoring, and preparedness for respiratory support. Implement close observation protocols and ensure availability of oxygen therapy equipment.",
                "stage": "Intermediate Risk",
                "stage_description": "Intermediate risk for respiratory failure"
            }
        }