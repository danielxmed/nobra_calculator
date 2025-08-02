"""
Modified Sequential Organ Failure Assessment (mSOFA) Score Models

Request and response models for mSOFA assessment of ICU mortality risk.

References (Vancouver style):
1. Grissom CK, Brown SM, Kuttler KG, Boltax JP, Jones J, Jephson AR, et al. A modified 
   sequential organ failure assessment score for critical care triage. Disaster Med Public 
   Health Prep. 2010;4(4):277-84. doi: 10.1001/dmp.2010.40.
2. Vahedian-Azimi A, Keramatinia AA, Bashar FR, Hajiesmaeili MR, Shojaei S, Hatamian S, 
   et al. Comparison of proposed modified and original sequential organ failure assessment 
   scores in predicting ICU mortality: a prospective, observational, follow-up study. 
   Turk J Anaesthesiol Reanim. 2017;45(1):16-22. doi: 10.5152/TJAR.2017.93798.
3. Rahmatinejad Z, Reihani H, Tohidinezhad F, Rahmatinejad F, Pourmand A, Abu-Hanna A, 
   et al. Prognostic utilization of models based on the SOFA score and red cell distribution 
   width in intensive care unit patients. Am J Emerg Med. 2018;36(5):775-781. doi: 10.1016/j.ajem.2017.10.011.

The Modified Sequential Organ Failure Assessment (mSOFA) Score predicts ICU mortality 
using mostly clinical variables and fewer laboratory tests compared to the original SOFA 
Score. It was designed for resource-constrained critical care environments during disasters 
or pandemics while maintaining similar predictive accuracy.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ModifiedSofaRequest(BaseModel):
    """
    Request model for Modified Sequential Organ Failure Assessment (mSOFA) Score
    
    The mSOFA Score evaluates five organ systems to predict ICU mortality with similar 
    accuracy to the original SOFA score while requiring fewer laboratory parameters:
    
    **Organ System Assessment:**
    
    **1. Respiratory System (SpO₂/FiO₂ Ratio):**
    - Assesses oxygenation using pulse oximetry and inspired oxygen fraction
    - Non-invasive alternative to PaO₂/FiO₂ ratio used in original SOFA
    - Scoring: >400 (0 pts), 315-400 (1 pt), 235-314 (2 pts), 150-234 (3 pts), ≤150 (4 pts)
    - Clinical significance: Lower ratios indicate more severe respiratory dysfunction
    - Important for patients on supplemental oxygen or mechanical ventilation
    
    **2. Liver System (Scleral Icterus):**
    - Simplified assessment using clinical examination findings
    - Replaces bilirubin measurement required in original SOFA
    - Scoring: Absent (0 pts), Present (3 pts)
    - Clinical assessment: Look for yellowing of sclera or jaundice of skin/mucous membranes
    - Resource-efficient alternative to laboratory hepatic function assessment
    
    **3. Cardiovascular System (Mean Arterial Pressure + Vasopressors):**
    - Assesses circulatory function and need for vasopressor support
    - Combines blood pressure measurement with medication requirements
    - MAP ≥70 mmHg: 0 points (normal perfusion pressure)
    - MAP <70 mmHg: 1 point (hypotension without vasopressor support)
    - Low-dose vasopressors: 2 points (dopamine ≤5 μg/kg/min or dobutamine any dose)
    - Moderate-dose vasopressors: 3 points (dopamine 5.1-15 μg/kg/min or norepinephrine ≤0.1 μg/kg/min)
    - High-dose vasopressors: 4 points (dopamine >15 μg/kg/min or norepinephrine >0.1 μg/kg/min or epinephrine >0.1 μg/kg/min)
    
    **4. Central Nervous System (Glasgow Coma Scale):**
    - Standard neurological assessment tool
    - Identical to original SOFA scoring system
    - Scoring: GCS 15 (0 pts), 13-14 (1 pt), 10-12 (2 pts), 6-9 (3 pts), <6 (4 pts)
    - Assesses consciousness level and neurological function
    - Important prognostic indicator in critically ill patients
    
    **5. Renal System (Serum Creatinine):**
    - Laboratory assessment of kidney function
    - Identical to original SOFA scoring system
    - Scoring: <1.2 mg/dL (0 pts), 1.2-1.9 (1 pt), 2.0-3.4 (2 pts), 3.5-4.9 (3 pts), ≥5.0 (4 pts)
    - Important marker of acute kidney injury in critical illness
    - Consider baseline kidney function when interpreting values
    
    **Clinical Applications:**
    
    **Resource-Constrained Settings:**
    - Reduces laboratory requirements compared to original SOFA
    - Maintains similar predictive accuracy (AUC 0.84 vs 0.83 for SOFA)
    - Particularly useful during disasters, pandemics, or in resource-limited facilities
    - Enables triage decisions when laboratory capacity is overwhelmed
    
    **ICU Mortality Prediction:**
    - Day 1 mSOFA scores perform equally well as original SOFA
    - Threshold of 9 provides 85.6% sensitivity and 74.6% specificity
    - Validated across multiple critical care populations
    - Useful for clinical decision-making and family communication
    
    **Triage Applications:**
    - Can guide resource allocation during mass casualty events
    - Helps identify patients most likely to benefit from intensive care
    - Supports objective decision-making in resource allocation
    - Consider in conjunction with other clinical factors and ethical guidelines
    
    **Limitations and Considerations:**
    - Should not be used as sole criterion for withholding care
    - Many patients with high scores may still survive with appropriate treatment
    - Consider trajectory of illness and response to treatment
    - Supplement with clinical judgment and individual patient factors
    
    **Implementation Guidelines:**
    - Assess all parameters within same time frame (preferably within 24 hours of ICU admission)
    - Use worst values during assessment period
    - Consider pre-existing conditions when interpreting scores
    - Reassess periodically to monitor clinical trajectory
    
    References (Vancouver style):
    1. Grissom CK, Brown SM, Kuttler KG, et al. A modified sequential organ failure 
       assessment score for critical care triage. Disaster Med Public Health Prep. 
       2010;4(4):277-84.
    2. Vahedian-Azimi A, Keramatinia AA, Bashar FR, et al. Comparison of proposed 
       modified and original sequential organ failure assessment scores in predicting 
       ICU mortality: a prospective, observational, follow-up study. Turk J Anaesthesiol 
       Reanim. 2017;45(1):16-22.
    """
    
    spo2_fio2_ratio: int = Field(
        ...,
        ge=50,
        le=500,
        description="SpO₂/FiO₂ ratio for respiratory assessment. Calculate by dividing oxygen saturation (SpO₂) by fraction of inspired oxygen (FiO₂). For room air, FiO₂ = 0.21. Higher ratios indicate better oxygenation.",
        example=280
    )
    
    scleral_icterus: Literal["absent", "present"] = Field(
        ...,
        description="Presence of scleral icterus or jaundice on clinical examination. Look for yellowing of the sclera (whites of eyes) or jaundice of skin and mucous membranes. This replaces bilirubin measurement from original SOFA.",
        example="absent"
    )
    
    mean_arterial_pressure: int = Field(
        ...,
        ge=30,
        le=200,
        description="Mean arterial pressure in mmHg. Can be measured directly via arterial line or calculated as (systolic + 2×diastolic)/3. Normal range is typically 70-100 mmHg. Values <70 mmHg suggest hypotension.",
        example=75
    )
    
    vasopressor_use: Literal["none", "low_dose", "moderate_dose", "high_dose"] = Field(
        ...,
        description="Level of vasopressor support required. None: no vasopressors. Low-dose: dopamine ≤5 μg/kg/min or dobutamine any dose. Moderate-dose: dopamine 5.1-15 μg/kg/min or norepinephrine ≤0.1 μg/kg/min. High-dose: dopamine >15 μg/kg/min, norepinephrine >0.1 μg/kg/min, or epinephrine >0.1 μg/kg/min.",
        example="none"
    )
    
    glasgow_coma_scale: int = Field(
        ...,
        ge=3,
        le=15,
        description="Glasgow Coma Scale score (3-15). Sum of eye opening (1-4), verbal response (1-5), and motor response (1-6). Normal is 15. Lower scores indicate more severe neurological dysfunction. Score of 8 or less typically indicates need for airway protection.",
        example=13
    )
    
    creatinine: float = Field(
        ...,
        ge=0.1,
        le=10.0,
        description="Serum creatinine level in mg/dL. Normal range varies by age, sex, and muscle mass but typically 0.6-1.2 mg/dL. Elevated levels indicate kidney dysfunction. Consider baseline values when interpreting acute changes.",
        example=1.1
    )
    
    class Config:
        schema_extra = {
            "example": {
                "spo2_fio2_ratio": 280,
                "scleral_icterus": "absent",
                "mean_arterial_pressure": 75,
                "vasopressor_use": "none",
                "glasgow_coma_scale": 13,
                "creatinine": 1.1
            }
        }


class ModifiedSofaResponse(BaseModel):
    """
    Response model for Modified Sequential Organ Failure Assessment (mSOFA) Score
    
    The mSOFA score ranges from 0-20 points and provides three risk stratification categories 
    for ICU mortality prediction:
    
    **Risk Stratification Categories:**
    
    **Low Risk (Score 0-7): 4% 30-day Mortality**
    - Represents minimal to mild organ dysfunction
    - Good prognosis with standard ICU supportive care
    - Low likelihood of requiring advanced life support interventions
    - Appropriate for routine ICU monitoring and management
    - Consider for step-down to intermediate care when clinically stable
    
    **Moderate Risk (Score 8-11): 31% 30-day Mortality**
    - Indicates moderate multi-organ dysfunction
    - Requires intensive monitoring and potentially aggressive interventions
    - Higher likelihood of complications and need for organ support
    - Consider early goals of care discussions and family communication
    - May benefit from multidisciplinary team involvement
    
    **High Risk (Score >11): 58% 30-day Mortality**
    - Severe multi-organ dysfunction with poor prognosis
    - Requires maximum intensive care support
    - High likelihood of requiring multiple organ support measures
    - Important to discuss prognosis and goals of care with patient/family
    - Consider palliative care consultation and limitation of care discussions
    
    **Clinical Utility and Validation:**
    
    **Predictive Performance:**
    - Area under ROC curve (AUC) of 0.84 for mortality prediction
    - Comparable to original SOFA score (AUC 0.83) with fewer lab requirements
    - Threshold of 9 provides 85.6% sensitivity and 74.6% specificity
    - Validated across multiple critical care populations and settings
    
    **Resource Efficiency:**
    - Requires only one laboratory test (creatinine) vs four in original SOFA
    - Uses clinical examination (scleral icterus) instead of bilirubin measurement
    - Maintains pulse oximetry-based respiratory assessment
    - Suitable for resource-constrained environments and disaster settings
    
    **Clinical Decision Support:**
    - Guides intensity of monitoring and intervention
    - Supports objective communication with families about prognosis
    - Assists with resource allocation decisions during capacity constraints
    - Helps identify patients who may benefit from palliative care consultation
    
    **Implementation Considerations:**
    - Should be used as part of comprehensive clinical assessment
    - Consider patient trajectory and response to treatment over time
    - Not intended as sole criterion for limiting or withdrawing care
    - Supplement with clinical judgment and individual patient factors
    
    **Quality Improvement Applications:**
    - Benchmark ICU performance and outcomes
    - Risk-adjust mortality statistics for quality reporting
    - Identify opportunities for early intervention
    - Support standardized ICU assessment protocols
    
    **Research and Validation:**
    - Extensively validated in diverse ICU populations
    - Shown to be non-inferior to original SOFA for mortality prediction
    - Particularly validated in sepsis patients and during resource constraints
    - Ongoing research in pandemic and disaster medicine applications
    
    Reference: Grissom CK, et al. Disaster Med Public Health Prep. 2010;4(4):277-84.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=20,
        description="mSOFA score ranging from 0-20 points indicating severity of multi-organ dysfunction",
        example=5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with mortality risk assessment and management recommendations based on mSOFA score category",
        example="mSOFA Score 5: Low mortality risk. The patient has a 4% risk of 30-day mortality in the ICU setting. This represents good prognosis with relatively mild organ dysfunction. Continue standard ICU care with routine monitoring."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the mortality risk level",
        example="4% 30-day mortality"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5,
                "unit": "points",
                "interpretation": "mSOFA Score 5: Low mortality risk. The patient has a 4% risk of 30-day mortality in the ICU setting. This represents good prognosis with relatively mild organ dysfunction. Continue standard ICU care with routine monitoring.",
                "stage": "Low Risk",
                "stage_description": "4% 30-day mortality"
            }
        }