"""
Modified Fisher Grading Scale for Subarachnoid Hemorrhage (SAH) Models

Request and response models for Modified Fisher Grading Scale assessment of aneurysmal SAH.

References (Vancouver style):
1. Frontera JA, Claassen J, Schmidt JM, Wartenberg KE, Temes R, Connolly ES Jr, 
   MacDonald RL, Mayer SA. Prediction of symptomatic vasospasm after subarachnoid 
   hemorrhage: the modified fisher scale. Neurosurgery. 2006 Jul;59(1):21-7; 
   discussion 21-7. doi: 10.1227/01.NEU.0000218821.34014.1B.
2. Claassen J, Bernardini GL, Kreiter K, Bates J, Du YE, Copeland D, Connolly ES, 
   Mayer SA. Effect of cisternal and ventricular blood on risk of delayed cerebral 
   ischemia after subarachnoid hemorrhage: the Fisher scale revisited. Stroke. 
   2001 Sep;32(9):2012-20. doi: 10.1161/hs0901.095677.
3. Fisher CM, Kistler JP, Davis JM. Relation of cerebral vasospasm to subarachnoid 
   hemorrhage visualized by computerized tomographic scanning. Neurosurgery. 
   1980 Jan;6(1):1-9. doi: 10.1227/00006123-198001000-00001.

The Modified Fisher Grading Scale improves upon the original Fisher scale by 
providing better prediction of symptomatic vasospasm after aneurysmal subarachnoid 
hemorrhage. It considers both the thickness of subarachnoid blood and the presence 
of intraventricular hemorrhage to stratify vasospasm risk from 0% to 40%.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ModifiedFisherGradingScaleRequest(BaseModel):
    """
    Request model for Modified Fisher Grading Scale for Subarachnoid Hemorrhage (SAH)
    
    The Modified Fisher Grading Scale assesses aneurysmal SAH severity based on CT findings:
    
    **SAH Thickness Assessment:**
    - None: No subarachnoid hemorrhage visible on CT
    - Thin: SAH thickness <1mm on CT scan
    - Thick: SAH thickness ≥1mm on CT scan
    
    **Intraventricular Hemorrhage (IVH):**
    - Presence or absence of blood in the ventricular system
    
    **Grading System:**
    - Grade 0: No SAH present (0% vasospasm risk)
    - Grade 1: Focal/diffuse thin SAH, no IVH (6-24% vasospasm risk)
    - Grade 2: Focal/diffuse thin SAH with IVH (15-33% vasospasm risk)
    - Grade 3: Focal/diffuse thick SAH, no IVH (33-35% vasospasm risk)
    - Grade 4: Focal/diffuse thick SAH with IVH (34-40% vasospasm risk)
    
    **Clinical Application:**
    - Only applies to aneurysmal subarachnoid hemorrhage
    - Does not apply to traumatic SAH, AVM, or other non-aneurysmal causes
    - Should be assessed on initial non-contrast head CT
    - Used to predict risk of delayed cerebral ischemia and guide monitoring
    
    **Advantages over Original Fisher Scale:**
    - Progressive increase in vasospasm risk with each grade
    - Accounts for combined thick SAH and IVH (Grade 4)
    - Better prediction of symptomatic vasospasm
    
    References (Vancouver style):
    1. Frontera JA, Claassen J, Schmidt JM, Wartenberg KE, Temes R, Connolly ES Jr, 
       MacDonald RL, Mayer SA. Prediction of symptomatic vasospasm after subarachnoid 
       hemorrhage: the modified fisher scale. Neurosurgery. 2006 Jul;59(1):21-7.
    2. Claassen J, Bernardini GL, Kreiter K, Bates J, Du YE, Copeland D, Connolly ES, 
       Mayer SA. Effect of cisternal and ventricular blood on risk of delayed cerebral 
       ischemia after subarachnoid hemorrhage: the Fisher scale revisited. Stroke. 
       2001 Sep;32(9):2012-20.
    """
    
    sah_thickness: Literal["none", "thin", "thick"] = Field(
        ...,
        description="Subarachnoid hemorrhage thickness on CT scan. None (no SAH), thin (<1mm thickness), thick (≥1mm thickness)",
        example="thick"
    )
    
    ivh_present: Literal["no", "yes"] = Field(
        ...,
        description="Presence of intraventricular hemorrhage (blood in ventricular system). No (absent), yes (present)",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "sah_thickness": "thick",
                "ivh_present": "no"
            }
        }


class ModifiedFisherGradingScaleResponse(BaseModel):
    """
    Response model for Modified Fisher Grading Scale for Subarachnoid Hemorrhage (SAH)
    
    The Modified Fisher Grade stratifies vasospasm risk after aneurysmal SAH:
    
    **Grade Interpretations:**
    - Grade 0: No SAH present (0% vasospasm risk)
      * No specific SAH monitoring required
      * Continue evaluation for other causes of symptoms
    
    - Grade 1: Focal/thin SAH, no IVH (6-24% vasospasm risk)
      * Low risk for delayed cerebral ischemia
      * Standard monitoring protocols recommended
    
    - Grade 2: Focal/thin SAH with IVH (15-33% vasospasm risk)
      * Moderate risk for delayed cerebral ischemia
      * Consider enhanced monitoring and nimodipine prophylaxis
    
    - Grade 3: Focal/thick SAH, no IVH (33-35% vasospasm risk)
      * High risk for delayed cerebral ischemia
      * Intensive monitoring, nimodipine prophylaxis recommended
      * Consider angiographic surveillance
    
    - Grade 4: Focal/thick SAH with IVH (34-40% vasospasm risk)
      * Highest risk for delayed cerebral ischemia
      * Intensive monitoring, nimodipine prophylaxis essential
      * Frequent neurological assessments and angiographic surveillance
    
    **Clinical Management Based on Grade:**
    - Higher grades warrant closer monitoring for delayed cerebral ischemia
    - Nimodipine prophylaxis typically indicated for Grades 2-4
    - Serial neurological assessments and transcranial Doppler monitoring
    - Consider angiography for high-grade SAH with clinical deterioration
    
    Reference: Frontera JA, et al. Neurosurgery. 2006;59(1):21-7.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=4,
        description="Modified Fisher grade indicating vasospasm risk after aneurysmal SAH (0-4)",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the grade",
        example="grade"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with vasospasm risk assessment and management recommendations based on Modified Fisher grade",
        example="Modified Fisher Grade 3: Focal or diffuse thick subarachnoid hemorrhage (≥1mm thickness) without intraventricular hemorrhage. Vasospasm risk: 33-35%. High risk for delayed cerebral ischemia. Intensive monitoring, nimodipine prophylaxis, and consideration of angiographic surveillance recommended."
    )
    
    stage: str = Field(
        ...,
        description="Modified Fisher grade classification (Grade 0-4)",
        example="Grade 3"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the SAH pattern and IVH status",
        example="Focal/thick SAH, no IVH"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "grade",
                "interpretation": "Modified Fisher Grade 3: Focal or diffuse thick subarachnoid hemorrhage (≥1mm thickness) without intraventricular hemorrhage. Vasospasm risk: 33-35%. High risk for delayed cerebral ischemia. Intensive monitoring, nimodipine prophylaxis, and consideration of angiographic surveillance recommended.",
                "stage": "Grade 3",
                "stage_description": "Focal/thick SAH, no IVH"
            }
        }