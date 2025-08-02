"""
VTE-BLEED Score Models

Request and response models for VTE-BLEED Score calculation.

References (Vancouver style):
1. Klok FA, Hösel V, Clemens A, et al. Prediction of bleeding events in patients with 
   venous thromboembolism on stable anticoagulation treatment. Eur Respir J. 
   2016;48(5):1369-1376. doi: 10.1183/13993003.00280-2016
2. Barco S, Klok FA, Mahé I, et al. Impact of sex, age, and risk factors for venous 
   thromboembolism on the risk of major bleeding in patients with acute venous 
   thromboembolism. Circulation. 2020;141(1):8-17. doi: 10.1161/CIRCULATIONAHA.119.042716
3. Mahé I, Chidiac J, Bertoletti L, et al. The clinical course of venous thromboembolism 
   may differ according to cancer site. Am J Med. 2017;130(3):337-347. 
   doi: 10.1016/j.amjmed.2016.10.017
4. Prandoni P, Noventa F, Ghirarduzzi A, et al. The risk of recurrent venous 
   thromboembolism after discontinuing anticoagulation in patients with acute proximal 
   deep vein thrombosis or pulmonary embolism. Haematologica. 2007;92(2):199-205. 
   doi: 10.3324/haematol.10516

The VTE-BLEED Score assesses bleeding risk on anticoagulation therapy in patients with 
venous thromboembolism (VTE). This validated risk score enables better stratification 
of bleeding risk during stable anticoagulation after a first VTE episode.

Unlike bleeding risk scores derived from atrial fibrillation patients (HAS-BLED, 
HEMORR2HAGES, ATRIA), the VTE-BLEED score is specifically designed for VTE patients 
who have different comorbidity profiles and risk factors. VTE patients are typically 
younger and have different prevalence of conditions like cancer versus renal dysfunction.

Scoring System (6 criteria):
- Age ≥60 years: 1.5 points
- Active cancer: 2.0 points
- Male with uncontrolled hypertension: 1.0 point
- Anemia: 1.5 points
- History of bleeding: 1.5 points
- Renal dysfunction (CrCl 30-60 mL/min): 1.5 points

Score interpretation:
- Score <2: Low bleeding risk
- Score ≥2: Elevated bleeding risk

Clinical significance:
- Most validated bleeding risk score in VTE settings
- Good prediction power for major bleeding events
- Can identify patients at risk of intracranial and fatal bleeding
- Validated for direct oral anticoagulants and vitamin K antagonists
- Designed for patients on stable anticoagulation after 30 days of treatment
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, List


class VteBleedScoreRequest(BaseModel):
    """
    Request model for VTE-BLEED Score
    
    The VTE-BLEED Score uses 6 clinical criteria to assess bleeding risk in patients 
    receiving anticoagulation therapy for venous thromboembolism. Each criterion 
    contributes specific point values to the total score.
    
    Scoring criteria and points:
    1. Age ≥60 years (1.5 points) - Advanced age increases bleeding risk
    2. Active cancer (2.0 points) - Highest weighted factor due to multiple bleeding risks
    3. Male with uncontrolled hypertension (1.0 point) - Gender-specific hypertension risk
    4. Anemia (1.5 points) - Hemoglobin <13 g/dL (men) or <12 g/dL (women)
    5. History of bleeding (1.5 points) - Previous major bleeding episodes
    6. Renal dysfunction (1.5 points) - Creatinine clearance 30-60 mL/min
    
    Clinical context:
    - Designed for VTE patients on stable anticoagulation (after 30 days)
    - Validated in European VTE cohorts with various anticoagulants
    - Unlike AF-derived scores, accounts for VTE-specific risk profile
    - Cancer prevalence higher in VTE vs AF populations
    - Age distribution typically younger in VTE patients
    
    Risk stratification:
    - Low risk (score <2): Standard anticoagulation with routine monitoring
    - Elevated risk (score ≥2): Enhanced monitoring and individualized management
    
    Active cancer definition:
    - Currently receiving cancer treatment
    - Treated for cancer within past 6 months
    - Metastatic cancer regardless of treatment status
    
    Uncontrolled hypertension criteria (male patients only):
    - Systolic blood pressure >140 mmHg OR
    - Diastolic blood pressure >90 mmHg
    
    Major bleeding history includes:
    - Bleeding requiring hospitalization
    - Bleeding requiring blood transfusion
    - Bleeding requiring surgical intervention
    - Life-threatening or fatal bleeding
    
    References (Vancouver style):
    1. Klok FA, Hösel V, Clemens A, et al. Prediction of bleeding events in patients with 
    venous thromboembolism on stable anticoagulation treatment. Eur Respir J. 
    2016;48(5):1369-1376. doi: 10.1183/13993003.00280-2016
    2. Barco S, Klok FA, Mahé I, et al. Impact of sex, age, and risk factors for venous 
    thromboembolism on the risk of major bleeding in patients with acute venous 
    thromboembolism. Circulation. 2020;141(1):8-17.
    """
    
    age_60_or_older: Literal["yes", "no"] = Field(
        ...,
        description="Patient age 60 years or older. Advanced age increases bleeding risk due to comorbidities and drug metabolism changes. Scores 1.5 points if present",
        example="no"
    )
    
    active_cancer: Literal["yes", "no"] = Field(
        ...,
        description="Active cancer (currently receiving treatment, treated within 6 months, or metastatic disease). Highest weighted factor due to multiple bleeding mechanisms. Scores 2.0 points if present",
        example="no"
    )
    
    male_uncontrolled_hypertension: Literal["yes", "no"] = Field(
        ...,
        description="Male patient with uncontrolled hypertension (systolic BP >140 mmHg or diastolic BP >90 mmHg). Gender-specific risk factor. Scores 1.0 point if present",
        example="no"
    )
    
    anemia: Literal["yes", "no"] = Field(
        ...,
        description="Anemia (hemoglobin <13 g/dL in men or <12 g/dL in women). Indicates underlying bleeding risk or predisposition. Scores 1.5 points if present",
        example="no"
    )
    
    history_of_bleeding: Literal["yes", "no"] = Field(
        ...,
        description="History of major bleeding episode requiring hospitalization, transfusion, or surgery. Strong predictor of future bleeding risk. Scores 1.5 points if present",
        example="no"
    )
    
    renal_dysfunction: Literal["yes", "no"] = Field(
        ...,
        description="Renal dysfunction with creatinine clearance 30-60 mL/min. Affects anticoagulant clearance and bleeding risk. Scores 1.5 points if present",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_60_or_older": "yes",
                "active_cancer": "no",
                "male_uncontrolled_hypertension": "no",
                "anemia": "yes",
                "history_of_bleeding": "no",
                "renal_dysfunction": "no"
            }
        }


class VteBleedScoreResponse(BaseModel):
    """
    Response model for VTE-BLEED Score
    
    Returns the VTE-BLEED score with bleeding risk stratification and management 
    recommendations for patients receiving anticoagulation therapy for VTE.
    
    Score interpretation:
    - Score <2: Low bleeding risk
      → Continue standard anticoagulation with routine monitoring
      → Benefits typically outweigh bleeding risks
      → Standard follow-up intervals and patient education
      → Consider extended anticoagulation as clinically indicated
    
    - Score ≥2: Elevated bleeding risk
      → Enhanced monitoring with more frequent follow-up
      → Consider dose optimization or alternative anticoagulants
      → Implement enhanced bleeding precautions
      → Individual risk-benefit assessment for duration
      → Comprehensive patient education about bleeding warning signs
    
    Component breakdown provides transparency showing:
    - Individual criterion scores and presence
    - Total positive criteria count
    - High-risk factors (≥1.5 points) contributing to elevated risk
    - Risk factors present and their clinical significance
    - Tailored clinical recommendations based on specific risk profile
    
    Clinical applications:
    - VTE patients on stable anticoagulation (after 30 days of treatment)
    - Treatment duration decision-making
    - Anticoagulant selection and dosing
    - Monitoring frequency determination
    - Patient counseling and education
    - Clinical trial stratification
    
    Validation context:
    - Developed and validated in European VTE cohorts
    - Effective for direct oral anticoagulants and vitamin K antagonists
    - Predicts major bleeding, intracranial bleeding, and fatal bleeding
    - Superior performance compared to AF-derived bleeding scores in VTE patients
    
    Reference: Klok FA, et al. Eur Respir J. 2016;48(5):1369-1376.
    """
    
    result: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="Total VTE-BLEED score calculated from clinical criteria (range: 0-10 points)",
        example=3.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the VTE-BLEED score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with specific recommendations for anticoagulation management and bleeding risk mitigation",
        example="VTE-BLEED score of 3.0 indicates elevated bleeding risk. Consider more frequent monitoring with enhanced surveillance for bleeding complications. Evaluate for careful medication selection, potential dose adjustments, and shorter anticoagulation duration when clinically appropriate. Implement enhanced bleeding precautions and comprehensive patient education. Perform individual risk-benefit assessment for extended anticoagulation therapy."
    )
    
    stage: str = Field(
        ...,
        description="Bleeding risk category (Low Risk, Elevated Risk)",
        example="Elevated Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the bleeding risk category",
        example="Elevated bleeding risk on anticoagulation"
    )
    
    component_breakdown: Dict = Field(
        ...,
        description="Detailed breakdown of score components showing individual criteria, points, risk factors, and tailored clinical recommendations",
        example={
            "total_score": 3.0,
            "risk_category": "Elevated Risk",
            "positive_criteria_count": 2,
            "positive_criteria": [
                {"criterion": "Age 60 Or Older", "points": 1.5},
                {"criterion": "Anemia", "points": 1.5}
            ],
            "component_scores": {
                "age_60_or_older": {"present": True, "points": 1.5},
                "active_cancer": {"present": False, "points": 0.0},
                "male_uncontrolled_hypertension": {"present": False, "points": 0.0},
                "anemia": {"present": True, "points": 1.5},
                "history_of_bleeding": {"present": False, "points": 0.0},
                "renal_dysfunction": {"present": False, "points": 0.0}
            },
            "high_risk_factors": [
                {"criterion": "Age 60 Or Older", "points": 1.5},
                {"criterion": "Anemia", "points": 1.5}
            ],
            "risk_factors_present": ["Age 60 Or Older", "Anemia"],
            "clinical_recommendations": [
                "Enhanced monitoring with more frequent follow-up",
                "Comprehensive bleeding risk assessment",
                "Consider dose optimization or alternative anticoagulants",
                "Investigate and treat underlying anemia",
                "Monitor hemoglobin levels regularly",
                "Individual risk-benefit assessment for anticoagulation duration",
                "Enhanced patient education about bleeding warning signs"
            ],
            "score_validation": {
                "designed_for": "VTE patients on stable anticoagulation after 30 days",
                "validated_for": "Direct oral anticoagulants and vitamin K antagonists",
                "prediction_focus": "Major bleeding events, intracranial bleeding, fatal bleeding"
            }
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3.0,
                "unit": "points",
                "interpretation": "VTE-BLEED score of 3.0 indicates elevated bleeding risk. Consider more frequent monitoring with enhanced surveillance for bleeding complications. Evaluate for careful medication selection, potential dose adjustments, and shorter anticoagulation duration when clinically appropriate. Implement enhanced bleeding precautions and comprehensive patient education. Perform individual risk-benefit assessment for extended anticoagulation therapy.",
                "stage": "Elevated Risk",
                "stage_description": "Elevated bleeding risk on anticoagulation",
                "component_breakdown": {
                    "total_score": 3.0,
                    "risk_category": "Elevated Risk",
                    "positive_criteria_count": 2,
                    "positive_criteria": [
                        {"criterion": "Age 60 Or Older", "points": 1.5},
                        {"criterion": "Anemia", "points": 1.5}
                    ],
                    "component_scores": {
                        "age_60_or_older": {"present": True, "points": 1.5},
                        "active_cancer": {"present": False, "points": 0.0},
                        "male_uncontrolled_hypertension": {"present": False, "points": 0.0},
                        "anemia": {"present": True, "points": 1.5},
                        "history_of_bleeding": {"present": False, "points": 0.0},
                        "renal_dysfunction": {"present": False, "points": 0.0}
                    },
                    "high_risk_factors": [
                        {"criterion": "Age 60 Or Older", "points": 1.5},
                        {"criterion": "Anemia", "points": 1.5}
                    ],
                    "risk_factors_present": ["Age 60 Or Older", "Anemia"],
                    "clinical_recommendations": [
                        "Enhanced monitoring with more frequent follow-up",
                        "Comprehensive bleeding risk assessment",
                        "Consider dose optimization or alternative anticoagulants",
                        "Investigate and treat underlying anemia",
                        "Monitor hemoglobin levels regularly",
                        "Individual risk-benefit assessment for anticoagulation duration",
                        "Enhanced patient education about bleeding warning signs"
                    ],
                    "score_validation": {
                        "designed_for": "VTE patients on stable anticoagulation after 30 days",
                        "validated_for": "Direct oral anticoagulants and vitamin K antagonists",
                        "prediction_focus": "Major bleeding events, intracranial bleeding, fatal bleeding"
                    }
                }
            }
        }