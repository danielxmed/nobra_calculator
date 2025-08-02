"""
Marburg Heart Score (MHS) Models

Request and response models for Marburg Heart Score calculation.

References (Vancouver style):
1. Bösner S, Haasenritter J, Becker A, Karatolios K, Vaucher P, Gencer B, et al. 
   Ruling out coronary artery disease in primary care: development and validation of 
   a simple prediction rule. CMAJ. 2010 Sep 7;182(12):1295-300. doi: 10.1503/cmaj.100212.
2. Haasenritter J, Bösner S, Vaucher P, Herzig L, Heinzel-Gutenbrunner M, Baum E, et al. 
   Ruling out coronary heart disease in primary care: external validation of a clinical 
   prediction rule. Br J Gen Pract. 2012 Jun;62(599):e415-21. doi: 10.3399/bjgp12X649106.
3. Harskamp RE, Laeven SC, Himmelreich JC, Lucassen WA, van Weert HC. Chest pain in 
   general practice: a systematic review of prediction rules. BMJ Open. 2019 Feb 21;9(2):e027081. 
   doi: 10.1136/bmjopen-2018-027081.

The Marburg Heart Score (MHS) is a validated clinical prediction rule developed to help 
primary care physicians rule out coronary artery disease (CAD) in patients aged 35 years 
and older presenting with chest pain. It uses five equally weighted clinical criteria 
to stratify patients into low-risk (score 0-2) or higher-risk (score ≥3) categories, 
providing a structured approach to reduce unnecessary urgent referrals while maintaining 
diagnostic safety. The score demonstrated a sensitivity of 87.1% and specificity of 80.8% 
for CAD detection in the original validation study.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class MarburgHeartScoreRequest(BaseModel):
    """
    Request model for Marburg Heart Score (MHS)
    
    The Marburg Heart Score evaluates five clinical criteria to assess the risk of 
    coronary artery disease in primary care patients with chest pain:
    
    **Five Clinical Criteria (1 point each):**
    1. **Age/Sex Criteria**: Female ≥65 years OR Male ≥55 years
    2. **Known Vascular Disease**: History of CAD, cerebrovascular disease, or PVD
    3. **Exercise-Related Pain**: Chest pain worsens with physical exercise
    4. **Non-Reproducible Pain**: Pain is NOT reproducible with palpation
    5. **Patient's Assumption**: Patient believes pain is of cardiac origin
    
    **Risk Stratification:**
    - **Low Risk (0-2 points)**: ~3% CAD risk, outpatient evaluation as needed
    - **Higher Risk (≥3 points)**: ~23% CAD risk, consider urgent evaluation
    
    **Clinical Performance:**
    - Sensitivity: 87.1% for detecting CAD
    - Specificity: 80.8% for ruling out CAD
    - Area under the curve: 0.87 (derivation), 0.90 (validation)
    
    **Target Population:**
    - Primary care patients aged ≥35 years with chest pain
    - NOT for emergency department use
    - NOT for patients with obvious alternative diagnoses
    - NOT for positive diagnosis of CAD (risk stratification only)
    
    **Clinical Applications:**
    - Risk stratification of chest pain in primary care
    - Decision support for urgent referral vs. outpatient management
    - Reduction of unnecessary urgent evaluations
    - Enhanced diagnostic safety through structured assessment
    - Support for shared decision-making with patients
    
    **Important Limitations:**
    - Designed as negative predictive tool (rule-out) rather than diagnostic
    - Should supplement, not replace, clinical judgment
    - Not validated in emergency or acute care settings
    - Modest positive predictive value (23%) for higher-risk category
    - Requires consideration of patient presentation and clinical context
    
    References (Vancouver style):
    1. Bösner S, Haasenritter J, Becker A, Karatolios K, Vaucher P, Gencer B, et al. 
       Ruling out coronary artery disease in primary care: development and validation of 
       a simple prediction rule. CMAJ. 2010 Sep 7;182(12):1295-300. doi: 10.1503/cmaj.100212.
    2. Haasenritter J, Bösner S, Vaucher P, Herzig L, Heinzel-Gutenbrunner M, Baum E, et al. 
       Ruling out coronary heart disease in primary care: external validation of a clinical 
       prediction rule. Br J Gen Pract. 2012 Jun;62(599):e415-21. doi: 10.3399/bjgp12X649106.
    """
    
    age_sex_criteria: Literal["yes", "no"] = Field(
        ...,
        description="Age and sex criteria met: Female ≥65 years OR Male ≥55 years. Based on established cardiovascular risk factors where advanced age combined with sex-specific risk patterns increases CAD likelihood",
        example="no"
    )
    
    known_vascular_disease: Literal["yes", "no"] = Field(
        ...,
        description="Known history of coronary artery disease, cerebrovascular disease, or peripheral vascular disease. Previous vascular disease significantly increases risk of additional CAD",
        example="no"
    )
    
    pain_worse_with_exercise: Literal["yes", "no"] = Field(
        ...,
        description="Chest pain worsens with physical exercise or exertion. Exercise-induced chest pain is characteristic of angina pectoris due to increased myocardial oxygen demand",
        example="yes"
    )
    
    pain_not_reproducible_palpation: Literal["yes", "no"] = Field(
        ...,
        description="Chest pain is NOT reproducible with palpation or chest wall pressure. Non-reproducible pain is more likely to be cardiac rather than musculoskeletal in origin",
        example="yes"
    )
    
    patient_assumes_cardiac: Literal["yes", "no"] = Field(
        ...,
        description="Patient assumes or believes the chest pain is of cardiac origin. Patient's clinical intuition about their symptoms has demonstrated diagnostic value in chest pain assessment",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_sex_criteria": "no",
                "known_vascular_disease": "no",
                "pain_worse_with_exercise": "yes",
                "pain_not_reproducible_palpation": "yes",
                "patient_assumes_cardiac": "yes"
            }
        }


class MarburgHeartScoreResponse(BaseModel):
    """
    Response model for Marburg Heart Score (MHS)
    
    The Marburg Heart Score provides risk stratification for coronary artery disease 
    in primary care patients with chest pain:
    
    **Low Risk (0-2 points):**
    - CAD probability: ~3%
    - Management: Outpatient evaluation as needed
    - Interpretation: Highly unlikely to have unstable CAD
    - Follow-up: Routine primary care, cardiovascular risk factor modification
    - Safety: Avoids unnecessary urgent referrals
    
    **Higher Risk (≥3 points):**
    - CAD probability: ~23%
    - Management: Consider urgent evaluation or inpatient admission
    - Evaluation: ECG, cardiac biomarkers, possible stress testing
    - Interpretation: Warrants comprehensive cardiac assessment
    - Note: Modest PPV emphasizes need for thorough evaluation
    
    **Clinical Decision Support:**
    - Structured approach to chest pain risk assessment
    - Evidence-based guidance for referral decisions
    - Enhanced diagnostic safety through systematic evaluation
    - Support for patient communication and shared decision-making
    
    **Quality Assurance:**
    - Validated in multiple primary care populations
    - Consistent performance across different healthcare systems
    - Integration with clinical judgment and patient presentation
    - Regular reassessment based on symptom evolution
    
    **Implementation Considerations:**
    - Use in conjunction with clinical assessment
    - Consider patient preferences and values
    - Account for comorbidities and functional status
    - Maintain awareness of score limitations and context
    
    Reference: Bösner S, et al. CMAJ. 2010;182(12):1295-300.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Comprehensive Marburg Heart Score assessment including individual criteria scores, risk stratification, and detailed clinical guidance",
        example={
            "total_score": 3,
            "criteria_scores": {
                "age_sex": 0,
                "vascular_disease": 0,
                "exercise_pain": 1,
                "not_reproducible": 1,
                "assumes_cardiac": 1
            },
            "criteria_breakdown": {
                "age_sex_criteria": "Age/Sex criteria: Not met",
                "known_vascular_disease": "Known vascular disease: Absent",
                "pain_worse_exercise": "Pain worse with exercise: Yes",
                "pain_not_reproducible": "Pain NOT reproducible: Yes",
                "patient_assumes_cardiac": "Patient assumes cardiac: Yes"
            },
            "assessment_data": {
                "risk_level": "Higher Risk",
                "cad_probability": "~23%",
                "recommendation": "Consider urgent evaluation or inpatient admission",
                "urgency": "Urgent evaluation warranted",
                "positive_criteria": "3/5 criteria positive",
                "score_threshold": "Cut-off ≥3 points for higher risk",
                "sensitivity": "87.1% (original validation)",
                "specificity": "80.8% (original validation)",
                "next_steps": "Clinical judgment should supplement score-based decisions"
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with risk assessment, CAD probability, management recommendations, and clinical guidance",
        example="Marburg Heart Score of 3 indicates higher risk for coronary artery disease with approximately 23% CAD probability. These patients warrant consideration for urgent evaluation or inpatient admission for comprehensive cardiac assessment."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Higher Risk)",
        example="Higher Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category and clinical implications",
        example="Higher risk for coronary artery disease requiring urgent evaluation"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "total_score": 3,
                    "criteria_scores": {
                        "age_sex": 0,
                        "vascular_disease": 0,
                        "exercise_pain": 1,
                        "not_reproducible": 1,
                        "assumes_cardiac": 1
                    },
                    "criteria_breakdown": {
                        "age_sex_criteria": "Age/Sex criteria: Not met",
                        "known_vascular_disease": "Known vascular disease: Absent",
                        "pain_worse_exercise": "Pain worse with exercise: Yes",
                        "pain_not_reproducible": "Pain NOT reproducible: Yes",
                        "patient_assumes_cardiac": "Patient assumes cardiac: Yes"
                    },
                    "assessment_data": {
                        "risk_level": "Higher Risk",
                        "cad_probability": "~23%",
                        "recommendation": "Consider urgent evaluation or inpatient admission",
                        "urgency": "Urgent evaluation warranted",
                        "positive_criteria": "3/5 criteria positive",
                        "score_threshold": "Cut-off ≥3 points for higher risk",
                        "sensitivity": "87.1% (original validation)",
                        "specificity": "80.8% (original validation)",
                        "next_steps": "Clinical judgment should supplement score-based decisions"
                    }
                },
                "unit": "points",
                "interpretation": "Marburg Heart Score of 3 indicates higher risk for coronary artery disease with approximately 23% CAD probability. These patients warrant consideration for urgent evaluation or inpatient admission for comprehensive cardiac assessment. Recommended evaluation includes 12-lead ECG, cardiac biomarkers (troponin), chest X-ray, and consideration for stress testing or coronary imaging as clinically indicated.",
                "stage": "Higher Risk",
                "stage_description": "Higher risk for coronary artery disease requiring urgent evaluation"
            }
        }