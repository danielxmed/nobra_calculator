"""
tPA Contraindications for Ischemic Stroke Models

Request and response models for tPA contraindications assessment.

References (Vancouver style):
1. Powers WJ, Rabinstein AA, Ackerson T, Adeoye OM, Bambakidis NC, Becker K, et al. 
   Guidelines for the Early Management of Patients With Acute Ischemic Stroke: 2019 
   Update to the 2018 Guidelines for the Early Management of Acute Ischemic Stroke: 
   A Guideline for Healthcare Professionals From the American Heart Association/American 
   Stroke Association. Stroke. 2019 Dec;50(12):e344-e418. doi: 10.1161/STR.0000000000000211.
2. Hacke W, Kaste M, Bluhmki E, Brozman M, Dávalos A, Guidetti D, et al. Thrombolysis 
   with alteplase 3 to 4.5 hours after acute ischemic stroke. N Engl J Med. 2008 Sep 
   25;359(13):1317-29. doi: 10.1056/NEJMoa0804656.
3. Jauch EC, Saver JL, Adams HP Jr, Bruno A, Connors JJ, Demaerschalk BM, et al. 
   Guidelines for the early management of patients with acute ischemic stroke: a guideline 
   for healthcare professionals from the American Heart Association/American Stroke 
   Association. Stroke. 2013 Mar;44(3):870-947. doi: 10.1161/STR.0b013e318284056a.

IV tPA (alteplase) is the standard thrombolytic therapy for acute ischemic stroke within 
4.5 hours of symptom onset. This tool evaluates absolute and relative contraindications 
based on AHA/ASA guidelines to determine eligibility and bleeding risk.
"""

from pydantic import BaseModel, Field
from typing import Literal, List, Optional


class TpaContraindicationsRequest(BaseModel):
    """
    Request model for tPA Contraindications assessment
    
    Evaluates eligibility for IV tPA in acute ischemic stroke by checking:
    1. Time window (critical for eligibility)
    2. Absolute contraindications (unacceptable bleeding risk)
    3. Relative contraindications (require risk-benefit analysis)
    
    Standard window: 0-3 hours from symptom onset
    Extended window: 3-4.5 hours (with additional exclusions)
    
    References (Vancouver style):
    1. Powers WJ, Rabinstein AA, Ackerson T, Adeoye OM, Bambakidis NC, Becker K, et al. 
       Guidelines for the Early Management of Patients With Acute Ischemic Stroke: 2019 
       Update to the 2018 Guidelines for the Early Management of Acute Ischemic Stroke. 
       Stroke. 2019 Dec;50(12):e344-e418.
    """
    
    # Time window - critical determination
    symptom_onset_time: Literal["within_3_hours", "3_to_4_5_hours", "over_4_5_hours", "unknown"] = Field(
        ...,
        description="Time since symptom onset. Standard window is within 3 hours, extended window 3-4.5 hours with additional exclusions",
        example="within_3_hours"
    )
    
    age: int = Field(
        ...,
        ge=0,
        le=120,
        description="Patient age in years. Age >80 is a contraindication for extended window (3-4.5 hours)",
        example=65
    )
    
    # History - Absolute contraindications
    ischemic_stroke_within_3_months: Literal["yes", "no"] = Field(
        ...,
        description="History of ischemic stroke within 3 months (absolute contraindication)",
        example="no"
    )
    
    severe_head_trauma_within_3_months: Literal["yes", "no"] = Field(
        ...,
        description="Severe head trauma within 3 months (absolute contraindication)",
        example="no"
    )
    
    intracranial_surgery_within_3_months: Literal["yes", "no"] = Field(
        ...,
        description="Intracranial or intraspinal surgery within 3 months (absolute contraindication)",
        example="no"
    )
    
    history_intracranial_hemorrhage: Literal["yes", "no"] = Field(
        ...,
        description="Any history of intracranial hemorrhage (absolute contraindication)",
        example="no"
    )
    
    # Current clinical findings - Absolute contraindications
    subarachnoid_hemorrhage: Literal["yes", "no"] = Field(
        ...,
        description="Symptoms suggestive of subarachnoid hemorrhage (absolute contraindication)",
        example="no"
    )
    
    gi_malignancy_bleeding_21_days: Literal["yes", "no"] = Field(
        ...,
        description="GI malignancy or GI bleeding within 21 days (absolute contraindication)",
        example="no"
    )
    
    coagulopathy: Literal["yes", "no"] = Field(
        ...,
        description="Known bleeding diathesis or coagulopathy (absolute contraindication)",
        example="no"
    )
    
    # Laboratory findings - Absolute contraindications
    inr_greater_1_7: Literal["yes", "no"] = Field(
        ...,
        description="INR >1.7 or PT >15 seconds (absolute contraindication)",
        example="no"
    )
    
    aptt_greater_40: Literal["yes", "no"] = Field(
        ...,
        description="aPTT >40 seconds (absolute contraindication)",
        example="no"
    )
    
    platelet_count_less_100k: Literal["yes", "no"] = Field(
        ...,
        description="Platelet count <100,000/mm³ (absolute contraindication)",
        example="no"
    )
    
    # Medications - Absolute contraindications
    tc_48h_lmwh: Literal["yes", "no"] = Field(
        ...,
        description="Treatment dose of low molecular weight heparin within 24 hours (absolute contraindication)",
        example="no"
    )
    
    thrombin_factor_xa_inhibitors: Literal["yes", "no"] = Field(
        ...,
        description="Current use of direct thrombin inhibitors or direct factor Xa inhibitors (absolute contraindication)",
        example="no"
    )
    
    # Other labs/vitals - Absolute contraindications
    glucose_less_50: Literal["yes", "no"] = Field(
        ...,
        description="Blood glucose <50 mg/dL (absolute contraindication)",
        example="no"
    )
    
    # Imaging findings - Absolute contraindications
    ct_ich: Literal["yes", "no"] = Field(
        ...,
        description="CT demonstrates intracranial hemorrhage (absolute contraindication)",
        example="no"
    )
    
    ct_hypodensity_one_third: Literal["yes", "no"] = Field(
        ...,
        description="CT shows multilobar infarction with hypodensity >1/3 cerebral hemisphere (absolute contraindication for extended window)",
        example="no"
    )
    
    # Blood pressure - Absolute contraindications
    sbp_greater_185: Literal["yes", "no"] = Field(
        ...,
        description="Systolic blood pressure >185 mmHg (absolute contraindication)",
        example="no"
    )
    
    dbp_greater_110: Literal["yes", "no"] = Field(
        ...,
        description="Diastolic blood pressure >110 mmHg (absolute contraindication)",
        example="no"
    )
    
    # Other conditions - Absolute contraindications
    infective_endocarditis: Literal["yes", "no"] = Field(
        ...,
        description="Active bacterial endocarditis (absolute contraindication)",
        example="no"
    )
    
    aortic_dissection: Literal["yes", "no"] = Field(
        ...,
        description="Known or suspected aortic arch dissection (absolute contraindication)",
        example="no"
    )
    
    neoplasm_increased_bleeding: Literal["yes", "no"] = Field(
        ...,
        description="Known intracranial neoplasm with increased bleeding risk (absolute contraindication)",
        example="no"
    )
    
    # Relative contraindications - Optional fields
    minor_symptoms: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Only minor and non-disabling stroke symptoms (relative contraindication)",
        example="no"
    )
    
    symptoms_clearing: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Stroke symptoms clearing spontaneously (relative contraindication)",
        example="no"
    )
    
    pregnancy: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Pregnancy (relative contraindication)",
        example="no"
    )
    
    seizure_at_onset: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Seizure at stroke onset with postictal neurological impairments (relative contraindication)",
        example="no"
    )
    
    major_surgery_14_days: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Major surgery or serious trauma within 14 days (relative contraindication)",
        example="no"
    )
    
    gi_hemorrhage_21_days: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Recent GI or urinary tract hemorrhage within 21 days (relative contraindication)",
        example="no"
    )
    
    mi_within_3_months: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Recent acute myocardial infarction within 3 months (relative contraindication)",
        example="no"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "symptom_onset_time": "within_3_hours",
                "age": 65,
                "ischemic_stroke_within_3_months": "no",
                "severe_head_trauma_within_3_months": "no",
                "intracranial_surgery_within_3_months": "no",
                "history_intracranial_hemorrhage": "no",
                "subarachnoid_hemorrhage": "no",
                "gi_malignancy_bleeding_21_days": "no",
                "coagulopathy": "no",
                "inr_greater_1_7": "no",
                "aptt_greater_40": "no",
                "platelet_count_less_100k": "no",
                "tc_48h_lmwh": "no",
                "thrombin_factor_xa_inhibitors": "no",
                "glucose_less_50": "no",
                "ct_ich": "no",
                "ct_hypodensity_one_third": "no",
                "sbp_greater_185": "no",
                "dbp_greater_110": "no",
                "infective_endocarditis": "no",
                "aortic_dissection": "no",
                "neoplasm_increased_bleeding": "no"
            }
        }
    }


class TpaContraindicationsResponse(BaseModel):
    """
    Response model for tPA Contraindications assessment
    
    Provides eligibility determination with detailed listing of:
    - Absolute contraindications (if any)
    - Relative contraindications (if any)
    - Clinical recommendations based on findings
    
    Reference: Powers WJ, et al. Stroke. 2019;50(12):e344-e418.
    """
    
    result: str = Field(
        ...,
        description="Eligibility assessment result",
        example="Eligible for tPA"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for this assessment)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with specific recommendations based on contraindications found",
        example="No contraindications identified for IV tPA administration (within 3 hours). Proceed with standard dosing: 0.9 mg/kg (maximum 90 mg), with 10% as bolus over 1 minute and remainder infused over 60 minutes. Monitor closely for bleeding."
    )
    
    stage: str = Field(
        ...,
        description="Contraindication category (Eligible, Relative Contraindication, or Absolute Contraindication)",
        example="Eligible"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of contraindication status",
        example="No contraindications"
    )
    
    absolute_contraindications: List[str] = Field(
        ...,
        description="List of absolute contraindications identified",
        example=[]
    )
    
    relative_contraindications: List[str] = Field(
        ...,
        description="List of relative contraindications identified",
        example=[]
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "result": "Eligible for tPA",
                "unit": "",
                "interpretation": "No contraindications identified for IV tPA administration (within 3 hours). Proceed with standard dosing: 0.9 mg/kg (maximum 90 mg), with 10% as bolus over 1 minute and remainder infused over 60 minutes. Monitor closely for bleeding.",
                "stage": "Eligible",
                "stage_description": "No contraindications",
                "absolute_contraindications": [],
                "relative_contraindications": []
            }
        }
    }