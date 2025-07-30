"""
Crohn's Disease Activity Index (CDAI) Models

Request and response models for CDAI calculation.

References (Vancouver style):
1. Best WR, Becktel JM, Singleton JW, Kern F Jr. Development of a Crohn's disease 
   activity index. National Cooperative Crohn's Disease Study. Gastroenterology. 
   1976;70(3):439-444.
2. Sandborn WJ, Feagan BG, Hanauer SB, et al. A review of activity indices and 
   efficacy endpoints for clinical trials of medical therapy in adults with Crohn's 
   disease. Gastroenterology. 2002;122(2):512-530.
3. Jørgensen LG, Fredholm L, Hyltoft Petersen P, et al. How accurate are clinical 
   activity indices for scoring of disease activity in inflammatory bowel disease (IBD)? 
   Clin Chem Lab Med. 2005;43(4):403-411.

The Crohn's Disease Activity Index (CDAI) is a validated clinical tool that quantifies 
disease activity in Crohn's disease patients. Developed in 1976 by the National 
Cooperative Crohn's Disease Study Group, it incorporates 8 clinical variables weighted 
by their relative importance to produce a score ranging from 0 to approximately 600 points.

The CDAI uses a 7-day patient diary to assess symptoms including liquid stool frequency, 
abdominal pain, and general well-being, combined with clinical findings such as 
extraintestinal complications, abdominal mass, and laboratory values (hematocrit) 
plus anthropometric data (weight). It remains the gold standard for assessing 
Crohn's disease activity in clinical trials and research.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Dict, List, Any


class CdaiCrohnsRequest(BaseModel):
    """
    Request model for Crohn's Disease Activity Index (CDAI)
    
    The CDAI evaluates Crohn's disease activity using 8 weighted components:
    
    1. **Liquid Stools** (past 7 days): Total count × 2
    2. **Abdominal Pain** (0-3 scale): Average daily rating × 5
    3. **General Well-being** (0-4 scale): Average daily rating × 7  
    4. **Extraintestinal Complications**: Number present × 20
       - Arthritis/arthralgias
       - Iritis/uveitis
       - Erythema nodosum
       - Anal fissure/fistula
       - Other fistulas
       - Fever >37.8°C
    5. **Antidiarrheal Use**: Present (1) or absent (0) × 30
    6. **Abdominal Mass**: None (0), questionable (2), definite (5) × 10
    7. **Hematocrit Deficit**: (Expected - observed) × 6
       - Expected: 47% (men), 42% (women)
    8. **Weight Deficit**: Percentage below ideal weight × 1
    
    **Score Interpretation:**
    - <150: Remission
    - 150-219: Mild disease activity
    - 220-299: Moderate disease activity
    - 300-450: Severe disease activity
    - >450: Very severe disease activity
    
    **Clinical Significance:**
    - ≥70 point decrease: Significant treatment response
    - ≥100 point decrease: Major clinical response
    - Used as primary endpoint in clinical trials
    
    **Assessment Requirements:**
    - 7-day patient diary for stool frequency, pain, and well-being
    - Physical examination for abdominal mass and complications
    - Laboratory hematocrit value
    - Accurate weight measurement and ideal weight calculation
    
    References (Vancouver style):
    1. Best WR, Becktel JM, Singleton JW, Kern F Jr. Development of a Crohn's disease 
    activity index. National Cooperative Crohn's Disease Study. Gastroenterology. 
    1976;70(3):439-444.
    2. Sandborn WJ, Feagan BG, Hanauer SB, et al. A review of activity indices and 
    efficacy endpoints for clinical trials of medical therapy in adults with Crohn's 
    disease. Gastroenterology. 2002;122(2):512-530.
    3. Jørgensen LG, Fredholm L, Hyltoft Petersen P, et al. How accurate are clinical 
    activity indices for scoring of disease activity in inflammatory bowel disease (IBD)? 
    Clin Chem Lab Med. 2005;43(4):403-411.
    """
    
    liquid_stools_week: int = Field(
        ...,
        ge=0,
        le=200,
        description="Total number of liquid or loose stools over the past 7 days from patient diary. Include all episodes of liquid consistency regardless of volume",
        example=14
    )
    
    abdominal_pain_score: Literal["none", "mild", "moderate", "severe"] = Field(
        ...,
        description="Average daily abdominal pain rating over past 7 days. 0=none, 1=mild, 2=moderate, 3=severe pain levels",
        example="moderate"
    )
    
    general_wellbeing_score: Literal["generally_well", "slightly_under_par", "poor", "very_poor", "terrible"] = Field(
        ...,
        description="Average daily general well-being over past 7 days. 0=generally well, 1=slightly under par, 2=poor, 3=very poor, 4=terrible",
        example="poor"
    )
    
    arthritis_arthralgias: Literal["yes", "no"] = Field(
        ...,
        description="Presence of arthritis or arthralgias (joint pain/inflammation). Include any joint symptoms related to IBD",
        example="no"
    )
    
    iritis_uveitis: Literal["yes", "no"] = Field(
        ...,
        description="Presence of iritis or uveitis (eye inflammation). Include any ocular inflammatory symptoms",
        example="no"
    )
    
    erythema_nodosum: Literal["yes", "no"] = Field(
        ...,
        description="Presence of erythema nodosum (painful red nodules on skin, typically legs). IBD-related skin manifestation",
        example="no"
    )
    
    anal_fissure_fistula: Literal["yes", "no"] = Field(
        ...,
        description="Presence of anal fissure, fistula, or abscess. Common perianal complications of Crohn's disease",
        example="yes"
    )
    
    other_fistulas: Literal["yes", "no"] = Field(
        ...,
        description="Presence of other fistulas (excluding anal). Include enteroenteric, enterovesical, enterocutaneous fistulas",
        example="no"
    )
    
    fever: Literal["yes", "no"] = Field(
        ...,
        description="Fever >37.8°C (100°F) during the past 7 days. Temperature must exceed this threshold to be considered positive",
        example="no"
    )
    
    antidiarrheal_use: Literal["yes", "no"] = Field(
        ...,
        description="Use of antidiarrheal medications (loperamide, diphenoxylate, codeine) during past 7 days. Include any antispasmodic use",
        example="yes"
    )
    
    abdominal_mass: Literal["none", "questionable", "definite"] = Field(
        ...,
        description="Presence of abdominal mass on physical examination. None=0 points, questionable=2 points, definite=5 points",
        example="questionable"
    )
    
    patient_sex: Literal["male", "female"] = Field(
        ...,
        description="Patient biological sex for expected hematocrit calculation. Men: 47% expected, Women: 42% expected",
        example="female"
    )
    
    observed_hematocrit: float = Field(
        ...,
        ge=10.0,
        le=60.0,
        description="Current hematocrit percentage from laboratory results. Normal ranges: men 41-50%, women 36-46%",
        example=38.5
    )
    
    current_weight: float = Field(
        ...,
        ge=30.0,
        le=300.0,
        description="Current body weight in kilograms. Weigh patient consistently (same time, clothing, scale)",
        example=58.0
    )
    
    ideal_weight: float = Field(
        ...,
        ge=30.0,
        le=300.0,
        description="Ideal body weight in kilograms. Can be calculated using height-weight formulas or pre-illness weight",
        example=65.0
    )
    
    @validator('ideal_weight')
    def validate_weight_relationship(cls, v, values):
        if 'current_weight' in values and v < values['current_weight'] * 0.5:
            raise ValueError('Ideal weight seems too low compared to current weight')
        if 'current_weight' in values and v > values['current_weight'] * 2.0:
            raise ValueError('Ideal weight seems too high compared to current weight')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "liquid_stools_week": 14,
                "abdominal_pain_score": "moderate",
                "general_wellbeing_score": "poor",
                "arthritis_arthralgias": "no",
                "iritis_uveitis": "no",
                "erythema_nodosum": "no",
                "anal_fissure_fistula": "yes",
                "other_fistulas": "no",
                "fever": "no",
                "antidiarrheal_use": "yes",
                "abdominal_mass": "questionable",
                "patient_sex": "female",
                "observed_hematocrit": 38.5,
                "current_weight": 58.0,
                "ideal_weight": 65.0
            }
        }


class CdaiCrohnsResponse(BaseModel):
    """
    Response model for Crohn's Disease Activity Index (CDAI)
    
    The CDAI provides a quantitative assessment of Crohn's disease activity ranging 
    from 0 to approximately 600 points. It serves as the gold standard for disease 
    activity assessment in clinical trials and research settings.
    
    **Score Interpretation:**
    - **<150**: Clinical remission - Continue maintenance therapy
    - **150-219**: Mild disease activity - Consider therapy optimization  
    - **220-299**: Moderate disease activity - Consider step-up therapy
    - **300-450**: Severe disease activity - Intensive therapy required
    - **>450**: Very severe disease activity - Consider hospitalization
    
    **Treatment Response Criteria:**
    - **Significant response**: ≥70 point decrease from baseline
    - **Major response**: ≥100 point decrease from baseline
    - **Remission**: Score <150 points
    
    **Clinical Applications:**
    - Primary endpoint in clinical trials
    - Treatment response monitoring
    - Disease severity stratification
    - Research standardization
    
    Reference: Best WR, et al. Gastroenterology. 1976;70(3):439-444.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=600,
        description="Total CDAI score calculated from weighted clinical components (range: 0-600 points)",
        example=287
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the CDAI score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with disease activity assessment and management recommendations",
        example="CDAI score of 287 indicates moderate disease activity. Consider corticosteroids, immunomodulators, or biologic therapy. Reassess in 2-4 weeks."
    )
    
    stage: str = Field(
        ...,
        description="Disease activity stage (Remission, Mild Disease, Moderate Disease, Severe Disease, Very Severe Disease)",
        example="Moderate Disease"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the disease activity stage",
        example="Moderate disease activity"
    )
    
    component_breakdown: Dict[str, Dict[str, Any]] = Field(
        ...,
        description="Detailed breakdown of scores for each CDAI component with multipliers",
        example={
            "liquid_stools": {
                "score": 28.0,
                "description": "Number of liquid stools × 2",
                "multiplier": 2
            },
            "abdominal_pain": {
                "score": 10.0,
                "description": "Abdominal pain rating × 5",
                "multiplier": 5
            },
            "general_wellbeing": {
                "score": 14.0,
                "description": "General well-being rating × 7",
                "multiplier": 7
            },
            "extraintestinal": {
                "score": 20.0,
                "description": "Number of extraintestinal complications × 20",
                "multiplier": 20
            },
            "antidiarrheal": {
                "score": 30.0,
                "description": "Antidiarrheal drug use × 30",
                "multiplier": 30
            },
            "abdominal_mass": {
                "score": 20.0,
                "description": "Abdominal mass presence × 10",
                "multiplier": 10
            },
            "hematocrit": {
                "score": 21.0,
                "description": "Hematocrit deficit × 6",
                "multiplier": 6
            },
            "weight": {
                "score": 10.8,
                "description": "Weight deficit percentage × 1",
                "multiplier": 1
            }
        }
    )
    
    clinical_significance: Dict[str, Any] = Field(
        ...,
        description="Clinical significance including treatment response criteria and monitoring recommendations",
        example={
            "treatment_response_criteria": {
                "significant_response": "≥70 point decrease from baseline",
                "major_response": "≥100 point decrease from baseline",
                "remission_threshold": "<150 points"
            },
            "clinical_trial_usage": "Primary endpoint in most Crohn's disease clinical trials",
            "monitoring_frequency": "Every 1-2 weeks with close monitoring",
            "treatment_considerations": [
                "Consider corticosteroids for rapid symptom control",
                "Initiate or optimize immunomodulators",
                "Consider biologic therapy",
                "Nutritional assessment and support"
            ]
        }
    )
    
    calculation_details: Dict[str, Any] = Field(
        ...,
        description="Detailed calculation information including formula and validation data",
        example={
            "formula": "CDAI = (Liquid stools × 2) + (Pain × 5) + (Well-being × 7) + (Complications × 20) + (Antidiarrheal × 30) + (Mass × 10) + (Hematocrit deficit × 6) + (Weight deficit × 1)",
            "total_possible_range": "0 to ~600 points",
            "assessment_period": "Based on 7-day patient diary",
            "original_study": "National Cooperative Crohn's Disease Study (1976)",
            "validation_studies": "Multiple validation studies confirm reliability and validity"
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 287,
                "unit": "points",
                "interpretation": "CDAI score of 287 indicates moderate disease activity. Consider corticosteroids, immunomodulators, or biologic therapy. Reassess in 2-4 weeks.",
                "stage": "Moderate Disease",
                "stage_description": "Moderate disease activity",
                "component_breakdown": {
                    "liquid_stools": {
                        "score": 28.0,
                        "description": "Number of liquid stools × 2",
                        "multiplier": 2
                    },
                    "abdominal_pain": {
                        "score": 10.0,
                        "description": "Abdominal pain rating × 5",
                        "multiplier": 5
                    },
                    "general_wellbeing": {
                        "score": 14.0,
                        "description": "General well-being rating × 7",
                        "multiplier": 7
                    },
                    "extraintestinal": {
                        "score": 20.0,
                        "description": "Number of extraintestinal complications × 20",
                        "multiplier": 20
                    },
                    "antidiarrheal": {
                        "score": 30.0,
                        "description": "Antidiarrheal drug use × 30",
                        "multiplier": 30
                    },
                    "abdominal_mass": {
                        "score": 20.0,
                        "description": "Abdominal mass presence × 10",
                        "multiplier": 10
                    },
                    "hematocrit": {
                        "score": 21.0,
                        "description": "Hematocrit deficit × 6",
                        "multiplier": 6
                    },
                    "weight": {
                        "score": 10.8,
                        "description": "Weight deficit percentage × 1",
                        "multiplier": 1
                    }
                },
                "clinical_significance": {
                    "treatment_response_criteria": {
                        "significant_response": "≥70 point decrease from baseline",
                        "major_response": "≥100 point decrease from baseline",
                        "remission_threshold": "<150 points"
                    },
                    "clinical_trial_usage": "Primary endpoint in most Crohn's disease clinical trials",
                    "monitoring_frequency": "Every 1-2 weeks with close monitoring",
                    "treatment_considerations": [
                        "Consider corticosteroids for rapid symptom control",
                        "Initiate or optimize immunomodulators",
                        "Consider biologic therapy",
                        "Nutritional assessment and support"
                    ]
                },
                "calculation_details": {
                    "formula": "CDAI = (Liquid stools × 2) + (Pain × 5) + (Well-being × 7) + (Complications × 20) + (Antidiarrheal × 30) + (Mass × 10) + (Hematocrit deficit × 6) + (Weight deficit × 1)",
                    "total_possible_range": "0 to ~600 points",
                    "assessment_period": "Based on 7-day patient diary",
                    "original_study": "National Cooperative Crohn's Disease Study (1976)",
                    "validation_studies": "Multiple validation studies confirm reliability and validity"
                }
            }
        }