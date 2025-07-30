"""
CAGE Questions for Alcohol Use Models

Request and response models for CAGE Questions calculation.

References (Vancouver style):
1. Ewing JA. Detecting alcoholism: The CAGE questionnaire. JAMA. 1984 Oct 12;252(14):1905-7. 
   doi: 10.1001/jama.252.14.1905. PMID: 6471323.
2. Dhalla S, Kopec JA. The CAGE questionnaire for alcohol misuse: a review of reliability 
   and validity studies. Clin Invest Med. 2007;30(1):33-41. doi: 10.25011/cim.v30i1.447. 
   PMID: 17716538.
3. Williams N. The CAGE questionnaire. Occup Med (Lond). 2014 Oct;64(6):473-4. 
   doi: 10.1093/occmed/kqu058. PMID: 25146056.

The CAGE questionnaire is a widely used 4-question screening tool for detecting potential
alcohol use disorders. The acronym CAGE is derived from key words in each question:
Cut down, Annoyed, Guilty, and Eye-opener. A score of 2 or more indicates a positive
screen with >90% sensitivity for alcohol disorders.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class CageQuestionsRequest(BaseModel):
    """
    Request model for CAGE Questions for Alcohol Use
    
    The CAGE questionnaire consists of 4 yes/no questions that screen for 
    problematic alcohol use. Each "yes" answer scores 1 point:
    
    Cut down: Assesses recognition of problematic drinking
    - Indicates awareness that drinking may be excessive
    - Suggests internal conflict about alcohol consumption
    
    Annoyed: Evaluates defensive reactions to feedback
    - Reflects social consequences of drinking
    - May indicate denial or resistance to acknowledging problems
    
    Guilty: Explores emotional consequences
    - Suggests moral distress about drinking behavior
    - Can indicate awareness of negative impacts
    
    Eye-opener: Screens for physical dependence
    - Morning drinking to relieve withdrawal symptoms
    - Strong indicator of physiologic dependence
    - Even if isolated, warrants serious concern
    
    Clinical Context:
    - Designed for adults and adolescents >16 years
    - Takes <1 minute to administer
    - Recommended in primary care, ED, psychiatric, and hospital settings
    - Particularly important for at-risk populations (pregnant women, students, legal issues)
    
    References (Vancouver style):
    1. Ewing JA. Detecting alcoholism: The CAGE questionnaire. JAMA. 1984 Oct 12;252(14):1905-7.
    """
    
    cut_down: Literal["yes", "no"] = Field(
        ...,
        description="Have you ever felt you needed to Cut down on your drinking? Indicates recognition of problematic drinking patterns.",
        example="no"
    )
    
    annoyed: Literal["yes", "no"] = Field(
        ...,
        description="Have people Annoyed you by criticizing your drinking? Reflects defensive reactions to feedback about alcohol use.",
        example="no"
    )
    
    guilty: Literal["yes", "no"] = Field(
        ...,
        description="Have you ever felt Guilty about drinking? Explores emotional/moral distress related to alcohol consumption.",
        example="yes"
    )
    
    eye_opener: Literal["yes", "no"] = Field(
        ...,
        description="Have you ever felt you needed a drink first thing in the morning (Eye-opener) to steady your nerves or to get rid of a hangover? Strong indicator of physical dependence.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "cut_down": "no",
                "annoyed": "no",
                "guilty": "yes",
                "eye_opener": "no"
            }
        }


class CageQuestionsResponse(BaseModel):
    """
    Response model for CAGE Questions for Alcohol Use
    
    The CAGE score ranges from 0-4 points:
    
    Scoring:
    - 0-1 points: Negative screen
    - 2-4 points: Positive screen (>90% sensitivity for alcohol disorders)
    
    Special Considerations:
    - A positive eye-opener response alone is concerning for physical dependence
    - Score ≥2 warrants further evaluation with tools like AUDIT or clinical interview
    - This is a screening tool, not a diagnostic test
    
    Next Steps for Positive Screen:
    - Detailed alcohol history (quantity, frequency, pattern)
    - Physical examination for signs of alcohol use disorder
    - Laboratory testing (liver function, CBC, etc.)
    - Consider referral to addiction specialist
    - Use additional tools: AUDIT, MAST, or clinical interview
    
    Limitations:
    - Does not assess quantity or frequency of drinking
    - Cannot diagnose Alcohol Use Disorder without clinical assessment
    - May have lower sensitivity in certain populations
    
    Reference: Ewing JA. JAMA. 1984;252(14):1905-7.
    """
    
    result: int = Field(
        ...,
        description="CAGE score (0-4 points). Each 'yes' answer contributes 1 point.",
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation based on score and individual responses, especially eye-opener question",
        example="CAGE score of 1 indicates a negative screen. While alcohol use disorder is less likely, clinical judgment should be used, especially if clinical suspicion remains high. Consider discussing safe drinking limits (no more than 14 drinks per week for men, 7 for women) and potential risks with the patient. Reassess periodically, particularly if drinking patterns change or new concerns arise."
    )
    
    stage: str = Field(
        ...,
        description="Screening result category (Negative Screen or Positive Screen)",
        example="Negative Screen"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the screening result",
        example="Low likelihood of alcohol use disorder"
    )
    
    details: Dict[str, Any] = Field(
        ...,
        description="Detailed breakdown of responses and screening status",
        example={
            "cut_down": "no",
            "annoyed": "no",
            "guilty": "yes",
            "eye_opener": "no",
            "positive_screen": False
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "CAGE score of 1 indicates a negative screen. While alcohol use disorder is less likely, clinical judgment should be used, especially if clinical suspicion remains high. Consider discussing safe drinking limits (no more than 14 drinks per week for men, 7 for women) and potential risks with the patient. Reassess periodically, particularly if drinking patterns change or new concerns arise.",
                "stage": "Negative Screen",
                "stage_description": "Low likelihood of alcohol use disorder",
                "details": {
                    "cut_down": "no",
                    "annoyed": "no",
                    "guilty": "yes",
                    "eye_opener": "no",
                    "positive_screen": False
                }
            }
        }