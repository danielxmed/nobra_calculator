"""
Berg Balance Scale (BBS) Models

Request and response models for Berg Balance Scale calculation.

References (Vancouver style):
1. Berg KO, Wood-Dauphinee SL, Williams JI, Maki B. Measuring balance in the elderly: 
   validation of an instrument. Can J Public Health. 1992 Jul-Aug;83 Suppl 2:S7-11.
2. Berg K, Wood-Dauphinee S, Williams JI, Gayton D. Measuring balance in the elderly: 
   preliminary development of an instrument. Physiother Can. 1989;41:304-311.
3. Bogle Thorbahn LD, Newton RA. Use of the Berg Balance Scale to predict falls in 
   elderly persons. Phys Ther. 1996 Jun;76(6):576-83; discussion 584-5.

The Berg Balance Scale (BBS) is a 14-item objective measure designed to assess static 
balance and fall risk in adult populations, particularly community-dwelling older adults. 
Each task is scored from 0-4 points, with a maximum total score of 56 points.
"""

from pydantic import BaseModel, Field
from typing import Literal


class BergBalanceScaleRequest(BaseModel):
    """
    Request model for Berg Balance Scale (BBS)
    
    The BBS is a validated 14-item assessment tool designed to evaluate balance and 
    predict fall risk in older adults and patients with neurological conditions. 
    Each task is scored from 0-4 points based on the individual's ability to perform 
    the task safely and independently.
    
    **Assessment Guidelines:**
    - Takes approximately 15-20 minutes to complete
    - Requires equipment: 2 chairs, stopwatch, step/footstool, ruler, shoe/slipper
    - Each task scored 0-4 points (0=unable, 4=independent and safe)
    - Maximum total score: 56 points
    
    **Scoring Criteria:**
    - **4 points**: Able to perform task independently and safely
    - **3 points**: Able to perform with minimal difficulty or supervision
    - **2 points**: Able to perform with moderate difficulty
    - **1 point**: Able to perform with significant difficulty or assistance
    - **0 points**: Unable to perform task safely
    
    **Clinical Interpretation:**
    - **≥45 points**: Good balance, low fall risk
    - **41-44 points**: Moderate impairment, increased fall risk
    - **21-40 points**: Significant impairment, requires walking aid
    - **≤20 points**: Severe impairment, typically wheelchair bound
    
    **Target Population:**
    - Community-dwelling older adults (≥65 years)
    - Patients with stroke, Parkinson's disease, multiple sclerosis
    - Individuals with vestibular disorders or brain injury
    - Adults requiring balance and fall risk assessment
    
    **Psychometric Properties:**
    - Excellent inter-rater reliability (ICC = 0.95)
    - Strong test-retest reliability (ICC = 0.91)
    - Good concurrent validity with other balance measures
    - Predictive validity for fall risk established
    
    References (Vancouver style):
    1. Berg KO, Wood-Dauphinee SL, Williams JI, Maki B. Measuring balance in the elderly: 
    validation of an instrument. Can J Public Health. 1992 Jul-Aug;83 Suppl 2:S7-11.
    2. Berg K, Wood-Dauphinee S, Williams JI, Gayton D. Measuring balance in the elderly: 
    preliminary development of an instrument. Physiother Can. 1989;41:304-311.
    3. Bogle Thorbahn LD, Newton RA. Use of the Berg Balance Scale to predict falls in 
    elderly persons. Phys Ther. 1996 Jun;76(6):576-83; discussion 584-5.
    """
    
    sitting_to_standing: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Ability to move from sitting to standing position. 0=Unable without help, 1=Needs minimal help, 2=Able using hands after tries, 3=Able using hands, 4=Able without hands independently",
        example=4
    )
    
    standing_unsupported: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Ability to stand unsupported for 2 minutes. 0=Unable 30 seconds, 1=Needs tries for 30 seconds, 2=Able 30 seconds, 3=Able 2 minutes with supervision, 4=Able 2 minutes safely",
        example=4
    )
    
    sitting_unsupported: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Ability to sit unsupported for 2 minutes. 0=Unable 10 seconds, 1=Able 10 seconds, 2=Able 30 seconds, 3=Able 2 minutes supervised, 4=Able 2 minutes safely",
        example=4
    )
    
    standing_to_sitting: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Ability to sit down. 0=Needs help, 1=Uncontrolled descent, 2=Uses legs against chair, 3=Uses hands for control, 4=Sits safely minimal hands",
        example=4
    )
    
    transfers: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Ability to transfer between chairs. 0=Cannot transfer safely, 1=Needs help, 2=Needs verbal cuing/supervision, 3=Needs hands for support, 4=Transfers safely without hands",
        example=3
    )
    
    standing_eyes_closed: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Standing with eyes closed for 10 seconds. 0=Needs help, 1=Unable 3 seconds but steady, 2=Able 3 seconds, 3=Able 10 seconds supervised, 4=Able 10 seconds safely",
        example=3
    )
    
    standing_feet_together: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Standing with feet together. 0=Needs help, unable 15 seconds, 1=Needs help but stands 15 seconds, 2=Independent but unable 30 seconds, 3=Independent 1 minute supervised, 4=Independent 1 minute safely",
        example=3
    )
    
    reaching_forward: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Reaching forward with outstretched arm. 0=Loses balance/needs support, 1=Reaches but needs supervision, 2=Can reach >5cm safely, 3=Can reach >12.5cm safely, 4=Can reach >25cm confidently",
        example=4
    )
    
    picking_up_object: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Picking up object from floor. 0=Unable/needs help, 1=Unable but needs supervision, 2=Unable but reaches 2-5cm independently, 3=Able but needs supervision, 4=Able safely and easily",
        example=2
    )
    
    turning_to_look_behind: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Turning to look behind. 0=Needs assistance, 1=Needs supervision, 2=Turns sideways only but balanced, 3=Looks behind one side only, 4=Looks behind both sides with good weight shift",
        example=3
    )
    
    turning_360_degrees: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Turn 360 degrees. 0=Needs assistance, 1=Needs supervision/cuing, 2=Able safely but slowly, 3=Able one side <4 seconds, 4=Able both sides <4 seconds safely",
        example=2
    )
    
    placing_alternate_foot_on_step: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Placing alternate foot on step. 0=Needs assistance/unable, 1=Able once with supervision, 2=Able twice with minimal support, 3=Able 4 times unsupported but supervised, 4=Able 8 times independently",
        example=1
    )
    
    standing_one_foot_in_front: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Standing one foot in front. 0=Loses balance, 1=Needs help but holds 15 seconds, 2=Small step independently 30 seconds, 3=Able ahead independently 30 seconds, 4=Able tandem independently 30 seconds",
        example=2
    )
    
    standing_on_one_leg: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Standing on one leg. 0=Unable or <3 seconds, 1=Able lift but cannot hold >3 seconds, 2=Able >3 but <10 seconds, 3=Able 10+ but <30 seconds, 4=Able >30 seconds",
        example=1
    )
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "title": "Good balance (BBS = 54)",
                    "value": {
                        "sitting_to_standing": 4,
                        "standing_unsupported": 4,
                        "sitting_unsupported": 4,
                        "standing_to_sitting": 4,
                        "transfers": 4,
                        "standing_eyes_closed": 4,
                        "standing_feet_together": 4,
                        "reaching_forward": 4,
                        "picking_up_object": 4,
                        "turning_to_look_behind": 4,
                        "turning_360_degrees": 4,
                        "placing_alternate_foot_on_step": 3,
                        "standing_one_foot_in_front": 3,
                        "standing_on_one_leg": 2
                    }
                },
                {
                    "title": "Moderate impairment with fall risk (BBS = 42)",
                    "value": {
                        "sitting_to_standing": 4,
                        "standing_unsupported": 4,
                        "sitting_unsupported": 4,
                        "standing_to_sitting": 4,
                        "transfers": 3,
                        "standing_eyes_closed": 3,
                        "standing_feet_together": 3,
                        "reaching_forward": 4,
                        "picking_up_object": 2,
                        "turning_to_look_behind": 3,
                        "turning_360_degrees": 2,
                        "placing_alternate_foot_on_step": 1,
                        "standing_one_foot_in_front": 2,
                        "standing_on_one_leg": 1
                    }
                }
            ]
        }


class BergBalanceScaleResponse(BaseModel):
    """
    Response model for Berg Balance Scale (BBS)
    
    Returns the calculated BBS score with detailed interpretation including:
    - Balance level classification (Independent, Increased Fall Risk, Walking with Assistance, Wheelchair Bound)
    - Fall risk assessment based on validated cut-off scores
    - Performance summary showing areas of strength and concern
    - Clinical recommendations for management and intervention
    
    The BBS provides a comprehensive assessment of functional balance through 14 standardized 
    tasks, helping healthcare providers identify fall risk and guide intervention strategies 
    for older adults and patients with balance disorders.
    
    **Score Interpretation:**
    - **45-56 points**: Independent - Good balance, low fall risk
    - **41-44 points**: Increased Fall Risk - Moderate impairment
    - **21-40 points**: Walking with Assistance - Significant impairment
    - **0-20 points**: Wheelchair Bound - Severe impairment
    
    **Clinical Utility:**
    - Baseline assessment and progress monitoring
    - Fall risk screening and prevention planning
    - Rehabilitation goal setting and outcome measurement
    - Discharge planning and safety assessment
    
    Reference: The BBS is widely used in clinical practice and research for balance 
    assessment, with established reliability, validity, and predictive ability for 
    fall risk in diverse populations.
    """
    
    result: int = Field(
        ...,
        description="Berg Balance Scale total score from 14 tasks (0-56 points)",
        ge=0,
        le=56,
        example=42
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the BBS score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation including balance level, fall risk assessment, performance summary, and management recommendations",
        example="Berg Balance Scale score: 42/56 points. Performance summary: 8/14 tasks completed with maximum score, 4/14 tasks showing significant impairment (≤2 points). Areas of concern: Picking up object from floor, Turning 360 degrees, Placing alternate foot on step, Standing on one leg. MODERATE IMPAIRMENT: Score indicates moderate balance impairment with increased fall risk. Patient may benefit from balance training and fall prevention interventions. Clinical recommendations: Implement structured balance training program (e.g., Tai Chi, balance exercises). Consider physical therapy evaluation for individualized intervention plan. Assess need for assistive devices and home safety modifications. Regular monitoring and reassessment every 3-6 months. Review medications for fall risk factors. Educate patient and family on fall prevention strategies and warning signs."
    )
    
    stage: str = Field(
        ...,
        description="Balance classification (Independent, Increased Fall Risk, Walking with Assistance, Wheelchair Bound)",
        example="Increased Fall Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the balance level with fall risk indication",
        example="Moderate balance impairment with increased fall risk"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 42,
                "unit": "points",
                "interpretation": "Berg Balance Scale score: 42/56 points. Performance summary: 8/14 tasks completed with maximum score, 4/14 tasks showing significant impairment (≤2 points). Areas of concern: Picking up object from floor, Turning 360 degrees, Placing alternate foot on step, Standing on one leg. MODERATE IMPAIRMENT: Score indicates moderate balance impairment with increased fall risk. Patient may benefit from balance training and fall prevention interventions. Clinical recommendations: Implement structured balance training program (e.g., Tai Chi, balance exercises). Consider physical therapy evaluation for individualized intervention plan. Assess need for assistive devices and home safety modifications. Regular monitoring and reassessment every 3-6 months. Review medications for fall risk factors. Educate patient and family on fall prevention strategies and warning signs.",
                "stage": "Increased Fall Risk",
                "stage_description": "Moderate balance impairment with increased fall risk"
            }
        }