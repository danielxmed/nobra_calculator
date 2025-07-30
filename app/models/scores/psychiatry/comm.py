"""
Current Opioid Misuse Measure (COMM) Models

Request and response models for COMM calculation.

References (Vancouver style):
1. Butler SF, Budman SH, Fernandez KC, et al. Development and validation of the Current 
   Opioid Misuse Measure. Pain. 2007;130(1-2):144-156. doi: 10.1016/j.pain.2007.01.014.
2. Butler SF, Budman SH, Fanciullo GJ, Jamison RN. Cross validation of the Current Opioid 
   Misuse Measure to monitor chronic pain patients on opioid therapy. Clin J Pain. 
   2010;26(9):770-776. doi: 10.1097/AJP.0b013e3181f195ba.
3. Meltzer EC, Rybin D, Saitz R, et al. Identifying prescription opioid use disorder in 
   primary care: diagnostic characteristics of the Current Opioid Misuse Measure (COMM). 
   Pain. 2011;152(2):397-402. doi: 10.1016/j.pain.2010.11.006.
4. Butler SF, Budman SH, Fanciullo GJ, Jamison RN. Development of a Brief Version of the 
   Current Opioid Misuse Measure (COMM): The COMM-9. Pain Med. 2019;20(1):113-118. 
   doi: 10.1093/pm/pny022.

The COMM is a validated self-report instrument for identifying and monitoring opioid 
misuse in chronic pain patients taking prescription opioids for pain management. It 
consists of 17 questions about behaviors in the past 30 days, each scored 0-4 points. 
A total score ≥9 indicates possible opioid misuse. The tool has excellent internal 
reliability (α = .86) and good test-retest reliability (ICC = .86).
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any, List


class CommRequest(BaseModel):
    """
    Request model for Current Opioid Misuse Measure (COMM)
    
    The COMM evaluates 17 behaviors over the past 30 days to identify potential opioid misuse 
    in patients on long-term opioid therapy. Each question is scored 0-4 points:
    
    **Scoring:**
    - 0 = Never
    - 1 = Seldom  
    - 2 = Sometimes
    - 3 = Often
    - 4 = Very often
    
    **Question Categories:**
    
    **Behavioral Indicators (5 questions):**
    - Taking medications differently than prescribed
    - Taking more medication than prescribed
    - Getting pain relief from other sources
    - Needing medications from others
    - Borrowing pain medication from others
    
    **Psychological Indicators (6 questions):**
    - Trouble thinking clearly or memory problems
    - Thoughts of self-harm
    - Time spent thinking about opioid medications
    - Being in arguments
    - Trouble controlling anger
    - Getting angry with people
    
    **Functional Indicators (1 question):**
    - Not completing necessary tasks
    
    **Healthcare Seeking (2 questions):**
    - Emergency clinic calls/visits
    - Emergency room visits
    
    **Substance Concerns (3 questions):**
    - Worried about handling medications
    - Others worried about medication handling
    - Using pain medicine for non-pain symptoms
    
    **Clinical Application:**
    - Total score ≥9 indicates possible opioid misuse (sensitivity 47%, specificity 89%)
    - Designed for patients already on long-term opioid therapy
    - Should be administered by healthcare professionals
    - Combines with clinical judgment for comprehensive assessment
    
    **Performance Characteristics:**
    - Area under curve: 0.84 (good discriminative ability)
    - Internal consistency: α = 0.86 (excellent)
    - Test-retest reliability: ICC = 0.86 (excellent)
    
    References (Vancouver style):
    1. Butler SF, Budman SH, Fernandez KC, et al. Development and validation of the Current 
       Opioid Misuse Measure. Pain. 2007;130(1-2):144-156. doi: 10.1016/j.pain.2007.01.014.
    2. Meltzer EC, Rybin D, Saitz R, et al. Identifying prescription opioid use disorder in 
       primary care: diagnostic characteristics of the Current Opioid Misuse Measure (COMM). 
       Pain. 2011;152(2):397-402. doi: 10.1016/j.pain.2010.11.006.
    """
    
    thinking_clearly: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="In the past 30 days, have you had trouble thinking clearly or memory problems? (0=Never, 1=Seldom, 2=Sometimes, 3=Often, 4=Very often)",
        example=1
    )
    
    not_completing_tasks: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="In the past 30 days, have people complained that you are not completing necessary tasks? (0=Never, 1=Seldom, 2=Sometimes, 3=Often, 4=Very often)",
        example=0
    )
    
    relief_other_sources: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="In the past 30 days, have you tried to get pain relief from sources other than your prescribing physician? (0=Never, 1=Seldom, 2=Sometimes, 3=Often, 4=Very often)",
        example=0
    )
    
    taking_differently: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="In the past 30 days, have you taken your medications differently than prescribed? (0=Never, 1=Seldom, 2=Sometimes, 3=Often, 4=Very often)",
        example=1
    )
    
    thinking_hurting_self: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="In the past 30 days, have you seriously thought about hurting yourself? (0=Never, 1=Seldom, 2=Sometimes, 3=Often, 4=Very often)",
        example=0
    )
    
    time_thinking_medications: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="In the past 30 days, how much time have you spent thinking about opioid medications? (0=Never, 1=Seldom, 2=Sometimes, 3=Often, 4=Very often)",
        example=2
    )
    
    being_in_arguments: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="In the past 30 days, have you been in arguments? (0=Never, 1=Seldom, 2=Sometimes, 3=Often, 4=Very often)",
        example=1
    )
    
    trouble_controlling_anger: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="In the past 30 days, have you had trouble controlling anger? (0=Never, 1=Seldom, 2=Sometimes, 3=Often, 4=Very often)",
        example=1
    )
    
    need_medications_from_others: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="In the past 30 days, have you had to take pain medications from someone else? (0=Never, 1=Seldom, 2=Sometimes, 3=Often, 4=Very often)",
        example=0
    )
    
    worried_handling_medications: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="In the past 30 days, have you been worried about how you are handling your medications? (0=Never, 1=Seldom, 2=Sometimes, 3=Often, 4=Very often)",
        example=1
    )
    
    others_worried_handling: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="In the past 30 days, have others been worried about how you are handling your medications? (0=Never, 1=Seldom, 2=Sometimes, 3=Often, 4=Very often)",
        example=0
    )
    
    emergency_clinic_visits: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="In the past 30 days, have you made emergency clinic calls or visits? (0=Never, 1=Seldom, 2=Sometimes, 3=Often, 4=Very often)",
        example=0
    )
    
    getting_angry_with_people: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="In the past 30 days, have you gotten angry with people? (0=Never, 1=Seldom, 2=Sometimes, 3=Often, 4=Very often)",
        example=1
    )
    
    taking_more_than_prescribed: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="In the past 30 days, have you taken more medication than prescribed? (0=Never, 1=Seldom, 2=Sometimes, 3=Often, 4=Very often)",
        example=0
    )
    
    borrowing_pain_medication: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="In the past 30 days, have you borrowed pain medication from others? (0=Never, 1=Seldom, 2=Sometimes, 3=Often, 4=Very often)",
        example=0
    )
    
    using_for_non_pain_symptoms: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="In the past 30 days, have you used pain medicine for symptoms other than pain? (0=Never, 1=Seldom, 2=Sometimes, 3=Often, 4=Very often)",
        example=0
    )
    
    visiting_emergency_room: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="In the past 30 days, have you visited the Emergency Room? (0=Never, 1=Seldom, 2=Sometimes, 3=Often, 4=Very often)",
        example=0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "thinking_clearly": 1,
                "not_completing_tasks": 0,
                "relief_other_sources": 0,
                "taking_differently": 1,
                "thinking_hurting_self": 0,
                "time_thinking_medications": 2,
                "being_in_arguments": 1,
                "trouble_controlling_anger": 1,
                "need_medications_from_others": 0,
                "worried_handling_medications": 1,
                "others_worried_handling": 0,
                "emergency_clinic_visits": 0,
                "getting_angry_with_people": 1,
                "taking_more_than_prescribed": 0,
                "borrowing_pain_medication": 0,
                "using_for_non_pain_symptoms": 0,
                "visiting_emergency_room": 0
            }
        }


class CommResponse(BaseModel):
    """
    Response model for Current Opioid Misuse Measure (COMM)
    
    Provides comprehensive assessment of opioid misuse risk based on patient-reported 
    behaviors in the past 30 days. The COMM score helps clinicians identify patients 
    who may be misusing prescription opioids and require enhanced monitoring or intervention.
    
    **Risk Categories:**
    - Low Risk (0-8): Not misusing medications, continue standard monitoring
    - High Risk (≥9): Possible misuse, enhanced monitoring and evaluation recommended
    
    **Clinical Action Points:**
    - Score ≥9: Consider substance abuse consultation, enhanced monitoring
    - Multiple red flags: Immediate clinical evaluation and intervention
    - Self-harm ideation: Immediate mental health evaluation
    
    Reference: Butler SF, et al. Pain. 2007;130(1-2):144-156.
    """
    
    result: int = Field(
        ...,
        description="COMM total score (sum of all 17 responses, range 0-68)",
        example=8
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of COMM results with recommendations",
        example="COMM total score of 8 is below the threshold (≥9) for opioid misuse risk. This suggests low probability of current opioid misuse behaviors. Patient demonstrates minimal pattern - few concerning behaviors. Continue standard monitoring and pain management protocols with routine reassessment."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on total score",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the risk category",
        example="Not misusing or abusing medications"
    )
    
    total_score: int = Field(
        ...,
        description="Total COMM score (0-68 points)",
        example=8
    )
    
    risk_level: str = Field(
        ...,
        description="Overall risk level (low or high)",
        example="low"
    )
    
    misuse_risk: str = Field(
        ...,
        description="Assessment of opioid misuse risk",
        example="Low risk for opioid misuse"
    )
    
    pattern_analysis: Dict[str, Any] = Field(
        ...,
        description="Analysis of response patterns across question categories",
        example={
            "category_scores": {
                "behavioral": {"score": 1, "max_possible": 20, "percentage": 5.0},
                "psychological": {"score": 6, "max_possible": 24, "percentage": 25.0}
            },
            "concerning_responses": 0,
            "moderate_responses": 1,
            "severity_pattern": "Minimal pattern - Few concerning behaviors"
        }
    )
    
    risk_factors: List[str] = Field(
        ...,
        description="Identified specific risk factors from responses",
        example=["Reports sometimes thinking about opioid medications"]
    )
    
    clinical_recommendations: List[str] = Field(
        ...,
        description="Clinical recommendations based on COMM assessment",
        example=[
            "Continue current pain management approach",
            "Routine monitoring with periodic COMM reassessment",
            "Standard opioid safety education and counseling"
        ]
    )
    
    monitoring_guidance: Dict[str, Any] = Field(
        ...,
        description="Monitoring recommendations including frequency and methods",
        example={
            "frequency": "Every 3-6 months or as clinically indicated",
            "intensity": "Standard monitoring",
            "methods": ["Clinical assessment", "COMM reassessment"],
            "additional_measures": "None routinely required"
        }
    )
    
    red_flags: List[str] = Field(
        ...,
        description="Immediate red flag indicators requiring urgent attention",
        example=[]
    )
    
    category_scores: Dict[str, Dict[str, Any]] = Field(
        ...,
        description="Scores breakdown by question categories",
        example={
            "behavioral": {"score": 1, "max_possible": 20, "percentage": 5.0, "questions_count": 5},
            "psychological": {"score": 6, "max_possible": 24, "percentage": 25.0, "questions_count": 6}
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 8,
                "unit": "points",
                "interpretation": "COMM total score of 8 is below the threshold (≥9) for opioid misuse risk. This suggests low probability of current opioid misuse behaviors. Patient demonstrates minimal pattern - few concerning behaviors. Continue standard monitoring and pain management protocols with routine reassessment.",
                "stage": "Low Risk",
                "stage_description": "Not misusing or abusing medications",
                "total_score": 8,
                "risk_level": "low",
                "misuse_risk": "Low risk for opioid misuse",
                "pattern_analysis": {
                    "category_scores": {
                        "behavioral": {"score": 1, "max_possible": 20, "percentage": 5.0, "questions_count": 5},
                        "psychological": {"score": 6, "max_possible": 24, "percentage": 25.0, "questions_count": 6},
                        "functional": {"score": 0, "max_possible": 4, "percentage": 0.0, "questions_count": 1},
                        "healthcare_seeking": {"score": 0, "max_possible": 8, "percentage": 0.0, "questions_count": 2},
                        "substance_concerns": {"score": 1, "max_possible": 12, "percentage": 8.3, "questions_count": 3}
                    },
                    "frequency_distribution": {"Never": 10, "Seldom": 6, "Sometimes": 1, "Often": 0, "Very often": 0},
                    "concerning_responses": 0,
                    "moderate_responses": 1,
                    "total_positive_responses": 7,
                    "severity_pattern": "Minimal pattern - Few concerning behaviors"
                },
                "risk_factors": ["Reports sometimes thinking about opioid medications"],
                "clinical_recommendations": [
                    "Continue current pain management approach",
                    "Routine monitoring with periodic COMM reassessment",
                    "Standard opioid safety education and counseling",
                    "Regular pain and function assessment"
                ],
                "monitoring_guidance": {
                    "frequency": "Every 3-6 months or as clinically indicated",
                    "intensity": "Standard monitoring",
                    "methods": ["Clinical assessment", "COMM reassessment", "Pain and function evaluation"],
                    "additional_measures": "None routinely required"
                },
                "red_flags": [],
                "category_scores": {
                    "behavioral": {"score": 1, "max_possible": 20, "percentage": 5.0, "questions_count": 5},
                    "psychological": {"score": 6, "max_possible": 24, "percentage": 25.0, "questions_count": 6},
                    "functional": {"score": 0, "max_possible": 4, "percentage": 0.0, "questions_count": 1},
                    "healthcare_seeking": {"score": 0, "max_possible": 8, "percentage": 0.0, "questions_count": 2},
                    "substance_concerns": {"score": 1, "max_possible": 12, "percentage": 8.3, "questions_count": 3}
                }
            }
        }