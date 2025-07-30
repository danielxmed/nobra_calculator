"""
CASPAR Criteria for Psoriatic Arthritis Models

Request and response models for CASPAR Criteria calculation.

References (Vancouver style):
1. Taylor W, Gladman D, Helliwell P, Marchesoni A, Mease P, Mielants H; CASPAR Study Group. Classification criteria for psoriatic arthritis: development of new criteria from a large international study. Arthritis Rheum. 2006 Aug;54(8):2665-73. doi: 10.1002/art.21972.
2. Chandran V, Schentag CT, Gladman DD. Sensitivity and specificity of the CASPAR criteria for psoriatic arthritis in a family medicine clinic setting. J Rheumatol. 2008 Oct;35(10):2069-70.
3. Helliwell PS, Taylor WJ. Classification and diagnostic criteria for psoriatic arthritis. Ann Rheum Dis. 2005 Mar;64 Suppl 2(Suppl 2):ii3-8. doi: 10.1136/ard.2004.032318.

The CASPAR (ClASsification criteria for Psoriatic ARthritis) criteria provide standardized classification for psoriatic arthritis in research settings. The criteria require:

MANDATORY CRITERION:
- Inflammatory articular disease (joint, spine, or entheseal)

ADDITIONAL CRITERIA (≥3 points required):
- Current psoriasis (2 points) OR Personal/family history of psoriasis (1 point)
- Nail dystrophy: onycholysis, pitting, hyperkeratosis (1 point)
- Rheumatoid factor negative (1 point)
- Dactylitis: current or historical swelling of entire digit (1 point)
- Juxtaarticular new bone formation on X-ray (1 point)

Clinical Performance:
- Sensitivity: 91%
- Specificity: 98%
- Developed from international study of 588 PsA patients across 30 clinics

Important Note: CASPAR criteria are classification criteria designed for research and clinical trial patient selection, not diagnostic criteria for individual clinical practice.
"""

from pydantic import BaseModel, Field
from typing import Literal


class CasparCriteriaRequest(BaseModel):
    """
    Request model for CASPAR Criteria for Psoriatic Arthritis
    
    The CASPAR criteria provide standardized classification for psoriatic arthritis research.
    
    MANDATORY CRITERION:
    - Inflammatory articular disease (joint, spine, or entheseal) must be present
    
    ADDITIONAL CRITERIA SCORING (need ≥3 points):
    - Current psoriasis diagnosed by rheumatologist/dermatologist: 2 points
    - Personal or family history of psoriasis (if no current psoriasis): 1 point
    - Nail dystrophy (onycholysis, pitting, hyperkeratosis): 1 point
    - Rheumatoid factor negative (preferred ELISA/nephelometry): 1 point
    - Dactylitis (current or historical entire digit swelling): 1 point
    - Juxtaarticular new bone formation (X-ray hands/feet): 1 point
    
    Clinical Application:
    - Primarily for research and clinical trial patient selection
    - Sensitivity: 91%, Specificity: 98%
    - Not intended as standalone diagnostic tool for individual patients
    - Should be used in conjunction with clinical judgment
    
    References (Vancouver style):
    1. Taylor W, Gladman D, Helliwell P, Marchesoni A, Mease P, Mielants H; CASPAR Study Group. Classification criteria for psoriatic arthritis: development of new criteria from a large international study. Arthritis Rheum. 2006 Aug;54(8):2665-73. doi: 10.1002/art.21972.
    2. Chandran V, Schentag CT, Gladman DD. Sensitivity and specificity of the CASPAR criteria for psoriatic arthritis in a family medicine clinic setting. J Rheumatol. 2008 Oct;35(10):2069-70.
    3. Helliwell PS, Taylor WJ. Classification and diagnostic criteria for psoriatic arthritis. Ann Rheum Dis. 2005 Mar;64 Suppl 2(Suppl 2):ii3-8. doi: 10.1136/ard.2004.032318.
    """
    
    inflammatory_articular_disease: Literal["yes", "no"] = Field(
        ...,
        description="MANDATORY CRITERION: Presence of inflammatory articular disease (joint, spine, or entheseal). Must be 'yes' to proceed with classification",
        example="yes"
    )
    
    psoriasis_status: Literal["current", "history", "none"] = Field(
        ...,
        description="Current psoriasis status or history. 'current' = diagnosed by rheumatologist/dermatologist (2 pts), 'history' = personal/family history (1 pt), 'none' = no psoriasis (0 pts)",
        example="current"
    )
    
    nail_dystrophy: Literal["yes", "no"] = Field(
        ...,
        description="Nail dystrophy present on examination: onycholysis, pitting, or hyperkeratosis (1 point if present)",
        example="yes"
    )
    
    rheumatoid_factor: Literal["negative", "positive"] = Field(
        ...,
        description="Rheumatoid factor status. Preferred methods: ELISA or nephelometry (1 point if negative)",
        example="negative"
    )
    
    dactylitis: Literal["yes", "no"] = Field(
        ...,
        description="Dactylitis: current or historical swelling of entire digit (sausage digit) (1 point if present)",
        example="no"
    )
    
    juxta_articular_new_bone: Literal["yes", "no"] = Field(
        ...,
        description="Juxtaarticular new bone formation: ill-defined ossification near joint margins on X-ray of hands or feet (1 point if present)",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "inflammatory_articular_disease": "yes",
                "psoriasis_status": "current",
                "nail_dystrophy": "yes",
                "rheumatoid_factor": "negative",
                "dactylitis": "no",
                "juxta_articular_new_bone": "no"
            }
        }


class CasparCriteriaResponse(BaseModel):
    """
    Response model for CASPAR Criteria for Psoriatic Arthritis
    
    Returns classification result based on CASPAR criteria with detailed scoring breakdown.
    
    Classification Requirements:
    1. Mandatory criterion: Inflammatory articular disease must be present
    2. Additional criteria: Must score ≥3 points from 6 possible criteria
    
    Interpretation:
    - "Meets CASPAR Criteria": ≥3 points + mandatory criterion = PsA classification
    - "Does Not Meet CASPAR Criteria": <3 points or missing mandatory criterion
    
    The response includes detailed scoring breakdown showing how each criterion
    contributed to the total score, helping clinicians understand which features
    support or refute the PsA classification.
    
    Important Note: CASPAR criteria are for research classification, not clinical
    diagnosis. Clinical judgment may still support PsA diagnosis even if formal
    criteria are not met.
    
    Reference: Taylor W, et al. Arthritis Rheum. 2006;54(8):2665-73.
    """
    
    result: dict = Field(
        ...,
        description="CASPAR classification result with scoring details",
        example={
            "total_points": 4,
            "meets_criteria": True,
            "mandatory_criterion_met": True,
            "scoring_breakdown": {
                "psoriasis": {"status": "Current psoriasis", "points": 2},
                "nail_dystrophy": {"status": "Present", "points": 1},
                "rheumatoid_factor": {"status": "Negative", "points": 1},
                "dactylitis": {"status": "Absent", "points": 0},
                "juxta_articular_new_bone": {"status": "Absent", "points": 0}
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the criteria",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and implications of the CASPAR classification result",
        example="Patient meets CASPAR criteria for psoriatic arthritis classification with 4/6 possible points. The presence of inflammatory articular disease plus ≥3 points from additional criteria supports PsA classification for research purposes. Note: CASPAR criteria are classification criteria designed for research, not diagnostic criteria for clinical practice."
    )
    
    stage: str = Field(
        ...,
        description="Classification stage (Meets CASPAR Criteria or Does Not Meet CASPAR Criteria)",
        example="Meets CASPAR Criteria"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the classification result",
        example="Meets criteria for psoriatic arthritis classification"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "total_points": 4,
                    "meets_criteria": True,
                    "mandatory_criterion_met": True,
                    "scoring_breakdown": {
                        "psoriasis": {"status": "Current psoriasis", "points": 2},
                        "nail_dystrophy": {"status": "Present", "points": 1},
                        "rheumatoid_factor": {"status": "Negative", "points": 1},
                        "dactylitis": {"status": "Absent", "points": 0},
                        "juxta_articular_new_bone": {"status": "Absent", "points": 0}
                    }
                },
                "unit": "points",
                "interpretation": "Patient meets CASPAR criteria for psoriatic arthritis classification with 4/6 possible points. The presence of inflammatory articular disease plus ≥3 points from additional criteria supports PsA classification for research purposes. Note: CASPAR criteria are classification criteria designed for research, not diagnostic criteria for clinical practice.",
                "stage": "Meets CASPAR Criteria",
                "stage_description": "Meets criteria for psoriatic arthritis classification"
            }
        }