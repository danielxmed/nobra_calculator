"""
Emergency Department Assessment of Chest Pain Score (EDACS) Models

Request and response models for EDACS calculation.

References (Vancouver style):
1. Than M, Flaws D, Sanders S, Doust J, Glasziou P, Kline J, et al. Development 
   and validation of the Emergency Department Assessment of Chest pain Score and 
   2 h accelerated diagnostic protocol. Emerg Med Australas. 2014;26(1):34-44. 
   doi: 10.1111/1742-6723.12164.
2. Than M, Cullen L, Aldous S, Parsonage WA, Reid CM, Greenslade J, et al. 
   2-Hour accelerated diagnostic protocol to assess patients with chest pain 
   symptoms using contemporary troponins as the only biomarker: the ADAPT-ADP. 
   J Am Coll Cardiol. 2012;59(23):2091-8. doi: 10.1016/j.jacc.2012.02.035.
3. Cullen L, Mueller C, Parsonage WA, Wildi K, Greenslade JH, Twerenbold R, et al. 
   Validation of high-sensitivity troponin I in a 2-hour diagnostic strategy to 
   assess 30-day outcomes in emergency department patients with possible acute 
   coronary syndrome. J Am Coll Cardiol. 2013;62(14):1242-9. doi: 10.1016/j.jacc.2013.02.078.
4. Pickering JW, Than MP, Cullen L, Aldous S, Ter Avest E, Body R, et al. Rapid 
   Rule-out of Acute Myocardial Infarction With a Single High-Sensitivity Cardiac 
   Troponin T Measurement Below the Limit of Detection: A Collaborative Meta-analysis. 
   Ann Intern Med. 2017;166(10):715-24. doi: 10.7326/M16-2562.

The Emergency Department Assessment of Chest Pain Score (EDACS) is a clinical 
decision tool developed in Australia and New Zealand for risk stratification of 
chest pain patients in the emergency department. It identifies low-risk patients 
who can be safely discharged when combined with no new ischemia on ECG and negative 
troponins at 0 and 2 hours.

The EDACS-Accelerated Diagnostic Protocol (EDACS-ADP) achieves >99% sensitivity 
for 30-day major adverse cardiac events (MACE) when all criteria are met. The tool 
was specifically designed for use in emergency department settings to facilitate 
early discharge of appropriate patients while maintaining safety.

Key clinical applications include risk stratification for chest pain patients, 
decision support for early discharge protocols, and integration with troponin 
testing strategies for optimal patient management.
"""

from pydantic import BaseModel, Field
from typing import Literal


class EmergencyDepartmentAssessmentChestPainEdacsRequest(BaseModel):
    """
    Request model for Emergency Department Assessment of Chest Pain Score (EDACS)
    
    The EDACS score uses seven clinical variables to risk stratify chest pain 
    patients for early discharge from the emergency department:
    
    Age-Based Scoring (Primary Risk Factor):
    - 18-45 years: +2 points
    - 46-50 years: +4 points
    - 51-55 years: +6 points
    - 56-60 years: +8 points
    - 61-65 years: +10 points
    - 66-70 years: +12 points
    - 71-75 years: +14 points
    - 76-80 years: +16 points
    - 81-85 years: +18 points
    - ≥86 years: +20 points
    
    Gender-Based Scoring:
    - Male: +6 points
    - Female: 0 points
    
    Risk Factor Assessment (Ages 18-50 Only):
    Known coronary artery disease OR ≥3 cardiovascular risk factors:
    - Risk factors include: hypertension, dyslipidemia, diabetes mellitus, 
      current smoking, family history of early coronary artery disease
    - Present: +4 points
    - Absent: 0 points
    - Not applicable for patients >50 years
    
    Clinical Symptoms and Signs:
    
    Diaphoresis (Excessive Sweating):
    - Present: +3 points
    - Absent: 0 points
    
    Pain Radiation Pattern:
    - Pain radiating to arm, shoulder, neck, or jaw: +5 points
    - No radiation: 0 points
    
    Pleuritic Chest Pain:
    - Pain that occurs or worsens with inspiration: -4 points (protective)
    - No inspiratory component: 0 points
    
    Chest Wall Tenderness:
    - Pain reproduced by palpation of chest wall: -6 points (protective)
    - No reproducible tenderness: 0 points
    
    EDACS-Accelerated Diagnostic Protocol (EDACS-ADP):
    
    Low-Risk Criteria (All Must Be Present):
    1. EDACS score <16 points
    2. No new ischemic changes on ECG
    3. Troponin negative at 0 hours
    4. Troponin negative at 2 hours
    
    Clinical Application and Safety:
    - EDACS-ADP has >99% sensitivity for 30-day MACE
    - MACE includes death, myocardial infarction, or revascularization
    - External validation in multiple populations confirms safety
    - Most validated in patients presenting within 12 hours of symptom onset
    
    Management Implications:
    - Low-risk patients (EDACS <16 + negative workup): Consider early discharge
    - Higher-risk patients (EDACS ≥16): Require further cardiac evaluation
    - Serial troponin testing is essential for complete protocol
    - Clinical judgment and institutional protocols should guide final decisions
    
    References (Vancouver style):
    1. Than M, Flaws D, Sanders S, Doust J, Glasziou P, Kline J, et al. Development 
    and validation of the Emergency Department Assessment of Chest pain Score and 
    2 h accelerated diagnostic protocol. Emerg Med Australas. 2014;26(1):34-44. 
    doi: 10.1111/1742-6723.12164.
    2. Than M, Cullen L, Aldous S, Parsonage WA, Reid CM, Greenslade J, et al. 
    2-Hour accelerated diagnostic protocol to assess patients with chest pain 
    symptoms using contemporary troponins as the only biomarker: the ADAPT-ADP. 
    J Am Coll Cardiol. 2012;59(23):2091-8. doi: 10.1016/j.jacc.2012.02.035.
    3. Cullen L, Mueller C, Parsonage WA, Wildi K, Greenslade JH, Twerenbold R, et al. 
    Validation of high-sensitivity troponin I in a 2-hour diagnostic strategy to 
    assess 30-day outcomes in emergency department patients with possible acute 
    coronary syndrome. J Am Coll Cardiol. 2013;62(14):1242-9. doi: 10.1016/j.jacc.2013.02.078.
    4. Pickering JW, Than MP, Cullen L, Aldous S, Ter Avest E, Body R, et al. Rapid 
    Rule-out of Acute Myocardial Infarction With a Single High-Sensitivity Cardiac 
    Troponin T Measurement Below the Limit of Detection: A Collaborative Meta-analysis. 
    Ann Intern Med. 2017;166(10):715-24. doi: 10.7326/M16-2562.
    """
    
    age: int = Field(
        ...,
        description="Patient age in years (18-120). Age is the primary risk factor with points assigned by decade",
        ge=18,
        le=120,
        example=55
    )
    
    sex: Literal["Male", "Female"] = Field(
        ...,
        description="Patient sex. Male patients receive +6 points, female patients receive 0 points",
        example="Female"
    )
    
    known_cad_or_risk_factors: Literal["Yes", "No", "Not applicable (age >50)"] = Field(
        ...,
        description="Known coronary artery disease OR ≥3 cardiovascular risk factors (hypertension, dyslipidemia, diabetes, current smoking, family history of early CAD). Applies only to patients aged 18-50 years. +4 points if present",
        example="Not applicable (age >50)"
    )
    
    diaphoresis: Literal["Yes", "No"] = Field(
        ...,
        description="Presence of diaphoresis (excessive sweating) during chest pain episode. +3 points if present",
        example="No"
    )
    
    pain_radiates: Literal["Yes", "No"] = Field(
        ...,
        description="Pain radiates to arm, shoulder, neck, or jaw. Classic pattern of cardiac ischemia. +5 points if present",
        example="Yes"
    )
    
    pain_with_inspiration: Literal["Yes", "No"] = Field(
        ...,
        description="Pain that occurs or worsens with inspiration (pleuritic chest pain). Suggests non-cardiac etiology. -4 points if present (protective factor)",
        example="No"
    )
    
    pain_reproduced_by_palpation: Literal["Yes", "No"] = Field(
        ...,
        description="Chest pain reproduced by palpation of the chest wall. Suggests musculoskeletal cause. -6 points if present (protective factor)",
        example="No"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 55,
                "sex": "Female",
                "known_cad_or_risk_factors": "Not applicable (age >50)",
                "diaphoresis": "No",
                "pain_radiates": "Yes",
                "pain_with_inspiration": "No",
                "pain_reproduced_by_palpation": "No"
            }
        }


class EmergencyDepartmentAssessmentChestPainEdacsResponse(BaseModel):
    """
    Response model for Emergency Department Assessment of Chest Pain Score (EDACS)
    
    The EDACS score ranges from negative values to over 30 points, with a critical 
    threshold at 16 points for risk stratification:
    
    Low Risk (EDACS <16):
    - Suitable for EDACS-Accelerated Diagnostic Protocol (EDACS-ADP)
    - When combined with no new ischemia on ECG and negative troponins at 0 and 2 hours
    - >99% sensitivity for 30-day major adverse cardiac events (MACE)
    - May be considered for early discharge with appropriate follow-up
    
    Higher Risk (EDACS ≥16):
    - Requires further cardiac evaluation and risk stratification
    - Not suitable for accelerated discharge protocols
    - Consider admission or extended observation
    - Serial troponins, stress testing, or coronary imaging as indicated
    
    Clinical Management Guidelines:
    
    For Low-Risk Patients (EDACS <16):
    - Complete EDACS-ADP protocol with ECG and 0/2-hour troponins
    - If all components negative, consider early discharge
    - Provide clear return precautions and follow-up instructions
    - Document rationale for early discharge decision
    - Consider outpatient stress testing if clinically indicated
    
    For Higher-Risk Patients (EDACS ≥16):
    - Pursue standard chest pain evaluation protocols
    - Consider cardiology consultation
    - Admission or extended emergency department observation
    - Serial cardiac biomarkers and monitoring
    - Risk stratification with stress testing or coronary imaging
    
    Implementation Considerations:
    - EDACS is most validated in patients presenting within 12 hours of symptom onset
    - Should be used in conjunction with clinical judgment
    - Institutional protocols may modify implementation
    - Staff training essential for proper application
    - Quality assurance monitoring recommended
    
    Safety and Effectiveness:
    - Negative predictive value approaches 100% when EDACS-ADP criteria met
    - Reduces length of stay and healthcare costs
    - Maintains safety while improving efficiency
    - External validation confirms performance across populations
    - Continuous monitoring of outcomes recommended
    
    Reference: Than M, et al. Emerg Med Australas. 2014;26(1):34-44.
    """
    
    result: int = Field(
        ...,
        description="EDACS score calculated from clinical variables (range: negative values to >30 points)",
        example=11
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on EDACS score",
        example="Low risk for major adverse cardiac events (MACE). When combined with no new ischemia on ECG and negative troponins at 0 and 2 hours, patients may be considered for early discharge."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk or Higher Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="EDACS <16 indicates low risk"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 11,
                "unit": "points",
                "interpretation": "Low risk for major adverse cardiac events (MACE). When combined with no new ischemia on ECG and negative troponins at 0 and 2 hours, patients may be considered for early discharge. The EDACS-Accelerated Diagnostic Protocol (EDACS-ADP) is >99% sensitive for 30-day MACE when all criteria are met. Patients should still receive appropriate follow-up and instruction for return if symptoms worsen.",
                "stage": "Low Risk",
                "stage_description": "EDACS <16 indicates low risk"
            }
        }