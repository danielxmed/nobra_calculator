"""
Canadian Syncope Risk Score Models

Request and response models for Canadian Syncope Risk Score calculation.

References (Vancouver style):
1. Thiruganasambandamoorthy V, Kwong K, Wells GA, Sivilotti ML, Mukarram M, 
   Rowe BH, et al. Development of the Canadian Syncope Risk Score to predict 
   serious adverse events after emergency department assessment of syncope. 
   CMAJ. 2016 Sep 6;188(12):E289-98. doi: 10.1503/cmaj.151469.
2. Thiruganasambandamoorthy V, Sivilotti MLA, Le Sage N, Yan JW, Huang P, 
   Hegdekar M, et al. Multicenter Emergency Department Validation of the 
   Canadian Syncope Risk Score. JAMA Intern Med. 2020 May 1;180(5):737-44. 
   doi: 10.1001/jamainternmed.2020.0288.
3. Thiruganasambandamoorthy V, Hess EP, Turko E, Perry JJ, Wells GA, Stiell IG. 
   Outcomes in Canadian emergency department syncope patients--are we doing a 
   good job? J Emerg Med. 2013 Feb;44(2):321-8. doi: 10.1016/j.jemermed.2012.06.028.

The Canadian Syncope Risk Score predicts 30-day serious adverse events in patients
presenting with syncope, helping guide disposition decisions in the emergency department.
"""

from pydantic import BaseModel, Field
from typing import Literal


class CanadianSyncopeRiskScoreRequest(BaseModel):
    """
    Request model for Canadian Syncope Risk Score
    
    The Canadian Syncope Risk Score (CSRS) is a validated tool for predicting 
    30-day serious adverse events in patients presenting with syncope to the ED.
    
    Inclusion criteria:
    - Age ≥16 years
    - Presenting within 24 hours of syncope
    
    Exclusion criteria:
    - Prolonged loss of consciousness (>5 minutes)
    - Change in mental status from baseline
    - Obvious witnessed seizure
    - Major trauma requiring admission
    - Intoxication with alcohol or illicit drugs
    - Language barrier
    - Head trauma causing loss of consciousness
    
    Serious adverse events include:
    - Death
    - Arrhythmia
    - Myocardial infarction
    - Serious structural heart disease
    - Aortic dissection
    - Pulmonary embolism
    - Severe pulmonary hypertension
    - Severe hemorrhage
    - Subarachnoid hemorrhage
    - Other serious conditions requiring intervention
    
    Score interpretation:
    - Very Low Risk (-3 to -2): 0.4-0.7% risk
    - Low Risk (-1 to 0): 1.2-1.9% risk
    - Medium Risk (1-3): 3.1-8.1% risk
    - High Risk (4-5): 12.9-19.7% risk
    - Very High Risk (6-11): 28.9-83.6% risk
    
    References (Vancouver style):
    1. Thiruganasambandamoorthy V, Kwong K, Wells GA, Sivilotti ML, Mukarram M, 
    Rowe BH, et al. Development of the Canadian Syncope Risk Score to predict 
    serious adverse events after emergency department assessment of syncope. 
    CMAJ. 2016 Sep 6;188(12):E289-98.
    """
    
    vasovagal_predisposition: Literal["yes", "no"] = Field(
        ...,
        description="Predisposition to vasovagal symptoms (triggered by being in a warm crowded place, prolonged standing, fear, emotion, or pain). Scores -1 point if yes",
        example="no"
    )
    
    heart_disease_history: Literal["yes", "no"] = Field(
        ...,
        description="History of heart disease including: coronary artery disease (CAD), atrial fibrillation or flutter, congestive heart failure (CHF), or valvular disease. Scores +1 point if yes",
        example="no"
    )
    
    systolic_bp_abnormal: Literal["yes", "no"] = Field(
        ...,
        description="Any systolic blood pressure reading <90 mmHg or >180 mmHg in the emergency department. Scores +2 points if yes",
        example="no"
    )
    
    troponin_elevated: Literal["yes", "no"] = Field(
        ...,
        description="Troponin level above the 99th percentile for the normal population. Scores +2 points if yes",
        example="no"
    )
    
    abnormal_qrs_axis: Literal["yes", "no"] = Field(
        ...,
        description="Abnormal QRS axis on ECG (axis <-30° or >100°). Scores +1 point if yes",
        example="no"
    )
    
    qrs_duration_prolonged: Literal["yes", "no"] = Field(
        ...,
        description="QRS duration >130 ms on ECG. Scores +1 point if yes",
        example="no"
    )
    
    qtc_interval_prolonged: Literal["yes", "no"] = Field(
        ...,
        description="Corrected QT interval >480 ms on ECG. Scores +2 points if yes",
        example="no"
    )
    
    ed_diagnosis: Literal["vasovagal_syncope", "cardiac_syncope", "neither"] = Field(
        ...,
        description="Emergency department diagnosis: vasovagal syncope (-2 points), cardiac syncope (+2 points), or neither (0 points)",
        example="neither"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "vasovagal_predisposition": "no",
                "heart_disease_history": "no",
                "systolic_bp_abnormal": "no",
                "troponin_elevated": "no",
                "abnormal_qrs_axis": "no",
                "qrs_duration_prolonged": "no",
                "qtc_interval_prolonged": "no",
                "ed_diagnosis": "neither"
            }
        }


class CanadianSyncopeRiskScoreResponse(BaseModel):
    """
    Response model for Canadian Syncope Risk Score
    
    The CSRS provides risk stratification for 30-day serious adverse events:
    
    Risk categories:
    - Very Low Risk (-3 to -2): Safe for discharge with routine follow-up
    - Low Risk (-1 to 0): Consider discharge with close follow-up
    - Medium Risk (1-3): Further ED evaluation and monitoring recommended
    - High Risk (4-5): Admission recommended with cardiac monitoring
    - Very High Risk (6-11): Urgent admission and cardiology consultation
    
    Performance characteristics:
    - Sensitivity: 99.2% for score ≥-2
    - Sensitivity: 97.7% for score ≥-1
    - C-statistic: 0.88 (95% CI 0.85-0.90)
    
    The score helps identify which patients can be safely discharged and which 
    require admission or further investigation for serious underlying causes.
    
    Reference: Thiruganasambandamoorthy V, et al. CMAJ. 2016;188(12):E289-98.
    """
    
    result: int = Field(
        ...,
        description="Canadian Syncope Risk Score (range: -3 to 11 points)",
        example=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (points)",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommendations based on risk category",
        example="Low risk of serious adverse event within 30 days. Consider discharge home with close follow-up. Outpatient evaluation may be appropriate based on clinical judgment."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Very Low Risk, Low Risk, Medium Risk, High Risk, or Very High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Percentage risk of serious adverse event within 30 days",
        example="1.2-1.9% risk of serious adverse event"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "Low risk of serious adverse event within 30 days. Consider discharge home with close follow-up. Outpatient evaluation may be appropriate based on clinical judgment.",
                "stage": "Low Risk",
                "stage_description": "1.2-1.9% risk of serious adverse event"
            }
        }