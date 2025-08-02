"""
Wexner Score for Obstructed Defecation Syndrome (ODS) Models

Request and response models for Wexner Score calculation.

References (Vancouver style):
1. Jorge JM, Wexner SD. Etiology and management of fecal incontinence. 
   Dis Colon Rectum. 1993;36(1):77-97. doi: 10.1007/BF02050307
2. Rockwood TH, Church JM, Fleshman JW, et al. Fecal Incontinence Quality of Life Scale: 
   quality of life instrument for patients with fecal incontinence. Dis Colon Rectum. 
   2000;43(1):9-16. doi: 10.1007/BF02237236
3. Vaizey CJ, Carapeti E, Cahill JA, Kamm MA. Prospective comparison of faecal 
   incontinence grading systems. Gut. 1999;44(1):77-80. doi: 10.1136/gut.44.1.77
4. Bharucha AE, Dunivan G, Goode PS, et al. Epidemiology, pathophysiology, and 
   classification of fecal incontinence: state of the science summary for the National 
   Institute of Diabetes and Digestive and Kidney Diseases (NIDDK) workshop. Am J 
   Gastroenterol. 2015;110(1):127-136. doi: 10.1038/ajg.2014.396

The Wexner Score, also known as the Cleveland Clinic Fecal Incontinence Score (CCFIS), 
is the most widely used and validated scoring system for assessing fecal incontinence 
severity. It evaluates five key aspects of incontinence using a standardized 5-point 
frequency scale, with scores ranging from 0 (perfect continence) to 20 (complete 
incontinence). A score ≥10 indicates clinically significant incontinence requiring 
active management.
"""

from pydantic import BaseModel, Field
from typing import Literal


class WexnerScoreOdsRequest(BaseModel):
    """
    Request model for Wexner Score for Obstructed Defecation Syndrome (ODS)
    
    The Wexner Score evaluates fecal incontinence severity using five standardized 
    parameters, each scored on a 5-point frequency scale:
    
    Frequency Scale (for all parameters):
    - 0: Never
    - 1: Less than once a month
    - 2: Less than once a week but at least once a month
    - 3: Less than once a day but at least once a week
    - 4: At least once a day
    
    Parameters:
    1. Incontinence to solid stool: Frequency of involuntary solid stool loss
    2. Incontinence to liquid stool: Frequency of involuntary liquid stool loss
    3. Incontinence to gas: Frequency of involuntary gas (flatus) loss
    4. Wears protective pads: Frequency of using protective padding
    5. Lifestyle alteration: Extent to which incontinence affects daily activities
    
    Score Interpretation:
    - 0 points: Perfect continence (no symptoms)
    - 1-9 points: Mild incontinence (conservative management)
    - 10-20 points: Clinical incontinence (requires active management)
    
    References (Vancouver style):
    1. Jorge JM, Wexner SD. Etiology and management of fecal incontinence. 
       Dis Colon Rectum. 1993;36(1):77-97. doi: 10.1007/BF02050307
    2. Rockwood TH, Church JM, Fleshman JW, et al. Fecal Incontinence Quality of Life Scale: 
       quality of life instrument for patients with fecal incontinence. Dis Colon Rectum. 
       2000;43(1):9-16. doi: 10.1007/BF02237236
    3. Bharucha AE, Dunivan G, Goode PS, et al. Epidemiology, pathophysiology, and 
       classification of fecal incontinence: state of the science summary for the National 
       Institute of Diabetes and Digestive and Kidney Diseases (NIDDK) workshop. Am J 
       Gastroenterol. 2015;110(1):127-136. doi: 10.1038/ajg.2014.396
    """
    
    incontinence_solid_stool: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Frequency of incontinence to solid stool. 0=Never, 1=Less than once a month, 2=Less than once a week but at least once a month, 3=Less than once a day but at least once a week, 4=At least once a day",
        example=1
    )
    
    incontinence_liquid_stool: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Frequency of incontinence to liquid stool. 0=Never, 1=Less than once a month, 2=Less than once a week but at least once a month, 3=Less than once a day but at least once a week, 4=At least once a day",
        example=2
    )
    
    incontinence_gas: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Frequency of incontinence to gas (flatus). 0=Never, 1=Less than once a month, 2=Less than once a week but at least once a month, 3=Less than once a day but at least once a week, 4=At least once a day",
        example=3
    )
    
    wears_pad: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Frequency of wearing protective pads due to incontinence. 0=Never, 1=Less than once a month, 2=Less than once a week but at least once a month, 3=Less than once a day but at least once a week, 4=At least once a day",
        example=2
    )
    
    lifestyle_alteration: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Extent to which incontinence alters the patient's lifestyle and daily activities. 0=Never affects lifestyle, 1=Less than once a month affects lifestyle, 2=Less than once a week but at least once a month affects lifestyle, 3=Less than once a day but at least once a week affects lifestyle, 4=At least once a day affects lifestyle",
        example=2
    )
    
    class Config:
        schema_extra = {
            "example": {
                "incontinence_solid_stool": 1,
                "incontinence_liquid_stool": 2,
                "incontinence_gas": 3,
                "wears_pad": 2,
                "lifestyle_alteration": 2
            }
        }


class WexnerScoreOdsResponse(BaseModel):
    """
    Response model for Wexner Score for Obstructed Defecation Syndrome (ODS)
    
    The Wexner Score ranges from 0-20 points and classifies fecal incontinence severity:
    
    Score Categories:
    - 0 points: Perfect Continence (no symptoms)
    - 1-9 points: Mild Incontinence (conservative management)
    - 10-20 points: Clinical Incontinence (requires active management)
    
    Clinical Significance:
    - Scores ≥10 indicate clinically significant incontinence requiring specialist evaluation
    - The score correlates well with patient-reported symptom severity and quality of life impact
    - Useful for monitoring treatment response and disease progression
    - Each component helps identify specific areas for targeted intervention
    
    Reference: Jorge JM, Wexner SD. Dis Colon Rectum. 1993;36(1):77-97.
    """
    
    result: int = Field(
        ...,
        description="Wexner Score calculated from clinical parameters (range: 0-20 points)",
        example=10
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on the score",
        example="Wexner score of 10 indicates clinically significant fecal incontinence requiring active management. Consider comprehensive evaluation including anorectal physiology testing, imaging studies, and specialist referral."
    )
    
    stage: str = Field(
        ...,
        description="Incontinence severity category (Perfect Continence, Mild Incontinence, Clinical Incontinence)",
        example="Clinical Incontinence"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the incontinence severity category",
        example="Clinically significant fecal incontinence"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 10,
                "unit": "points",
                "interpretation": "Wexner score of 10 indicates clinically significant fecal incontinence requiring active management. Consider comprehensive evaluation including anorectal physiology testing, imaging studies, and specialist referral. Treatment options may include advanced conservative therapies, biofeedback, sacral nerve stimulation, or surgical interventions depending on underlying etiology.",
                "stage": "Clinical Incontinence",
                "stage_description": "Clinically significant fecal incontinence"
            }
        }