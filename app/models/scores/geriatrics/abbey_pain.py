"""
AbbeyPain calculation models
"""

from pydantic import BaseModel, Field

# Abbey Pain Scale Models
class AbbeyPainRequest(BaseModel):
    """
    Request model for Abbey Pain Scale calculation
    
    The Abbey Pain Scale is a validated tool for assessing pain in people with dementia
    who cannot verbally communicate their pain experience.
    
    **Clinical Use**:
    - Pain assessment in dementia patients
    - Non-verbal pain evaluation
    - Monitoring pain management effectiveness
    - Care planning in aged care facilities
    - Quality of life assessment
    - Medication adjustment guidance
    
    **Assessment Domains**:
    1. Vocalization (whimpering, groaning, crying)
    2. Facial expression (grimacing, frowning, distorted expressions)
    3. Body language (guarding, rigidity, fidgeting, withdrawal)
    4. Behavioral change (increased confusion, refusing food, alteration in usual patterns)
    5. Physiological change (temperature, pulse, blood pressure changes, perspiring, flushing/pallor)
    6. Physical change (skin tears, pressure areas, arthritis, contractures, previous injuries)
    
    **Scoring**: Each domain scored 0-3 (0=absent, 1=mild, 2=moderate, 3=severe)
    
    **Reference**: Abbey J, et al. The Abbey pain scale: a 1-minute numerical indicator for people with end-stage dementia. Int J Palliat Nurs. 2004;10(1):6-13.
    """
    vocalization: int = Field(
        ..., 
        ge=0, 
        le=3, 
        description="Vocalization assessment (0=absent, 1=occasional moaning/groaning, 2=repeated calling out/noisy breathing, 3=loud moaning/crying/distressed sounds). Includes whimpering, groaning, crying.",
        example=1
    )
    facial_expression: int = Field(
        ..., 
        ge=0, 
        le=3, 
        description="Facial expression assessment (0=serene/peaceful, 1=sad/frightened/frown, 2=facial grimacing, 3=facial grimacing with jaw clenching). Look for grimacing, frowning, distorted expressions.",
        example=2
    )
    body_language: int = Field(
        ..., 
        ge=0, 
        le=3, 
        description="Body language assessment (0=relaxed, 1=tense/distressed pacing/fidgeting, 2=rigid/fists clenched/knees pulled up/pulling away, 3=rigid/fists clenched/knees pulled up/striking out). Includes guarding, rigidity, withdrawal.",
        example=1
    )
    behavioral_change: int = Field(
        ..., 
        ge=0, 
        le=3, 
        description="Behavioral change assessment (0=no change, 1=increase in confusion/refusing medication, 2=alteration in behavior patterns/aggressive/withdrawn, 3=crying/increased confusion/agitation). Changes from usual patterns.",
        example=0
    )
    physiological_change: int = Field(
        ..., 
        ge=0, 
        le=3, 
        description="Physiological change assessment (0=no change, 1=pale/flushed/diaphoretic, 2=breathing changes/hyperventilation, 3=fever/blood pressure changes). Temperature, pulse, BP changes, perspiring, flushing/pallor.",
        example=1
    )
    physical_change: int = Field(
        ..., 
        ge=0, 
        le=3, 
        description="Physical change assessment (0=no physical changes, 1=skin tears/pressure sores/lesions/cuts/bruises, 2=limping/arthritis/contractures, 3=previous injuries/surgery). Skin tears, pressure areas, arthritis, contractures.",
        example=0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "vocalization": 1,
                "facial_expression": 2,
                "body_language": 1,
                "behavioral_change": 0,
                "physiological_change": 1,
                "physical_change": 0
            }
        }


class AbbeyPainResponse(BaseModel):
    """
    Response model for Abbey Pain Scale calculation
    
    Provides comprehensive pain assessment for dementia patients with evidence-based
    interpretation and management recommendations.
    
    **Pain Classification**:
    - Score 0-2: No pain - continue routine monitoring
    - Score 3-7: Mild pain - consider non-pharmacological interventions
    - Score 8-13: Moderate pain - analgesics and non-pharmacological approaches
    - Score 14-18: Severe pain - immediate pain management, consider specialist referral
    
    **Management Strategies**:
    - Non-pharmacological: repositioning, comfort measures, environmental modifications
    - Mild pain: paracetamol, topical analgesics, heat/cold therapy
    - Moderate pain: regular analgesics, consider opioids for breakthrough pain
    - Severe pain: regular opioids, specialist pain management consultation
    
    **Monitoring Recommendations**:
    - Reassess after interventions (15-30 minutes for medications)
    - Document response to treatments
    - Regular reassessment (every 4-8 hours or as needed)
    """
    result: int = Field(
        ..., 
        description="Total Abbey Pain Scale score ranging from 0-18 points. Higher scores indicate more severe pain requiring more intensive management.",
        example=5
    )
    unit: str = Field(
        ..., 
        description="Unit of the score result",
        example="points"
    )
    interpretation: str = Field(
        ..., 
        description="Evidence-based interpretation of pain intensity with specific management recommendations appropriate for dementia care settings.",
        example="Mild pain present. Monitor and consider non-pharmacological interventions."
    )
    stage: str = Field(
        ..., 
        description="Pain intensity classification (No Pain, Mild Pain, Moderate Pain, Severe Pain)",
        example="Mild Pain"
    )
    stage_description: str = Field(
        ..., 
        description="Description of the pain intensity level with clinical implications",
        example="Mild pain"
    )
    pain_present: bool = Field(
        ..., 
        description="Boolean indicator of whether clinically significant pain is present (typically score ≥3 indicates pain presence).",
        example=True
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5,
                "unit": "points",
                "interpretation": "Mild pain present. Monitor and consider non-pharmacological interventions.",
                "stage": "Mild Pain",
                "stage_description": "Mild pain",
                "pain_present": True
            }
        }