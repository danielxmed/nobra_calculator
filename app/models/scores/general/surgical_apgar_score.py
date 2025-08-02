"""
Surgical Apgar Score (SAS) Models

Request and response models for Surgical Apgar Score calculation.

References (Vancouver style):
1. Gawande AA, Kwaan MR, Regenbogen SE, Lipsitz SA, Zinner MJ. An Apgar 
   score for surgery. J Am Coll Surg. 2007 Apr;204(2):201-8. 
   doi: 10.1016/j.jamcollsurg.2006.11.011.
2. Regenbogen SE, Lancaster RT, Lipsitz SR, Greenberg CC, Hutter MM, 
   Gawande AA. Does the Surgical Apgar Score measure intraoperative 
   performance? Ann Surg. 2008 Aug;248(2):320-8. 
   doi: 10.1097/SLA.0b013e318181c6d8.

The Surgical Apgar Score (SAS) is a simple 10-point scoring system developed 
to predict postoperative risk of major complications and death in patients 
undergoing major surgery. Analogous to the Virginia Apgar score for newborns, 
the SAS provides immediate postoperative risk stratification using three 
intraoperative parameters measured during surgery.
"""

from pydantic import BaseModel, Field
from typing import Literal


class SurgicalApgarScoreRequest(BaseModel):
    """
    Request model for Surgical Apgar Score (SAS) calculation
    
    The Surgical Apgar Score (SAS) is a validated clinical prediction tool 
    that provides immediate postoperative risk stratification for patients 
    undergoing major surgery. Developed by Atul Gawande and colleagues in 2007, 
    this scoring system fills a critical gap in perioperative medicine by 
    offering objective, standardized assessment of surgical outcomes based 
    on intraoperative parameters.
    
    Historical Development and Clinical Rationale:
    
    Background and Inspiration:
    The SAS was conceptualized as a surgical analogue to Virginia Apgar's 
    revolutionary scoring system for newborns, which has been used since 1953 
    to rapidly assess neonatal condition and guide immediate care decisions. 
    Just as the Apgar score transformed neonatal care by providing standardized 
    assessment criteria, the Surgical Apgar Score was designed to standardize 
    postoperative risk assessment and improve surgical outcomes.
    
    The development team recognized that while numerous preoperative risk 
    assessment tools existed (ASA classification, POSSUM score, etc.), there 
    was a significant void in tools that could provide immediate postoperative 
    risk stratification based on what actually occurred during the surgical 
    procedure itself.
    
    Clinical Problem Addressed:
    Traditional risk assessment models primarily rely on preoperative patient 
    characteristics and planned surgical procedures, but they fail to account 
    for intraoperative events that can dramatically influence postoperative 
    outcomes. Factors such as unexpected bleeding, hemodynamic instability, 
    or technical complications during surgery can fundamentally alter a 
    patient's risk profile regardless of their preoperative status.
    
    The SAS addresses this limitation by incorporating real-time intraoperative 
    data to provide dynamic risk assessment that reflects what actually 
    transpired during the surgical procedure.
    
    Intraoperative Parameter Selection and Physiologic Rationale:
    
    The three parameters included in the SAS were selected based on their 
    physiologic significance, ease of measurement, and correlation with 
    postoperative outcomes:
    
    Estimated Blood Loss (EBL):
    
    Physiologic Significance:
    Blood loss during surgery reflects multiple factors including surgical 
    complexity, technical difficulty, anatomical variations, and hemostatic 
    competence. Excessive bleeding can lead to hypovolemic shock, coagulopathy, 
    hypothermia, and the need for blood transfusion, all of which increase 
    perioperative morbidity and mortality.
    
    Clinical Correlation:
    Studies have consistently demonstrated that increased intraoperative blood 
    loss correlates with higher rates of postoperative complications including:
    - Increased infection risk due to immunosuppressive effects of transfusion
    - Coagulopathy and bleeding complications
    - Respiratory complications from transfusion-related acute lung injury
    - Cardiovascular stress from volume shifts and anemia
    - Prolonged hospital stay and increased resource utilization
    
    Measurement Considerations:
    EBL estimation includes blood in suction canisters, blood-soaked sponges, 
    and visual assessment of blood loss. While subjective, this measurement 
    can be standardized through team training and protocols.
    
    Scoring Thresholds:
    - ≤100 mL: 3 points (minimal blood loss, uncomplicated procedure)
    - 101-600 mL: 2 points (moderate blood loss, routine procedure)
    - 601-1,000 mL: 1 point (significant blood loss, complex procedure)
    - >1,000 mL: 0 points (major blood loss, high-risk procedure)
    
    Lowest Mean Arterial Pressure (MAP):
    
    Physiologic Significance:
    Mean arterial pressure represents the average pressure in the arterial 
    system during the cardiac cycle and is a key determinant of organ perfusion. 
    Hypotension during surgery can lead to inadequate tissue perfusion, organ 
    ischemia, and subsequent complications.
    
    Clinical Correlation:
    Intraoperative hypotension has been associated with:
    - Acute kidney injury due to reduced renal perfusion
    - Myocardial ischemia and cardiac complications
    - Cerebral hypoperfusion and neurologic complications
    - Hepatic dysfunction from reduced hepatic blood flow
    - Wound healing complications from impaired tissue perfusion
    
    Pathophysiologic Mechanisms:
    Hypotension during surgery can result from multiple factors including:
    - Anesthetic-induced vasodilation and cardiac depression
    - Hypovolemia from bleeding or fluid losses
    - Surgical manipulation affecting venous return
    - Underlying cardiovascular disease
    - Sepsis or systemic inflammatory response
    
    Scoring Thresholds:
    - ≥70 mmHg: 3 points (adequate perfusion pressure maintained)
    - 55-69 mmHg: 2 points (mild hypotension, generally tolerable)
    - 40-54 mmHg: 1 point (moderate hypotension, concerning)
    - <40 mmHg: 0 points (severe hypotension, high risk for complications)
    
    Lowest Heart Rate:
    
    Physiologic Significance:
    Heart rate is a fundamental vital sign that reflects autonomic nervous 
    system function, intravascular volume status, cardiac function, and 
    response to surgical stress. Both bradycardia and tachycardia can 
    indicate physiologic compromise during surgery.
    
    Clinical Correlations:
    
    Bradycardia (low heart rate) may indicate:
    - Adequate anesthesia and surgical conditions
    - Increased intracranial pressure
    - Hypothermia
    - Medication effects (beta-blockers, anesthetics)
    - Cardiac conduction abnormalities
    
    Tachycardia (high heart rate) may indicate:
    - Inadequate anesthesia or pain control
    - Hypovolemia or bleeding
    - Hyperthermia or malignant hyperthermia
    - Medication effects (sympathomimetics)
    - Underlying cardiac disease
    - Sepsis or inflammatory response
    
    Optimal Range Consideration:
    The scoring system reflects that moderate heart rates (56-65 bpm) often 
    indicate optimal surgical conditions with adequate anesthesia and 
    hemodynamic stability, while extreme values in either direction may 
    suggest physiologic stress or instability.
    
    Scoring Thresholds:
    - ≤55 bpm: 4 points (optimal - indicates stable, well-controlled conditions)
    - 56-65 bpm: 3 points (excellent - ideal surgical heart rate range)
    - 66-75 bpm: 2 points (good - acceptable heart rate range)
    - 76-85 bpm: 1 point (concerning - may indicate stress or inadequate anesthesia)
    - >85 bpm: 0 points (worrisome - suggests physiologic stress or instability)
    
    Clinical Implementation and Workflow Integration:
    
    Timing of Assessment:
    The SAS should be calculated at the conclusion of the surgical procedure, 
    after skin closure but before transfer to the recovery area. This timing 
    ensures that all intraoperative events have been captured while the 
    information is still immediately relevant for postoperative care decisions.
    
    Data Collection Responsibilities:
    - Anesthesiology team: Heart rate and blood pressure monitoring and documentation
    - Surgical team: Estimation of blood loss including all sources
    - Circulating nurse: Coordination of data collection and score calculation
    - All team members: Verification of accuracy and completeness
    
    Documentation Requirements:
    - Record all three parameters clearly in the operative record
    - Calculate and document the total SAS score
    - Include the score in handoff communication to recovery staff
    - Use the score to guide immediate postoperative care decisions
    
    Quality Assurance and Standardization:
    - Implement standardized protocols for EBL estimation
    - Ensure consistent blood pressure and heart rate monitoring
    - Regular team training on score calculation and interpretation
    - Audit score accuracy and correlation with outcomes
    
    Clinical Decision-Making Framework:
    
    Risk Stratification and Triage:
    
    Very High Risk (Scores ≤4):
    These patients have approximately 58.6% risk of 30-day mortality or major 
    morbidity and require immediate intensive intervention:
    
    Recommended Actions:
    - Immediate ICU admission with intensive monitoring
    - Arterial line and central venous access if not already present
    - Frequent laboratory monitoring including blood gases, lactate, coagulation studies
    - Early consultation with critical care specialists
    - Aggressive hemodynamic optimization and organ support
    - Family notification and discussion of prognosis
    - Consider early re-exploration if surgical complications suspected
    
    High Risk (Scores 5-6):
    These patients have elevated risk requiring enhanced surveillance:
    
    Recommended Actions:
    - Step-down unit or high-dependency care admission
    - Frequent vital sign monitoring (every 15-30 minutes initially)
    - Early mobility and respiratory care protocols
    - Proactive pain and nausea management
    - Low threshold for ICU transfer if deterioration occurs
    - Enhanced nursing ratios and monitoring protocols
    - Regular assessment for developing complications
    
    Low Risk (Scores ≥7):
    These patients have low complication risk (3.6% for scores 9-10) and can 
    receive standard care:
    
    Recommended Actions:
    - Standard postoperative unit admission
    - Routine vital sign monitoring protocols
    - Standard pain management and mobility protocols
    - Normal discharge planning timelines
    - Routine follow-up arrangements
    - Standard patient education and home care instructions
    
    Integration with Existing Risk Assessment Tools:
    
    Complementary Use with Preoperative Scores:
    The SAS should be used in conjunction with, not as a replacement for, 
    preoperative risk assessment tools such as:
    - ASA Physical Status Classification
    - Revised Cardiac Risk Index (RCRI)
    - POSSUM score
    - Surgical Risk Calculator (NSQIP)
    
    Enhanced Predictive Value:
    When combined with preoperative risk factors, the SAS provides more 
    accurate risk prediction than either approach alone, creating a 
    comprehensive perioperative risk assessment strategy.
    
    Dynamic Risk Adjustment:
    The SAS allows for real-time adjustment of risk assessment based on 
    actual intraoperative events, providing more nuanced and accurate 
    postoperative risk stratification.
    
    Special Considerations and Limitations:
    
    Surgical Specialty Considerations:
    
    Cardiac Surgery:
    - May require different threshold values due to unique physiology
    - Consider cardiopulmonary bypass effects on hemodynamics
    - Account for planned hypothermia and its effects on vital signs
    
    Neurosurgery:
    - Consider intracranial pressure effects on heart rate and blood pressure
    - Account for positioning-related hemodynamic changes
    - Be aware of anesthetic techniques that may affect vital signs
    
    Emergency Surgery:
    - May have limited baseline data for comparison
    - Consider pre-existing shock or instability
    - Account for resuscitation effects on measured parameters
    
    Pediatric Surgery:
    - Age-appropriate normal ranges for vital signs
    - Different blood loss thresholds relative to body weight
    - Developmental considerations in physiologic responses
    
    System-Level Implementation:
    
    Electronic Health Record Integration:
    - Automated calculation tools within anesthesia records
    - Real-time alerts for high-risk scores
    - Integration with postoperative order sets and protocols
    - Trending analysis for quality improvement initiatives
    
    Quality Improvement Applications:
    - Benchmarking surgical and anesthetic performance
    - Identifying opportunities for process improvement
    - Monitoring outcomes and correlation with scores
    - Educational tool for resident and fellow training
    
    Resource Allocation:
    - Objective criteria for ICU bed allocation
    - Staffing decisions based on predicted acuity
    - Equipment and monitoring resource planning
    - Cost-effectiveness analysis of interventions
    
    Research and Validation:
    
    Ongoing Validation Studies:
    The SAS continues to be validated across diverse surgical populations, 
    healthcare systems, and international settings to ensure broad 
    applicability and accuracy.
    
    Outcome Correlation:
    Studies consistently demonstrate correlation between SAS scores and:
    - 30-day mortality and morbidity
    - Length of hospital stay
    - ICU admission requirements
    - Readmission rates
    - Healthcare resource utilization
    
    The Surgical Apgar Score represents a significant advancement in 
    perioperative medicine, providing a simple, objective, and immediately 
    available tool for postoperative risk assessment that enhances clinical 
    decision-making and potentially improves patient outcomes through better 
    risk stratification and resource allocation.
    
    References (Vancouver style):
    1. Gawande AA, Kwaan MR, Regenbogen SE, Lipsitz SA, Zinner MJ. An Apgar 
       score for surgery. J Am Coll Surg. 2007 Apr;204(2):201-8. 
       doi: 10.1016/j.jamcollsurg.2006.11.011.
    2. Regenbogen SE, Lancaster RT, Lipsitz SR, Greenberg CC, Hutter MM, 
       Gawande AA. Does the Surgical Apgar Score measure intraoperative 
       performance? Ann Surg. 2008 Aug;248(2):320-8. 
       doi: 10.1097/SLA.0b013e318181c6d8.
    """
    
    estimated_blood_loss: Literal["≤100 mL", "101-600 mL", "601-1,000 mL", ">1,000 mL"] = Field(
        ...,
        description="Total estimated blood loss during the surgical procedure. Includes blood in suction "
                   "canisters, blood-soaked sponges, and visual assessment. ≤100 mL indicates minimal "
                   "blood loss with uncomplicated procedure (3 points). 101-600 mL represents moderate "
                   "blood loss in routine procedures (2 points). 601-1,000 mL indicates significant "
                   "blood loss in complex procedures (1 point). >1,000 mL represents major blood loss "
                   "in high-risk procedures (0 points).",
        example="101-600 mL"
    )
    
    lowest_mean_arterial_pressure: Literal["<40 mmHg", "40-54 mmHg", "55-69 mmHg", "≥70 mmHg"] = Field(
        ...,
        description="Lowest mean arterial pressure recorded during the surgical procedure. MAP represents "
                   "average arterial pressure during cardiac cycle and indicates organ perfusion adequacy. "
                   "≥70 mmHg indicates adequate perfusion pressure maintained (3 points). 55-69 mmHg "
                   "represents mild hypotension generally tolerable (2 points). 40-54 mmHg indicates "
                   "moderate hypotension of concern (1 point). <40 mmHg represents severe hypotension "
                   "with high complication risk (0 points).",
        example="≥70 mmHg"
    )
    
    lowest_heart_rate: Literal["≤55 bpm", "56-65 bpm", "66-75 bpm", "76-85 bpm", ">85 bpm"] = Field(
        ...,
        description="Lowest heart rate recorded during the surgical procedure. Heart rate reflects "
                   "autonomic function, volume status, and response to surgical stress. ≤55 bpm "
                   "indicates optimal stable conditions (4 points). 56-65 bpm represents excellent "
                   "ideal surgical range (3 points). 66-75 bpm indicates good acceptable range "
                   "(2 points). 76-85 bpm may indicate stress or inadequate anesthesia (1 point). "
                   ">85 bpm suggests physiologic stress or instability (0 points).",
        example="56-65 bpm"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "estimated_blood_loss": "101-600 mL",
                "lowest_mean_arterial_pressure": "≥70 mmHg",
                "lowest_heart_rate": "56-65 bpm"
            }
        }


class SurgicalApgarScoreResponse(BaseModel):
    """
    Response model for Surgical Apgar Score (SAS) calculation
    
    The Surgical Apgar Score provides immediate postoperative risk stratification 
    with scores ranging from 0-10 points. Higher scores indicate better surgical 
    outcomes and lower risk of major complications, while lower scores identify 
    patients requiring intensive monitoring and intervention.
    
    Score Interpretation and Clinical Decision Framework:
    
    Very High Risk Category (Scores ≤4):
    
    Clinical Significance:
    Patients with SAS scores ≤4 represent a critically high-risk population 
    with approximately 58.6% risk of 30-day mortality or major morbidity. 
    These scores indicate that significant physiologic compromise occurred 
    during surgery, requiring immediate and intensive postoperative intervention.
    
    Pathophysiologic Implications:
    Low SAS scores typically result from combinations of:
    - Major blood loss (>600-1,000 mL) indicating complex surgery or complications
    - Significant hypotension (<55 mmHg MAP) suggesting inadequate organ perfusion
    - Hemodynamic instability (HR >85 or extreme bradycardia) indicating physiologic stress
    
    These factors collectively suggest that the patient experienced substantial 
    physiologic stress during surgery and is at high risk for multiple organ 
    dysfunction, complications, and mortality.
    
    Immediate Management Priorities:
    - ICU admission with 1:1 nursing ratios and continuous monitoring
    - Arterial line placement for beat-to-beat blood pressure monitoring
    - Central venous access for fluid management and medication administration
    - Frequent laboratory monitoring: ABG, lactate, CBC, comprehensive metabolic panel
    - Coagulation studies if bleeding concerns or massive transfusion occurred
    - Early goal-directed therapy for hemodynamic optimization
    - Aggressive temperature management and warming protocols
    - Early consultation with critical care specialists and surgeon
    
    Monitoring Protocols:
    - Continuous cardiac monitoring with arrhythmia detection
    - Hourly urine output monitoring with Foley catheter
    - Neurologic assessment every 2 hours or continuous if indicated
    - Respiratory status monitoring with potential for mechanical ventilation
    - Pain assessment and multimodal analgesia to reduce physiologic stress
    - Early mobilization protocols as soon as hemodynamically stable
    
    High Risk Category (Scores 5-6):
    
    Clinical Significance:
    Patients with SAS scores of 5-6 have elevated risk of postoperative 
    complications and require enhanced surveillance and proactive management. 
    While not as critical as very high-risk patients, they still experienced 
    significant intraoperative events that increase complication risk.
    
    Risk Factors and Implications:
    These scores typically indicate:
    - Moderate blood loss (400-800 mL) suggesting surgical complexity
    - Mild to moderate hypotension (MAP 40-69 mmHg) indicating some hemodynamic compromise
    - Heart rate abnormalities suggesting physiologic stress response
    
    Management Strategy:
    - Step-down unit or progressive care unit admission
    - Enhanced nursing surveillance with 1:2 or 1:3 nursing ratios
    - Vital sign monitoring every 15-30 minutes for first 4-6 hours
    - Early warning system activation for clinical deterioration
    - Proactive fluid management and electrolyte monitoring
    - Multimodal pain management to minimize physiologic stress
    - Early mobilization and respiratory therapy
    - Low threshold for ICU transfer if any signs of deterioration
    
    Surveillance Protocols:
    - Trending vital signs with automated alert systems
    - Laboratory monitoring every 6-12 hours initially
    - Daily assessment of organ function (renal, hepatic, cardiac)
    - Early identification and treatment of complications
    - Structured handoff communication between shifts
    - Family education about potential complications and warning signs
    
    Low Risk Category (Scores ≥7):
    
    Clinical Significance:
    Patients with SAS scores ≥7 have low risk of major postoperative 
    complications, with those scoring 9-10 having only 3.6% risk of 
    mortality or major morbidity. These scores indicate that surgery 
    proceeded smoothly with minimal physiologic compromise.
    
    Favorable Prognostic Indicators:
    High SAS scores typically reflect:
    - Minimal blood loss (≤600 mL) indicating uncomplicated surgery
    - Stable blood pressure (MAP ≥55 mmHg) indicating adequate perfusion
    - Optimal heart rate control indicating stable anesthetic management
    
    Standard Care Approach:
    - General surgical ward admission with standard monitoring
    - Routine vital sign assessment every 4 hours initially
    - Standard pain management protocols
    - Early mobilization and diet advancement as tolerated
    - Normal discharge planning timelines
    - Routine follow-up arrangements
    
    Enhanced Recovery Protocols:
    - Early removal of urinary catheters and monitoring devices
    - Encouragement of early ambulation and self-care activities
    - Patient education for home care and activity restrictions
    - Standard wound care and infection prevention measures
    - Routine medication management and discharge planning
    
    Resource Allocation and Economic Implications:
    
    Cost-Effectiveness Considerations:
    The SAS enables more efficient resource allocation by:
    - Identifying patients who truly need intensive monitoring
    - Reducing unnecessary ICU admissions for low-risk patients
    - Optimizing nursing assignments based on acuity
    - Preventing complications through early identification of high-risk patients
    - Reducing length of stay through appropriate level of care placement
    
    Quality Metrics and Benchmarking:
    - Hospital-wide SAS score distributions for quality assessment
    - Correlation between SAS scores and actual complication rates
    - Surgeon and anesthesiologist performance benchmarking
    - Identification of opportunities for process improvement
    - Patient safety indicator and outcome predictor
    
    Integration with Clinical Pathways:
    
    Electronic Health Record Integration:
    - Automated calculation and documentation of SAS scores
    - Clinical decision support alerts based on score thresholds
    - Integration with postoperative order sets and protocols
    - Trending analysis for individual patients and populations
    - Quality improvement dashboards and reporting
    
    Interdisciplinary Communication:
    - Standardized handoff communication including SAS scores
    - Nursing protocols based on risk stratification
    - Physician rounding priorities based on SAS scores
    - Family communication regarding prognosis and expectations
    - Discharge planning considerations based on risk assessment
    
    Long-term Outcomes and Follow-up:
    
    Predictive Value for Extended Outcomes:
    Research demonstrates that SAS scores correlate not only with immediate 
    postoperative complications but also with:
    - 30-day readmission rates
    - Overall length of stay
    - Long-term functional outcomes
    - Healthcare resource utilization
    - Patient satisfaction scores
    
    Continuous Quality Improvement:
    - Regular validation of SAS score predictive accuracy
    - Adjustment of protocols based on outcome data
    - Staff education and training on score utilization
    - Research initiatives to further validate and refine the tool
    - Integration with national quality databases and registries
    
    The Surgical Apgar Score serves as a powerful tool for immediate 
    postoperative risk stratification, enabling healthcare teams to provide 
    more targeted, efficient, and effective perioperative care while 
    optimizing resource utilization and improving patient outcomes.
    
    Reference: Gawande AA, et al. J Am Coll Surg. 2007;204(2):201-8.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=10,
        description="Calculated Surgical Apgar Score based on intraoperative parameters. "
                   "Total score ranges from 0-10 points with higher scores indicating lower "
                   "risk of postoperative complications. Score calculated by summing points from "
                   "estimated blood loss (0-3 points), lowest MAP (0-3 points), and lowest "
                   "heart rate (0-4 points) measured during surgery.",
        example=8
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the calculated score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation of the Surgical Apgar Score with specific "
                   "recommendations for postoperative management, monitoring protocols, and clinical "
                   "decision guidance. Includes risk stratification, expected complication rates, "
                   "and evidence-based care recommendations based on score category.",
        example="Surgical Apgar Score of 8 indicates low risk of major postoperative complications. "
                "Standard postoperative care and monitoring are appropriate. Follow routine recovery "
                "protocols with standard vital sign monitoring, pain management, and early mobilization. "
                "While the risk is low, continue routine surveillance for potential complications."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on calculated Surgical Apgar Score",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category and recommended clinical approach",
        example="Low risk - usual care recommended"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 8,
                "unit": "points",
                "interpretation": "Surgical Apgar Score of 8 indicates low risk of major postoperative complications. Standard postoperative care and monitoring are appropriate. Follow routine recovery protocols with standard vital sign monitoring, pain management, and early mobilization. While the risk is low, continue routine surveillance for potential complications and provide appropriate patient education for postoperative care and warning signs.",
                "stage": "Low Risk",
                "stage_description": "Low risk - usual care recommended"
            }
        }