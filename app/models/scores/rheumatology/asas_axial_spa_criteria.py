"""
ASAS Criteria for Axial Spondyloarthritis (SpA) Models

Request and response models for ASAS criteria classification.

References (Vancouver style):
1. Rudwaleit M, van der Heijde D, Landewé R, Listing J, Akkoc N, Brandt J, et al. 
   The development of Assessment of SpondyloArthritis international Society 
   classification criteria for axial spondyloarthritis (part II): validation and 
   final selection. Ann Rheum Dis. 2009;68(6):777-83.
2. Sieper J, Rudwaleit M, Baraliakos X, Brandt J, Braun J, Burgos-Vargas R, et al. 
   The Assessment of SpondyloArthritis international Society (ASAS) handbook: 
   a guide to assess spondyloarthritis. Ann Rheum Dis. 2009;68 Suppl 2:ii1-44.
3. Sieper J, van der Heijde D, Landewé R, Brandt J, Burgos-Vargas R, Collantes-Estevez E, 
   et al. New criteria for inflammatory back pain in patients with chronic back pain: 
   a real patient exercise by experts from the Assessment of SpondyloArthritis 
   International Society (ASAS). Ann Rheum Dis. 2009;68(6):784-8.

The ASAS classification criteria for axial spondyloarthritis allow for early diagnosis 
by incorporating both clinical and imaging features. The criteria require an entry 
criterion of chronic back pain ≥3 months with age at onset <45 years, followed by 
either the imaging arm (sacroiliitis + ≥1 SpA feature) or clinical arm (HLA-B27 + 
≥2 SpA features).

Entry Criterion:
- Back pain ≥3 months AND age at onset <45 years

Classification Arms:
1. Imaging arm: Sacroiliitis on imaging + ≥1 SpA feature
2. Clinical arm: HLA-B27 positive + ≥2 SpA features

SpA features include:
- Inflammatory back pain (4/5 ASAS criteria: age onset <40y, insidious onset, 
  improvement with exercise, no improvement with rest, pain at night)
- Arthritis (past/present active synovitis)
- Enthesitis (heel enthesitis)
- Uveitis (past/present anterior uveitis)
- Dactylitis (past/present dactylitis)
- Psoriasis (past/present psoriasis)
- Inflammatory bowel disease (Crohn's/colitis)
- Good response to NSAIDs (24-48h resolution)
- Family history (SpA, psoriasis, uveitis, reactive arthritis, IBD)
- Elevated CRP (excluding other causes)
"""

from pydantic import BaseModel, Field
from typing import Literal


class AsasAxialSpaCriteriaRequest(BaseModel):
    """
    Request model for ASAS Criteria for Axial Spondyloarthritis (SpA)
    
    The ASAS classification criteria allow for early diagnosis of axial spondyloarthritis
    by incorporating both clinical and imaging features. These are classification criteria,
    not diagnostic criteria, and should be applied in patients with chronic back pain.
    
    Entry Criterion (mandatory):
    - Back pain ≥3 months AND age at onset <45 years
    
    If entry criterion is met, classification follows two arms:
    
    Imaging arm: Sacroiliitis on imaging + ≥1 SpA feature
    Clinical arm: HLA-B27 positive + ≥2 SpA features
    
    References (Vancouver style):
    1. Rudwaleit M, van der Heijde D, Landewé R, Listing J, Akkoc N, Brandt J, et al. 
       The development of Assessment of SpondyloArthritis international Society 
       classification criteria for axial spondyloarthritis (part II): validation and 
       final selection. Ann Rheum Dis. 2009;68(6):777-83.
    2. Sieper J, Rudwaleit M, Baraliakos X, Brandt J, Braun J, Burgos-Vargas R, et al. 
       The Assessment of SpondyloArthritis international Society (ASAS) handbook: 
       a guide to assess spondyloarthritis. Ann Rheum Dis. 2009;68 Suppl 2:ii1-44.
    """
    
    back_pain_duration_months: int = Field(
        ...,
        description="Duration of back pain in months (≥3 months required for entry criterion)",
        ge=0,
        le=1200,
        example=6
    )
    
    age_at_onset: int = Field(
        ...,
        description="Age at onset of back pain in years (<45 years required for entry criterion)",
        ge=0,
        le=100,
        example=28
    )
    
    sacroiliitis_imaging: Literal["present", "absent"] = Field(
        ...,
        description="Sacroiliitis on imaging. Present: X-ray (bilateral grade 2-4 or unilateral grade 3-4) or MRI (active inflammatory lesions suggestive of sacroiliitis associated with SpA)",
        example="present"
    )
    
    hla_b27_positive: Literal["yes", "no"] = Field(
        ...,
        description="HLA-B27 positive according to standard laboratory techniques. Required for clinical arm classification",
        example="yes"
    )
    
    inflammatory_back_pain: Literal["yes", "no"] = Field(
        ...,
        description="Inflammatory back pain according to ASAS experts: 4 out of 5 criteria (age at onset <40 years, insidious onset, improvement with exercise, no improvement with rest, pain at night with improvement upon getting up)",
        example="yes"
    )
    
    arthritis: Literal["yes", "no"] = Field(
        ...,
        description="Past or present active synovitis diagnosed by a doctor (peripheral or axial joints)",
        example="no"
    )
    
    enthesitis: Literal["yes", "no"] = Field(
        ...,
        description="Heel enthesitis: past or present spontaneous pain or tenderness at examination at the site of the insertion of the Achilles tendon or plantar fascia at the calcaneus",
        example="no"
    )
    
    uveitis: Literal["yes", "no"] = Field(
        ...,
        description="Past or present anterior uveitis confirmed by an ophthalmologist (not posterior uveitis)",
        example="no"
    )
    
    dactylitis: Literal["yes", "no"] = Field(
        ...,
        description="Past or present dactylitis (sausage-like swelling of digits) diagnosed by a doctor",
        example="no"
    )
    
    psoriasis: Literal["yes", "no"] = Field(
        ...,
        description="Past or present psoriasis diagnosed by a doctor (any type of psoriasis)",
        example="no"
    )
    
    crohns_colitis: Literal["yes", "no"] = Field(
        ...,
        description="Past or present Crohn's disease or ulcerative colitis diagnosed by a doctor",
        example="no"
    )
    
    good_response_nsaids: Literal["yes", "no"] = Field(
        ...,
        description="Good response to NSAIDs: at 24-48h after a full dose of NSAID the back pain is not present anymore or much better",
        example="yes"
    )
    
    family_history: Literal["yes", "no"] = Field(
        ...,
        description="Family history: presence in first-degree or second-degree relatives of ankylosing spondylitis, psoriasis, uveitis, reactive arthritis, or inflammatory bowel disease",
        example="no"
    )
    
    elevated_crp: Literal["yes", "no"] = Field(
        ...,
        description="CRP above upper normal limit in the presence of back pain, after exclusion of other causes for elevated CRP concentration",
        example="yes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "back_pain_duration_months": 6,
                "age_at_onset": 28,
                "sacroiliitis_imaging": "present",
                "hla_b27_positive": "yes",
                "inflammatory_back_pain": "yes",
                "arthritis": "no",
                "enthesitis": "no",
                "uveitis": "no",
                "dactylitis": "no",
                "psoriasis": "no",
                "crohns_colitis": "no",
                "good_response_nsaids": "yes",
                "family_history": "no",
                "elevated_crp": "yes"
            }
        }


class AsasAxialSpaCriteriaResponse(BaseModel):
    """
    Response model for ASAS Criteria for Axial Spondyloarthritis (SpA)
    
    The ASAS criteria classify patients into three possible outcomes:
    1. "Axial SpA" - Fulfills classification criteria
    2. "Not Axial SpA" - Does not fulfill classification criteria
    3. "Entry Criterion Not Met" - Entry criterion not fulfilled
    
    Entry criterion: Back pain ≥3 months AND age at onset <45 years
    
    If entry criterion met:
    - Imaging arm: Sacroiliitis + ≥1 SpA feature
    - Clinical arm: HLA-B27 + ≥2 SpA features
    
    Reference: Rudwaleit M, et al. Ann Rheum Dis. 2009;68(6):777-83.
    """
    
    result: str = Field(
        ...,
        description="Classification result according to ASAS criteria",
        example="Axial SpA"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for classification)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended next steps based on the classification",
        example="Patient fulfills the ASAS classification criteria for axial spondyloarthritis. Further rheumatological evaluation and appropriate treatment should be considered."
    )
    
    stage: str = Field(
        ...,
        description="Classification stage (Axial SpA, Not Axial SpA, or Entry Criterion Not Met)",
        example="Axial SpA"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the classification stage",
        example="Meets ASAS criteria for axial spondyloarthritis"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Axial SpA",
                "unit": "",
                "interpretation": "Patient fulfills the ASAS classification criteria for axial spondyloarthritis. Further rheumatological evaluation and appropriate treatment should be considered.",
                "stage": "Axial SpA",
                "stage_description": "Meets ASAS criteria for axial spondyloarthritis"
            }
        }
