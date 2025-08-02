"""
mMRC (Modified Medical Research Council) Dyspnea Scale Models

Request and response models for mMRC Dyspnea Scale assessment.

References (Vancouver style):
1. Mahler DA, Wells CK. Evaluation of clinical methods for rating dyspnea. 
   Chest. 1988 Mar;93(3):580-6. doi: 10.1378/chest.93.3.580.
2. Bestall JC, Paul EA, Garrod R, Garnham R, Jones PW, Wedzicha JA. Usefulness 
   of the Medical Research Council (MRC) dyspnoea scale as a measure of disability 
   in patients with chronic obstructive pulmonary disease. Thorax. 1999 Jul;
   54(7):581-6. doi: 10.1136/thx.54.7.581.
3. Kocks JW, Tuinenga MG, Uil SM, van den Berg JW, Ståhl E, van der Molen T. 
   Health status measurement in COPD: the minimal clinically important difference 
   of the clinical COPD questionnaire. Respir Res. 2006 Apr 7;7:62. 
   doi: 10.1186/1465-9921-7-62.
4. Global Initiative for Chronic Obstructive Lung Disease. Global Strategy for 
   the Diagnosis, Management, and Prevention of Chronic Obstructive Pulmonary 
   Disease (2023 Report). Available from: https://goldcopd.org

The mMRC (Modified Medical Research Council) Dyspnea Scale is a validated tool 
for assessing the degree of baseline functional disability due to dyspnea in 
patients with respiratory diseases, particularly COPD. The scale ranges from 
Grade 0 (dyspnea only with strenuous exercise) to Grade 4 (too dyspneic to 
leave house or breathless when dressing). It has high inter-rater reliability 
(98%) and correlates with health-related quality of life measures.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MmrcDyspneaScaleRequest(BaseModel):
    """
    Request model for mMRC (Modified Medical Research Council) Dyspnea Scale
    
    The mMRC Dyspnea Scale assesses functional disability due to dyspnea by 
    categorizing patients based on activities that trigger breathlessness:
    
    Grade 0 (No Dyspnea):
    - grade_0: "Dyspnea only with strenuous exercise"
    - Normal exercise tolerance with minimal functional impairment
    - Patient can perform most activities without significant breathlessness
    
    Grade 1 (Mild Dyspnea):
    - grade_1: "Dyspnea when hurrying or walking up a slight hill"
    - Slight limitation in activities involving exertion or walking uphill
    - Generally good functional capacity for daily activities
    
    Grade 2 (Moderate Dyspnea):
    - grade_2: "Walks slower than people of the same age because of dyspnea, 
               or has to stop for breath when walking at own pace"
    - Moderate limitation affecting walking speed and endurance on level ground
    
    Grade 3 (Severe Dyspnea):
    - grade_3: "Stops for breath after walking 100 yards (91 m) or after 
               a few minutes"
    - Significant limitation in walking distance on level ground
    - Severely impaired exercise tolerance
    
    Grade 4 (Very Severe Dyspnea):
    - grade_4: "Too dyspneic to leave house or breathless when dressing"
    - Severe disability with breathlessness at rest or with minimal activity
    - Housebound due to dyspnea

    References (Vancouver style):
    1. Mahler DA, Wells CK. Evaluation of clinical methods for rating dyspnea. 
       Chest. 1988 Mar;93(3):580-6. doi: 10.1378/chest.93.3.580.
    2. Bestall JC, Paul EA, Garrod R, Garnham R, Jones PW, Wedzicha JA. Usefulness 
       of the Medical Research Council (MRC) dyspnoea scale as a measure of disability 
       in patients with chronic obstructive pulmonary disease. Thorax. 1999 Jul;
       54(7):581-6. doi: 10.1136/thx.54.7.581.
    3. Kocks JW, Tuinenga MG, Uil SM, van den Berg JW, Ståhl E, van der Molen T. 
       Health status measurement in COPD: the minimal clinically important difference 
       of the clinical COPD questionnaire. Respir Res. 2006 Apr 7;7:62. 
       doi: 10.1186/1465-9921-7-62.
    4. Global Initiative for Chronic Obstructive Lung Disease. Global Strategy for 
       the Diagnosis, Management, and Prevention of Chronic Obstructive Pulmonary 
       Disease (2023 Report). Available from: https://goldcopd.org
    """
    
    dyspnea_grade: Literal["grade_0", "grade_1", "grade_2", "grade_3", "grade_4"] = Field(
        ...,
        description="Patient's functional limitation due to dyspnea. Select based on the activity level that triggers breathlessness: Grade 0 (strenuous exercise), Grade 1 (hurrying/uphill), Grade 2 (walking slower/stopping), Grade 3 (after 100 yards), Grade 4 (dressing/housebound)",
        example="grade_2"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "dyspnea_grade": "grade_2"
            }
        }


class MmrcDyspneaScaleResponse(BaseModel):
    """
    Response model for mMRC (Modified Medical Research Council) Dyspnea Scale
    
    The mMRC scale provides a standardized assessment of functional disability 
    due to dyspnea with grades 0-4:
    
    Grade 0 (No Dyspnea):
    - Minimal functional limitation
    - Dyspnea only with strenuous exercise
    - Normal exercise tolerance for daily activities
    
    Grade 1 (Mild Dyspnea):
    - Mild functional limitation
    - Dyspnea when hurrying or walking uphill
    - Good functional capacity for most activities
    
    Grade 2 (Moderate Dyspnea):
    - Moderate functional limitation
    - Walks slower than peers or stops for breath
    - Moderate limitation affecting walking endurance
    
    Grade 3 (Severe Dyspnea):
    - Severe functional limitation
    - Stops after 100 yards or few minutes walking
    - Significantly impaired exercise tolerance
    
    Grade 4 (Very Severe Dyspnea):
    - Very severe functional limitation
    - Too dyspneic to leave house or breathless dressing
    - Housebound with breathlessness at rest
    
    Clinical Applications:
    - Part of GOLD guidelines for COPD assessment
    - Component of BODE Index for COPD prognosis
    - Correlates with health-related quality of life
    - High inter-rater reliability (98%)
    
    Reference: Mahler DA, Wells CK. Chest. 1988;93(3):580-6.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=4,
        description="mMRC dyspnea grade indicating severity of functional limitation (0-4)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the grade",
        example="grade"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of functional limitation and breathlessness severity",
        example="Walks slower than people of the same age because of dyspnea, or has to stop for breath when walking at own pace on level ground. Moderate limitation affecting walking speed and endurance."
    )
    
    stage: str = Field(
        ...,
        description="Dyspnea severity category (No Dyspnea, Mild Dyspnea, Moderate Dyspnea, Severe Dyspnea, Very Severe Dyspnea)",
        example="Moderate Dyspnea"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of functional limitation level",
        example="Moderate functional limitation"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "grade",
                "interpretation": "Walks slower than people of the same age because of dyspnea, or has to stop for breath when walking at own pace on level ground. Moderate limitation affecting walking speed and endurance.",
                "stage": "Moderate Dyspnea",
                "stage_description": "Moderate functional limitation"
            }
        }