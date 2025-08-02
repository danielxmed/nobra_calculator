"""
qSOFA (Quick SOFA) Score for Sepsis Models

Request and response models for qSOFA Score calculation.

References (Vancouver style):
1. Seymour CW, Liu VX, Iwashyna TJ, Brunkhorst FM, Rea TD, Scherag A, et al. 
   Assessment of Clinical Criteria for Sepsis: For the Third International Consensus 
   Definitions for Sepsis and Septic Shock (Sepsis-3). JAMA. 2016 Feb 23;315(8):762-74. 
   doi: 10.1001/jama.2016.0288.
2. Singer M, Deutschman CS, Seymour CW, Shankar-Hari M, Annane D, Bauer M, et al. 
   The Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3). 
   JAMA. 2016 Feb 23;315(8):801-10. doi: 10.1001/jama.2016.0287.
3. Freund Y, Lemachatti N, Krastinova E, Van Laer M, Claessens YE, Avondo A, et al. 
   Prognostic Accuracy of Sepsis-3 Criteria for In-Hospital Mortality Among Patients 
   With Suspected Infection Presenting to the Emergency Department. JAMA. 2017 Jan 17;317(3):301-308. 
   doi: 10.1001/jama.2016.20328.

The qSOFA (Quick SOFA) Score for Sepsis is a simplified, rapid bedside clinical assessment 
tool designed to identify patients with suspected infection who are at greater risk for 
poor outcomes outside the intensive care unit (ICU). Introduced by the Sepsis-3 task force 
in February 2016, the qSOFA represents a significant advancement in sepsis recognition by 
providing a practical tool that requires no laboratory tests and can be calculated quickly 
at the bedside.

Clinical Background and Development:
The qSOFA was developed as part of the Third International Consensus Definitions for Sepsis 
and Septic Shock (Sepsis-3), which redefined sepsis as "life-threatening organ dysfunction 
caused by a dysregulated host response to infection." The qSOFA simplifies the full Sequential 
Organ Failure Assessment (SOFA) score by focusing on three easily assessable clinical criteria 
that can be rapidly evaluated in any healthcare setting.

Clinical Applications:
- Rapid identification of high-risk patients with suspected infection outside the ICU
- Triggering immediate sepsis management protocols and interventions
- Risk stratification for in-hospital mortality in suspected sepsis
- Guiding decisions about level of care and monitoring intensity
- Supporting early recognition and treatment initiatives
- Quality improvement and sepsis surveillance programs
- Emergency department triage and disposition planning
- Clinical research stratification and endpoint assessment

qSOFA Score Components:
The qSOFA uses three simple clinical criteria, each contributing 1 point when present:

1. Respiratory Rate ≥22 breaths per minute (1 point):
   - Indicates respiratory distress or compensation for metabolic acidosis
   - Easily assessed at bedside without equipment
   - May be earliest sign of physiologic deterioration
   - Consider measurement over full minute for accuracy

2. Altered Mental Status (Glasgow Coma Scale <15) (1 point):
   - Any deviation from baseline cognitive function
   - Includes confusion, disorientation, somnolence, or decreased responsiveness
   - May indicate cerebral hypoperfusion or sepsis-associated encephalopathy
   - Assess using formal GCS or simplified AVPU scale

3. Systolic Blood Pressure ≤100 mmHg (1 point):
   - Indicates potential hypotension and circulatory compromise
   - May represent early shock or cardiovascular dysfunction
   - Should be confirmed with repeated measurements if possible
   - Consider patient's baseline blood pressure when interpreting

Risk Stratification and Clinical Outcomes:
The qSOFA score stratifies patients into two primary risk categories:

Low Risk (qSOFA 0-1 points):
- Lower risk for poor outcomes associated with sepsis
- In-hospital mortality risk remains elevated but less than high-risk group
- Continue standard infection management with close monitoring
- Consider full SOFA score calculation if clinical suspicion remains high
- Monitor for clinical deterioration and reassess qSOFA serially

High Risk (qSOFA ≥2 points):
- 3- to 14-fold increase in risk of in-hospital mortality
- Strongly suggests presence of sepsis with organ dysfunction
- Triggers immediate implementation of sepsis management protocols
- Requires urgent evaluation for ICU admission and advanced care
- Mandates aggressive resuscitation and antibiotic therapy

Validation and Performance:
The qSOFA has been extensively validated across diverse populations:
- Original derivation and validation: 148,907 patients with suspected infection
- Demonstrated superior predictive validity outside ICU settings
- Consistent performance across multiple healthcare systems and countries
- Area under ROC curve comparable to full SOFA for mortality prediction
- Simple calculation enhances clinical usability and rapid implementation

Clinical Implementation Guidelines:
- Calculate for all patients with suspected infection outside the ICU
- Reassess serially if clinical condition changes
- Use as part of comprehensive sepsis evaluation, not in isolation
- Combine with clinical judgment and infection probability assessment
- Document score and rationale for clinical decisions
- Integrate into sepsis protocols and clinical decision support systems
- Train healthcare providers on proper assessment techniques

Important Clinical Considerations:
- qSOFA is a mortality predictor, not a diagnostic test for sepsis
- Designed specifically for non-ICU settings; full SOFA preferred in ICU
- Should not delay appropriate treatment while calculating score
- Consider patient baseline and chronic conditions when interpreting
- May have different performance characteristics in specific populations
- Results should always be interpreted in clinical context

Treatment Implications by Score:
qSOFA <2: Continue infection management with standard monitoring and consider full SOFA
qSOFA ≥2: Implement immediate sepsis protocols including:
- Blood cultures before antibiotics (if feasible without delay)
- Broad-spectrum antibiotics within 1 hour
- Intravenous fluid resuscitation (30 mL/kg crystalloid within 3 hours)
- Vasopressor therapy if hypotension persists after fluid resuscitation
- Serial lactate measurements and hemodynamic monitoring
- Consider ICU consultation and advanced supportive care

Quality Assurance and Monitoring:
- Regular training on proper assessment techniques
- Audit compliance with qSOFA-triggered interventions
- Monitor outcomes and quality metrics for qSOFA-positive patients
- Integrate into electronic health record systems for automated calculation
- Use for performance improvement initiatives and sepsis care bundles

The qSOFA score represents a paradigm shift toward rapid, practical sepsis recognition 
that can be implemented across healthcare settings to improve early identification and 
treatment of sepsis, ultimately reducing mortality and improving patient outcomes.
"""

from pydantic import BaseModel, Field
from typing import Literal


class QsofaScoreRequest(BaseModel):
    """
    Request model for qSOFA (Quick SOFA) Score for Sepsis
    
    The qSOFA score provides rapid bedside assessment to identify patients with suspected 
    infection who are at greater risk for poor outcomes outside the ICU. This simplified 
    tool uses three easily assessable clinical criteria to quickly stratify mortality risk 
    and trigger appropriate sepsis management protocols.
    
    Clinical Assessment Guidelines:
    
    1. Respiratory Rate Assessment:
       - Count respirations for a full minute when possible for accuracy
       - Threshold: ≥22 breaths per minute indicates respiratory distress
       - May be earliest sign of physiologic deterioration in sepsis
       - Consider baseline respiratory rate and underlying lung disease
       - Document if patient is receiving supplemental oxygen or ventilatory support
    
    2. Mental Status Evaluation:
       - Use Glasgow Coma Scale (GCS) or simplified AVPU assessment
       - Threshold: GCS <15 or any alteration from baseline mental status
       - Include confusion, disorientation, somnolence, or decreased responsiveness
       - Consider baseline cognitive function and recent medications
       - Document specific findings (confusion type, GCS components, etc.)
    
    3. Blood Pressure Measurement:
       - Use standard blood pressure measurement techniques
       - Threshold: Systolic blood pressure ≤100 mmHg
       - Consider patient's baseline blood pressure when interpreting
       - Confirm with repeated measurements if possible
       - Document position (sitting vs. lying) and cuff size used
    
    Clinical Context and Timing:
    - Assess in patients with suspected or confirmed infection
    - Calculate at initial evaluation and reassess if condition changes
    - Use for non-ICU patients; full SOFA preferred for ICU patients
    - Document time of assessment and clinical context
    - Consider serial measurements to track progression
    
    Interpretation Framework:
    - qSOFA <2: Lower risk, continue standard infection management
    - qSOFA ≥2: High risk, implement immediate sepsis protocols
    - Always combine with clinical judgment and infection probability
    - Consider patient-specific factors not captured in the score
    
    Quality Assurance:
    - Ensure accurate measurement and documentation of all components
    - Verify proper assessment techniques for each criterion
    - Document rationale for clinical decisions based on qSOFA results
    - Plan appropriate monitoring and follow-up based on risk level
    
    References: See module docstring for complete citation list.
    """
    
    respiratory_rate_22_or_higher: Literal["yes", "no"] = Field(
        ...,
        description="Respiratory rate 22 breaths per minute or higher. Count respirations for a full minute when possible. This indicates respiratory distress or compensation and contributes 1 point to the qSOFA score.",
        example="yes"
    )
    
    altered_mental_status: Literal["yes", "no"] = Field(
        ...,
        description="Altered mental status defined as Glasgow Coma Scale (GCS) less than 15. Includes any confusion, disorientation, somnolence, or decreased responsiveness from baseline. Contributes 1 point to the qSOFA score.",
        example="no"
    )
    
    systolic_bp_100_or_lower: Literal["yes", "no"] = Field(
        ...,
        description="Systolic blood pressure 100 mmHg or lower. Indicates potential hypotension and circulatory compromise. Consider patient's baseline blood pressure and confirm with repeated measurements if possible. Contributes 1 point to the qSOFA score.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "respiratory_rate_22_or_higher": "yes",
                "altered_mental_status": "no",
                "systolic_bp_100_or_lower": "no"
            }
        }


class QsofaScoreResponse(BaseModel):
    """
    Response model for qSOFA (Quick SOFA) Score for Sepsis
    
    The qSOFA score provides critical risk stratification for patients with suspected 
    infection, enabling rapid identification of those at higher risk for poor outcomes 
    and guiding immediate clinical decision-making. Understanding qSOFA results is 
    essential for timely sepsis recognition and appropriate treatment implementation.
    
    Risk Category Interpretation and Clinical Management:
    
    Low Risk (qSOFA 0-1 points):
    - Lower risk for poor outcomes, but still requires careful monitoring
    - Continue standard infection management protocols
    - Monitor closely for clinical deterioration and reassess qSOFA serially
    - Consider full SOFA score calculation if high clinical suspicion for sepsis
    - Standard antibiotic therapy and supportive care as indicated
    - Document rationale for monitoring plan and follow-up schedule
    
    High Risk (qSOFA ≥2 points, 3-14 fold increased mortality):
    - Significantly increased risk for in-hospital mortality
    - Strongly suggests presence of sepsis with organ dysfunction
    - Triggers immediate implementation of comprehensive sepsis management
    - Requires urgent evaluation and consideration for higher level of care
    - Mandates aggressive interventions within specified time windows
    - Continuous monitoring and frequent reassessment required
    
    Immediate Clinical Actions for High-Risk Patients (qSOFA ≥2):
    
    Within 1 Hour (Hour-1 Bundle):
    - Obtain blood cultures before antibiotics (if feasible without delay)
    - Administer broad-spectrum antibiotics based on suspected source
    - Measure serum lactate level for additional risk stratification
    - Begin aggressive intravenous fluid resuscitation (30 mL/kg crystalloid within 3 hours)
    - Assess and document hemodynamic status and perfusion
    
    Monitoring and Assessment:
    - Continuous cardiac monitoring and frequent vital signs
    - Serial mental status assessments and neurologic checks
    - Hourly urine output monitoring and fluid balance
    - Blood pressure monitoring and perfusion assessment
    - Serial lactate measurements and laboratory monitoring
    - Consider invasive hemodynamic monitoring for complex cases
    
    Advanced Interventions (if indicated):
    - Vasopressor therapy if hypotension persists after adequate fluid resuscitation
    - ICU consultation and evaluation for intensive care admission
    - Consider mechanical ventilation for respiratory failure
    - Evaluate for source control interventions (drainage, debridement, etc.)
    - Specialist consultation as clinically appropriate
    
    Clinical Decision Support:
    
    Antibiotic Selection:
    - Broad-spectrum coverage based on suspected source and local resistance patterns
    - Consider patient allergies, renal function, and drug interactions
    - Adjust based on culture results and clinical response
    - Ensure adequate dosing for severity of illness
    
    Fluid Resuscitation Strategy:
    - Initial bolus: 30 mL/kg crystalloid within first 3 hours
    - Reassess volume status and response to fluid therapy
    - Consider balanced crystalloids over normal saline
    - Monitor for fluid overload in patients with heart failure or renal disease
    
    Vasopressor Considerations:
    - Initiate if MAP <65 mmHg despite adequate fluid resuscitation
    - Norepinephrine is typically first-line agent
    - Target mean arterial pressure ≥65 mmHg
    - Monitor for end-organ perfusion and titrate accordingly
    
    Quality Assurance and Documentation:
    - Document qSOFA score calculation and interpretation
    - Record time-sensitive interventions and response to therapy
    - Plan systematic reassessment and monitoring schedule
    - Consider integration with sepsis protocols and quality metrics
    
    Follow-up and Monitoring:
    - Serial qSOFA assessments to track clinical progression
    - Full SOFA score calculation for comprehensive organ dysfunction assessment
    - Regular evaluation of treatment response and clinical trajectory
    - Adjustment of therapy based on patient response and culture results
    
    Limitations and Clinical Judgment:
    - qSOFA is a mortality predictor, not a diagnostic test for sepsis
    - Consider patient-specific factors and clinical context
    - May have different performance in certain populations (immunocompromised, elderly)
    - Should supplement, not replace, comprehensive clinical assessment
    - Reassess if clinical condition changes significantly
    
    The qSOFA score enables rapid, evidence-based identification of high-risk patients 
    with suspected infection, facilitating timely implementation of life-saving sepsis 
    interventions and improving overall patient outcomes through systematic risk-based care.
    
    Reference: See module docstring for complete citation list.
    """
    
    result: int = Field(
        ...,
        description="qSOFA score calculated from clinical criteria. Score ranges from 0 to 3 points, with scores ≥2 indicating significantly increased risk for in-hospital mortality and need for immediate sepsis management.",
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the qSOFA score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including mortality risk category, sepsis management recommendations, monitoring guidance, and treatment protocols based on the calculated qSOFA score.",
        example="qSOFA score <2. Lower risk for poor outcomes associated with sepsis. Continue standard infection management and monitoring. Consider obtaining full SOFA score with laboratory results if clinical suspicion remains high for sepsis. Monitor closely for clinical deterioration and reassess qSOFA if patient condition changes."
    )
    
    stage: str = Field(
        ...,
        description="qSOFA risk category (Low Risk or High Risk) with associated clinical significance for sepsis management",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the mortality risk level associated with the calculated qSOFA score",
        example="Low mortality risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "qSOFA score <2. Lower risk for poor outcomes associated with sepsis. Continue standard infection management and monitoring. Consider obtaining full SOFA score with laboratory results if clinical suspicion remains high for sepsis. Monitor closely for clinical deterioration and reassess qSOFA if patient condition changes.",
                "stage": "Low Risk",
                "stage_description": "Low mortality risk"
            }
        }