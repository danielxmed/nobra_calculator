"""
Urticaria Activity Score (UAS) Models

Request and response models for Urticaria Activity Score calculation.

References (Vancouver style):
1. Młynek A, Zalewska-Janowska A, Martus P, et al. How to assess disease activity 
   in patients with chronic urticaria? Allergy. 2008;63(6):777-780.
2. Hawro T, Ohanyan T, Schoepke N, et al. The Urticaria Activity Score--Validity, 
   Reliability, and Responsiveness. J Allergy Clin Immunol Pract. 2018;6(4):1185-1190.e1.
3. Zuberbier T, Aberer W, Asero R, et al. The EAACI/GA²LEN/EDF/WAO Guideline for 
   the definition, classification, diagnosis, and management of urticaria: the 2014 
   revision. Allergy. 2014;69(7):868-887.

The Urticaria Activity Score (UAS) is a diary-based patient-reported outcome measure 
that assesses the key sign (hives/wheals) and symptom (itch/pruritus) of chronic 
spontaneous urticaria (CSU). The UAS7 score is calculated by summing daily scores 
over 7 consecutive days, providing a standardized measure for urticaria activity 
monitoring and treatment response assessment.

Scoring criteria:
- Wheals: 0=None, 1=Mild (<20/24h), 2=Moderate (20-50/24h), 3=Intense (>50/24h or confluent)
- Itch: 0=None, 1=Mild (present but not annoying), 2=Moderate (troublesome but doesn't interfere with activity), 3=Intense (severe, interferes with activity/sleep)

Clinical interpretation:
- UAS7 0: Urticaria-free
- UAS7 1-6: Well-controlled (very mild activity)
- UAS7 7-15: Mild activity
- UAS7 16-27: Moderate activity
- UAS7 28-42: Severe activity
"""

from pydantic import BaseModel, Field
from typing import Literal


class UrticariaActivityScoreRequest(BaseModel):
    """
    Request model for Urticaria Activity Score (UAS) calculation
    
    The UAS assesses urticaria severity through daily scoring of wheals (hives) and 
    itch intensity over 7 consecutive days. Each parameter is scored 0-3 daily.
    
    Wheals scoring (number of hives in past 24 hours):
    - 0: None
    - 1: Mild (<20 wheals/24 hours)
    - 2: Moderate (20-50 wheals/24 hours)  
    - 3: Intense (>50 wheals/24 hours or large confluent areas)
    
    Itch scoring (pruritus intensity in past 24 hours):
    - 0: None
    - 1: Mild (present but not annoying)
    - 2: Moderate (troublesome but doesn't interfere with daily activity)
    - 3: Intense (severe, interferes with daily activity or sleep)
    
    Daily UAS = wheals score + itch score (range 0-6 per day)
    UAS7 = sum of daily UAS scores over 7 days (range 0-42)
    
    The UAS7 score provides standardized assessment for:
    - Monitoring chronic spontaneous urticaria activity
    - Evaluating treatment response
    - Clinical trial endpoints
    - Treatment decision making
    
    References (Vancouver style):
    1. Młynek A, Zalewska-Janowska A, Martus P, et al. How to assess disease activity 
    in patients with chronic urticaria? Allergy. 2008;63(6):777-780.
    2. Hawro T, Ohanyan T, Schoepke N, et al. The Urticaria Activity Score--Validity, 
    Reliability, and Responsiveness. J Allergy Clin Immunol Pract. 2018;6(4):1185-1190.e1.
    3. Zuberbier T, Aberer W, Asero R, et al. The EAACI/GA²LEN/EDF/WAO Guideline for 
    the definition, classification, diagnosis, and management of urticaria: the 2014 
    revision. Allergy. 2014;69(7):868-887.
    """
    
    day1_wheals: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Day 1 - Number of wheals (hives) in past 24 hours. 0=None, 1=Mild (<20), 2=Moderate (20-50), 3=Intense (>50 or confluent)",
        example=2
    )
    
    day1_itch: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Day 1 - Itch intensity in past 24 hours. 0=None, 1=Mild (not annoying), 2=Moderate (troublesome), 3=Intense (interferes with activity/sleep)",
        example=2
    )
    
    day2_wheals: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Day 2 - Number of wheals (hives) in past 24 hours. 0=None, 1=Mild (<20), 2=Moderate (20-50), 3=Intense (>50 or confluent)",
        example=1
    )
    
    day2_itch: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Day 2 - Itch intensity in past 24 hours. 0=None, 1=Mild (not annoying), 2=Moderate (troublesome), 3=Intense (interferes with activity/sleep)",
        example=1
    )
    
    day3_wheals: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Day 3 - Number of wheals (hives) in past 24 hours. 0=None, 1=Mild (<20), 2=Moderate (20-50), 3=Intense (>50 or confluent)",
        example=2
    )
    
    day3_itch: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Day 3 - Itch intensity in past 24 hours. 0=None, 1=Mild (not annoying), 2=Moderate (troublesome), 3=Intense (interferes with activity/sleep)",
        example=1
    )
    
    day4_wheals: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Day 4 - Number of wheals (hives) in past 24 hours. 0=None, 1=Mild (<20), 2=Moderate (20-50), 3=Intense (>50 or confluent)",
        example=1
    )
    
    day4_itch: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Day 4 - Itch intensity in past 24 hours. 0=None, 1=Mild (not annoying), 2=Moderate (troublesome), 3=Intense (interferes with activity/sleep)",
        example=2
    )
    
    day5_wheals: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Day 5 - Number of wheals (hives) in past 24 hours. 0=None, 1=Mild (<20), 2=Moderate (20-50), 3=Intense (>50 or confluent)",
        example=0
    )
    
    day5_itch: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Day 5 - Itch intensity in past 24 hours. 0=None, 1=Mild (not annoying), 2=Moderate (troublesome), 3=Intense (interferes with activity/sleep)",
        example=1
    )
    
    day6_wheals: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Day 6 - Number of wheals (hives) in past 24 hours. 0=None, 1=Mild (<20), 2=Moderate (20-50), 3=Intense (>50 or confluent)",
        example=1
    )
    
    day6_itch: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Day 6 - Itch intensity in past 24 hours. 0=None, 1=Mild (not annoying), 2=Moderate (troublesome), 3=Intense (interferes with activity/sleep)",
        example=1
    )
    
    day7_wheals: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Day 7 - Number of wheals (hives) in past 24 hours. 0=None, 1=Mild (<20), 2=Moderate (20-50), 3=Intense (>50 or confluent)",
        example=1
    )
    
    day7_itch: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Day 7 - Itch intensity in past 24 hours. 0=None, 1=Mild (not annoying), 2=Moderate (troublesome), 3=Intense (interferes with activity/sleep)",
        example=0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "day1_wheals": 2,
                "day1_itch": 2,
                "day2_wheals": 1,
                "day2_itch": 1,
                "day3_wheals": 2,
                "day3_itch": 1,
                "day4_wheals": 1,
                "day4_itch": 2,
                "day5_wheals": 0,
                "day5_itch": 1,
                "day6_wheals": 1,
                "day6_itch": 1,
                "day7_wheals": 1,
                "day7_itch": 0
            }
        }


class UrticariaActivityScoreResponse(BaseModel):
    """
    Response model for Urticaria Activity Score (UAS) calculation
    
    Returns the UAS7 score (sum of daily scores over 7 days) with clinical interpretation.
    
    The UAS7 score ranges from 0-42 and is categorized as:
    - 0: Urticaria-free (no activity)
    - 1-6: Well-controlled (very mild activity)  
    - 7-15: Mild activity
    - 16-27: Moderate activity
    - 28-42: Severe activity
    
    Clinical significance:
    - UAS7 <7 generally indicates adequate disease control
    - UAS7 ≥11 suggests active disease (sensitivity 74%, specificity 86%)
    - UAS7 >28 indicates severe disease requiring intensive management
    
    The UAS is recommended by international guidelines for monitoring chronic 
    spontaneous urticaria and is the primary endpoint in clinical trials.
    
    Reference: Zuberbier T, et al. The EAACI/GA²LEN/EDF/WAO Guideline for urticaria. 
    Allergy. 2014;69(7):868-887.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=42,
        description="UAS7 score calculated as sum of daily scores over 7 consecutive days",
        example=12
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the UAS7 score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the UAS7 score with treatment recommendations and disease activity assessment",
        example="UAS7 score of 12/42 (average daily score: 1.7). Daily scores: 4, 2, 3, 3, 1, 2, 1. Mild urticaria activity that may require monitoring and potential adjustment of therapy. A UAS7 score <7 generally indicates adequate disease control, so scores in this range suggest mild but noticeable disease activity. This score suggests active disease requiring attention."
    )
    
    stage: str = Field(
        ...,
        description="Clinical severity category based on UAS7 score",
        example="Mild"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the severity category",
        example="Mild urticaria activity"
    )
    
    daily_scores: list[int] = Field(
        ...,
        description="Individual daily UAS scores (day 1 through day 7), each ranging from 0-6",
        example=[4, 2, 3, 3, 1, 2, 1]
    )
    
    average_daily_score: float = Field(
        ...,
        description="Average daily UAS score calculated as UAS7 total divided by 7 days",
        example=1.7
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 12,
                "unit": "points",
                "interpretation": "UAS7 score of 12/42 (average daily score: 1.7). Daily scores: 4, 2, 3, 3, 1, 2, 1. Mild urticaria activity that may require monitoring and potential adjustment of therapy. A UAS7 score <7 generally indicates adequate disease control, so scores in this range suggest mild but noticeable disease activity. This score suggests active disease requiring attention.",
                "stage": "Mild",
                "stage_description": "Mild urticaria activity",
                "daily_scores": [4, 2, 3, 3, 1, 2, 1],
                "average_daily_score": 1.7
            }
        }