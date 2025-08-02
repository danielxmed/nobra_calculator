"""
Sudbury Vertigo Risk Score Models

Request and response models for Sudbury Vertigo Risk Score calculation.

References (Vancouver style):
1. Lelli D, Dinh J, Ahuja N, Morissette MP, Hamel M, Khorasani S, et al. Development of a 
   Clinical Risk Score to Risk Stratify for a Serious Cause of Vertigo in Patients Presenting 
   to the Emergency Department. Ann Emerg Med. 2024 Nov;84(5):500-511. 
   doi: 10.1016/j.annemergmed.2024.06.003.
2. de Guise C, Chagnon M, Boudier-Revéret M, Chang MC, Fliss K, Vézina F. Validation of the 
   Sudbury Vertigo Risk Score to risk stratify for a serious cause of vertigo. Acad Emerg Med. 
   2024 Dec;31(12):1218-1227. doi: 10.1111/acem.14950.
3. Newman-Toker DE, Edlow JA. TiTrATE: A Novel, Evidence-Based Approach to Diagnosing Acute 
   Dizziness and Vertigo. Neurol Clin. 2015 Aug;33(3):577-99. doi: 10.1016/j.ncl.2015.04.011.

The Sudbury Vertigo Risk Score is a clinical risk stratification tool designed to identify 
patients at risk for serious causes of vertigo (stroke, TIA, vertebral artery dissection, 
or brain tumor) in the emergency department. It uses 7 clinical variables to stratify patients 
into risk categories, with a score <5 having 100% sensitivity for ruling out serious causes.
"""

from pydantic import BaseModel, Field
from typing import Literal


class SudburyVertigoRiskScoreRequest(BaseModel):
    """
    Request model for Sudbury Vertigo Risk Score
    
    The Sudbury Vertigo Risk Score uses 7 clinical variables to assess risk:
    
    Risk Factors (positive points):
    - Male sex: Male patients have higher risk
    - Age >65 years: Advanced age increases risk
    - Hypertension: History of high blood pressure
    - Diabetes: History of diabetes mellitus
    - Motor/sensory deficits: Any motor weakness or sensory loss on exam
    - Cerebellar signs: Including diplopia, dysarthria, dysphagia, dysmetria, ataxia
    
    Protective Factor (negative points):
    - BPPV diagnosis: Clinical diagnosis of benign paroxysmal positional vertigo
    
    Total score ranges from -4 to 17 points
    
    References (Vancouver style):
    1. Lelli D, Dinh J, Ahuja N, Morissette MP, Hamel M, Khorasani S, et al. Development of a 
       Clinical Risk Score to Risk Stratify for a Serious Cause of Vertigo in Patients Presenting 
       to the Emergency Department. Ann Emerg Med. 2024 Nov;84(5):500-511. 
       doi: 10.1016/j.annemergmed.2024.06.003.
    2. de Guise C, Chagnon M, Boudier-Revéret M, Chang MC, Fliss K, Vézina F. Validation of the 
       Sudbury Vertigo Risk Score to risk stratify for a serious cause of vertigo. Acad Emerg Med. 
       2024 Dec;31(12):1218-1227. doi: 10.1111/acem.14950.
    """
    
    male_sex: Literal["yes", "no"] = Field(
        ...,
        description="Patient is male. Male sex is associated with higher risk of serious causes of vertigo",
        example="no"
    )
    
    age_over_65: Literal["yes", "no"] = Field(
        ...,
        description="Patient age is over 65 years. Advanced age is a risk factor for central causes of vertigo",
        example="yes"
    )
    
    hypertension: Literal["yes", "no"] = Field(
        ...,
        description="History of hypertension (high blood pressure). Vascular risk factor for stroke",
        example="yes"
    )
    
    diabetes: Literal["yes", "no"] = Field(
        ...,
        description="History of diabetes mellitus (type 1 or 2). Vascular risk factor for stroke",
        example="no"
    )
    
    motor_sensory_deficits: Literal["yes", "no"] = Field(
        ...,
        description="Motor or sensory deficits on neurological examination. Suggests central nervous system involvement",
        example="no"
    )
    
    cerebellar_signs: Literal["yes", "no"] = Field(
        ...,
        description="Cerebellar signs/symptoms including: diplopia (double vision), dysarthria (speech difficulty), dysphagia (swallowing difficulty), dysmetria (impaired distance estimation), or ataxia (impaired coordination)",
        example="no"
    )
    
    bppv_diagnosis: Literal["yes", "no"] = Field(
        ...,
        description="Clinical diagnosis of benign paroxysmal positional vertigo (BPPV). Protective factor - reduces risk of serious cause. Typically presents with brief episodes of vertigo triggered by head position changes",
        example="no"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "male_sex": "no",
                "age_over_65": "yes",
                "hypertension": "yes",
                "diabetes": "no",
                "motor_sensory_deficits": "no",
                "cerebellar_signs": "no",
                "bppv_diagnosis": "no"
            }
        }
    }


class SudburyVertigoRiskScoreResponse(BaseModel):
    """
    Response model for Sudbury Vertigo Risk Score
    
    The score ranges from -4 to 17 points and stratifies risk:
    - Score <5: 0% risk of serious diagnosis (100% sensitivity)
    - Score 5-8: 2.1% risk of serious diagnosis
    - Score >8: 41% risk of serious diagnosis
    
    Serious diagnoses include: stroke, TIA, vertebral artery dissection, brain tumor
    
    Reference: Lelli D, et al. Ann Emerg Med. 2024;84(5):500-511.
    """
    
    result: int = Field(
        ...,
        ge=-4,
        le=17,
        description="Total Sudbury Vertigo Risk Score (range: -4 to 17 points)",
        example=6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended actions based on the score",
        example="Low but non-zero risk of serious cause. Consider further clinical assessment, observation, or targeted imaging based on clinical judgment and specific symptoms."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Moderate Risk, High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Risk percentage for serious diagnosis",
        example="2.1% risk of serious diagnosis"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": "Low but non-zero risk of serious cause. Consider further clinical assessment, observation, or targeted imaging based on clinical judgment and specific symptoms.",
                "stage": "Moderate Risk",
                "stage_description": "2.1% risk of serious diagnosis"
            }
        }
    }