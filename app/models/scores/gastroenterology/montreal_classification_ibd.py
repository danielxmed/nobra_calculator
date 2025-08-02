"""
Montreal Classification for Inflammatory Bowel Disease (IBD) Models

Request and response models for Montreal Classification IBD calculation.

References (Vancouver style):
1. Silverberg MS, Satsangi J, Ahmad T, Arnott ID, Bernstein CN, Brant SR, et al. 
   Toward an integrated clinical, molecular and serological classification of inflammatory 
   bowel disease: report of a Working Party of the 2005 Montreal World Congress of 
   Gastroenterology. Can J Gastroenterol. 2005;19 Suppl A:5A-36A. doi: 10.1155/2005/269076.
2. Satsangi J, Silverberg MS, Vermeire S, Colombel JF. The Montreal classification of 
   inflammatory bowel disease: controversies, consensus, and implications. Gut. 2006;55(6):749-53. 
   doi: 10.1136/gut.2005.082909.
3. Thia KT, Sandborn WJ, Harmsen WS, Zinsmeister AR, Loftus EV Jr. Risk factors associated 
   with progression to intestinal complications of Crohn's disease in a population-based cohort. 
   Gastroenterology. 2010;139(4):1147-55. doi: 10.1053/j.gastro.2010.06.070.

The Montreal Classification provides standardized phenotypic characterization of 
inflammatory bowel disease, replacing the Vienna Classification in 2005. It classifies 
IBD based on age at diagnosis, anatomical distribution (location/extent), and disease 
behavior/severity to guide clinical management and predict disease course.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Optional


class MontrealClassificationIbdRequest(BaseModel):
    """
    Request model for Montreal Classification for Inflammatory Bowel Disease (IBD)
    
    The Montreal Classification system provides standardized phenotypic characterization:
    
    Age Categories (both diseases):
    - A1: <17 years (pediatric onset)
    - A2: 17-40 years (young adult onset)
    - A3: >40 years (older adult onset)
    
    For Crohn's Disease:
    Location (L):
    - L1: Ileal (terminal ileum ± cecum)
    - L2: Colonic (any colonic location between cecum and rectum)
    - L3: Ileocolonic (terminal ileum + any colonic location)
    - L4: Upper GI (proximal to terminal ileum)
    
    Behavior (B):
    - B1: Inflammatory (non-stricturing, non-penetrating)
    - B2: Stricturing (intestinal stenosis)
    - B3: Penetrating (fistula, abscess, perforation)
    
    Perianal Modifier (p):
    - Can be added to any behavior (B1p, B2p, B3p)
    
    For Ulcerative Colitis:
    Extent (E):
    - E1: Proctitis (rectum only)
    - E2: Left-sided colitis (distal to splenic flexure)
    - E3: Extensive colitis (proximal to splenic flexure)
    
    Severity (S):
    - S0: Clinical remission
    - S1: Mild activity
    - S2: Moderate activity
    - S3: Severe activity
    
    Final Classification Examples:
    - Crohn's: A2L3B2p (young adult onset, ileocolonic, stricturing with perianal disease)
    - UC: A1E3S2 (pediatric onset, extensive colitis, moderate activity)

    References (Vancouver style):
    1. Silverberg MS, Satsangi J, Ahmad T, Arnott ID, Bernstein CN, Brant SR, et al. 
    Toward an integrated clinical, molecular and serological classification of inflammatory 
    bowel disease: report of a Working Party of the 2005 Montreal World Congress of 
    Gastroenterology. Can J Gastroenterol. 2005;19 Suppl A:5A-36A. doi: 10.1155/2005/269076.
    2. Satsangi J, Silverberg MS, Vermeire S, Colombel JF. The Montreal classification of 
    inflammatory bowel disease: controversies, consensus, and implications. Gut. 2006;55(6):749-53. 
    doi: 10.1136/gut.2005.082909.
    3. Thia KT, Sandborn WJ, Harmsen WS, Zinsmeister AR, Loftus EV Jr. Risk factors associated 
    with progression to intestinal complications of Crohn's disease in a population-based cohort. 
    Gastroenterology. 2010;139(4):1147-55. doi: 10.1053/j.gastro.2010.06.070.
    """
    
    disease_type: Literal["crohns_disease", "ulcerative_colitis"] = Field(
        ...,
        description="Type of inflammatory bowel disease to classify",
        example="crohns_disease"
    )
    
    age_at_diagnosis: int = Field(
        ...,
        ge=0,
        le=120,
        description="Age at diagnosis in years for Montreal Age classification (A1: <17, A2: 17-40, A3: >40)",
        example=28
    )
    
    crohns_location: Optional[Literal["L1_ileal", "L2_colonic", "L3_ileocolonic", "L4_upper_gi"]] = Field(
        None,
        description="Location of Crohn's disease. L1: Ileal, L2: Colonic, L3: Ileocolonic, L4: Upper GI. Required for Crohn's disease",
        example="L3_ileocolonic"
    )
    
    crohns_behavior: Optional[Literal["B1_inflammatory", "B2_stricturing", "B3_penetrating"]] = Field(
        None,
        description="Behavior pattern of Crohn's disease. B1: Inflammatory, B2: Stricturing, B3: Penetrating. Required for Crohn's disease",
        example="B1_inflammatory"
    )
    
    perianal_disease: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Presence of perianal disease modifier (p) for Crohn's disease. Can be added to any behavior pattern",
        example="no"
    )
    
    uc_extent: Optional[Literal["E1_proctitis", "E2_left_sided", "E3_extensive"]] = Field(
        None,
        description="Extent of ulcerative colitis. E1: Proctitis, E2: Left-sided colitis, E3: Extensive colitis. Required for UC",
        example="E2_left_sided"
    )
    
    uc_severity: Optional[Literal["S0_remission", "S1_mild", "S2_moderate", "S3_severe"]] = Field(
        None,
        description="Severity of ulcerative colitis. S0: Remission, S1: Mild, S2: Moderate, S3: Severe. Required for UC",
        example="S1_mild"
    )
    
    @validator('crohns_location', 'crohns_behavior', 'perianal_disease')
    def validate_crohns_fields(cls, v, values):
        """Validate that Crohn's disease fields are provided when disease_type is crohns_disease"""
        if 'disease_type' in values and values['disease_type'] == 'crohns_disease':
            if v is None and cls.__name__ in ['crohns_location', 'crohns_behavior']:
                raise ValueError(f"{cls.__name__} is required for Crohn's disease")
        return v
    
    @validator('uc_extent', 'uc_severity')
    def validate_uc_fields(cls, v, values):
        """Validate that UC fields are provided when disease_type is ulcerative_colitis"""
        if 'disease_type' in values and values['disease_type'] == 'ulcerative_colitis':
            if v is None:
                raise ValueError(f"{cls.__name__} is required for ulcerative colitis")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "disease_type": "crohns_disease",
                "age_at_diagnosis": 28,
                "crohns_location": "L3_ileocolonic",
                "crohns_behavior": "B1_inflammatory",
                "perianal_disease": "no",
                "uc_extent": None,
                "uc_severity": None
            }
        }


class MontrealClassificationIbdResponse(BaseModel):
    """
    Response model for Montreal Classification for Inflammatory Bowel Disease (IBD)
    
    The Montreal Classification provides a standardized code that characterizes IBD phenotype:
    
    For Crohn's Disease: A[age]L[location]B[behavior]p (if perianal disease present)
    - Example: A2L3B1 = Young adult onset, ileocolonic, inflammatory
    - Example: A1L1B3p = Pediatric onset, ileal, penetrating with perianal disease
    
    For Ulcerative Colitis: A[age]E[extent]S[severity]
    - Example: A2E2S1 = Young adult onset, left-sided colitis, mild activity
    - Example: A3E3S3 = Older adult onset, extensive colitis, severe activity
    
    Clinical Significance:
    - Standardizes IBD phenotyping for clinical management and research
    - Helps predict disease course and complications
    - Guides treatment intensity and surveillance strategies
    - Evolution of classification over time reflects disease progression
    - Essential for personalized IBD management approaches
    
    Prognostic Implications:
    - Pediatric onset (A1) often has more aggressive course
    - Crohn's behavior progresses from B1→B2→B3 over time
    - Extensive UC (E3) has highest colorectal cancer risk
    - Perianal disease (p modifier) indicates complex Crohn's disease
    
    Reference: Silverberg MS, et al. Can J Gastroenterol. 2005;19 Suppl A:5A-36A.
    """
    
    result: str = Field(
        ...,
        description="Complete Montreal Classification code (e.g., A2L3B1, A1E3S2)",
        example="A2L3B1"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the classification",
        example="Montreal Classification"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on the Montreal Classification",
        example="Montreal Classification A2L3B1. Ileocolonic disease has highest risk for surgical complications. Close monitoring needed. Inflammatory behavior may respond well to medical therapy. Monitor for disease progression. This classification helps predict disease course and guide therapeutic decisions."
    )
    
    stage: str = Field(
        ...,
        description="Disease classification category (Crohn's Disease Classification or Ulcerative Colitis Classification)",
        example="Crohn's Disease Classification"
    )
    
    stage_description: str = Field(
        ...,
        description="Detailed description of the classification components",
        example="Crohn's Disease: Young adult onset (17-40 years), Ileocolonic (terminal ileum + any colonic location), Inflammatory (non-stricturing, non-penetrating)"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "A2L3B1",
                "unit": "Montreal Classification",
                "interpretation": "Montreal Classification A2L3B1. Ileocolonic disease has highest risk for surgical complications. Close monitoring needed. Inflammatory behavior may respond well to medical therapy. Monitor for disease progression. This classification helps predict disease course and guide therapeutic decisions.",
                "stage": "Crohn's Disease Classification",
                "stage_description": "Crohn's Disease: Young adult onset (17-40 years), Ileocolonic (terminal ileum + any colonic location), Inflammatory (non-stricturing, non-penetrating)"
            }
        }