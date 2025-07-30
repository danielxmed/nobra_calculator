"""
CHADS-65 (Canadian Society of Cardiology Guideline) Models

Request and response models for CHADS-65 decision algorithm.

References (Vancouver style):
1. Andrade JG, Aguilar M, Atzema C, Bell A, Cairns JA, Cheung CC, et al. 
   The 2020 Canadian Cardiovascular Society/Canadian Heart Rhythm Society 
   Comprehensive Guidelines for the Management of Atrial Fibrillation. 
   Can J Cardiol. 2020 Dec;36(12):1847-1948. doi: 10.1016/j.cjca.2020.09.001.
2. Verma A, Cairns JA, Mitchell LB, Macle L, Stiell IG, Gladstone D, et al. 
   2014 focused update of the Canadian Cardiovascular Society Guidelines for 
   the management of atrial fibrillation. Can J Cardiol. 2014 Oct;30(10):1114-30. 
   doi: 10.1016/j.cjca.2014.08.001.
3. Canadian Agency for Drugs and Technologies in Health (CADTH). CHAD65 and 
   CHA2DS2-VASc Risk Stratification Tools for Patients with Atrial Fibrillation: 
   A Review of Clinical Effectiveness and Guidelines. Ottawa: CADTH; 2019 Mar.

The CHADS-65 is a clinical decision algorithm (not a numerical scoring system) 
developed by the Canadian Cardiovascular Society to guide antithrombotic therapy 
for patients with nonvalvular atrial fibrillation or atrial flutter. It uses age 
as the primary decision point to determine appropriate stroke prevention therapy.

Algorithm Structure (Sequential Decision Tree):

Step 1: Age Assessment
- Age ≥65 years? → YES: Oral Anticoagulation (OAC) → END
- Age ≥65 years? → NO: Proceed to Step 2

Step 2: CHADS₂ Risk Factor Assessment  
- Any CHADS₂ risk factors present?
  - Congestive heart failure
  - Hypertension
  - Diabetes mellitus  
  - Stroke/TIA history
- YES: Oral Anticoagulation (OAC) → END
- NO: Proceed to Step 3

Step 3: Vascular Disease Assessment
- Coronary artery disease OR Peripheral artery disease?
- YES: Antiplatelet therapy (ASA 81mg daily) → END
- NO: No antithrombotic therapy → END

Key Clinical Principles:
- Age ≥65 years alone is sufficient indication for anticoagulation
- Direct oral anticoagulants (DOACs) preferred over warfarin
- Simplifies decision-making compared to complex numerical risk scores
- Annual stroke risk: 2.1% (ages 65-74), 4.4% (ages ≥75)
- Strong Recommendation, High-Quality Evidence (CCS 2020 Guidelines)
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class Chads65Request(BaseModel):
    """
    Request model for CHADS-65 (Canadian Society of Cardiology Guideline)
    
    The CHADS-65 algorithm uses a sequential decision tree approach to determine 
    antithrombotic therapy for nonvalvular atrial fibrillation patients:
    
    Primary Decision Point:
    - Age ≥65 years: Primary threshold for anticoagulation recommendation
      - Based on data showing annual stroke risk of 2.1% (ages 65-74) and 4.4% (≥75)
      - Age alone is sufficient indication for oral anticoagulation
    
    CHADS₂ Risk Factors (for patients <65 years):
    - Congestive Heart Failure: History of heart failure or left ventricular dysfunction
    - Hypertension: History of hypertension or current antihypertensive treatment
    - Diabetes Mellitus: History of diabetes or current antidiabetic treatment  
    - Stroke/TIA History: Previous cerebrovascular events or thromboembolism
    
    Vascular Disease Factors (for low-risk patients <65 years):  
    - Coronary Artery Disease: Including MI, coronary revascularization
    - Peripheral Artery Disease: Including amputation, bypass surgery, angioplasty
    
    Treatment Outcomes:
    - Oral Anticoagulation: Age ≥65 OR any CHADS₂ risk factor present
    - Antiplatelet Therapy: Age <65, no CHADS₂ factors, but vascular disease present
    - No Therapy: Age <65, no CHADS₂ factors, no vascular disease
    
    Clinical Impact: This algorithm represents a paradigm shift emphasizing age-based 
    risk stratification and has been endorsed with Strong Recommendation, High-Quality 
    Evidence in the 2020 Canadian Cardiovascular Society Guidelines.
    
    References (Vancouver style):
    1. Andrade JG, Aguilar M, Atzema C, Bell A, Cairns JA, Cheung CC, et al. 
    The 2020 Canadian Cardiovascular Society/Canadian Heart Rhythm Society 
    Comprehensive Guidelines for the Management of Atrial Fibrillation. 
    Can J Cardiol. 2020 Dec;36(12):1847-1948. doi: 10.1016/j.cjca.2020.09.001.
    2. Verma A, Cairns JA, Mitchell LB, Macle L, Stiell IG, Gladstone D, et al. 
    2014 focused update of the Canadian Cardiovascular Society Guidelines for 
    the management of atrial fibrillation. Can J Cardiol. 2014 Oct;30(10):1114-30. 
    doi: 10.1016/j.cjca.2014.08.001.
    """
    
    age_65_or_older: Literal["yes", "no"] = Field(
        ...,
        description="Patient age 65 years or older. Primary decision point - age ≥65 automatically qualifies for oral anticoagulation based on increased stroke risk",
        example="no"
    )
    
    congestive_heart_failure: Literal["yes", "no"] = Field(
        ...,
        description="History of congestive heart failure or left ventricular dysfunction. CHADS₂ risk factor that qualifies for anticoagulation if age <65",
        example="no"
    )
    
    hypertension: Literal["yes", "no"] = Field(
        ...,
        description="History of hypertension or current antihypertensive treatment. CHADS₂ risk factor that qualifies for anticoagulation if age <65",
        example="yes"
    )
    
    diabetes_mellitus: Literal["yes", "no"] = Field(
        ...,
        description="History of diabetes mellitus or current antidiabetic treatment. CHADS₂ risk factor that qualifies for anticoagulation if age <65",
        example="no"
    )
    
    stroke_tia_history: Literal["yes", "no"] = Field(
        ...,
        description="Previous stroke, transient ischemic attack, or thromboembolism. CHADS₂ risk factor that qualifies for anticoagulation if age <65",
        example="no"
    )
    
    coronary_artery_disease: Literal["yes", "no"] = Field(
        ...,
        description="Coronary artery disease including myocardial infarction or coronary revascularization. Vascular disease factor qualifying for antiplatelet therapy in low-risk patients",
        example="no"
    )
    
    peripheral_artery_disease: Literal["yes", "no"] = Field(
        ...,
        description="Peripheral artery disease including previous amputation, bypass surgery, or angioplasty. Vascular disease factor qualifying for antiplatelet therapy in low-risk patients",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_65_or_older": "no",
                "congestive_heart_failure": "no",
                "hypertension": "yes",
                "diabetes_mellitus": "no",
                "stroke_tia_history": "no",
                "coronary_artery_disease": "no",
                "peripheral_artery_disease": "no"
            }
        }


class Chads65Response(BaseModel):
    """
    Response model for CHADS-65 (Canadian Society of Cardiology Guideline)
    
    The CHADS-65 algorithm provides evidence-based antithrombotic therapy 
    recommendations through a sequential decision tree approach:
    
    Treatment Categories:
    
    Oral Anticoagulation (OAC):
    - Indications: Age ≥65 years OR any CHADS₂ risk factor present
    - Preferred agents: Direct oral anticoagulants (DOACs) over warfarin
    - Monitoring: Regular follow-up for efficacy and bleeding complications
    - Contraindications: Assess bleeding risk, drug interactions, patient preferences
    
    Antiplatelet Therapy:
    - Indications: Age <65, no CHADS₂ factors, but vascular disease present
    - Medication: ASA 81mg daily
    - Monitoring: Annual reassessment and bleeding risk evaluation
    - Contraindications: History of major bleeding, peptic ulcer disease
    
    No Antithrombotic Therapy:
    - Indications: Age <65, no CHADS₂ factors, no vascular disease
    - Monitoring: Annual reassessment as risk factors may change
    - Clinical note: Very low stroke risk based on current assessment
    
    Algorithm Steps and Decision Points:
    
    Step 1: Age ≥65 years assessment
    - If YES → Oral anticoagulation recommended (END)
    - If NO → Proceed to Step 2
    
    Step 2: CHADS₂ risk factor assessment (CHF, HTN, DM, Stroke/TIA)
    - If ANY present → Oral anticoagulation recommended (END)
    - If NONE present → Proceed to Step 3
    
    Step 3: Vascular disease assessment (CAD or PAD)
    - If present → Antiplatelet therapy recommended (END)
    - If absent → No antithrombotic therapy recommended (END)
    
    Clinical Evidence and Guidelines:
    - Endorsed with Strong Recommendation, High-Quality Evidence (CCS 2020)
    - Based on Danish national cohort data and validated CHADS₂ components
    - Designed for emergency departments and primary care settings
    - Emphasizes age as primary, easily determined risk factor
    
    Reference: Andrade JG, et al. Can J Cardiol. 2020;36(12):1847-1948.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Detailed CHADS-65 algorithm result with therapy recommendation and clinical guidance",
        example={
            "therapy_recommendation": "Oral Anticoagulation",
            "decision_step": "Step 2: CHADS₂ Risk Factor Assessment",
            "rationale": "CHADS₂ risk factors present: Hypertension",
            "medication_details": "Direct oral anticoagulants (DOACs) preferred over warfarin",
            "indication": "Stroke prevention in nonvalvular atrial fibrillation",
            "monitoring_requirements": "Regular follow-up for efficacy and bleeding complications",
            "clinical_considerations": "Assess bleeding risk, drug interactions, and patient preferences",
            "algorithm_breakdown": {
                "algorithm_steps": {
                    "step_1_age_assessment": {
                        "question": "Is patient ≥65 years old?",
                        "answer": "No",
                        "result": "Proceed to Step 2"
                    },
                    "step_2_chads2_assessment": {
                        "question": "Any CHADS₂ risk factors present?",
                        "risk_factors": {
                            "congestive_heart_failure": False,
                            "hypertension": True,
                            "diabetes_mellitus": False,
                            "stroke_tia_history": False
                        },
                        "any_present": True,
                        "result": "Proceed to OAC"
                    },
                    "step_3_vascular_assessment": {
                        "question": "Coronary or peripheral artery disease present?",
                        "vascular_diseases": {
                            "coronary_artery_disease": False,
                            "peripheral_artery_disease": False
                        },
                        "any_present": False,
                        "result": "No therapy"
                    }
                },
                "final_decision": {
                    "decision_step": "Step 2: CHADS₂ Risk Factor Assessment",
                    "therapy_recommendation": "Oral Anticoagulation",
                    "rationale": "CHADS₂ risk factors present: Hypertension"
                },
                "clinical_context": {
                    "algorithm_type": "Sequential decision tree (not numerical scoring)",
                    "primary_endpoint": "Stroke prevention in nonvalvular atrial fibrillation",
                    "evidence_level": "Strong Recommendation, High-Quality Evidence (CCS 2020)",
                    "key_principle": "Age ≥65 years alone is sufficient for anticoagulation"
                }
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the algorithm",
        example="algorithm"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with algorithm step and evidence-based therapy recommendation",
        example="CHADS-65 Algorithm - Step 2: CHADS₂ risk factors present (Hypertension). Oral anticoagulation recommended despite age <65 years. These risk factors significantly increase stroke risk and warrant anticoagulation therapy."
    )
    
    stage: str = Field(
        ...,
        description="Therapy recommendation category (Oral Anticoagulation, Antiplatelet Therapy, No Antithrombotic Therapy)",
        example="Oral Anticoagulation"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the therapy indication",
        example="Age ≥65 or CHADS₂ risk factors present"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "therapy_recommendation": "Oral Anticoagulation",
                    "decision_step": "Step 2: CHADS₂ Risk Factor Assessment",
                    "rationale": "CHADS₂ risk factors present: Hypertension",
                    "medication_details": "Direct oral anticoagulants (DOACs) preferred over warfarin",
                    "indication": "Stroke prevention in nonvalvular atrial fibrillation",
                    "monitoring_requirements": "Regular follow-up for efficacy and bleeding complications",
                    "clinical_considerations": "Assess bleeding risk, drug interactions, and patient preferences",
                    "algorithm_breakdown": {
                        "algorithm_steps": {
                            "step_1_age_assessment": {
                                "question": "Is patient ≥65 years old?",
                                "answer": "No",
                                "result": "Proceed to Step 2"
                            },
                            "step_2_chads2_assessment": {
                                "question": "Any CHADS₂ risk factors present?",
                                "risk_factors": {
                                    "congestive_heart_failure": False,
                                    "hypertension": True,
                                    "diabetes_mellitus": False,
                                    "stroke_tia_history": False
                                },
                                "any_present": True,
                                "result": "Proceed to OAC"
                            },
                            "step_3_vascular_assessment": {
                                "question": "Coronary or peripheral artery disease present?",
                                "vascular_diseases": {
                                    "coronary_artery_disease": False,
                                    "peripheral_artery_disease": False
                                },
                                "any_present": False,
                                "result": "No therapy"
                            }
                        },
                        "final_decision": {
                            "decision_step": "Step 2: CHADS₂ Risk Factor Assessment",
                            "therapy_recommendation": "Oral Anticoagulation",
                            "rationale": "CHADS₂ risk factors present: Hypertension"
                        },
                        "clinical_context": {
                            "algorithm_type": "Sequential decision tree (not numerical scoring)",
                            "primary_endpoint": "Stroke prevention in nonvalvular atrial fibrillation",
                            "evidence_level": "Strong Recommendation, High-Quality Evidence (CCS 2020)",
                            "key_principle": "Age ≥65 years alone is sufficient for anticoagulation"
                        }
                    }
                },
                "unit": "algorithm",
                "interpretation": "CHADS-65 Algorithm - Step 2: CHADS₂ risk factors present (Hypertension). Oral anticoagulation recommended despite age <65 years. These risk factors significantly increase stroke risk and warrant anticoagulation therapy.",
                "stage": "Oral Anticoagulation",
                "stage_description": "Age ≥65 or CHADS₂ risk factors present"
            }
        }