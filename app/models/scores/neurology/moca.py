"""
Montreal Cognitive Assessment (MoCA) Models

Request and response models for MoCA calculation.

References (Vancouver style):
1. Nasreddine ZS, Phillips NA, Bédirian V, Charbonneau S, Whitehead V, Collin I, et al. 
   The Montreal Cognitive Assessment, MoCA: a brief screening tool for mild cognitive 
   impairment. J Am Geriatr Soc. 2005;53(4):695-9. doi: 10.1111/j.1532-5415.2005.53221.x.
2. Luis CA, Keegan AP, Mullan M. Cross validation of the Montreal Cognitive Assessment 
   in community dwelling older adults residing in the Southeastern US. Int J Geriatr 
   Psychiatry. 2009;24(2):197-201. doi: 10.1002/gps.2101.
3. Roalf DR, Moberg PJ, Xie SX, Wolk DA, Moelter ST, Arnold SE. Comparative accuracies 
   of two common screening instruments for classification of Alzheimer's disease, mild 
   cognitive impairment, and healthy aging. Alzheimers Dement. 2013;9(5):529-37. 
   doi: 10.1016/j.jalz.2012.10.001.

The MoCA is a 30-point cognitive screening tool designed to detect mild cognitive 
impairment. It assesses multiple cognitive domains and is more sensitive than the 
MMSE for detecting mild cognitive impairment. The test takes approximately 10-15 
minutes to administer and includes an education adjustment factor.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MocaRequest(BaseModel):
    """
    Request model for Montreal Cognitive Assessment (MoCA)
    
    The MoCA assesses 8 cognitive domains with a total possible score of 30 points:
    
    1. Visuospatial/Executive Function (5 points):
       - Alternating Trail Making Task (1 point)
       - Cube Copy (1 point) 
       - Clock Drawing (3 points: contour=1, numbers=1, hands=1)
    
    2. Naming (3 points):
       - Lion (1 point)
       - Rhinoceros (1 point)
       - Camel (1 point)
    
    3. Memory Registration (5 points - NOT counted in total):
       - 5 words: Face, Velvet, Church, Daisy, Red
       - Used for delayed recall testing only
    
    4. Attention (6 points):
       - Forward Digit Span (1 point): ≥5 digits forward
       - Backward Digit Span (1 point): ≥3 digits backward
       - Vigilance Task (1 point): tap when hear letter 'A'
       - Serial 7s (3 points): 93, 86, 79, 72, 65 (1 point per correct subtraction, max 3)
    
    5. Language (3 points):
       - Sentence Repetition (2 points): 1 point each for 2 sentences
       - Phonemic Fluency (1 point): ≥11 words beginning with 'F' in 1 minute
    
    6. Abstraction (2 points):
       - Similarities: "What do they have in common?"
       - Train-bicycle (1 point): means of transportation
       - Watch-ruler (1 point): measuring instruments
    
    7. Delayed Recall (5 points):
       - Recall 5 words from memory registration (no cues)
       - Face, Velvet, Church, Daisy, Red (1 point each)
    
    8. Orientation (6 points):
       - Date (1 point), Month (1 point), Year (1 point)
       - Day of week (1 point), Place (1 point), City (1 point)
    
    Education Adjustment:
    - Add 1 point if formal education ≤12 years
    - Maximum total score remains 30 points
    
    Interpretation:
    - ≥26: Normal cognition
    - 18-25: Mild cognitive impairment 
    - 10-17: Moderate cognitive impairment
    - <10: Severe cognitive impairment

    References (Vancouver style):
    1. Nasreddine ZS, Phillips NA, Bédirian V, Charbonneau S, Whitehead V, Collin I, et al. 
    The Montreal Cognitive Assessment, MoCA: a brief screening tool for mild cognitive 
    impairment. J Am Geriatr Soc. 2005;53(4):695-9. doi: 10.1111/j.1532-5415.2005.53221.x.
    2. Luis CA, Keegan AP, Mullan M. Cross validation of the Montreal Cognitive Assessment 
    in community dwelling older adults residing in the Southeastern US. Int J Geriatr 
    Psychiatry. 2009;24(2):197-201. doi: 10.1002/gps.2101.
    3. Roalf DR, Moberg PJ, Xie SX, Wolk DA, Moelter ST, Arnold SE. Comparative accuracies 
    of two common screening instruments for classification of Alzheimer's disease, mild 
    cognitive impairment, and healthy aging. Alzheimers Dement. 2013;9(5):529-37. 
    doi: 10.1016/j.jalz.2012.10.001.
    """
    
    visuospatial_executive: int = Field(
        ...,
        ge=0,
        le=5,
        description="Visuospatial/Executive Function score: Alternating Trail Making (1pt) + Cube Copy (1pt) + Clock Drawing (3pts for contour, numbers, hands)",
        example=4
    )
    
    naming: int = Field(
        ...,
        ge=0,
        le=3,
        description="Naming score: Lion (1pt) + Rhinoceros (1pt) + Camel (1pt). Total 3 points for correctly naming all three animals",
        example=3
    )
    
    memory_registration: int = Field(
        ...,
        ge=0,
        le=5,
        description="Memory Registration score for 5 words (Face, Velvet, Church, Daisy, Red). NOT counted in total score but needed for delayed recall",
        example=5
    )
    
    attention: int = Field(
        ...,
        ge=0,
        le=6,
        description="Attention score: Forward Digit Span ≥5 digits (1pt) + Backward Digit Span ≥3 digits (1pt) + Vigilance Task letter A (1pt) + Serial 7s subtraction (3pts)",
        example=5
    )
    
    language: int = Field(
        ...,
        ge=0,
        le=3,
        description="Language score: Sentence Repetition 2 sentences (2pts) + Phonemic Fluency ≥11 words with F (1pt)",
        example=2
    )
    
    abstraction: int = Field(
        ...,
        ge=0,
        le=2,
        description="Abstraction score: Similarities between train-bicycle (1pt) and watch-ruler (1pt). Tests abstract thinking",
        example=2
    )
    
    delayed_recall: int = Field(
        ...,
        ge=0,
        le=5,
        description="Delayed Recall score: Recall 5 words from memory registration without cues (Face, Velvet, Church, Daisy, Red)",
        example=3
    )
    
    orientation: int = Field(
        ...,
        ge=0,
        le=6,
        description="Orientation score: Date (1pt) + Month (1pt) + Year (1pt) + Day of week (1pt) + Place (1pt) + City (1pt)",
        example=6
    )
    
    education_level: Literal["less_than_12_years", "12_or_more_years"] = Field(
        ...,
        description="Education level for score adjustment. Add 1 point if ≤12 years of formal education",
        example="12_or_more_years"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "visuospatial_executive": 4,
                "naming": 3,
                "memory_registration": 5,
                "attention": 5,
                "language": 2,
                "abstraction": 2,
                "delayed_recall": 3,
                "orientation": 6,
                "education_level": "12_or_more_years"
            }
        }


class MocaResponse(BaseModel):
    """
    Response model for Montreal Cognitive Assessment (MoCA)
    
    The MoCA total score ranges from 0-30 points (after education adjustment) and is interpreted as:
    - ≥26: Normal cognition - No cognitive impairment detected
    - 18-25: Mild cognitive impairment - Possible MCI, further evaluation recommended  
    - 10-17: Moderate cognitive impairment - Significant decline, comprehensive evaluation needed
    - <10: Severe cognitive impairment - Marked decline, immediate evaluation required
    
    Key Features:
    - More sensitive than MMSE for detecting mild cognitive impairment
    - Assesses multiple cognitive domains in 10-15 minutes
    - Education adjustment adds 1 point if ≤12 years formal education
    - Memory registration score not included in total (used for delayed recall only)
    - Cut-off of <26 suggests cognitive impairment requiring further evaluation
    - Validated across multiple populations and available in many languages
    
    Clinical Use:
    - Primary care screening for cognitive concerns
    - Monitoring cognitive changes over time
    - Research tool for MCI and dementia studies
    - Should be administered by trained healthcare professionals
    - Abnormal scores require comprehensive neuropsychological evaluation
    
    Reference: Nasreddine ZS, et al. J Am Geriatr Soc. 2005;53(4):695-9.
    """
    
    result: int = Field(
        ...,
        description="MoCA total score after education adjustment (range: 0-30 points)",
        example=25
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommendations based on the MoCA score",
        example="Possible mild cognitive impairment (MCI). This score suggests subtle cognitive changes that may affect daily functioning but do not meet criteria for dementia. Further comprehensive neuropsychological evaluation is recommended to confirm the diagnosis and identify specific cognitive domains affected."
    )
    
    stage: str = Field(
        ...,
        description="Cognitive status category (Normal Cognition, Mild Cognitive Impairment, Moderate Cognitive Impairment, Severe Cognitive Impairment)",
        example="Mild Cognitive Impairment"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the cognitive status level",
        example="Possible mild cognitive impairment"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 25,
                "unit": "points",
                "interpretation": "Possible mild cognitive impairment (MCI). This score suggests subtle cognitive changes that may affect daily functioning but do not meet criteria for dementia. Further comprehensive neuropsychological evaluation is recommended to confirm the diagnosis and identify specific cognitive domains affected.",
                "stage": "Mild Cognitive Impairment",
                "stage_description": "Possible mild cognitive impairment"
            }
        }