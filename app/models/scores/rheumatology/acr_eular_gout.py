"""
ACR/EULAR Gout Classification Criteria Models

Request and response models for ACR/EULAR gout classification criteria calculation.

References (Vancouver style):
1. Neogi T, Jansen TL, Dalbeth N, Fransen J, Schumacher HR, Berendsen D, Brown M, 
   Choi H, Edwards NL, Janssens HJ, Liote F, Naden RP, Nuki G, Ogdie A, Perez-Ruiz F, 
   Saag K, Singh JA, Sundy JS, Tausche AK, Vaquez-Mellado J, Yarows SA, Taylor WJ. 
   2015 Gout classification criteria: an American College of Rheumatology/European 
   League Against Rheumatism collaborative initiative. Ann Rheum Dis. 2015 Oct;74(10):1789-98. 
   doi: 10.1136/annrheumdis-2015-208237.

2. Taylor WJ, Fransen J, Jansen TL, Dalbeth N, Schumacher HR, Brown M, Louthrenoo W, 
   Vazquez-Mellado J, Eliseev M, McCarthy G, Stamp LK, Perez-Ruiz F, Nuki G, Bardin T, 
   Uhlig T, Kalra S, Sundy JS, Yarows S, Becce F, Cavagna L, Jatuworapruk K, Lioté F, 
   Pineda C, Chua J, Tausche AK, Christensen R, Gibson T, Gout Classification Criteria 
   Consortium, Ogdie A, Neogi T. Study for Updated Gout Classification Criteria: 
   identification of features to classify gout. Arthritis Care Res (Hoboken). 2015 Sep;67(9):1304-15. 
   doi: 10.1002/acr.22585.

The ACR/EULAR 2015 gout classification criteria use a 3-step approach for gout classification:

Step 1 - Entry Criterion: At least one episode of swelling, pain, or tenderness in a 
peripheral joint or bursa must be present to proceed.

Step 2 - Sufficient Criterion: If monosodium urate (MSU) crystals are identified in a 
symptomatic joint, bursa, or tophus by polarized light microscopy, the diagnosis is 
definite gout.

Step 3 - Classification Criteria: If MSU crystals are not identified or synovial fluid 
analysis was not performed, a scoring system is used. A total score ≥7 points indicates 
classification as gout.

The classification criteria scoring domains include:
- Pattern of joint/bursa involvement (0-2 points)
- Characteristics of symptomatic episodes (0-3 points)  
- Time course of symptomatic episodes (0-2 points)
- Evidence of tophus (0 or 4 points)
- Serum urate levels (-4 to +4 points)
- Synovial fluid analysis (-2 or 0 points)
- Imaging evidence of urate deposition (0 or 4 points)
- Imaging evidence of gout-related joint damage (0 or 4 points)

These criteria were developed to enable early identification and classification of gout 
for clinical and research purposes, with high sensitivity and specificity when used 
appropriately.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AcrEularGoutRequest(BaseModel):
    """
    Request model for ACR/EULAR Gout Classification Criteria
    
    The ACR/EULAR 2015 gout classification criteria use a systematic 3-step approach:
    
    Step 1 - Entry Criterion:
    At least one episode of swelling, pain, or tenderness in a peripheral joint or bursa
    
    Step 2 - Sufficient Criterion:
    Presence of monosodium urate (MSU) crystals in symptomatic joint/bursa/tophus = definite gout
    
    Step 3 - Classification Criteria (if MSU crystals not identified):
    Scoring system across 8 domains, requiring ≥7 points for gout classification:
    
    1. Pattern of joint/bursa involvement (0-2 points):
       - other_joint: Joint/bursa other than ankle, midfoot, or 1st MTP (0 points)
       - ankle_midfoot: Ankle OR midfoot as part of mono/oligoarticular episode without 1st MTP (1 point)
       - first_mtp: 1st MTP as part of mono/oligoarticular episode (2 points)
    
    2. Characteristics of symptomatic episodes (0-3 points):
       Based on presence of: erythema overlying joint, can't bear touch/pressure, great difficulty walking
       - none: No characteristics (0 points)
       - one: One characteristic (1 point)
       - two: Two characteristics (2 points)
       - three: Three characteristics (3 points)
    
    3. Time course of symptomatic episodes (0-2 points):
       Episodes with ≥2 of: time to max pain <24h, resolution ≤14 days, complete resolution between episodes
       - none: No typical episodes (0 points)
       - one: One typical episode (1 point)
       - recurrent: Recurrent typical episodes (2 points)
    
    4. Evidence of tophus (0 or 4 points):
       Draining or chalk-like subcutaneous nodule in typical locations
       - absent: No tophus (0 points)
       - present: Tophus present (4 points)
    
    5. Serum urate (-4 to +4 points):
       Measured by uricase method, ideally when not on urate-lowering therapy and >4 weeks from episode
       - under_4: <4 mg/dL [<0.24 mM] (-4 points)
       - 4_to_6: ≥4 to <6 mg/dL [≥0.24 to <0.36 mM] (0 points)
       - 6_to_8: ≥6 to <8 mg/dL [≥0.36 to <0.48 mM] (2 points)
       - 8_to_10: ≥8 to <10 mg/dL [≥0.48 to <0.60 mM] (3 points)
       - over_10: ≥10 mg/dL [≥0.60 mM] (4 points)
    
    6. Synovial fluid analysis (-2 or 0 points):
       Should be assessed by trained observer
       - negative_msu: Negative for MSU crystals (-2 points)
       - not_done: Analysis not performed (0 points)
    
    7. Imaging evidence of urate deposition (0 or 4 points):
       Ultrasound double-contour sign OR DECT demonstration of urate deposition
       - absent: No evidence or not done (0 points)
       - present: Evidence present (4 points)
    
    8. Imaging evidence of gout-related joint damage (0 or 4 points):
       X-ray of hands or feet with ≥1 erosion
       - absent: No erosions (0 points)
       - present: ≥1 erosion present (4 points)
    
    References (Vancouver style):
    1. Neogi T, Jansen TL, Dalbeth N, et al. 2015 Gout classification criteria: an American 
    College of Rheumatology/European League Against Rheumatism collaborative initiative. 
    Ann Rheum Dis. 2015;74(10):1789-98.
    2. Taylor WJ, Fransen J, Jansen TL, et al. Study for Updated Gout Classification Criteria: 
    identification of features to classify gout. Arthritis Care Res (Hoboken). 2015;67(9):1304-15.
    """
    
    entry_criterion: Literal["yes", "no"] = Field(
        ...,
        description="Entry criterion: ≥1 episode of swelling, pain, or tenderness in a peripheral joint or bursa. Must be 'yes' to proceed with classification.",
        example="yes"
    )
    
    msu_crystals_present: Literal["yes", "no", "not_tested"] = Field(
        ...,
        description="Sufficient criterion: Presence of monosodium urate (MSU) crystals in symptomatic joint, bursa, or tophus by polarized light microscopy. If 'yes', diagnosis is definite gout.",
        example="not_tested"
    )
    
    joint_pattern: Literal["other_joint", "ankle_midfoot", "first_mtp"] = Field(
        ...,
        description="Pattern of joint/bursa involvement during symptomatic episodes. other_joint (0 pts): joints other than ankle/midfoot/1st MTP. ankle_midfoot (1 pt): ankle OR midfoot without 1st MTP involvement. first_mtp (2 pts): 1st metatarsophalangeal joint involvement.",
        example="first_mtp"
    )
    
    episode_characteristics: Literal["none", "one", "two", "three"] = Field(
        ...,
        description="Number of characteristics during symptomatic episodes: (1) erythema overlying affected joint, (2) can't bear touch or pressure to joint, (3) great difficulty with walking or inability to use joint. Count how many of these three are present.",
        example="three"
    )
    
    typical_episodes: Literal["none", "one", "recurrent"] = Field(
        ...,
        description="Number of episodes with typical time-course having ≥2 of: (1) time to maximal pain <24 hours, (2) resolution of symptoms in ≤14 days, (3) complete resolution between episodes. none (0 pts), one (1 pt), recurrent (2 pts).",
        example="recurrent"
    )
    
    tophus_evidence: Literal["absent", "present"] = Field(
        ...,
        description="Evidence of tophus: draining or chalk-like subcutaneous nodule located in typical locations (joints, ears, olecranon bursae, finger pads, tendons such as Achilles). absent (0 pts), present (4 pts).",
        example="absent"
    )
    
    serum_urate: Literal["under_4", "4_to_6", "6_to_8", "8_to_10", "over_10"] = Field(
        ...,
        description="Serum urate level measured by uricase method. Ideally measured when not taking urate-lowering treatment and >4 weeks from acute episode. Use highest value regardless of timing. under_4: <4 mg/dL (-4 pts), 4_to_6: 4-6 mg/dL (0 pts), 6_to_8: 6-8 mg/dL (2 pts), 8_to_10: 8-10 mg/dL (3 pts), over_10: ≥10 mg/dL (4 pts).",
        example="8_to_10"
    )
    
    synovial_fluid_analysis: Literal["negative_msu", "not_done"] = Field(
        ...,
        description="Synovial fluid analysis of symptomatic joint or bursa, assessed by trained observer. negative_msu: MSU crystals not identified (-2 pts), not_done: analysis not performed (0 pts). Note: if MSU crystals are positive, this should be indicated in msu_crystals_present field instead.",
        example="not_done"
    )
    
    imaging_urate_deposition: Literal["absent", "present"] = Field(
        ...,
        description="Imaging evidence of urate deposition in symptomatic joint/bursa. Ultrasound showing double-contour sign OR dual-energy CT (DECT) demonstrating urate deposition. absent (0 pts), present (4 pts).",
        example="absent"
    )
    
    imaging_joint_damage: Literal["absent", "present"] = Field(
        ...,
        description="Imaging evidence of gout-related joint damage. X-ray of hands or feet showing ≥1 erosion. absent (0 pts), present (4 pts).",
        example="absent"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "entry_criterion": "yes",
                "msu_crystals_present": "not_tested",
                "joint_pattern": "first_mtp",
                "episode_characteristics": "three",
                "typical_episodes": "recurrent",
                "tophus_evidence": "absent",
                "serum_urate": "8_to_10",
                "synovial_fluid_analysis": "not_done",
                "imaging_urate_deposition": "absent",
                "imaging_joint_damage": "absent"
            }
        }


class AcrEularGoutResponse(BaseModel):
    """
    Response model for ACR/EULAR Gout Classification Criteria
    
    The ACR/EULAR 2015 gout classification provides three possible outcomes:
    
    1. Entry criterion not met: Patient does not have ≥1 episode of peripheral joint/bursa 
       swelling, pain, or tenderness
    
    2. Definite gout: MSU crystals identified in symptomatic joint, bursa, or tophus 
       (sufficient criterion met)
    
    3. Classification criteria result: Score-based classification when MSU crystals not 
       identified or not tested:
       - Score ≥7 points: Meets criteria for gout classification
       - Score <7 points: Does not meet criteria for gout classification
    
    The classification criteria scoring ranges from -6 to +23 points across 8 domains.
    This scoring system has demonstrated high sensitivity (85%) and specificity (78%) 
    for gout classification in clinical studies.
    
    Reference: Neogi T, et al. Ann Rheum Dis. 2015;74(10):1789-98.
    """
    
    result: str = Field(
        ...,
        description="Classification result: entry criterion status, definite gout if MSU crystals present, or score-based classification result",
        example="Score 7/23 points"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with recommended next steps based on the classification result",
        example="Score 7/23 points. Meets ACR/EULAR 2015 classification criteria for gout. Diagnosis consistent with gout. Consider appropriate urate-lowering therapy and management of acute attacks."
    )
    
    stage: str = Field(
        ...,
        description="Classification stage (Entry criterion not met, Definite gout, Meets criteria for gout, Does not meet criteria)",
        example="Meets criteria for gout"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the classification stage",
        example="Meets gout classification criteria"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Score 7/23 points",
                "unit": "points",
                "interpretation": "Score 7/23 points. Meets ACR/EULAR 2015 classification criteria for gout. Diagnosis consistent with gout. Consider appropriate urate-lowering therapy and management of acute attacks.",
                "stage": "Meets criteria for gout",
                "stage_description": "Meets gout classification criteria"
            }
        }