"""
Modified Bishop Score for Vaginal Delivery and Induction of Labor Models

Request and response models for Modified Bishop Score assessment.

References (Vancouver style):
1. Bishop EH. Pelvic scoring for elective induction. Obstet Gynecol. 1964 Aug;24:266-8. 
   PMID: 14199536.
2. Laughon SK, Zhang J, Troendle J, Sun L, Reddy UM. Using a simplified Bishop score to 
   predict vaginal delivery. Obstet Gynecol. 2011 Apr;117(4):805-11. 
   doi: 10.1097/AOG.0b013e3182114ad2.
3. Kolkman DG, Verhoeven CJ, Brinkhorst SJ, van der Post JA, Pajkrt E, Opmeer BC, et al. 
   The Bishop score as a predictor of labor induction success: a systematic review. 
   Am J Perinatol. 2013 Sep;30(8):625-30. doi: 10.1055/s-0032-1331024.

The Modified Bishop Score predicts likelihood of successful vaginal delivery by 
assessing cervical favorability for labor induction. It uses the traditional 
5 Bishop score components (dilation, effacement/length, station, position, 
consistency) plus additional clinical modifiers (parity, pre-eclampsia, 
postdate pregnancy, nulliparity, PPROM) to enhance predictive accuracy.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class ModifiedBishopScoreRequest(BaseModel):
    """
    Request model for Modified Bishop Score for Vaginal Delivery and Induction of Labor
    
    The Modified Bishop Score assesses cervical favorability for labor induction by 
    evaluating five cervical characteristics plus clinical modifiers:
    
    Primary Cervical Components:
    1. Cervical Dilation (0-6 points):
       - Closed: 0 points
       - 1-2 cm: 2 points
       - 3-4 cm: 4 points
       - >4 cm: 6 points
    
    2. Cervical Length (0-3 points):
       - 3 cm: 0 points
       - 2 cm: 1 point
       - 1 cm: 2 points
       - 0 cm (fully effaced): 3 points
    
    3. Fetal Station (0-3 points):
       - -3: 0 points
       - -2: 1 point
       - -1 or 0: 2 points
       - +1 or +2: 3 points
    
    4. Cervical Position (0-2 points):
       - Posterior: 0 points
       - Mid-position: 1 point
       - Anterior: 2 points
    
    5. Cervical Consistency (0-2 points):
       - Firm: 0 points
       - Medium: 1 point
       - Soft: 2 points
    
    Clinical Modifiers:
    - Prior vaginal deliveries: +1 point if yes
    - Pre-eclampsia: +1 point if yes
    - Postdate pregnancy: +1 point if yes
    - Nulliparity: -1 point if yes
    - PPROM: +1 point if yes
    
    Score Interpretation:
    - ≤5: Unfavorable cervix, consider cervical ripening
    - 6-7: Intermediate, clinical judgment required
    - ≥8: Favorable cervix, induction likely successful
    
    References (Vancouver style):
    1. Bishop EH. Pelvic scoring for elective induction. Obstet Gynecol. 1964 Aug;24:266-8.
    2. Laughon SK, Zhang J, Troendle J, Sun L, Reddy UM. Using a simplified Bishop score to 
       predict vaginal delivery. Obstet Gynecol. 2011 Apr;117(4):805-11.
    3. Kolkman DG, Verhoeven CJ, Brinkhorst SJ, van der Post JA, Pajkrt E, Opmeer BC, et al. 
       The Bishop score as a predictor of labor induction success: a systematic review. 
       Am J Perinatol. 2013 Sep;30(8):625-30.
    """
    
    cervical_dilation: Literal["closed", "1_2_cm", "3_4_cm", "greater_than_4_cm"] = Field(
        ...,
        description="Cervical dilation assessed on digital examination. Closed = 0 points, 1-2 cm = 2 points, 3-4 cm = 4 points, >4 cm = 6 points",
        example="1_2_cm"
    )
    
    cervical_length: Literal["3_cm", "2_cm", "1_cm", "0_cm"] = Field(
        ...,
        description="Cervical length (effacement) in centimeters. 3 cm = 0 points, 2 cm = 1 point, 1 cm = 2 points, 0 cm (fully effaced) = 3 points",
        example="2_cm"
    )
    
    fetal_station: Literal["minus_3", "minus_2", "minus_1_or_0", "plus_1_or_2"] = Field(
        ...,
        description="Fetal station relative to ischial spines. -3 = 0 points, -2 = 1 point, -1 or 0 = 2 points, +1 or +2 = 3 points",
        example="minus_2"
    )
    
    cervical_position: Literal["posterior", "mid_position", "anterior"] = Field(
        ...,
        description="Position of cervix in relation to fetal head. Posterior = 0 points, mid-position = 1 point, anterior = 2 points",
        example="mid_position"
    )
    
    cervical_consistency: Literal["firm", "medium", "soft"] = Field(
        ...,
        description="Consistency of cervix on palpation. Firm = 0 points, medium = 1 point, soft = 2 points",
        example="medium"
    )
    
    prior_vaginal_deliveries: Literal["yes", "no"] = Field(
        ...,
        description="History of prior successful vaginal deliveries. Adds 1 point if yes (increases likelihood of successful induction)",
        example="no"
    )
    
    preeclampsia: Literal["yes", "no"] = Field(
        ...,
        description="Current diagnosis of pre-eclampsia. Adds 1 point if yes (medical indication may influence induction success)",
        example="no"
    )
    
    postdate_pregnancy: Literal["yes", "no"] = Field(
        ...,
        description="Pregnancy beyond 42 weeks gestation (postdate). Adds 1 point if yes (cervical changes with prolonged pregnancy)",
        example="no"
    )
    
    nulliparity: Literal["yes", "no"] = Field(
        ...,
        description="First pregnancy (nulliparous patient). Subtracts 1 point if yes (nulliparous cervix less favorable for induction)",
        example="yes"
    )
    
    pprom: Literal["yes", "no"] = Field(
        ...,
        description="Preterm premature rupture of membranes (PPROM). Adds 1 point if yes (membrane rupture may facilitate cervical changes)",
        example="no"
    )
    
    @validator('nulliparity', always=True)
    def validate_nulliparity_consistency(cls, v, values):
        """Validate consistency between nulliparity and prior deliveries"""
        if 'prior_vaginal_deliveries' in values:
            if v == "yes" and values['prior_vaginal_deliveries'] == "yes":
                raise ValueError("Cannot be nulliparous (first pregnancy) and have prior vaginal deliveries")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "cervical_dilation": "1_2_cm",
                "cervical_length": "2_cm",
                "fetal_station": "minus_2",
                "cervical_position": "mid_position",
                "cervical_consistency": "medium",
                "prior_vaginal_deliveries": "no",
                "preeclampsia": "no",
                "postdate_pregnancy": "no",
                "nulliparity": "yes",
                "pprom": "no"
            }
        }


class ModifiedBishopScoreResponse(BaseModel):
    """
    Response model for Modified Bishop Score for Vaginal Delivery and Induction of Labor
    
    The Modified Bishop Score ranges from approximately -1 to 20 points and stratifies 
    cervical favorability for labor induction:
    
    Unfavorable Cervix (≤5 points):
    - Low likelihood of successful vaginal delivery
    - Consider cervical ripening agents before induction
    - Higher risk of failed induction and cesarean delivery
    - May require mechanical or pharmacological cervical preparation
    
    Intermediate Favorability (6-7 points):
    - Uncertain prediction for successful vaginal delivery
    - Clinical judgment required based on individual factors
    - Consider cervical ripening if time permits
    - Monitor closely during induction process
    
    Favorable Cervix (≥8 points):
    - High likelihood of successful vaginal delivery
    - Induction likely to be successful without cervical ripening
    - May proceed with oxytocin or amniotomy as appropriate
    - Good candidate for labor induction
    
    Clinical Considerations:
    - Score should be used in conjunction with clinical judgment
    - Individual patient factors may override score recommendations
    - Consider maternal preferences and delivery urgency
    - Reassess cervical status if induction delayed
    
    Reference: Bishop EH. Obstet Gynecol. 1964;24:266-8.
    """
    
    result: int = Field(
        ...,
        ge=-1,
        le=20,
        description="Modified Bishop Score indicating cervical favorability for delivery (approximately -1 to 20 points)",
        example=6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with likelihood assessment and management recommendations",
        example="Modified Bishop Score of 6 indicates intermediate cervical favorability. Uncertain prediction for successful vaginal delivery. Clinical judgment required based on individual patient factors, obstetric history, and indication for delivery."
    )
    
    stage: str = Field(
        ...,
        description="Cervical favorability category (Unfavorable, Intermediate, Favorable)",
        example="Intermediate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the favorability level",
        example="Intermediate favorability"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": "Modified Bishop Score of 6 indicates intermediate cervical favorability. Uncertain prediction for successful vaginal delivery. Clinical judgment required based on individual patient factors, obstetric history, and indication for delivery. Consider cervical ripening if time permits.",
                "stage": "Intermediate",
                "stage_description": "Intermediate favorability"
            }
        }