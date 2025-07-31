"""
CHA₂DS₂-VA Score for Atrial Fibrillation Stroke Risk Models

Request and response models for CHA₂DS₂-VA Score calculation.

References (Vancouver style):
1. Lip GYH, Keshishian A, Li X, Hamilton M, Masseria C, Gupta K, Mardekian J, Friend K, 
   Nadkarni A, Pan X, Baser O, Deitelzweig S. Effectiveness and Safety of Oral Anticoagulants 
   Among Nonvalvular Atrial Fibrillation Patients. Stroke. 2018;49(12):2933-2944.
2. Hindricks G, Potpara T, Dagres N, et al. 2020 ESC Guidelines for the diagnosis and 
   management of atrial fibrillation developed in collaboration with the European Association 
   for Cardio-Thoracic Surgery (EACTS). Eur Heart J. 2021;42(5):373-498.
3. Romiti GF, Pastori D, Rivera-Caravaca JM, et al. Adherence to the 'Atrial Fibrillation 
   Better Care' pathway in patients with atrial fibrillation: impact on clinical outcomes-a 
   systematic review and meta-analysis of 285,000 patients. Thromb Haemost. 2022;122(3):406-414.

The CHA₂DS₂-VA Score is a simplified version of the CHA₂DS₂-VASc score that excludes 
female sex as a risk factor. Introduced in the 2024 ESC guidelines, it maintains 
comparable discrimination ability while addressing concerns about gender-based scoring 
complexity and inclusivity.

CHA₂DS₂-VA Components:

C - Congestive Heart Failure (1 point):
- History of heart failure or left ventricular dysfunction
- Includes both systolic and diastolic heart failure
- Clinical diagnosis or echocardiographic evidence

H - Hypertension (1 point):
- History of hypertension or current antihypertensive treatment
- Blood pressure ≥140/90 mmHg on repeated measurements
- Includes well-controlled hypertension on medication

A₂ - Age ≥75 years (2 points):
- Advanced age as major stroke risk factor
- Worth 2 points reflecting high impact on stroke risk

D - Diabetes Mellitus (1 point):
- Type 1 or Type 2 diabetes mellitus
- Current antidiabetic treatment or dietary management
- Includes well-controlled diabetes

S₂ - Prior Stroke/TIA/Thromboembolism (2 points):
- Previous ischemic stroke, hemorrhagic stroke, or TIA
- History of arterial thromboembolism
- Worth 2 points due to high recurrence risk

V - Vascular Disease (1 point):
- Myocardial infarction, peripheral artery disease, or aortic plaque
- Complex atherosclerotic disease
- History of coronary, carotid, or peripheral revascularization

A - Age 65-74 years (1 point):
- Moderate age-related stroke risk
- Intermediate risk category between <65 and ≥75 years

Clinical Decision Thresholds:
- Score 0: No anticoagulation recommended (0.5 strokes/100 patient-years)
- Score 1: Clinical judgment required (1.5 strokes/100 patient-years)
- Score ≥2: Oral anticoagulation recommended (2.9-19.5 strokes/100 patient-years)

Rationale for Removing Female Sex:
- Female sex as age-dependent rather than independent risk factor
- Reduced thromboembolic risk in women over time (2007-2018)
- Simplifies clinical practice for healthcare professionals and patients
- Includes non-binary, transgender, and gender-diverse individuals
- Maintains comparable discrimination to CHA₂DS₂-VASc score

Clinical Applications:
- Primary stroke prevention in nonvalvular atrial fibrillation
- Anticoagulation decision-making
- Risk stratification for clinical trials
- Quality improvement initiatives
- Simplified alternative to CHA₂DS₂-VASc scoring
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class Cha2ds2VaScoreRequest(BaseModel):
    """
    Request model for CHA₂DS₂-VA Score for Atrial Fibrillation Stroke Risk
    
    The CHA₂DS₂-VA score uses 6 clinical risk factors to assess annual stroke risk in 
    patients with nonvalvular atrial fibrillation. This simplified version of the 
    CHA₂DS₂-VASc score removes female sex as a risk factor, addressing concerns about 
    gender-based complexity and improving inclusivity.
    
    Age Component (Graduated Risk):
    Age represents the most significant modifiable risk factor with graduated scoring:
    - <65 years: 0 points (baseline risk)
    - 65-74 years: 1 point (moderate age-related risk)
    - ≥75 years: 2 points (high age-related risk)
    
    Clinical Risk Factors:
    
    Congestive Heart Failure (1 point):
    - Clinical syndrome of heart failure regardless of ejection fraction
    - Left ventricular dysfunction documented by echocardiography
    - History of hospitalization for heart failure
    - Current or prior use of heart failure medications
    
    Hypertension (1 point):
    - History of hypertension diagnosed by healthcare provider
    - Blood pressure ≥140/90 mmHg on repeated measurements
    - Current use of antihypertensive medications
    - Includes well-controlled hypertension
    
    Diabetes Mellitus (1 point):
    - Type 1 or Type 2 diabetes mellitus
    - Fasting glucose ≥126 mg/dL or HbA1c ≥6.5%
    - Current use of antidiabetic medications
    - Diet-controlled diabetes qualifies
    
    Prior Stroke/TIA/Thromboembolism (2 points):
    - Previous ischemic or hemorrhagic stroke
    - Transient ischemic attack with neurological symptoms
    - Arterial thromboembolism (excluding pulmonary embolism)
    - Worth 2 points due to very high recurrence risk
    
    Vascular Disease (1 point):
    - Myocardial infarction (current or prior)
    - Peripheral artery disease with symptoms or intervention
    - Aortic plaque or complex atherosclerotic disease
    - History of coronary, carotid, or peripheral revascularization
    
    Clinical Decision Framework:
    
    Score 0 (Very Low Risk):
    - Annual stroke rate: 0.5 per 100 patient-years
    - Recommendation: No anticoagulation
    - Alternative: Consider bleeding risk assessment only
    
    Score 1 (Low-Moderate Risk):
    - Annual stroke rate: 1.5 per 100 patient-years
    - Recommendation: Clinical judgment required
    - Consider: Patient preferences, bleeding risk, comorbidities
    
    Score ≥2 (High Risk):
    - Annual stroke rate: 2.9-19.5 per 100 patient-years
    - Recommendation: Oral anticoagulation recommended
    - Options: Warfarin, DOACs (dabigatran, rivaroxaban, apixaban, edoxaban)
    
    Advantages of CHA₂DS₂-VA vs CHA₂DS₂-VASc:
    - Simplified scoring without gender considerations
    - Inclusive of non-binary and transgender patients
    - Reduced complexity for clinical decision-making
    - Comparable predictive performance
    - Aligned with contemporary understanding of female stroke risk
    
    Clinical Implementation:
    - Use for nonvalvular atrial fibrillation patients
    - Consider bleeding risk assessment (HAS-BLED) alongside stroke risk
    - Reassess periodically as patient conditions change
    - Integrate with shared decision-making processes
    - Document rationale for anticoagulation decisions
    
    References (Vancouver style):
    1. Lip GYH, Keshishian A, Li X, Hamilton M, Masseria C, Gupta K, Mardekian J, Friend K, 
    Nadkarni A, Pan X, Baser O, Deitelzweig S. Effectiveness and Safety of Oral Anticoagulants 
    Among Nonvalvular Atrial Fibrillation Patients. Stroke. 2018;49(12):2933-2944.
    2. Hindricks G, Potpara T, Dagres N, et al. 2020 ESC Guidelines for the diagnosis and 
    management of atrial fibrillation developed in collaboration with the European Association 
    for Cardio-Thoracic Surgery (EACTS). Eur Heart J. 2021;42(5):373-498.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in years. Graduated scoring: <65y (0 pts), 65-74y (1 pt), ≥75y (2 pts)",
        example=68
    )
    
    congestive_heart_failure: Literal["yes", "no"] = Field(
        ...,
        description="Congestive heart failure or left ventricular dysfunction. Clinical syndrome or echocardiographic evidence. Scores 1 point if present",
        example="no"
    )
    
    hypertension: Literal["yes", "no"] = Field(
        ...,
        description="History of hypertension or current antihypertensive treatment. BP ≥140/90 mmHg or on medications. Scores 1 point if present",
        example="yes"
    )
    
    diabetes_mellitus: Literal["yes", "no"] = Field(
        ...,
        description="Type 1 or Type 2 diabetes mellitus. Includes diet-controlled and medication-controlled diabetes. Scores 1 point if present",
        example="no"
    )
    
    stroke_tia_thromboembolism: Literal["yes", "no"] = Field(
        ...,
        description="Prior stroke, TIA, or arterial thromboembolism. High recurrence risk factor. Scores 2 points if present",
        example="no"
    )
    
    vascular_disease: Literal["yes", "no"] = Field(
        ...,
        description="Vascular disease: MI, peripheral artery disease, aortic plaque. Complex atherosclerotic disease. Scores 1 point if present",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 68,
                "congestive_heart_failure": "no",
                "hypertension": "yes",
                "diabetes_mellitus": "no",
                "stroke_tia_thromboembolism": "no",
                "vascular_disease": "no"
            }
        }


class Cha2ds2VaScoreResponse(BaseModel):
    """
    Response model for CHA₂DS₂-VA Score for Atrial Fibrillation Stroke Risk
    
    The CHA₂DS₂-VA score provides stroke risk stratification with evidence-based 
    anticoagulation recommendations. Score ranges from 0-8 points with corresponding 
    annual stroke rates and management guidance.
    
    Risk Stratification and Management:
    
    Very Low Risk (Score 0):
    - Annual stroke rate: 0.5 per 100 patient-years
    - Management: No anticoagulation recommended
    - Rationale: Very low stroke risk does not justify bleeding risks
    - Consider: Bleeding risk assessment, patient education
    
    Low-Moderate Risk (Score 1):
    - Annual stroke rate: 1.5 per 100 patient-years
    - Management: Clinical judgment required
    - Considerations: Patient preferences, bleeding risk, comorbidities
    - Options: Anticoagulation vs observation with monitoring
    
    High Risk (Score ≥2):
    - Annual stroke rate: 2.9-19.5 per 100 patient-years
    - Management: Oral anticoagulation recommended
    - Options: Warfarin (INR 2.0-3.0), DOACs preferred
    - Monitoring: Regular assessment for efficacy and safety
    
    Anticoagulation Options:
    
    Direct Oral Anticoagulants (DOACs) - Preferred:
    - Dabigatran: 150 mg BID (110 mg BID if bleeding risk)
    - Rivaroxaban: 20 mg daily (15 mg if CrCl 30-49)
    - Apixaban: 5 mg BID (2.5 mg BID if ≥2: age ≥80, weight ≤60kg, SCr ≥1.5)
    - Edoxaban: 60 mg daily (30 mg if CrCl 30-50, weight ≤60kg)
    
    Warfarin (Alternative):
    - Target INR 2.0-3.0
    - Requires regular monitoring
    - Drug and food interactions
    - Consider when DOACs contraindicated
    
    Clinical Implementation:
    
    Shared Decision-Making:
    - Discuss stroke risk vs bleeding risk
    - Consider patient values and preferences
    - Address concerns about anticoagulation
    - Provide educational materials
    
    Bleeding Risk Assessment:
    - Use HAS-BLED score alongside CHA₂DS₂-VA
    - Identify modifiable bleeding risk factors
    - Consider drug interactions and comorbidities
    - Balance stroke prevention with bleeding risk
    
    Follow-up and Monitoring:
    - Reassess stroke risk periodically
    - Monitor anticoagulation adherence
    - Screen for bleeding complications
    - Adjust therapy based on changes in condition
    
    Quality Measures:
    - Appropriate anticoagulation for AF (CMS measures)
    - Time in therapeutic range for warfarin
    - Stroke and bleeding event rates
    - Medication adherence metrics
    
    Advantages of CHA₂DS₂-VA Score:
    - Simplified compared to CHA₂DS₂-VASc
    - Gender-inclusive approach
    - Maintains predictive accuracy
    - Reduces clinical complexity
    - Aligns with contemporary stroke risk understanding
    
    Clinical Context:
    - Apply to nonvalvular atrial fibrillation only
    - Consider individual patient factors beyond score
    - Integrate with comprehensive AF management
    - Document decision-making rationale
    - Reassess when clinical status changes
    
    Reference: Hindricks G, et al. Eur Heart J. 2021;42(5):373-498.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Comprehensive CHA₂DS₂-VA assessment including score, stroke risk, and anticoagulation recommendations",
        example={
            "total_score": 2,
            "annual_stroke_risk_percent": 2.9,
            "risk_level": "High",
            "stroke_incidence": "2.9 per 100 patient-years",
            "anticoagulation_recommendation": "Oral Anticoagulation Recommended",
            "recommendation_details": "Oral anticoagulation is recommended to reduce stroke risk unless contraindicated.",
            "recommendation_strength": "Strong recommendation for",
            "clinical_rationale": "High stroke risk justifies anticoagulation therapy benefits over bleeding risks",
            "scoring_breakdown": {
                "component_scores": {
                    "age": {
                        "category": "Age 68 years (65-74)",
                        "points": 1,
                        "description": "Age-based scoring: <65y (0 pts), 65-74y (1 pt), ≥75y (2 pts)"
                    },
                    "congestive_heart_failure": {
                        "present": False,
                        "points": 0,
                        "description": "Congestive heart failure or left ventricular dysfunction"
                    },
                    "hypertension": {
                        "present": True,
                        "points": 1,
                        "description": "History of hypertension or current antihypertensive treatment"
                    },
                    "diabetes_mellitus": {
                        "present": False,
                        "points": 0,
                        "description": "Diabetes mellitus"
                    },
                    "stroke_tia_thromboembolism": {
                        "present": False,
                        "points": 0,
                        "description": "Prior stroke, TIA, or arterial thromboembolism (worth 2 points)"
                    },
                    "vascular_disease": {
                        "present": False,
                        "points": 0,
                        "description": "Vascular disease (MI, peripheral artery disease, aortic plaque)"
                    }
                },
                "score_acronym": {
                    "C": "Congestive heart failure (1 point)",
                    "H": "Hypertension (1 point)",
                    "A2": "Age ≥75 years (2 points)",
                    "D": "Diabetes mellitus (1 point)",
                    "S2": "Prior Stroke/TIA/thromboembolism (2 points)",
                    "V": "Vascular disease (1 point)",
                    "A": "Age 65-74 years (1 point)"
                },
                "clinical_context": {
                    "development": "Simplified version of CHA₂DS₂-VASc removing sex category",
                    "guideline": "Recommended in 2024 ESC guidelines",
                    "rationale": "Female sex as age-dependent rather than independent risk factor",
                    "inclusivity": "Includes non-binary and transgender individuals without gender bias",
                    "performance": "Discrimination ability comparable to CHA₂DS₂-VASc score"
                },
                "score_range": {
                    "minimum": 0,
                    "maximum": 8,
                    "current_score": 2
                }
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
        example="CHA₂DS₂-VA Score 2: High stroke risk (2.9 strokes per 100 patient-years). Oral anticoagulation is recommended to reduce stroke risk unless contraindicated."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Low Risk, Moderate Risk, High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the stroke risk category",
        example="High stroke risk"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": {
                    "total_score": 2,
                    "annual_stroke_risk_percent": 2.9,
                    "risk_level": "High",
                    "stroke_incidence": "2.9 per 100 patient-years",
                    "anticoagulation_recommendation": "Oral Anticoagulation Recommended",
                    "recommendation_details": "Oral anticoagulation is recommended to reduce stroke risk unless contraindicated.",
                    "recommendation_strength": "Strong recommendation for",
                    "clinical_rationale": "High stroke risk justifies anticoagulation therapy benefits over bleeding risks",
                    "scoring_breakdown": {
                        "component_scores": {
                            "age": {
                                "category": "Age 68 years (65-74)",
                                "points": 1,
                                "description": "Age-based scoring: <65y (0 pts), 65-74y (1 pt), ≥75y (2 pts)"
                            },
                            "congestive_heart_failure": {
                                "present": False,
                                "points": 0,
                                "description": "Congestive heart failure or left ventricular dysfunction"
                            },
                            "hypertension": {
                                "present": True,
                                "points": 1,
                                "description": "History of hypertension or current antihypertensive treatment"
                            },
                            "diabetes_mellitus": {
                                "present": False,
                                "points": 0,
                                "description": "Diabetes mellitus"
                            },
                            "stroke_tia_thromboembolism": {
                                "present": False,
                                "points": 0,
                                "description": "Prior stroke, TIA, or arterial thromboembolism (worth 2 points)"
                            },
                            "vascular_disease": {
                                "present": False,
                                "points": 0,
                                "description": "Vascular disease (MI, peripheral artery disease, aortic plaque)"
                            }
                        },
                        "score_acronym": {
                            "C": "Congestive heart failure (1 point)",
                            "H": "Hypertension (1 point)",
                            "A2": "Age ≥75 years (2 points)",
                            "D": "Diabetes mellitus (1 point)",
                            "S2": "Prior Stroke/TIA/thromboembolism (2 points)",
                            "V": "Vascular disease (1 point)",
                            "A": "Age 65-74 years (1 point)"
                        },
                        "clinical_context": {
                            "development": "Simplified version of CHA₂DS₂-VASc removing sex category",
                            "guideline": "Recommended in 2024 ESC guidelines",
                            "rationale": "Female sex as age-dependent rather than independent risk factor",
                            "inclusivity": "Includes non-binary and transgender individuals without gender bias",
                            "performance": "Discrimination ability comparable to CHA₂DS₂-VASc score"
                        },
                        "score_range": {
                            "minimum": 0,
                            "maximum": 8,
                            "current_score": 2
                        }
                    }
                },
                "unit": "points",
                "interpretation": "CHA₂DS₂-VA Score 2: High stroke risk (2.9 strokes per 100 patient-years). Oral anticoagulation is recommended to reduce stroke risk unless contraindicated.",
                "stage": "High Risk",
                "stage_description": "High stroke risk"
            }
        }