"""
Eczema Area and Severity Index (EASI) Models

Request and response models for EASI calculation.

References (Vancouver style):
1. Hanifin JM, Thurston M, Omoto M, Cherill R, Tofte SJ, Graeber M. The eczema area 
   and severity index (EASI): assessment of reliability in atopic dermatitis. EASI 
   Evaluator Group. Exp Dermatol. 2001;10(1):11-8. doi: 10.1034/j.1600-0625.2001.100102.x.
2. Schmitt J, Langan S, Deckert S, Svensson A, von Kobyletzki L, Thomas K, et al. 
   Assessment of clinical signs of atopic dermatitis: a systematic review and 
   recommendation. J Allergy Clin Immunol. 2013;132(6):1337-47. doi: 10.1016/j.jaci.2013.07.008.
3. Barbarot S, Auziere S, Gadkari A, Girolomoni G, Puig L, Simpson EL, et al. 
   Epidemiology of atopic dermatitis in adults: Results from an international survey. 
   Allergy. 2018;73(6):1284-1293. doi: 10.1111/all.13401.
4. Silverberg JI, Paller AS, Fishbein AB, Kaplan DH, Simpson EL. Eczema prevalence, 
   severity and impact in the United States. Dermatitis. 2019;30(1):66-72. 
   doi: 10.1097/DER.0000000000000408.

The EASI is the most validated and widely used assessment tool for atopic dermatitis 
severity in clinical practice and research. It assesses eczema severity across four 
body regions (head/neck, upper extremities, trunk, lower extremities) by evaluating 
both area involvement (0-6 scale) and four severity signs (0-3 scale each): erythema, 
edema/papulation, excoriation, and lichenification. The total score ranges from 0 to 72 points.
"""

from pydantic import BaseModel, Field
from typing import Literal


class EczemaAreaSeverityIndexRequest(BaseModel):
    """
    Request model for Eczema Area and Severity Index (EASI)
    
    The EASI evaluates atopic dermatitis severity by assessing four body regions and 
    four severity signs in each region. Assessment requires approximately 6 minutes 
    when performed by a trained investigator.
    
    Body Regions Assessed:
    1. Head and Neck: Face, scalp, neck area
    2. Upper Extremities: Arms, hands (excluding trunk areas)
    3. Trunk: Chest, back, abdomen (includes axilla and groin)
    4. Lower Extremities: Legs, feet, buttocks
    
    Area Involvement Scoring (0-6 scale for each region):
    - 0: 0% involvement (no lesions in this region)
    - 1: 1-9% involvement (minimal lesions)
    - 2: 10-29% involvement (limited lesions)
    - 3: 30-49% involvement (moderate lesions)
    - 4: 50-69% involvement (extensive lesions)
    - 5: 70-89% involvement (very extensive lesions)
    - 6: 90-100% involvement (near-complete involvement)
    
    Severity Signs Assessed (0-3 scale for each sign in each region):
    
    1. Erythema (Redness):
    - 0: Absent (no redness)
    - 1: Mild (light pink/red)
    - 2: Moderate (definite red)
    - 3: Severe (deep/dark red)
    * Important: Consider underlying skin pigmentation - may need to increase score 
      by 1 grade in patients with darker skin to avoid underestimation
    
    2. Edema/Papulation (Swelling/Bumps):
    - 0: Absent (no swelling or bumps)
    - 1: Mild (just detectable elevation)
    - 2: Moderate (clearly elevated lesions)
    - 3: Severe (marked elevation with significant papules/plaques)
    
    3. Excoriation (Scratching Marks):
    - 0: Absent (no scratch marks)
    - 1: Mild (few superficial scratch marks)
    - 2: Moderate (multiple scratch marks, some deeper)
    - 3: Severe (extensive deep scratching, possible secondary infection)
    
    4. Lichenification (Skin Thickening):
    - 0: Absent (normal skin texture)
    - 1: Mild (slight thickening)
    - 2: Moderate (definite thickening with accentuated skin markings)
    - 3: Severe (marked thickening with very prominent skin markings)
    
    Age-Based Regional Multipliers:
    - Children (0-7 years): Head/neck = 0.2, Upper extremities = 0.2, Trunk = 0.3, Lower extremities = 0.4
    - Adults (8+ years): Head/neck = 0.1, Upper extremities = 0.2, Trunk = 0.3, Lower extremities = 0.4
    
    Calculation Formula:
    Regional Score = (Sum of 4 severity signs) × Area score × Regional multiplier
    Total EASI = Sum of all 4 regional scores (Range: 0-72 points)
    
    Clinical Interpretation:
    - 0: Clear (no eczema)
    - 0.1-1.0: Almost clear
    - 1.1-7.0: Mild eczema
    - 7.1-21.0: Moderate eczema  
    - 21.1-50.0: Severe eczema
    - 50.1-72.0: Very severe eczema
    
    Assessment Considerations:
    - Perform in good lighting for accurate erythema assessment
    - EASI should be completed independently of previous assessments (static tool)
    - Does not assess dryness or scaling (limitation of the tool)
    - Higher scores correlate with increased pruritus, sleep disturbance, and QoL impairment
    - Recommended primary endpoint for clinical trials in atopic dermatitis
    
    References (Vancouver style):
    1. Hanifin JM, Thurston M, Omoto M, Cherill R, Tofte SJ, Graeber M. The eczema area 
       and severity index (EASI): assessment of reliability in atopic dermatitis. EASI 
       Evaluator Group. Exp Dermatol. 2001;10(1):11-8.
    2. Schmitt J, Langan S, Deckert S, Svensson A, von Kobyletzki L, Thomas K, et al. 
       Assessment of clinical signs of atopic dermatitis: a systematic review and 
       recommendation. J Allergy Clin Immunol. 2013;132(6):1337-47.
    """
    
    age_category: Literal["child_0_7", "adult_8_plus"] = Field(
        ...,
        description="Patient age category for regional multiplier calculation. Children (0-7 years) have different head/neck multiplier (0.2 vs 0.1)",
        example="adult_8_plus"
    )
    
    # Head and Neck Region
    head_neck_area: int = Field(
        ...,
        ge=0, le=6,
        description="Head and neck area involvement (0=0%, 1=1-9%, 2=10-29%, 3=30-49%, 4=50-69%, 5=70-89%, 6=90-100%)",
        example=2
    )
    
    head_neck_erythema: int = Field(
        ...,
        ge=0, le=3,
        description="Head and neck erythema severity (0=absent, 1=mild, 2=moderate, 3=severe). Consider skin pigmentation - may need higher score in darker skin",
        example=2
    )
    
    head_neck_edema: int = Field(
        ...,
        ge=0, le=3,
        description="Head and neck edema/papulation severity (0=absent, 1=mild, 2=moderate, 3=severe)",
        example=1
    )
    
    head_neck_excoriation: int = Field(
        ...,
        ge=0, le=3,
        description="Head and neck excoriation severity (0=absent, 1=mild, 2=moderate, 3=severe)",
        example=1
    )
    
    head_neck_lichenification: int = Field(
        ...,
        ge=0, le=3,
        description="Head and neck lichenification severity (0=absent, 1=mild, 2=moderate, 3=severe)",
        example=0
    )
    
    # Upper Extremities Region
    upper_extremities_area: int = Field(
        ...,
        ge=0, le=6,
        description="Upper extremities area involvement (0=0%, 1=1-9%, 2=10-29%, 3=30-49%, 4=50-69%, 5=70-89%, 6=90-100%)",
        example=3
    )
    
    upper_extremities_erythema: int = Field(
        ...,
        ge=0, le=3,
        description="Upper extremities erythema severity (0=absent, 1=mild, 2=moderate, 3=severe)",
        example=2
    )
    
    upper_extremities_edema: int = Field(
        ...,
        ge=0, le=3,
        description="Upper extremities edema/papulation severity (0=absent, 1=mild, 2=moderate, 3=severe)",
        example=2
    )
    
    upper_extremities_excoriation: int = Field(
        ...,
        ge=0, le=3,
        description="Upper extremities excoriation severity (0=absent, 1=mild, 2=moderate, 3=severe)",
        example=2
    )
    
    upper_extremities_lichenification: int = Field(
        ...,
        ge=0, le=3,
        description="Upper extremities lichenification severity (0=absent, 1=mild, 2=moderate, 3=severe)",
        example=1
    )
    
    # Trunk Region
    trunk_area: int = Field(
        ...,
        ge=0, le=6,
        description="Trunk area involvement including axilla and groin (0=0%, 1=1-9%, 2=10-29%, 3=30-49%, 4=50-69%, 5=70-89%, 6=90-100%)",
        example=2
    )
    
    trunk_erythema: int = Field(
        ...,
        ge=0, le=3,
        description="Trunk erythema severity (0=absent, 1=mild, 2=moderate, 3=severe)",
        example=1
    )
    
    trunk_edema: int = Field(
        ...,
        ge=0, le=3,
        description="Trunk edema/papulation severity (0=absent, 1=mild, 2=moderate, 3=severe)",
        example=1
    )
    
    trunk_excoriation: int = Field(
        ...,
        ge=0, le=3,
        description="Trunk excoriation severity (0=absent, 1=mild, 2=moderate, 3=severe)",
        example=0
    )
    
    trunk_lichenification: int = Field(
        ...,
        ge=0, le=3,
        description="Trunk lichenification severity (0=absent, 1=mild, 2=moderate, 3=severe)",
        example=0
    )
    
    # Lower Extremities Region
    lower_extremities_area: int = Field(
        ...,
        ge=0, le=6,
        description="Lower extremities area involvement including feet and buttocks (0=0%, 1=1-9%, 2=10-29%, 3=30-49%, 4=50-69%, 5=70-89%, 6=90-100%)",
        example=4
    )
    
    lower_extremities_erythema: int = Field(
        ...,
        ge=0, le=3,
        description="Lower extremities erythema severity (0=absent, 1=mild, 2=moderate, 3=severe)",
        example=3
    )
    
    lower_extremities_edema: int = Field(
        ...,
        ge=0, le=3,
        description="Lower extremities edema/papulation severity (0=absent, 1=mild, 2=moderate, 3=severe)",
        example=2
    )
    
    lower_extremities_excoriation: int = Field(
        ...,
        ge=0, le=3,
        description="Lower extremities excoriation severity (0=absent, 1=mild, 2=moderate, 3=severe)",
        example=3
    )
    
    lower_extremities_lichenification: int = Field(
        ...,
        ge=0, le=3,
        description="Lower extremities lichenification severity (0=absent, 1=mild, 2=moderate, 3=severe)",
        example=2
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age_category": "adult_8_plus",
                "head_neck_area": 2,
                "head_neck_erythema": 2,
                "head_neck_edema": 1,
                "head_neck_excoriation": 1,
                "head_neck_lichenification": 0,
                "upper_extremities_area": 3,
                "upper_extremities_erythema": 2,
                "upper_extremities_edema": 2,
                "upper_extremities_excoriation": 2,
                "upper_extremities_lichenification": 1,
                "trunk_area": 2,
                "trunk_erythema": 1,
                "trunk_edema": 1,
                "trunk_excoriation": 0,
                "trunk_lichenification": 0,
                "lower_extremities_area": 4,
                "lower_extremities_erythema": 3,
                "lower_extremities_edema": 2,
                "lower_extremities_excoriation": 3,
                "lower_extremities_lichenification": 2
            }
        }


class EczemaAreaSeverityIndexResponse(BaseModel):
    """
    Response model for Eczema Area and Severity Index (EASI)
    
    The EASI score ranges from 0 to 72 points and provides validated severity categories 
    with corresponding treatment recommendations:
    
    Severity Categories and Clinical Management:
    
    Clear (0 points):
    - No active eczema lesions present
    - Continue maintenance skincare routine with regular moisturizing
    - Environmental management to prevent flares
    - No active treatment needed, focus on prevention
    
    Almost Clear (0.1-1.0 points):
    - Minimal residual signs of atopic dermatitis
    - Continue current effective treatment regimen
    - Monitor for improvement or potential relapse
    - Maintain consistent skincare routine and trigger avoidance
    
    Mild (1.1-7.0 points):
    - Limited eczema involvement with mild severity signs
    - First-line treatment: Regular moisturizers (at least twice daily)
    - Low-potency topical corticosteroids (Class VI-VII) for active lesions
    - Trigger identification and avoidance strategies
    - Gentle skincare practices and barrier repair focus
    
    Moderate (7.1-21.0 points):
    - More extensive involvement or moderate severity signs
    - Medium-potency topical corticosteroids (Class III-V) may be needed
    - Consider topical calcineurin inhibitors for maintenance
    - May require systemic therapy if topical treatments inadequate
    - Specialist dermatology referral if not responding to initial treatment
    - Address psychosocial impact (sleep, quality of life)
    
    Severe (21.1-50.0 points):
    - Extensive involvement or severe signs requiring intensive treatment
    - High-potency topical corticosteroids (Class I-II) for acute flares
    - Topical calcineurin inhibitors for long-term maintenance
    - Consider systemic immunosuppressants (cyclosporine, methotrexate)
    - Biologic therapy evaluation (dupilumab, tralokinumab)
    - Dermatology consultation strongly recommended
    - Assess for secondary bacterial infections
    
    Very Severe (50.1-72.0 points):
    - Extensive severe disease requiring aggressive multimodal treatment
    - Systemic immunosuppressants often necessary
    - Biologic therapy (dupilumab first-line for moderate-to-severe AD)
    - Specialist dermatology management essential
    - Comprehensive quality of life assessment and support
    - Consider psychological counseling for coping strategies
    - Hospitalization may be needed for severe complications
    
    Treatment Principles Across All Severities:
    - Maintain skin barrier with regular moisturizing (2-3 times daily)
    - Identify and avoid personal triggers (allergens, irritants, stress)
    - Use gentle, fragrance-free skincare products
    - Consider wet wrap therapy for severe flares
    - Address itch-scratch cycle with appropriate antihistamines
    - Patient and family education on disease management
    - Regular follow-up to monitor treatment response and adjust therapy
    
    EASI Clinical Utility:
    - Validated primary endpoint for clinical trials
    - Substantial inter-rater reliability (κ = 0.75)
    - Correlates with patient-reported outcomes (pruritus, sleep, QoL)
    - Useful for monitoring treatment response over time
    - Takes approximately 6 minutes to complete when properly trained
    
    Limitations to Consider:
    - Does not assess dryness or scaling (common AD features)
    - May underestimate erythema in patients with darker skin
    - Static assessment tool - should be completed independently each time
    - Requires training for reliable and consistent scoring
    - Does not capture patient-reported symptoms directly
    
    Reference: Hanifin JM, et al. Exp Dermatol. 2001;10(1):11-8.
    """
    
    result: float = Field(
        ...,
        description="EASI total score calculated from all body regions (range: 0-72 points)",
        example=12.4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the EASI score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and treatment recommendations based on EASI severity category",
        example="Moderate atopic dermatitis. Consider medium-potency topical corticosteroids (Class III-V), topical calcineurin inhibitors, or systemic therapy if topical treatments are inadequate. May require specialist referral."
    )
    
    stage: str = Field(
        ...,
        description="EASI severity category (Clear, Almost Clear, Mild, Moderate, Severe, Very Severe)",
        example="Moderate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the eczema severity level",
        example="Moderate eczema"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 12.4,
                "unit": "points",
                "interpretation": "Moderate atopic dermatitis. Consider medium-potency topical corticosteroids (Class III-V), topical calcineurin inhibitors, or systemic therapy if topical treatments are inadequate. May require specialist referral.",
                "stage": "Moderate",
                "stage_description": "Moderate eczema"
            }
        }