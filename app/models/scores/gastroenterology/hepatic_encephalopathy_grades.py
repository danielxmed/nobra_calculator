"""
Hepatic Encephalopathy Grades/Stages (West Haven Criteria) Models

Request and response models for Hepatic Encephalopathy grading.

References (Vancouver style):
1. Vilstrup H, Amodio P, Bajaj J, Cordoba J, Ferenci P, Mullen KD, et al.; American 
   Association for the Study of Liver Diseases; European Association for the Study 
   of the Liver. Hepatic encephalopathy in chronic liver disease: 2014 practice 
   guideline by the American Association for the Study of Liver Diseases and the 
   European Association for the Study of the Liver. J Hepatol. 2014 Sep;61(3):642-59. 
   doi: 10.1016/j.jhep.2014.05.042.
2. European Association for the Study of the Liver. EASL Clinical Practice Guidelines 
   on the management of hepatic encephalopathy. J Hepatol. 2022 Oct;77(3):807-824. 
   doi: 10.1016/j.jhep.2022.06.001.
3. Ferenci P, Lockwood A, Mullen K, Tarter R, Weissenborn K, Blei AT. Hepatic 
   encephalopathy--definition, nomenclature, diagnosis, and quantification: final 
   report of the working party at the 11th World Congresses of Gastroenterology, 
   Vienna, 1998. Hepatology. 2002 Mar;35(3):716-21. doi: 10.1053/jhep.2002.31250.

The West Haven Criteria is the most widely used classification system for hepatic 
encephalopathy, providing a semi-quantitative grading of mental state based on 
changes in consciousness, intellectual function, behavior, and neuromuscular function.
"""

from pydantic import BaseModel, Field
from typing import Literal


class HepaticEncephalopathyGradesRequest(BaseModel):
    """
    Request model for Hepatic Encephalopathy Grades/Stages (West Haven Criteria)
    
    The West Haven Criteria classifies hepatic encephalopathy into 5 grades (0-4):
    
    Covert HE (Grades 0-1):
    - Grade 0 (Minimal HE): No clinical symptoms, only detectable by psychometric tests
    - Grade 1: Minimal changes in behavior and consciousness
    
    Overt HE (Grades 2-4):
    - Grade 2: Gross disorientation, drowsiness, asterixis
    - Grade 3: Marked confusion, somnolence but arousable
    - Grade 4: Coma, unresponsive to stimuli
    
    This grading system helps guide clinical management and assess prognosis in patients
    with liver disease. Higher grades are associated with increased risk of cerebral edema
    in acute liver failure.
    
    References (Vancouver style):
    1. Vilstrup H, Amodio P, Bajaj J, Cordoba J, Ferenci P, Mullen KD, et al. Hepatic 
       encephalopathy in chronic liver disease: 2014 practice guideline by the American 
       Association for the Study of Liver Diseases and the European Association for the 
       Study of the Liver. J Hepatol. 2014 Sep;61(3):642-59.
    2. European Association for the Study of the Liver. EASL Clinical Practice Guidelines 
       on the management of hepatic encephalopathy. J Hepatol. 2022 Oct;77(3):807-824.
    """
    
    clinical_features: Literal["grade_0", "grade_1", "grade_2", "grade_3", "grade_4"] = Field(
        ...,
        description="Clinical presentation of the patient based on West Haven Criteria. "
                    "grade_0: Minimal HE - no clinical symptoms, abnormal psychometric tests only. "
                    "grade_1: Trivial lack of awareness, shortened attention span, altered sleep. "
                    "grade_2: Lethargy, disorientation for time, obvious asterixis, inappropriate behavior. "
                    "grade_3: Somnolence to semi-stupor, confusion, gross disorientation, bizarre behavior. "
                    "grade_4: Coma, unresponsive to verbal or noxious stimuli.",
        example="grade_2"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "clinical_features": "grade_2"
            }
        }


class HepaticEncephalopathyGradesResponse(BaseModel):
    """
    Response model for Hepatic Encephalopathy Grades/Stages (West Haven Criteria)
    
    Returns the West Haven grade with detailed clinical interpretation. The grading 
    system differentiates between:
    - Covert HE (Grades 0-1): Subtle changes often only detected by testing or family
    - Overt HE (Grades 2-4): Clinically apparent changes requiring medical intervention
    
    This standardized grading helps in:
    - Assessing disease severity and progression
    - Guiding treatment decisions
    - Determining prognosis
    - Research standardization
    
    Reference: Vilstrup H, et al. J Hepatol. 2014;61(3):642-59.
    """
    
    result: str = Field(
        ...,
        description="West Haven Grade of hepatic encephalopathy (Grade 0 through Grade 4)",
        example="Grade 2"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="grade"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation of the grade including symptoms, signs, and clinical significance",
        example="Lethargy or apathy, minimal disorientation for time or place, subtle personality change, inappropriate behavior, impaired performance of subtraction. Obvious asterixis. Patient is drowsy but arousable. This is the first stage clearly identifiable on clinical examination."
    )
    
    stage: str = Field(
        ...,
        description="Stage classification including grade number and HE type (Minimal/Covert/Overt)",
        example="Grade 2 (Overt HE)"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief clinical description of the grade",
        example="Gross disorientation, drowsiness, possibly asterixis, inappropriate behavior"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Grade 2",
                "unit": "grade",
                "interpretation": "Lethargy or apathy, minimal disorientation for time or place, subtle personality change, inappropriate behavior, impaired performance of subtraction. Obvious asterixis. Patient is drowsy but arousable. This is the first stage clearly identifiable on clinical examination.",
                "stage": "Grade 2 (Overt HE)",
                "stage_description": "Gross disorientation, drowsiness, possibly asterixis, inappropriate behavior"
            }
        }