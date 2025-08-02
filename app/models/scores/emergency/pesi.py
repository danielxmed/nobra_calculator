"""
Pulmonary Embolism Severity Index (PESI) Models

Request and response models for PESI calculation.

References (Vancouver style):
1. Aujesky D, Obrosky DS, Stone RA, Auble TE, Perrier A, Cornuz J, et al. 
   Derivation and validation of a prognostic model for pulmonary embolism. 
   Am J Respir Crit Care Med. 2005;172(8):1041-6. doi: 10.1164/rccm.200506-862OC.
2. Aujesky D, Roy PM, Verschuren F, Righini M, Osterwalder J, Egloff M, et al. 
   Outpatient versus inpatient treatment for patients with acute pulmonary 
   embolism: an international, open-label, randomised, non-inferiority trial. 
   Lancet. 2011;378(9785):41-8. doi: 10.1016/S0140-6736(11)60824-6.
3. Jiménez D, Aujesky D, Moores L, Gómez V, Lobo JL, Uresandi F, et al. 
   Simplification of the pulmonary embolism severity index for prognostication 
   in patients with acute symptomatic pulmonary embolism. Arch Intern Med. 
   2010;170(15):1383-9. doi: 10.1001/archinternmed.2010.199.
4. Kearon C, Akl EA, Ornelas J, Blaivas A, Jimenez D, Bounameaux H, et al. 
   Antithrombotic Therapy for VTE Disease: CHEST Guideline and Expert Panel Report. 
   Chest. 2016;149(2):315-352. doi: 10.1016/j.chest.2015.11.026.

The Pulmonary Embolism Severity Index (PESI) is a extensively validated prognostic 
tool that predicts 30-day mortality and morbidity in patients with acute pulmonary 
embolism. Developed by Aujesky et al. in 2005 from a cohort of over 15,000 patients, 
PESI uses 11 readily available clinical variables to stratify patients into five 
risk classes with corresponding 30-day mortality rates.

Clinical Applications:
- Risk stratification for disposition planning (outpatient vs. inpatient)
- Guiding intensity of monitoring and treatment
- Identifying low-risk patients suitable for outpatient management
- Prognostication and patient/family counseling
- Quality improvement initiatives for PE care pathways
- Research stratification and clinical trial enrollment

PESI Calculation Method:
The PESI score incorporates 11 clinical variables with the following point assignments:
- Age: Absolute age value (e.g., 65 years = 65 points)
- Male sex: +10 points
- Cancer history: +30 points (active cancer or treatment within 6 months)
- Heart failure history: +10 points
- Chronic lung disease: +10 points
- Heart rate ≥110 bpm: +20 points
- Systolic BP <100 mmHg: +30 points
- Respiratory rate ≥30/min: +20 points
- Temperature <36°C: +20 points
- Altered mental status: +60 points
- Oxygen saturation <90%: +20 points

Risk Classes and 30-Day Mortality:
- Class I (≤65 points): 0.0-1.6% mortality (Very Low Risk)
- Class II (66-85 points): 1.7-3.5% mortality (Low Risk)
- Class III (86-105 points): 3.2-7.1% mortality (Intermediate Risk)
- Class IV (106-125 points): 4.0-11.4% mortality (High Risk)
- Class V (≥126 points): 10.0-24.5% mortality (Very High Risk)

Clinical Decision Making:
- Classes I and II: Consider outpatient management with oral anticoagulation
- Class III: Careful evaluation for outpatient eligibility, may require brief hospitalization
- Classes IV and V: Inpatient management with close monitoring and advanced therapies

Validation and Performance:
- Area under ROC curve (c-index): 0.78 in derivation, 0.77 in internal validation
- External validation across multiple studies and populations
- Strong evidence supporting use in clinical guidelines
- Comparable performance to Wells score for prognostication
- Superior to clinical gestalt for identifying low-risk patients

Limitations:
- Does not predict recurrence risk or guide anticoagulation duration
- May not capture all clinical nuances affecting prognosis
- Requires clinical judgment for final disposition decisions
- Social factors and support systems not incorporated in score
- Does not assess bleeding risk for anticoagulation

Implementation Considerations:
- Should be calculated for all patients with confirmed PE
- Results should supplement, not replace, clinical judgment
- Consider simplified PESI (sPESI) for streamlined assessment
- Reassess if clinical condition changes during treatment
- Document rationale for decisions that deviate from score recommendations

The PESI has revolutionized PE management by providing evidence-based risk 
stratification that safely identifies patients appropriate for outpatient treatment, 
reducing healthcare costs while maintaining excellent patient outcomes.
"""

from pydantic import BaseModel, Field
from typing import Literal


class PesiRequest(BaseModel):
    """
    Request model for Pulmonary Embolism Severity Index (PESI)
    
    PESI utilizes 11 readily available clinical variables to assess 30-day mortality 
    risk in patients with acute pulmonary embolism. The score guides critical decisions 
    about disposition, monitoring intensity, and treatment approach.
    
    Clinical Variable Categories:
    
    1. Demographics (Age, Sex):
       - Age contributes its absolute value (e.g., 65 years = 65 points)
       - Male sex associated with higher mortality (+10 points)
    
    2. Comorbidities (Cancer, Heart Failure, Chronic Lung Disease):
       - Cancer: Active malignancy or treatment within 6 months (+30 points)
       - Heart failure: Known diagnosis or clinical signs of CHF (+10 points)
       - Chronic lung disease: COPD, ILD, or chronic respiratory impairment (+10 points)
    
    3. Vital Signs and Clinical Findings:
       - Heart rate ≥110 bpm: Indicates hemodynamic stress (+20 points)
       - Systolic BP <100 mmHg: Suggests hemodynamic compromise (+30 points)
       - Respiratory rate ≥30/min: Indicates respiratory distress (+20 points)
       - Temperature <36°C: Associated with poor prognosis (+20 points)
       - Altered mental status: Confusion, somnolence, or coma (+60 points)
       - Oxygen saturation <90%: Indicates significant hypoxemia (+20 points)
    
    Assessment Guidelines:
    - Use initial vital signs and clinical findings at presentation
    - Cancer history includes active treatment or diagnosis within 6 months
    - Heart failure includes both systolic and diastolic dysfunction
    - Chronic lung disease includes COPD, pulmonary fibrosis, and other chronic conditions
    - Altered mental status is any deviation from baseline cognitive function
    - Oxygen saturation should be measured on room air when possible
    
    Clinical Context:
    - Calculate for all patients with confirmed acute PE
    - Consider patient-specific factors not captured in the score
    - Use in conjunction with bleeding risk assessment
    - Evaluate social support and follow-up capabilities for outpatient management
    - Document rationale for decisions that deviate from score recommendations
    
    References: See module docstring for complete citation list.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in years. Age contributes its absolute value as points to the total PESI score (e.g., a 65-year-old patient receives 65 points for age).",
        example=65
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient biological sex. Male sex is associated with higher mortality risk in pulmonary embolism and contributes 10 points to the PESI score.",
        example="male"
    )
    
    cancer_history: Literal["yes", "no"] = Field(
        ...,
        description="History of cancer, defined as active malignancy or cancer treatment (chemotherapy, radiation, surgery) within the previous 6 months. Contributes 30 points if present due to significantly increased mortality risk.",
        example="no"
    )
    
    heart_failure_history: Literal["yes", "no"] = Field(
        ...,
        description="History of heart failure including both systolic and diastolic dysfunction, or clinical signs of congestive heart failure. Contributes 10 points if present due to reduced cardiopulmonary reserve.",
        example="no"
    )
    
    chronic_lung_disease_history: Literal["yes", "no"] = Field(
        ...,
        description="History of chronic lung disease including COPD, interstitial lung disease, pulmonary fibrosis, or other chronic respiratory impairment. Contributes 10 points if present due to limited respiratory reserve.",
        example="yes"
    )
    
    heart_rate_110_or_higher: Literal["yes", "no"] = Field(
        ...,
        description="Heart rate 110 beats per minute or higher at presentation. Tachycardia indicates hemodynamic stress and contributes 20 points to reflect increased mortality risk.",
        example="yes"
    )
    
    systolic_bp_less_than_100: Literal["yes", "no"] = Field(
        ...,
        description="Systolic blood pressure less than 100 mmHg at presentation. Hypotension suggests hemodynamic compromise and contributes 30 points due to significantly increased mortality risk.",
        example="no"
    )
    
    respiratory_rate_30_or_higher: Literal["yes", "no"] = Field(
        ...,
        description="Respiratory rate 30 breaths per minute or higher at presentation. Tachypnea indicates respiratory distress and contributes 20 points to the PESI score.",
        example="no"
    )
    
    temperature_less_than_36: Literal["yes", "no"] = Field(
        ...,
        description="Body temperature less than 36°C (96.8°F) at presentation. Hypothermia is associated with poor prognosis and contributes 20 points to the PESI score.",
        example="no"
    )
    
    altered_mental_status: Literal["yes", "no"] = Field(
        ...,
        description="Altered mental status including confusion, disorientation, somnolence, stupor, or coma. Any deviation from baseline cognitive function contributes 60 points due to very high mortality risk.",
        example="no"
    )
    
    oxygen_saturation_less_than_90: Literal["yes", "no"] = Field(
        ...,
        description="Oxygen saturation less than 90% on room air at presentation. Significant hypoxemia indicates severe pulmonary compromise and contributes 20 points to the PESI score.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "sex": "male",
                "cancer_history": "no",
                "heart_failure_history": "no",
                "chronic_lung_disease_history": "yes",
                "heart_rate_110_or_higher": "yes",
                "systolic_bp_less_than_100": "no",
                "respiratory_rate_30_or_higher": "no",
                "temperature_less_than_36": "no",
                "altered_mental_status": "no",
                "oxygen_saturation_less_than_90": "no"
            }
        }


class PesiResponse(BaseModel):
    """
    Response model for Pulmonary Embolism Severity Index (PESI)
    
    The PESI score provides evidence-based risk stratification for patients with 
    acute pulmonary embolism, guiding critical decisions about disposition, monitoring 
    intensity, and treatment approach. Understanding PESI results is essential for 
    optimal PE management and patient safety.
    
    Risk Class Interpretation and Management:
    
    Class I - Very Low Risk (≤65 points, 0.0-1.6% mortality):
    - Excellent prognosis with minimal risk of adverse outcomes
    - Strong candidate for outpatient management with oral anticoagulation
    - Requires appropriate social support and follow-up within 24-72 hours
    - Consider patient preferences and comorbidities not captured in score
    - Ensure no contraindications to outpatient treatment (bleeding risk, adherence concerns)
    
    Class II - Low Risk (66-85 points, 1.7-3.5% mortality):
    - Low risk with good prognosis for recovery
    - May be suitable for outpatient management or brief observation
    - Consider 23-hour observation for monitoring and early discharge
    - Evaluate social factors, support systems, and follow-up availability
    - Initiate oral anticoagulation with appropriate monitoring plan
    
    Class III - Intermediate Risk (86-105 points, 3.2-7.1% mortality):
    - Moderate risk requiring careful clinical assessment
    - Generally requires inpatient management with standard monitoring
    - May consider outpatient management in selected patients with excellent support
    - Monitor for clinical deterioration and response to anticoagulation
    - Standard hospitalization with daily clinical assessment
    
    Class IV - High Risk (106-125 points, 4.0-11.4% mortality):
    - High risk requiring inpatient management and close monitoring
    - Consider telemetry monitoring for hemodynamic assessment
    - Evaluate for advanced therapies if clinically appropriate
    - Monitor for signs of right heart failure and hemodynamic instability
    - Consider echocardiography to assess right heart function
    
    Class V - Very High Risk (≥126 points, 10.0-24.5% mortality):
    - Very high risk requiring intensive management and monitoring
    - Consider ICU admission for close hemodynamic monitoring
    - Evaluate for advanced therapies: thrombolysis, catheter-directed therapy, embolectomy
    - Aggressive supportive care with monitoring for shock and respiratory failure
    - Multidisciplinary approach with cardiothoracic surgery and interventional cardiology consultation
    
    Clinical Decision Support:
    
    Outpatient Management Considerations:
    - Classes I and II are generally appropriate for outpatient treatment
    - Ensure adequate social support and ability to seek emergency care
    - Confirm no contraindications to anticoagulation
    - Arrange close follow-up within 24-72 hours
    - Provide clear instructions for symptom monitoring and emergency care
    
    Anticoagulation Strategy:
    - Initiate appropriate anticoagulation based on bleeding risk assessment
    - Consider direct oral anticoagulants (DOACs) for eligible patients
    - Monitor for bleeding complications and therapeutic response
    - Plan duration of anticoagulation based on PE etiology and risk factors
    
    Monitoring and Follow-up:
    - Outpatient: Follow-up within 24-72 hours, then as clinically indicated
    - Inpatient: Daily assessment with monitoring for clinical improvement
    - High-risk: Intensive monitoring with frequent vital sign assessment
    - Long-term: Evaluate for chronic thromboembolic disease and post-PE syndrome
    
    Quality Assurance:
    - Document PESI score and rationale for disposition decision
    - Consider simplified PESI (sPESI) for streamlined assessment
    - Reassess if clinical condition changes significantly
    - Use clinical judgment to supplement score-based recommendations
    
    The PESI score has been extensively validated and provides robust evidence for 
    safe disposition decisions in pulmonary embolism management, particularly for 
    identifying low-risk patients appropriate for outpatient treatment.
    
    Reference: See module docstring for complete citation list.
    """
    
    result: int = Field(
        ...,
        description="PESI score calculated from clinical variables. Score typically ranges from 30-200+ points, with higher scores indicating greater 30-day mortality risk and need for intensive management.",
        example=105
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the PESI score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including risk class, mortality risk, disposition recommendations, monitoring guidance, and treatment considerations based on the calculated PESI score.",
        example="Intermediate risk for mortality (3.2-7.1%). Consider inpatient management with standard monitoring and anticoagulation therapy. Requires careful evaluation for outpatient management eligibility. Monitor for clinical deterioration and response to treatment."
    )
    
    stage: str = Field(
        ...,
        description="PESI risk class with descriptive risk level (Class I-V with Very Low Risk, Low Risk, Intermediate Risk, High Risk, or Very High Risk)",
        example="Class III (Intermediate Risk)"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the 30-day mortality risk level associated with the calculated PESI score",
        example="Intermediate 30-day mortality risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 105,
                "unit": "points",
                "interpretation": "Intermediate risk for mortality (3.2-7.1%). Consider inpatient management with standard monitoring and anticoagulation therapy. Requires careful evaluation for outpatient management eligibility. Monitor for clinical deterioration and response to treatment.",
                "stage": "Class III (Intermediate Risk)",
                "stage_description": "Intermediate 30-day mortality risk"
            }
        }