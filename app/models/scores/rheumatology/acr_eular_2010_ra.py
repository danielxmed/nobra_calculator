"""
ACR/EULAR 2010 Rheumatoid Arthritis Classification Criteria Models

Request and response models for ACR/EULAR 2010 RA classification criteria calculation.

References (Vancouver style):
1. Aletaha D, Neogi T, Silman AJ, Funovits J, Felson DT, Bingham CO 3rd, Birnbaum NS, 
   Burmester GR, Bykerk VP, Cohen MD, Combe B, Costenbader KH, Dougados M, Emery P, 
   Ferraccioli G, Hazes JM, Hobbs K, Huizinga TW, Kavanaugh A, Kay J, Kvien TK, Laing T, 
   Mease P, Ménard HA, Moreland LW, Naden RL, Pincus T, Smolen JS, Stanislawska-Biernat E, 
   Symmons D, Tak PP, Upchurch KS, Vencovský J, Wolfe F, Hawker G. 2010 Rheumatoid 
   arthritis classification criteria: an American College of Rheumatology/European League 
   Against Rheumatism collaborative initiative. Arthritis Rheum. 2010 Sep;62(9):2569-81. 
   doi: 10.1002/art.27584.

2. Aletaha D, Neogi T, Silman AJ, Funovits J, Felson DT, Bingham CO 3rd, Birnbaum NS, 
   Burmester GR, Bykerk VP, Cohen MD, Combe B, Costenbader KH, Dougados M, Emery P, 
   Ferraccioli G, Hazes JM, Hobbs K, Huizinga TW, Kavanaugh A, Kay J, Kvien TK, Laing T, 
   Mease P, Ménard HA, Moreland LW, Naden RL, Pincus T, Smolen JS, Stanislawska-Biernat E, 
   Symmons D, Tak PP, Upchurch KS, Vencovský J, Wolfe F, Hawker G. 2010 rheumatoid 
   arthritis classification criteria: an American College of Rheumatology/European League 
   Against Rheumatism collaborative initiative. Ann Rheum Dis. 2010 Sep;69(9):1580-8. 
   doi: 10.1136/ard.2010.138461.

The ACR/EULAR 2010 criteria were developed to facilitate early identification of RA in 
patients with undifferentiated inflammatory synovitis, enabling timely initiation of 
disease-modifying antirheumatic drugs (DMARDs). The criteria comprise four domains: 
joint involvement (0-5 points), serology (0-3 points), acute-phase reactants (0-1 point), 
and duration of symptoms (0-1 point). A score ≥6 indicates definite RA.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AcrEular2010RaRequest(BaseModel):
    """
    Request model for ACR/EULAR 2010 Rheumatoid Arthritis Classification Criteria
    
    The ACR/EULAR 2010 criteria assess four domains to classify rheumatoid arthritis:
    
    1. Joint Involvement (0-5 points):
       - 1_large: 1 large joint (0 points)
       - 2_to_10_large: 2-10 large joints (1 point)
       - 1_to_3_small: 1-3 small joints with or without large joints (2 points)
       - 4_to_10_small: 4-10 small joints with or without large joints (3 points)
       - more_than_10_small: >10 joints with at least 1 small joint (5 points)
    
    2. Serology (0-3 points):
       - Both RF and ACPA negative (0 points)
       - Low-positive RF or ACPA (2 points) - IU values >ULN but <3x ULN
       - High-positive RF or ACPA (3 points) - IU values ≥3x ULN
       - Highest score is used when both tests are positive
    
    3. Acute-phase Reactants (0-1 point):
       - Both CRP and ESR normal (0 points)
       - Either CRP or ESR abnormal (1 point)
    
    4. Duration of Symptoms (0-1 point):
       - <6 weeks (0 points)
       - ≥6 weeks (1 point)
    
    Prerequisites:
    - At least one swollen joint
    - No better explanation for synovitis
    - At least one serology test result available
    - At least one acute-phase reactant test result available
    
    Large joints: shoulders, elbows, hips, knees, ankles
    Small joints: MCPs, PIPs, thumb IPs, wrists, MTPs (excluding DIP joints and 1st MCP/MTP)
    
    References (Vancouver style):
    1. Aletaha D, Neogi T, Silman AJ, et al. 2010 Rheumatoid arthritis classification 
    criteria: an American College of Rheumatology/European League Against Rheumatism 
    collaborative initiative. Arthritis Rheum. 2010;62(9):2569-81.
    2. Aletaha D, Neogi T, Silman AJ, et al. 2010 rheumatoid arthritis classification 
    criteria: an American College of Rheumatology/European League Against Rheumatism 
    collaborative initiative. Ann Rheum Dis. 2010;69(9):1580-8.
    """
    
    joint_involvement: Literal[
        "1_large", 
        "2_to_10_large", 
        "1_to_3_small", 
        "4_to_10_small", 
        "more_than_10_small"
    ] = Field(
        ...,
        description="Joint involvement pattern based on swollen/tender joints on examination. Large joints: shoulders, elbows, hips, knees, ankles. Small joints: MCPs, PIPs, thumb IPs, wrists, MTPs (excluding DIP joints and 1st MCP/MTP). Select the option that assigns the most possible points.",
        example="1_to_3_small"
    )
    
    rf_status: Literal["negative", "low_positive", "high_positive"] = Field(
        ...,
        description="Rheumatoid factor (RF) test result. Negative: ≤ULN per lab/assay. Low-positive: >ULN but <3x ULN. High-positive: ≥3x ULN. If RF reported only as positive/negative, positive result should be scored as low-positive.",
        example="negative"
    )
    
    acpa_status: Literal["negative", "low_positive", "high_positive"] = Field(
        ...,
        description="Anti-citrullinated protein antibody (ACPA) test result. Negative: ≤ULN per lab/assay. Low-positive: >ULN but <3x ULN. High-positive: ≥3x ULN.",
        example="high_positive"
    )
    
    crp_status: Literal["normal", "abnormal"] = Field(
        ...,
        description="C-reactive protein (CRP) test result according to laboratory reference ranges.",
        example="abnormal"
    )
    
    esr_status: Literal["normal", "abnormal"] = Field(
        ...,
        description="Erythrocyte sedimentation rate (ESR) test result according to laboratory reference ranges.",
        example="normal"
    )
    
    symptom_duration: Literal["less_than_6_weeks", "6_weeks_or_more"] = Field(
        ...,
        description="Duration of synovitis signs/symptoms (pain, swelling, tenderness) in joints clinically involved at the time of assessment, based on patient self-report, regardless of treatment status.",
        example="6_weeks_or_more"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "joint_involvement": "1_to_3_small",
                "rf_status": "negative",
                "acpa_status": "high_positive",
                "crp_status": "abnormal",
                "esr_status": "normal",
                "symptom_duration": "6_weeks_or_more"
            }
        }


class AcrEular2010RaResponse(BaseModel):
    """
    Response model for ACR/EULAR 2010 Rheumatoid Arthritis Classification Criteria
    
    The ACR/EULAR 2010 score ranges from 0-10 points and classifies patients as:
    - Score <6 points: Does not meet criteria for RA classification
    - Score ≥6 points: Meets criteria for definite RA classification
    
    The criteria were developed to identify patients with early RA who would benefit 
    from DMARD therapy before irreversible joint damage occurs. A score ≥6 indicates 
    the patient has definite RA and should be considered for early therapeutic intervention.
    
    Reference: Aletaha D, et al. Arthritis Rheum. 2010;62(9):2569-81.
    """
    
    result: int = Field(
        ...,
        description="ACR/EULAR 2010 classification score calculated from clinical and laboratory variables (range: 0-10 points)",
        example=6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on the score",
        example="Score 6/10 points. Meets ACR/EULAR 2010 classification criteria for rheumatoid arthritis. Consider early DMARD therapy initiation."
    )
    
    stage: str = Field(
        ...,
        description="Classification result (Non-RA, Definite RA)",
        example="Definite RA"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the classification result",
        example="Meets classification criteria"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": "Score 6/10 points. Meets ACR/EULAR 2010 classification criteria for rheumatoid arthritis. Consider early DMARD therapy initiation.",
                "stage": "Definite RA",
                "stage_description": "Meets classification criteria"
            }
        }