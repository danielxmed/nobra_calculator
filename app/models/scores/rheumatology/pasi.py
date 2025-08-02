"""
Psoriasis Area and Severity Index (PASI) Models

Request and response models for PASI calculation.

References (Vancouver style):
1. Fredriksson T, Pettersson U. Severe psoriasis--oral therapy with a new retinoid. 
   Dermatologica. 1978;157(4):238-44. doi: 10.1159/000250839.
2. Langley RG, Ellis CN. Evaluating psoriasis with Psoriasis Area and Severity 
   Index, Psoriasis Global Assessment, and Lattice System Physician's Global 
   Assessment. J Am Acad Dermatol. 2004;51(4):563-9. doi: 10.1016/j.jaad.2004.04.012.
3. Schmitt J, Wozel G. The psoriasis area and severity index is the adequate 
   criterion to define severity in chronic plaque-type psoriasis. Dermatology. 
   2005;210(3):194-9. doi: 10.1159/000083509.
4. Puzenat E, Bronsard V, Prey S, Gourraud PA, Aractingi S, Bagot M, et al. 
   What are the best outcome measures for assessing plaque psoriasis severity? 
   A systematic review of the literature. J Eur Acad Dermatol Venereol. 
   2010;24 Suppl 2:10-6. doi: 10.1111/j.1468-3083.2009.03562.x.

The Psoriasis Area and Severity Index (PASI) is the gold standard tool for quantifying 
psoriasis severity in clinical practice and research. Developed by Fredriksson and 
Pettersson in 1978, PASI combines assessment of disease severity (erythema, induration, 
desquamation) with the extent of body surface area involvement across four anatomical 
regions (head/neck, upper limbs, trunk, lower limbs).

Clinical Applications:
- Baseline severity assessment for treatment planning
- Monitoring treatment response and disease progression
- Primary endpoint in clinical trials and research studies
- Determining eligibility for systemic therapies and biologics
- Quality improvement initiatives and comparative effectiveness research
- Regulatory approval studies for new psoriasis treatments

PASI Calculation Method:
The PASI score is calculated using the formula:
PASI = 0.1×(E_h+I_h+D_h)×A_h + 0.2×(E_a+I_a+D_a)×A_a + 0.3×(E_t+I_t+D_t)×A_t + 0.4×(E_l+I_l+D_l)×A_l

Where:
- E = Erythema (redness) severity (0-4)
- I = Induration (thickness/infiltration) severity (0-4)
- D = Desquamation (scaling) severity (0-4)
- A = Area involvement score (0-6)
- Subscripts: h=head/neck, a=arms, t=trunk, l=legs

Severity Scoring (0-4 scale):
- 0: None (no signs of psoriasis)
- 1: Slight (minimal, barely perceptible)
- 2: Moderate (clearly visible, moderate severity)
- 3: Severe (marked, pronounced severity)
- 4: Very severe (maximum severity possible)

Area Scoring (0-6 scale):
- 0: 0% of region affected
- 1: 1-9% of region affected
- 2: 10-29% of region affected
- 3: 30-49% of region affected
- 4: 50-69% of region affected
- 5: 70-89% of region affected
- 6: 90-100% of region affected

Body Surface Area Weights:
- Head/neck: 0.1 (represents 10% of total body surface area)
- Upper limbs: 0.2 (represents 20% of total body surface area)
- Trunk: 0.3 (represents 30% of total body surface area)
- Lower limbs: 0.4 (represents 40% of total body surface area)

Clinical Significance:
- Total PASI scores range from 0-72 (higher scores indicate more severe disease)
- PASI <5: Mild psoriasis (topical therapy typically adequate)
- PASI 5-10: Moderate psoriasis (phototherapy or systemic therapy consideration)
- PASI 10-20: Severe psoriasis (systemic therapy usually required)
- PASI >20: Very severe psoriasis (aggressive systemic treatment indicated)

Treatment Response Measures:
- PASI 50: 50% improvement from baseline (minimal response)
- PASI 75: 75% improvement from baseline (good response, clinical trial standard)
- PASI 90: 90% improvement from baseline (excellent response)
- PASI 100: 100% improvement (complete clearance)

Limitations and Considerations:
- Requires trained evaluator for consistent scoring
- Less sensitive for mild, localized psoriasis
- Does not assess nail involvement or quality of life impact
- May underestimate severity in darker skin due to erythema assessment challenges
- Inter-rater variability can occur without proper training
- Not applicable to non-plaque psoriasis variants (pustular, erythrodermic)

The PASI remains the most widely used and validated measure for psoriasis severity 
assessment, serving as the foundation for treatment decisions and research outcomes 
in dermatology practice worldwide.
"""

from pydantic import BaseModel, Field
from typing import Literal


class PasiRequest(BaseModel):
    """
    Request model for Psoriasis Area and Severity Index (PASI)
    
    PASI evaluates psoriasis severity across four body regions (head/neck, upper limbs, 
    trunk, lower limbs) by assessing three clinical features in each region:
    
    Clinical Features Assessment (0-4 scale for each):
    1. Erythema (Redness):
       - Assesses the intensity of red coloration in psoriatic lesions
       - Scored from 0 (no redness) to 4 (very severe, intense redness)
       - Can be challenging to assess in darker skin tones
    
    2. Induration (Thickness/Infiltration):
       - Evaluates the thickness and raised appearance of plaques
       - Scored from 0 (no elevation) to 4 (very thick, markedly elevated)
       - Best assessed by gentle palpation of lesion borders
    
    3. Desquamation (Scaling):
       - Measures the amount and thickness of scaling/flaking
       - Scored from 0 (no scaling) to 4 (very thick, abundant scaling)
       - May be reduced if patient recently bathed or applied topical treatments
    
    Area Assessment (0-6 scale):
    Percentage of each body region affected by psoriasis lesions:
    - 0: No involvement (0%)
    - 1: Minimal involvement (1-9%)
    - 2: Mild involvement (10-29%)
    - 3: Moderate involvement (30-49%)
    - 4: Extensive involvement (50-69%)
    - 5: Very extensive involvement (70-89%)
    - 6: Almost complete involvement (90-100%)
    
    Body Region Definitions:
    - Head/neck: Scalp, face, ears, neck (10% of total body surface area)
    - Upper limbs: Arms, forearms, hands (20% of total body surface area)
    - Trunk: Chest, abdomen, back, buttocks (30% of total body surface area)
    - Lower limbs: Thighs, legs, feet (40% of total body surface area)
    
    Assessment Guidelines:
    - Evaluate the most representative/average severity in each region
    - Consider the most severe lesions if heterogeneous presentation
    - Assess in good lighting conditions for accurate color evaluation
    - Document any factors that might influence scoring (recent treatments, lighting conditions)
    - Training and experience improve inter-rater reliability significantly
    
    References: See module docstring for complete citation list.
    """
    
    head_erythema: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Erythema (redness) severity in head/neck region. Score 0=none, 1=slight (barely perceptible), 2=moderate (clearly visible), 3=severe (marked intensity), 4=very severe (maximum possible redness).",
        example=2
    )
    
    head_induration: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Induration (thickness/elevation) severity in head/neck region. Score 0=none (flat), 1=slight elevation, 2=moderate thickness, 3=severe elevation, 4=very severe (markedly thick plaques).",
        example=2
    )
    
    head_desquamation: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Desquamation (scaling) severity in head/neck region. Score 0=none, 1=slight scaling, 2=moderate scaling, 3=severe (thick scales), 4=very severe (very thick, abundant scaling).",
        example=3
    )
    
    head_area: Literal[0, 1, 2, 3, 4, 5, 6] = Field(
        ...,
        description="Percentage of head/neck area affected by psoriasis. Score 0=0%, 1=1-9%, 2=10-29%, 3=30-49%, 4=50-69%, 5=70-89%, 6=90-100%.",
        example=1
    )
    
    arms_erythema: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Erythema (redness) severity in upper limbs/arms region. Score 0=none, 1=slight (barely perceptible), 2=moderate (clearly visible), 3=severe (marked intensity), 4=very severe (maximum possible redness).",
        example=1
    )
    
    arms_induration: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Induration (thickness/elevation) severity in upper limbs/arms region. Score 0=none (flat), 1=slight elevation, 2=moderate thickness, 3=severe elevation, 4=very severe (markedly thick plaques).",
        example=1
    )
    
    arms_desquamation: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Desquamation (scaling) severity in upper limbs/arms region. Score 0=none, 1=slight scaling, 2=moderate scaling, 3=severe (thick scales), 4=very severe (very thick, abundant scaling).",
        example=2
    )
    
    arms_area: Literal[0, 1, 2, 3, 4, 5, 6] = Field(
        ...,
        description="Percentage of upper limbs/arms area affected by psoriasis. Score 0=0%, 1=1-9%, 2=10-29%, 3=30-49%, 4=50-69%, 5=70-89%, 6=90-100%.",
        example=2
    )
    
    trunk_erythema: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Erythema (redness) severity in trunk region. Score 0=none, 1=slight (barely perceptible), 2=moderate (clearly visible), 3=severe (marked intensity), 4=very severe (maximum possible redness).",
        example=2
    )
    
    trunk_induration: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Induration (thickness/elevation) severity in trunk region. Score 0=none (flat), 1=slight elevation, 2=moderate thickness, 3=severe elevation, 4=very severe (markedly thick plaques).",
        example=3
    )
    
    trunk_desquamation: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Desquamation (scaling) severity in trunk region. Score 0=none, 1=slight scaling, 2=moderate scaling, 3=severe (thick scales), 4=very severe (very thick, abundant scaling).",
        example=2
    )
    
    trunk_area: Literal[0, 1, 2, 3, 4, 5, 6] = Field(
        ...,
        description="Percentage of trunk area affected by psoriasis. Score 0=0%, 1=1-9%, 2=10-29%, 3=30-49%, 4=50-69%, 5=70-89%, 6=90-100%.",
        example=3
    )
    
    legs_erythema: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Erythema (redness) severity in lower limbs/legs region. Score 0=none, 1=slight (barely perceptible), 2=moderate (clearly visible), 3=severe (marked intensity), 4=very severe (maximum possible redness).",
        example=1
    )
    
    legs_induration: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Induration (thickness/elevation) severity in lower limbs/legs region. Score 0=none (flat), 1=slight elevation, 2=moderate thickness, 3=severe elevation, 4=very severe (markedly thick plaques).",
        example=2
    )
    
    legs_desquamation: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Desquamation (scaling) severity in lower limbs/legs region. Score 0=none, 1=slight scaling, 2=moderate scaling, 3=severe (thick scales), 4=very severe (very thick, abundant scaling).",
        example=1
    )
    
    legs_area: Literal[0, 1, 2, 3, 4, 5, 6] = Field(
        ...,
        description="Percentage of lower limbs/legs area affected by psoriasis. Score 0=0%, 1=1-9%, 2=10-29%, 3=30-49%, 4=50-69%, 5=70-89%, 6=90-100%.",
        example=1
    )
    
    class Config:
        schema_extra = {
            "example": {
                "head_erythema": 2,
                "head_induration": 2,
                "head_desquamation": 3,
                "head_area": 1,
                "arms_erythema": 1,
                "arms_induration": 1,
                "arms_desquamation": 2,
                "arms_area": 2,
                "trunk_erythema": 2,
                "trunk_induration": 3,
                "trunk_desquamation": 2,
                "trunk_area": 3,
                "legs_erythema": 1,
                "legs_induration": 2,
                "legs_desquamation": 1,
                "legs_area": 1
            }
        }


class PasiResponse(BaseModel):
    """
    Response model for Psoriasis Area and Severity Index (PASI)
    
    The PASI score provides comprehensive assessment of psoriasis severity, guiding 
    treatment decisions and monitoring therapeutic response. Understanding PASI results 
    is crucial for optimal psoriasis management and patient care coordination.
    
    PASI Score Interpretation:
    
    Mild Psoriasis (PASI <5):
    - Limited disease burden with minimal functional impact
    - Topical treatments usually adequate (corticosteroids, vitamin D analogues, calcineurin inhibitors)
    - Lifestyle modifications and patient education important
    - Regular monitoring for disease progression
    - Generally does not qualify for systemic therapies
    
    Moderate Psoriasis (PASI 5-10):
    - Significant disease burden affecting quality of life
    - Consider phototherapy (narrowband UV-B therapy)
    - Evaluate for systemic conventional therapies (methotrexate, cyclosporine, acitretin)
    - May qualify for biologic therapy depending on other factors
    - Regular dermatology follow-up recommended
    
    Severe Psoriasis (PASI 10-20):
    - Substantial disease burden with significant impact on quality of life
    - Systemic therapy typically required (biologics preferred)
    - Consider TNF-α inhibitors, IL-17 inhibitors, or IL-23 inhibitors
    - May require combination therapy for optimal control
    - Screen for psoriatic arthritis and comorbidities
    - Multidisciplinary care approach recommended
    
    Very Severe Psoriasis (PASI >20):
    - Extensive disease with major impact on physical and psychological well-being
    - Aggressive systemic treatment required (biologics first-line)
    - Consider hospitalization for erythrodermic or unstable disease
    - Urgent dermatology referral if not already under specialist care
    - Address comorbidities (cardiovascular disease, metabolic syndrome, depression)
    - Psychosocial support and patient advocacy resources important
    
    Treatment Response Monitoring:
    - PASI 50: Minimal meaningful improvement (50% reduction from baseline)
    - PASI 75: Good therapeutic response (75% reduction, clinical trial standard)
    - PASI 90: Excellent response (90% reduction, near-complete clearance)
    - PASI 100: Complete clearance (no visible psoriatic lesions)
    
    Clinical Decision Points:
    - PASI ≥10 often used as threshold for systemic therapy eligibility
    - PASI improvement of ≥75% considered successful treatment response
    - Failure to achieve PASI 50 by 12-16 weeks may indicate need for treatment change
    - PASI 75 response typically required for continued biologic therapy coverage
    
    Additional Considerations:
    - PASI should be interpreted alongside body surface area (BSA) and quality of life measures
    - Localized severe disease may have low PASI but high impact (e.g., genital, palmoplantar)
    - Patient-reported outcomes and functional assessment complement PASI scoring
    - Regular reassessment recommended to monitor treatment response and adjust therapy
    
    The PASI score serves as the foundation for evidence-based psoriasis treatment 
    decisions and remains the gold standard for severity assessment in clinical practice.
    
    Reference: See module docstring for complete citation list.
    """
    
    result: float = Field(
        ...,
        description="PASI score calculated from clinical assessment across four body regions. Range 0-72 points, with higher scores indicating more severe psoriasis. Most patients score <20 even with extensive disease.",
        example=8.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the PASI score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including severity classification, treatment recommendations, monitoring guidance, and quality of life considerations based on the calculated PASI score.",
        example="Moderate psoriasis requiring active treatment consideration. Evaluate for phototherapy (narrowband UV-B), systemic conventional therapy (methotrexate, cyclosporine), or biologic therapy based on patient factors, treatment response, and quality of life impact. Regular monitoring with dermatology follow-up and adjustment of therapy may be needed. Consider combination treatments for optimal outcomes."
    )
    
    stage: str = Field(
        ...,
        description="Psoriasis severity classification based on PASI score (Mild, Moderate, Severe, Very Severe)",
        example="Moderate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the psoriasis severity level",
        example="Moderate psoriasis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 8.5,
                "unit": "points",
                "interpretation": "Moderate psoriasis requiring active treatment consideration. Evaluate for phototherapy (narrowband UV-B), systemic conventional therapy (methotrexate, cyclosporine), or biologic therapy based on patient factors, treatment response, and quality of life impact. Regular monitoring with dermatology follow-up and adjustment of therapy may be needed. Consider combination treatments for optimal outcomes.",
                "stage": "Moderate",
                "stage_description": "Moderate psoriasis"
            }
        }