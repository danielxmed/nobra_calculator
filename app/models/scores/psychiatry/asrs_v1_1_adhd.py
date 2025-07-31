"""
Adult Self-Report Scale (ASRS v1.1) for ADHD Models

Request and response models for ASRS v1.1 ADHD screening calculation.

References (Vancouver style):
1. Kessler RC, Adler L, Ames M, Demler O, Faraone S, Hiripi E, et al. The World Health 
   Organization Adult ADHD Self-Report Scale (ASRS): a short screening scale for use in 
   the general population. Psychol Med. 2005 Feb;35(2):245-56. 
   doi: 10.1017/s0033291704002892.
2. Schweitzer JB, Cummins TK, Kant CA. Attention-deficit/hyperactivity disorder. 
   Med Clin North Am. 2001 May;85(3):757-77. doi: 10.1016/s0025-7125(05)70348-2.
3. Adler LA, Spencer T, Faraone SV, Kessler RC, Howes MJ, Biederman J, et al. 
   Validity of pilot Adult ADHD Self-Report Scale (ASRS) to Rate Adult ADHD symptoms. 
   Ann Clin Psychiatry. 2006 Jul-Sep;18(3):145-8. doi: 10.1080/10401230600801077.

The Adult Self-Report Scale (ASRS v1.1) is an 18-question screening tool developed 
in collaboration with the World Health Organization (WHO) and Harvard Medical School 
researchers to identify adult ADHD based on DSM-IV-TR criteria. The scale consists 
of two parts: Part A (questions 1-6) serves as the primary screener with weighted 
scoring, while Part B (questions 7-18) provides additional clinical information.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AsrsV11AdhdRequest(BaseModel):
    """
    Request model for Adult Self-Report Scale (ASRS v1.1) for ADHD
    
    The ASRS v1.1 is an 18-question self-report screening tool for adult ADHD 
    based on DSM-IV-TR criteria. It consists of two parts:
    
    Part A (Questions 1-6) - Primary Screener:
    Uses weighted scoring with specific thresholds for each question. A score 
    of ≥4 indicates positive screening for ADHD.
    
    Part B (Questions 7-18) - Additional Clinical Information:
    Provides supplementary symptom assessment for clinical evaluation.
    
    All questions assess symptom frequency over the past 6 months using a 
    5-point scale: Never, Rarely, Sometimes, Often, Very Often.
    
    The tool takes approximately 5 minutes to complete and is intended for 
    adults aged 18 years and older.

    References (Vancouver style):
    1. Kessler RC, Adler L, Ames M, Demler O, Faraone S, Hiripi E, et al. The World Health 
    Organization Adult ADHD Self-Report Scale (ASRS): a short screening scale for use in 
    the general population. Psychol Med. 2005 Feb;35(2):245-56. 
    doi: 10.1017/s0033291704002892.
    2. Schweitzer JB, Cummins TK, Kant CA. Attention-deficit/hyperactivity disorder. 
    Med Clin North Am. 2001 May;85(3):757-77. doi: 10.1016/s0025-7125(05)70348-2.
    3. Adler LA, Spencer T, Faraone SV, Kessler RC, Howes MJ, Biederman J, et al. 
    Validity of pilot Adult ADHD Self-Report Scale (ASRS) to Rate Adult ADHD symptoms. 
    Ann Clin Psychiatry. 2006 Jul-Sep;18(3):145-8. doi: 10.1080/10401230600801077.
    """
    
    # Part A - Primary Screener (Questions 1-6)
    q1_wrapping_details: Literal["never", "rarely", "sometimes", "often", "very_often"] = Field(
        ...,
        description="How often do you have trouble wrapping up the final details of a project, once the challenging parts have been done?",
        example="sometimes"
    )
    
    q2_organization: Literal["never", "rarely", "sometimes", "often", "very_often"] = Field(
        ...,
        description="How often do you have difficulty getting things in order when you have to do a task that requires organization?",
        example="often"
    )
    
    q3_appointments: Literal["never", "rarely", "sometimes", "often", "very_often"] = Field(
        ...,
        description="How often do you have problems remembering appointments or obligations?",
        example="sometimes"
    )
    
    q4_avoidance: Literal["never", "rarely", "sometimes", "often", "very_often"] = Field(
        ...,
        description="When you have a task that requires a lot of thought, how often do you avoid or delay getting started?",
        example="often"
    )
    
    q5_fidgeting: Literal["never", "rarely", "sometimes", "often", "very_often"] = Field(
        ...,
        description="How often do you fidget or squirm with your hands or feet when you have to sit down for a long time?",
        example="sometimes"
    )
    
    q6_hyperactivity: Literal["never", "rarely", "sometimes", "often", "very_often"] = Field(
        ...,
        description="How often do you feel overly active and compelled to do things, like you were driven by a motor?",
        example="rarely"
    )
    
    # Part B - Additional Clinical Information (Questions 7-18)
    q7_careless_mistakes: Literal["never", "rarely", "sometimes", "often", "very_often"] = Field(
        ...,
        description="How often do you make careless mistakes when you have to work on a boring or difficult project?",
        example="sometimes"
    )
    
    q8_attention_difficulty: Literal["never", "rarely", "sometimes", "often", "very_often"] = Field(
        ...,
        description="How often do you have difficulty keeping your attention when you are doing boring or repetitive work?",
        example="often"
    )
    
    q9_concentration: Literal["never", "rarely", "sometimes", "often", "very_often"] = Field(
        ...,
        description="How often do you have difficulty concentrating on what people say to you, even when they are speaking to you directly?",
        example="sometimes"
    )
    
    q10_misplacing: Literal["never", "rarely", "sometimes", "often", "very_often"] = Field(
        ...,
        description="How often do you misplace or have difficulty finding things at home or at work?",
        example="sometimes"
    )
    
    q11_distractibility: Literal["never", "rarely", "sometimes", "often", "very_often"] = Field(
        ...,
        description="How often are you distracted by activity or noise around you?",
        example="often"
    )
    
    q12_leaving_seat: Literal["never", "rarely", "sometimes", "often", "very_often"] = Field(
        ...,
        description="How often do you leave your seat in meetings or other situations in which you are expected to remain seated?",
        example="rarely"
    )
    
    q13_restlessness: Literal["never", "rarely", "sometimes", "often", "very_often"] = Field(
        ...,
        description="How often do you feel restless or fidgety?",
        example="sometimes"
    )
    
    q14_difficulty_relaxing: Literal["never", "rarely", "sometimes", "often", "very_often"] = Field(
        ...,
        description="How often do you have difficulty unwinding and relaxing when you have time to yourself?",
        example="sometimes"
    )
    
    q15_talking_too_much: Literal["never", "rarely", "sometimes", "often", "very_often"] = Field(
        ...,
        description="How often do you find yourself talking too much when you are in social situations?",
        example="rarely"
    )
    
    q16_finishing_sentences: Literal["never", "rarely", "sometimes", "often", "very_often"] = Field(
        ...,
        description="When you're in a conversation, how often do you find yourself finishing the sentences of the people you are talking to, before they can finish them themselves?",
        example="rarely"
    )
    
    q17_waiting_turn: Literal["never", "rarely", "sometimes", "often", "very_often"] = Field(
        ...,
        description="How often do you have difficulty waiting your turn in situations when turn taking is required?",
        example="sometimes"
    )
    
    q18_interrupting: Literal["never", "rarely", "sometimes", "often", "very_often"] = Field(
        ...,
        description="How often do you interrupt others when they are busy?",
        example="rarely"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "q1_wrapping_details": "sometimes",
                "q2_organization": "often",
                "q3_appointments": "sometimes",
                "q4_avoidance": "often",
                "q5_fidgeting": "sometimes",
                "q6_hyperactivity": "rarely",
                "q7_careless_mistakes": "sometimes",
                "q8_attention_difficulty": "often",
                "q9_concentration": "sometimes",
                "q10_misplacing": "sometimes",
                "q11_distractibility": "often",
                "q12_leaving_seat": "rarely",
                "q13_restlessness": "sometimes",
                "q14_difficulty_relaxing": "sometimes",
                "q15_talking_too_much": "rarely",
                "q16_finishing_sentences": "rarely",
                "q17_waiting_turn": "sometimes",
                "q18_interrupting": "rarely"
            }
        }


class AsrsV11AdhdResponse(BaseModel):
    """
    Response model for Adult Self-Report Scale (ASRS v1.1) for ADHD
    
    The ASRS v1.1 provides screening results based on Part A scoring:
    
    - Negative Screen (Part A <4): Symptoms less likely consistent with adult ADHD
    - Positive Screen (Part A ≥4): Symptoms highly consistent with adult ADHD, 
      further clinical evaluation warranted
    
    Part A uses weighted scoring with specific thresholds for each question based 
    on validation studies. Part B provides additional clinical information but 
    does not contribute to the screening decision.
    
    Reference: Kessler RC, et al. Psychol Med. 2005;35(2):245-56.
    """
    
    result: str = Field(
        ...,
        description="Formatted result showing Part A score (primary screener) and total score",
        example="Part A: 4/6 | Total: 42/72"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the scores",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommendations based on screening results",
        example="Screening positive for ADHD (Part A score: 4/6). Score ≥4 on Part A indicates symptoms highly consistent with adult ADHD. Further comprehensive clinical evaluation by a qualified healthcare professional is warranted to confirm diagnosis and determine appropriate treatment options."
    )
    
    stage: str = Field(
        ...,
        description="Screening result category (Negative Screen or Positive Screen)",
        example="Positive Screen"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the screening result",
        example="Possible ADHD"
    )
    
    part_a_score: int = Field(
        ...,
        ge=0,
        le=6,
        description="Part A score (primary screener, range 0-6). Score ≥4 indicates positive screening",
        example=4
    )
    
    part_b_total: int = Field(
        ...,
        ge=0,
        le=48,
        description="Part B total score (additional clinical information, range 0-48)",
        example=24
    )
    
    total_score: int = Field(
        ...,
        ge=0,
        le=72,
        description="Total score across all 18 questions (range 0-72, for clinical reference)",
        example=42
    )
    
    screening_positive: bool = Field(
        ...,
        description="Whether the screening is positive (Part A score ≥4)",
        example=True
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Part A: 4/6 | Total: 42/72",
                "unit": "points",
                "interpretation": "Screening positive for ADHD (Part A score: 4/6). Score ≥4 on Part A indicates symptoms highly consistent with adult ADHD. Further comprehensive clinical evaluation by a qualified healthcare professional is warranted to confirm diagnosis and determine appropriate treatment options.",
                "stage": "Positive Screen",
                "stage_description": "Possible ADHD",
                "part_a_score": 4,
                "part_b_total": 24,
                "total_score": 42,
                "screening_positive": True
            }
        }