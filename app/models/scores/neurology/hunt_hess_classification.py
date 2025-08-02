"""
Hunt & Hess Classification of Subarachnoid Hemorrhage Models

Request and response models for Hunt-Hess Classification calculation.

References (Vancouver style):
1. Hunt WE, Hess RM. Surgical risk as related to time of intervention in the repair of 
   intracranial aneurysms. J Neurosurg. 1968 Jan;28(1):14-20. doi: 10.3171/jns.1968.28.1.0014.
2. Hunt WE, Kosnik EJ. Timing and perioperative care in intracranial aneurysm surgery. 
   Clin Neurosurg. 1974;21:79-89. PMID: 4370936.
3. Oshiro EM, Walter KA, Piantadosi S, Witham TF, Tamargo RJ. A new subarachnoid hemorrhage 
   grading system based on the Glasgow Coma Scale: a comparison with the Hunt and Hess and 
   World Federation of Neurosurgical Societies Scales in a clinical series. Neurosurgery. 
   1997 Jul;41(1):140-7. doi: 10.1097/00006123-199707000-00027.

The Hunt-Hess Classification system grades aneurysmal subarachnoid hemorrhage severity 
from I to V based on clinical presentation and neurological status. Originally developed 
in 1968 and modified in 1974, it remains widely used for mortality prediction and surgical 
risk assessment. Higher grades correlate with increased mortality rates and surgical risk.
"""

from pydantic import BaseModel, Field
from typing import Literal


class HuntHessClassificationRequest(BaseModel):
    """
    Request model for Hunt & Hess Classification of Subarachnoid Hemorrhage
    
    The Hunt-Hess Classification uses clinical presentation to assign grades I-V:
    
    Grade I: Asymptomatic or minimal headache and slight nuchal rigidity
    - Survival rate: ~70%
    - Surgical risk: Low
    
    Grade II: Moderate to severe headache, nuchal rigidity, no neurologic deficit 
    except cranial nerve palsy
    - Survival rate: ~60%
    - Surgical risk: Low-Moderate
    
    Grade III: Drowsiness, confusion, or mild focal deficit
    - Survival rate: ~50%
    - Surgical risk: Moderate
    
    Grade IV: Stupor, moderate to severe hemiparesis, possibly early decerebrate 
    rigidity and vegetative disturbances
    - Survival rate: ~40%
    - Surgical risk: High
    
    Grade V: Deep coma, decerebrate rigidity, moribund appearance
    - Survival rate: ~10%
    - Surgical risk: Very High
    
    Modification Rule: Add one grade if serious systemic disease is present 
    (hypertension, diabetes, severe arteriosclerosis, chronic pulmonary disease, 
    severe vasospasm on angiography).
    
    References (Vancouver style):
    1. Hunt WE, Hess RM. Surgical risk as related to time of intervention in the repair of 
       intracranial aneurysms. J Neurosurg. 1968 Jan;28(1):14-20. doi: 10.3171/jns.1968.28.1.0014.
    2. Hunt WE, Kosnik EJ. Timing and perioperative care in intracranial aneurysm surgery. 
       Clin Neurosurg. 1974;21:79-89. PMID: 4370936.
    """
    
    clinical_presentation: Literal[
        "asymptomatic_minimal_headache",
        "moderate_severe_headache_nuchal_rigidity",
        "drowsiness_confusion_mild_focal_deficit", 
        "stupor_moderate_severe_hemiparesis",
        "deep_coma_decerebrate_rigidity_moribund"
    ] = Field(
        ...,
        description="Clinical presentation and neurological status on admission. "
                   "asymptomatic_minimal_headache: Grade I - Asymptomatic or minimal headache with slight nuchal rigidity. "
                   "moderate_severe_headache_nuchal_rigidity: Grade II - Moderate to severe headache, nuchal rigidity, no neurologic deficit except cranial nerve palsy. "
                   "drowsiness_confusion_mild_focal_deficit: Grade III - Drowsiness, confusion, or mild focal neurologic deficit. "
                   "stupor_moderate_severe_hemiparesis: Grade IV - Stupor, moderate to severe hemiparesis, possibly early decerebrate rigidity. "
                   "deep_coma_decerebrate_rigidity_moribund: Grade V - Deep coma, decerebrate rigidity, moribund appearance.",
        example="moderate_severe_headache_nuchal_rigidity"
    )
    
    serious_systemic_disease: Literal["yes", "no"] = Field(
        ...,
        description="Presence of serious systemic disease such as hypertension, diabetes mellitus, "
                   "severe arteriosclerosis, chronic pulmonary disease, or severe vasospasm on angiography. "
                   "If present, increases grade by one level (maximum Grade V).",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "clinical_presentation": "moderate_severe_headache_nuchal_rigidity",
                "serious_systemic_disease": "no"
            }
        }


class HuntHessClassificationResponse(BaseModel):
    """
    Response model for Hunt & Hess Classification of Subarachnoid Hemorrhage
    
    The Hunt-Hess Classification provides grades I-V with corresponding prognosis:
    
    - Grade I: 70% survival, excellent prognosis, low surgical risk
    - Grade II: 60% survival, good prognosis, low-moderate surgical risk  
    - Grade III: 50% survival, fair prognosis, moderate surgical risk
    - Grade IV: 40% survival, poor prognosis, high surgical risk
    - Grade V: 10% survival, very poor prognosis, very high surgical risk
    
    The classification helps guide treatment decisions and provides prognostic 
    information for patients and families. Higher grades indicate more severe 
    hemorrhage with increased mortality and surgical complications.
    
    Reference: Hunt WE, Hess RM. J Neurosurg. 1968;28(1):14-20.
    """
    
    result: str = Field(
        ...,
        description="Hunt-Hess grade in Roman numeral format (Grade I, Grade II, Grade III, Grade IV, or Grade V)",
        example="Grade II"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the classification",
        example="grade"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with prognosis, survival rate, and surgical risk assessment based on the Hunt-Hess grade",
        example="Moderate to severe headache, nuchal rigidity, no neurologic deficit other than cranial nerve palsy. Good prognosis with ~60% survival rate. Reasonable surgical candidate."
    )
    
    stage: str = Field(
        ...,
        description="Grade classification (Grade I, Grade II, Grade III, Grade IV, or Grade V)",
        example="Grade II"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the clinical presentation for this grade",
        example="Moderate to severe headache"
    )
    
    numeric_grade: int = Field(
        ...,
        ge=1,
        le=5,
        description="Numeric Hunt-Hess grade (1-5) for computational purposes",
        example=2
    )
    
    survival_rate_percent: int = Field(
        ...,
        ge=0,
        le=100,
        description="Approximate survival rate percentage based on historical data for this grade",
        example=60
    )
    
    mortality_rate_percent: int = Field(
        ...,
        ge=0,
        le=100,
        description="Approximate mortality rate percentage based on historical data for this grade",
        example=40
    )
    
    grade_adjusted_for_systemic_disease: bool = Field(
        ...,
        description="Boolean indicating whether the grade was increased due to presence of serious systemic disease",
        example=False
    )
    
    surgical_risk: str = Field(
        ...,
        description="Surgical risk level (Low, Low-Moderate, Moderate, High, or Very High) based on the Hunt-Hess grade",
        example="Low-Moderate"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Grade II",
                "unit": "grade",
                "interpretation": "Moderate to severe headache, nuchal rigidity, no neurologic deficit other than cranial nerve palsy. Good prognosis with ~60% survival rate. Reasonable surgical candidate.",
                "stage": "Grade II",
                "stage_description": "Moderate to severe headache",
                "numeric_grade": 2,
                "survival_rate_percent": 60,
                "mortality_rate_percent": 40,
                "grade_adjusted_for_systemic_disease": False,
                "surgical_risk": "Low-Moderate"
            }
        }