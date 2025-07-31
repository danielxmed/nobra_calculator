"""
Neck Disability Index (NDI) Models

Request and response models for NDI calculation.

References (Vancouver style):
1. Vernon H, Mior S. The Neck Disability Index: a study of reliability and validity. 
   J Manipulative Physiol Ther. 1991 Sep;14(7):409-15. PMID: 1834753.
2. Vernon H. The Neck Disability Index: state-of-the-art, 1991-2008. 
   J Manipulative Physiol Ther. 2008 Sep;31(7):491-502. doi: 10.1016/j.jmpt.2008.08.006.
3. MacDermid JC, Walton DM, Avery S, Blanchard A, Etruw E, McAlpine C, et al. 
   Measurement properties of the neck disability index: a systematic review. 
   J Orthop Sports Phys Ther. 2009 May;39(5):400-17. doi: 10.2519/jospt.2009.2930.

The NDI is a modification of the Oswestry Low Back Pain Disability Index and has been 
shown to be the most widely used and validated instrument for assessing self-rated 
disability in patients with neck pain. It consists of 10 domains of daily living, 
each scored 0-5, with higher scores indicating greater disability.
"""

from pydantic import BaseModel, Field
from typing import Literal


class NdiRequest(BaseModel):
    """
    Request model for Neck Disability Index (NDI)
    
    The NDI consists of 10 domains assessing functional limitations due to neck pain:
    
    1. Pain Intensity: Current pain level (0-5 points)
    2. Personal Care: Ability to wash, dress, etc. (0-5 points)
    3. Lifting: Ability to lift objects (0-5 points)
    4. Reading: Impact on reading activities (0-5 points)
    5. Headaches: Frequency and severity (0-5 points)
    6. Concentration: Ability to concentrate (0-5 points)
    7. Work: Work capacity (0-5 points)
    8. Driving: Ability to drive (0-5 points)
    9. Sleeping: Sleep quality (0-5 points)
    10. Recreation: Recreational activities (0-5 points)
    
    Each domain is scored from 0 (no disability) to 5 (complete disability).
    Total score ranges from 0-50 points.

    References (Vancouver style):
    1. Vernon H, Mior S. The Neck Disability Index: a study of reliability and validity. 
    J Manipulative Physiol Ther. 1991 Sep;14(7):409-15. PMID: 1834753.
    2. Vernon H. The Neck Disability Index: state-of-the-art, 1991-2008. 
    J Manipulative Physiol Ther. 2008 Sep;31(7):491-502. doi: 10.1016/j.jmpt.2008.08.006.
    """
    
    pain_intensity: Literal[0, 1, 2, 3, 4, 5] = Field(
        ...,
        description="Pain intensity: 0=No pain, 1=Very mild, 2=Moderate, 3=Fairly severe, 4=Very severe, 5=Worst imaginable",
        example=2
    )
    
    personal_care: Literal[0, 1, 2, 3, 4, 5] = Field(
        ...,
        description="Personal care (washing, dressing): 0=Normal without pain, 1=Normal with pain, 2=Painful and slow, 3=Need some help, 4=Need help daily, 5=Cannot dress/wash",
        example=1
    )
    
    lifting: Literal[0, 1, 2, 3, 4, 5] = Field(
        ...,
        description="Lifting: 0=Heavy weights without pain, 1=Heavy weights with pain, 2=Cannot lift from floor, 3=Only light/medium weights, 4=Only very light weights, 5=Cannot lift anything",
        example=2
    )
    
    reading: Literal[0, 1, 2, 3, 4, 5] = Field(
        ...,
        description="Reading: 0=No pain, 1=Slight pain, 2=Moderate pain, 3=Cannot read as much as wanted, 4=Can hardly read, 5=Cannot read at all",
        example=1
    )
    
    headaches: Literal[0, 1, 2, 3, 4, 5] = Field(
        ...,
        description="Headaches: 0=None, 1=Slight infrequent, 2=Moderate infrequent, 3=Moderate frequent, 4=Severe frequent, 5=Almost constant",
        example=1
    )
    
    concentration: Literal[0, 1, 2, 3, 4, 5] = Field(
        ...,
        description="Concentration: 0=No difficulty, 1=Slight difficulty, 2=Fair difficulty, 3=A lot of difficulty, 4=Great deal of difficulty, 5=Cannot concentrate",
        example=1
    )
    
    work: Literal[0, 1, 2, 3, 4, 5] = Field(
        ...,
        description="Work: 0=As much as wanted, 1=Usual work only, 2=Most of usual work, 3=Cannot do usual work, 4=Hardly any work, 5=Cannot work",
        example=1
    )
    
    driving: Literal[0, 1, 2, 3, 4, 5] = Field(
        ...,
        description="Driving: 0=No neck pain, 1=Slight pain, 2=Moderate pain, 3=Cannot drive as long as wanted, 4=Can hardly drive, 5=Cannot drive",
        example=0
    )
    
    sleeping: Literal[0, 1, 2, 3, 4, 5] = Field(
        ...,
        description="Sleeping: 0=No trouble, 1=Slightly disturbed (<1hr), 2=Mildly disturbed (1-2hr), 3=Moderately disturbed (2-3hr), 4=Greatly disturbed (3-5hr), 5=Completely disturbed (5-7hr)",
        example=1
    )
    
    recreation: Literal[0, 1, 2, 3, 4, 5] = Field(
        ...,
        description="Recreation: 0=All activities without pain, 1=All activities with some pain, 2=Most activities, 3=Few activities, 4=Hardly any activities, 5=No activities",
        example=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "pain_intensity": 2,
                "personal_care": 1,
                "lifting": 2,
                "reading": 1,
                "headaches": 1,
                "concentration": 1,
                "work": 1,
                "driving": 0,
                "sleeping": 1,
                "recreation": 1
            }
        }


class NdiResponse(BaseModel):
    """
    Response model for Neck Disability Index (NDI)
    
    The NDI score ranges from 0 to 50 points and classifies disability into:
    - 0-4 points (0-8%): No disability
    - 5-14 points (10-28%): Mild disability
    - 15-24 points (30-48%): Moderate disability
    - 25-34 points (50-68%): Severe disability
    - 35-50 points (70-100%): Complete disability
    
    Minimum clinically important difference (MCID): 5 points or 10%
    
    Reference: Vernon H. J Manipulative Physiol Ther. 2008;31(7):491-502.
    """
    
    result: int = Field(
        ...,
        description="NDI score calculated from 10 functional domains (range: 0-50 points)",
        example=11
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation based on disability level",
        example="The patient has mild neck-related disability. Most activities of daily living are not significantly affected, though some discomfort may be present."
    )
    
    stage: str = Field(
        ...,
        description="Disability level (None, Mild, Moderate, Severe, Complete)",
        example="Mild"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the disability level",
        example="Mild disability"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 11,
                "unit": "points",
                "interpretation": "The patient has mild neck-related disability. Most activities of daily living are not significantly affected, though some discomfort may be present.",
                "stage": "Mild",
                "stage_description": "Mild disability"
            }
        }