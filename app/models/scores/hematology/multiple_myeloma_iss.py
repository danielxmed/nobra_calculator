"""
Multiple Myeloma International Staging System (ISS) Models

Request and response models for Multiple Myeloma ISS staging calculation.

References (Vancouver style):
1. Greipp PR, San Miguel J, Durie BG, Crowley JJ, Barlogie B, Bladé J, et al. 
   International staging system for multiple myeloma. J Clin Oncol. 2005;23(15):3412-20. 
   doi: 10.1200/JCO.2005.04.242.
2. Durie BG, Salmon SE. A clinical staging system for multiple myeloma. Correlation of 
   measured myeloma cell mass with presenting clinical features, response to treatment, 
   and survival. Cancer. 1975;36(3):842-54. 
   doi: 10.1002/1097-0142(197509)36:3<842::aid-cncr2820360303>3.0.co;2-u.
3. Palumbo A, Avet-Loiseau H, Oliva S, Lokhorst HM, Goldschmidt H, Rosinol L, et al. 
   Revised International Staging System for Multiple Myeloma: A Report From International 
   Myeloma Working Group. J Clin Oncol. 2015;33(26):2863-9. doi: 10.1200/JCO.2015.61.2267.

The International Staging System (ISS) for multiple myeloma is a simple, reproducible 
staging system based on two readily available laboratory parameters: serum β2 microglobulin 
and serum albumin. Developed from a database of 10,750 patients, it provides superior 
prognostic information compared to the previous Durie-Salmon staging system.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MultipleMyelomaIssRequest(BaseModel):
    """
    Request model for Multiple Myeloma International Staging System (ISS)
    
    The ISS uses two laboratory parameters to stage newly diagnosed multiple myeloma:
    
    Serum β2 Microglobulin:
    - Reflects tumor burden and kidney function
    - Elevated levels indicate higher disease burden
    - Normal range: typically 1.0-2.4 mg/L
    - Levels ≥5.5 mg/L indicate Stage III disease
    
    Serum Albumin:
    - Reflects nutritional status and overall disease burden
    - Lower levels correlate with worse prognosis
    - Normal range: typically 3.5-5.0 g/dL
    - Levels <3.5 g/dL indicate more advanced disease
    
    ISS Staging Criteria:
    - Stage I: β2 microglobulin <3.5 mg/L AND albumin ≥3.5 g/dL
    - Stage II: Either (β2 microglobulin <3.5 mg/L AND albumin <3.5 g/dL) 
                OR (β2 microglobulin 3.5-5.4 mg/L regardless of albumin)
    - Stage III: β2 microglobulin ≥5.5 mg/L (regardless of albumin level)
    
    Clinical Applications:
    - Prognostic stratification at diagnosis
    - Treatment planning and intensity decisions
    - Patient counseling regarding expected outcomes
    - Clinical trial stratification
    - Research and epidemiological studies
    
    Validation and Performance:
    - Developed from 10,750 patients across multiple institutions
    - Validated across different geographic regions and populations
    - Superior to Durie-Salmon staging system
    - Simple, objective, and reproducible
    - Uses routinely available laboratory tests
    
    Important Limitations:
    - Only validated for newly diagnosed multiple myeloma
    - Not applicable to relapsed/refractory disease
    - Does not incorporate cytogenetic risk factors
    - Should be interpreted alongside other prognostic markers
    
    References (Vancouver style):
    1. Greipp PR, San Miguel J, Durie BG, Crowley JJ, Barlogie B, Bladé J, et al. 
    International staging system for multiple myeloma. J Clin Oncol. 2005;23(15):3412-20. 
    doi: 10.1200/JCO.2005.04.242.
    2. Durie BG, Salmon SE. A clinical staging system for multiple myeloma. Correlation of 
    measured myeloma cell mass with presenting clinical features, response to treatment, 
    and survival. Cancer. 1975;36(3):842-54. 
    doi: 10.1002/1097-0142(197509)36:3<842::aid-cncr2820360303>3.0.co;2-u.
    3. Palumbo A, Avet-Loiseau H, Oliva S, Lokhorst HM, Goldschmidt H, Rosinol L, et al. 
    Revised International Staging System for Multiple Myeloma: A Report From International 
    Myeloma Working Group. J Clin Oncol. 2015;33(26):2863-9. doi: 10.1200/JCO.2015.61.2267.
    """
    
    serum_beta2_microglobulin: float = Field(
        ...,
        ge=0.1,
        le=50.0,
        description="Serum β2 microglobulin level in mg/L. Reflects tumor burden and kidney function. Normal range typically 1.0-2.4 mg/L. Higher levels indicate more advanced disease",
        example=4.2
    )
    
    serum_albumin: float = Field(
        ...,
        ge=1.0,
        le=6.0,
        description="Serum albumin level in g/dL. Reflects nutritional status and disease burden. Normal range typically 3.5-5.0 g/dL. Lower levels correlate with worse prognosis",
        example=3.1
    )
    
    class Config:
        schema_extra = {
            "example": {
                "serum_beta2_microglobulin": 4.2,
                "serum_albumin": 3.1
            }
        }


class MultipleMyelomaIssResponse(BaseModel):
    """
    Response model for Multiple Myeloma International Staging System (ISS)
    
    The ISS provides three prognostic stages with distinct survival outcomes:
    
    Stage I (Best Prognosis):
    - Criteria: β2 microglobulin <3.5 mg/L AND albumin ≥3.5 g/dL
    - Median overall survival: 62 months
    - Represents patients with lowest tumor burden and best nutritional status
    - Typically respond well to standard treatment regimens
    - Best candidates for autologous stem cell transplantation
    
    Stage II (Intermediate Prognosis):
    - Criteria: Either (β2 microglobulin <3.5 mg/L AND albumin <3.5 g/dL) 
               OR (β2 microglobulin 3.5-5.4 mg/L regardless of albumin)
    - Median overall survival: 44 months
    - Intermediate tumor burden or compromised nutritional status
    - May benefit from intensified treatment approaches
    - Autologous stem cell transplant should be considered if eligible
    
    Stage III (Poorest Prognosis):
    - Criteria: β2 microglobulin ≥5.5 mg/L (regardless of albumin level)
    - Median overall survival: 29 months
    - Highest tumor burden and/or compromised kidney function
    - Requires aggressive treatment and intensive supportive care
    - May benefit from novel therapeutic approaches and clinical trials
    
    Clinical Management Implications:
    
    All Stages:
    - Complete staging workup including bone marrow biopsy and cytogenetics
    - Assessment of transplant eligibility based on age and comorbidities
    - Baseline imaging studies for bone disease evaluation
    - Regular monitoring of laboratory parameters during treatment
    
    Treatment Considerations:
    - Stage I: Standard induction therapy, consider transplant if eligible
    - Stage II: Standard to intensified therapy, transplant consideration
    - Stage III: Aggressive therapy, novel agents, clinical trial enrollment
    
    Follow-up Monitoring:
    - Regular assessment of β2 microglobulin and albumin levels
    - Monitor for disease progression and treatment response
    - Surveillance for treatment-related complications
    - Reassessment of staging parameters during follow-up
    
    Integration with Other Systems:
    - ISS should be combined with cytogenetic risk assessment
    - Consider Revised ISS (R-ISS) if genetic data available
    - Incorporate performance status and comorbidity assessment
    - Use alongside other prognostic markers (LDH, plasmacytosis degree)
    
    Reference: Greipp PR, et al. J Clin Oncol. 2005;23(15):3412-20.
    """
    
    result: str = Field(
        ...,
        description="ISS stage classification (Stage I, Stage II, or Stage III)",
        example="Stage II"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for staging system)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed prognostic interpretation with clinical management recommendations and survival data",
        example="ISS Stage II Multiple Myeloma: Either β2 microglobulin 4.2 mg/L (<3.5) with albumin 3.1 g/dL (<3.5), OR β2 microglobulin 3.5-5.4 mg/L (regardless of albumin level). PROGNOSIS: Intermediate prognostic group with median overall survival of 44 months. CLINICAL SIGNIFICANCE: Patients have moderate tumor burden or compromised nutritional status. Disease characteristics fall between Stage I and Stage III in terms of expected outcomes. MANAGEMENT RECOMMENDATIONS: Standard induction therapy with close monitoring for treatment response and toxicity. Autologous stem cell transplant should be considered if patient is eligible. May benefit from more intensive supportive care if albumin is low. Nutritional assessment and optimization may be beneficial. FOLLOW-UP: Close monitoring every 2-3 months during active treatment. Watch for progression to higher stage or development of complications."
    )
    
    stage: str = Field(
        ...,
        description="ISS stage designation (Stage I, Stage II, Stage III)",
        example="Stage II"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the prognostic category",
        example="Intermediate prognosis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Stage II",
                "unit": "",
                "interpretation": "ISS Stage II Multiple Myeloma: Either β2 microglobulin 4.2 mg/L (<3.5) with albumin 3.1 g/dL (<3.5), OR β2 microglobulin 3.5-5.4 mg/L (regardless of albumin level). PROGNOSIS: Intermediate prognostic group with median overall survival of 44 months. CLINICAL SIGNIFICANCE: Patients have moderate tumor burden or compromised nutritional status. Disease characteristics fall between Stage I and Stage III in terms of expected outcomes. MANAGEMENT RECOMMENDATIONS: Standard induction therapy with close monitoring for treatment response and toxicity. Autologous stem cell transplant should be considered if patient is eligible. May benefit from more intensive supportive care if albumin is low. Nutritional assessment and optimization may be beneficial. FOLLOW-UP: Close monitoring every 2-3 months during active treatment. Watch for progression to higher stage or development of complications.",
                "stage": "Stage II",
                "stage_description": "Intermediate prognosis"
            }
        }