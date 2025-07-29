"""
ASAS Criteria for Peripheral SpondyloArthritis (SpA) Models

Request and response models for ASAS Criteria for Peripheral SpondyloArthritis calculation.

References (Vancouver style):
1. Rudwaleit M, van der Heijde D, Landewé R, Listing J, Akkoc N, Brandt J, et al. 
   The Assessment of SpondyloArthritis International Society classification criteria 
   for peripheral spondyloarthritis and for spondyloarthritis in general. 
   Ann Rheum Dis. 2011 Jan;70(1):25-31. doi: 10.1136/ard.2010.133645.
2. Sieper J, Rudwaleit M, Baraliakos X, Brandt J, Braun J, Burgos-Vargas R, et al. 
   The Assessment of SpondyloArthritis international Society (ASAS) handbook: 
   a guide to assess spondyloarthritis. Ann Rheum Dis. 2009;68 Suppl 2:ii1-44. 
   doi: 10.1136/ard.2008.104018.

The ASAS criteria for peripheral SpA are intended for patients with predominant 
peripheral manifestations including peripheral arthritis, enthesitis, and dactylitis. 
The criteria require an entry criterion (at least one of arthritis, enthesitis, or 
dactylitis) plus additional SpA features from two groups:

Group A (need ≥1): psoriasis, inflammatory bowel disease, preceding infection, 
HLA-B27, uveitis, sacroiliitis on imaging

Group B (need ≥2): arthritis, enthesitis, dactylitis, inflammatory back pain 
in the past, family history of SpA

Classification requires entry criterion PLUS either ≥1 Group A feature OR ≥2 Group B features.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AsasPeripheralSpaCriteriaRequest(BaseModel):
    """
    Request model for ASAS Criteria for Peripheral SpondyloArthritis (SpA)
    
    The ASAS criteria for peripheral SpA classify patients with predominant peripheral 
    manifestations. Entry criterion requires at least one of: arthritis, enthesitis, 
    or dactylitis.
    
    Classification Features:
    
    Entry Criterion (at least one required):
    - Peripheral arthritis: Usually predominantly lower limbs and/or asymmetric arthritis
    - Enthesitis: Clinically assessed inflammation at tendon/ligament insertion sites
    - Dactylitis: Clinically assessed "sausage digit" swelling of entire finger or toe
    
    Group A Features (≥1 required for classification):
    - Psoriasis: Past or present psoriasis diagnosed by a doctor
    - Inflammatory bowel disease: Past or present Crohn's or ulcerative colitis
    - Preceding infection: Urethritis/cervicitis or diarrhea within 1 month before arthritis
    - HLA-B27: Positive testing according to standard laboratory techniques
    - Uveitis anterior: Past or present anterior uveitis confirmed by ophthalmologist
    - Sacroiliitis on imaging: Bilateral grade 2-4 or unilateral grade 3-4 on X-rays OR active sacroiliitis on MRI
    
    Group B Features (≥2 required for classification):
    - Arthritis: As defined in entry criterion
    - Enthesitis: As defined in entry criterion  
    - Dactylitis: As defined in entry criterion
    - Inflammatory back pain past: History of inflammatory back pain
    - Family history SpA: First/second-degree relatives with AS, psoriasis, uveitis, reactive arthritis, or IBD
    
    Classification: Entry criterion + (≥1 Group A feature OR ≥2 Group B features)
    
    References (Vancouver style):
    1. Rudwaleit M, van der Heijde D, Landewé R, Listing J, Akkoc N, Brandt J, et al. 
    The Assessment of SpondyloArthritis International Society classification criteria 
    for peripheral spondyloarthritis and for spondyloarthritis in general. 
    Ann Rheum Dis. 2011 Jan;70(1):25-31. doi: 10.1136/ard.2010.133645.
    2. Sieper J, Rudwaleit M, Baraliakos X, Brandt J, Braun J, Burgos-Vargas R, et al. 
    The Assessment of SpondyloArthritis international Society (ASAS) handbook: 
    a guide to assess spondyloarthritis. Ann Rheum Dis. 2009;68 Suppl 2:ii1-44. 
    doi: 10.1136/ard.2008.104018.
    """
    
    peripheral_arthritis: Literal["yes", "no"] = Field(
        ...,
        description="Peripheral arthritis present (usually predominantly lower limbs and/or asymmetric arthritis)",
        example="yes"
    )
    
    enthesitis: Literal["yes", "no"] = Field(
        ...,
        description="Enthesitis present (clinically assessed inflammation at tendon/ligament insertion sites)",
        example="no"
    )
    
    dactylitis: Literal["yes", "no"] = Field(
        ...,
        description="Dactylitis present (clinically assessed 'sausage digit' swelling of entire finger or toe)",
        example="no"
    )
    
    psoriasis: Literal["yes", "no"] = Field(
        ...,
        description="Past or present psoriasis diagnosed by a doctor",
        example="yes"
    )
    
    inflammatory_bowel_disease: Literal["yes", "no"] = Field(
        ...,
        description="Past or present Crohn's disease or ulcerative colitis diagnosed by a doctor",
        example="no"
    )
    
    preceding_infection: Literal["yes", "no"] = Field(
        ...,
        description="Preceding infection: urethritis/cervicitis or diarrhea within 1 month before arthritis onset",
        example="no"
    )
    
    hla_b27: Literal["yes", "no"] = Field(
        ...,
        description="HLA-B27 positive testing according to standard laboratory techniques",
        example="no"
    )
    
    uveitis_anterior: Literal["yes", "no"] = Field(
        ...,
        description="Past or present anterior uveitis confirmed by an ophthalmologist",
        example="no"
    )
    
    sacroiliitis_imaging: Literal["yes", "no"] = Field(
        ...,
        description="Sacroiliitis on imaging: bilateral grade 2-4 or unilateral grade 3-4 on X-rays OR active sacroiliitis on MRI according to ASAS definition",
        example="no"
    )
    
    inflammatory_back_pain_past: Literal["yes", "no"] = Field(
        ...,
        description="History of inflammatory back pain in the past",
        example="no"
    )
    
    family_history_spa: Literal["yes", "no"] = Field(
        ...,
        description="Family history of spondyloarthritis: presence in first or second-degree relatives of ankylosing spondylitis, psoriasis, uveitis, reactive arthritis, or inflammatory bowel disease",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "peripheral_arthritis": "yes",
                "enthesitis": "no",
                "dactylitis": "no",
                "psoriasis": "yes",
                "inflammatory_bowel_disease": "no",
                "preceding_infection": "no",
                "hla_b27": "no",
                "uveitis_anterior": "no",
                "sacroiliitis_imaging": "no",
                "inflammatory_back_pain_past": "no",
                "family_history_spa": "no"
            }
        }


class AsasPeripheralSpaCriteriaResponse(BaseModel):
    """
    Response model for ASAS Criteria for Peripheral SpondyloArthritis (SpA)
    
    The ASAS criteria classify patients with peripheral SpA based on:
    - Entry criterion: arthritis and/or enthesitis and/or dactylitis
    - Plus either ≥1 Group A feature OR ≥2 Group B features
    
    Group A features: psoriasis, IBD, preceding infection, HLA-B27, uveitis, sacroiliitis
    Group B features: arthritis, enthesitis, dactylitis, IBP past, family history SpA
    
    Sensitivity: 77.8%, Specificity: 82.9%
    
    Reference: Rudwaleit M, et al. Ann Rheum Dis. 2011;70(1):25-31.
    """
    
    result: str = Field(
        ...,
        description="Classification result: 'Peripheral SpA Criteria Met' or 'Peripheral SpA Criteria NOT Met'",
        example="Peripheral SpA Criteria Met"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for classification criteria)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and explanation of the classification result",
        example="Patient meets the ASAS classification criteria for peripheral spondyloarthritis. Entry criterion (arthritis and/or enthesitis and/or dactylitis) is fulfilled. Group A pathway satisfied: 1 Group A feature(s) present (≥1 required). Group B features: 1/5. Note: These are classification criteria for research purposes, not diagnostic criteria for clinical practice."
    )
    
    stage: str = Field(
        ...,
        description="Classification stage or status",
        example="Criteria fulfilled"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the classification stage",
        example="Meets ASAS criteria for peripheral spondyloarthritis"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Peripheral SpA Criteria Met",
                "unit": "",
                "interpretation": "Patient meets the ASAS classification criteria for peripheral spondyloarthritis. Entry criterion (arthritis and/or enthesitis and/or dactylitis) is fulfilled. Group A pathway satisfied: 1 Group A feature(s) present (≥1 required). Group B features: 1/5. Note: These are classification criteria for research purposes, not diagnostic criteria for clinical practice.",
                "stage": "Criteria fulfilled",
                "stage_description": "Meets ASAS criteria for peripheral spondyloarthritis"
            }
        }
