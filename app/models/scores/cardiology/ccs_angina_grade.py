"""
Canadian Cardiovascular Society (CCS) Angina Grade Models

Request and response models for CCS Angina Grade calculation.

References (Vancouver style):
1. Campeau L. Letter: Grading of angina pectoris. Circulation. 1976 Sep;54(3):522-3. 
   PMID: 947585.
2. Campeau L. The Canadian Cardiovascular Society grading of angina pectoris revisited 
   30 years later. Can J Cardiol. 2002 Apr;18(4):371-9. PMID: 11992130.
3. Goldman L, Hashimoto B, Cook EF, Loscalzo A. Comparative reproducibility and 
   validity of systems for assessing cardiovascular functional class: advantages of 
   a new specific activity scale. Circulation. 1981 Dec;64(6):1227-34. 
   doi: 10.1161/01.cir.64.6.1227.

The CCS Angina Grade is a standardized classification system used to grade the severity
of exertional angina based on functional limitations. It helps clinicians communicate
about symptom severity and has been associated with prognosis in coronary artery disease.
"""

from pydantic import BaseModel, Field
from typing import Literal


class CcsAnginaGradeRequest(BaseModel):
    """
    Request model for Canadian Cardiovascular Society (CCS) Angina Grade
    
    The CCS Angina Grade classifies patients into four categories based on the 
    level of physical activity that triggers angina symptoms. This standardized 
    grading system was developed in 1972 and published in 1976 to provide uniform 
    terminology for describing functional limitations in coronary artery disease.
    
    Classification levels:
    - Grade I: Angina only with strenuous, rapid, or prolonged exertion
    - Grade II: Slight limitation of ordinary activity
    - Grade III: Marked limitation of ordinary physical activity
    - Grade IV: Inability to carry out any physical activity without discomfort
    
    Clinical applications:
    - Standardizes communication about angina severity
    - Used in clinical trials and registries
    - Helps guide treatment decisions
    - Used to assess fitness to fly (British Cardiovascular Society)
    - Associated with mortality and morbidity outcomes
    
    Limitations:
    - Does not account for anti-anginal medication use before exertion
    - Personal warm-up effects not considered
    - Not designed as a prognostic tool (though associated with outcomes)
    
    References (Vancouver style):
    1. Campeau L. Letter: Grading of angina pectoris. Circulation. 1976 Sep;54(3):522-3.
    2. Campeau L. The Canadian Cardiovascular Society grading of angina pectoris revisited 
       30 years later. Can J Cardiol. 2002 Apr;18(4):371-9.
    """
    
    angina_symptoms: Literal[
        "strenuous_exertion_only",
        "moderate_exertion_limitation", 
        "marked_limitation",
        "symptoms_at_rest"
    ] = Field(
        ...,
        description="""Select the level of physical activity that triggers angina symptoms:
        
        - strenuous_exertion_only: Ordinary physical activity does not cause angina. 
          Angina only with strenuous, rapid, or prolonged exertion at work or recreation.
          
        - moderate_exertion_limitation: Slight limitation of ordinary activity. Angina with:
          • Walking or climbing stairs rapidly
          • Walking uphill
          • Walking or stair climbing after meals, in cold, wind, or under emotional stress
          • Walking >2 blocks on level ground or climbing >1 flight of stairs at normal pace
          
        - marked_limitation: Marked limitation of ordinary activity. Angina with:
          • Walking 1-2 blocks on level ground
          • Climbing 1 flight of stairs at normal pace in normal conditions
          
        - symptoms_at_rest: Unable to perform any physical activity without discomfort.
          Anginal symptoms may occur at rest.""",
        example="moderate_exertion_limitation"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "angina_symptoms": "moderate_exertion_limitation"
            }
        }


class CcsAnginaGradeResponse(BaseModel):
    """
    Response model for Canadian Cardiovascular Society (CCS) Angina Grade
    
    Returns the CCS grade (I-IV) with detailed interpretation of functional limitations.
    
    Clinical significance:
    - Grade I: No limitation of ordinary physical activity
    - Grade II: Slight limitation of ordinary activity
    - Grade III: Marked limitation of ordinary physical activity
    - Grade IV: Inability to carry out any physical activity without discomfort
    
    Prognostic associations (though not designed as prognostic tool):
    - Higher grades associated with increased mortality
    - 8-year mortality rates: Grade I (20.5%), II (24.1%), III (40.4%), IV (35.3%)
    - Associated with coronary revascularization and myocardial infarction risk
    
    Reference: Campeau L. Circulation. 1976;54(3):522-3.
    """
    
    result: str = Field(
        ...,
        description="CCS Angina Grade (Grade I, Grade II, Grade III, or Grade IV)",
        example="Grade II"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (grade)",
        example="grade"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed interpretation of the CCS grade including specific functional limitations",
        example="Angina occurs on walking or climbing stairs rapidly, walking uphill, walking or stair climbing after meals, in cold, in wind, under emotional stress, or only during the few hours after awakening. Angina on walking more than 2 blocks on the level and climbing more than 1 flight of ordinary stairs at normal pace and in normal conditions."
    )
    
    stage: str = Field(
        ...,
        description="CCS Angina Grade (same as result)",
        example="Grade II"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the functional limitation level",
        example="Slight limitation of ordinary activity"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Grade II",
                "unit": "grade",
                "interpretation": "Angina occurs on walking or climbing stairs rapidly, walking uphill, walking or stair climbing after meals, in cold, in wind, under emotional stress, or only during the few hours after awakening. Angina on walking more than 2 blocks on the level and climbing more than 1 flight of ordinary stairs at normal pace and in normal conditions.",
                "stage": "Grade II",
                "stage_description": "Slight limitation of ordinary activity"
            }
        }