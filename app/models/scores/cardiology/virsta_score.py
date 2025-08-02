"""
VIRSTA Score for Infective Endocarditis Risk Assessment Models

Request and response models for VIRSTA Score calculation.

References (Vancouver style):
1. Sunnerhagen T, Törnell A, Vikbrant M, et al. VIRSTA score: prediction of infective 
   endocarditis and mortality in Staphylococcus aureus bacteremia; a cohort study. 
   Clin Microbiol Infect. 2019;25(4):480-486. doi: 10.1016/j.cmi.2018.06.021
2. Palraj BR, Baddour LM, Hess EP, et al. Predicting risk of endocarditis using a 
   clinical tool (PREDICT): scoring system to guide use of echocardiography in the 
   setting of Staphylococcus aureus bacteremia. Clin Infect Dis. 2015;61(1):18-28. 
   doi: 10.1093/cid/civ235
3. Bouza E, Kestler M, Beca T, et al. The NOVA score: a proposal to reduce the need 
   for transesophageal echocardiography in patients with enterococcal bacteremia. 
   Clin Infect Dis. 2015;60(4):528-535. doi: 10.1093/cid/ciu872

The VIRSTA Score is a clinical decision tool used to risk-stratify suspected infective 
endocarditis cases before obtaining echocardiography. This score helps identify patients 
at very low risk for infective endocarditis who may not require immediate echocardiographic 
evaluation, thereby reducing unnecessary testing and healthcare costs while maintaining 
diagnostic safety.

Scoring System:
- Valve disease or prosthetic valve: 5 points
- Injection drug use: 5 points  
- Vascular phenomena: 4 points
- Immunologic phenomena: 3 points
- Systemic emboli: 3 points
- Temperature >38°C: 2 points
- Age >60 years: 2 points
- WBC >11,000/μL: 1 point
- Central venous catheter: 1 point
- Staphylococcus aureus bacteremia: 1 point

Clinical interpretation:
- Score ≤1: Very low risk (NPV >99%), echocardiography may be deferred
- Score ≥2: Higher risk, echocardiography recommended

Originally developed and validated in patients with Staphylococcus aureus bacteremia,
with excellent discrimination ability (AUC 0.87-0.89) for predicting infective endocarditis.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict


class VirstaScoreRequest(BaseModel):
    """
    Request model for VIRSTA Score for Infective Endocarditis Risk Assessment
    
    The VIRSTA Score uses 10 clinical criteria to assess the probability of infective 
    endocarditis in patients with suspected disease, particularly those with bacteremia.
    Each criterion is assessed as present ("yes") or absent ("no") and contributes 
    different point values to the total score.
    
    High-value criteria (≥3 points):
    1. Valve disease or prosthetic valve (5 points) - Including rheumatic heart disease,
       congenital valve disease, degenerative valve disease, or any prosthetic valve
    2. Injection drug use (5 points) - Current or past history of intravenous drug use
    3. Vascular phenomena (4 points) - Major arterial emboli, septic pulmonary infarcts,
       mycotic aneurysm, intracranial hemorrhage, conjunctival hemorrhages, Janeway lesions
    4. Immunologic phenomena (3 points) - Glomerulonephritis, Osler nodes, Roth spots,
       positive rheumatoid factor
    5. Systemic emboli (3 points) - Evidence of arterial embolic events
    
    Medium-value criteria (2 points):
    6. Temperature >38°C (2 points) - Fever documented above 38°C (100.4°F)
    7. Age >60 years (2 points) - Patient age greater than 60 years
    
    Low-value criteria (1 point):
    8. WBC >11,000/μL (1 point) - Leukocytosis above 11.0 × 10⁹/L
    9. Central venous catheter (1 point) - Presence of central line or intravascular device
    10. Staphylococcus aureus bacteremia (1 point) - MSSA or MRSA in blood cultures
    
    Clinical context:
    - Best validated in patients with confirmed bacteremia
    - Particularly useful in emergency department and inpatient settings
    - Score ≤1 has negative predictive value >99% for ruling out endocarditis
    - Should be used alongside clinical judgment, not as sole determinant
    - May help reduce unnecessary echocardiographic studies
    
    References (Vancouver style):
    1. Sunnerhagen T, Törnell A, Vikbrant M, et al. VIRSTA score: prediction of infective 
    endocarditis and mortality in Staphylococcus aureus bacteremia; a cohort study. 
    Clin Microbiol Infect. 2019;25(4):480-486. doi: 10.1016/j.cmi.2018.06.021
    2. Palraj BR, Baddour LM, Hess EP, et al. Predicting risk of endocarditis using a 
    clinical tool (PREDICT): scoring system to guide use of echocardiography in the 
    setting of Staphylococcus aureus bacteremia. Clin Infect Dis. 2015;61(1):18-28.
    """
    
    valve_disease_or_prosthetic_valve: Literal["yes", "no"] = Field(
        ...,
        description="Known valve disease (rheumatic, congenital, degenerative) or prosthetic valve. Scores 5 points if present",
        example="no"
    )
    
    injection_drug_use: Literal["yes", "no"] = Field(
        ...,
        description="History of injection drug use (current or past intravenous drug use). Scores 5 points if present",
        example="no"
    )
    
    vascular_phenomena: Literal["yes", "no"] = Field(
        ...,
        description="Vascular phenomena: major arterial emboli, septic pulmonary infarcts, mycotic aneurysm, intracranial hemorrhage, conjunctival hemorrhages, or Janeway lesions. Scores 4 points if present",
        example="no"
    )
    
    immunologic_phenomena: Literal["yes", "no"] = Field(
        ...,
        description="Immunologic phenomena: glomerulonephritis, Osler nodes, Roth spots, or positive rheumatoid factor. Scores 3 points if present",
        example="no"
    )
    
    systemic_emboli: Literal["yes", "no"] = Field(
        ...,
        description="Evidence of systemic arterial emboli (excluding those included in vascular phenomena). Scores 3 points if present",
        example="no"
    )
    
    temperature_over_38c: Literal["yes", "no"] = Field(
        ...,
        description="Fever with documented temperature greater than 38°C (100.4°F). Scores 2 points if present",
        example="yes"
    )
    
    age_over_60: Literal["yes", "no"] = Field(
        ...,
        description="Patient age greater than 60 years. Scores 2 points if present",
        example="no"
    )
    
    wbc_over_11000: Literal["yes", "no"] = Field(
        ...,
        description="White blood cell count greater than 11,000/μL (11.0 × 10⁹/L). Scores 1 point if present",
        example="yes"
    )
    
    central_venous_catheter: Literal["yes", "no"] = Field(
        ...,
        description="Presence of central venous catheter or other intravascular device. Scores 1 point if present",
        example="no"
    )
    
    staph_aureus_bacteremia: Literal["yes", "no"] = Field(
        ...,
        description="Staphylococcus aureus bacteremia (methicillin-sensitive or methicillin-resistant). Scores 1 point if present",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "valve_disease_or_prosthetic_valve": "no",
                "injection_drug_use": "no",
                "vascular_phenomena": "no",
                "immunologic_phenomena": "no",
                "systemic_emboli": "no",
                "temperature_over_38c": "yes",
                "age_over_60": "no",
                "wbc_over_11000": "yes",
                "central_venous_catheter": "no",
                "staph_aureus_bacteremia": "yes"
            }
        }


class VirstaScoreResponse(BaseModel):
    """
    Response model for VIRSTA Score for Infective Endocarditis Risk Assessment
    
    Returns the VIRSTA score with risk stratification and clinical interpretation
    for guiding echocardiographic evaluation in suspected infective endocarditis.
    
    Score interpretation:
    - Score ≤1: Very low risk (NPV >99%)
      → Echocardiography may be deferred unless high clinical suspicion
      → Consider alternative diagnoses and outpatient management
      → Close follow-up recommended
    
    - Score ≥2: Higher risk 
      → Echocardiography recommended for further evaluation
      → Consider TEE if TTE negative and suspicion remains high
      → Initiate appropriate antimicrobial therapy
      → Monitor for complications (emboli, heart failure, abscess)
    
    Component breakdown provides transparency showing:
    - Individual criterion scores and presence
    - Total positive criteria count
    - High-value criteria (≥4 points) that significantly increase risk
    - Clinical context and validation notes
    
    Clinical significance:
    - Developed specifically for Staphylococcus aureus bacteremia patients
    - Excellent discrimination ability (AUC 0.87-0.89)
    - Helps reduce unnecessary echocardiographic studies
    - Maintains diagnostic safety with high negative predictive value
    - Should complement, not replace, clinical judgment
    
    Reference: Sunnerhagen T, et al. Clin Microbiol Infect. 2019;25(4):480-486.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=27,
        description="Total VIRSTA score calculated from clinical criteria (range: 0-27 points)",
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the VIRSTA score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with specific recommendations for echocardiographic evaluation and management",
        example="VIRSTA score of 4 indicates increased risk for infective endocarditis. Echocardiography is recommended for further evaluation. Consider transesophageal echocardiography if transthoracic echocardiography is negative and clinical suspicion remains high. Initiate appropriate antimicrobial therapy based on blood culture results and monitor closely for complications including embolic events, heart failure, and abscess formation."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification category (Very Low Risk, Higher Risk)",
        example="Higher Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Increased probability of infective endocarditis"
    )
    
    component_breakdown: Dict = Field(
        ...,
        description="Detailed breakdown of score components showing individual criteria, points, and clinical context",
        example={
            "total_score": 4,
            "positive_criteria_count": 3,
            "positive_criteria": [
                {"criterion": "Temperature Over 38C", "points": 2},
                {"criterion": "Wbc Over 11000", "points": 1},
                {"criterion": "Staph Aureus Bacteremia", "points": 1}
            ],
            "component_scores": {
                "valve_disease_or_prosthetic_valve": {"present": False, "points": 0},
                "injection_drug_use": {"present": False, "points": 0},
                "vascular_phenomena": {"present": False, "points": 0},
                "immunologic_phenomena": {"present": False, "points": 0},
                "systemic_emboli": {"present": False, "points": 0},
                "temperature_over_38c": {"present": True, "points": 2},
                "age_over_60": {"present": False, "points": 0},
                "wbc_over_11000": {"present": True, "points": 1},
                "central_venous_catheter": {"present": False, "points": 0},
                "staph_aureus_bacteremia": {"present": True, "points": 1}
            },
            "high_value_criteria": [],
            "scoring_notes": [
                "Score ≤1 has negative predictive value >99% for ruling out infective endocarditis",
                "Originally developed and validated in Staphylococcus aureus bacteremia patients",
                "Should be used in conjunction with clinical judgment"
            ]
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "VIRSTA score of 4 indicates increased risk for infective endocarditis. Echocardiography is recommended for further evaluation. Consider transesophageal echocardiography if transthoracic echocardiography is negative and clinical suspicion remains high. Initiate appropriate antimicrobial therapy based on blood culture results and monitor closely for complications including embolic events, heart failure, and abscess formation.",
                "stage": "Higher Risk",
                "stage_description": "Increased probability of infective endocarditis",
                "component_breakdown": {
                    "total_score": 4,
                    "positive_criteria_count": 3,
                    "positive_criteria": [
                        {"criterion": "Temperature Over 38C", "points": 2},
                        {"criterion": "Wbc Over 11000", "points": 1},
                        {"criterion": "Staph Aureus Bacteremia", "points": 1}
                    ],
                    "component_scores": {
                        "valve_disease_or_prosthetic_valve": {"present": False, "points": 0},
                        "injection_drug_use": {"present": False, "points": 0},
                        "vascular_phenomena": {"present": False, "points": 0},
                        "immunologic_phenomena": {"present": False, "points": 0},
                        "systemic_emboli": {"present": False, "points": 0},
                        "temperature_over_38c": {"present": True, "points": 2},
                        "age_over_60": {"present": False, "points": 0},
                        "wbc_over_11000": {"present": True, "points": 1},
                        "central_venous_catheter": {"present": False, "points": 0},
                        "staph_aureus_bacteremia": {"present": True, "points": 1}
                    },
                    "high_value_criteria": [],
                    "scoring_notes": [
                        "Score ≤1 has negative predictive value >99% for ruling out infective endocarditis",
                        "Originally developed and validated in Staphylococcus aureus bacteremia patients",
                        "Should be used in conjunction with clinical judgment"
                    ]
                }
            }
        }