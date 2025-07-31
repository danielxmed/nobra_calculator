"""
New York Heart Association (NYHA) Functional Classification for Heart Failure Models

Request and response models for NYHA Functional Classification calculation.

References (Vancouver style):
1. Dolgin M, Association NYH, Fox AC, Gorlin R, Levin RI, New York Heart Association. 
   Criteria Committee. Nomenclature and criteria for diagnosis of diseases of the heart 
   and great vessels. 9th ed. Boston, MA: Lippincott Williams and Wilkins; March 1, 1994.
2. Goldman L, Hashimoto B, Cook EF, Loscalzo A. Comparative reproducibility and validity 
   of systems for assessing cardiovascular functional class: advantages of a new specific 
   activity scale. Circulation. 1981 Dec;64(6):1227-34. doi: 10.1161/01.cir.64.6.1227.
3. Raphael C, Briscoe C, Davies J, Ian Whinnett Z, Manisty C, Sutton R, et al. 
   Limitations of the New York Heart Association functional classification system and 
   self-reported walking distances in chronic heart failure. Heart. 2007 Apr;93(4):476-82. 
   doi: 10.1136/hrt.2006.089656.

The NYHA Functional Classification provides a simple way of classifying the extent of 
heart failure. It places patients in one of four categories based on how much they are 
limited during physical activity; the limitations/symptoms are in regard to normal 
breathing and varying degrees in shortness of breath and/or angina.
"""

from pydantic import BaseModel, Field
from typing import Literal


class NyhaFunctionalClassificationRequest(BaseModel):
    """
    Request model for New York Heart Association (NYHA) Functional Classification
    
    The NYHA classification has been a cornerstone of heart failure assessment since 1928,
    providing a common language for physicians to communicate about functional capacity.
    Despite its subjective nature and limited reproducibility, it remains arguably the 
    most important prognostic marker in routine clinical use for heart failure today.
    
    Classes:
    - Class I: No limitation of physical activity (≥7 METs capacity)
    - Class II: Slight limitation of physical activity (≥5 to <7 METs capacity)  
    - Class III: Marked limitation of physical activity (≥2 to <5 METs capacity)
    - Class IV: Unable to carry on any physical activity without discomfort (<2 METs capacity)
    
    MET = Metabolic Equivalent of Task (1 MET = 3.5 mL O2/kg/min)
    
    References (Vancouver style):
    1. Dolgin M, Association NYH, Fox AC, Gorlin R, Levin RI, New York Heart Association. 
    Criteria Committee. Nomenclature and criteria for diagnosis of diseases of the heart 
    and great vessels. 9th ed. Boston, MA: Lippincott Williams and Wilkins; March 1, 1994.
    2. Goldman L, Hashimoto B, Cook EF, Loscalzo A. Comparative reproducibility and validity 
    of systems for assessing cardiovascular functional class: advantages of a new specific 
    activity scale. Circulation. 1981 Dec;64(6):1227-34. doi: 10.1161/01.cir.64.6.1227.
    """
    
    physical_ability: Literal[
        "Class I - No limitation of physical activity",
        "Class II - Slight limitation of physical activity", 
        "Class III - Marked limitation of physical activity",
        "Class IV - Unable to carry on any physical activity without discomfort"
    ] = Field(
        ...,
        description="""Patient's physical ability and symptom level. Select the class that best describes the patient:
        
        • Class I: No limitation of physical activity. Ordinary physical activity does not cause undue fatigue, palpitation, or dyspnea.
        
        • Class II: Slight limitation of physical activity. Comfortable at rest. Ordinary physical activity results in fatigue, palpitation, or dyspnea.
        
        • Class III: Marked limitation of physical activity. Comfortable at rest. Less than ordinary activity causes fatigue, palpitation, or dyspnea.
        
        • Class IV: Unable to carry on any physical activity without discomfort. Symptoms of heart failure at rest. If any physical activity is undertaken, discomfort increases.""",
        example="Class II - Slight limitation of physical activity"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "physical_ability": "Class II - Slight limitation of physical activity"
            }
        }


class NyhaFunctionalClassificationResponse(BaseModel):
    """
    Response model for New York Heart Association (NYHA) Functional Classification
    
    Returns the NYHA functional class with interpretation and MET capacity.
    The classification helps guide treatment decisions and provides prognostic information,
    though it should be used in conjunction with objective measures of cardiac function.
    
    Reference: Dolgin M, et al. Nomenclature and criteria for diagnosis of diseases 
    of the heart and great vessels. 9th ed. Lippincott Williams and Wilkins; 1994.
    """
    
    result: str = Field(
        ...,
        description="NYHA functional classification (Class I, II, III, or IV)",
        example="Class II"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for classification)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the NYHA class with functional capacity details",
        example="Comfortable at rest. Ordinary physical activity results in fatigue, palpitation, or dyspnea. Patients can perform activities requiring ≥5 METs but <7 METs."
    )
    
    stage: str = Field(
        ...,
        description="NYHA classification stage",
        example="Class II"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the functional limitation",
        example="Slight limitation of physical activity"
    )
    
    met_capacity: str = Field(
        ...,
        description="Metabolic equivalent capacity range for this NYHA class",
        example="≥5 to <7 METs"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Class II",
                "unit": "",
                "interpretation": "Comfortable at rest. Ordinary physical activity results in fatigue, palpitation, or dyspnea. Patients can perform activities requiring ≥5 METs but <7 METs.",
                "stage": "Class II",
                "stage_description": "Slight limitation of physical activity",
                "met_capacity": "≥5 to <7 METs"
            }
        }