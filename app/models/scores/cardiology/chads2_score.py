"""
CHADS₂ Score for Atrial Fibrillation Stroke Risk Models

Request and response models for CHADS₂ Score calculation.

References (Vancouver style):
1. Gage BF, Waterman AD, Shannon W, Boechler M, Rich MW, Radford MJ. 
   Validation of clinical classification schemes for predicting stroke: results 
   from the National Registry of Atrial Fibrillation. JAMA. 2001;285(22):2864-70.
2. Gage BF, van Walraven C, Pearce L, Hart RG, Koudstaal PJ, Boode BS, Petersen P. 
   Selecting patients with atrial fibrillation for anticoagulation: stroke risk 
   stratification in patients taking aspirin. Circulation. 2004;110(16):2287-92.
3. Olesen JB, Lip GY, Hansen ML, Hansen PR, Tolstrup JS, Lindhardsen J, Selmer C, 
   Ahlehoff O, Olsen AM, Gislason GH, Torp-Pedersen C. Validation of risk 
   stratification schemes for predicting stroke and thromboembolism in patients 
   with atrial fibrillation: nationwide cohort study. BMJ. 2011;342:d124.
4. Singer DE, Albers GW, Dalen JE, Fang MC, Go AS, Halperin JL, Lip GY, Manning WJ; 
   American College of Chest Physicians. Antithrombotic therapy in atrial fibrillation: 
   American College of Chest Physicians Evidence-Based Clinical Practice Guidelines 
   (8th Edition). Chest. 2008;133(6 Suppl):546S-592S.

The CHADS₂ score estimates annual stroke risk in patients with atrial fibrillation 
to guide anticoagulation therapy decisions. Developed from the National Registry of 
Atrial Fibrillation in 2001, it uses five clinical risk factors with specific point values.

CHADS₂ Components (Acronym):
- C: Congestive Heart Failure (1 point)
- H: Hypertension (1 point)  
- A: Age ≥75 years (1 point)
- D: Diabetes mellitus (1 point)
- S₂: Stroke/TIA/thromboembolism history (2 points)

Score ranges from 0-6 points with corresponding annual stroke risk:
- Score 0: 1.9% annual risk (Low)
- Score 1: 2.8% annual risk (Low-Intermediate)
- Score 2: 4.0% annual risk (Intermediate) 
- Score 3: 5.9% annual risk (High)
- Score 4: 8.5% annual risk (High)
- Score 5: 12.5% annual risk (Very High)
- Score 6: 18.2% annual risk (Very High)

Clinical Applications:
- Anticoagulation decision-making in atrial fibrillation
- Score ≥2 generally indicates anticoagulation benefit outweighs bleeding risk
- Score 0-1 may require further risk stratification with CHA₂DS₂-VASc
- Simple bedside calculation for rapid risk assessment

Historical Context: While historically important and still referenced, CHADS₂ has 
been largely superseded by the CHA₂DS₂-VASc score which includes additional risk 
factors for more comprehensive stroke risk assessment.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class Chads2ScoreRequest(BaseModel):
    """
    Request model for CHADS₂ Score for Atrial Fibrillation Stroke Risk
    
    The CHADS₂ score uses five clinical risk factors to estimate annual stroke risk 
    in patients with nonvalvular atrial fibrillation:
    
    CHADS₂ Components (each worth points as specified):
    
    C - Congestive Heart Failure (1 point):
    - History of heart failure or left ventricular dysfunction
    - Includes both systolic and diastolic heart failure
    - Based on clinical diagnosis or imaging evidence
    
    H - Hypertension (1 point):
    - History of hypertension or current antihypertensive treatment
    - Blood pressure >140/90 mmHg on repeated measurements
    - Includes controlled hypertension on medication
    
    A - Age ≥75 years (1 point):
    - Advanced age as an independent stroke risk factor
    - Note: CHA₂DS₂-VASc includes age 65-74 for more comprehensive assessment
    
    D - Diabetes Mellitus (1 point):
    - History of diabetes or current antidiabetic treatment
    - Type 1 or Type 2 diabetes mellitus
    - Includes diet-controlled and medication-controlled diabetes
    
    S₂ - Stroke/TIA/Thromboembolism (2 points):
    - Previous ischemic stroke, hemorrhagic stroke, or TIA
    - History of systemic thromboembolism
    - Worth 2 points due to high recurrence risk
    
    Risk Categories and Management:
    - Score 0 (1.9%/year): Consider CHA₂DS₂-VASc or aspirin based on bleeding risk
    - Score 1 (2.8%/year): Consider further stratification or anticoagulation
    - Score ≥2 (4.0-18.2%/year): Strong recommendation for anticoagulation
    
    The score helps balance stroke prevention benefit against bleeding risk in 
    anticoagulation decision-making for atrial fibrillation patients.
    
    References (Vancouver style):
    1. Gage BF, Waterman AD, Shannon W, Boechler M, Rich MW, Radford MJ. 
    Validation of clinical classification schemes for predicting stroke: results 
    from the National Registry of Atrial Fibrillation. JAMA. 2001;285(22):2864-70.
    2. Gage BF, van Walraven C, Pearce L, Hart RG, Koudstaal PJ, Boode BS, Petersen P. 
    Selecting patients with atrial fibrillation for anticoagulation: stroke risk 
    stratification in patients taking aspirin. Circulation. 2004;110(16):2287-92.
    """
    
    congestive_heart_failure: Literal["yes", "no"] = Field(
        ...,
        description="History of congestive heart failure or left ventricular dysfunction. Includes both systolic and diastolic heart failure. Scores 1 point if present",
        example="no"
    )
    
    hypertension: Literal["yes", "no"] = Field(
        ...,
        description="History of hypertension or current antihypertensive treatment. Includes controlled hypertension on medication. Scores 1 point if present",
        example="yes"
    )
    
    age_75_or_older: Literal["yes", "no"] = Field(
        ...,
        description="Patient age 75 years or older. Advanced age as independent stroke risk factor. Scores 1 point if present",
        example="no"
    )
    
    diabetes_mellitus: Literal["yes", "no"] = Field(
        ...,
        description="History of diabetes mellitus or current antidiabetic treatment. Includes Type 1, Type 2, diet-controlled, and medication-controlled diabetes. Scores 1 point if present",
        example="yes"
    )
    
    stroke_tia_thromboembolism: Literal["yes", "no"] = Field(
        ...,
        description="Previous stroke, transient ischemic attack, or systemic thromboembolism. High recurrence risk factor. Scores 2 points if present",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "congestive_heart_failure": "no",
                "hypertension": "yes",
                "age_75_or_older": "no",
                "diabetes_mellitus": "yes",
                "stroke_tia_thromboembolism": "no"
            }
        }


class Chads2ScoreResponse(BaseModel):
    """
    Response model for CHADS₂ Score for Atrial Fibrillation Stroke Risk
    
    The CHADS₂ score provides stroke risk stratification with corresponding annual 
    stroke rates and evidence-based anticoagulation recommendations:
    
    Risk Categories and Annual Stroke Rates:
    
    Low Risk (Score 0):
    - 1.9% annual stroke risk (95% CI: 1.2-3.0%)
    - Consider further risk stratification with CHA₂DS₂-VASc
    - May consider aspirin or observation based on bleeding risk
    
    Low-Intermediate Risk (Score 1):
    - 2.8% annual stroke risk (95% CI: 2.0-3.8%)
    - Consider further stratification or anticoagulation based on bleeding risk
    - Individual decision-making important
    
    Intermediate Risk (Score 2):
    - 4.0% annual stroke risk (95% CI: 3.1-5.1%)
    - Anticoagulation generally recommended unless contraindicated
    - Threshold where benefit typically outweighs bleeding risk
    
    High Risk (Score 3-4):
    - 5.9-8.5% annual stroke risk
    - Strong recommendation for anticoagulation therapy
    - Warfarin or direct oral anticoagulants (DOACs)
    
    Very High Risk (Score 5-6):
    - 12.5-18.2% annual stroke risk
    - Strong recommendation for anticoagulation therapy
    - Careful monitoring and adherence critical
    
    Anticoagulation Options:
    - Warfarin: Traditional option with INR monitoring (target 2.0-3.0)
    - DOACs: Dabigatran, rivaroxaban, apixaban, edoxaban
    - Consider patient preferences, adherence, and bleeding risk
    
    Clinical Context:
    - Developed from National Registry of Atrial Fibrillation (2001)
    - C-statistic ~0.68 for stroke prediction
    - Validated across multiple populations and healthcare systems
    - Evolution: CHA₂DS₂-VASc now preferred for more comprehensive assessment
    
    Reference: Gage BF, et al. JAMA. 2001;285(22):2864-70.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Detailed CHADS₂ assessment including score, stroke risk, and anticoagulation recommendations",
        example={
            "total_score": 2,
            "annual_stroke_risk_percent": 4.0,
            "stroke_risk_range": "3.1-5.1",
            "risk_category": "Intermediate",
            "anticoagulation_recommendation": "Anticoagulation generally recommended",
            "therapy_details": "Warfarin or direct oral anticoagulants (DOACs) unless contraindicated",
            "recommendation_strength": "Strong recommendation",
            "scoring_breakdown": {
                "chads2_components": {
                    "congestive_heart_failure": {"present": False, "points": 0, "description": "History of congestive heart failure or left ventricular dysfunction"},
                    "hypertension": {"present": True, "points": 1, "description": "History of hypertension or current antihypertensive treatment"},
                    "age_75_or_older": {"present": False, "points": 0, "description": "Age 75 years or older"},
                    "diabetes_mellitus": {"present": True, "points": 1, "description": "History of diabetes mellitus or current antidiabetic treatment"},
                    "stroke_tia_thromboembolism": {"present": False, "points": 0, "description": "Previous stroke, TIA, or thromboembolism (worth 2 points)"}
                },
                "clinical_context": {
                    "development": "Developed from National Registry of Atrial Fibrillation (2001)",
                    "validation": "C-statistic ~0.68 for stroke prediction",
                    "evolution": "Largely superseded by CHA₂DS₂-VASc score for more comprehensive assessment",
                    "population": "Validated in multiple healthcare systems and populations"
                },
                "limitations": [
                    "Does not capture all stroke risk factors (vascular disease, gender)",
                    "Age cutoff at 75 misses moderate risk in 65-74 age group",
                    "Better at identifying high-risk than truly low-risk patients",
                    "Current guidelines recommend CHA₂DS₂-VASc for more accurate stratification"
                ]
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
        description="Clinical interpretation with stroke risk assessment and evidence-based anticoagulation recommendations",
        example="CHADS₂ Score 2: Intermediate stroke risk (4.0% per year, 95% CI: 3.1-5.1%). Anticoagulation generally recommended unless contraindicated due to bleeding risk."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Low Risk, Low-Intermediate Risk, Intermediate Risk, High Risk, Very High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Intermediate annual stroke risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "total_score": 2,
                    "annual_stroke_risk_percent": 4.0,
                    "stroke_risk_range": "3.1-5.1",
                    "risk_category": "Intermediate",
                    "anticoagulation_recommendation": "Anticoagulation generally recommended",
                    "therapy_details": "Warfarin or direct oral anticoagulants (DOACs) unless contraindicated",
                    "recommendation_strength": "Strong recommendation",
                    "scoring_breakdown": {
                        "chads2_components": {
                            "congestive_heart_failure": {
                                "present": False,
                                "points": 0,
                                "description": "History of congestive heart failure or left ventricular dysfunction"
                            },
                            "hypertension": {
                                "present": True,
                                "points": 1,
                                "description": "History of hypertension or current antihypertensive treatment"
                            },
                            "age_75_or_older": {
                                "present": False,
                                "points": 0,
                                "description": "Age 75 years or older"
                            },
                            "diabetes_mellitus": {
                                "present": True,
                                "points": 1,
                                "description": "History of diabetes mellitus or current antidiabetic treatment"
                            },
                            "stroke_tia_thromboembolism": {
                                "present": False,
                                "points": 0,
                                "description": "Previous stroke, TIA, or thromboembolism (worth 2 points)"
                            }
                        },
                        "clinical_context": {
                            "development": "Developed from National Registry of Atrial Fibrillation (2001)",
                            "validation": "C-statistic ~0.68 for stroke prediction",
                            "evolution": "Largely superseded by CHA₂DS₂-VASc score for more comprehensive assessment",
                            "population": "Validated in multiple healthcare systems and populations"
                        },
                        "limitations": [
                            "Does not capture all stroke risk factors (vascular disease, gender)",
                            "Age cutoff at 75 misses moderate risk in 65-74 age group",
                            "Better at identifying high-risk than truly low-risk patients",
                            "Current guidelines recommend CHA₂DS₂-VASc for more accurate stratification"
                        ]
                    }
                },
                "unit": "points",
                "interpretation": "CHADS₂ Score 2: Intermediate stroke risk (4.0% per year, 95% CI: 3.1-5.1%). Anticoagulation generally recommended unless contraindicated due to bleeding risk.",
                "stage": "Intermediate Risk",
                "stage_description": "Intermediate annual stroke risk"
            }
        }