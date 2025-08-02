"""
Subtle Anterior STEMI Calculator (4-Variable) Models

Request and response models for Subtle Anterior STEMI 4-Variable calculation.

References (Vancouver style):
1. Driver BE, Khalil A, Henry T, Kazmi F, Adil A, Smith SW. A new 4-variable 
   formula to differentiate normal variant ST segment elevation in V2-V4 (early 
   repolarization) from subtle left anterior descending coronary occlusion – 
   Adding QRS amplitude of V2 improves the model. J Electrocardiol. 2017 
   Nov-Dec;50(6):836-843. doi: 10.1016/j.jelectrocard.2017.08.005.
2. Smith SW, Khalil A, Henry TD, Rosas M, Chang RJ, Hocken C, et al. 
   Electrocardiographic differentiation of early repolarization from subtle 
   anterior ST-elevation myocardial infarction. Ann Emerg Med. 2012 
   Jul;60(1):45-56.e2. doi: 10.1016/j.annemergmed.2012.02.015.

The Subtle Anterior STEMI Calculator (4-Variable) is a clinical decision tool 
developed by Dr. Stephen Smith to differentiate normal variant ST elevation 
(benign early repolarization) from subtle anterior STEMI that may require urgent 
percutaneous coronary intervention. This enhanced 4-variable version improves 
upon the original 3-variable formula by adding QRS amplitude in lead V2.
"""

from pydantic import BaseModel, Field


class SubtleAnteriorStemi4VariableRequest(BaseModel):
    """
    Request model for Subtle Anterior STEMI Calculator (4-Variable)
    
    The Subtle Anterior STEMI Calculator (4-Variable) is an evidence-based clinical 
    decision tool designed to help emergency physicians and cardiologists distinguish 
    between normal variant ST elevation (benign early repolarization) and subtle 
    anterior ST-elevation myocardial infarction (STEMI) that may require urgent 
    intervention.
    
    Clinical Context and Development:
    
    Historical Background:
    Developed by Dr. Stephen Smith and colleagues, this calculator addresses a critical 
    clinical challenge in emergency cardiology. Some patients present with chest pain 
    and subtle ECG changes that are non-diagnostic for STEMI but may still represent 
    100% coronary artery occlusion requiring immediate intervention. Missing these 
    subtle anterior STEMIs can result in significant morbidity and mortality, while 
    false positives lead to unnecessary invasive procedures and resource utilization.
    
    The original research by Smith et al. (2012) established the foundation for 
    electrocardiographic differentiation, and Driver et al. (2017) enhanced the 
    model by adding QRS amplitude in lead V2 as the fourth variable, improving 
    diagnostic accuracy from the original 3-variable formula.
    
    Clinical Problem Addressed:
    Traditional STEMI criteria may miss subtle anterior wall myocardial infarctions, 
    particularly those involving the left anterior descending (LAD) artery. Benign 
    early repolarization (BER) is a common normal variant that can mimic STEMI, 
    especially in young patients, creating diagnostic uncertainty. This calculator 
    provides objective criteria to guide clinical decision-making in these challenging 
    cases.
    
    Prerequisites for Calculator Use:
    
    Inclusion Criteria:
    - Patient presenting with chest pain or symptoms suggestive of acute coronary syndrome
    - ECG demonstrates ≥1 mm ST elevation in ≥1 of the precordial leads V2, V3, or V4
    - ECG appearance is non-diagnostic but suspicious for anterior MI
    - Clinical uncertainty about whether ST elevation represents BER or subtle STEMI
    
    Exclusion Criteria (DO NOT use calculator if any present):
    - Non-concave ST elevation (suggests obvious STEMI)
    - Inferior reciprocal changes (ST depression in leads II, III, aVF, or V6)
    - Anterior ST depression (reciprocal changes)
    - Q waves present in any of leads V2, V3, or V4
    - T wave inversion present in any lead from V2 to V6
    - Obvious STEMI by standard criteria
    - Bundle branch blocks or paced rhythm
    - Previous MI with known ECG changes
    
    ECG Parameter Measurement Guidelines:
    
    QTc Interval (Bazett-corrected):
    - Measure the QT interval from the beginning of the QRS complex to the end of the T wave
    - Use the most clearly defined QT interval, typically in leads II or V5
    - Apply Bazett's correction formula: QTc = QT / √RR interval
    - Normal range typically 300-450 ms (males) and 300-470 ms (females)
    - Prolonged QTc may support STEMI diagnosis as ischemia can prolong repolarization
    
    QRS Amplitude in Lead V2:
    - Measure the total height of the QRS complex in lead V2
    - Measure from the lowest point (nadir of S wave) to the highest point (peak of R wave)
    - If no S wave is present, measure from baseline to R wave peak
    - Typical range: 5-20 mm in healthy individuals
    - Lower QRS amplitude may suggest anterior wall ischemia affecting ventricular depolarization
    
    R Wave Amplitude in Lead V4:
    - Measure the height of the R wave in lead V4 from baseline to peak
    - Do not include any S wave depth in this measurement
    - Typical range: 8-25 mm in healthy individuals
    - Reduced R wave amplitude may indicate anterior wall myocardial injury
    - Lead V4 overlies the anterior-lateral wall supplied by the LAD
    
    ST Elevation in Lead V3 (60 ms after J point):
    - Identify the J point (junction between QRS complex and ST segment)
    - Measure ST elevation exactly 60 milliseconds (1.5 small boxes at 25 mm/s) after the J point
    - Do not measure at the J point itself, as this may be inaccurate
    - Measure from the baseline (isoelectric line) to the ST segment level
    - Normal individuals may have up to 1-2 mm of ST elevation, especially in young males
    - The timing of 60 ms after J point improves specificity for ischemic changes
    
    Clinical Application and Workflow:
    
    Patient Assessment Protocol:
    1. Obtain 12-lead ECG in all patients with chest pain
    2. Identify patients with ST elevation in V2-V4 who don't meet obvious STEMI criteria
    3. Verify absence of exclusion criteria listed above
    4. Carefully measure the four required ECG parameters
    5. Input measurements into the calculator
    6. Interpret results in clinical context
    7. Consider serial ECGs and biomarkers regardless of calculator result
    
    Interpretation Framework:
    - Score <18.2: Likely benign early repolarization (sensitivity 83.3%, specificity 87.7%)
    - Score ≥18.2: Likely subtle anterior STEMI requiring urgent intervention
    - Clinical correlation remains essential regardless of calculator result
    - Consider cardiology consultation for scores near the threshold (17-19)
    
    Diagnostic Performance:
    The 4-variable formula demonstrates superior performance compared to clinical 
    judgment alone and the original 3-variable version:
    - Sensitivity: 83.3% for detecting subtle anterior STEMI
    - Specificity: 87.7% for ruling out STEMI in BER cases
    - Overall diagnostic accuracy: 85.9%
    - Positive predictive value varies with prevalence of disease
    - Negative predictive value: High in appropriate clinical context
    
    Clinical Impact and Outcomes:
    
    Benefits of Accurate Identification:
    - Early recognition of subtle STEMI enables timely percutaneous coronary intervention
    - Reduced door-to-balloon times for true STEMI patients
    - Decreased false positive catheterization laboratory activations
    - Improved resource utilization and cost-effectiveness
    - Enhanced patient safety through appropriate triage decisions
    
    Consequences of Missed Diagnosis:
    - Delayed reperfusion therapy leading to larger infarct size
    - Increased risk of mechanical complications (rupture, papillary muscle dysfunction)
    - Higher mortality and morbidity rates
    - Potential for cardiogenic shock development
    - Long-term left ventricular dysfunction and heart failure
    
    Special Clinical Considerations:
    
    Age and Gender Factors:
    - Benign early repolarization is more common in young males, particularly athletes
    - Consider patient demographics when interpreting borderline results
    - Elderly patients with BER pattern are less common
    - Women may have different normal ECG parameters affecting calculation
    
    Comorbidity Considerations:
    - Previous MI may alter baseline ECG appearance
    - Cardiomyopathy can affect QRS morphology and amplitude
    - Electrolyte abnormalities may influence QTc interval
    - Medications (antiarrhythmics, psychotropics) can prolong QTc
    
    Serial Assessment Strategy:
    - Obtain serial ECGs every 15-30 minutes if clinical suspicion persists
    - Monitor for evolution of ST segments or new Q wave development
    - Consider troponin levels, though may be initially normal in acute STEMI
    - Reassess if symptoms worsen or new clinical findings develop
    
    Integration with Other Clinical Tools:
    - Combine with clinical risk scores (TIMI, GRACE)
    - Consider echocardiography to assess wall motion abnormalities
    - Use in conjunction with point-of-care troponin when available
    - Complement with clinical assessment of chest pain characteristics
    
    Quality Assurance and Training:
    
    ECG Measurement Accuracy:
    - Ensure high-quality ECG recordings with minimal artifact
    - Use consistent measurement techniques across providers
    - Consider digital calipers for precise measurements
    - Validate measurements with colleagues when uncertain
    
    Provider Education:
    - Train emergency physicians and cardiologists on proper use
    - Regular case-based discussions to reinforce learning
    - Audit outcomes to ensure appropriate utilization
    - Update protocols based on emerging evidence
    
    Limitations and Cautions:
    
    Calculator Limitations:
    - Does not replace clinical judgment and comprehensive assessment
    - May be less accurate in patients with baseline ECG abnormalities
    - Limited validation in certain populations (elderly, multiple comorbidities)
    - Requires accurate ECG measurement technique for reliability
    
    Clinical Cautions:
    - Always consider clinical context and symptom severity
    - Do not delay treatment if high clinical suspicion despite negative score
    - Consider alternative diagnoses (aortic dissection, pulmonary embolism)
    - Maintain low threshold for cardiology consultation in uncertain cases
    
    The Subtle Anterior STEMI Calculator (4-Variable) represents a significant 
    advancement in emergency cardiac care, providing objective criteria to guide 
    clinical decision-making in challenging cases of chest pain with non-diagnostic 
    ECG changes. When used appropriately within the clinical context, it can 
    improve patient outcomes by facilitating timely recognition of subtle anterior 
    STEMIs while reducing unnecessary invasive procedures for benign conditions.
    
    References (Vancouver style):
    1. Driver BE, Khalil A, Henry T, Kazmi F, Adil A, Smith SW. A new 4-variable 
       formula to differentiate normal variant ST segment elevation in V2-V4 (early 
       repolarization) from subtle left anterior descending coronary occlusion – 
       Adding QRS amplitude of V2 improves the model. J Electrocardiol. 2017 
       Nov-Dec;50(6):836-843. doi: 10.1016/j.jelectrocard.2017.08.005.
    2. Smith SW, Khalil A, Henry TD, Rosas M, Chang RJ, Hocken C, et al. 
       Electrocardiographic differentiation of early repolarization from subtle 
       anterior ST-elevation myocardial infarction. Ann Emerg Med. 2012 
       Jul;60(1):45-56.e2. doi: 10.1016/j.annemergmed.2012.02.015.
    """
    
    qtc_interval: float = Field(
        ...,
        ge=300,
        le=700,
        description="Bazett-corrected QT interval measured on 12-lead ECG. Calculate using QTc = QT / √RR interval. "
                   "Measure QT from beginning of QRS to end of T wave in the clearest lead (typically II or V5). "
                   "Prolonged QTc may suggest ischemic changes affecting ventricular repolarization. "
                   "Normal range: 300-450 ms (males), 300-470 ms (females).",
        example=420.5
    )
    
    qrs_amplitude_v2: float = Field(
        ...,
        ge=0,
        le=50,
        description="Total QRS amplitude (height) in lead V2 measured in millimeters. Measure from the lowest "
                   "point (nadir of S wave if present) to the highest point (peak of R wave). If no S wave, "
                   "measure from baseline to R wave peak. Lead V2 overlies the interventricular septum. "
                   "Reduced amplitude may indicate anterior wall ischemia. Typical range: 5-20 mm.",
        example=12.5
    )
    
    r_wave_amplitude_v4: float = Field(
        ...,
        ge=0,
        le=50,
        description="R wave amplitude (height) in lead V4 measured from baseline to peak of R wave in millimeters. "
                   "Do not include S wave depth in this measurement. Lead V4 overlies the anterior-lateral wall "
                   "supplied by the left anterior descending artery. Reduced R wave amplitude may indicate "
                   "anterior wall myocardial injury. Typical range: 8-25 mm.",
        example=15.0
    )
    
    st_elevation_v3: float = Field(
        ...,
        ge=0,
        le=10,
        description="ST segment elevation measured exactly 60 milliseconds (1.5 small boxes at 25 mm/s paper speed) "
                   "after the J point in lead V3, expressed in millimeters. Identify the J point (junction between "
                   "QRS and ST segment), then measure 60 ms later from baseline to ST segment level. This timing "
                   "improves specificity for ischemic changes. Normal individuals may have 1-2 mm elevation.",
        example=1.5
    )
    
    class Config:
        schema_extra = {
            "example": {
                "qtc_interval": 420.5,
                "qrs_amplitude_v2": 12.5,
                "r_wave_amplitude_v4": 15.0,
                "st_elevation_v3": 1.5
            }
        }


class SubtleAnteriorStemi4VariableResponse(BaseModel):
    """
    Response model for Subtle Anterior STEMI Calculator (4-Variable)
    
    The Subtle Anterior STEMI Calculator (4-Variable) provides a quantitative score 
    to differentiate normal variant ST elevation (benign early repolarization) from 
    subtle anterior STEMI that may require urgent percutaneous coronary intervention. 
    The calculator uses four ECG parameters to generate a score with established 
    diagnostic thresholds.
    
    Score Interpretation and Clinical Decision-Making:
    
    Diagnostic Threshold: 18.2 points
    This threshold was derived from receiver operating characteristic (ROC) curve 
    analysis to optimize the balance between sensitivity and specificity for detecting 
    subtle anterior STEMI while minimizing false positive results.
    
    Low Risk Category (Score <18.2):
    
    Clinical Interpretation:
    - Likely represents benign early repolarization rather than acute coronary occlusion
    - Low probability of anterior STEMI requiring urgent intervention
    - Suggests normal variant ST elevation commonly seen in young, healthy individuals
    
    Diagnostic Performance:
    - High specificity (87.7%) for ruling out STEMI
    - Negative predictive value is excellent in appropriate clinical context
    - Reduces unnecessary catheterization laboratory activations
    
    Recommended Management:
    - Continue standard chest pain evaluation protocol
    - Obtain serial ECGs every 15-30 minutes to monitor for changes
    - Check cardiac biomarkers (troponin) per institutional protocols
    - Consider stress testing or CT coronary angiography for ongoing symptoms
    - Discharge planning appropriate if clinical picture remains stable
    - Patient education on when to return for evaluation
    
    Clinical Cautions for Low Scores:
    - Do not ignore high clinical suspicion based solely on calculator result
    - Consider alternative diagnoses (aortic dissection, pulmonary embolism)
    - Serial assessment remains important even with low scores
    - Maintain vigilance for symptom progression or ECG evolution
    
    High Risk Category (Score ≥18.2):
    
    Clinical Interpretation:
    - High probability of subtle anterior STEMI with likely LAD occlusion
    - May represent 100% coronary artery occlusion despite subtle ECG changes
    - Urgent intervention may significantly improve patient outcomes
    - Time-sensitive condition requiring immediate action
    
    Diagnostic Performance:
    - Good sensitivity (83.3%) for detecting subtle anterior STEMI
    - Positive predictive value varies with patient population and prevalence
    - Superior to clinical judgment alone in identifying subtle cases
    
    Recommended Management:
    - Immediate cardiology consultation for urgent evaluation
    - Consider emergent cardiac catheterization and primary PCI
    - Activate catheterization laboratory if available and appropriate
    - Dual antiplatelet therapy (aspirin + P2Y12 inhibitor) unless contraindicated
    - Anticoagulation with heparin or bivalirudin per protocol
    - Serial ECGs and continuous cardiac monitoring
    - Rapid transport to PCI-capable facility if not immediately available
    
    Advanced Management Considerations:
    - Door-to-balloon time goal <90 minutes for primary PCI
    - Consider fibrinolytic therapy if PCI not available within appropriate timeframe
    - Monitor for mechanical complications (papillary muscle rupture, VSD)
    - Assess for cardiogenic shock and need for hemodynamic support
    - Post-PCI care including statin therapy and cardiac rehabilitation referral
    
    Borderline Scores (17-19 range):
    
    Clinical Approach:
    - Heightened clinical vigilance and frequent reassessment
    - Strong consideration for cardiology consultation
    - Serial ECGs every 10-15 minutes for dynamic changes
    - Point-of-care troponin if available
    - Echocardiography to assess regional wall motion
    - Low threshold for proceeding with cardiac catheterization
    
    Quality Assurance and Outcome Monitoring:
    
    Performance Metrics:
    - Track door-to-balloon times for confirmed STEMI cases
    - Monitor false positive catheterization laboratory activations
    - Assess patient outcomes and major adverse cardiac events
    - Regular review of missed diagnoses and system improvements
    
    Educational Components:
    - Case-based discussions for challenging interpretations
    - Regular updates on evidence-based practice
    - Interdisciplinary team communication protocols
    - Continuous quality improvement initiatives
    
    Integration with Clinical Workflow:
    
    Emergency Department Protocols:
    - Incorporate calculator into chest pain evaluation pathways
    - Standardize ECG measurement techniques across providers
    - Establish clear consultation and activation criteria
    - Document decision-making rationale in medical record
    
    Cardiology Consultation Guidelines:
    - Provide complete clinical context with calculator results
    - Include serial ECG changes and symptom progression
    - Communicate urgency level based on score and clinical assessment
    - Collaborative decision-making for borderline cases
    
    Long-term Follow-up Considerations:
    
    For Patients with Low Scores:
    - Outpatient cardiology follow-up as clinically indicated
    - Risk factor modification and lifestyle counseling
    - Consider functional testing if symptoms persist
    - Patient education on cardiac risk factors
    
    For Patients with High Scores (Confirmed STEMI):
    - Comprehensive post-MI care including medication optimization
    - Cardiac rehabilitation referral and lifestyle modification
    - Regular follow-up for heart failure prevention
    - Secondary prevention strategies and risk factor management
    
    Research and Future Directions:
    
    Ongoing Validation:
    - External validation in diverse patient populations
    - Assessment of calculator performance in different healthcare settings
    - Evaluation of impact on clinical outcomes and resource utilization
    - Development of decision support tools and electronic health record integration
    
    The Subtle Anterior STEMI Calculator (4-Variable) serves as a valuable clinical 
    decision support tool that, when used appropriately within the broader clinical 
    context, can improve patient outcomes by facilitating timely recognition and 
    treatment of subtle anterior STEMIs while reducing unnecessary procedures for 
    benign conditions.
    
    Reference: Driver BE, et al. J Electrocardiol. 2017;50(6):836-843.
    """
    
    result: float = Field(
        ...,
        description="Calculated Subtle Anterior STEMI 4-Variable score using the validated formula. "
                   "Score incorporates QTc interval, QRS amplitude in V2, R wave amplitude in V4, "
                   "and ST elevation in V3 to differentiate benign early repolarization from subtle STEMI. "
                   "Threshold of 18.2 provides optimal diagnostic accuracy.",
        example=16.8
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the calculated score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation of the calculated score with specific recommendations "
                   "for patient management, including diagnostic probability, recommended interventions, "
                   "monitoring protocols, and clinical decision guidance. Includes sensitivity and specificity "
                   "data to support evidence-based decision-making.",
        example="Score 16.8 is below the diagnostic threshold of 18.2, suggesting benign early repolarization "
                "rather than acute coronary occlusion. This indicates a low probability of anterior STEMI "
                "requiring urgent intervention. However, clinical correlation is essential - continue to "
                "monitor symptoms and consider serial ECGs if chest pain persists or clinical suspicion "
                "remains high. The 4-variable formula has 83.3% sensitivity and 87.7% specificity."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic category based on calculated score and established threshold",
        example="Benign Early Repolarization"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic category and recommended clinical approach",
        example="Low probability of anterior STEMI"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 16.8,
                "unit": "points",
                "interpretation": "Score 16.8 is below the diagnostic threshold of 18.2, suggesting benign early repolarization rather than acute coronary occlusion. This indicates a low probability of anterior STEMI requiring urgent intervention. However, clinical correlation is essential - continue to monitor symptoms and consider serial ECGs if chest pain persists or clinical suspicion remains high. The 4-variable formula has 83.3% sensitivity and 87.7% specificity for detecting subtle anterior STEMI.",
                "stage": "Benign Early Repolarization",
                "stage_description": "Low probability of anterior STEMI"
            }
        }