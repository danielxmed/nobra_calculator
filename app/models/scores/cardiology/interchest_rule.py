"""
INTERCHEST Clinical Prediction Rule Models

Request and response models for INTERCHEST Clinical Prediction Rule calculation.

References (Vancouver style):
1. Aerts M, Minalu G, Bösner S, et al. Pooled individual patient data from five countries 
   were used to derive a multi-variable clinical prediction rule for the diagnosis of 
   coronary artery disease in primary care. J Clin Epidemiol. 2017 Jan;81:120-129. 
   doi: 10.1016/j.jclinepi.2016.09.011.
2. Bösner S, Haasenritter J, Becker A, et al. Ruling out coronary artery disease in 
   primary care: development and validation of a simple prediction rule. CMAJ. 2010 
   Sep 7;182(12):1295-300. doi: 10.1503/cmaj.100212.
3. Cayley WE Jr. Chest pain--tools to improve your in-office evaluation. J Fam Pract. 
   2014 May;63(5):246-51.

The INTERCHEST Clinical Prediction Rule for Chest Pain in Primary Care rules out 
coronary artery disease (CAD) in primary care patients 30 years and older presenting 
with chest pain. This clinical prediction rule identifies patients with very low 
likelihood of chest pain due to unstable CAD, allowing for safe discharge without 
urgent evaluation. The rule uses 6 clinical variables with scores ranging from -1 
to +5, where scores ≤1 indicate low CAD risk (2.1% probability, 98% NPV).
"""

from pydantic import BaseModel, Field
from typing import Literal


class InterchestRuleRequest(BaseModel):
    """
    Request model for INTERCHEST Clinical Prediction Rule calculation
    
    Assesses CAD risk in primary care patients ≥30 years with chest pain using 6 clinical variables:
    
    Scoring System (Range: -1 to +5 points):
    - History of CAD: Previous MI, revascularization, or known CAD (+1 point if yes)
    - Age/Gender risk: Female ≥65 or Male ≥55 years (+1 point if yes)
    - Effort-related pain: Chest pain related to physical exertion (+1 point if yes)
    - Pain reproducible by palpation: Chest wall tenderness (-1 point if yes - protective)
    - Physician suspected serious: Clinical suspicion of serious condition (+1 point if yes)
    - Pressure sensation: Chest discomfort feels like pressure/squeezing (+1 point if yes)
    
    Risk Interpretation:
    - Score ≤1: Low risk (2.1% CAD probability, 98% NPV) - safe discharge
    - Score ≥2: Higher risk (43% CAD probability) - requires further evaluation
    
    Important Limitations:
    - Only for primary care settings (NOT emergency department use)
    - Patients must be ≥30 years old
    - Not for positive diagnosis of CAD - only negative screening tool
    - Should not be used if obvious cause of chest pain or clear cardiac findings
    
    References (Vancouver style):
    1. Aerts M, Minalu G, Bösner S, et al. Pooled individual patient data from five countries 
       were used to derive a multi-variable clinical prediction rule for the diagnosis of 
       coronary artery disease in primary care. J Clin Epidemiol. 2017 Jan;81:120-129.
    2. Bösner S, Haasenritter J, Becker A, et al. Ruling out coronary artery disease in 
       primary care: development and validation of a simple prediction rule. CMAJ. 2010 
       Sep 7;182(12):1295-300.
    """
    
    history_of_cad: Literal["no", "yes"] = Field(
        ...,
        description="Previous history of coronary artery disease including myocardial infarction, coronary revascularization (PCI/CABG), or previously diagnosed CAD. Scores: No (0), Yes (+1)",
        example="no"
    )
    
    age_gender_risk: Literal["no", "yes"] = Field(
        ...,
        description="Age and gender risk factor: Female ≥65 years OR Male ≥55 years. This reflects higher CAD risk in older patients with gender-specific thresholds. Scores: No (0), Yes (+1)",
        example="yes"
    )
    
    effort_related_pain: Literal["no", "yes"] = Field(
        ...,
        description="Chest pain is related to physical effort or exertion. Exertional chest pain increases likelihood of CAD as it suggests demand-supply mismatch. Scores: No (0), Yes (+1)",
        example="yes"
    )
    
    pain_reproducible_palpation: Literal["no", "yes"] = Field(
        ...,
        description="Pain is reproducible by chest wall palpation. This suggests musculoskeletal etiology and decreases likelihood of CAD. Scores: No (0), Yes (-1 - protective factor)",
        example="no"
    )
    
    physician_suspected_serious: Literal["no", "yes"] = Field(
        ...,
        description="Physician initially suspected a serious condition based on clinical presentation. This incorporates clinical gestalt and overall assessment. Scores: No (0), Yes (+1)",
        example="no"
    )
    
    pressure_sensation: Literal["no", "yes"] = Field(
        ...,
        description="Chest discomfort feels like pressure, squeezing, or tightness. This describes typical anginal chest pain quality associated with CAD. Scores: No (0), Yes (+1)",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "history_of_cad": "no",
                "age_gender_risk": "yes",
                "effort_related_pain": "yes",
                "pain_reproducible_palpation": "no",
                "physician_suspected_serious": "no",
                "pressure_sensation": "yes"
            }
        }


class InterchestRuleResponse(BaseModel):
    """
    Response model for INTERCHEST Clinical Prediction Rule calculation
    
    Returns the INTERCHEST score with CAD risk stratification:
    - Low Risk (≤1 points): 2.1% CAD probability, 98% NPV - safe discharge
    - Higher Risk (2-5 points): 43% CAD probability - requires evaluation
    
    The INTERCHEST rule helps primary care physicians identify patients at very low 
    risk for unstable CAD who can be safely managed without urgent cardiac evaluation. 
    This reduces unnecessary testing and healthcare costs while maintaining safety. 
    The rule has good diagnostic performance (AUC 0.84) and better predictive 
    properties than the Marburg Heart Score.
    
    Clinical Application:
    - Use only in primary care settings for patients ≥30 years
    - Not for emergency department or acute care use
    - Not for positive diagnosis - only negative screening
    - Consider ECG and basic workup before applying rule
    
    Reference: Aerts M, et al. J Clin Epidemiol. 2017;81:120-129.
    """
    
    result: int = Field(
        ...,
        description="INTERCHEST score calculated from 6 clinical variables (range -1 to +5 points)",
        example=3,
        ge=-1,
        le=5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the INTERCHEST score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on CAD risk category",
        example="Cannot rule out unstable CAD (43% probability). Requires further urgent evaluation with ECG, cardiac biomarkers, and consideration for stress testing or cardiology consultation."
    )
    
    stage: str = Field(
        ...,
        description="CAD risk category (Low Risk, Higher Risk)",
        example="Higher Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category with score range",
        example="Score 3 points (2-5 points)"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "Cannot rule out unstable CAD (43% probability). Requires further urgent evaluation with ECG, cardiac biomarkers, and consideration for stress testing or cardiology consultation.",
                "stage": "Higher Risk",
                "stage_description": "Score 3 points (2-5 points)"
            }
        }