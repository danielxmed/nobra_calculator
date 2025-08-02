"""
Migraine Treatment Optimization Questionnaire-4 (mTOQ-4) Models

Request and response models for mTOQ-4 calculation.

References (Vancouver style):
1. Lipton RB, Kolodner K, Bigal ME, Valade D, Láinez MJ, Pascual J, et al. Validity and 
   reliability of the migraine-treatment optimization questionnaire. Cephalalgia. 
   2009 Jul;29(7):751-9. doi: 10.1111/j.1468-2982.2008.01786.x. Epub 2009 Feb 5.
2. Lipton RB, Fanning KM, Serrano D, Reed ML, Cady R, Buse DC. Ineffective acute treatment 
   of episodic migraine is associated with new-onset chronic migraine. Neurology. 
   2015 Feb 17;84(7):688-95. doi: 10.1212/WNL.0000000000001256. Epub 2015 Jan 21.
3. Silberstein SD, Lipton RB, Dodick DW, Goadsby PJ, Freitag F, Mathew N, et al. Efficacy 
   and safety of topiramate for the treatment of chronic migraine: a randomized, double-blind, 
   placebo-controlled trial. Headache. 2007 Feb;47(2):170-80. doi: 10.1111/j.1526-4610.2006.00684.x.

The mTOQ-4 is a validated 4-item questionnaire that assesses the effectiveness of acute 
migraine treatment. It evaluates 2-hour pain freedom, 24-hour relief, ability to plan 
activities, and feeling in control after medication use.
"""

from pydantic import BaseModel, Field
from typing import Literal


class Mtoq4Request(BaseModel):
    """
    Request model for Migraine Treatment Optimization Questionnaire-4 (mTOQ-4)
    
    The mTOQ-4 assesses treatment effectiveness across 4 key domains:
    
    1. 2-Hour Pain Freedom: Rapid and complete pain relief
    2. 24-Hour Sustained Relief: Lasting effect without recurrence
    3. Ability to Plan: Confidence in treatment allows normal planning
    4. Feeling in Control: Return to normal function after treatment
    
    Clinical Context:
    Poor treatment optimization is associated with increased risk of progression 
    from episodic to chronic migraine. The mTOQ-4 helps identify patients who 
    would benefit from treatment modifications to prevent chronification.
    
    Scoring:
    Each question is scored 0-2 points based on frequency of positive response:
    - Never or rarely = 0 points
    - Less than half the time = 1 point
    - Half the time or greater = 2 points
    
    References (Vancouver style):
    1. Lipton RB, Kolodner K, Bigal ME, Valade D, Láinez MJ, Pascual J, et al. Validity and 
       reliability of the migraine-treatment optimization questionnaire. Cephalalgia. 
       2009 Jul;29(7):751-9. doi: 10.1111/j.1468-2982.2008.01786.x.
    """
    
    pain_free_2_hours: Literal["never_rarely", "less_than_half", "half_or_more"] = Field(
        ...,
        description="After taking your migraine medication, are you pain-free within 2 hours "
                    "for most attacks? This assesses rapid complete relief, a key treatment goal.",
        example="half_or_more"
    )
    
    relief_24_hours: Literal["never_rarely", "less_than_half", "half_or_more"] = Field(
        ...,
        description="Does 1 dose of your migraine medication usually relieve your headache and "
                    "keep it away for at least 24 hours? This assesses sustained relief without recurrence.",
        example="less_than_half"
    )
    
    able_to_plan: Literal["never_rarely", "less_than_half", "half_or_more"] = Field(
        ...,
        description="Are you comfortable enough with your migraine medication to be able to plan "
                    "your daily activities? This assesses confidence in treatment reliability.",
        example="less_than_half"
    )
    
    feel_in_control: Literal["never_rarely", "less_than_half", "half_or_more"] = Field(
        ...,
        description="After taking your migraine medication, do you feel in control of your migraines "
                    "enough so that you feel you can return to normal function? This assesses functional restoration.",
        example="half_or_more"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "pain_free_2_hours": "half_or_more",
                "relief_24_hours": "less_than_half",
                "able_to_plan": "less_than_half",
                "feel_in_control": "half_or_more"
            }
        }


class Mtoq4Response(BaseModel):
    """
    Response model for Migraine Treatment Optimization Questionnaire-4 (mTOQ-4)
    
    Treatment Efficacy Categories and Risk of Chronic Migraine:
    - Very Poor (0): 6.8% risk of progression to chronic migraine
    - Poor (1-5): 4.4% risk of progression to chronic migraine
    - Moderate (6-7): 2.7% risk of progression to chronic migraine
    - Maximum (8): 1.9% risk of progression to chronic migraine
    
    Clinical Action Points:
    - Scores <8 indicate suboptimal treatment requiring modification
    - Consider changing acute medication, dose, or route of administration
    - Add or optimize preventive therapy for frequent migraines
    - Reassess treatment effectiveness periodically
    
    Reference: Lipton RB, et al. Neurology. 2015;84(7):688-95.
    """
    
    result: int = Field(
        ...,
        description="mTOQ-4 total score (0-8 points). Higher scores indicate better treatment optimization.",
        example=5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with treatment recommendations and risk assessment",
        example="Current migraine treatment shows limited effectiveness. Recommend modifying acute treatment medication or dosing strategy. Patient has 4.4% risk of progression to chronic migraine. Consider preventive therapy."
    )
    
    stage: str = Field(
        ...,
        description="Treatment efficacy category (Very Poor, Poor, Moderate, Maximum)",
        example="Poor"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the treatment efficacy level",
        example="Poor treatment efficacy"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5,
                "unit": "points",
                "interpretation": "Current migraine treatment shows limited effectiveness. Recommend modifying acute treatment medication or dosing strategy. Patient has 4.4% risk of progression to chronic migraine. Consider preventive therapy.",
                "stage": "Poor",
                "stage_description": "Poor treatment efficacy"
            }
        }