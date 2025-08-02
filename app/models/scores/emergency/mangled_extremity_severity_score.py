"""
Mangled Extremity Severity Score (MESS) Models

Request and response models for MESS calculation.

References (Vancouver style):
1. Johansen K, Daines M, Howey T, Helfet D, Hansen ST Jr. Objective criteria accurately 
   predict amputation following lower extremity trauma. J Trauma. 1990 May;30(5):568-73. 
   doi: 10.1097/00005373-199005000-00007.
2. Bosse MJ, MacKenzie EJ, Kellam JF, Burgess AR, Webb LX, Swiontkowski MF, et al. 
   A prospective evaluation of the clinical utility of the lower-extremity injury-severity 
   scores. J Bone Joint Surg Am. 2001 Jan;83(1):3-14. doi: 10.2106/00004623-200101000-00002.
3. Georgiadis GM, Behrens FF, Joyce MJ, Earle AS, Simmons AL. Open tibial fractures with 
   severe soft-tissue loss. Limb salvage compared with below-the-knee amputation. J Bone 
   Joint Surg Am. 1993 Oct;75(10):1431-41. doi: 10.2106/00004623-199310000-00003.

The Mangled Extremity Severity Score (MESS) is a validated trauma assessment tool that 
estimates viability of an extremity after severe trauma to guide decisions between limb 
salvage and primary amputation. Developed in 1990 for lower extremity trauma, it evaluates 
four key factors: limb ischemia, patient age, shock status, and injury mechanism. While 
traditionally a score ≥7 suggested amputation, modern surgical advances have led to higher 
recommended thresholds (8-9 points) and emphasis on clinical judgment.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class MangledExtremitySeverityScoreRequest(BaseModel):
    """
    Request model for Mangled Extremity Severity Score (MESS)
    
    The MESS evaluates four critical factors to assess extremity viability after trauma:
    
    1. Limb Ischemia (1-3 points, doubled if >6 hours):
       - Reduced pulse, normal perfusion: 1 point
       - Pulseless, paresthesias, slow capillary refill: 2 points
       - Cool, paralyzed, numb/insensate: 3 points
       - Points doubled if ischemia duration >6 hours
    
    2. Patient Age (0-2 points):
       - <30 years: 0 points
       - 30-50 years: 1 point
       - ≥50 years: 2 points
       - Reflects healing capacity and complication risk
    
    3. Shock Status (0-2 points):
       - No shock (SBP >90 mmHg): 0 points
       - Transient hypotension: 1 point
       - Persistent hypotension: 2 points
       - Indicates systemic compromise affecting outcomes
    
    4. Injury Mechanism (1-4 points):
       - Low energy (stab, simple fracture, pistol GSW): 1 point
       - Medium energy (open/multiple fractures, dislocation): 2 points
       - High energy (high speed MVA, rifle GSW): 3 points
       - Very high energy (high speed + gross contamination): 4 points
    
    Score Interpretation:
    - 1-6 points: Limb salvage likely (good prognosis)
    - 7 points: Borderline decision (requires clinical judgment)
    - 8-14 points: Amputation likely (poor prognosis for salvage)
    
    Clinical Applications:
    - Emergency department trauma assessment
    - Surgical planning for mangled extremities
    - Resource allocation and triage decisions
    - Patient and family counseling
    - Documentation for quality assurance
    
    Important Considerations:
    - Developed primarily for lower extremity trauma
    - Less reliable in pediatric and upper extremity injuries
    - Should complement, not replace, clinical judgment
    - Modern surgical advances have improved salvage rates
    - Consider surgeon experience and available resources
    
    References (Vancouver style):
    1. Johansen K, Daines M, Howey T, Helfet D, Hansen ST Jr. Objective criteria accurately 
       predict amputation following lower extremity trauma. J Trauma. 1990 May;30(5):568-73. 
       doi: 10.1097/00005373-199005000-00007.
    2. Bosse MJ, MacKenzie EJ, Kellam JF, Burgess AR, Webb LX, Swiontkowski MF, et al. 
       A prospective evaluation of the clinical utility of the lower-extremity injury-severity 
       scores. J Bone Joint Surg Am. 2001 Jan;83(1):3-14. doi: 10.2106/00004623-200101000-00002.
    """
    
    limb_ischemia: Literal["reduced_pulse_normal_perfusion", "pulseless_paresthesias_slow_capillary_refill", "cool_paralyzed_numb_insensate"] = Field(
        ...,
        description="Assessment of limb perfusion and neurovascular status. Reduced pulse/normal perfusion (1pt), pulseless with paresthesias/slow capillary refill (2pts), or cool/paralyzed/numb/insensate (3pts). Points doubled if duration >6 hours",
        example="reduced_pulse_normal_perfusion"
    )
    
    ischemia_duration_hours: float = Field(
        ...,
        ge=0.0,
        le=24.0,
        description="Duration of limb ischemia in hours since injury. Critical factor: ischemia >6 hours doubles the ischemia component score due to increased tissue damage and reduced salvage potential",
        example=4.0
    )
    
    patient_age: int = Field(
        ...,
        ge=0,
        le=120,
        description="Patient age in years. Age categories: <30 years (0pts), 30-50 years (1pt), ≥50 years (2pts). Older patients have reduced healing capacity and increased complication risk",
        example=35
    )
    
    shock_status: Literal["no_shock_sbp_greater_than_90", "transient_hypotension", "persistent_hypotension"] = Field(
        ...,
        description="Hemodynamic status assessment. No shock with SBP >90 mmHg (0pts), transient hypotension (1pt), or persistent hypotension (2pts). Shock indicates systemic compromise affecting limb salvage outcomes",
        example="no_shock_sbp_greater_than_90"
    )
    
    injury_mechanism: Literal["low_energy", "medium_energy", "high_energy", "very_high_energy"] = Field(
        ...,
        description="Energy level and mechanism of injury. Low energy like stab/simple fracture/pistol GSW (1pt), medium energy like open/multiple fractures (2pts), high energy like high-speed MVA/rifle GSW (3pts), or very high energy with gross contamination (4pts)",
        example="medium_energy"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "limb_ischemia": "reduced_pulse_normal_perfusion",
                "ischemia_duration_hours": 4.0,
                "patient_age": 35,
                "shock_status": "no_shock_sbp_greater_than_90",
                "injury_mechanism": "medium_energy"
            }
        }


class MangledExtremitySeverityScoreResponse(BaseModel):
    """
    Response model for Mangled Extremity Severity Score (MESS)
    
    The MESS provides evidence-based guidance for limb salvage versus amputation decisions:
    
    Limb Salvage Likely (1-6 points):
    - Good prognosis for successful limb preservation
    - Proceed with aggressive salvage efforts
    - Multidisciplinary approach with close monitoring
    - Early rehabilitation planning recommended
    
    Borderline Decision (7 points):
    - Traditional amputation threshold, but modern practice varies
    - Requires careful clinical judgment and patient factors
    - Consider surgeon experience and available resources
    - Multidisciplinary discussion strongly recommended
    
    Amputation Likely (8-14 points):
    - High probability that primary amputation is most appropriate
    - Modern thresholds often higher due to surgical advances
    - Consider patient preferences and quality of life
    - Experienced teams may still attempt salvage in selected cases
    
    The MESS serves as a prognostic guide rather than a definitive decision-making tool.
    Final decisions should integrate clinical judgment, patient factors, available expertise,
    and institutional resources for optimal outcomes.
    
    Reference: Johansen K, et al. J Trauma. 1990;30(5):568-73.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="MESS assessment results including total score, component scores, risk categories, and detailed clinical guidance",
        example={
            "total_score": 4,
            "ischemia_base_score": 1,
            "ischemia_multiplier": 1,
            "final_ischemia_score": 1,
            "age_score": 1,
            "shock_score": 0,
            "mechanism_score": 2,
            "ischemia_category": "Limb ischemia: reduced pulse normal perfusion",
            "ischemia_duration_category": "Ischemia duration: 4.0 hours",
            "age_category": "Age: 35 years",
            "shock_category": "Shock status: no shock sbp greater than 90",
            "mechanism_category": "Injury mechanism: medium energy",
            "assessment_data": {
                "traditional_threshold": "≥7 points (traditional)",
                "modern_threshold": "≥8-9 points (modern recommendation)",
                "recommendation": "Limb salvage recommended",
                "confidence_level": "High confidence for salvage success",
                "ischemia_concerns": "Manageable",
                "decision_factors": "Consider surgeon experience, available resources, patient preferences"
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
        description="Comprehensive clinical interpretation with risk assessment, salvage likelihood, and detailed management recommendations",
        example="MESS score suggests limb salvage is likely to be successful. Proceed with aggressive limb preservation efforts including vascular repair, fracture stabilization, and soft tissue reconstruction."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification category (Limb Salvage Likely, Borderline Decision, Amputation Likely)",
        example="Limb Salvage Likely"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level and expected outcomes",
        example="Low risk for amputation with good salvage potential"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "total_score": 4,
                    "ischemia_base_score": 1,
                    "ischemia_multiplier": 1,
                    "final_ischemia_score": 1,
                    "age_score": 1,
                    "shock_score": 0,
                    "mechanism_score": 2,
                    "ischemia_category": "Limb ischemia: reduced pulse normal perfusion",
                    "ischemia_duration_category": "Ischemia duration: 4.0 hours",
                    "age_category": "Age: 35 years",
                    "shock_category": "Shock status: no shock sbp greater than 90",
                    "mechanism_category": "Injury mechanism: medium energy",
                    "assessment_data": {
                        "traditional_threshold": "≥7 points (traditional)",
                        "modern_threshold": "≥8-9 points (modern recommendation)",
                        "recommendation": "Limb salvage recommended",
                        "confidence_level": "High confidence for salvage success",
                        "ischemia_concerns": "Manageable",
                        "decision_factors": "Consider surgeon experience, available resources, patient preferences"
                    }
                },
                "unit": "points",
                "interpretation": "MESS score suggests limb salvage is likely to be successful. Proceed with aggressive limb preservation efforts including vascular repair, fracture stabilization, and soft tissue reconstruction.",
                "stage": "Limb Salvage Likely",
                "stage_description": "Low risk for amputation with good salvage potential"
            }
        }