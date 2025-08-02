"""
ROSE (Risk Stratification of Syncope in the Emergency Department) Rule Models

Request and response models for ROSE rule syncope risk stratification.

References (Vancouver style):
1. Reed MJ, Newby DE, Coull AJ, Prescott RJ, Jacques KG, Gray AJ. The ROSE (risk 
   stratification of syncope in the emergency department) study. J Am Coll Cardiol. 
   2010 Feb 23;55(8):713-21. doi: 10.1016/j.jacc.2009.09.049.
2. Reed MJ, Mills NL, Weir CJ. Sensitive troponin assay predicts outcome in syncope. 
   Emerg Med J. 2012 Dec;29(12):1001-3. doi: 10.1136/emermed-2011-200456.
3. Colivicchi F, Ammirati F, Melina D, Guido V, Imperoli G, Santini M; OESIL 
   (Osservatorio Epidemiologico sulla Sincope nel Lazio) Study Investigators. 
   Development and prospective validation of a risk stratification system for patients 
   with syncope in the emergency department: the OESIL risk score. Eur Heart J. 
   2003 May;24(9):811-9. doi: 10.1016/s0195-668x(02)00713-0.

CLINICAL BACKGROUND:

Syncope is a common presenting complaint in emergency departments, accounting for 
1-2% of all ED visits and up to 6% of hospital admissions. The challenge for emergency 
physicians lies in distinguishing patients at high risk for serious outcomes who 
require hospitalization from those who can be safely discharged. The ROSE (Risk 
Stratification of Syncope in the Emergency Department) rule was developed to address 
this clinical need through evidence-based risk stratification.

SYNCOPE EVALUATION CHALLENGES:

Diagnostic Uncertainty:
- Broad differential diagnosis including cardiac, neurologic, and vasovagal causes
- Limited diagnostic yield from routine testing in undifferentiated syncope
- High rate of unexplained syncope despite comprehensive evaluation
- Difficulty predicting which patients will experience serious outcomes

Risk Stratification Complexity:
- Wide spectrum of underlying etiologies with varying prognoses
- Need to balance patient safety with resource utilization
- Pressure to avoid unnecessary admissions while preventing missed diagnoses
- Limited time and resources in busy emergency department settings

Economic Considerations:
- High cost of inpatient evaluation and monitoring
- Significant healthcare resource utilization for low-yield workups
- Need for efficient decision-making tools to optimize resource allocation
- Potential for reduced length of stay and improved patient flow

ROSE RULE DEVELOPMENT:

Study Design and Population:
The ROSE rule was derived from a prospective observational study of 550 patients 
presenting with syncope to emergency departments. The derivation cohort included 
adults ≥16 years old with syncope defined as transient loss of consciousness with 
spontaneous recovery. Patients were followed for 1 month to identify serious outcomes.

Primary Outcome Definition:
Serious outcomes included death, myocardial infarction, arrhythmia requiring 
intervention, structural heart disease diagnosis, pulmonary embolism, stroke, 
subarachnoid hemorrhage, significant hemorrhage requiring transfusion, or any 
condition requiring immediate intervention to prevent death or serious morbidity.

Statistical Development:
Multivariate logistic regression was used to identify independent predictors of 
serious outcomes. The final model included 7 variables that could be readily 
assessed in the emergency department setting without specialized testing or 
prolonged observation periods.

ROSE RULE CRITERIA:

The ROSE rule identifies HIGH RISK patients when ANY of the following criteria are present:

1. B-type Natriuretic Peptide (BNP) ≥300 pg/ml:
   - Strongest single predictor with odds ratio of 7.3
   - Reflects cardiac stress and volume overload
   - Associated with 36% of serious cardiovascular outcomes
   - Accounts for 89% of deaths in the study population
   - Requires point-of-care testing availability

2. Bradycardia ≤50 bpm in ED or Pre-hospital:
   - May indicate sick sinus syndrome or conduction abnormalities
   - Includes heart rate documented by EMS or ED staff
   - Reflects potential underlying cardiac conduction disease
   - Associated with increased risk of cardiac events

3. Positive Fecal Occult Blood Test:
   - Highest odds ratio (13.2) among all criteria
   - Indicates potential gastrointestinal bleeding as cause of syncope
   - Requires rectal examination when GI bleeding suspected
   - May reveal occult bleeding contributing to hypotension and syncope

4. Anemia (Hemoglobin ≤90 g/l or ≤9.0 g/dl):
   - Corresponds to WHO definition of severe anemia
   - May contribute to decreased oxygen delivery and syncope
   - Could indicate underlying bleeding or chronic disease
   - Associated with increased mortality risk

5. Chest Pain Associated with Syncope:
   - Suggests potential cardiac etiology
   - May indicate acute coronary syndrome or aortic dissection
   - Temporal association with syncope episode important
   - Warrants cardiac evaluation and monitoring

6. Q Wave on ECG (not in lead III):
   - Indicates prior myocardial infarction or structural heart disease
   - Lead III Q waves excluded due to positional artifacts
   - Suggests underlying coronary artery disease
   - Associated with increased risk of cardiac events

7. Oxygen Saturation ≤94% on Room Air:
   - May indicate pulmonary embolism or cardiac causes
   - Reflects impaired gas exchange or cardiac output
   - Must be measured on room air for accuracy
   - Associated with serious cardiopulmonary conditions

VALIDATION AND PERFORMANCE:

Original Validation Results:
- Sensitivity: 87.2% for identifying patients with serious outcomes
- Specificity: 65.5% for correctly identifying low-risk patients
- Negative Predictive Value: 98.5% when no criteria present
- Positive Predictive Value: 27.9% when criteria present

Clinical Outcomes:
- 1-month serious outcomes occurred in 7.1-7.3% of study patients
- Death rate was 1.6% in the validation cohort
- Cardiovascular events comprised the majority of serious outcomes
- Rule performed consistently across derivation and validation cohorts

Limitations and Considerations:
- Requires BNP testing which may not be available in all emergency departments
- Performance may vary in different healthcare systems and populations
- Does not replace clinical judgment for other indications for admission
- Validation studies have shown variable performance in different settings

CLINICAL APPLICATIONS:

Emergency Department Decision Making:

High-Risk Patients (Positive ROSE Criteria):
- Strong consideration for hospital admission
- Cardiac monitoring and serial cardiac biomarkers
- Echocardiography to assess structural heart disease
- Consultation with cardiology or electrophysiology as indicated
- Additional testing based on specific risk factors present

Low-Risk Patients (Negative ROSE Criteria):
- May be considered for discharge with appropriate follow-up
- Outpatient cardiology evaluation within reasonable timeframe
- Primary care follow-up within 24-48 hours
- Patient education about return precautions and warning signs
- Consideration of outpatient monitoring if clinically indicated

Complementary Evaluation:

Routine ED Assessment:
- Complete history including medication review and family history
- Physical examination including orthostatic vital signs
- 12-lead ECG with rhythm strip
- Basic laboratory studies including complete blood count and chemistry panel
- Consideration of additional testing based on clinical presentation

Additional Risk Stratification:
- Use in conjunction with other validated syncope rules when appropriate
- Consider Canadian Syncope Risk Score or San Francisco Syncope Rule
- Clinical gestalt remains important for overall assessment
- Integration with hospital admission criteria and resource availability

IMPLEMENTATION CONSIDERATIONS:

Resource Requirements:
- Point-of-care BNP testing capability
- Standardized assessment protocols for all criteria
- Staff training on rule application and interpretation
- Documentation systems to support decision-making

Quality Assurance:
- Regular monitoring of rule adherence and outcomes
- Validation of performance in local patient population
- Feedback mechanisms for continuous improvement
- Integration with electronic health record systems

Patient Safety:
- Clear protocols for high-risk patient management
- Backup evaluation pathways for clinical concerns beyond rule criteria
- Communication plans for disposition decisions
- Follow-up mechanisms for discharged patients

The ROSE rule provides a structured, evidence-based approach to syncope risk 
stratification in the emergency department, helping clinicians make informed 
decisions about disposition while optimizing resource utilization and patient safety.
"""

from pydantic import BaseModel, Field
from typing import Literal


class RoseRuleRequest(BaseModel):
    """
    Request model for ROSE (Risk Stratification of Syncope in the Emergency Department) Rule
    
    The ROSE rule predicts 1-month serious outcome or death in patients presenting 
    with syncope to the emergency department. Any positive criterion indicates HIGH RISK 
    requiring strong consideration for admission and further workup.
    
    ROSE Rule Criteria (ANY positive = HIGH RISK):
    1. BNP level ≥300 pg/ml (strongest predictor, OR 7.3)
    2. Bradycardia ≤50 bpm in ED or pre-hospital
    3. Positive fecal occult blood test (highest OR 13.2)
    4. Anemia with hemoglobin ≤90 g/l (≤9.0 g/dl)
    5. Chest pain associated with syncope
    6. Q wave on ECG (excluding lead III)
    7. Oxygen saturation ≤94% on room air
    
    Clinical Context:
    Syncope accounts for 1-2% of ED visits with significant diagnostic uncertainty. 
    The ROSE rule helps distinguish high-risk patients requiring hospitalization 
    from those who can be safely discharged. Validation studies showed 87.2% 
    sensitivity and 98.5% negative predictive value for serious outcomes.
    
    Serious Outcomes Include:
    - Death, myocardial infarction, arrhythmia requiring intervention
    - Structural heart disease diagnosis, pulmonary embolism
    - Stroke, subarachnoid hemorrhage, significant hemorrhage
    - Any condition requiring immediate intervention to prevent serious morbidity
    
    References (Vancouver style):
    1. Reed MJ, Newby DE, Coull AJ, Prescott RJ, Jacques KG, Gray AJ. The ROSE (risk 
       stratification of syncope in the emergency department) study. J Am Coll Cardiol. 
       2010 Feb 23;55(8):713-21. doi: 10.1016/j.jacc.2009.09.049.
    2. Reed MJ, Mills NL, Weir CJ. Sensitive troponin assay predicts outcome in syncope. 
       Emerg Med J. 2012 Dec;29(12):1001-3. doi: 10.1136/emermed-2011-200456.
    3. Colivicchi F, Ammirati F, Melina D, Guido V, Imperoli G, Santini M; OESIL Study 
       Investigators. Development and prospective validation of a risk stratification 
       system for patients with syncope in the emergency department: the OESIL risk score. 
       Eur Heart J. 2003 May;24(9):811-9. doi: 10.1016/s0195-668x(02)00713-0.
    """
    
    bnp_level: Literal["yes", "no"] = Field(
        ...,
        description="B-type natriuretic peptide (BNP) level ≥300 pg/ml. BNP is the strongest "
                   "single predictor in the ROSE rule with an odds ratio of 7.3 for serious outcomes. "
                   "Elevated BNP reflects cardiac stress and volume overload, and was associated with "
                   "36% of serious cardiovascular outcomes and 89% of deaths in the original study. "
                   "This criterion requires point-of-care BNP testing capability in the emergency "
                   "department. Normal BNP levels (<300 pg/ml) suggest lower risk for cardiac causes "
                   "of syncope, while elevated levels warrant cardiac evaluation and monitoring.",
        example="no"
    )
    
    bradycardia: Literal["yes", "no"] = Field(
        ...,
        description="Bradycardia with heart rate ≤50 bpm documented in the emergency department "
                   "or by pre-hospital emergency medical services. This criterion may indicate "
                   "underlying cardiac conduction abnormalities such as sick sinus syndrome, "
                   "atrioventricular blocks, or medication effects. Bradycardia can contribute to "
                   "decreased cardiac output and syncope, particularly in elderly patients or those "
                   "with underlying heart disease. The heart rate threshold of 50 bpm was chosen "
                   "based on clinical significance and association with serious outcomes in the "
                   "derivation study. Documentation by EMS is included as pre-hospital bradycardia "
                   "may resolve by ED arrival but remains clinically significant.",
        example="no"
    )
    
    fecal_occult_blood: Literal["yes", "no"] = Field(
        ...,
        description="Positive fecal occult blood test on rectal examination (if performed when "
                   "gastrointestinal bleeding is suspected). This criterion has the highest odds "
                   "ratio (13.2) among all ROSE rule variables, indicating strong association with "
                   "serious outcomes. Occult gastrointestinal bleeding may contribute to anemia, "
                   "hypovolemia, and subsequent syncope. Rectal examination with fecal occult blood "
                   "testing should be considered when clinical suspicion for GI bleeding exists "
                   "based on history, physical examination, or laboratory findings. Positive results "
                   "warrant gastroenterology consultation and appropriate GI evaluation.",
        example="no"
    )
    
    anemia: Literal["yes", "no"] = Field(
        ...,
        description="Anemia with hemoglobin level ≤90 g/l (≤9.0 g/dl). This threshold corresponds "
                   "to the World Health Organization definition of severe anemia and is associated "
                   "with increased mortality risk. Severe anemia can contribute to decreased oxygen "
                   "delivery, compensatory tachycardia, and eventual syncope when cardiac output "
                   "cannot be maintained. Anemia may result from acute bleeding, chronic disease, "
                   "nutritional deficiencies, or hematologic disorders. Patients with severe anemia "
                   "require investigation of underlying cause and may need blood transfusion or "
                   "other immediate interventions to address the anemia and prevent further complications.",
        example="no"
    )
    
    chest_pain: Literal["yes", "no"] = Field(
        ...,
        description="Chest pain associated temporally with the syncope episode. This criterion "
                   "suggests potential cardiac etiology for syncope including acute coronary syndrome, "
                   "aortic dissection, pulmonary embolism, or other cardiopulmonary conditions. "
                   "The chest pain should be related to the syncopal episode rather than chronic "
                   "or unrelated pain. Chest pain with syncope warrants cardiac evaluation including "
                   "serial cardiac biomarkers, echocardiography, and consideration of advanced "
                   "cardiac imaging. The combination of chest pain and syncope significantly increases "
                   "the likelihood of serious cardiac pathology requiring immediate evaluation and "
                   "treatment.",
        example="no"
    )
    
    q_wave_ecg: Literal["yes", "no"] = Field(
        ...,
        description="Pathologic Q wave present on 12-lead ECG (excluding lead III). Q waves "
                   "typically indicate prior myocardial infarction or structural heart disease "
                   "and suggest underlying coronary artery disease. Lead III Q waves are specifically "
                   "excluded due to potential positional artifacts and lower clinical significance. "
                   "Pathologic Q waves are defined as ≥0.04 seconds in duration and ≥25% of the "
                   "R wave amplitude in the same lead. The presence of Q waves indicates increased "
                   "risk for cardiac arrhythmias and events. Patients with Q waves on ECG warrant "
                   "cardiac evaluation including echocardiography and possible stress testing or "
                   "cardiac catheterization based on clinical presentation.",
        example="no"
    )
    
    oxygen_saturation: Literal["yes", "no"] = Field(
        ...,
        description="Oxygen saturation ≤94% measured on room air. This criterion may indicate "
                   "underlying cardiopulmonary pathology such as pulmonary embolism, heart failure, "
                   "pneumonia, or other conditions affecting gas exchange. The oxygen saturation "
                   "must be measured on room air (without supplemental oxygen) for accurate assessment. "
                   "Hypoxemia in the setting of syncope suggests serious underlying pathology requiring "
                   "immediate evaluation and treatment. Causes may include pulmonary embolism (especially "
                   "relevant in syncope), cardiac causes leading to poor perfusion, or primary "
                   "pulmonary pathology. Patients with hypoxemia require chest imaging, arterial "
                   "blood gas analysis, and evaluation for thromboembolic disease.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "bnp_level": "no",
                "bradycardia": "no",
                "fecal_occult_blood": "no",
                "anemia": "no",
                "chest_pain": "no",
                "q_wave_ecg": "no",
                "oxygen_saturation": "no"
            }
        }


class RoseRuleResponse(BaseModel):
    """
    Response model for ROSE (Risk Stratification of Syncope in the Emergency Department) Rule
    
    The ROSE rule provides evidence-based risk stratification for emergency department 
    patients presenting with syncope, helping clinicians make informed decisions about 
    disposition, further workup, and resource allocation.
    
    Risk Stratification Results:
    
    LOW RISK (No ROSE Criteria Present):
    - Negative predictive value: 98.5% for serious outcomes
    - May consider discharge with appropriate follow-up
    - Outpatient cardiology evaluation within reasonable timeframe
    - Primary care follow-up within 24-48 hours recommended
    - Patient education about return precautions essential
    
    HIGH RISK (Any ROSE Criteria Present):
    - Strong consideration for hospital admission warranted
    - Further workup and cardiac monitoring recommended
    - Risk of serious outcomes significantly increased
    - Evaluation based on specific positive criteria
    - Multidisciplinary approach often beneficial
    
    Clinical Management by Risk Level:
    
    Low-Risk Management:
    1. Discharge Planning:
       - Ensure hemodynamic stability and symptom resolution
       - Arrange outpatient cardiology follow-up within 1-2 weeks
       - Primary care appointment within 24-48 hours
       - Patient education about warning signs and return precautions
       - Consider outpatient event monitoring if clinically indicated
    
    2. Follow-up Instructions:
       - Return immediately for recurrent syncope, chest pain, or dyspnea
       - Avoid driving until cleared by cardiology or primary care
       - Medication review to identify potential contributors to syncope
       - Lifestyle modifications including adequate hydration and gradual position changes
    
    High-Risk Management:
    1. Initial Stabilization:
       - Continuous cardiac monitoring in emergency department
       - IV access and hemodynamic monitoring
       - Serial cardiac biomarkers (troponin, CK-MB)
       - Chest X-ray and additional imaging as clinically indicated
    
    2. Specific Workup Based on Positive Criteria:
       - Elevated BNP: Echocardiography, heart failure evaluation, cardiology consultation
       - Bradycardia: Rhythm monitoring, electrophysiology consultation if indicated
       - Occult GI bleeding: GI consultation, upper/lower endoscopy consideration
       - Anemia: CBC with reticulocyte count, iron studies, hematology consultation
       - Chest pain: Acute coronary syndrome protocol, cardiac catheterization consideration
       - Q waves: Echocardiography, stress testing, cardiology consultation
       - Hypoxemia: CT pulmonary angiogram, arterial blood gas, pulmonary consultation
    
    3. Admission Considerations:
       - Telemetry monitoring for cardiac rhythm assessment
       - Serial cardiac biomarkers every 6-8 hours
       - Echocardiography within 24 hours if not done emergently
       - Consultations based on specific abnormalities identified
       - Medication reconciliation and optimization
    
    4. Advanced Evaluation Options:
       - Electrophysiology study for patients with conduction abnormalities
       - Stress testing for patients with suspected coronary artery disease
       - Implantable loop recorder for recurrent unexplained syncope
       - Tilt table testing for suspected vasovagal syncope in appropriate candidates
    
    Performance Characteristics and Limitations:
    
    Validation Results:
    - Sensitivity: 87.2% (identifies most patients with serious outcomes)
    - Specificity: 65.5% (correctly identifies low-risk patients)
    - Negative Predictive Value: 98.5% (very reliable when negative)
    - Positive Predictive Value: 27.9% (moderate when positive)
    
    Clinical Limitations:
    - Requires BNP testing which may not be available in all emergency departments
    - Performance may vary across different healthcare systems and populations
    - Does not replace clinical judgment for other admission indications
    - Some criteria (fecal occult blood) may not be routinely performed
    - Rule developed in specific population and may not generalize universally
    
    Integration with Clinical Care:
    - Use as adjunct to, not replacement for, clinical assessment
    - Consider other validated syncope risk stratification tools
    - Account for patient-specific factors and comorbidities
    - Ensure appropriate follow-up regardless of risk stratification result
    - Document rationale for disposition decisions clearly
    
    Quality Assurance Considerations:
    - Regular monitoring of rule implementation and outcomes
    - Staff training on appropriate application and interpretation
    - Integration with electronic health record systems
    - Feedback mechanisms for continuous quality improvement
    - Validation of performance in local patient population
    
    The ROSE rule represents a valuable tool for emergency physicians managing 
    syncope patients, providing structured risk assessment while maintaining 
    flexibility for clinical judgment and individual patient factors.
    
    Reference: Reed MJ, et al. J Am Coll Cardiol. 2010;55(8):713-21.
    """
    
    result: str = Field(
        ...,
        description="ROSE rule risk assessment result: 'High Risk' if any criteria present, 'Low Risk' if no criteria present",
        example="Low Risk"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk assessment",
        example="risk level"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with risk-based management recommendations and disposition guidance",
        example="Low risk for 1-month serious outcome or death. Patient may be considered for discharge with appropriate follow-up. The ROSE rule has a negative predictive value of 98.5% when no criteria are present. Consider outpatient cardiology follow-up, primary care follow-up within 24-48 hours, and patient education about return precautions. Ensure no other clinical concerns that would warrant admission independent of syncope risk stratification."
    )
    
    stage: str = Field(
        ...,
        description="Risk level classification (Low Risk or High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="No ROSE criteria present"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Low Risk",
                "unit": "risk level",
                "interpretation": "Low risk for 1-month serious outcome or death. Patient may be considered for discharge with appropriate follow-up. The ROSE rule has a negative predictive value of 98.5% when no criteria are present. Consider outpatient cardiology follow-up, primary care follow-up within 24-48 hours, and patient education about return precautions. Ensure no other clinical concerns that would warrant admission independent of syncope risk stratification.",
                "stage": "Low Risk",
                "stage_description": "No ROSE criteria present"
            }
        }