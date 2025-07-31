"""
Abbreviated Mental Test 4 (AMT-4) Models

Request and response models for AMT-4 calculation.

References (Vancouver style):
1. Swain DG, Nightingale PG. Evaluation of a shortened version of the Abbreviated Mental Test 
   in a series of elderly patients. Clin Rehabil. 1997 Aug;11(3):243-8. 
   doi: 10.1177/026921559701100308.
2. Hodkinson HM. Evaluation of a mental test score for assessment of mental impairment in 
   the elderly. Age Ageing. 1972 Nov;1(4):233-8. doi: 10.1093/ageing/1.4.233.
3. Brooke P, Bullock R. Validation of a 6 item cognitive impairment test with a view to 
   primary care usage. Int J Geriatr Psychiatry. 1999 Nov;14(11):936-40.

The AMT-4 is a shortened version of the original 10-item Abbreviated Mental Test (AMT-10), 
developed by Dr. David G. Swain for rapid cognitive screening in elderly patients. It consists 
of four simple questions about age, date of birth, place, and year. A score of 4/4 indicates 
normal cognitive function, while scores <4 suggest cognitive impairment requiring further assessment.
"""

from pydantic import BaseModel, Field
from typing import Literal


class Amt4Request(BaseModel):
    """
    Request model for Abbreviated Mental Test 4 (AMT-4)
    
    The AMT-4 is a rapid cognitive screening tool consisting of four questions:
    
    Questions (each scored as correct/incorrect):
    1. Age - Patient correctly states their age (1 point if correct)
    2. Date of birth - Patient correctly states their date of birth (1 point if correct)
    3. Place - Patient correctly identifies current place/location (1 point if correct)
    4. Year - Patient correctly states the current year (1 point if correct)
    
    Scoring:
    - Each correct response scores 1 point
    - Total score ranges from 0 to 4 points
    - Score of 4/4 indicates normal cognitive function
    - Score <4 suggests cognitive impairment requiring further assessment
    
    Clinical Application:
    - Useful for rapid cognitive screening in emergency departments and acute care settings
    - Should not be used as sole diagnostic tool for dementia or cognitive disorders
    - False positives may occur with sensory impairments, language barriers, or severe illness
    
    References (Vancouver style):
    1. Swain DG, Nightingale PG. Evaluation of a shortened version of the Abbreviated Mental Test 
    in a series of elderly patients. Clin Rehabil. 1997 Aug;11(3):243-8. 
    doi: 10.1177/026921559701100308.
    2. Hodkinson HM. Evaluation of a mental test score for assessment of mental impairment in 
    the elderly. Age Ageing. 1972 Nov;1(4):233-8. doi: 10.1093/ageing/1.4.233.
    3. Brooke P, Bullock R. Validation of a 6 item cognitive impairment test with a view to 
    primary care usage. Int J Geriatr Psychiatry. 1999 Nov;14(11):936-40.
    """
    
    age: Literal["correct", "incorrect"] = Field(
        ...,
        description="Whether the patient correctly states their age. Scores 1 point if correct, 0 if incorrect",
        example="correct"
    )
    
    date_of_birth: Literal["correct", "incorrect"] = Field(
        ...,
        description="Whether the patient correctly states their date of birth. Scores 1 point if correct, 0 if incorrect",
        example="correct"
    )
    
    place: Literal["correct", "incorrect"] = Field(
        ...,
        description="Whether the patient correctly identifies their current place/location (e.g., hospital, home, clinic). Scores 1 point if correct, 0 if incorrect",
        example="correct"
    )
    
    year: Literal["correct", "incorrect"] = Field(
        ...,
        description="Whether the patient correctly states the current year. Scores 1 point if correct, 0 if incorrect",
        example="correct"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": "correct",
                "date_of_birth": "correct",
                "place": "correct",
                "year": "correct"
            }
        }


class Amt4Response(BaseModel):
    """
    Response model for Abbreviated Mental Test 4 (AMT-4)
    
    The AMT-4 score ranges from 0 to 4 points and indicates:
    - Score 4/4: Normal cognitive function - no cognitive impairment detected
    - Score <4: Cognitive impairment likely - further detailed assessment recommended
    
    The test is a rapid screening tool and should not be used as the sole diagnostic 
    criterion for dementia or other cognitive disorders.
    
    Reference: Swain DG, et al. Clin Rehabil. 1997;11(3):243-8.
    """
    
    result: int = Field(
        ...,
        description="AMT-4 score calculated from four cognitive questions (range: 0 to 4 points)",
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended next steps based on the score",
        example="Score of 4/4 suggests normal cognitive function. No cognitive impairment detected on this brief screening test."
    )
    
    stage: str = Field(
        ...,
        description="Cognitive assessment category (Normal Cognition or Cognitive Impairment)",
        example="Normal Cognition"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the cognitive status",
        example="Normal cognitive function"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "Score of 4/4 suggests normal cognitive function. No cognitive impairment detected on this brief screening test.",
                "stage": "Normal Cognition",
                "stage_description": "Normal cognitive function"
            }
        }