"""
Ottawa Subarachnoid Hemorrhage (SAH) Rule for Headache Evaluation Models

Request and response models for Ottawa SAH Rule calculation.

References (Vancouver style):
1. Perry JJ, Stiell IG, Sivilotti ML, Bullard MJ, Emond M, Symington C, et al. 
   Sensitivity of computed tomography performed within six hours of onset of 
   headache for diagnosis of subarachnoid haemorrhage: prospective cohort study. 
   BMJ. 2011;343:d4277. doi: 10.1136/bmj.d4277.
2. Perry JJ, Stiell IG, Sivilotti ML, Bullard MJ, Lee JS, Eisenhauer M, et al. 
   High risk clinical characteristics for subarachnoid haemorrhage in patients 
   with acute headache: prospective cohort study. BMJ. 2010;341:c5204. 
   doi: 10.1136/bmj.c5204.
3. Perry JJ, Sivilotti ML, Sutherland J, Hohl CM, Émond M, Calder LA, et al. 
   Validation of the Ottawa Subarachnoid Hemorrhage Rule in patients with acute 
   headache. CMAJ. 2017;189(45):E1379-E1385. doi: 10.1503/cmaj.170072.

The Ottawa SAH Rule is a highly sensitive clinical decision tool for ruling out 
subarachnoid hemorrhage in alert patients presenting to emergency departments with 
acute headache. With 100% sensitivity and 15.3% specificity, this rule is designed 
as a rule-out tool to safely exclude SAH while guiding appropriate imaging decisions.
"""

from pydantic import BaseModel, Field
from typing import Literal


class OttawaSahRuleRequest(BaseModel):
    """
    Request model for Ottawa Subarachnoid Hemorrhage (SAH) Rule for Headache Evaluation
    
    The Ottawa SAH Rule is a validated clinical decision tool developed to help 
    emergency physicians identify patients with acute headache who are at risk for 
    subarachnoid hemorrhage. This rule demonstrates 100% sensitivity for detecting 
    SAH, making it an excellent rule-out tool, though with limited specificity (15.3%).
    
    Clinical Context and Importance:
    
    Subarachnoid hemorrhage is a rare but life-threatening cause of acute headache, 
    occurring in approximately 1-2% of emergency department patients presenting with 
    headache. However, the consequences of missing SAH are severe, with mortality 
    rates of 25-50% and significant morbidity in survivors. Early recognition and 
    treatment are crucial for optimal outcomes.
    
    Diagnostic Challenge:
    
    The challenge in emergency medicine is identifying which patients with acute 
    headache require urgent neuroimaging or lumbar puncture to rule out SAH, while 
    avoiding unnecessary testing in the majority of patients with benign headaches. 
    Traditional approaches often led to overuse of CT scans and lumbar punctures, 
    increasing healthcare costs and patient discomfort without improving outcomes.
    
    Rule Development and Validation:
    
    The Ottawa SAH Rule was derived from a prospective cohort study of 2,131 patients 
    with acute headache, including 132 cases of SAH. The rule was subsequently 
    validated in multiple external studies involving over 4,000 patients, consistently 
    demonstrating 100% sensitivity for SAH detection across different populations 
    and healthcare settings.
    
    Patient Selection Criteria:
    
    The Ottawa SAH Rule should be applied to patients who meet specific inclusion criteria:
    
    Inclusion Criteria:
    - Alert patients (Glasgow Coma Scale 15)
    - Age ≥15 years
    - New severe headache
    - Headache reaching maximum intensity within 1 hour
    - Presenting to emergency department within 14 days of headache onset
    - Non-traumatic headache (no history of head trauma in past 7 days)
    
    Exclusion Criteria:
    - New neurological findings on examination
    - Prior aneurysm, previous SAH, or known brain tumors
    - Chronic recurrent headaches (≥3 episodes of same character and intensity over >6 months)
    - Altered mental status or neurological deficits
    - Traumatic headache or recent head trauma
    
    Rule Components and Clinical Rationale:
    
    The Ottawa SAH Rule consists of six clinical criteria, each independently 
    associated with increased risk of subarachnoid hemorrhage:
    
    1. Age ≥40 Years:
    Advanced age is associated with increased risk of aneurysmal SAH due to:
    - Higher prevalence of intracranial aneurysms with aging
    - Increased vessel wall weakness and degenerative changes
    - Higher likelihood of hypertension and other vascular risk factors
    - Statistical association with aneurysm rupture in epidemiological studies
    
    2. Neck Pain or Stiffness:
    Meningeal irritation from blood in the subarachnoid space commonly causes:
    - Nuchal rigidity due to inflammatory response
    - Neck pain from chemical meningitis
    - Reflex muscle spasm in response to meningeal inflammation
    - Classic triad component (headache, neck stiffness, altered consciousness)
    
    3. Witnessed Loss of Consciousness:
    Sudden loss of consciousness at headache onset suggests:
    - Acute increase in intracranial pressure from bleeding
    - Transient global cerebral hypoperfusion
    - Reflection of severity and acuity of the hemorrhage
    - Strong predictor of aneurysmal rupture vs. other headache causes
    
    4. Onset During Exertion:
    Physical activity or straining can trigger aneurysm rupture through:
    - Acute elevation in blood pressure and intracranial pressure
    - Increased shear stress on vessel walls
    - Valsalva maneuver effects during lifting, coughing, or sexual activity
    - Common trigger for aneurysmal SAH in previously stable patients
    
    5. Thunderclap Headache:
    Instantaneous onset of maximum pain intensity is pathognomonic for:
    - Sudden vessel rupture and immediate blood extravasation
    - Acute increase in intracranial pressure
    - Classic presentation of aneurysmal SAH
    - Distinguished from gradual onset headaches of other etiologies
    
    6. Limited Neck Flexion on Examination:
    Objective finding of meningeal irritation demonstrated by:
    - Inability to touch chin to chest due to pain
    - Passive neck flexion limitation due to muscle spasm
    - Physical sign of blood-induced chemical meningitis
    - Reliable objective correlate of subjective neck stiffness
    
    Clinical Application and Decision Making:
    
    Rule Interpretation:
    - If ALL criteria are negative: SAH can be ruled out with 100% sensitivity
    - If ANY criterion is positive: SAH cannot be ruled out, further investigation needed
    
    Recommended Actions for Positive Rule:
    - Non-contrast head CT scan within 6 hours of headache onset
    - Consider lumbar puncture if CT negative and clinical suspicion remains high
    - Neurology or neurosurgical consultation for suspected SAH
    - Blood pressure monitoring and management
    - Analgesia and supportive care as appropriate
    
    Performance Characteristics and Limitations:
    
    Strengths:
    - 100% sensitivity for SAH across multiple validation studies
    - Excellent negative predictive value for ruling out SAH
    - Simple bedside application without complex calculations
    - Validated across diverse patient populations and healthcare settings
    - Reduces unnecessary testing while maintaining safety
    
    Limitations:
    - Low specificity (15.3%) leading to many false positives
    - Cannot be used to diagnose SAH (rule-out tool only)
    - Requires careful patient selection meeting inclusion criteria
    - Not applicable to patients with chronic headaches or neurological deficits
    - May increase imaging utilization in some populations
    
    Clinical Impact and Outcomes:
    
    Implementation of the Ottawa SAH Rule has been associated with:
    - Reduced variability in clinical decision-making
    - Improved confidence in ruling out SAH without testing
    - Decreased unnecessary lumbar punctures
    - Maintained safety while standardizing care
    - Enhanced medical-legal protection for clinicians
    
    Special Considerations:
    
    High-Risk Populations:
    - Patients with family history of SAH or known genetic conditions
    - Those with multiple risk factors for aneurysm formation
    - Patients taking anticoagulant medications
    - Individuals with polycystic kidney disease or connective tissue disorders
    
    Clinical Judgment:
    The Ottawa SAH Rule should supplement, not replace, clinical judgment. 
    Clinicians should maintain appropriate suspicion for SAH in high-risk 
    patients and consider imaging even when the rule is negative if clinical 
    concern remains high.
    
    References (Vancouver style):
    1. Perry JJ, Stiell IG, Sivilotti ML, Bullard MJ, Emond M, Symington C, et al. 
    Sensitivity of computed tomography performed within six hours of onset of 
    headache for diagnosis of subarachnoid haemorrhage: prospective cohort study. 
    BMJ. 2011;343:d4277. doi: 10.1136/bmj.d4277.
    2. Perry JJ, Stiell IG, Sivilotti ML, Bullard MJ, Lee JS, Eisenhauer M, et al. 
    High risk clinical characteristics for subarachnoid haemorrhage in patients 
    with acute headache: prospective cohort study. BMJ. 2010;341:c5204. 
    doi: 10.1136/bmj.c5204.
    3. Perry JJ, Sivilotti ML, Sutherland J, Hohl CM, Émond M, Calder LA, et al. 
    Validation of the Ottawa Subarachnoid Hemorrhage Rule in patients with acute 
    headache. CMAJ. 2017;189(45):E1379-E1385. doi: 10.1503/cmaj.170072.
    """
    
    age_40_or_older: Literal["yes", "no"] = Field(
        ...,
        description="Patient age 40 years or older. Advanced age increases risk of aneurysmal SAH due to higher prevalence of intracranial aneurysms and vessel wall degenerative changes",
        example="yes"
    )
    
    neck_pain_stiffness: Literal["yes", "no"] = Field(
        ...,
        description="Complaint of neck pain or neck stiffness. Indicates meningeal irritation from blood in subarachnoid space causing chemical meningitis and reflex muscle spasm",
        example="yes"
    )
    
    witnessed_loss_of_consciousness: Literal["yes", "no"] = Field(
        ...,
        description="Witnessed loss of consciousness at time of headache onset. Suggests acute increase in intracranial pressure and transient global cerebral hypoperfusion from hemorrhage",
        example="no"
    )
    
    onset_during_exertion: Literal["yes", "no"] = Field(
        ...,
        description="Headache onset during exertion, physical activity, or straining (including sexual activity, lifting, coughing). Can trigger aneurysm rupture through acute blood pressure elevation",
        example="no"
    )
    
    thunderclap_headache: Literal["yes", "no"] = Field(
        ...,
        description="Thunderclap headache with instantaneous onset reaching maximum pain intensity immediately. Pathognomonic for sudden vessel rupture and acute intracranial pressure increase",
        example="yes"
    )
    
    limited_neck_flexion: Literal["yes", "no"] = Field(
        ...,
        description="Limited neck flexion on physical examination (inability to touch chin to chest due to pain or passive resistance). Objective sign of meningeal irritation and blood-induced chemical meningitis",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_40_or_older": "yes",
                "neck_pain_stiffness": "yes", 
                "witnessed_loss_of_consciousness": "no",
                "onset_during_exertion": "no",
                "thunderclap_headache": "yes",
                "limited_neck_flexion": "yes"
            }
        }


class OttawaSahRuleResponse(BaseModel):
    """
    Response model for Ottawa Subarachnoid Hemorrhage (SAH) Rule for Headache Evaluation
    
    The Ottawa SAH Rule provides critical guidance for emergency physicians in 
    determining which patients with acute headache require further investigation 
    for subarachnoid hemorrhage, balancing the need for thorough evaluation with 
    resource utilization and patient safety.
    
    Result Interpretation and Clinical Decision Making:
    
    SAH Ruled Out (All Criteria Negative):
    - Interpretation: Subarachnoid hemorrhage can be safely ruled out
    - Sensitivity: 100% for detecting SAH across multiple validation studies
    - Clinical Action: No further testing specifically required for SAH
    - Management: Focus on alternative headache diagnoses and symptomatic treatment
    - Safety: Validated in over 4,000 patients with consistent 100% sensitivity
    - Follow-up: Routine headache management with return precautions
    
    Cannot Rule Out SAH (One or More Criteria Positive):
    - Interpretation: SAH cannot be excluded, further investigation required
    - Specificity: 15.3% (many false positives expected)
    - Clinical Action: Immediate workup with neuroimaging and possible lumbar puncture
    - Management: Urgent evaluation with neurology/neurosurgery consultation
    - Monitoring: Close observation with blood pressure management
    
    Recommended Diagnostic Workup for Positive Results:
    
    Primary Investigation:
    - Non-contrast head CT scan within 6 hours of headache onset
    - CT sensitivity: 99% within 6 hours, 95% within 24 hours, decreases over time
    - Interpretation by experienced radiologist or emergency physician
    - Look for hyperdense areas in basal cisterns, sylvian fissures, or ventricles
    
    Secondary Investigation (if CT negative):
    - Lumbar puncture for xanthochromia and red blood cell count
    - Perform LP 12 hours after headache onset for optimal xanthochromia detection
    - Centrifuge CSF immediately and examine for yellow discoloration
    - Elevated RBC count with failure to clear across tubes suggests SAH
    
    Advanced Imaging (if indicated):
    - CT angiography (CTA) to identify source of bleeding
    - MR angiography (MRA) as alternative to CTA
    - Digital subtraction angiography (DSA) for definitive vascular imaging
    - Consider if SAH confirmed and aneurysm source suspected
    
    Emergency Management Principles:
    
    Initial Stabilization:
    - Airway, breathing, circulation assessment
    - Neurological examination and Glasgow Coma Scale
    - Blood pressure monitoring and careful management
    - Avoid aggressive BP reduction that could worsen cerebral perfusion
    - Target systolic BP <160 mmHg while maintaining adequate perfusion
    
    Symptom Management:
    - Analgesia with acetaminophen or mild opioids
    - Avoid aspirin or NSAIDs due to bleeding risk
    - Anti-emetics for nausea and vomiting
    - Maintain quiet, darkened environment
    
    Monitoring and Consultation:
    - Frequent neurological assessments for deterioration
    - Neurology or neurosurgical consultation for suspected SAH
    - ICU monitoring if SAH confirmed
    - Discuss with interventional neuroradiology for potential treatment
    
    Complications and Warning Signs:
    
    Immediate Complications:
    - Rebleeding (highest risk in first 24 hours)
    - Hydrocephalus from blood blocking CSF drainage
    - Increased intracranial pressure
    - Cerebral edema and herniation
    - Seizures (less common but possible)
    
    Delayed Complications:
    - Vasospasm (peak risk days 4-14 after bleeding)
    - Delayed cerebral ischemia
    - Hyponatremia from SIADH or cerebral salt wasting
    - Cardiac arrhythmias and neurogenic pulmonary edema
    
    Prognosis and Outcomes:
    
    Factors Affecting Prognosis:
    - Glasgow Coma Scale at presentation
    - Amount and location of blood on imaging
    - Patient age and comorbidities
    - Time from onset to treatment
    - Development of complications (rebleeding, vasospasm)
    
    Overall Outcomes:
    - Mortality: 25-50% depending on severity
    - Good functional recovery: 30-60% of survivors
    - Significant disability: 20-30% of survivors
    - Quality of life improvements with early intervention
    
    Prevention and Risk Factor Modification:
    
    Modifiable Risk Factors:
    - Hypertension control
    - Smoking cessation
    - Alcohol moderation
    - Avoidance of stimulant drugs
    - Management of underlying conditions
    
    Genetic Counseling:
    - Consider for patients with family history of SAH
    - Screening recommendations for high-risk families
    - Genetic testing for specific conditions (PKD, connective tissue disorders)
    
    Long-term Management:
    
    Survivor Care:
    - Neurological rehabilitation
    - Cognitive assessment and therapy
    - Depression screening and treatment
    - Return to work and activity planning
    - Long-term follow-up with neurology
    
    Family Education:
    - Recognition of warning signs
    - When to seek emergency care
    - Lifestyle modifications
    - Genetic counseling if appropriate
    
    Quality Assurance and Clinical Governance:
    
    Documentation Requirements:
    - Clear documentation of inclusion/exclusion criteria
    - Detailed neurological examination findings
    - Rationale for testing decisions
    - Follow-up planning and instructions
    
    Performance Monitoring:
    - Track rule utilization and outcomes
    - Monitor for missed SAH cases
    - Assess impact on imaging utilization
    - Regular review of clinical decision-making
    
    Reference: Perry JJ, et al. CMAJ. 2017;189(45):E1379-E1385.
    """
    
    result: str = Field(
        ...,
        description="Ottawa SAH Rule result: 'SAH Ruled Out' if all criteria negative, 'Cannot Rule Out SAH' if any criteria positive",
        example="Cannot Rule Out SAH"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="result"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation with specific management recommendations and emergency protocols",
        example="CANNOT RULE OUT SUBARACHNOID HEMORRHAGE: 4 positive criterion/criteria detected: Age ≥40 years, Neck pain or stiffness, Thunderclap headache, Limited neck flexion. IMMEDIATE ACTION: Further investigation required to exclude SAH. RECOMMENDED WORKUP: Non-contrast head CT scan within 6 hours of headache onset (99% sensitive within 6 hours, 95% sensitive within 24 hours). If CT negative and high clinical suspicion, consider lumbar puncture for xanthochromia and red blood cell count. CONSULTATION: Neurology or neurosurgical consultation if SAH suspected. MONITORING: Close observation, blood pressure control, analgesia as appropriate. SAFETY: The Ottawa SAH Rule has 15.3% specificity, so positive results require careful evaluation but do not confirm SAH diagnosis."
    )
    
    stage: str = Field(
        ...,
        description="Clinical decision category",
        example="Cannot Rule Out SAH"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the clinical decision",
        example="Cannot rule out subarachnoid hemorrhage"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Cannot Rule Out SAH",
                "unit": "result",
                "interpretation": "CANNOT RULE OUT SUBARACHNOID HEMORRHAGE: 4 positive criterion/criteria detected: Age ≥40 years, Neck pain or stiffness, Thunderclap headache, Limited neck flexion. IMMEDIATE ACTION: Further investigation required to exclude SAH. RECOMMENDED WORKUP: Non-contrast head CT scan within 6 hours of headache onset (99% sensitive within 6 hours, 95% sensitive within 24 hours). If CT negative and high clinical suspicion, consider lumbar puncture for xanthochromia and red blood cell count. CONSULTATION: Neurology or neurosurgical consultation if SAH suspected. MONITORING: Close observation, blood pressure control, analgesia as appropriate. SAFETY: The Ottawa SAH Rule has 15.3% specificity, so positive results require careful evaluation but do not confirm SAH diagnosis.",
                "stage": "Cannot Rule Out SAH",
                "stage_description": "Cannot rule out subarachnoid hemorrhage"
            }
        }