"""
History and Electrocardiogram-only Manchester Acute Coronary Syndromes (HE-MACS) Models

Request and response models for HE-MACS calculation.

References (Vancouver style):
1. Alghamdi A, Cook E, Carlton E, Siriwardena A, Hann M, Thompson A, et al. 
   Enhanced triage for patients with suspected cardiac chest pain: the History 
   and Electrocardiogram-only Manchester Acute Coronary Syndromes (HE-MACS) 
   decision aid. Eur J Emerg Med. 2019 Oct;26(5):356-361. 
   doi: 10.1097/MEJ.0000000000000575.
2. Body R, Carley S, Wibberley C, McDowell G, Ferguson J, Mackway-Jones K. 
   The value of symptoms and signs in the emergent diagnosis of acute coronary 
   syndromes. Resuscitation. 2010 Mar;81(3):281-6. 
   doi: 10.1016/j.resuscitation.2009.11.014.
3. Body R, Cook G, Burrows G, Carley S, Lewis PS. Can emergency physicians 
   'rule in' and 'rule out' acute myocardial infarction with clinical judgement? 
   Emerg Med J. 2014 Nov;31(11):872-6. doi: 10.1136/emermed-2014-203832.

The HE-MACS decision aid provides rapid risk stratification for acute coronary 
syndrome using only history and ECG findings, without requiring troponin results. 
This allows for immediate triage decisions in the emergency department.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class HeMacsRequest(BaseModel):
    """
    Request model for History and Electrocardiogram-only Manchester Acute Coronary Syndromes (HE-MACS)
    
    HE-MACS uses 8 clinical variables to calculate the probability of ACS or major 
    adverse cardiac events (MACE) within 30 days:
    
    Clinical Variables:
    - Age: Continuous variable (older age increases risk)
    - Sex: Male sex associated with higher risk
    - Sweating: Diaphoresis observed during presentation
    - Acute ECG ischemia: New ST depression or T wave inversion
    - Pain radiating to right arm/shoulder: Specific radiation pattern
    - Vomiting: Associated with pain presentation
    - Hypotension: Systolic BP <100 mmHg
    - Current smoking: Active tobacco use
    
    ECG Criteria for Ischemia:
    - New ST depression ≥0.5mm in ≥2 contiguous leads
    - New T wave inversion ≥1mm in ≥2 contiguous leads
    
    Important Notes:
    - For patients ≥18 years with suspected cardiac chest pain
    - Presentation within 24 hours of symptom onset
    - Not yet prospectively validated - use with clinical judgment
    - Does not require troponin, allowing immediate risk stratification
    
    References (Vancouver style):
    1. Alghamdi A, Cook E, Carlton E, Siriwardena A, Hann M, Thompson A, et al. 
       Enhanced triage for patients with suspected cardiac chest pain: the History 
       and Electrocardiogram-only Manchester Acute Coronary Syndromes (HE-MACS) 
       decision aid. Eur J Emerg Med. 2019 Oct;26(5):356-361.
    2. Body R, Carley S, Wibberley C, McDowell G, Ferguson J, Mackway-Jones K. 
       The value of symptoms and signs in the emergent diagnosis of acute coronary 
       syndromes. Resuscitation. 2010 Mar;81(3):281-6.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in years. Older age is associated with increased risk of ACS. "
                    "Each year adds 0.024 to the risk calculation. Range: 18-120 years.",
        example=65
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient sex. Male sex is associated with higher risk of ACS, adding "
                    "0.462 to the risk calculation.",
        example="male"
    )
    
    sweating: Literal["yes", "no"] = Field(
        ...,
        description="Sweating (diaphoresis) observed during presentation. A classic sign of MI, "
                    "particularly with inferior wall involvement. Adds 1.426 to risk if present.",
        example="yes"
    )
    
    acute_ecg_ischemia: Literal["yes", "no"] = Field(
        ...,
        description="Acute ECG ischemia defined as new ST depression ≥0.5mm or T wave inversion "
                    "≥1mm in ≥2 contiguous leads. Strong predictor of ACS. Adds 1.838 to risk if present.",
        example="no"
    )
    
    pain_radiating_right_arm: Literal["yes", "no"] = Field(
        ...,
        description="Pain radiating to right arm or shoulder. Less common than left-sided radiation "
                    "but still predictive of ACS. Adds 0.734 to risk if present.",
        example="no"
    )
    
    vomiting: Literal["yes", "no"] = Field(
        ...,
        description="Vomiting associated with chest pain presentation. Often seen with inferior MI "
                    "due to vagal stimulation. Adds 0.996 to risk if present.",
        example="no"
    )
    
    systolic_bp_low: Literal["yes", "no"] = Field(
        ...,
        description="Systolic blood pressure <100 mmHg. Hypotension may indicate cardiogenic shock "
                    "or significant myocardial dysfunction. Adds 1.353 to risk if present.",
        example="no"
    )
    
    current_smoker: Literal["yes", "no"] = Field(
        ...,
        description="Current tobacco smoker. Major modifiable risk factor for coronary artery disease. "
                    "Adds 0.675 to risk if present.",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "sex": "male",
                "sweating": "yes",
                "acute_ecg_ischemia": "no",
                "pain_radiating_right_arm": "no",
                "vomiting": "no",
                "systolic_bp_low": "no",
                "current_smoker": "yes"
            }
        }


class HeMacsResponse(BaseModel):
    """
    Response model for History and Electrocardiogram-only Manchester Acute Coronary Syndromes (HE-MACS)
    
    Returns the calculated probability of ACS or MACE within 30 days with risk stratification:
    - Very Low Risk (<4%): Consider discharge with follow-up
    - Low Risk (4-6.9%): Consider serial troponins
    - Moderate Risk (7-49.9%): Requires further investigation
    - High Risk (≥50%): Urgent cardiology consultation needed
    
    Clinical Application:
    - Allows rapid triage without waiting for troponin results
    - Identifies very low risk patients who may be suitable for discharge
    - High negative predictive value for very low risk category
    - Should be used alongside clinical judgment
    
    Reference: Alghamdi A, et al. Eur J Emerg Med. 2019;26(5):356-361.
    """
    
    result: float = Field(
        ...,
        description="Calculated probability of ACS or MACE within 30 days as a percentage (0-100%)",
        example=8.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="percent"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with management recommendations based on risk category",
        example="Moderate risk of ACS or major adverse cardiac events within 30 days. Requires further investigation with troponins and possible admission."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Very Low Risk, Low Risk, Moderate Risk, or High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the risk percentage range",
        example="7-49.9% risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 8.5,
                "unit": "percent",
                "interpretation": "Moderate risk of ACS or major adverse cardiac events within 30 days. Requires further investigation with troponins and possible admission.",
                "stage": "Moderate Risk",
                "stage_description": "7-49.9% risk"
            }
        }