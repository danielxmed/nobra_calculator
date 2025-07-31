"""
Adverse Childhood Experiences (ACE) Score Models

Request and response models for ACE Score calculation.

References (Vancouver style):
1. Felitti VJ, Anda RF, Nordenberg D, Williamson DF, Spitz AM, Edwards V, et al. 
   Relationship of childhood abuse and household dysfunction to many of the leading 
   causes of death in adults. The Adverse Childhood Experiences (ACE) Study. 
   Am J Prev Med. 1998;14(4):245-58. doi: 10.1016/s0749-3797(98)00017-8.
2. Anda RF, Felitti VJ, Bremner JD, Walker JD, Whitfield C, Perry BD, et al. 
   The enduring effects of abuse and related adverse experiences in childhood. 
   A convergence of evidence from neurobiology and epidemiology. Eur Arch Psychiatry 
   Clin Neurosci. 2006;256(3):174-86. doi: 10.1007/s00406-005-0624-4.
3. Hughes K, Bellis MA, Hardcastle KA, Sethi D, Butchart A, Mikton C, et al. 
   The effect of multiple adverse childhood experiences on health: a systematic 
   review and meta-analysis. Lancet Public Health. 2017;2(8):e356-e366. 
   doi: 10.1016/S2468-2667(17)30118-4.

The ACE Score is a screening tool that quantifies exposure to adverse childhood 
experiences during the first 18 years of life. It was developed from the seminal 
CDC-Kaiser Permanente study that found strong correlations between childhood trauma 
and adult health outcomes. The score ranges from 0-10, with each "yes" response 
adding one point to the total score.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AceScoreRequest(BaseModel):
    """
    Request model for Adverse Childhood Experiences (ACE) Score
    
    The ACE Score assesses 10 categories of adverse childhood experiences:
    
    Abuse Categories:
    - Emotional abuse: Verbal abuse or threats of physical harm
    - Physical abuse: Physical violence that caused marks or injury  
    - Sexual abuse: Sexual contact by someone ≥5 years older
    
    Neglect Categories:
    - Emotional neglect: Lack of love, support, or family closeness
    - Physical neglect: Inadequate food, clothing, protection, or medical care
    
    Household Dysfunction Categories:
    - Parental separation/divorce
    - Mother treated violently (domestic violence)
    - Household substance abuse (alcohol or drugs)
    - Household mental illness (depression, suicide attempts)
    - Household member incarceration
    
    Each category is scored as "yes" (1 point) or "no" (0 points), with total 
    scores ranging from 0-10. Higher scores indicate greater exposure to childhood 
    trauma and increased risk for adverse health outcomes in adulthood.

    References (Vancouver style):
    1. Felitti VJ, Anda RF, Nordenberg D, Williamson DF, Spitz AM, Edwards V, et al. 
    Relationship of childhood abuse and household dysfunction to many of the leading 
    causes of death in adults. The Adverse Childhood Experiences (ACE) Study. 
    Am J Prev Med. 1998;14(4):245-58. doi: 10.1016/s0749-3797(98)00017-8.
    2. Anda RF, Felitti VJ, Bremner JD, Walker JD, Whitfield C, Perry BD, et al. 
    The enduring effects of abuse and related adverse experiences in childhood. 
    A convergence of evidence from neurobiology and epidemiology. Eur Arch Psychiatry 
    Clin Neurosci. 2006;256(3):174-86. doi: 10.1007/s00406-005-0624-4.
    3. Hughes K, Bellis MA, Hardcastle KA, Sethi D, Butchart A, Mikton C, et al. 
    The effect of multiple adverse childhood experiences on health: a systematic 
    review and meta-analysis. Lancet Public Health. 2017;2(8):e356-e366. 
    doi: 10.1016/S2468-2667(17)30118-4.
    """
    
    emotional_abuse: Literal["yes", "no"] = Field(
        ...,
        description="Did a parent or other adult in the household often or very often swear at you, insult you, put you down, or humiliate you? OR act in a way that made you afraid that you might be physically hurt?",
        example="no"
    )
    
    physical_abuse: Literal["yes", "no"] = Field(
        ...,
        description="Did a parent or other adult in the household often or very often push, grab, slap, or throw something at you? OR ever hit you so hard that you had marks or were injured?",
        example="no"
    )
    
    sexual_abuse: Literal["yes", "no"] = Field(
        ...,
        description="Did an adult or person at least 5 years older than you ever touch or fondle you or have you touch their body in a sexual way? OR attempt or actually have oral, anal, or vaginal intercourse with you?",
        example="no"
    )
    
    emotional_neglect: Literal["yes", "no"] = Field(
        ...,
        description="Did you often or very often feel that no one in your family loved you or thought you were important or special? OR your family didn't look out for each other, feel close to each other, or support each other?",
        example="no"
    )
    
    physical_neglect: Literal["yes", "no"] = Field(
        ...,
        description="Did you often or very often feel that you didn't have enough to eat, had to wear dirty clothes, and had no one to protect you? OR your parents were too drunk or high to take care of you or take you to the doctor if you needed it?",
        example="no"
    )
    
    parental_separation: Literal["yes", "no"] = Field(
        ...,
        description="Were your parents ever separated or divorced?",
        example="yes"
    )
    
    mother_treated_violently: Literal["yes", "no"] = Field(
        ...,
        description="Was your mother or stepmother often or very often pushed, grabbed, slapped, or had something thrown at her? OR sometimes, often, or very often kicked, bitten, hit with a fist, or hit with something hard? OR ever repeatedly hit over at least a few minutes or threatened with a gun or knife?",
        example="no"
    )
    
    household_substance_abuse: Literal["yes", "no"] = Field(
        ...,
        description="Did you live with anyone who was a problem drinker or alcoholic or who used street drugs?",
        example="no"
    )
    
    household_mental_illness: Literal["yes", "no"] = Field(
        ...,
        description="Was a household member depressed or mentally ill, or did a household member attempt suicide?",
        example="no"
    )
    
    household_member_incarcerated: Literal["yes", "no"] = Field(
        ...,
        description="Did a household member go to prison?",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "emotional_abuse": "no",
                "physical_abuse": "no",
                "sexual_abuse": "no",
                "emotional_neglect": "no",
                "physical_neglect": "no",
                "parental_separation": "yes",
                "mother_treated_violently": "no",
                "household_substance_abuse": "no",
                "household_mental_illness": "no",
                "household_member_incarcerated": "no"
            }
        }


class AceScoreResponse(BaseModel):
    """
    Response model for Adverse Childhood Experiences (ACE) Score
    
    The ACE Score ranges from 0-10 points and provides risk stratification:
    - 0 points: No ACEs - Low risk for health problems
    - 1-3 points: Low to Moderate risk - Some increased risk exists
    - 4-5 points: High risk - Significant risk for health problems
    - 6+ points: Very High risk - Strong recommendation for trauma-informed care
    
    Higher ACE scores are associated with increased risks of:
    - Mental health disorders (depression, anxiety, PTSD, suicide)
    - Substance use disorders (alcohol, drugs, smoking)
    - Chronic diseases (heart disease, diabetes, cancer, stroke)
    - Risky behaviors (early sexual activity, multiple partners)
    - Social problems (unemployment, relationship difficulties)
    
    However, the ACE score is not deterministic - many people with high scores 
    lead healthy, productive lives, especially with appropriate support and 
    trauma-informed interventions.
    
    Reference: Felitti VJ, et al. Am J Prev Med. 1998;14(4):245-58.
    """
    
    result: int = Field(
        ...,
        description="ACE score calculated from adverse childhood experiences (range: 0-10 points)",
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and risk assessment based on the score",
        example="Moderate risk for health problems. While some increased risk exists, many people with scores in this range lead healthy lives. Protective factors and resilience can significantly mitigate risks."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (No ACEs, Low to Moderate, High, Very High)",
        example="Low to Moderate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="1-3 adverse childhood experiences"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "Moderate risk for health problems. While some increased risk exists, many people with scores in this range lead healthy lives. Protective factors and resilience can significantly mitigate risks.",
                "stage": "Low to Moderate",
                "stage_description": "1-3 adverse childhood experiences"
            }
        }