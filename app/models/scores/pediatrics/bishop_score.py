"""
Bishop Score for Vaginal Delivery and Induction of Labor Models

Request and response models for Bishop Score calculation.

References (Vancouver style):
1. Bishop EH. Pelvic scoring for elective induction. Obstet Gynecol. 1964 Aug;24:266-8.
2. Laughon SK, Zhang J, Troendle J, Sun L, Reddy UM. Using a simplified Bishop score 
   to predict vaginal delivery. Obstet Gynecol. 2011 Apr;117(4):805-11. 
   doi: 10.1097/AOG.0b013e31820dc6b3.
3. Crane JM. Factors predicting labor induction success: a critical analysis. 
   Clin Obstet Gynecol. 2006 Sep;49(3):573-84. doi: 10.1097/01.grf.0000236555.95579.1f.

The Bishop Score, developed by Dr. Edward Bishop in 1964, is a standardized 
pelvic scoring system used to assess cervical readiness for labor and predict 
the likelihood of successful vaginal delivery. It remains one of the most widely 
used assessment tools in obstetrics for evaluating cervical favorability before 
labor induction.

The score evaluates five key components through systematic pelvic examination:
cervical dilation, effacement (thinning), fetal station (descent), cervical 
position, and cervical consistency. Each component is assigned points based on 
objective findings, with the total score ranging from 0-13 points.

Clinical interpretation guides labor management decisions:
- Scores ≤5: Unfavorable cervix, consider cervical ripening before induction
- Scores 6-7: Indeterminate, use clinical judgment for timing
- Scores ≥8: Favorable cervix, good candidate for induction with high success rate

This scoring system helps clinicians make evidence-based decisions regarding 
timing of delivery, method of induction, and risk stratification for cesarean 
delivery, ultimately improving maternal and fetal outcomes.
"""

from pydantic import BaseModel, Field
from typing import Literal


class BishopScoreRequest(BaseModel):
    """
    Request model for Bishop Score for Vaginal Delivery and Induction of Labor
    
    The Bishop Score evaluates five cervical and fetal parameters through standardized 
    pelvic examination to predict successful vaginal delivery:
    
    **1. Cervical Dilation:**
    - **Closed (0 points)**: Cervical os is completely closed
    - **1-2 cm (1 point)**: Minimal cervical opening, admits fingertip
    - **3-4 cm (2 points)**: Moderate dilation, admits 1-2 fingers easily
    - **≥5 cm (3 points)**: Significant dilation, active labor pattern
    
    **2. Cervical Effacement (Thinning):**
    - **0-30% (0 points)**: Thick, uneffaced cervix, normal length
    - **40-50% (1 point)**: Mild thinning, moderate shortening
    - **60-70% (2 points)**: Significant thinning, marked shortening
    - **≥80% (3 points)**: Minimal cervical length, nearly completely thinned
    
    **3. Fetal Station (Descent):**
    - **-3 (0 points)**: Presenting part high above ischial spines
    - **-2 (1 point)**: Presenting part moderately high
    - **-1/0 (2 points)**: Presenting part at or near ischial spine level
    - **+1/+2 (3 points)**: Presenting part descended below ischial spines
    
    **4. Cervical Position:**
    - **Posterior (0 points)**: Cervix directed toward maternal back
    - **Mid-position (1 point)**: Cervix in intermediate position
    - **Anterior (2 points)**: Cervix directed toward maternal front, most favorable
    
    **5. Cervical Consistency:**
    - **Firm (0 points)**: Cervix feels firm like nasal tip
    - **Moderately firm (1 point)**: Intermediate consistency
    - **Soft (2 points)**: Cervix feels soft like lips, most favorable
    
    **Clinical Assessment Guidelines:**
    - Examination should be performed by experienced clinician
    - Use sterile technique with appropriate positioning
    - Assess systematically and document findings objectively
    - Consider maternal comfort and safety during examination
    - May require repeated assessments to track cervical changes
    
    **Timing Considerations:**
    - Typically assessed at 37+ weeks gestation when considering delivery
    - Most useful when evaluating candidates for labor induction
    - May be repeated during labor to track progress
    - Should not be used before term without obstetric consultation
    
    References (Vancouver style):
    1. Bishop EH. Pelvic scoring for elective induction. Obstet Gynecol. 1964 Aug;24:266-8.
    2. Laughon SK, Zhang J, Troendle J, Sun L, Reddy UM. Using a simplified Bishop score 
    to predict vaginal delivery. Obstet Gynecol. 2011 Apr;117(4):805-11. 
    doi: 10.1097/AOG.0b013e31820dc6b3.
    3. Crane JM. Factors predicting labor induction success: a critical analysis. 
    Clin Obstet Gynecol. 2006 Sep;49(3):573-84. doi: 10.1097/01.grf.0000236555.95579.1f.
    """
    
    cervical_dilation: Literal["closed", "1_2_cm", "3_4_cm", "5_or_more_cm"] = Field(
        ...,
        description="Cervical dilation measured in centimeters. Closed=0 points, 1-2cm=1 point, 3-4cm=2 points, ≥5cm=3 points.",
        example="1_2_cm"
    )
    
    cervical_effacement: Literal["0_30_percent", "40_50_percent", "60_70_percent", "80_or_more_percent"] = Field(
        ...,
        description="Cervical effacement (thinning) as percentage. 0-30%=0 points, 40-50%=1 point, 60-70%=2 points, ≥80%=3 points.",
        example="40_50_percent"
    )
    
    fetal_station: Literal["minus_3", "minus_2", "minus_1_or_0", "plus_1_or_2"] = Field(
        ...,
        description="Fetal station relative to ischial spines. -3=0 points, -2=1 point, -1/0=2 points, +1/+2=3 points.",
        example="minus_2"
    )
    
    cervical_position: Literal["posterior", "mid_position", "anterior"] = Field(
        ...,
        description="Position of cervix relative to vaginal axis. Posterior=0 points, mid-position=1 point, anterior=2 points.",
        example="mid_position"
    )
    
    cervical_consistency: Literal["firm", "moderately_firm", "soft"] = Field(
        ...,
        description="Consistency of cervix on palpation. Firm=0 points, moderately firm=1 point, soft=2 points.",
        example="moderately_firm"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "cervical_dilation": "1_2_cm",
                "cervical_effacement": "40_50_percent",
                "fetal_station": "minus_2",
                "cervical_position": "mid_position",
                "cervical_consistency": "moderately_firm"
            }
        }


class BishopScoreResponse(BaseModel):
    """
    Response model for Bishop Score for Vaginal Delivery and Induction of Labor
    
    The Bishop Score ranges from 0-13 points and classifies cervical favorability:
    
    **Unfavorable Cervix (≤5 points)**:
    - Low likelihood of successful vaginal delivery
    - Labor induction may be necessary
    - Consider cervical ripening agents before induction
    - Higher risk of cesarean delivery
    - Close monitoring required if induction attempted
    
    **Indeterminate (6-7 points)**:
    - Intermediate cervical favorability
    - Success of labor induction uncertain
    - Clinical judgment should guide decision-making
    - Consider individual patient factors and circumstances
    - May benefit from cervical ripening or expectant management
    
    **Favorable Cervix (≥8 points)**:
    - High likelihood of successful vaginal delivery
    - Spontaneous labor likely to occur soon
    - Labor induction has good chance of success
    - Low risk of cesarean delivery
    - Good candidate for elective induction if indicated
    
    **Clinical Implications:**
    - Guides timing and method of labor induction
    - Helps predict risk of cesarean delivery
    - Informs patient counseling and expectation setting
    - Assists in resource allocation and labor management planning
    
    Reference: Bishop EH. Obstet Gynecol. 1964;24:266-8.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=13,
        description="Bishop score calculated from cervical and fetal parameters (0-13 points)",
        example=5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the Bishop score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with management recommendations based on Bishop score",
        example="Unfavorable cervix with low likelihood of successful vaginal delivery. Labor induction may be necessary and cervical ripening agents should be considered before induction. Higher risk of cesarean delivery."
    )
    
    stage: str = Field(
        ...,
        description="Cervical favorability category (Unfavorable Cervix, Indeterminate, Favorable Cervix)",
        example="Unfavorable Cervix"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the cervical favorability category",
        example="Scores ≤5 suggest unfavorable cervix"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 5,
                "unit": "points",
                "interpretation": "Unfavorable cervix with low likelihood of successful vaginal delivery. Labor induction may be necessary and cervical ripening agents should be considered before induction. Higher risk of cesarean delivery.",
                "stage": "Unfavorable Cervix",
                "stage_description": "Scores ≤5 suggest unfavorable cervix"
            }
        }