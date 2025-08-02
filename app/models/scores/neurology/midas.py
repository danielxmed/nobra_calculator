"""
Migraine Disability Assessment (MIDAS) Models

Request and response models for MIDAS calculation.

References (Vancouver style):
1. Stewart WF, Lipton RB, Kolodner K, Liberman J, Sawyer J. Reliability of the migraine 
   disability assessment score in a population-based sample of headache sufferers. 
   Cephalalgia. 1999 Mar;19(2):107-14; discussion 74. doi: 10.1046/j.1468-2982.1999.019002107.x.
2. Stewart WF, Lipton RB, Dowson AJ, Sawyer J. Development and testing of the Migraine 
   Disability Assessment (MIDAS) Questionnaire to assess headache-related disability. 
   Neurology. 2001;56(6 Suppl 1):S20-8. doi: 10.1212/wnl.56.suppl_1.s20.
3. Stewart WF, Lipton RB, Kolodner KB, Sawyer J, Lee C, Liberman JN. Validity of the 
   Migraine Disability Assessment (MIDAS) score in comparison to a diary-based measure 
   in a population sample of migraine sufferers. Pain. 2000 Oct;88(1):41-52. 
   doi: 10.1016/S0304-3959(00)00305-5.

The MIDAS is a 5-item questionnaire that quantifies headache-related disability over 
the past 3 months across work, household, and social domains. It helps physicians 
determine treatment strategies based on the functional impact of migraines.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class MidasRequest(BaseModel):
    """
    Request model for Migraine Disability Assessment (MIDAS)
    
    The MIDAS questionnaire measures disability across three domains over 3 months:
    
    Work/School Domain (Questions 1-2):
    - Days of complete activity loss (100% productivity loss)
    - Days of partial activity loss (≥50% productivity reduction)
    
    Household Work Domain (Questions 3-4):
    - Days unable to do household work
    - Days household productivity reduced by half or more
    
    Social/Leisure Domain (Question 5):
    - Days missed family, social, or leisure activities
    
    Clinical Application:
    The MIDAS helps identify patients who need preventive therapy and tracks treatment 
    response. A score ≥11 indicates moderate to severe disability warranting prophylaxis.
    
    Important Notes:
    - Each question asks about the PAST 3 MONTHS (90 days maximum)
    - Days are counted only once (no double counting across questions)
    - The tool also includes Questions A & B about headache frequency and intensity,
      but these are NOT included in the total score calculation
    
    References (Vancouver style):
    1. Stewart WF, Lipton RB, Kolodner K, Liberman J, Sawyer J. Reliability of the migraine 
       disability assessment score in a population-based sample of headache sufferers. 
       Cephalalgia. 1999 Mar;19(2):107-14; discussion 74. doi: 10.1046/j.1468-2982.1999.019002107.x.
    """
    
    missed_work_school: int = Field(
        ...,
        ge=0,
        le=90,
        description="On how many days in the last 3 months did you miss work or school because "
                    "of your headaches? (0-90 days). Count only days completely missed.",
        example=5
    )
    
    reduced_work_school: int = Field(
        ...,
        ge=0,
        le=90,
        description="How many days in the last 3 months was your productivity at work or school "
                    "reduced by half or more because of your headaches? (0-90 days). Do not "
                    "include days counted in Question 1.",
        example=10
    )
    
    missed_household: int = Field(
        ...,
        ge=0,
        le=90,
        description="On how many days in the last 3 months did you not do household work because "
                    "of your headaches? (0-90 days). Count days unable to do any household tasks.",
        example=3
    )
    
    reduced_household: int = Field(
        ...,
        ge=0,
        le=90,
        description="How many days in the last 3 months was your productivity in household work "
                    "reduced by half or more because of your headaches? (0-90 days). Do not "
                    "include days counted in Question 3.",
        example=8
    )
    
    missed_social: int = Field(
        ...,
        ge=0,
        le=90,
        description="On how many days in the last 3 months did you miss family, social, or "
                    "leisure activities because of your headaches? (0-90 days).",
        example=4
    )
    
    @validator('missed_work_school', 'reduced_work_school', 'missed_household', 
               'reduced_household', 'missed_social')
    def validate_days(cls, v):
        """Ensure days are whole numbers within 90-day period"""
        if not isinstance(v, int):
            raise ValueError(f"Value must be a whole number of days")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "missed_work_school": 5,
                "reduced_work_school": 10,
                "missed_household": 3,
                "reduced_household": 8,
                "missed_social": 4
            }
        }


class MidasResponse(BaseModel):
    """
    Response model for Migraine Disability Assessment (MIDAS)
    
    MIDAS Grades and Treatment Implications:
    - Grade I (0-5): Little/no disability - Simple analgesics, lifestyle changes
    - Grade II (6-10): Mild disability - Consider migraine-specific treatments
    - Grade III (11-20): Moderate disability - Recommend prophylaxis
    - Grade IV (≥21): Severe disability - Urgent need for prophylaxis + specialist referral
    
    Clinical Decision Support:
    Grades III-IV typically require preventive therapy in addition to acute treatment.
    The score can be repeated every 3 months to monitor treatment effectiveness.
    A reduction of ≥5 points or one grade level is considered clinically meaningful.
    
    Reference: Stewart WF, et al. Neurology. 2001;56(6 Suppl 1):S20-8.
    """
    
    result: int = Field(
        ...,
        description="MIDAS total score (0-270 points). Sum of all 5 questions.",
        example=30
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with treatment recommendations based on disability grade",
        example="Patient has severe headache-related disability. Urgent need for effective acute treatment and prophylaxis. Consider referral to headache specialist if not already under specialist care."
    )
    
    stage: str = Field(
        ...,
        description="MIDAS disability grade (Grade I-IV)",
        example="Grade IV"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the disability level",
        example="Severe disability"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 30,
                "unit": "points",
                "interpretation": "Patient has severe headache-related disability. Urgent need for effective acute treatment and prophylaxis. Consider referral to headache specialist if not already under specialist care.",
                "stage": "Grade IV",
                "stage_description": "Severe disability"
            }
        }