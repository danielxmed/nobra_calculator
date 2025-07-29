"""
Barthel Index for Activities of Daily Living (ADL) Models

Request and response models for Barthel Index calculation.

References (Vancouver style):
1. Mahoney FI, Barthel DW. Functional evaluation: the Barthel Index. 
   Md State Med J. 1965 Feb;14:61-5.
2. Collin C, Wade DT, Davies S, Horne V. The Barthel ADL Index: a reliability 
   study. Int Disabil Stud. 1988;10(2):61-3. doi: 10.3109/09638288809164103.
3. Sainsbury A, Seebass G, Bansal A, Young JB. Reliability of the Barthel Index 
   when used with older people. Age Ageing. 2005 May;34(3):228-32. 
   doi: 10.1093/ageing/afi063.

The Barthel Index is the most widely used assessment tool for measuring performance 
in basic activities of daily living (ADL). It uses 10 items to measure functional 
independence in personal care and mobility, with scores ranging from 0 (totally 
dependent) to 100 (fully independent). It is particularly useful in rehabilitation 
settings and for monitoring functional recovery in stroke patients.
"""

from pydantic import BaseModel, Field
from typing import Literal


class BarthelIndexRequest(BaseModel):
    """
    Request model for Barthel Index for Activities of Daily Living (ADL)
    
    The Barthel Index assesses 10 activities of daily living:
    
    Activities and Scoring:
    1. Feeding (0-10 points)
    2. Bathing (0-5 points)
    3. Grooming (0-5 points)
    4. Dressing (0-10 points)
    5. Bowel control (0-10 points)
    6. Bladder control (0-10 points)
    7. Toilet use (0-10 points)
    8. Transfers (0-15 points)
    9. Mobility (0-15 points)
    10. Stairs (0-10 points)
    
    Total score: 0-100 points
    Higher scores indicate greater independence
    
    References (Vancouver style):
    1. Mahoney FI, Barthel DW. Functional evaluation: the Barthel Index. 
    Md State Med J. 1965 Feb;14:61-5.
    """
    
    feeding: Literal["independent", "needs_help", "unable"] = Field(
        ...,
        description="Feeding ability: Independent (10 pts) = can feed self from tray/table when food within reach; Needs help (5 pts) = needs help cutting, spreading butter, etc; Unable (0 pts) = dependent",
        example="independent"
    )
    
    bathing: Literal["independent", "unable"] = Field(
        ...,
        description="Bathing/shower ability: Independent (5 pts) = bathes self completely or needs help only with one body part; Unable (0 pts) = dependent",
        example="independent"
    )
    
    grooming: Literal["independent", "unable"] = Field(
        ...,
        description="Personal hygiene and grooming: Independent (5 pts) = washes face, combs hair, shaves, cleans teeth; Unable (0 pts) = needs help",
        example="independent"
    )
    
    dressing: Literal["independent", "needs_help", "unable"] = Field(
        ...,
        description="Dressing ability: Independent (10 pts) = gets clothes and dresses without assistance; Needs help (5 pts) = needs help but can do about half; Unable (0 pts) = dependent",
        example="needs_help"
    )
    
    bowel_control: Literal["continent", "occasional_accident", "incontinent"] = Field(
        ...,
        description="Bowel control: Continent (10 pts) = no accidents; Occasional accident (5 pts) = less than once per week; Incontinent (0 pts) = needs enemas or is incontinent",
        example="continent"
    )
    
    bladder_control: Literal["continent", "occasional_accident", "incontinent"] = Field(
        ...,
        description="Bladder control: Continent (10 pts) = no accidents; Occasional accident (5 pts) = less than once per day; Incontinent (0 pts) = incontinent or catheterized",
        example="continent"
    )
    
    toilet_use: Literal["independent", "needs_help", "unable"] = Field(
        ...,
        description="Toilet use: Independent (10 pts) = gets on/off toilet, handles clothes, wipes, flushes; Needs help (5 pts) = needs some help; Unable (0 pts) = dependent",
        example="independent"
    )
    
    transfers: Literal["independent", "needs_minor_help", "needs_major_help", "unable"] = Field(
        ...,
        description="Bed to chair transfers: Independent (15 pts); Needs minor help (10 pts) = verbal or physical assistance; Needs major help (5 pts) = can sit but needs lifting; Unable (0 pts) = no sitting balance",
        example="needs_minor_help"
    )
    
    mobility: Literal["independent", "walks_with_help", "wheelchair_independent", "immobile"] = Field(
        ...,
        description="Mobility on level surfaces: Independent >50 yards (15 pts); Walks with help >50 yards (10 pts); Wheelchair independent >50 yards (5 pts); Immobile <50 yards (0 pts)",
        example="walks_with_help"
    )
    
    stairs: Literal["independent", "needs_help", "unable"] = Field(
        ...,
        description="Stair climbing: Independent (10 pts) = up and down independently; Needs help (5 pts) = verbal, physical, or carrying aid; Unable (0 pts) = cannot",
        example="needs_help"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "feeding": "independent",
                "bathing": "independent",
                "grooming": "independent",
                "dressing": "needs_help",
                "bowel_control": "continent",
                "bladder_control": "continent",
                "toilet_use": "independent",
                "transfers": "needs_minor_help",
                "mobility": "walks_with_help",
                "stairs": "needs_help"
            }
        }


class BarthelIndexResponse(BaseModel):
    """
    Response model for Barthel Index for Activities of Daily Living (ADL)
    
    Score interpretation:
    - 80-100: Independent
    - 60-79: Minimally dependent
    - 40-59: Partially dependent
    - 20-39: Very dependent
    - 0-19: Totally dependent
    
    Reference: Mahoney FI, Barthel DW. Md State Med J. 1965;14:61-5.
    """
    
    result: int = Field(
        ...,
        description="Total Barthel Index score (0-100 points)",
        ge=0,
        le=100,
        example=75
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of functional independence level and care needs",
        example="Patient requires minimal assistance with daily activities. Generally able to live independently with some support."
    )
    
    stage: str = Field(
        ...,
        description="Functional independence category",
        example="Minimally Dependent"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the dependency level",
        example="Minimal dependency"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 75,
                "unit": "points",
                "interpretation": "Patient requires minimal assistance with daily activities. Generally able to live independently with some support.",
                "stage": "Minimally Dependent",
                "stage_description": "Minimal dependency"
            }
        }