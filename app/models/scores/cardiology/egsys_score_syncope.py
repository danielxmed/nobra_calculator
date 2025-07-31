"""
EGSYS (Evaluation of Guidelines in SYncope Study) Score for Syncope Models

Request and response models for EGSYS cardiac syncope risk assessment.

References (Vancouver style):
1. Del Rosso A, Ungar A, Maggi R, Giada F, Petix NR, De Santo T, et al. Clinical predictors 
   of cardiac syncope at initial evaluation in patients referred urgently to a general 
   hospital: the EGSYS score. Heart. 2008;94(12):1620-6. doi: 10.1136/hrt.2008.143123.
2. Kariman H, Harati S, Safari S, Baratloo A, Pishgahi M, Ardalani AR. Validation of EGSYS 
   Score in Prediction of Cardiogenic Syncope. Emerg Med Int. 2015;2015:515370. 
   doi: 10.1155/2015/515370.
3. Task Force for the Diagnosis and Management of Syncope; European Society of Cardiology (ESC); 
   European Heart Rhythm Association (EHRA); Heart Failure Association (HFA); Heart Rhythm Society (HRS). 
   Guidelines for the diagnosis and management of syncope (version 2009). Eur Heart J. 2009;30(21):2631-71. 
   doi: 10.1093/eurheartj/ehp298.
4. Brignole M, Moya A, de Lange FJ, Deharo JC, Elliott PM, Fanciulli A, et al. 2018 ESC Guidelines 
   for the diagnosis and management of syncope. Eur Heart J. 2018;39(21):1883-1948. 
   doi: 10.1093/eurheartj/ehy037.

The EGSYS (Evaluation of Guidelines in SYncope Study) Score predicts the likelihood that 
syncope is of cardiac cause, helping emergency clinicians with screening and risk 
stratification in patients presenting with syncope episodes.
"""

from pydantic import BaseModel, Field
from typing import Literal


class EgsysScoreSyncopeRequest(BaseModel):
    """
    Request model for EGSYS (Evaluation of Guidelines in SYncope Study) Score for Syncope
    
    The EGSYS score is a validated clinical decision tool designed to differentiate between 
    cardiac and non-cardiac causes of syncope in emergency department settings. It uses six 
    clinical variables to calculate a risk score that helps clinicians determine the likelihood 
    of cardiac etiology and guide appropriate management decisions.
    
    Clinical Context and Development:
    
    Syncope is a common presenting complaint in emergency departments, accounting for 1-3% of 
    all ED visits. The challenge lies in distinguishing between benign causes (such as vasovagal 
    syncope) and potentially life-threatening cardiac causes. The EGSYS score was developed to 
    provide a standardized, evidence-based approach to this clinical challenge.
    
    The original EGSYS study analyzed 516 patients with syncope across multiple European centers, 
    identifying key clinical predictors that distinguish cardiac from non-cardiac causes. The 
    score has been subsequently validated in multiple international studies with consistent 
    performance characteristics.
    
    Scoring Parameters and Clinical Rationale:
    
    Positive Predictors (Increase Cardiac Likelihood):
    
    1. Abnormal EKG and/or Heart Disease (+3 points):
       - Most significant structural predictor of cardiac syncope
       - Includes any EKG abnormality or known cardiac condition
       - Strong association with arrhythmic and structural cardiac causes
       - Examples: bundle branch blocks, Q waves, arrhythmias, cardiomyopathy
    
    2. Palpitations Before Syncope (+4 points):
       - Strongest individual predictor in the EGSYS model
       - Suggests arrhythmic etiology preceding loss of consciousness
       - Typically reported as rapid, irregular, or forceful heartbeats
       - May indicate ventricular or supraventricular arrhythmias
    
    3. Syncope During Effort (+3 points):
       - Classic presentation of exercise-induced cardiac syncope
       - Associated with hypertrophic cardiomyopathy, aortic stenosis
       - May indicate catecholamine-sensitive arrhythmias
       - Excludes effort-related vasovagal responses
    
    4. Syncope in Supine Position (+2 points):
       - Unusual for typical vasovagal syncope (which requires upright posture)
       - More consistent with arrhythmic causes
       - Eliminates orthostatic and situational triggers
       - Significant because most benign syncope requires gravitational component
    
    Negative Predictors (Decrease Cardiac Likelihood):
    
    5. Autonomic Prodromes (-1 point):
       - Classic vasovagal warning symptoms
       - Includes nausea, vomiting, diaphoresis, feeling warm/cold
       - Suggests intact autonomic nervous system response
       - Typical of neurally-mediated syncope
    
    6. Precipitating/Predisposing Factors (-1 point):
       - Identifiable triggers for neurally-mediated syncope
       - Includes fear, pain, emotional stress, prolonged standing
       - Orthostatic hypotension triggers
       - Situational syncope triggers (coughing, micturition, defecation)
    
    Score Interpretation and Performance:
    
    The EGSYS score ranges from -2 to +16 points, with a validated cut-off of ≥3 points:
    
    Score ≥3 (High Risk - Cardiac Syncope Likely):
    - Sensitivity: 95% for detecting cardiac syncope
    - Specificity: 61% for excluding non-cardiac causes
    - Positive Predictive Value: 33%
    - Negative Predictive Value: 99%
    - 21-24 month mortality: 17%
    
    Score <3 (Low Risk - Cardiac Syncope Less Likely):
    - Very high negative predictive value (99%)
    - 21-24 month mortality: 3%
    - Suitable for outpatient evaluation in stable patients
    
    Clinical Management Implications:
    
    High-Risk Patients (Score ≥3):
    - Consider hospital admission for diagnostic confirmation
    - Cardiology consultation recommended
    - Continuous cardiac monitoring (telemetry)
    - Comprehensive cardiac evaluation:
      * Echocardiogram to assess structure and function
      * Extended cardiac monitoring (Holter, event monitor)
      * Exercise testing if effort-related symptoms
      * Electrophysiology study consideration
    - Medication review for pro-arrhythmic drugs
    
    Low-Risk Patients (Score <3):
    - Outpatient management may be appropriate for stable patients
    - Standard syncope evaluation for non-cardiac causes
    - Basic cardiac assessment (EKG, basic metabolic panel)
    - Neurovascular assessment if indicated
    - Safety netting with clear return precautions
    - Follow-up with primary care or appropriate specialist
    
    Limitations and Considerations:
    
    Important limitations to recognize:
    - Designed for emergency department screening, not definitive diagnosis
    - Should complement, not replace, clinical judgment
    - Performance may vary in different patient populations
    - Less useful in outpatient settings where patients are pre-selected
    - Does not capture all potential cardiac causes
    - Some high-risk features may warrant admission regardless of score
    
    Validation and Evidence Base:
    
    The EGSYS score has been validated in multiple studies:
    - Original validation in 516 patients across European centers
    - Subsequent validation studies in diverse populations
    - Consistent performance across different healthcare systems
    - Long-term mortality data supporting prognostic value
    - Comparison studies with other syncope risk stratification tools
    
    Integration with Clinical Practice:
    
    Best practices for EGSYS implementation:
    - Use as part of comprehensive syncope evaluation
    - Combine with clinical assessment and other risk factors
    - Consider local resources and cardiology availability
    - Document decision-making rationale
    - Ensure appropriate follow-up arrangements
    - Patient education about warning signs and return precautions
    
    Alternative Risk Stratification Tools:
    
    Other validated syncope risk scores include:
    - San Francisco Syncope Rule (may be more reliable according to some experts)
    - Canadian Syncope Risk Score
    - ROSE (Risk stratification Of Syncope in the Emergency department) rule
    - Boston Syncope Criteria
    
    Quality Improvement Applications:
    
    Healthcare systems can use EGSYS for:
    - Standardizing syncope evaluation protocols
    - Reducing unnecessary admissions for low-risk patients
    - Ensuring appropriate workup for high-risk patients
    - Quality metrics and performance monitoring
    - Staff education and training programs
    
    References (Vancouver style):
    1. Del Rosso A, Ungar A, Maggi R, Giada F, Petix NR, De Santo T, et al. Clinical predictors 
       of cardiac syncope at initial evaluation in patients referred urgently to a general 
       hospital: the EGSYS score. Heart. 2008;94(12):1620-6.
    2. Kariman H, Harati S, Safari S, Baratloo A, Pishgahi M, Ardalani AR. Validation of EGSYS 
       Score in Prediction of Cardiogenic Syncope. Emerg Med Int. 2015;2015:515370.
    3. Brignole M, Moya A, de Lange FJ, Deharo JC, Elliott PM, Fanciulli A, et al. 2018 ESC Guidelines 
       for the diagnosis and management of syncope. Eur Heart J. 2018;39(21):1883-1948.
    """
    
    abnormal_ecg_heart_disease: Literal["yes", "no"] = Field(
        ...,
        description="Abnormal EKG and/or heart disease present. Includes any EKG abnormality, known cardiac conditions, cardiomyopathy, or structural heart disease. Scores +3 points if yes",
        example="no"
    )
    
    palpitations_before_syncope: Literal["yes", "no"] = Field(
        ...,
        description="Palpitations before syncope episode. Patient reports awareness of rapid, irregular, or forceful heartbeats immediately preceding the syncopal event. Scores +4 points if yes (strongest predictor)",
        example="no"
    )
    
    syncope_during_effort: Literal["yes", "no"] = Field(
        ...,
        description="Syncope occurred during physical effort or exertion. Classic presentation of exercise-induced cardiac syncope, associated with structural heart disease or catecholamine-sensitive arrhythmias. Scores +3 points if yes",
        example="no"
    )
    
    syncope_supine_position: Literal["yes", "no"] = Field(
        ...,
        description="Syncope occurred while in supine (lying down) position. Unusual for typical vasovagal syncope which requires upright posture, more consistent with arrhythmic causes. Scores +2 points if yes",
        example="no"
    )
    
    autonomic_prodromes: Literal["yes", "no"] = Field(
        ...,
        description="Autonomic prodromes present (nausea, vomiting, diaphoresis, feeling warm/cold). Classic vasovagal warning symptoms suggesting neurally-mediated syncope. Scores -1 point if yes (reduces cardiac likelihood)",
        example="yes"
    )
    
    precipitating_factors: Literal["yes", "no"] = Field(
        ...,
        description="Predisposing or precipitating factors present (fear, pain, emotional stress, prolonged standing, orthostasis). Identifiable triggers for neurally-mediated or situational syncope. Scores -1 point if yes (reduces cardiac likelihood)",
        example="yes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "abnormal_ecg_heart_disease": "no",
                "palpitations_before_syncope": "no",
                "syncope_during_effort": "no",
                "syncope_supine_position": "no",
                "autonomic_prodromes": "yes",
                "precipitating_factors": "yes"
            }
        }


class EgsysScoreSyncopeResponse(BaseModel):
    """
    Response model for EGSYS (Evaluation of Guidelines in SYncope Study) Score for Syncope
    
    The EGSYS score provides critical risk stratification for patients presenting with syncope, 
    helping clinicians distinguish between cardiac and non-cardiac causes and guide appropriate 
    management decisions. The score's high negative predictive value makes it particularly 
    valuable for identifying low-risk patients suitable for outpatient management.
    
    Score Interpretation and Clinical Decision Making:
    
    Low Risk (Score <3 points) - Cardiac Syncope Less Likely:
    
    Clinical Significance:
    - 99% negative predictive value for cardiac syncope
    - 21-24 month mortality risk: approximately 3%
    - Strong evidence against cardiac etiology
    
    Management Approach:
    - Outpatient evaluation appropriate for hemodynamically stable patients
    - Focus on non-cardiac causes of syncope:
      * Neurally-mediated (vasovagal) syncope
      * Orthostatic hypotension
      * Situational syncope
      * Medication-related causes
      * Neurological causes (rare)
    
    Recommended Evaluation:
    - Basic cardiac assessment (12-lead EKG, basic metabolic panel)
    - Orthostatic vital signs
    - Medication review for hypotensive agents
    - Consider tilt table testing if recurrent vasovagal syncope suspected
    - Neurovascular assessment if focal neurological symptoms
    
    Follow-up and Safety Netting:
    - Primary care follow-up within 1-2 weeks
    - Clear return precautions for recurrent episodes
    - Patient education on vasovagal triggers and prevention
    - Consider neurology referral if neurological symptoms present
    - Reassurance about low cardiac risk
    
    High Risk (Score ≥3 points) - Cardiac Syncope Likely:
    
    Clinical Significance:
    - 95% sensitivity for detecting cardiac syncope
    - 21-24 month mortality risk: approximately 17%
    - Strong indication for comprehensive cardiac evaluation
    - Significantly increased long-term mortality risk
    
    Immediate Management:
    - Consider hospital admission for diagnostic confirmation
    - Continuous cardiac monitoring (telemetry) recommended
    - Hemodynamic stabilization if needed
    - Avoid discharge until cardiac evaluation completed
    
    Comprehensive Cardiac Evaluation:
    
    Essential Testing:
    - 12-lead EKG (repeat if initial normal)
    - Continuous cardiac monitoring for arrhythmia detection
    - Echocardiogram to assess cardiac structure and function
    - Cardiac enzymes to exclude myocardial infarction
    - Electrolyte panel including magnesium and phosphate
    
    Extended Cardiac Monitoring:
    - Inpatient telemetry monitoring during admission
    - Consider Holter monitor (24-48 hours) if inpatient monitoring negative
    - Event monitor or implantable loop recorder for recurrent episodes
    - Consider electrophysiology study if high suspicion of arrhythmia
    
    Specialized Testing (As Indicated):
    - Exercise stress testing if effort-related syncope
    - Coronary angiography if ischemic etiology suspected  
    - Cardiac MRI for suspected cardiomyopathy or infiltrative disease
    - Genetic testing for inherited arrhythmia syndromes in young patients
    
    Cardiology Consultation:
    - Urgent cardiology consultation recommended
    - Consider electrophysiology referral for suspected arrhythmic causes
    - Heart failure specialist if structural heart disease present
    - Inherited cardiac disease specialist for young patients with family history
    
    Risk Stratification and Prognosis:
    
    Mortality Risk Factors:
    - Score ≥3 associated with 17% mortality at 21-24 months
    - Higher scores correlate with increased mortality risk
    - Structural heart disease carries highest risk
    - Arrhythmic causes have variable prognosis depending on underlying substrate
    
    Long-term Monitoring:
    - Regular cardiology follow-up for high-risk patients
    - Serial echocardiograms if structural heart disease
    - Monitoring for heart failure development
    - Assessment for need for device therapy (pacemaker, ICD)
    
    Treatment Considerations:
    
    Arrhythmic Causes:
    - Antiarrhythmic medications as appropriate
    - Pacemaker for symptomatic bradycardia or heart block
    - Implantable cardioverter-defibrillator (ICD) for ventricular arrhythmias
    - Catheter ablation for recurrent supraventricular or ventricular arrhythmias
    
    Structural Heart Disease:
    - Heart failure management optimization
    - Valve replacement or repair for severe valvular disease
    - Risk stratification for sudden cardiac death
    - Activity restrictions as clinically indicated
    
    Quality Assurance and Documentation:
    
    Documentation Requirements:
    - Complete EGSYS score calculation with rationale
    - Description of all clinical variables assessed
    - Risk stratification and management plan
    - Patient counseling and education provided
    - Follow-up arrangements and safety netting
    
    Performance Monitoring:
    - Track adherence to EGSYS-based protocols
    - Monitor patient outcomes and satisfaction
    - Assess appropriateness of admission and discharge decisions
    - Quality metrics for cardiac evaluation completion
    
    Patient Education and Communication:
    
    Low-Risk Patients:
    - Explanation of low cardiac risk
    - Education about likely non-cardiac causes
    - Return precautions for concerning symptoms
    - Lifestyle modifications for vasovagal syncope prevention
    
    High-Risk Patients:
    - Explanation of need for cardiac evaluation
    - Discussion of potential cardiac causes
    - Importance of completing recommended testing
    - Activity restrictions until evaluation complete
    - Emergency return precautions
    
    Limitations and Clinical Judgment:
    
    Important Considerations:
    - EGSYS score should complement, not replace, clinical assessment
    - Some high-risk features may warrant admission regardless of score
    - Consider patient-specific factors (comorbidities, social situation)
    - Local resources and cardiology availability may influence management
    - Some patients may require individualized approach beyond score recommendations
    
    Integration with Other Risk Scores:
    - Consider using in conjunction with other validated syncope scores
    - Clinical judgment remains paramount in complex cases
    - Some experts prefer alternative tools like San Francisco Syncope Rule
    - Local protocols may specify preferred risk stratification approach
    
    Reference: Del Rosso A, et al. Heart. 2008;94(12):1620-6.
    """
    
    result: int = Field(
        ...,
        description="EGSYS score calculated from clinical variables (range: -2 to +16 points)",
        example=-2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the EGSYS score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on cardiac syncope risk assessment",
        example="Score <3 suggests cardiac syncope is less likely. 21-24 month mortality risk approximately 3%. Continue standard syncope evaluation and consider non-cardiac causes. Outpatient follow-up may be appropriate for stable patients without high-risk features. Contributing factors: Autonomic prodromes present (nausea, vomiting, feeling warm/cold) (-1 points); Predisposing or precipitating factors present (fear, pain, emotion, orthostasis) (-1 points). Low-risk patients may be suitable for outpatient evaluation with appropriate follow-up and safety netting."
    )
    
    stage: str = Field(
        ...,
        description="Risk category for cardiac syncope (Low Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the cardiac syncope likelihood",
        example="Cardiac syncope less likely"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": -2,
                "unit": "points",
                "interpretation": "Score <3 suggests cardiac syncope is less likely. 21-24 month mortality risk approximately 3%. Continue standard syncope evaluation and consider non-cardiac causes. Outpatient follow-up may be appropriate for stable patients without high-risk features. Contributing factors: Autonomic prodromes present (nausea, vomiting, feeling warm/cold) (-1 points); Predisposing or precipitating factors present (fear, pain, emotion, orthostasis) (-1 points). Low-risk patients may be suitable for outpatient evaluation with appropriate follow-up and safety netting.",
                "stage": "Low Risk",
                "stage_description": "Cardiac syncope less likely"
            }
        }