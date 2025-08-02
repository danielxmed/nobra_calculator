"""
McMahon Score for Rhabdomyolysis Models

Request and response models for McMahon Score calculation.

References (Vancouver style):
1. McMahon GM, Zeng X, Waikar SS. A risk prediction score for kidney failure or mortality 
   in rhabdomyolysis. JAMA Intern Med. 2013 Oct 28;173(19):1821-8. 
   doi: 10.1001/jamainternmed.2013.9774.
2. Safari S, Yousefifard M, Hashemi B, Baratloo A, Forouzanfar MM, Rahmati F, et al. 
   The value of serum creatine kinase in predicting the risk of rhabdomyolysis-induced 
   acute kidney injury: a systematic review and meta-analysis. Clin Exp Nephrol. 
   2016 Apr;20(2):153-61. doi: 10.1007/s10157-015-1204-1.
3. Premru V, Kovač J, Buturović-Ponikvar J, Ponikvar R. Some kinetic considerations 
   in the treatment of acute kidney injury caused by rhabdomyolysis. Ther Apher Dial. 
   2017 Oct;21(5):451-456. doi: 10.1111/1744-9987.12547.
4. Rodriguez E, Soler MJ, Rap O, Barrios C, Orfila MA, Pascual J. Risk factors for 
   acute kidney injury in severe rhabdomyolysis. PLoS One. 2013 Dec 12;8(12):e82992. 
   doi: 10.1371/journal.pone.0082992.

The McMahon Score is a validated clinical prediction tool that helps identify patients 
with rhabdomyolysis at risk for severe outcomes including death or acute kidney injury 
requiring renal replacement therapy. Developed from a cohort of 2371 patients with 
CPK >5000 U/L, the score uses 8 clinical variables available on admission to stratify 
risk and guide early management decisions.
"""

from pydantic import BaseModel, Field
from typing import Literal


class McMahonScoreRequest(BaseModel):
    """
    Request model for McMahon Score for Rhabdomyolysis
    
    The McMahon Score uses 8 clinical variables to assess the risk of mortality or 
    acute kidney injury requiring renal replacement therapy in rhabdomyolysis patients:
    
    Demographic factors:
    - Age: ≤50 years (0 points), 51-70 years (1.5 points), 71-80 years (2.5 points), >80 years (3 points)
    - Sex: Male (0 points), Female (1 point)
    
    Laboratory values on admission:
    - Initial creatinine: <1.4 mg/dL (0 points), 1.4-2.2 mg/dL (1.5 points), >2.2 mg/dL (3 points)
    - Initial calcium <7.5 mg/dL: No (0 points), Yes (2 points)
    - Initial CPK >40,000 U/L: No (0 points), Yes (2 points)
    - Initial phosphate: <4.0 mg/dL (0 points), 4.0-5.4 mg/dL (1.5 points), >5.4 mg/dL (3 points)
    - Initial bicarbonate <19 mEq/L: No (0 points), Yes (2 points)
    
    Clinical context:
    - Rhabdomyolysis cause: Known causes including seizures, syncope, exercise, statins, 
      myositis (0 points) vs. Other causes (3 points)
    
    Scoring interpretation:
    - Score <6: Low risk (3% risk of death/AKI requiring RRT)
    - Score ≥6: Not low risk, consider aggressive renal protective therapy
    
    Note: The score was developed for patients with CPK >5,000 U/L within 3 days of admission.
    A score ≥6 is 68% specific and 86% sensitive for predicting need for RRT.
    
    References (Vancouver style):
    1. McMahon GM, Zeng X, Waikar SS. A risk prediction score for kidney failure or mortality 
       in rhabdomyolysis. JAMA Intern Med. 2013 Oct 28;173(19):1821-8. 
       doi: 10.1001/jamainternmed.2013.9774.
    2. Safari S, Yousefifard M, Hashemi B, Baratloo A, Forouzanfar MM, Rahmati F, et al. 
       The value of serum creatine kinase in predicting the risk of rhabdomyolysis-induced 
       acute kidney injury: a systematic review and meta-analysis. Clin Exp Nephrol. 
       2016 Apr;20(2):153-61. doi: 10.1007/s10157-015-1204-1.
    """
    
    age: Literal["<=50", "51-70", "71-80", ">80"] = Field(
        ...,
        description="Patient age category. ≤50 years scores 0 points, 51-70 years scores 1.5 points, 71-80 years scores 2.5 points, >80 years scores 3 points",
        example="51-70"
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient biological sex. Male scores 0 points, female scores 1 point",
        example="male"
    )
    
    initial_creatinine: Literal["<1.4", "1.4-2.2", ">2.2"] = Field(
        ...,
        description="Initial serum creatinine level in mg/dL. <1.4 scores 0 points, 1.4-2.2 scores 1.5 points, >2.2 scores 3 points",
        example="<1.4"
    )
    
    initial_calcium_low: Literal["yes", "no"] = Field(
        ...,
        description="Initial calcium less than 7.5 mg/dL. Hypocalcemia is common in rhabdomyolysis and indicates more severe disease. Scores 2 points if yes",
        example="no"
    )
    
    initial_cpk_high: Literal["yes", "no"] = Field(
        ...,
        description="Initial creatine phosphokinase (CPK) greater than 40,000 U/L. Very high CPK indicates more extensive muscle damage. Scores 2 points if yes",
        example="no"
    )
    
    rhabdo_cause: Literal["known_causes", "other_causes"] = Field(
        ...,
        description="Rhabdomyolysis etiology. Known causes (seizures, syncope, exercise, statins, myositis) score 0 points. Other causes (trauma, immobilization, drugs, infections, etc.) score 3 points",
        example="known_causes"
    )
    
    initial_phosphate: Literal["<4.0", "4.0-5.4", ">5.4"] = Field(
        ...,
        description="Initial phosphate level in mg/dL. <4.0 scores 0 points, 4.0-5.4 scores 1.5 points, >5.4 scores 3 points. Hyperphosphatemia indicates more severe muscle breakdown",
        example="<4.0"
    )
    
    initial_bicarbonate_low: Literal["yes", "no"] = Field(
        ...,
        description="Initial bicarbonate less than 19 mEq/L. Low bicarbonate indicates metabolic acidosis. Scores 2 points if yes",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": "51-70",
                "sex": "male",
                "initial_creatinine": "<1.4",
                "initial_calcium_low": "no",
                "initial_cpk_high": "no",
                "rhabdo_cause": "known_causes",
                "initial_phosphate": "<4.0",
                "initial_bicarbonate_low": "no"
            }
        }


class McMahonScoreResponse(BaseModel):
    """
    Response model for McMahon Score for Rhabdomyolysis
    
    The McMahon Score ranges from 0 to 17.5 points and stratifies patients into:
    - Low Risk (<6 points): 3% risk of death or AKI requiring RRT
    - Not Low Risk (≥6 points): Increased risk requiring aggressive management
    
    Clinical application:
    - Low-risk patients may be managed with standard supportive care
    - Not low-risk patients should receive aggressive fluid resuscitation and close monitoring
    - Early nephrology consultation recommended for scores ≥6
    - Score ≥6 is 68% specific and 86% sensitive for predicting need for RRT
    
    Reference: McMahon GM, et al. JAMA Intern Med. 2013;173(19):1821-8.
    """
    
    result: float = Field(
        ...,
        description="McMahon Score calculated from clinical variables (range: 0 to 17.5 points)",
        example=3.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on the score",
        example="3% risk of death or acute kidney injury requiring renal replacement therapy. Consider standard supportive care with fluid resuscitation and monitoring."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk or Not Low Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Low risk for death or AKI requiring RRT"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3.5,
                "unit": "points",
                "interpretation": "3% risk of death or acute kidney injury requiring renal replacement therapy. Consider standard supportive care with fluid resuscitation and monitoring.",
                "stage": "Low Risk",
                "stage_description": "Low risk for death or AKI requiring RRT"
            }
        }