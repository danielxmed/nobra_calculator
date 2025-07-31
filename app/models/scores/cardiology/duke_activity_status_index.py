"""
Duke Activity Status Index (DASI) Models

Request and response models for Duke Activity Status Index calculation.

References (Vancouver style):
1. Hlatky MA, Boineau RE, Higginbotham MB, Lee KL, Mark DB, Califf RM, et al. 
   A brief self-administered questionnaire to determine functional capacity 
   (the Duke Activity Status Index). Am J Cardiol. 1989;64(10):651-4. 
   doi: 10.1016/0002-9149(89)90496-7.
2. Wijeysundera DN, Pearse RM, Shulman MA, Abbott TEF, Torres E, Ambosta A, et al. 
   Assessment of functional capacity before major non-cardiac surgery: an international, 
   prospective cohort study. Lancet. 2018;391(10140):2631-2640. 
   doi: 10.1016/S0140-6736(18)31131-0.
3. Struthers R, Erasmus P, Holmes K, Warman P, Collingwood A, Sneyd JR. Assessing 
   fitness for surgery: a comparison of questionnaire, incremental shuttle walk, and 
   cardiopulmonary exercise testing in general surgical patients. Br J Anaesth. 
   2008;101(6):774-80. doi: 10.1093/bja/aen310.

The Duke Activity Status Index (DASI) is a brief self-administered questionnaire 
that estimates functional capacity through assessment of 12 daily activities. 
Each activity has a specific weight based on its metabolic cost (MET value). 
The DASI score ranges from 0 to 58.2 points and correlates with VO2 max and 
estimated METs from cardiopulmonary exercise testing. A score ≥34 represents 
a threshold for reduced perioperative risk and complications.
"""

from pydantic import BaseModel, Field
from typing import Literal


class DukeActivityStatusIndexRequest(BaseModel):
    """
    Request model for Duke Activity Status Index (DASI)
    
    The DASI assesses functional capacity through 12 activities of daily living, 
    each weighted according to their metabolic equivalent of task (MET) values:
    
    Activity Categories and Weights:
    - Personal care (2.75 points): Basic self-care activities
    - Walking indoors (1.75 points): Basic mobility
    - Walking 1-2 blocks (2.75 points): Short-distance walking
    - Climbing stairs (5.50 points): Vertical mobility
    - Running short distance (8.00 points): Higher intensity activity
    - Light housework (2.70 points): Dusting, washing dishes
    - Moderate housework (3.50 points): Vacuuming, carrying groceries
    - Heavy housework (8.00 points): Scrubbing floors, moving furniture
    - Yard work (4.50 points): Raking, weeding, mowing
    - Sexual relations (5.25 points): Intimate physical activity
    - Moderate recreation (6.00 points): Golf, bowling, dancing, doubles tennis
    - Strenuous sports (7.50 points): Swimming, singles tennis, skiing
    
    Score Interpretation:
    - 0-19 points: Poor functional capacity (<4 METs, high perioperative risk)
    - 20-33 points: Moderate functional capacity (4-7 METs, intermediate risk)
    - 34-58.2 points: Good functional capacity (>7 METs, lower perioperative risk)
    
    Clinical Applications:
    - Preoperative risk assessment for intermediate and major surgery
    - Cardiovascular disease management and risk stratification
    - Quality of life assessment and treatment evaluation
    - Alternative to formal exercise testing when not feasible
    - Cardiac rehabilitation program assessment
    
    METs Estimation:
    Estimated METs = (DASI Score + 43.24) / 9.6

    References (Vancouver style):
    1. Hlatky MA, Boineau RE, Higginbotham MB, Lee KL, Mark DB, Califf RM, et al. 
       A brief self-administered questionnaire to determine functional capacity 
       (the Duke Activity Status Index). Am J Cardiol. 1989;64(10):651-4.
    2. Wijeysundera DN, Pearse RM, Shulman MA, Abbott TEF, Torres E, Ambosta A, et al. 
       Assessment of functional capacity before major non-cardiac surgery: an international, 
       prospective cohort study. Lancet. 2018;391(10140):2631-2640.
    3. Struthers R, Erasmus P, Holmes K, Warman P, Collingwood A, Sneyd JR. Assessing 
       fitness for surgery: a comparison of questionnaire, incremental shuttle walk, and 
       cardiopulmonary exercise testing in general surgical patients. Br J Anaesth. 
       2008;101(6):774-80.
    """
    
    personal_care: Literal["yes", "no"] = Field(
        ...,
        description="Can you take care of yourself, that is, eating, dressing, bathing, or using the toilet? Weight: 2.75 points",
        example="yes"
    )
    
    walk_indoors: Literal["yes", "no"] = Field(
        ...,
        description="Can you walk indoors, such as around your house? Weight: 1.75 points",
        example="yes"
    )
    
    walk_1_2_blocks: Literal["yes", "no"] = Field(
        ...,
        description="Can you walk a block or two on level ground? Weight: 2.75 points",
        example="yes"
    )
    
    climb_stairs: Literal["yes", "no"] = Field(
        ...,
        description="Can you climb a flight of stairs or walk up a hill? Weight: 5.50 points",
        example="yes"
    )
    
    run_short_distance: Literal["yes", "no"] = Field(
        ...,
        description="Can you run a short distance? Weight: 8.00 points",
        example="no"
    )
    
    light_housework: Literal["yes", "no"] = Field(
        ...,
        description="Can you do light work around the house like dusting or washing dishes? Weight: 2.70 points",
        example="yes"
    )
    
    moderate_housework: Literal["yes", "no"] = Field(
        ...,
        description="Can you do moderate work around the house like vacuuming, sweeping floors, or carrying in groceries? Weight: 3.50 points",
        example="yes"
    )
    
    heavy_housework: Literal["yes", "no"] = Field(
        ...,
        description="Can you do heavy work around the house like scrubbing floors or lifting or moving heavy furniture? Weight: 8.00 points",
        example="no"
    )
    
    yard_work: Literal["yes", "no"] = Field(
        ...,
        description="Can you do yard work like raking leaves, weeding, or pushing a power mower? Weight: 4.50 points",
        example="yes"
    )
    
    sexual_relations: Literal["yes", "no"] = Field(
        ...,
        description="Can you have sexual relations? Weight: 5.25 points",
        example="yes"
    )
    
    moderate_recreation: Literal["yes", "no"] = Field(
        ...,
        description="Can you participate in moderate recreational activities like golf, bowling, dancing, doubles tennis, or throwing a baseball or football? Weight: 6.00 points",
        example="no"
    )
    
    strenuous_sports: Literal["yes", "no"] = Field(
        ...,
        description="Can you participate in strenuous sports like swimming, singles tennis, football, basketball, or skiing? Weight: 7.50 points",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "personal_care": "yes",
                "walk_indoors": "yes",
                "walk_1_2_blocks": "yes",
                "climb_stairs": "yes",
                "run_short_distance": "no",
                "light_housework": "yes",
                "moderate_housework": "yes",
                "heavy_housework": "no",
                "yard_work": "yes",
                "sexual_relations": "yes",
                "moderate_recreation": "no",
                "strenuous_sports": "no"
            }
        }


class DukeActivityStatusIndexResponse(BaseModel):
    """
    Response model for Duke Activity Status Index (DASI)
    
    The DASI score ranges from 0 to 58.2 points and provides functional capacity assessment:
    
    Functional Capacity Categories:
    - Poor (0-19 points): Limited functional capacity
      * Estimated <4 METs
      * High perioperative risk for major surgery
      * Consider cardiopulmonary exercise testing and optimization
      * May require intensive perioperative monitoring
      * Associated with higher rates of postoperative complications
    
    - Moderate (20-33 points): Moderate functional capacity
      * Estimated 4-7 METs
      * Intermediate perioperative risk
      * Consider further cardiovascular evaluation before major surgery
      * May benefit from preoperative optimization
      * Adequate for most daily activities
    
    - Good (34-58.2 points): Good functional capacity
      * Estimated >7 METs
      * Lower perioperative risk
      * DASI ≥34 associated with reduced odds of adverse outcomes
      * Generally adequate for major surgery without additional testing
      * Associated with better quality of life and cardiovascular health
    
    Clinical Significance:
    - Score correlates with VO2 max and cardiopulmonary exercise test results
    - Threshold of 34 points identifies patients at reduced risk for:
      * 30-day death or myocardial injury
      * Moderate-to-severe postoperative complications
      * 1-year death or new disability
    - Higher scores indicate better cardiovascular fitness and exercise tolerance
    
    METs Estimation:
    - Estimated METs calculated using validated formula: (DASI + 43.24) / 9.6
    - METs represent multiples of resting metabolic rate
    - Useful for activity prescription and risk stratification
    - Correlates with formal exercise testing results
    
    Important Considerations:
    - Self-reported functional capacity may overestimate actual capacity
    - Should be interpreted in clinical context with other risk factors
    - May be limited by orthopedic, neurological, or other non-cardiac conditions
    - Consider objective testing if discordance with clinical presentation
    
    Reference: Hlatky MA, et al. Am J Cardiol. 1989;64(10):651-4.
    """
    
    result: float = Field(
        ...,
        description="DASI score (0-58.2 points)",
        example=25.2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommendations based on functional capacity",
        example="Moderate functional capacity with estimated 7.1 METs. Intermediate perioperative risk. Consider further cardiovascular evaluation if planning major surgery. May benefit from preoperative optimization."
    )
    
    stage: str = Field(
        ...,
        description="Functional capacity category (Poor, Moderate, Good)",
        example="Moderate Functional Capacity"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of functional capacity level",
        example="Moderate functional capacity (4-7 METs)"
    )
    
    estimated_mets: float = Field(
        ...,
        description="Estimated metabolic equivalent of tasks (METs) calculated from DASI score",
        example=7.1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 25.2,
                "unit": "points",
                "interpretation": "Moderate functional capacity with estimated 7.1 METs. Intermediate perioperative risk. Consider further cardiovascular evaluation if planning major surgery. May benefit from preoperative optimization.",
                "stage": "Moderate Functional Capacity",
                "stage_description": "Moderate functional capacity (4-7 METs)",
                "estimated_mets": 7.1
            }
        }