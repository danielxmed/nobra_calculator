"""
ED-SAFE Patient Safety Screener 3 (PSS-3) Models

Request and response models for PSS-3 suicide risk screening.

References (Vancouver style):
1. Boudreaux ED, Camargo CA Jr, Arias SA, Blais RK, Horton BJ, Jaques ML, et al. 
   Improving Suicide Risk Screening and Detection in the Emergency Department. 
   Am J Prev Med. 2016;50(4):445-453. doi: 10.1016/j.amepre.2015.09.029.
2. Boudreaux ED, Jaques ML, Brady KM, Matson A, Allen MH. The patient safety screener: 
   validation of a brief suicide risk screener for emergency department settings. 
   Arch Suicide Res. 2015;19(2):151-60. doi: 10.1080/13811118.2015.1034604.
3. Miller IW, Camargo CA Jr, Arias SA, Sullivan AF, Allen MH, Goldstein AB, et al. 
   Suicide prevention in an emergency department population: the ED-SAFE study. 
   JAMA Psychiatry. 2017;74(6):563-570. doi: 10.1001/jamapsychiatry.2017.0678.
4. Boudreaux ED, Miller I, Goldstein AB, Sullivan AF, Allen MH, Manton AP, et al. 
   The Emergency Department Safety Assessment and Follow-up Evaluation (ED-SAFE): 
   method and design considerations. Contemp Clin Trials. 2013;36(1):14-24. 
   doi: 10.1016/j.cct.2013.05.008.

The ED-SAFE Patient Safety Screener 3 (PSS-3) is a brief, validated suicide risk 
screening tool designed for universal use in emergency departments. It consists of 
three questions that can rapidly identify patients at risk for suicide, including 
those presenting with non-psychiatric chief complaints. The tool was developed as 
part of the National Institute of Mental Health (NIMH) ED-SAFE study and has been 
shown to double the rate of suicide risk detection in emergency departments.
"""

from pydantic import BaseModel, Field
from typing import Literal


class EdSafePatientSafetyScreenerRequest(BaseModel):
    """
    Request model for ED-SAFE Patient Safety Screener 3 (PSS-3)
    
    The PSS-3 is a brief, evidence-based suicide risk screening tool specifically 
    designed for emergency department settings. It can be administered to all patients 
    ≥18 years old regardless of their chief complaint, making it ideal for universal 
    screening in busy emergency departments.
    
    Clinical Context and Rationale:
    - Suicide is a leading cause of death, with emergency departments serving as 
      critical intervention points for at-risk individuals
    - Among patients presenting to EDs with non-psychiatric complaints, 3-12% 
      also have suicidal ideation
    - Traditional clinical assessment identifies only 2.9% of at-risk patients
    - PSS-3 universal screening increases detection to 5.7% (doubling detection rate)
    - Brief administration time fits into existing ED triage workflow
    
    Administration Guidelines:
    - Administer during triage or primary nursing assessment
    - Can be given to patients with any chief complaint (psychiatric or non-psychiatric)
    - Should be administered verbally by trained healthcare personnel
    - Takes approximately 1-2 minutes to complete
    - Universal screening approach recommended for all ED patients ≥18 years
    
    Screening Questions (in order):
    
    1. Depression Assessment (Past 2 Weeks):
    "Over the past 2 weeks, have you felt down, depressed, or hopeless?"
    - Assesses for depressive symptoms as contextual risk factor
    - Does not independently determine positive screening result
    - Provides important clinical context for overall risk assessment
    
    2. Active Suicidal Ideation (Past 2 Weeks):
    "Over the past 2 weeks, have you had thoughts of killing yourself?"
    - Primary screening criterion for current suicide risk
    - Positive response (Yes) = Automatic positive screen requiring intervention
    - Most critical question for immediate safety assessment
    
    3. Lifetime Suicide Attempt History:
    "Have you ever in your lifetime made a suicide attempt?"
    - Primary screening criterion based on historical risk factor
    - Positive response (Yes) = Automatic positive screen requiring intervention
    - History of suicide attempt is strongest predictor of future attempts
    
    Positive Screening Criteria:
    A patient screens POSITIVE if they answer "Yes" to either:
    - Question 2 (active suicidal ideation in past 2 weeks), OR
    - Question 3 (lifetime history of suicide attempt)
    
    Note: Question 1 (depression) provides clinical context but does not 
    independently determine positive screening status.
    
    Validation and Psychometric Properties:
    - Strong agreement with Beck Scale for Suicide Ideation (κ = 0.94-0.95)
    - Excellent agreement for suicide attempt history (κ = 0.97-0.98)
    - Good agreement for ideation detection (κ = 0.61)
    - Sensitivity and specificity optimized for emergency department populations
    - Validated across diverse patient populations and chief complaints
    
    Clinical Implementation:
    - Part of comprehensive ED-SAFE suicide prevention protocol
    - Positive screens require immediate further assessment by clinician
    - Consider mental health consultation for positive screens
    - Follow-up with ED-SAFE Secondary Screener (ESS-6) for risk stratification
    - Safety planning and continuous monitoring for positive screens
    - Documentation important for continuity of care and quality improvement
    
    Workflow Integration:
    - Designed to fit seamlessly into existing ED triage processes
    - Can be administered by nurses, technicians, or other trained staff
    - Results should be immediately communicated to treating physician
    - Positive screens trigger enhanced safety protocols and assessment pathways
    
    Limitations and Considerations:
    - Screening tool only - not a comprehensive suicide risk assessment
    - Positive screens require follow-up clinical evaluation
    - Cultural and language considerations may affect administration
    - Patient privacy and confidentiality important during administration
    - Staff training recommended for optimal implementation and sensitivity
    
    References (Vancouver style):
    1. Boudreaux ED, Camargo CA Jr, Arias SA, Blais RK, Horton BJ, Jaques ML, et al. 
       Improving Suicide Risk Screening and Detection in the Emergency Department. 
       Am J Prev Med. 2016;50(4):445-453.
    2. Boudreaux ED, Jaques ML, Brady KM, Matson A, Allen MH. The patient safety screener: 
       validation of a brief suicide risk screener for emergency department settings. 
       Arch Suicide Res. 2015;19(2):151-60.
    3. Miller IW, Camargo CA Jr, Arias SA, Sullivan AF, Allen MH, Goldstein AB, et al. 
       Suicide prevention in an emergency department population: the ED-SAFE study. 
       JAMA Psychiatry. 2017;74(6):563-570.
    """
    
    depression_past_2_weeks: Literal["yes", "no"] = Field(
        ...,
        description="Over the past 2 weeks, have you felt down, depressed, or hopeless? Assesses depressive symptoms as contextual risk factor",
        example="no"
    )
    
    suicidal_thoughts_past_2_weeks: Literal["yes", "no"] = Field(
        ...,
        description="Over the past 2 weeks, have you had thoughts of killing yourself? PRIMARY SCREENING CRITERION - Yes response = automatic positive screen",
        example="yes"
    )
    
    lifetime_suicide_attempt: Literal["yes", "no"] = Field(
        ...,
        description="Have you ever in your lifetime made a suicide attempt? PRIMARY SCREENING CRITERION - Yes response = automatic positive screen",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "depression_past_2_weeks": "no",
                "suicidal_thoughts_past_2_weeks": "yes",
                "lifetime_suicide_attempt": "no"
            }
        }


class EdSafePatientSafetyScreenerResponse(BaseModel):
    """
    Response model for ED-SAFE Patient Safety Screener 3 (PSS-3)
    
    The PSS-3 screening result provides critical information for immediate clinical 
    decision-making in emergency departments. Results guide whether additional 
    assessment, safety precautions, and mental health interventions are needed.
    
    Screening Results and Clinical Actions:
    
    Negative Screen:
    - No current suicidal ideation (past 2 weeks) reported
    - No lifetime history of suicide attempt reported
    - Clinical Actions:
      * Continue with routine emergency care for presenting complaint
      * Document negative screening result in medical record
      * No immediate suicide-specific interventions required
      * Consider addressing depressive symptoms if reported (Question 1)
      * Maintain standard clinical vigilance during care
    
    Positive Screen:
    - Active suicidal ideation in past 2 weeks (Question 2 = Yes), OR
    - Lifetime history of suicide attempt (Question 3 = Yes), OR
    - Both criteria present
    - Clinical Actions:
      * IMMEDIATE further assessment by treating clinician required
      * Patient should not be left alone - implement continuous monitoring
      * Consider mental health consultation/psychiatric evaluation
      * Implement safety precautions (remove potential means, secure environment)
      * Conduct comprehensive suicide risk assessment
      * Develop safety plan with patient if appropriate
      * Consider administration of ED-SAFE Secondary Screener (ESS-6) for risk stratification
      * Coordinate appropriate disposition (inpatient, outpatient follow-up, crisis services)
      * Ensure proper documentation and communication during care transitions
    
    Risk Stratification Considerations:
    
    Higher Risk Indicators (require enhanced assessment):
    - Both current ideation AND history of attempt present
    - Current ideation with specific plan or means
    - Recent attempt (within past year)
    - Depression symptoms combined with suicidality
    - Multiple previous attempts
    - Access to lethal means
    - Social isolation or recent losses
    
    Secondary Assessment Tools:
    - ED-SAFE Secondary Screener (ESS-6) for detailed risk stratification
    - Columbia Suicide Severity Rating Scale (C-SSRS) for comprehensive assessment
    - Beck Scale for Suicide Ideation (BSSI) for research or detailed clinical use
    - Patient Health Questionnaire-9 (PHQ-9) for depression severity
    
    Safety Planning Components:
    - Identify personal warning signs and triggers
    - List internal coping strategies patient can use
    - Identify social contacts and social settings that provide distraction
    - List family members or friends to contact during crisis
    - Identify mental health professionals and agencies to contact
    - Ensure environment safety (means restriction)
    
    Disposition Considerations:
    
    Positive Screen + High Risk:
    - Psychiatric admission or emergency psychiatric evaluation
    - Crisis stabilization services
    - Intensive outpatient programs with rapid follow-up
    - Mobile crisis team activation
    
    Positive Screen + Moderate Risk:
    - Outpatient mental health referral with urgent follow-up (24-48 hours)
    - Crisis hotline information and safety planning
    - Family/support system activation
    - Primary care follow-up coordination
    
    Documentation Requirements:
    - Complete PSS-3 screening results
    - Clinical response to positive screening
    - Safety measures implemented
    - Mental health consultation results (if obtained)
    - Safety plan development
    - Disposition and follow-up arrangements
    - Family/caregiver notification (as appropriate and consented)
    
    Quality Improvement and Monitoring:
    - Track screening completion rates
    - Monitor positive screening rates and clinical responses
    - Evaluate patient outcomes and follow-up completion
    - Staff training effectiveness and protocol adherence
    - Patient and family satisfaction with screening process
    
    Legal and Ethical Considerations:
    - Mandatory reporting requirements (varies by jurisdiction)
    - Confidentiality and privacy protections
    - Informed consent for mental health interventions
    - Involuntary commitment criteria and procedures
    - Documentation standards for medicolegal protection
    
    Implementation Support:
    - Staff training on screening administration and response protocols
    - Integration with electronic health record systems
    - Quality assurance and protocol compliance monitoring
    - Resource availability (mental health consultation, crisis services)
    - Policy development for positive screening management
    
    Reference: Boudreaux ED, et al. Am J Prev Med. 2016;50(4):445-453.
    """
    
    result: str = Field(
        ...,
        description="PSS-3 screening result indicating suicide risk status (Negative Screen or Positive Screen)",
        example="Positive Screen"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the screening result",
        example="status"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and immediate action recommendations based on screening result",
        example="Positive screen for suicide risk. Patient reports active suicidal ideation in past 2 weeks. Requires immediate further assessment by treating clinician. Consider mental health consultation, comprehensive suicide risk assessment, and safety planning. Risk stratification with ED-SAFE Secondary Screener (ESS-6) recommended if available. Patient should not be left alone and requires continuous monitoring until comprehensive assessment is completed."
    )
    
    stage: str = Field(
        ...,
        description="Screening result category (Negative Screen, Positive Screen)",
        example="Positive Screen"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the screening result",
        example="Positive for suicide risk indicators"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Positive Screen",
                "unit": "status",
                "interpretation": "Positive screen for suicide risk. Patient reports active suicidal ideation in past 2 weeks. Requires immediate further assessment by treating clinician. Consider mental health consultation, comprehensive suicide risk assessment, and safety planning. Risk stratification with ED-SAFE Secondary Screener (ESS-6) recommended if available. Patient should not be left alone and requires continuous monitoring until comprehensive assessment is completed.",
                "stage": "Positive Screen",
                "stage_description": "Positive for suicide risk indicators"
            }
        }