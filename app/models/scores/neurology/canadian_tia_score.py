"""
Canadian Transient Ischemic Attack (TIA) Score Models

Request and response models for Canadian TIA Score calculation.

References (Vancouver style):
1. Perry JJ, Sharma M, Sivilotti ML, Sutherland J, Symington C, Worster A, et al. 
   Prospective validation of the ABCD2 score for patients in the emergency department 
   with transient ischemic attack. CMAJ. 2011 Jul 12;183(10):1137-45. 
   doi: 10.1503/cmaj.101668.
2. Perry JJ, Sivilotti ML, Sutherland J, Hohl CM, Émond M, Calder LA, et al. 
   Validation of the Ottawa Subarachnoid Hemorrhage Rule in patients with acute 
   headache. CMAJ. 2013 Nov 19;185(17):E805-12. doi: 10.1503/cmaj.121745.
3. Perry JJ, Sharma M, Sivilotti ML, Sutherland J, Worster A, Émond M, et al. 
   A prospective cohort study of patients with transient ischemic attack to identify 
   high-risk clinical characteristics. Stroke. 2014 Jan;45(1):92-100. 
   doi: 10.1161/STROKEAHA.113.003085.

The Canadian TIA Score identifies risk of stroke, carotid endarterectomy, or carotid 
artery stenting within 7 days in patients who experienced TIA symptoms. It incorporates 
13 predictive variables from history, physical examination, and testing routinely 
performed in the emergency department, and is more accurate than ABCD² and ABCD²I 
scores for 7-day stroke risk prediction.
"""

from pydantic import BaseModel, Field
from typing import Literal


class CanadianTiaScoreRequest(BaseModel):
    """
    Request model for Canadian Transient Ischemic Attack (TIA) Score
    
    The Canadian TIA Score is a validated clinical decision tool that predicts 
    7-day risk of stroke, carotid endarterectomy, or carotid artery stenting 
    in patients presenting with TIA symptoms.
    
    The score incorporates 13 clinical variables:
    
    Clinical History Variables:
    - First TIA in lifetime (+2 points if yes)
    - Symptoms ≥10 minutes (+2 points if yes)
    - History of carotid stenosis (+2 points if yes)
    - Already on antiplatelet therapy (+3 points if yes)
    - History of gait disturbance (+1 point if yes)
    - History of unilateral weakness (+1 point if yes)
    - History of vertigo (-3 points if yes) [only negative score]
    
    Physical Examination Variables:
    - Initial triage diastolic BP ≥110 mmHg (+3 points if yes)
    - Dysarthria or aphasia (+1 point if yes)
    
    Investigation Variables (ED testing):
    - Atrial fibrillation on ECG (+2 points if yes)
    - Infarction on CT scan (+1 point if yes)
    - Platelet count ≥400×10⁹/L (+2 points if yes)
    - Glucose ≥15 mmol/L (270 mg/dL) (+3 points if yes)
    
    Risk Stratification:
    - Low Risk (≤3 points): 0.01-0.5% risk within 7 days
    - Medium Risk (4-8 points): 1-5% risk within 7 days
    - High Risk (≥9 points): 5.9-27.6% risk within 7 days
    
    Performance: More accurate than ABCD² (AUC 0.70 vs 0.60) and ABCD²I 
    (AUC 0.70 vs 0.64) for predicting 7-day outcomes.
    
    References (Vancouver style):
    1. Perry JJ, Sharma M, Sivilotti ML, Sutherland J, Worster A, Émond M, et al. 
    A prospective cohort study of patients with transient ischemic attack to identify 
    high-risk clinical characteristics. Stroke. 2014 Jan;45(1):92-100.
    """
    
    first_tia_lifetime: Literal["yes", "no"] = Field(
        ...,
        description="First TIA episode in patient's lifetime. Scores +2 points if yes",
        example="no"
    )
    
    symptoms_ten_minutes: Literal["yes", "no"] = Field(
        ...,
        description="TIA symptoms lasted 10 minutes or longer. Scores +2 points if yes",
        example="yes"
    )
    
    history_carotid_stenosis: Literal["yes", "no"] = Field(
        ...,
        description="Known history of carotid artery stenosis (>50% stenosis). Scores +2 points if yes",
        example="no"
    )
    
    on_antiplatelet_therapy: Literal["yes", "no"] = Field(
        ...,
        description="Patient already on antiplatelet therapy (ASA, clopidogrel, etc.) at time of TIA. Scores +3 points if yes",
        example="no"
    )
    
    history_gait_disturbance: Literal["yes", "no"] = Field(
        ...,
        description="History of gait disturbance or ataxia during the TIA episode. Scores +1 point if yes",
        example="no"
    )
    
    history_unilateral_weakness: Literal["yes", "no"] = Field(
        ...,
        description="History of unilateral motor weakness during the TIA episode. Scores +1 point if yes",
        example="yes"
    )
    
    history_vertigo: Literal["yes", "no"] = Field(
        ...,
        description="History of vertigo during the TIA episode. Scores -3 points if yes (protective factor)",
        example="no"
    )
    
    diastolic_bp_110: Literal["yes", "no"] = Field(
        ...,
        description="Initial triage diastolic blood pressure ≥110 mmHg in the emergency department. Scores +3 points if yes",
        example="no"
    )
    
    dysarthria_aphasia: Literal["yes", "no"] = Field(
        ...,
        description="Presence of dysarthria (speech difficulty) or aphasia (language difficulty) during the TIA episode. Scores +1 point if yes",
        example="yes"
    )
    
    atrial_fibrillation_ecg: Literal["yes", "no"] = Field(
        ...,
        description="Atrial fibrillation detected on ECG performed in the emergency department. Scores +2 points if yes",
        example="no"
    )
    
    infarction_on_ct: Literal["yes", "no"] = Field(
        ...,
        description="Acute infarction visible on CT scan of the head. Scores +1 point if yes",
        example="no"
    )
    
    platelet_count_400: Literal["yes", "no"] = Field(
        ...,
        description="Platelet count ≥400×10⁹/L (400,000/μL) on laboratory testing. Scores +2 points if yes",
        example="no"
    )
    
    glucose_15_mmol: Literal["yes", "no"] = Field(
        ...,
        description="Blood glucose ≥15 mmol/L (270 mg/dL) on laboratory testing. Scores +3 points if yes",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "first_tia_lifetime": "no",
                "symptoms_ten_minutes": "yes",
                "history_carotid_stenosis": "no",
                "on_antiplatelet_therapy": "no",
                "history_gait_disturbance": "no",
                "history_unilateral_weakness": "yes",
                "history_vertigo": "no",
                "diastolic_bp_110": "no",
                "dysarthria_aphasia": "yes",
                "atrial_fibrillation_ecg": "no",
                "infarction_on_ct": "no",
                "platelet_count_400": "no",
                "glucose_15_mmol": "no"
            }
        }


class CanadianTiaScoreResponse(BaseModel):
    """
    Response model for Canadian Transient Ischemic Attack (TIA) Score
    
    The Canadian TIA Score provides risk stratification for stroke, carotid 
    endarterectomy, or carotid artery stenting within 7 days:
    
    Risk Categories:
    - Low Risk (≤3 points): 0.01-0.5% risk - discharge with outpatient follow-up
    - Medium Risk (4-8 points): 1-5% risk - consider admission or urgent outpatient workup
    - High Risk (≥9 points): 5.9-27.6% risk - recommend admission and urgent evaluation
    
    Clinical Applications:
    - Superior to ABCD² and ABCD²I scores for 7-day risk prediction
    - Helps guide ED disposition decisions (discharge vs. admission)
    - Informs timing of investigations and specialist referral
    - Assists in prioritizing patients for urgent vs. routine care
    
    Performance Characteristics:
    - Area under the curve: 0.70 (95% CI 0.66-0.73)
    - Sensitivity for high-risk outcomes: 75.9% at score ≥4
    - Specificity: 53.8% at score ≥4
    - Validated in 8,355 patients across multiple centers
    
    Reference: Perry JJ, et al. Stroke. 2014;45(1):92-100.
    """
    
    result: int = Field(
        ...,
        description="Canadian TIA Score calculated from clinical variables (range: -3 to 23 points)",
        example=5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on risk category",
        example="Medium risk of stroke, carotid endarterectomy, or carotid artery stenting within 7 days. Consider admission or urgent outpatient workup within 24-48 hours. Expedited imaging and specialist consultation recommended."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Medium Risk, or High Risk)",
        example="Medium Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Percentage risk of adverse outcome within 7 days",
        example="1-5% risk of stroke/intervention within 7 days"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 5,
                "unit": "points",
                "interpretation": "Medium risk of stroke, carotid endarterectomy, or carotid artery stenting within 7 days. Consider admission or urgent outpatient workup within 24-48 hours. Expedited imaging and specialist consultation recommended.",
                "stage": "Medium Risk",
                "stage_description": "1-5% risk of stroke/intervention within 7 days"
            }
        }