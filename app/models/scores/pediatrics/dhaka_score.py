"""
Dehydration: Assessing Kids Accurately (DHAKA) Score Models

Request and response models for DHAKA score calculation for pediatric dehydration assessment.

References (Vancouver style):
1. Chisti MJ, Pietroni MAC, Smith JH, et al. Derivation and validation of a clinical 
   dehydration scale for children with acute diarrhoea: a prospective cohort study. 
   Lancet Glob Health. 2015;3(4):e204-e211. doi: 10.1016/S2214-109X(15)70015-1.
2. Pietroni MAC, Chisti MJ, Dewan ML, et al. External validation of the DHAKA score 
   and comparison with the current IMCI algorithm for the assessment of dehydration 
   in children with diarrhoea: a prospective cohort study. Lancet Glob Health. 
   2016;4(10):e744-e751. doi: 10.1016/S2214-109X(16)30150-4.
3. Goldman RD, Friedman JN, Parkin PC. Validation of the clinical dehydration scale 
   for children with acute gastroenteritis. Pediatrics. 2008;122(3):545-549. 
   doi: 10.1542/peds.2007-2134.
4. World Health Organization. The treatment of diarrhoea: a manual for physicians 
   and other senior health workers. 4th rev. Geneva: World Health Organization; 2005.

The DHAKA score is the first clinical dehydration assessment tool both empirically 
derived and externally validated for use in low-income country settings. It classifies 
dehydration severity in children under 5 years old with acute diarrhea using four 
readily available clinical parameters.

Scoring System:
- General Appearance: 0-4 points (normal, restless/irritable, lethargic/unconscious)
- Respirations: 0-2 points (normal, deep)
- Skin Pinch: 0-4 points (normal, slow, very slow)
- Tears: 0-2 points (normal, decreased, absent)

Dehydration Categories:
- No Dehydration (0-1 points): <3% fluid loss - home management
- Some Dehydration (2-3 points): 3-9% fluid loss - supervised ORT
- Severe Dehydration (4+ points): ≥10% fluid loss - IV rehydration, hospitalization

The tool demonstrates superior accuracy compared to the WHO IMCI algorithm and is 
specifically validated for children under 60 months with acute diarrhea (≥3 loose 
stools per day for <14 days).
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional, List, Dict, Any


class DhakaScoreRequest(BaseModel):
    """
    Request model for DHAKA Score for Pediatric Dehydration Assessment
    
    The DHAKA score uses four clinical parameters to assess dehydration severity:
    
    General Appearance:
    - normal: Child is alert, active, and interactive (0 points)
    - restless_irritable: Child is fussy, difficult to console, or restless (2 points)
    - lethargic_unconscious: Child is lethargic, drowsy, or unconscious (4 points)
    
    Respirations:
    - normal: Regular, unlabored breathing pattern (0 points)
    - deep: Deep, rapid breathing suggesting metabolic acidosis (2 points)
    
    Skin Pinch (Elasticity Test):
    - normal: Skin returns immediately when pinched (<2 seconds) (0 points)
    - slow: Skin returns slowly when pinched (2-5 seconds) (2 points)
    - very_slow: Skin returns very slowly or remains tented (>5 seconds) (4 points)
    
    Tears:
    - normal: Normal tear production when child cries or is distressed (0 points)
    - decreased: Reduced tear production when crying (1 point)
    - absent: No tears present when child cries (2 points)
    
    Validity Criteria:
    This score is validated for children under 60 months (5 years) with acute diarrhea 
    defined as ≥3 loose stools per day for <14 days. It should be used in conjunction 
    with clinical judgment and is particularly valuable in resource-limited settings.
    
    Clinical Application:
    The DHAKA score guides treatment decisions ranging from home management for minimal 
    dehydration to hospitalization for severe dehydration. It has demonstrated superior 
    accuracy compared to the WHO IMCI algorithm for dehydration assessment.
    
    Assessment Technique:
    - General appearance should be assessed during normal interaction with the child
    - Skin pinch test should be performed on lateral abdominal wall
    - Tear assessment requires observation during crying or distress
    - Deep respirations indicate compensatory hyperventilation for acidosis
    
    References (Vancouver style):
    1. Chisti MJ, Pietroni MAC, Smith JH, et al. Derivation and validation of a clinical 
    dehydration scale for children with acute diarrhoea: a prospective cohort study. 
    Lancet Glob Health. 2015;3(4):e204-e211. doi: 10.1016/S2214-109X(15)70015-1.
    2. Pietroni MAC, Chisti MJ, Dewan ML, et al. External validation of the DHAKA score 
    and comparison with the current IMCI algorithm for the assessment of dehydration 
    in children with diarrhoea: a prospective cohort study. Lancet Glob Health. 
    2016;4(10):e744-e751. doi: 10.1016/S2214-109X(16)30150-4.
    """
    
    general_appearance: Literal["normal", "restless_irritable", "lethargic_unconscious"] = Field(
        ...,
        description="Child's general appearance and level of consciousness. Normal (0 points), restless/irritable (2 points), or lethargic/unconscious (4 points)",
        example="restless_irritable"
    )
    
    respirations: Literal["normal", "deep"] = Field(
        ...,
        description="Respiratory pattern assessment. Normal breathing (0 points) or deep respirations suggesting acidosis (2 points)",
        example="normal"
    )
    
    skin_pinch: Literal["normal", "slow", "very_slow"] = Field(
        ...,
        description="Skin elasticity test on lateral abdominal wall. Normal return <2 seconds (0 points), slow return 2-5 seconds (2 points), or very slow return >5 seconds (4 points)",
        example="slow"
    )
    
    tears: Literal["normal", "decreased", "absent"] = Field(
        ...,
        description="Tear production when child cries or is distressed. Normal tears (0 points), decreased tears (1 point), or absent tears (2 points)",
        example="decreased"
    )
    
    child_age_months: Optional[int] = Field(
        None,
        ge=1,
        le=59,
        description="Child's age in months (must be <60 months for score validity). Used for clinical context and management guidance",
        example=18
    )
    
    diarrhea_duration: Optional[int] = Field(
        None,
        ge=1,
        le=13,
        description="Duration of current diarrheal illness in days (must be <14 days for acute diarrhea definition)",
        example=3
    )
    
    class Config:
        schema_extra = {
            "example": {
                "general_appearance": "restless_irritable",
                "respirations": "normal",
                "skin_pinch": "slow",
                "tears": "decreased",
                "child_age_months": 18,
                "diarrhea_duration": 3
            }
        }


class DhakaScoreResponse(BaseModel):
    """
    Response model for DHAKA Score for Pediatric Dehydration Assessment
    
    The DHAKA score provides comprehensive assessment of dehydration severity with:
    - Quantitative assessment (score 0-10)
    - Dehydration category classification (None/Some/Severe)
    - Estimated fluid loss percentages
    - Evidence-based management recommendations
    - Detailed rehydration guidance
    - Caregiver education and follow-up instructions
    
    Dehydration Categories and Fluid Loss:
    - No Dehydration (0-1 points): <3% fluid loss
    - Some Dehydration (2-3 points): 3-9% fluid loss
    - Severe Dehydration (4+ points): ≥10% fluid loss
    
    Management Approach:
    No dehydration requires home management with continued feeding, some dehydration 
    requires supervised oral rehydration therapy, and severe dehydration requires 
    immediate IV rehydration and hospitalization.
    
    Clinical Decision Support:
    The tool guides disposition decisions, fluid therapy selection, and monitoring 
    intensity while providing structured guidance for caregiver education and 
    follow-up planning.
    
    Reference: Chisti MJ, et al. Lancet Glob Health. 2015;3(4):e204-e211.
    """
    
    result: int = Field(
        ...,
        description="DHAKA score calculated from clinical variables (range: 0-10 points)",
        example=5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the DHAKA score",
        example="DHAKA score"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with dehydration severity and management recommendation",
        example="DHAKA score of 5 indicates Severe Dehydration with ≥10% estimated fluid loss. Child has severe dehydration requiring immediate intravenous rehydration and hospitalization for intensive monitoring."
    )
    
    stage: str = Field(
        ...,
        description="Dehydration category classification based on DHAKA score",
        example="Severe Dehydration"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the dehydration severity",
        example="Significant fluid loss requiring immediate intervention"
    )
    
    dhaka_score: int = Field(
        ...,
        description="The calculated DHAKA score",
        example=5
    )
    
    dehydration_category: str = Field(
        ...,
        description="Dehydration category classification (none, some, severe)",
        example="severe"
    )
    
    fluid_loss: str = Field(
        ...,
        description="Estimated percentage of fluid loss based on dehydration category",
        example="≥10%"
    )
    
    management: str = Field(
        ...,
        description="Primary management approach based on dehydration severity",
        example="Immediate IV rehydration, potential hospitalization"
    )
    
    monitoring_level: str = Field(
        ...,
        description="Required monitoring intensity",
        example="Intensive monitoring"
    )
    
    disposition: str = Field(
        ...,
        description="Recommended care setting and disposition",
        example="Hospitalization required"
    )
    
    clinical_assessment: Dict[str, Any] = Field(
        ...,
        description="Detailed clinical assessment including score components, validity criteria, and risk factors"
    )
    
    management_recommendations: Dict[str, Any] = Field(
        ...,
        description="Comprehensive management recommendations including fluid therapy guidance and monitoring requirements"
    )
    
    rehydration_details: Dict[str, Any] = Field(
        ...,
        description="Specific rehydration protocol details including urgency, setting, and success indicators"
    )
    
    score_components: List[Dict[str, Any]] = Field(
        ...,
        description="Detailed breakdown of individual score components and their point contributions"
    )
    
    caregiver_education: List[str] = Field(
        ...,
        description="Key education points for caregivers about dehydration management and monitoring"
    )
    
    follow_up_recommendations: Dict[str, Any] = Field(
        ...,
        description="Follow-up monitoring recommendations including timing, location, and red flag symptoms"
    )
    
    warning_signs: List[str] = Field(
        ...,
        description="Universal warning signs that require immediate medical attention"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5,
                "unit": "DHAKA score",
                "interpretation": "DHAKA score of 5 indicates Severe Dehydration with ≥10% estimated fluid loss. Child has severe dehydration requiring immediate intravenous rehydration and hospitalization for intensive monitoring.",
                "stage": "Severe Dehydration",
                "stage_description": "Significant fluid loss requiring immediate intervention",
                "dhaka_score": 5,
                "dehydration_category": "severe",
                "fluid_loss": "≥10%",
                "management": "Immediate IV rehydration, potential hospitalization",
                "monitoring_level": "Intensive monitoring",
                "disposition": "Hospitalization required",
                "clinical_assessment": {
                    "dhaka_score": 5,
                    "dehydration_category": "severe",
                    "score_components": [
                        "Restless or irritable (2 points)",
                        "Normal respirations (0 points)",
                        "Slow skin pinch return (2 points)",
                        "Decreased tears when crying (1 point)"
                    ],
                    "validity_criteria": [
                        "Age 18 months (<60 months) - score validity met",
                        "Diarrhea duration 3 days (<14 days) - acute diarrhea criteria met"
                    ],
                    "risk_factors": [
                        "Altered mental status indicates significant dehydration",
                        "Poor skin elasticity indicates volume depletion",
                        "Reduced tear production indicates dehydration"
                    ]
                },
                "management_recommendations": {
                    "primary_recommendations": [
                        "Immediate intravenous fluid resuscitation",
                        "Rapid assessment and stabilization of vital signs",
                        "Monitor for complications (shock, electrolyte imbalances)"
                    ],
                    "fluid_therapy": {
                        "route": "Intravenous",
                        "solution": "Lactated Ringer's or Normal Saline",
                        "rate": "20 mL/kg bolus, then 100 mL/kg over 6 hours",
                        "monitoring": "Continuous monitoring with frequent vital signs"
                    }
                },
                "rehydration_details": {
                    "urgency": "Emergency",
                    "setting": "Emergency department or hospital",
                    "expected_duration": "6-24 hours",
                    "success_indicators": [
                        "Improved perfusion and mental status",
                        "Stabilized vital signs",
                        "Improved urine output"
                    ]
                },
                "score_components": [
                    {
                        "component": "General Appearance",
                        "value": "restless_irritable",
                        "points": 2,
                        "description": "Child's level of consciousness and activity"
                    },
                    {
                        "component": "Skin Pinch",
                        "value": "slow",
                        "points": 2,
                        "description": "Skin elasticity and turgor"
                    }
                ],
                "caregiver_education": [
                    "Child has severe dehydration requiring immediate medical care",
                    "Hospital treatment is necessary",
                    "IV fluids will be needed initially",
                    "Continue breastfeeding throughout illness if applicable"
                ],
                "follow_up_recommendations": {
                    "timing": "Continuous until stable, then daily monitoring",
                    "location": "Hospital until stable, then outpatient follow-up",
                    "red_flags": "Any signs of clinical deterioration or complications"
                },
                "warning_signs": [
                    "Child becomes increasingly lethargic or difficult to wake",
                    "Persistent vomiting preventing fluid intake",
                    "High fever (>39°C/102.2°F)",
                    "Significant decrease or absence of urination"
                ]
            }
        }