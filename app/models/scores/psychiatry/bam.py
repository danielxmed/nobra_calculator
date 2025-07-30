"""
Brief Addiction Monitor (BAM) Models

Request and response models for BAM calculation.

References (Vancouver style):
1. Cacciola JS, Alterman AI, DePhilippis D, Drapkin ML, Valadez C Jr, Fala NC, et al. 
   Development and initial evaluation of the Brief Addiction Monitor (BAM). J Subst 
   Abuse Treat. 2013 Mar;44(3):256-63. doi: 10.1016/j.jsat.2012.07.013.
2. Nelson KG, Young K, Chapman H. Examining the performance of the Brief Addiction 
   Monitor. J Subst Abuse Treat. 2014 Apr;46(4):472-81. doi: 10.1016/j.jsat.2013.07.002.
3. McDonell MG, Kerbrat AH, Comtois KA, Russo J, Lowe JM, Ries RK. Validation of the 
   Brief Addiction Monitor in United States Veterans with Substance Use Disorders. Addict 
   Behav. 2016 Dec;63:118-24. doi: 10.1016/j.addbeh.2016.07.011.

The BAM is a 17-item self-report instrument designed to monitor substance use behaviors 
and protective/risk factors in individuals with substance use disorders. It provides a 
comprehensive assessment of substance use, physical and mental health, social support, 
and recovery activities over the past 30 days.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class BamRequest(BaseModel):
    """
    Request model for Brief Addiction Monitor (BAM)
    
    The BAM uses 17 questions to assess substance use behaviors over the past 30 days:
    
    Response options for most questions:
    - 0: 0 days/Not at all
    - 1: 1-5 days/Slightly
    - 2: 6-10 days/Moderately
    - 3: 11-15 days/Considerably  
    - 4: 16-30 days/Extremely
    
    Physical health uses different scale:
    - 0: Poor
    - 1: Fair
    - 2: Good
    - 3: Very good
    - 4: Excellent
    
    Income adequate is binary:
    - 0: No
    - 4: Yes
    
    The BAM assesses three domains:
    1. Use Factors (Questions 4-7): Substance use frequency
    2. Risk Factors (Questions 1-3, 8, 11, 15): Health, cravings, risky situations
    3. Protective Factors (Questions 9-10, 12-14, 16-17): Recovery support and activities
    """
    
    physical_health: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="How would you say your physical health has been? (0=Poor, 1=Fair, 2=Good, 3=Very good, 4=Excellent)",
        example=2
    )
    
    sleep_troubles: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="How many nights have you had trouble falling asleep or staying asleep? (0=0 nights, 1=1-5, 2=6-10, 3=11-15, 4=16-30)",
        example=1
    )
    
    emotional_distress: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="How many days have you felt depressed, anxious, angry or very upset throughout most of the day? (0=0 days, 1=1-5, 2=6-10, 3=11-15, 4=16-30)",
        example=2
    )
    
    alcohol_use: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="How many days have you drunk ANY alcohol? (0=0 days, 1=1-5, 2=6-10, 3=11-15, 4=16-30)",
        example=0
    )
    
    alcohol_intoxication: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="How many days have you been drunk or intoxicated? (0=0 days, 1=1-5, 2=6-10, 3=11-15, 4=16-30)",
        example=0
    )
    
    illegal_drug_use: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="How many days have you used illegal drugs or abused prescribed medication? (0=0 days, 1=1-5, 2=6-10, 3=11-15, 4=16-30)",
        example=0
    )
    
    marijuana_use: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="How many days have you used marijuana (cannabis, pot, weed)? (0=0 days, 1=1-5, 2=6-10, 3=11-15, 4=16-30)",
        example=0
    )
    
    cravings: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="How much have you been bothered by cravings or urges to drink alcohol or use drugs? (0=Not at all, 1=Slightly, 2=Moderately, 3=Considerably, 4=Extremely)",
        example=1
    )
    
    abstinence_confidence: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="How confident are you in your ability to be completely abstinent (clean) from alcohol and drugs in the next 30 days? (0=Not at all, 1=Slightly, 2=Moderately, 3=Considerably, 4=Extremely)",
        example=3
    )
    
    self_help_attendance: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="How many days have you attended self-help meetings like AA or NA to support recovery? (0=0 days, 1=1-5, 2=6-10, 3=11-15, 4=16-30)",
        example=2
    )
    
    risky_situations: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="How many days were you in situations or with people that might put you at an increased risk for using alcohol or drugs? (0=0 days, 1=1-5, 2=6-10, 3=11-15, 4=16-30)",
        example=1
    )
    
    spiritual_support: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="How much does your religion or spirituality help support your recovery? (0=Not at all, 1=Slightly, 2=Moderately, 3=Considerably, 4=Extremely)",
        example=2
    )
    
    work_participation: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="How many days did you attend work, school, or volunteer activities? (0=0 days, 1=1-5, 2=6-10, 3=11-15, 4=16-30)",
        example=4
    )
    
    income_adequate: Literal[0, 4] = Field(
        ...,
        description="Do you have enough income (from legal sources) to pay for necessities? (0=No, 4=Yes)",
        example=4
    )
    
    family_conflicts: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="How stressful have things been between you and your family and/or significant others? (0=Not at all, 1=Slightly, 2=Moderately, 3=Considerably, 4=Extremely)",
        example=1
    )
    
    social_support: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="How many days have you been in contact or spent time with family and/or friends who are supportive of your recovery? (0=0 days, 1=1-5, 2=6-10, 3=11-15, 4=16-30)",
        example=3
    )
    
    recovery_satisfaction: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="How satisfied are you with your progress toward achieving your recovery goals? (0=Not at all, 1=Slightly, 2=Moderately, 3=Considerably, 4=Extremely)",
        example=3
    )
    
    class Config:
        schema_extra = {
            "example": {
                "physical_health": 2,
                "sleep_troubles": 1,
                "emotional_distress": 2,
                "alcohol_use": 0,
                "alcohol_intoxication": 0,
                "illegal_drug_use": 0,
                "marijuana_use": 0,
                "cravings": 1,
                "abstinence_confidence": 3,
                "self_help_attendance": 2,
                "risky_situations": 1,
                "spiritual_support": 2,
                "work_participation": 4,
                "income_adequate": 4,
                "family_conflicts": 1,
                "social_support": 3,
                "recovery_satisfaction": 3
            }
        }


class BamResponse(BaseModel):
    """
    Response model for Brief Addiction Monitor (BAM)
    
    The BAM total score ranges from 0-68 points with three subscales:
    - Use Factors (0-16): Higher scores indicate more substance use
    - Risk Factors (0-24): Higher scores indicate more risk factors
    - Protective Factors (0-28): Higher scores indicate fewer protective factors
    
    Reference: Cacciola JS, et al. J Subst Abuse Treat. 2013;44(3):256-63.
    """
    
    result: int = Field(
        ...,
        description="Total BAM score (range: 0-68 points)",
        example=25
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the BAM score and subscales",
        example="Minimal substance use reported. Moderate risk factors present. Moderate protective factors present. Overall low severity profile suggesting good recovery status."
    )
    
    stage: str = Field(
        ...,
        description="Assessment status",
        example="Assessment Complete"
    )
    
    stage_description: str = Field(
        ...,
        description="Summary of total and subscale scores",
        example="Total: 25, Use: 0, Risk: 10, Protective: 15"
    )
    
    subscales: Dict[str, int] = Field(
        ...,
        description="Subscale scores for use factors, risk factors, and protective factors",
        example={"use_factors": 0, "risk_factors": 10, "protective_factors": 15}
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 25,
                "unit": "points",
                "interpretation": "Minimal substance use reported. Moderate risk factors present. Moderate protective factors present. Overall low severity profile suggesting good recovery status.",
                "stage": "Assessment Complete",
                "stage_description": "Total: 25, Use: 0, Risk: 10, Protective: 15",
                "subscales": {
                    "use_factors": 0,
                    "risk_factors": 10,
                    "protective_factors": 15
                }
            }
        }