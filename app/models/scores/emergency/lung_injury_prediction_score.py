"""
Lung Injury Prediction Score (LIPS) Models

Request and response models for LIPS calculation to identify patients at risk for acute lung injury.

References (Vancouver style):
1. Gajic O, Dabbagh O, Park PK, Adesanya A, Chang SY, Hou P, et al. Early identification 
   of patients at risk of acute lung injury: evaluation of lung injury prediction score 
   in a multicenter cohort study. Am J Respir Crit Care Med. 2011 Feb 15;183(4):462-70. 
   doi: 10.1164/rccm.201004-0549OC.
2. Kor DJ, Warner DO, Alsara A, Fernández-Pérez ER, Malinchoc M, Kashyap R, et al. 
   Derivation and diagnostic accuracy of the surgical lung injury prediction model. 
   Anesthesiology. 2011 Jul;115(1):117-28. doi: 10.1097/ALN.0b013e31821b5839.
3. Trillo-Alvarez C, Cartin-Ceba R, Kor DJ, Kojicic M, Kashyap R, Thakur S, et al. 
   Acute lung injury prediction score: derivation and validation in a population-based sample. 
   Eur Respir J. 2011 Mar;37(3):604-9. doi: 10.1183/09031936.00036810.

The Lung Injury Prediction Score (LIPS) identifies patients at high risk for developing 
acute lung injury (ALI) using predisposing conditions, high-risk procedures, and risk 
modifiers. It enables early implementation of preventive strategies before mechanical 
ventilation is required. Score >4 points indicates high risk requiring lung-protective 
measures, conservative fluid management, and close monitoring.
"""

from pydantic import BaseModel, Field
from typing import Literal


class LungInjuryPredictionScoreRequest(BaseModel):
    """
    Request model for Lung Injury Prediction Score (LIPS)
    
    The LIPS uses predisposing conditions, high-risk procedures, and risk modifiers 
    to identify patients at risk for acute lung injury development:
    
    Predisposing Conditions:
    - Shock: Shock requiring vasopressors (2 points)
    - Aspiration: Witnessed or strongly suspected aspiration (2 points)  
    - Sepsis: Systemic inflammatory response to infection (1 point)
    - Pneumonia: Pneumonia present (1.5 points)
    - Pancreatitis: Pancreatitis present (1 point)
    
    High-Risk Surgery:
    - None: No high-risk surgery (0 points)
    - Orthopedic spine: Spine surgery (1 point)
    - Acute abdomen: Emergency abdominal surgery (2 points)
    - Cardiac: Cardiac surgery (2.5 points)
    - Aortic vascular: Aortic vascular surgery (3.5 points)
    - Emergency surgery: Any emergency surgery (1.5 points)
    
    High-Risk Trauma:
    - None: No high-risk trauma (0 points)
    - Traumatic brain injury: TBI (2 points)
    - Smoke inhalation: Smoke inhalation injury (2 points)
    - Near drowning: Near drowning event (2 points)
    - Lung contusion: Pulmonary contusion (1.5 points)
    - Multiple fractures: Multiple fractures (1.5 points)
    
    Risk Modifiers:
    - Alcohol abuse: History of alcohol abuse (1 point)
    - Obesity: BMI >30 kg/m² (1 point)
    - Hypoalbuminemia: Albumin <3.5 g/dL (1 point)
    - Chemotherapy: Recent chemotherapy (1 point)
    - FiO₂ >35%: Oxygen requirement >35% (2 points)
    - Tachypnea: Respiratory rate >30/min (1.5 points)
    - SpO₂ <95%: Oxygen saturation <95% (1 point)
    - Acidosis: pH <7.35 (1.5 points)
    - Diabetes with sepsis: Protective factor if sepsis present (-1 point)
    
    Score Interpretation:
    - ≤4 points: Low risk for ALI development
    - >4 points: High risk for ALI development (15-25% probability)
    
    Clinical Application:
    - Calculate within 24 hours of admission or ICU transfer
    - High-risk patients benefit from lung-protective strategies
    - Useful for ALI prevention trial enrollment
    - ALI typically develops within 2 days (median) of assessment
    
    References (Vancouver style):
    1. Gajic O, Dabbagh O, Park PK, Adesanya A, Chang SY, Hou P, et al. Early identification 
    of patients at risk of acute lung injury: evaluation of lung injury prediction score 
    in a multicenter cohort study. Am J Respir Crit Care Med. 2011 Feb 15;183(4):462-70. 
    doi: 10.1164/rccm.201004-0549OC.
    2. Kor DJ, Warner DO, Alsara A, Fernández-Pérez ER, Malinchoc M, Kashyap R, et al. 
    Derivation and diagnostic accuracy of the surgical lung injury prediction model. 
    Anesthesiology. 2011 Jul;115(1):117-28. doi: 10.1097/ALN.0b013e31821b5839.
    3. Trillo-Alvarez C, Cartin-Ceba R, Kor DJ, Kojicic M, Kashyap R, Thakur S, et al. 
    Acute lung injury prediction score: derivation and validation in a population-based sample. 
    Eur Respir J. 2011 Mar;37(3):604-9. doi: 10.1183/09031936.00036810.
    """
    
    shock: Literal["yes", "no"] = Field(
        ...,
        description="Shock requiring vasopressors. Scores 2 points if present",
        example="no"
    )
    
    aspiration: Literal["yes", "no"] = Field(
        ...,
        description="Aspiration witnessed or strongly suspected. Scores 2 points if present",
        example="no"
    )
    
    sepsis: Literal["yes", "no"] = Field(
        ...,
        description="Sepsis (systemic inflammatory response to infection). Scores 1 point if present",
        example="yes"
    )
    
    pneumonia: Literal["yes", "no"] = Field(
        ...,
        description="Pneumonia present. Scores 1.5 points if present",
        example="yes"
    )
    
    pancreatitis: Literal["yes", "no"] = Field(
        ...,
        description="Pancreatitis present. Scores 1 point if present",
        example="no"
    )
    
    high_risk_surgery: Literal[
        "none", "orthopedic_spine", "acute_abdomen", "cardiac", "aortic_vascular", "emergency_surgery"
    ] = Field(
        ...,
        description="High-risk surgery type. "
                   "none (0 pts), orthopedic_spine (1 pt), acute_abdomen (2 pts), "
                   "cardiac (2.5 pts), aortic_vascular (3.5 pts), emergency_surgery (1.5 pts)",
        example="none"
    )
    
    high_risk_trauma: Literal[
        "none", "traumatic_brain_injury", "smoke_inhalation", "near_drowning", "lung_contusion", "multiple_fractures"
    ] = Field(
        ...,
        description="High-risk trauma type. "
                   "none (0 pts), traumatic_brain_injury (2 pts), smoke_inhalation (2 pts), "
                   "near_drowning (2 pts), lung_contusion (1.5 pts), multiple_fractures (1.5 pts)",
        example="none"
    )
    
    alcohol_abuse: Literal["yes", "no"] = Field(
        ...,
        description="History of alcohol abuse. Scores 1 point if present",
        example="no"
    )
    
    obesity: Literal["yes", "no"] = Field(
        ...,
        description="Obesity (BMI >30 kg/m²). Scores 1 point if present",
        example="no"
    )
    
    hypoalbuminemia: Literal["yes", "no"] = Field(
        ...,
        description="Hypoalbuminemia (albumin <3.5 g/dL). Scores 1 point if present",
        example="yes"
    )
    
    chemotherapy: Literal["yes", "no"] = Field(
        ...,
        description="Recent chemotherapy. Scores 1 point if present",
        example="no"
    )
    
    fio2_over_35: Literal["yes", "no"] = Field(
        ...,
        description="FiO₂ >35% or >0.35. Scores 2 points if present",
        example="no"
    )
    
    tachypnea: Literal["yes", "no"] = Field(
        ...,
        description="Tachypnea (respiratory rate >30/min). Scores 1.5 points if present",
        example="yes"
    )
    
    spo2_under_95: Literal["yes", "no"] = Field(
        ...,
        description="SpO₂ <95%. Scores 1 point if present",
        example="yes"
    )
    
    acidosis: Literal["yes", "no"] = Field(
        ...,
        description="Acidosis (pH <7.35). Scores 1.5 points if present",
        example="no"
    )
    
    diabetes_with_sepsis: Literal["yes", "no"] = Field(
        ...,
        description="Diabetes mellitus (protective factor, scores -1 point if sepsis also present)",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "shock": "no",
                "aspiration": "no", 
                "sepsis": "yes",
                "pneumonia": "yes",
                "pancreatitis": "no",
                "high_risk_surgery": "none",
                "high_risk_trauma": "none",
                "alcohol_abuse": "no",
                "obesity": "no",
                "hypoalbuminemia": "yes",
                "chemotherapy": "no",
                "fio2_over_35": "no",
                "tachypnea": "yes",
                "spo2_under_95": "yes",
                "acidosis": "no",
                "diabetes_with_sepsis": "no"
            }
        }


class LungInjuryPredictionScoreResponse(BaseModel):
    """
    Response model for Lung Injury Prediction Score (LIPS)
    
    The LIPS provides risk stratification for acute lung injury development:
    
    Score Interpretation:
    - 0-4 points: Low risk for ALI development (<10% probability)
      Standard monitoring and care with routine clinical assessment
    
    - >4 points: High risk for ALI development (15-25% probability)
      Implement preventive strategies including lung-protective ventilation,
      conservative fluid management, and close monitoring
    
    Clinical Significance:
    - Sensitivity: 69% for ALI development
    - Specificity: 78% for ALI development  
    - Positive likelihood ratio: 3.1
    - Negative likelihood ratio: 0.4
    - Area under ROC curve: 0.84 (95% CI 0.80-0.89)
    - ALI typically develops within 2 days (median) of assessment
    
    Prevention Strategies for High-Risk Patients:
    - Lung-protective ventilation (low tidal volume, appropriate PEEP)
    - Conservative IV fluid management
    - Minimize high FiO₂ exposure
    - Close SpO₂ monitoring
    - Treat underlying conditions aggressively
    
    Reference: Gajic O, et al. Am J Respir Crit Care Med. 2011;183(4):462-70.
    """
    
    result: float = Field(
        ...,
        description="LIPS score calculated from predisposing conditions and risk factors (range 0-20+ points)",
        ge=0,
        le=25,
        example=5.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the LIPS score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with risk assessment and prevention strategies",
        example="Lung Injury Prediction Score (LIPS) Assessment:\n\nComponent Scores:\n• Predisposing conditions: 2.5 points\n• High-risk surgery: 0 points\n• High-risk trauma: 0 points\n• Risk modifiers: 2.5 points\n• Total LIPS score: 5.0/20+ points"
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on LIPS score",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of ALI development risk",
        example="High risk for acute lung injury"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5.0,
                "unit": "points",
                "interpretation": "Lung Injury Prediction Score (LIPS) Assessment:\n\nComponent Scores:\n• Predisposing conditions: 2.5 points\n• High-risk surgery: 0 points\n• High-risk trauma: 0 points\n• Risk modifiers: 2.5 points\n• Total LIPS score: 5.0/20+ points\n\nRisk Assessment:\n• Risk category: High Risk\n• Probability of ALI development: 15-25%\n• Typical time to ALI development: 2 days (median)\n\nPrevention Strategies:\n• Monitoring: Close SpO₂ monitoring and frequent assessment\n• Ventilation: Lung-protective ventilation (low tidal volume 6-8 mL/kg PBW, PEEP 5-10 cmH₂O)\n• Fluid management: Conservative IV fluid strategy, avoid fluid overload\n• Interventions: Minimize high FiO₂, avoid unnecessary procedures, treat underlying conditions",
                "stage": "High Risk",
                "stage_description": "High risk for acute lung injury"
            }
        }