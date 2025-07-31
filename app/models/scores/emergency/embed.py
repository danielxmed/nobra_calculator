"""
Emergency Department-Initiated Buprenorphine for Opioid Use Disorder (EMBED) Models

Request and response models for EMBED assessment calculation.

References (Vancouver style):
1. D'Onofrio G, Chawarski MC, O'Connor PG, Pantalon MV, Busch SH, Owens PH, et al. 
   Emergency department-initiated buprenorphine for opioid dependence with continuation 
   in primary care: outcomes during and after intervention. J Gen Intern Med. 
   2017 Jun;32(6):660-666. doi: 10.1007/s11606-017-3993-2.
2. Hawk K, D'Onofrio G, Chawarski MC, O'Connor PG, Cowan E, Lyons MS, et al. 
   Barriers and facilitators to clinician readiness to provide emergency department-initiated 
   buprenorphine. JAMA Netw Open. 2020 May 1;3(5):e204561. doi: 10.1001/jamanetworkopen.2020.4561.
3. American Psychiatric Association. Diagnostic and statistical manual of mental disorders 
   (5th ed.). Arlington, VA: American Psychiatric Publishing; 2013.
4. Wesson DR, Ling W. The Clinical Opiate Withdrawal Scale (COWS). J Psychoactive Drugs. 
   2003 Apr-Jun;35(2):253-9. doi: 10.1080/02791072.2003.10400007.

The EMBED tool assesses opioid use disorder using DSM-5 criteria, evaluates withdrawal 
severity with the Clinical Opiate Withdrawal Scale (COWS), and determines patient 
readiness for emergency department-initiated buprenorphine treatment. This comprehensive 
assessment helps clinicians make evidence-based decisions about buprenorphine induction 
in the emergency department setting.
"""

from pydantic import BaseModel, Field
from typing import Literal


class EmbedRequest(BaseModel):
    """
    Request model for Emergency Department-Initiated Buprenorphine (EMBED) Assessment
    
    The EMBED tool combines multiple assessment components:
    
    DSM-5 Opioid Use Disorder Diagnostic Criteria (11 criteria):
    At least 2 criteria must be met within a 12-month period for OUD diagnosis.
    Severity is determined by criteria count: Mild (2-3), Moderate (4-5), Severe (≥6).
    
    Clinical Opiate Withdrawal Scale (COWS):
    11-item clinician-administered scale rating common opioid withdrawal symptoms.
    Scores range from 0-48, with higher scores indicating more severe withdrawal.
    Interpretation: <8 (None to Mild), 8-12 (Mild to Moderate), >12 (Moderate to Severe).
    
    Treatment Readiness Assessment:
    Brief negotiation interview to assess patient motivation for treatment.
    
    Clinical Factors:
    Pregnancy status and provider buprenorphine waiver/certification requirements.
    
    References (Vancouver style):
    1. D'Onofrio G, Chawarski MC, O'Connor PG, Pantalon MV, Busch SH, Owens PH, et al. 
       Emergency department-initiated buprenorphine for opioid dependence with continuation 
       in primary care: outcomes during and after intervention. J Gen Intern Med. 
       2017 Jun;32(6):660-666. doi: 10.1007/s11606-017-3993-2.
    2. American Psychiatric Association. Diagnostic and statistical manual of mental disorders 
       (5th ed.). Arlington, VA: American Psychiatric Publishing; 2013.
    3. Wesson DR, Ling W. The Clinical Opiate Withdrawal Scale (COWS). J Psychoactive Drugs. 
       2003 Apr-Jun;35(2):253-9. doi: 10.1080/02791072.2003.10400007.
    """
    
    # DSM-5 Opioid Use Disorder Criteria
    opioid_larger_amounts: Literal["yes", "no"] = Field(
        ...,
        description="Taking opioids in larger amounts or for longer than intended? (DSM-5 Criterion 1)",
        example="yes"
    )
    
    unsuccessful_cut_down: Literal["yes", "no"] = Field(
        ...,
        description="Persistent desire or unsuccessful efforts to cut down or control opioid use? (DSM-5 Criterion 2)",
        example="yes"
    )
    
    time_obtaining_using: Literal["yes", "no"] = Field(
        ...,
        description="Spending a lot of time obtaining, using, or recovering from opioid effects? (DSM-5 Criterion 3)",
        example="no"
    )
    
    craving_desire: Literal["yes", "no"] = Field(
        ...,
        description="Craving or strong desire to use opioids? (DSM-5 Criterion 4)",
        example="yes"
    )
    
    failure_obligations: Literal["yes", "no"] = Field(
        ...,
        description="Failure to fulfill major obligations at work, school, or home due to opioid use? (DSM-5 Criterion 5)",
        example="no"
    )
    
    continued_despite_problems: Literal["yes", "no"] = Field(
        ...,
        description="Continued opioid use despite persistent social or interpersonal problems? (DSM-5 Criterion 6)",
        example="no"
    )
    
    activities_given_up: Literal["yes", "no"] = Field(
        ...,
        description="Important social, occupational, or recreational activities given up or reduced due to opioid use? (DSM-5 Criterion 7)",
        example="no"
    )
    
    hazardous_situations: Literal["yes", "no"] = Field(
        ...,
        description="Recurrent opioid use in physically hazardous situations? (DSM-5 Criterion 8)",
        example="no"
    )
    
    physical_psychological_problems: Literal["yes", "no"] = Field(
        ...,
        description="Continued opioid use despite physical or psychological problems caused or worsened by opioids? (DSM-5 Criterion 9)",
        example="yes"
    )
    
    tolerance: Literal["yes", "no"] = Field(
        ...,
        description="Tolerance (need for increased amounts or diminished effect with same amount)? Note: Not met if opioids taken under appropriate medical supervision (DSM-5 Criterion 10)",
        example="yes"
    )
    
    withdrawal: Literal["yes", "no"] = Field(
        ...,
        description="Withdrawal syndrome or using opioids to avoid withdrawal symptoms? Note: Not met if opioids taken under appropriate medical supervision (DSM-5 Criterion 11)",
        example="yes"
    )
    
    # Clinical Opiate Withdrawal Scale (COWS)
    cows_score: int = Field(
        ...,
        description="Clinical Opiate Withdrawal Scale (COWS) total score. Range 0-48 points. Assessment includes: restlessness, sweating, dilated pupils, bone/joint aches, runny nose/tearing, GI upset, tremor, yawning, anxiety/irritability, gooseflesh, current withdrawal severity",
        ge=0,
        le=48,
        example=15
    )
    
    # Treatment Readiness Assessment
    treatment_readiness: Literal["ready", "not_ready"] = Field(
        ...,
        description="Patient readiness for treatment assessed via brief negotiation interview. Consider motivation, understanding of treatment, and willingness to engage in care",
        example="ready"
    )
    
    # Clinical Factors
    pregnancy_status: Literal["yes", "no"] = Field(
        ...,
        description="Is the patient pregnant? Pregnancy requires specialized consultation and modified treatment approach",
        example="no"
    )
    
    buprenorphine_waiver: Literal["yes", "no"] = Field(
        ...,
        description="Does the provider have buprenorphine prescription waiver/certification (X-waiver, DATA 2000, or updated requirements)? Required for prescribing buprenorphine",
        example="yes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "opioid_larger_amounts": "yes",
                "unsuccessful_cut_down": "yes",
                "time_obtaining_using": "no",
                "craving_desire": "yes",
                "failure_obligations": "no",
                "continued_despite_problems": "no",
                "activities_given_up": "no",
                "hazardous_situations": "no",
                "physical_psychological_problems": "yes",
                "tolerance": "yes",
                "withdrawal": "yes",
                "cows_score": 15,
                "treatment_readiness": "ready",
                "pregnancy_status": "no",
                "buprenorphine_waiver": "yes"
            }
        }


class EmbedResponse(BaseModel):
    """
    Response model for Emergency Department-Initiated Buprenorphine (EMBED) Assessment
    
    The EMBED assessment provides recommendations for buprenorphine treatment initiation:
    
    Results:
    - not_candidate: Patient does not meet criteria for ED-initiated buprenorphine
    - candidate_home_induction: Patient meets criteria but home induction recommended
    - candidate_ed_induction: Patient meets criteria for ED induction protocol
    
    Decision factors include:
    - DSM-5 OUD diagnosis (≥2 criteria required)
    - COWS score (>12 favors ED induction, ≤12 favors home induction)
    - Treatment readiness
    - Clinical contraindications (pregnancy, provider certification)
    
    Reference: D'Onofrio G, et al. J Gen Intern Med. 2017;32(6):660-666.
    """
    
    result: str = Field(
        ...,
        description="EMBED assessment result determining buprenorphine treatment approach (not_candidate, candidate_home_induction, candidate_ed_induction)",
        example="candidate_ed_induction"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="recommendation"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including OUD severity, withdrawal severity, and specific treatment recommendations",
        example="Patient meets all criteria for ED-initiated buprenorphine induction. OUD severity: Severe (6/11 criteria). Withdrawal severity: Moderate to Severe (COWS: 15). COWS >12 indicates moderate to severe withdrawal suitable for immediate ED induction. Proceed with ED induction protocol, monitor for precipitated withdrawal, and arrange follow-up care."
    )
    
    stage: str = Field(
        ...,
        description="Clinical recommendation category (Not Candidate, Candidate - Home Induction, Candidate - ED Induction)",
        example="Candidate - ED Induction"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the treatment recommendation",
        example="Candidate for emergency department induction"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "candidate_ed_induction",
                "unit": "recommendation",
                "interpretation": "Patient meets all criteria for ED-initiated buprenorphine induction. OUD severity: Severe (6/11 criteria). Withdrawal severity: Moderate to Severe (COWS: 15). COWS >12 indicates moderate to severe withdrawal suitable for immediate ED induction. Proceed with ED induction protocol, monitor for precipitated withdrawal, and arrange follow-up care.",
                "stage": "Candidate - ED Induction",
                "stage_description": "Candidate for emergency department induction"
            }
        }