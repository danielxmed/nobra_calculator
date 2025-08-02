"""
Troponin-only Manchester Acute Coronary Syndromes (T-MACS) Decision Aid Models

Request and response models for T-MACS calculation.

References (Vancouver style):
1. Body R, Carlton E, Sperrin M, et al. Troponin-only Manchester Acute Coronary 
   Syndromes (T-MACS) decision aid: single biomarker re-derivation and external 
   validation in three cohorts. Emerg Med J. 2017;34(6):349-356. 
   doi: 10.1136/emermed-2016-206366.
2. Greenslade JH, Carlton EW, Van Hise C, et al. Diagnostic accuracy of the 
   Troponin-only Manchester Acute Coronary Syndromes (T-MACS) decision aid 
   with a point-of-care cardiac troponin assay. Acad Emerg Med. 2020;27(6):459-466. 
   doi: 10.1111/acem.13953.
3. Body R, Burrows G, Carley S, et al. Rapid exclusion of acute myocardial infarction 
   in patients with undetectable troponin using a sensitive troponin I assay. 
   Clin Chem. 2015;61(7):983-989. doi: 10.1373/clinchem.2014.236232.

The T-MACS decision aid is a clinical prediction tool that uses high-sensitivity 
cardiac troponin T (hs-cTnT) concentration on arrival and clinical factors to 
calculate the probability of acute coronary syndrome (ACS) in emergency department 
patients presenting with chest pain. It can safely rule out ACS in approximately 
40% of patients with <1% probability of missed ACS, while ruling in ACS in 5% 
of patients with >95% probability.
"""

from pydantic import BaseModel, Field
from typing import Literal


class TroponinOnlyMacsRequest(BaseModel):
    """
    Request model for Troponin-only Manchester Acute Coronary Syndromes (T-MACS) Decision Aid
    
    The T-MACS decision aid uses a single high-sensitivity cardiac troponin T measurement 
    and clinical factors to calculate the probability of acute coronary syndrome in 
    emergency department patients presenting with chest pain.
    
    Clinical Parameters:
    
    Laboratory Parameter:
    - High-sensitivity cardiac troponin T (hs-cTnT): The only biomarker required. 
      Measured on arrival (single measurement, not serial). Normal reference range 
      is typically <14 ng/L, but elevated values increase ACS probability.
    
    Clinical Factors (each scored as present/absent):
    - EKG Ischemia: New ischemic changes on 12-lead ECG including ST depression 
      ≥0.5mm, ST elevation, T-wave inversion, or new LBBB.
    - Crescendo Angina: Worsening or crescendo pattern of chest pain with increasing 
      frequency, severity, or duration over hours to days.
    - Pain Radiating to Right Arm/Shoulder: Chest pain that radiates specifically 
      to the right arm or right shoulder (classic symptom).
    - Vomiting: Nausea or vomiting associated with chest pain episode.
    - Sweating: Diaphoresis or sweating observed by clinician or reported by patient.
    - Hypotension: Systolic blood pressure <100 mmHg documented during evaluation.
    
    Clinical Applications:
    The T-MACS tool is designed for use in emergency departments to:
    
    1. Rule Out ACS (Very Low Risk <2%):
       - Safely discharge patients with appropriate follow-up
       - Avoid unnecessary hospital admissions and serial troponin testing
       - Reduce healthcare costs and patient anxiety
    
    2. Risk Stratification (Low Risk 2-5%, Moderate Risk 5-95%):
       - Guide decision-making for observation periods
       - Determine need for serial troponin measurements
       - Consider stress testing or CT coronary angiography
    
    3. Rule In ACS (High Risk ≥95%):
       - Immediate cardiology consultation
       - Initiate ACS treatment protocols
       - Expedite cardiac catheterization if indicated
    
    Limitations and Considerations:
    - Not applicable to patients with obvious STEMI or ACS on presentation
    - Requires accurate troponin measurement with high-sensitivity assay
    - Should be used in conjunction with clinical judgment
    - Validated primarily in white European populations
    - May require adjustment for different troponin assays
    - Not validated in patients <25 years old
    
    Study Performance:
    In validation studies, T-MACS demonstrated:
    - 99.3% negative predictive value for ruling out ACS
    - 98.7% sensitivity for detecting ACS
    - Ability to rule out 37.7% of patients as very low risk
    - 100% positive predictive value in high-risk category
    
    Implementation Benefits:
    - Reduces average length of stay from 2 days to same-day discharge for low-risk patients
    - Superior performance compared to NICE guidelines
    - Over 3,500 patients successfully managed using T-MACS at Manchester Royal Infirmary
    - Significant reduction in unnecessary hospital admissions
    
    References:
    1. Body R, Carlton E, Sperrin M, et al. Troponin-only Manchester Acute Coronary 
       Syndromes (T-MACS) decision aid: single biomarker re-derivation and external 
       validation in three cohorts. Emerg Med J. 2017;34(6):349-356.
    2. Greenslade JH, Carlton EW, Van Hise C, et al. Diagnostic accuracy of the 
       Troponin-only Manchester Acute Coronary Syndromes (T-MACS) decision aid 
       with a point-of-care cardiac troponin assay. Acad Emerg Med. 2020;27(6):459-466.
    """
    
    hs_ctnt_ng_l: float = Field(
        ...,
        description="High-sensitivity cardiac troponin T concentration on arrival in ng/L. Normal <14 ng/L, values >100 ng/L strongly suggest myocardial injury.",
        ge=0,
        le=10000,
        example=25.0
    )
    
    ekg_ischemia: Literal["yes", "no"] = Field(
        ...,
        description="Presence of ischemic changes on 12-lead ECG (ST depression ≥0.5mm, ST elevation, T-wave inversion, or new LBBB).",
        example="no"
    )
    
    crescendo_angina: Literal["yes", "no"] = Field(
        ...,
        description="Worsening or crescendo pattern of angina with increasing frequency, severity, or duration over recent hours to days.",
        example="no"
    )
    
    pain_right_arm: Literal["yes", "no"] = Field(
        ...,
        description="Chest pain radiating specifically to the right arm or right shoulder (classic anginal symptom).",
        example="no"
    )
    
    vomiting: Literal["yes", "no"] = Field(
        ...,
        description="Nausea or vomiting associated with the chest pain episode (may indicate vagal response to ischemia).",
        example="no"
    )
    
    sweating: Literal["yes", "no"] = Field(
        ...,
        description="Diaphoresis or sweating observed by clinician or reported by patient during chest pain episode.",
        example="no"
    )
    
    hypotension: Literal["yes", "no"] = Field(
        ...,
        description="Hypotension with systolic blood pressure less than 100 mmHg documented during evaluation.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "hs_ctnt_ng_l": 25.0,
                "ekg_ischemia": "no",
                "crescendo_angina": "no",
                "pain_right_arm": "no",
                "vomiting": "no",
                "sweating": "no",
                "hypotension": "no"
            }
        }


class TroponinOnlyMacsResponse(BaseModel):
    """
    Response model for Troponin-only Manchester Acute Coronary Syndromes (T-MACS) Decision Aid
    
    The T-MACS result provides a probability of acute coronary syndrome and clinical 
    risk stratification with specific management recommendations:
    
    Risk Categories and Management:
    
    **Very Low Risk (<2% probability) - ACS Ruled Out:**
    - Clinical Action: Safe for discharge with appropriate safety netting
    - Follow-up: Outpatient cardiology follow-up if ongoing symptoms
    - Benefits: Avoids unnecessary admission, reduces healthcare costs
    - Evidence: 99.3% negative predictive value in validation studies
    
    **Low Risk (2-5% probability) - Low Risk:**
    - Clinical Action: Consider serial troponin in ED or observation unit
    - Monitoring: 3-6 hour observation with repeat troponin measurement
    - Discharge: If serial troponin negative and clinically stable
    - Follow-up: Early outpatient stress testing or cardiology evaluation
    
    **Moderate Risk (5-95% probability) - Intermediate Risk:**
    - Clinical Action: Requires further risk stratification
    - Testing: Serial troponin measurements over 6-12 hours
    - Advanced Testing: Consider stress testing or CT coronary angiography
    - Admission: May require overnight observation depending on clinical course
    - Management: Antiplatelet therapy if high suspicion and no contraindications
    
    **High Risk (≥95% probability) - ACS Ruled In:**
    - Clinical Action: Immediate cardiology consultation
    - Treatment: Initiate ACS treatment protocols immediately
    - Antiplatelet: Dual antiplatelet therapy unless contraindicated
    - Anticoagulation: Consider heparin or other anticoagulants
    - Interventional: Expedite cardiac catheterization if NSTEMI/unstable angina
    - Monitoring: Continuous cardiac monitoring and frequent vital signs
    
    Clinical Decision Support:
    
    **Emergency Department Management:**
    - Very Low Risk: Discharge planning with safety netting instructions
    - Low Risk: Short-term observation with repeat biomarkers
    - Moderate Risk: Extended observation with advanced testing
    - High Risk: Immediate ACS pathway activation
    
    **Quality Metrics:**
    - Sensitivity: 98.7% for detecting ACS
    - Specificity: High specificity for ruling out ACS
    - Negative Predictive Value: 99.3% in validation cohorts
    - Clinical Impact: 40% of patients can be classified as very low risk
    
    **Safety Considerations:**
    - All patients should receive clear discharge instructions
    - Return precautions for worsening or new symptoms
    - Follow-up arrangements within 72 hours for ongoing symptoms
    - Patient education about when to seek immediate medical attention
    
    **Implementation Benefits:**
    - Reduced average length of stay from 2 days to same-day discharge
    - Significant reduction in unnecessary admissions
    - Cost-effective approach to chest pain evaluation
    - Superior performance compared to traditional clinical pathways
    
    **Limitations:**
    - Requires high-sensitivity cardiac troponin T assay
    - Not applicable to obvious STEMI presentations
    - Should be interpreted within clinical context
    - May require local validation for different populations
    
    Reference: Body R, et al. Emerg Med J. 2017;34(6):349-356.
    """
    
    result: float = Field(
        ...,
        description="Calculated probability of acute coronary syndrome (range 0.000-1.000)",
        example=0.035
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the probability result",
        example="probability"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk stratification and management recommendations based on ACS probability",
        example="Low risk (3.5% probability) of acute coronary syndrome. Consider serial troponin measurement in the emergency department or observation unit to further stratify risk."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Very Low Risk, Low Risk, Moderate Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the clinical management approach",
        example="Low risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0.035,
                "unit": "probability",
                "interpretation": "Low risk (3.5% probability) of acute coronary syndrome. Consider serial troponin measurement in the emergency department or observation unit to further stratify risk.",
                "stage": "Low Risk",
                "stage_description": "Low risk"
            }
        }